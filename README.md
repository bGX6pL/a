# investor-db

A database of real, active private-market investors (VC funds, private equity, family offices,
angels, large private investors), built only from public data. Every record is meant to carry its
investor type, sector focus, typical investments and ticket size, total capital, and a source plus
date that proves the investor actually invests.

Everything lives on `D:\investor-db`: Postgres binaries, the database cluster, code, raw downloads
and exports.

## Layout

| Path | What |
|---|---|
| `pgsql/` | PostgreSQL 16.14 binaries (copied from the local install so the project is self-contained) |
| `pgdata/` | the database cluster |
| `scripts/` | PowerShell helpers: start/stop the server, psql, first-time role/database setup |
| `sql/migrations/` | schema, applied in order by `investordb.migrate` |
| `src/investordb/` | Python tooling: migrations, seed loader, exporter, link checker, fetchers (`fetch/`), dossier loader, checks (`build`), review, metrics |
| `data/seed/` | hand-curated rows (research catalog) loaded by `investordb.load_seed` |
| `data/curated/` | analyst dossiers (one JSON per screened investor) and review verdicts |
| `docs/` | Task A plan, dossier format, pilot metrics and results |
| `data/raw/` | untouched downloads written by fetch scripts (rebuildable, not exported) |
| `exports/` | output of `investordb.export` |
| `reports/`, `research_notes/` | research on data sources and competitors |
| `.env`, `.pgpass` | local credentials, generated at setup; keep private |

## Database

- Server: `localhost:5440` (5432 is the old C: install's service, 5433 is taken by another
  Postgres on this machine). Listens on localhost only, SCRAM password auth.
- Database `investor_db`, owner role `investor`; superuser `postgres`. Passwords are in `.env`.
- UTF-8 with the ICU root collation, so `upper()`/`lower()` and sorting work for č, š, ž and the like.
- Schemas: `meta` (migrations, fetch runs, fetched files, link checks), `raw` (source data as
  fetched), `core` (curated investors; designed with the inclusion rules), `ref` (research catalog).

The server does not start on boot. Start and stop it with:

```powershell
.\scripts\pg-start.ps1
.\scripts\pg-stop.ps1
.\scripts\psql.ps1              # interactive psql as the app role
```

Rebuilding from scratch: `pgsql\bin\initdb` into `pgdata`, append the overrides at the end of
`pgdata\postgresql.conf`, then `scripts\bootstrap-db.ps1` and `uv run python -m investordb.migrate`.

## Python

```powershell
$env:UV_CACHE_DIR = "D:\investor-db\.uv-cache"   # keeps the package cache on D:
uv sync
uv run python -m investordb.migrate      # apply new migrations
uv run python -m investordb.load_seed    # (re)load data/seed/*.json
uv run python -m investordb.check_links  # re-fetch every evidence URL, log to meta.link_check
```

### Investor pipeline (Task A)

| Document | |
|---|---|
| [docs/task-a-plan.md](docs/task-a-plan.md) | plan: who is in and out (I1–I5, E1–E11), evidence standard, verification, coverage and reliability estimate, revisions after the pilot |
| [docs/task-a-pilot-results.md](docs/task-a-pilot-results.md) | pilot on Czech VC with Slovakia as reference: results, measured accuracy, limits |
| [docs/pilot-metrics.md](docs/pilot-metrics.md) | generated metrics and every published record with its dated proof of investing |
| [docs/global-expansion-cost.md](docs/global-expansion-cost.md) | cost of expanding worldwide |
| [docs/dossier-format.md](docs/dossier-format.md), [docs/review-protocol.md](docs/review-protocol.md) | analyst dossier format, review protocol |

```powershell
uv run python -m investordb.fetch.jerrs --date 2026-10-25 --from-file s15_managers=<saved.html>  # ČNB lists (CAPTCHA: see --help)
uv run python -m investordb.fetch.nbs          # NBS register export (SK)
uv run python -m investordb.fetch.cvca         # CVCA member profiles
uv run python -m investordb.load_dossiers      # validate + load data/curated/dossiers/**.json into core.*
uv run python -m investordb.fetch.ares         # ARES for every Czech IČO (JERRS + dossiers)
uv run python -m investordb.fetch.ruz          # RÚZ entities + balance sheets for Slovak IČOs
uv run python -m investordb.fetch.evidence     # re-fetch every cited URL, check quotes (V2/V3)
uv run python -m investordb.build              # checks V1-V7, confidence, core.investor_card
uv run python -m investordb.review sample      # draw review samples; review load loads verdicts
uv run python -m investordb.metrics            # writes docs/pilot-metrics.md
uv run python tests/test_quote_match.py
```

`core.investor_card` is the flat, one-row-per-investor result (published = true for the records
that passed); every field has its method and source URL alongside.

### Re-fetchable data

Rules every data-loading script follows:

1. Each source has a fetch script that downloads from the original public URL. Raw files go
   to `data/raw/<source>/` and are never edited by hand.
2. Every run is logged in `meta.fetch_run` (which must name a source in `ref.data_source`),
   with each downloaded file in `meta.fetched_file` (URL, HTTP status, SHA-256, local path).
3. Curated tables are derived from `raw` by code, so deleting `raw` and `core` and re-running
   the fetch and build scripts reproduces them.
4. Hand-curated facts (the research catalog) live in `data/seed/` with their evidence URLs.
   `check_links` re-fetches those URLs to confirm they still resolve.

## Export to other databases

```powershell
uv run python -m investordb.export --verify                      # every format
uv run python -m investordb.export --format sqlite,parquet --schemas ref,core
```

Writes `exports/<UTC timestamp>/<format>/` with a `manifest.json` (row counts, SHA-256 of files).

| Format | Target | Checked by `--verify` |
|---|---|---|
| `pgdump` | `pg_restore` into PostgreSQL 16+ | restored into a scratch database, row counts compared |
| `pgsql` | plain SQL for `psql -f` | same, via psql |
| `csv` | anything; NULL = empty unquoted field, arrays/JSON as JSON text, `schema.json` alongside | row counts |
| `jsonl` | MongoDB, Elasticsearch, BigQuery | row counts |
| `parquet` | DuckDB, Spark, Snowflake, BigQuery, ClickHouse, pandas | row counts |
| `sqlite` | single `.sqlite` file, tables named `schema__table` | row counts |
| `duckdb` | single `.duckdb` file with native types and constraints (DuckDB can't do cross-schema foreign keys, so those are left out) | row counts |
| `mysql` | MySQL 8 / MariaDB 10.5+ script, tables named `schema__table` | not checked (needs a server) |
| `mssql` | SQL Server 2017+ T-SQL script with matching schemas | not checked (needs a server) |

Defaults to the `core`, `ref` and `meta` schemas; `raw` is left out because the fetch scripts
rebuild it. `tests/test_export_roundtrip.py` exports a table with every supported column type
and compares the values read back from DuckDB, Parquet, SQLite, CSV and JSONL with Postgres:

```powershell
uv run python tests/test_export_roundtrip.py
```
