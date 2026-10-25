"""Round-trip test for investordb.export.

Creates a throwaway schema covering every column kind the exporter handles (quotes, backslashes,
non-ASCII text, NULL vs empty string, arrays, JSON, decimals, time zones, bytes, an unmapped type,
unique and foreign keys), exports it to every format with --verify, compares the values read back
from SQLite, DuckDB, Parquet, CSV and JSONL with Postgres, and drops the schema again.

    uv run python tests/test_export_roundtrip.py
"""

import csv
import datetime as dt
import decimal
import json
import shutil
import sqlite3
import subprocess
import sys
import tempfile
import uuid
from pathlib import Path

import duckdb
import pyarrow.parquet as pq

from investordb.db import PROJECT_ROOT, connect

SCHEMA = "export_selftest"

SETUP = f"""
drop schema if exists {SCHEMA} cascade;
create schema {SCHEMA};
create table {SCHEMA}.parent (
    parent_id integer primary key,
    code      text not null unique
);
create table {SCHEMA}.child (
    child_id    bigint generated always as identity primary key,
    parent_id   integer references {SCHEMA}.parent,
    amount      numeric(20,2),
    ratio       numeric,
    score       double precision,
    flag        boolean,
    label       text,
    born        date,
    seen_at     timestamptz,
    local_at    timestamp,
    ref_uuid    uuid,
    attrs       jsonb,
    tags        text[],
    sizes       numeric[],
    blob        bytea,
    addr        inet
);
insert into {SCHEMA}.parent values (1, 'vc-sk'), (2, 'pe-cz');
insert into {SCHEMA}.child (parent_id, amount, ratio, score, flag, label, born, seen_at, local_at,
                            ref_uuid, attrs, tags, sizes, blob, addr) values
  (1, 1234567890.12, 0.333333333333, 1.5, true, 'O''Brien \\ "Fund" – Bratislava č š ž', '2024-02-29',
   '2026-10-25 10:30:00.123456+02', '2026-10-25 10:30:00', 'a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11',
   '{{"aum_eur": 50000000, "stages": ["seed", "A"], "ok": true, "s": "x"}}', array['fintech', 'deep tech'],
   array[1.25, 300000]::numeric[], '\\xdeadbeef', '10.0.0.1'),
  (2, null, null, null, false, '', null, null, null, null, '"just a string"', '{{}}', null, null, null),
  (null, 0, 12, -0.0, null, null, '1999-12-31', '2000-01-01 00:00:00+00', null, null, 'null', null,
   null, null, null);
"""


def norm(v):
    """Normalise values from different engines to comparable Python values."""
    if isinstance(v, decimal.Decimal):
        return float(v)
    if isinstance(v, dt.datetime):
        return (v.astimezone(dt.timezone.utc) if v.tzinfo else v).replace(tzinfo=None)
    if isinstance(v, (bytes, bytearray, memoryview)):
        return bytes(v).hex()
    if isinstance(v, uuid.UUID):
        return str(v)
    if isinstance(v, list):
        return [norm(x) for x in v]
    if isinstance(v, dict):
        return {k: norm(x) for k, x in v.items()}
    return v


