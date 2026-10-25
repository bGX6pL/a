"""Export the project database to other database engines and interchange formats.

    uv run python -m investordb.export                                 # every format
    uv run python -m investordb.export --format sqlite,parquet --schemas ref,core
    uv run python -m investordb.export --verify                        # re-read exports, compare row counts

Output goes to exports/<UTC timestamp>/<format>/, each with a manifest.json of row counts and
SHA-256 hashes. By default the curated schemas (core, ref, meta) are exported; raw is left out
because the fetch scripts can rebuild it, but --schemas raw,... includes it.

Formats
    pgdump   pg_dump custom archive; restore with pg_restore into PostgreSQL 16+
    pgsql    plain PostgreSQL SQL script (psql -f)
    csv      one UTF-8 CSV per table + schema.json; NULL is an empty unquoted field,
             arrays and JSON are JSON text
    jsonl    one JSON Lines file per table + schema.json (MongoDB, Elasticsearch, BigQuery)
    parquet  one Parquet file per table (DuckDB, Spark, Snowflake, BigQuery, ClickHouse, pandas)
    sqlite   one SQLite database file; tables are named schema__table
    duckdb   one DuckDB database file with native types, schemas and constraints
    mysql    MySQL 8 / MariaDB 10.5+ script: DDL + INSERTs; tables are named schema__table
    mssql    SQL Server 2017+ T-SQL script: DDL + INSERTs into matching schemas
"""

import argparse
import csv
import datetime as dt
import decimal
import hashlib
import json
import os
import sqlite3
import subprocess
import sys
import uuid
from dataclasses import dataclass, field
from pathlib import Path

import duckdb
import pyarrow as pa
import pyarrow.parquet as pq
from psycopg import sql

from investordb.db import PROJECT_ROOT, connect, credentials, pg_tool

DEFAULT_SCHEMAS = ["core", "ref", "meta"]
FORMATS = ["pgdump", "pgsql", "csv", "jsonl", "parquet", "sqlite", "duckdb", "mysql", "mssql"]
UNCONSTRAINED_DECIMAL = (38, 10)  # used where the target needs a fixed precision
INSERT_BATCH = 500

# Postgres type name -> portable kind. Anything else is exported as text.
SCALAR_KINDS = {
    "int2": "integer", "int4": "integer", "int8": "bigint",
    "numeric": "decimal", "float4": "double", "float8": "double",
    "bool": "boolean",
    "text": "text", "varchar": "text", "bpchar": "text", "name": "text", "citext": "text",
    "date": "date", "timestamp": "timestamp", "timestamptz": "timestamptz",
    "uuid": "uuid", "json": "json", "jsonb": "json", "bytea": "binary",
}


@dataclass
class Column:
    name: str
    pg_type: str  # format_type() text, e.g. numeric(20,2) or text[]
    kind: str  # one of SCALAR_KINDS values, or "array"
    nullable: bool
    precision: int | None = None
    scale: int | None = None
    length: int | None = None
    elem: str | None = None  # element kind of an array
    cast_to_text: bool = False  # type with no portable kind


@dataclass
class Table:
    schema: str
    name: str
    columns: list[Column]
    primary_key: list[str] = field(default_factory=list)
    uniques: list[tuple[str, list[str]]] = field(default_factory=list)
    foreign_keys: list[dict] = field(default_factory=list)
    rows: list[tuple] = field(default_factory=list)

    @property
    def qualified(self) -> str:
        return f"{self.schema}.{self.name}"

    @property
    def flat(self) -> str:
        return f"{self.schema}__{self.name}"

    def key_columns(self) -> set[str]:
        cols = set(self.primary_key)
        for _, unique_cols in self.uniques:
            cols.update(unique_cols)
        for fk in self.foreign_keys:
            cols.update(fk["columns"])
        return cols

    def max_text_length(self, column: str) -> int:
        i = [c.name for c in self.columns].index(column)
        return max((len(str(r[i])) for r in self.rows if r[i] is not None), default=0)


# --------------------------------------------------------------------------- introspection

