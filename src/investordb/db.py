"""Connection settings for the project database, read from the project's .env file."""

import os
from pathlib import Path

import psycopg
from dotenv import dotenv_values
from psycopg.conninfo import make_conninfo

PROJECT_ROOT = Path(__file__).resolve().parents[2]
PG_BIN = PROJECT_ROOT / "pgsql" / "bin"


def settings() -> dict[str, str]:
    """.env values, overridden by PG* variables already set in the environment."""
    values = {k: v for k, v in dotenv_values(PROJECT_ROOT / ".env").items() if v is not None}
    values.update({k: v for k, v in os.environ.items() if k.startswith("PG")})
    return values


def credentials(superuser: bool = False) -> dict[str, str]:
    s = settings()
    return {
        "host": s.get("PGHOST", "localhost"),
        "port": s.get("PGPORT", "5440"),
        "dbname": s.get("PGDATABASE", "investor_db"),
        "user": s["PG_SUPERUSER"] if superuser else s["PGUSER"],
        "password": s["PG_SUPERUSER_PASSWORD"] if superuser else s["PGPASSWORD"],
    }


def connect(superuser: bool = False, **kwargs) -> psycopg.Connection:
    return psycopg.connect(make_conninfo(**credentials(superuser)), **kwargs)


def pg_tool(name: str) -> str:
    """Path to a bundled Postgres client tool (pg_dump, psql, ...)."""
    exe = PG_BIN / f"{name}.exe"
    return str(exe if exe.exists() else PG_BIN / name)