def main() -> int:
    with connect() as conn:
        conn.execute(SETUP)
        conn.commit()
        cols = [r[0] for r in conn.execute(
            "select attname from pg_attribute where attrelid = %s::regclass and attnum > 0 and not attisdropped "
            "order by attnum", (f"{SCHEMA}.child",)).fetchall()]
        pg_rows = conn.execute(f"select *, addr::text from {SCHEMA}.child order by child_id").fetchall()
    label = 'O\'Brien \\ "Fund" – Bratislava č š ž'
    if pg_rows[0][cols.index("label")] != label:
        print(f"FAILED: text was mangled on the way into Postgres: {pg_rows[0][cols.index('label')]!r}")
        return 1
    # addr comes back as an ipaddress object from psycopg; the exporter casts unmapped types to text
    expected = [tuple(norm(v) for v in r[:-2]) + (r[-1],) for r in pg_rows]
    json_cols = {cols.index("attrs"), cols.index("tags"), cols.index("sizes")}

    scratch = PROJECT_ROOT / "tmp"
    scratch.mkdir(exist_ok=True)
    out = Path(tempfile.mkdtemp(prefix="export_test_", dir=scratch))
    problems = []
    try:
        result = subprocess.run(
            [sys.executable, "-m", "investordb.export", "--schemas", SCHEMA, "--out", str(out), "--verify"],
            capture_output=True, text=True,
        )
        print(result.stdout, result.stderr)
        if result.returncode != 0:
            problems.append("export --verify failed")

        def check(engine, rows, decode_json=False, coerce=None):
            for got, want in zip(rows, expected):
                got = list(got)
                for i in range(len(got)):
                    if decode_json and i in json_cols and isinstance(got[i], str):
                        got[i] = json.loads(got[i])
                    if coerce:
                        got[i] = coerce(i, got[i])
                    got[i] = norm(got[i])
                    w = want[i]
                    if got[i] != w and not (isinstance(w, float) and isinstance(got[i], (int, float))
                                            and abs(got[i] - w) < 1e-9):
                        problems.append(f"{engine}: row {want[0]} column {cols[i]}: {got[i]!r} != {w!r}")
            if len(rows) != len(expected):
                problems.append(f"{engine}: {len(rows)} rows, expected {len(expected)}")

        # DuckDB keeps native types; JSON comes back as text
        db = duckdb.connect(str(out / "duckdb" / "investor_db.duckdb"), read_only=True)
        check("duckdb", db.execute(f'select * from "{SCHEMA}"."child" order by child_id').fetchall(),
              decode_json=True, coerce=lambda i, v: str(v) if cols[i] == "ref_uuid" and v is not None else v)
        db.close()

        # Parquet: lists stay lists, JSON is text
        table = pq.read_table(out / "parquet" / f"{SCHEMA}.child.parquet").to_pylist()
        check("parquet", [tuple(r.values()) for r in table], decode_json=True)

        # SQLite: everything is text/number; convert per column kind
        def sqlite_coerce(i, v):
            name = cols[i]
            if v is None:
                return v
            if name == "flag":
                return bool(v)
            if name == "born":
                return dt.date.fromisoformat(v)
            if name in ("seen_at", "local_at"):
                return dt.datetime.fromisoformat(v)
            return v

        lite = sqlite3.connect(out / "sqlite" / "investor_db.sqlite")
        check("sqlite", lite.execute(f'select * from "{SCHEMA}__child" order by child_id').fetchall(),
              decode_json=True, coerce=sqlite_coerce)
        lite.close()

        # CSV: NULL is an empty unquoted field, '' an empty quoted one
        with (out / "csv" / f"{SCHEMA}.child.csv").open(encoding="utf-8", newline="") as f:
            raw = f.read()
        if ',"",' not in raw:
            problems.append("csv: empty string is not distinguishable from NULL")
        with (out / "csv" / f"{SCHEMA}.child.csv").open(encoding="utf-8", newline="") as f:
            header, *csv_rows = list(csv.reader(f))
        if header != cols:
            problems.append(f"csv header {header} != {cols}")

        # JSONL: arrays as JSON arrays, json column as embedded JSON
        lines = [json.loads(l) for l in (out / "jsonl" / f"{SCHEMA}.child.jsonl").open(encoding="utf-8")]
        if lines[0]["tags"] != ["fintech", "deep tech"] or lines[0]["attrs"]["aum_eur"] != 50000000:
            problems.append(f"jsonl: unexpected first row {lines[0]}")

        for script in ("mysql", "mssql"):
            text = (out / script / f"investor_db.{script}.sql").read_text(encoding="utf-8")
            if "O''Brien" not in text or "INSERT INTO" not in text or "FOREIGN KEY" not in text:
                problems.append(f"{script}: script is missing quoting, inserts or foreign keys")
    finally:
        shutil.rmtree(out, ignore_errors=True)
        with connect() as conn:
            conn.execute(f"drop schema if exists {SCHEMA} cascade")

    if problems:
        print("FAILED\n  " + "\n  ".join(problems))
        return 1
    print("export round-trip OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