COLUMNS_SQL = """
select n.nspname, c.relname, a.attname, not a.attnotnull, format_type(a.atttypid, a.atttypmod),
       case when t.typcategory = 'A' then et.typname else t.typname end,
       t.typcategory = 'A', a.atttypmod
from pg_class c
join pg_namespace n on n.oid = c.relnamespace
join pg_attribute a on a.attrelid = c.oid and a.attnum > 0 and not a.attisdropped
join pg_type t on t.oid = a.atttypid
left join pg_type et on et.oid = t.typelem
where c.relkind in ('r', 'p') and not c.relispartition and n.nspname = any(%s)
order by n.nspname, c.relname, a.attnum
"""

CONSTRAINTS_SQL = """
select n.nspname, c.relname, con.conname, con.contype,
       (select array_agg(a.attname order by k.ord) from unnest(con.conkey) with ordinality k(attnum, ord)
          join pg_attribute a on a.attrelid = con.conrelid and a.attnum = k.attnum),
       fn.nspname, fc.relname,
       (select array_agg(a.attname order by k.ord) from unnest(con.confkey) with ordinality k(attnum, ord)
          join pg_attribute a on a.attrelid = con.confrelid and a.attnum = k.attnum)
from pg_constraint con
join pg_class c on c.oid = con.conrelid
join pg_namespace n on n.oid = c.relnamespace
left join pg_class fc on fc.oid = con.confrelid
left join pg_namespace fn on fn.oid = fc.relnamespace
where con.contype in ('p', 'u', 'f') and n.nspname = any(%s)
order by n.nspname, c.relname, con.conname
"""


def make_column(name: str, nullable: bool, pg_type: str, typname: str, is_array: bool, typmod: int) -> Column:
    kind = SCALAR_KINDS.get(typname)
    col = Column(name, pg_type, "array" if is_array else (kind or "text"), nullable, cast_to_text=kind is None)
    if is_array:
        col.elem = kind or "text"
    if typname == "numeric" and typmod >= 4:
        col.precision, col.scale = ((typmod - 4) >> 16) & 0xFFFF, (typmod - 4) & 0xFFFF
    elif typname in ("varchar", "bpchar") and typmod >= 4:
        col.length = typmod - 4
    return col


def load_tables(conn, schemas: list[str]) -> list[Table]:
    tables: dict[str, Table] = {}
    for schema, table, *col_info in conn.execute(COLUMNS_SQL, (schemas,)).fetchall():
        key = f"{schema}.{table}"
        tables.setdefault(key, Table(schema, table, [])).columns.append(make_column(*col_info))

    for schema, table, name, kind, cols, ref_schema, ref_table, ref_cols in conn.execute(
        CONSTRAINTS_SQL, (schemas,)
    ).fetchall():
        t = tables[f"{schema}.{table}"]
        if kind == "p":
            t.primary_key = cols
        elif kind == "u":
            t.uniques.append((name, cols))
        elif f"{ref_schema}.{ref_table}" in tables:
            t.foreign_keys.append(
                {"name": name, "columns": cols, "ref_schema": ref_schema, "ref_table": ref_table, "ref_columns": ref_cols}
            )
        else:
            print(f"  note: FK {name} on {schema}.{table} points outside the exported schemas; dropped")

    for t in tables.values():
        select_list = [
            sql.SQL("{}::text{}").format(sql.Identifier(c.name), sql.SQL("[]" if c.kind == "array" else ""))
            if c.cast_to_text
            else sql.Identifier(c.name)
            for c in t.columns
        ]
        order = t.primary_key or [c.name for c in t.columns if c.kind not in ("json", "array", "binary")]
        query = sql.SQL("select {} from {}.{}").format(
            sql.SQL(", ").join(select_list), sql.Identifier(t.schema), sql.Identifier(t.name)
        )
        if order:
            query += sql.SQL(" order by {}").format(sql.SQL(", ").join(map(sql.Identifier, order)))
        t.rows = conn.execute(query).fetchall()
    return topo_sort(list(tables.values()))


def topo_sort(tables: list[Table]) -> list[Table]:
    """Order tables so that every FK target comes before the table referencing it."""
    by_name = {t.qualified: t for t in tables}
    ordered, done = [], set()

    def visit(t: Table, path: tuple[str, ...]) -> None:
        if t.qualified in done:
            return
        for fk in t.foreign_keys:
            target = f"{fk['ref_schema']}.{fk['ref_table']}"
            if target != t.qualified and target not in path:
                visit(by_name[target], path + (t.qualified,))
        done.add(t.qualified)
        ordered.append(t)

    for t in tables:
        visit(t, ())
    return ordered


