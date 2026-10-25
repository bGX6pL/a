"""Apply SQL migrations from sql/migrations in filename order; each file runs once.

    uv run python -m investordb.migrate
"""

import hashlib
import sys

from investordb.db import PROJECT_ROOT, connect

MIGRATIONS_DIR = PROJECT_ROOT / "sql" / "migrations"


def main() -> int:
    with connect() as conn:
        conn.execute("create schema if not exists meta")
        conn.execute(
            """create table if not exists meta.schema_migration (
                   filename   text primary key,
                   sha256     text not null,
                   applied_at timestamptz not null default now())"""
        )
        applied = dict(conn.execute("select filename, sha256 from meta.schema_migration").fetchall())
        conn.commit()

        for path in sorted(MIGRATIONS_DIR.glob("*.sql")):
            sql = path.read_text(encoding="utf-8").replace("\r\n", "\n")
            digest = hashlib.sha256(sql.encode()).hexdigest()
            if path.name in applied:
                if applied[path.name] != digest:
                    print(f"WARNING: {path.name} changed after it was applied; add a new migration instead")
                continue
            with conn.transaction():
                conn.execute(sql)
                conn.execute(
                    "insert into meta.schema_migration (filename, sha256) values (%s, %s)", (path.name, digest)
                )
            print(f"applied {path.name}")
    print("migrations up to date")
    return 0


if __name__ == "__main__":
    sys.exit(main())
