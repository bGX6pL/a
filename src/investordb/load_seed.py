"""Load curated seed files (data/seed/*.json) into their tables.

Each file looks like {"table": "ref.data_source", "key": "slug", "rows": [{...}, ...]}.
Rows are upserted on the key; rows that are no longer in the file are deleted unless something
still references them. Re-running is safe.

    uv run python -m investordb.load_seed                     # every seed file
    uv run python -m investordb.load_seed data_sources.json   # just one
"""

import json
import sys

from psycopg import errors, sql
from psycopg.types.json import Jsonb

from investordb.db import PROJECT_ROOT, connect

SEED_DIR = PROJECT_ROOT / "data" / "seed"


def load_file(conn, path) -> None:
    spec = json.loads(path.read_text(encoding="utf-8"))
    schema, table = spec["table"].split(".")
    key, rows = spec["key"], spec["rows"]
    target = sql.Identifier(schema, table)
    jsonb_cols = {
        r[0] for r in conn.execute(
            "select column_name from information_schema.columns "
            "where table_schema = %s and table_name = %s and data_type = 'jsonb'", (schema, table)
        )
    }

    for row in rows:
        cols = list(row)
        values = [Jsonb(row[c]) if c in jsonb_cols else row[c] for c in cols]
        updates = [c for c in cols if c != key]
        conn.execute(
            sql.SQL("insert into {} ({}) values ({}) on conflict ({}) do update set {}").format(
                target,
                sql.SQL(", ").join(map(sql.Identifier, cols)),
                sql.SQL(", ").join(sql.Placeholder() * len(cols)),
                sql.Identifier(key),
                sql.SQL(", ").join(sql.SQL("{0} = excluded.{0}").format(sql.Identifier(c)) for c in updates),
            ),
            values,
        )

    keep = [r[key] for r in rows]
    stale = [r[0] for r in conn.execute(
        sql.SQL("select {} from {} where not ({} = any(%s))").format(sql.Identifier(key), target, sql.Identifier(key)),
        (keep,),
    )]
    for value in stale:
        try:
            with conn.transaction():
                conn.execute(sql.SQL("delete from {} where {} = %s").format(target, sql.Identifier(key)), (value,))
        except errors.ForeignKeyViolation:
            print(f"  kept {spec['table']} {value!r}: removed from seed but still referenced")
    print(f"{path.name}: {len(rows)} rows upserted into {spec['table']}, {len(stale)} stale")


def main() -> int:
    only = set(sys.argv[1:])  # optional file names, e.g. data_sources.json
    files = [p for p in sorted(SEED_DIR.glob("*.json")) if not only or p.name in only]
    if not files:
        print(f"no seed files in {SEED_DIR}")
        return 1
    with connect() as conn:
        for path in files:
            with conn.transaction():
                load_file(conn, path)
    return 0


if __name__ == "__main__":
    sys.exit(main())