# --------------------------------------------------------------------------- value helpers


def _json_default(v):
    if isinstance(v, decimal.Decimal):
        return int(v) if v == v.to_integral_value() else float(v)
    if isinstance(v, dt.datetime):
        return utc_iso(v)
    if isinstance(v, (dt.date, uuid.UUID)):
        return str(v)
    if isinstance(v, (bytes, memoryview)):
        return bytes(v).hex()
    raise TypeError(f"not JSON serializable: {type(v)}")


def to_json_text(v) -> str:
    return json.dumps(v, ensure_ascii=False, default=_json_default)


def utc_iso(v: dt.datetime) -> str:
    return (v.astimezone(dt.timezone.utc) if v.tzinfo else v).isoformat()


def text_value(v, col: Column):
    """Value as a string for CSV / SQL literals; None stays None."""
    if v is None:
        return None
    if col.kind in ("json", "array"):
        return to_json_text(v)
    if isinstance(v, bool):
        return "true" if v else "false"
    if isinstance(v, dt.datetime):
        return utc_iso(v)
    if isinstance(v, (bytes, memoryview)):
        return bytes(v).hex()
    return str(v)


def json_value(v, col: Column):
    if v is None or col.kind == "json":
        return v
    return json.loads(to_json_text(v))


def file_sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def schema_doc(tables: list[Table]) -> dict:
    return {
        t.qualified: {
            "columns": [
                {"name": c.name, "postgres_type": c.pg_type, "kind": c.kind, "element_kind": c.elem, "nullable": c.nullable}
                for c in t.columns
            ],
            "primary_key": t.primary_key,
            "unique": [cols for _, cols in t.uniques],
            "foreign_keys": t.foreign_keys,
            "rows": len(t.rows),
        }
        for t in tables
    }


# --------------------------------------------------------------------------- PostgreSQL native


def export_pg(fmt: str, out: Path, schemas: list[str], tables: list[Table]) -> None:
    c = credentials()
    target = out / ("investor_db.dump" if fmt == "pgdump" else "investor_db.sql")
    args = [pg_tool("pg_dump"), "-h", c["host"], "-p", c["port"], "-U", c["user"], "-d", c["dbname"],
            "--no-owner", "--no-privileges", "-F", "c" if fmt == "pgdump" else "p", "-f", str(target)]
    for s in schemas:
        args += ["-n", s]
    subprocess.run(args, check=True, env={**os.environ, "PGPASSWORD": c["password"]})


# --------------------------------------------------------------------------- CSV / JSONL / Parquet


def export_csv(out: Path, tables: list[Table]) -> None:
    for t in tables:
        with (out / f"{t.qualified}.csv").open("w", encoding="utf-8", newline="") as f:
            w = csv.writer(f, quoting=csv.QUOTE_NOTNULL)
            w.writerow([c.name for c in t.columns])
            for r in t.rows:
                w.writerow([text_value(v, c) for v, c in zip(r, t.columns)])
    (out / "schema.json").write_text(json.dumps(schema_doc(tables), indent=2), encoding="utf-8")


def export_jsonl(out: Path, tables: list[Table]) -> None:
    for t in tables:
        with (out / f"{t.qualified}.jsonl").open("w", encoding="utf-8") as f:
            for r in t.rows:
                doc = {c.name: json_value(v, c) for v, c in zip(r, t.columns)}
                f.write(json.dumps(doc, ensure_ascii=False, default=_json_default) + "\n")
    (out / "schema.json").write_text(json.dumps(schema_doc(tables), indent=2), encoding="utf-8")


def _arrow_type(kind: str, col: Column) -> pa.DataType:
    if kind == "decimal":
        p, s = (col.precision, col.scale) if col.precision else UNCONSTRAINED_DECIMAL
        return pa.decimal128(p, s)
    return {
        "integer": pa.int32(), "bigint": pa.int64(), "double": pa.float64(), "boolean": pa.bool_(),
        "date": pa.date32(), "timestamp": pa.timestamp("us"), "timestamptz": pa.timestamp("us", tz="UTC"),
        "binary": pa.binary(),
    }.get(kind, pa.string())


def _arrow_value(v, kind: str, col: Column):
    if v is None:
        return None
    if kind == "json":
        return to_json_text(v)
    if kind == "uuid":
        return str(v)
    if kind == "decimal" and not col.precision:
        return v.quantize(decimal.Decimal(1).scaleb(-UNCONSTRAINED_DECIMAL[1]))
    if kind == "binary":
        return bytes(v)
    return v


def arrow_table(t: Table) -> pa.Table:
    arrays, fields = [], []
    for i, c in enumerate(t.columns):
        if c.kind == "array":
            typ = pa.list_(_arrow_type(c.elem, c))
            values = [None if r[i] is None else [_arrow_value(e, c.elem, c) for e in r[i]] for r in t.rows]
        else:
            typ = _arrow_type(c.kind, c)
            values = [_arrow_value(r[i], c.kind, c) for r in t.rows]
        arrays.append(pa.array(values, type=typ))
        fields.append(pa.field(c.name, typ, nullable=c.nullable))
    return pa.Table.from_arrays(arrays, schema=pa.schema(fields))


def export_parquet(out: Path, tables: list[Table]) -> None:
    for t in tables:
        pq.write_table(arrow_table(t), out / f"{t.qualified}.parquet", compression="zstd")


# --------------------------------------------------------------------------- SQLite / DuckDB

SQLITE_TYPES = {"integer": "INTEGER", "bigint": "INTEGER", "decimal": "NUMERIC", "double": "REAL",
                "boolean": "INTEGER", "binary": "BLOB"}


def _constraint_clauses(t: Table, quote, table_name, same_schema_fks_only: bool = False) -> list[str]:
    parts = []
    if t.primary_key:
        parts.append(f"PRIMARY KEY ({', '.join(map(quote, t.primary_key))})")
    for name, cols in t.uniques:
        parts.append(f"CONSTRAINT {quote(name)} UNIQUE ({', '.join(map(quote, cols))})")
    for fk in t.foreign_keys:
        if same_schema_fks_only and fk["ref_schema"] != t.schema:
            print(f"  note: {fk['name']} crosses schemas, which this target does not support; left out")
            continue
        parts.append(
            f"CONSTRAINT {quote(fk['name'])} FOREIGN KEY ({', '.join(map(quote, fk['columns']))}) "
            f"REFERENCES {table_name(fk['ref_schema'], fk['ref_table'])} ({', '.join(map(quote, fk['ref_columns']))})"
        )
    return parts


def dquote(name: str) -> str:
    return '"' + name.replace('"', '""') + '"'


def _sqlite_value(v, col: Column):
    if v is None:
        return None
    if col.kind in ("json", "array"):
        return to_json_text(v)
    if isinstance(v, bool):
        return int(v)
    if isinstance(v, (bytes, memoryview)):
        return bytes(v)
    if isinstance(v, (int, float, str)):
        return v
    return text_value(v, col)


def export_sqlite(out: Path, tables: list[Table]) -> None:
    db = sqlite3.connect(out / "investor_db.sqlite")
    try:
        flat = lambda s, n: dquote(f"{s}__{n}")
        for t in tables:
            cols = [f"{dquote(c.name)} {SQLITE_TYPES.get(c.kind, 'TEXT')}{'' if c.nullable else ' NOT NULL'}"
                    for c in t.columns]
            db.execute(f"CREATE TABLE {dquote(t.flat)} ({', '.join(cols + _constraint_clauses(t, dquote, flat))})")
            db.executemany(
                f"INSERT INTO {dquote(t.flat)} VALUES ({', '.join('?' * len(t.columns))})",
                ([_sqlite_value(v, c) for v, c in zip(r, t.columns)] for r in t.rows),
            )
        db.commit()
    finally:
        db.close()


def _duck_type(kind: str, col: Column) -> str:
    if kind == "decimal":
        p, s = (col.precision, col.scale) if col.precision and col.precision <= 38 else UNCONSTRAINED_DECIMAL
        return f"DECIMAL({p},{s})"
    return {"integer": "INTEGER", "bigint": "BIGINT", "double": "DOUBLE", "boolean": "BOOLEAN", "date": "DATE",
            "timestamp": "TIMESTAMP", "timestamptz": "TIMESTAMPTZ", "uuid": "UUID", "json": "JSON",
            "binary": "BLOB"}.get(kind, "VARCHAR")


def export_duckdb(out: Path, tables: list[Table]) -> None:
    db = duckdb.connect(str(out / "investor_db.duckdb"))
    try:
        db.execute("SET TimeZone = 'UTC'")
        qualified = lambda s, n: f"{dquote(s)}.{dquote(n)}"
        for schema in dict.fromkeys(t.schema for t in tables):
            db.execute(f"CREATE SCHEMA IF NOT EXISTS {dquote(schema)}")
        for t in tables:
            types = [_duck_type(c.elem, c) + "[]" if c.kind == "array" else _duck_type(c.kind, c) for c in t.columns]
            cols = [f"{dquote(c.name)} {typ}{'' if c.nullable else ' NOT NULL'}" for c, typ in zip(t.columns, types)]
            db.execute(f"CREATE TABLE {qualified(t.schema, t.name)} "
                       f"({', '.join(cols + _constraint_clauses(t, dquote, qualified, same_schema_fks_only=True))})")
            if t.rows:
                db.register("src", arrow_table(t))
                casts = ", ".join(f"CAST({dquote(c.name)} AS {typ})" for c, typ in zip(t.columns, types))
                db.execute(f"INSERT INTO {qualified(t.schema, t.name)} SELECT {casts} FROM src")
                db.unregister("src")
    finally:
        db.close()


# --------------------------------------------------------------------------- MySQL / SQL Server scripts


def _key_length(t: Table, col: Column, limit: int) -> int:
    longest = t.max_text_length(col.name)
    if longest > limit:
        print(f"  warning: {t.qualified}.{col.name} has values of {longest} chars, longer than the key limit {limit}")
    return min(limit, max(col.length or 0, 64, longest))


def _mysql_type(t: Table, c: Column, keys: set[str]) -> str:
    if c.kind in ("text", "uuid") and c.name in keys:
        return f"VARCHAR({_key_length(t, c, 768)})"
    if c.kind == "decimal":
        p, s = (c.precision, c.scale) if c.precision and c.precision <= 65 else UNCONSTRAINED_DECIMAL
        return f"DECIMAL({p},{s})"
    return {"integer": "INT", "bigint": "BIGINT", "double": "DOUBLE", "boolean": "BOOLEAN", "date": "DATE",
            "timestamp": "DATETIME(6)", "timestamptz": "DATETIME(6)", "uuid": "CHAR(36)", "json": "JSON",
            "array": "JSON", "binary": "LONGBLOB"}.get(c.kind, "LONGTEXT")


def _mssql_type(t: Table, c: Column, keys: set[str]) -> str:
    if c.kind == "text" and c.name in keys:
        return f"NVARCHAR({_key_length(t, c, 450)})"
    if c.kind == "decimal":
        p, s = (c.precision, c.scale) if c.precision and c.precision <= 38 else UNCONSTRAINED_DECIMAL
        return f"DECIMAL({p},{s})"
    return {"integer": "INT", "bigint": "BIGINT", "double": "FLOAT", "boolean": "BIT", "date": "DATE",
            "timestamp": "DATETIME2(6)", "timestamptz": "DATETIMEOFFSET(6)", "uuid": "UNIQUEIDENTIFIER",
            "binary": "VARBINARY(MAX)"}.get(c.kind, "NVARCHAR(MAX)")


def _sql_literal(v, col: Column, dialect: str) -> str:
    if v is None:
        return "NULL"
    if col.kind in ("json", "array"):
        text = to_json_text(v)
    elif isinstance(v, bool):
        return ("TRUE" if v else "FALSE") if dialect == "mysql" else ("1" if v else "0")
    elif isinstance(v, (int, decimal.Decimal)):
        return str(v)
    elif isinstance(v, float):
        return repr(v) if v == v and abs(v) != float("inf") else "NULL"
    elif isinstance(v, (bytes, memoryview)):
        return ("X'" + bytes(v).hex() + "'") if dialect == "mysql" else ("0x" + bytes(v).hex())
    elif isinstance(v, dt.datetime):
        if v.tzinfo:
            v = v.astimezone(dt.timezone.utc)
        text = v.replace(tzinfo=None).isoformat(sep=" ") if dialect == "mysql" else v.isoformat()
    else:
        text = text_value(v, col)
    escaped = text.replace("'", "''")
    return f"'{escaped}'" if dialect == "mysql" else f"N'{escaped}'"


def export_sql_script(dialect: str, out: Path, tables: list[Table]) -> None:
    if dialect == "mysql":
        quote = lambda n: "`" + n.replace("`", "``") + "`"
        name = lambda s, n: quote(f"{s}__{n}")
        col_type = _mysql_type
        header = ["SET NAMES utf8mb4;",
                  "SET SESSION sql_mode = CONCAT_WS(',', NULLIF(@@SESSION.sql_mode, ''), 'NO_BACKSLASH_ESCAPES');",
                  "SET FOREIGN_KEY_CHECKS = 0;"]
        footer = ["SET FOREIGN_KEY_CHECKS = 1;"]
        table_suffix = " ENGINE=InnoDB DEFAULT CHARSET=utf8mb4"
    else:
        quote = lambda n: "[" + n.replace("]", "]]") + "]"
        name = lambda s, n: f"{quote(s)}.{quote(n)}"
        col_type = _mssql_type
        header = ["SET XACT_ABORT ON;", "SET NOCOUNT ON;"] + [
            f"IF SCHEMA_ID(N'{s}') IS NULL EXEC(N'CREATE SCHEMA {quote(s)}');"
            for s in dict.fromkeys(t.schema for t in tables)
        ]
        footer = []
        table_suffix = ""

    target = out / f"investor_db.{dialect}.sql"
    with target.open("w", encoding="utf-8", newline="\n") as f:
        f.write(f"-- investor_db export for {dialect}, generated {dt.datetime.now(dt.timezone.utc).isoformat()}\n")
        f.write("-- Re-running this script drops and recreates the exported tables.\n")
        f.write("\n".join(header) + "\n\n")
        for t in reversed(tables):
            f.write(f"DROP TABLE IF EXISTS {name(t.schema, t.name)};\n")
        for t in tables:
            keys = t.key_columns()
            cols = [f"  {quote(c.name)} {col_type(t, c, keys)}{'' if c.nullable else ' NOT NULL'}" for c in t.columns]
            if t.primary_key:
                cols.append(f"  PRIMARY KEY ({', '.join(map(quote, t.primary_key))})")
            for uname, ucols in t.uniques:
                cols.append(f"  CONSTRAINT {quote(uname)} UNIQUE ({', '.join(map(quote, ucols))})")
            f.write(f"\nCREATE TABLE {name(t.schema, t.name)} (\n" + ",\n".join(cols) + f"\n){table_suffix};\n")
            col_list = ", ".join(quote(c.name) for c in t.columns)
            for start in range(0, len(t.rows), INSERT_BATCH):
                batch = t.rows[start : start + INSERT_BATCH]
                values = ",\n".join(
                    "(" + ", ".join(_sql_literal(v, c, dialect) for v, c in zip(r, t.columns)) + ")" for r in batch
                )
                f.write(f"INSERT INTO {name(t.schema, t.name)} ({col_list}) VALUES\n{values};\n")
        f.write("\n")
        for t in tables:
            for fk in t.foreign_keys:
                f.write(
                    f"ALTER TABLE {name(t.schema, t.name)} ADD CONSTRAINT {quote(fk['name'])} "
                    f"FOREIGN KEY ({', '.join(map(quote, fk['columns']))}) "
                    f"REFERENCES {name(fk['ref_schema'], fk['ref_table'])} ({', '.join(map(quote, fk['ref_columns']))});\n"
                )
        f.write("\n".join(footer) + "\n")


# --------------------------------------------------------------------------- verification


def verify(fmt: str, out: Path, tables: list[Table]) -> dict[str, int] | None:
    """Row counts read back from the export, or None where that needs a server we don't have."""
    if fmt == "sqlite":
        db = sqlite3.connect(out / "investor_db.sqlite")
        try:
            return {t.qualified: db.execute(f"SELECT count(*) FROM {dquote(t.flat)}").fetchone()[0] for t in tables}
        finally:
            db.close()
    if fmt == "duckdb":
        db = duckdb.connect(str(out / "investor_db.duckdb"), read_only=True)
        try:
            return {t.qualified: db.execute(f"SELECT count(*) FROM {dquote(t.schema)}.{dquote(t.name)}").fetchone()[0]
                    for t in tables}
        finally:
            db.close()
    if fmt == "parquet":
        return {t.qualified: pq.read_metadata(out / f"{t.qualified}.parquet").num_rows for t in tables}
    if fmt == "csv":
        counts = {}
        for t in tables:
            with (out / f"{t.qualified}.csv").open(encoding="utf-8", newline="") as f:
                counts[t.qualified] = sum(1 for _ in csv.reader(f)) - 1
        return counts
    if fmt == "jsonl":
        return {t.qualified: sum(1 for _ in (out / f"{t.qualified}.jsonl").open(encoding="utf-8")) for t in tables}
    if fmt == "pgdump":
        return verify_pg_restore(out / "investor_db.dump", tables)
    if fmt == "pgsql":
        return verify_pg_restore(out / "investor_db.sql", tables)
    return None


def verify_pg_restore(dump: Path, tables: list[Table]) -> dict[str, int]:
    """Restore the archive or SQL script into a throwaway database and count rows there."""
    su = credentials(superuser=True)
    scratch = "investor_db_export_check"
    env = {**os.environ, "PGPASSWORD": su["password"]}
    base = ["-h", su["host"], "-p", su["port"], "-U", su["user"]]
    subprocess.run([pg_tool("dropdb"), *base, "--if-exists", scratch], check=True, env=env)
    subprocess.run([pg_tool("createdb"), *base, scratch], check=True, env=env)
    try:
        if dump.suffix == ".sql":
            subprocess.run([pg_tool("psql"), *base, "-d", scratch, "-X", "-q", "-v", "ON_ERROR_STOP=1",
                            "-f", str(dump)], check=True, env=env, stdout=subprocess.DEVNULL)
        else:
            subprocess.run([pg_tool("pg_restore"), *base, "-d", scratch, "--no-owner", "--exit-on-error",
                            str(dump)], check=True, env=env)
        import psycopg

        with psycopg.connect(**{**su, "dbname": scratch}) as conn:
            return {t.qualified: conn.execute(
                sql.SQL("select count(*) from {}.{}").format(sql.Identifier(t.schema), sql.Identifier(t.name))
            ).fetchone()[0] for t in tables}
    finally:
        subprocess.run([pg_tool("dropdb"), *base, "--if-exists", scratch], check=True, env=env)


# --------------------------------------------------------------------------- main

EXPORTERS = {
    "csv": export_csv, "jsonl": export_jsonl, "parquet": export_parquet, "sqlite": export_sqlite,
    "duckdb": export_duckdb,
    "mysql": lambda out, tables: export_sql_script("mysql", out, tables),
    "mssql": lambda out, tables: export_sql_script("mssql", out, tables),
}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--format", default="all", help=f"comma-separated subset of: {', '.join(FORMATS)} (default all)")
    parser.add_argument("--schemas", default=",".join(DEFAULT_SCHEMAS), help="comma-separated schemas to export")
    parser.add_argument("--out", type=Path, help="output directory (default exports/<UTC timestamp>)")
    parser.add_argument("--verify", action="store_true", help="read each export back and compare row counts")
    args = parser.parse_args()

    formats = FORMATS if args.format == "all" else [f.strip() for f in args.format.split(",")]
    unknown = set(formats) - set(FORMATS)
    if unknown:
        parser.error(f"unknown format(s): {', '.join(sorted(unknown))}")
    schemas = [s.strip() for s in args.schemas.split(",") if s.strip()]
    stamp = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    root = args.out or PROJECT_ROOT / "exports" / stamp

    with connect() as conn:
        tables = load_tables(conn, schemas)
    expected = {t.qualified: len(t.rows) for t in tables}
    print(f"exporting {len(tables)} tables, {sum(expected.values())} rows from schemas {', '.join(schemas)}")

    failures = 0
    for fmt in formats:
        out = root / fmt
        out.mkdir(parents=True, exist_ok=True)
        if fmt in ("pgdump", "pgsql"):
            export_pg(fmt, out, schemas, tables)
        else:
            EXPORTERS[fmt](out, tables)
        manifest = {
            "format": fmt, "created_at": stamp, "schemas": schemas, "rows": expected,
            "files": {p.name: file_sha256(p) for p in sorted(out.iterdir()) if p.name != "manifest.json"},
        }
        status = "written"
        if args.verify:
            counts = verify(fmt, out, tables)
            if counts is None:
                status = "written (row counts not checked: needs a live server)"
            elif counts == expected:
                status = "verified"
            else:
                failures += 1
                status = f"MISMATCH {counts}"
            manifest["verification"] = status
        (out / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
        print(f"  {fmt:8} {status}  -> {out.relative_to(PROJECT_ROOT) if out.is_relative_to(PROJECT_ROOT) else out}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
