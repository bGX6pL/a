"""Fetch ARES (Czech business register aggregator) records for every Czech IČO we hold.

    uv run python -m investordb.fetch.ares                # IČOs not fetched in the last 30 days
    uv run python -m investordb.fetch.ares --refresh      # all of them

IČOs come from the JERRS snapshot (raw.jerrs_entity) and from dossiers (core.legal_entity, CZ-ICO).
"""

import argparse
import sys

from psycopg.types.json import Jsonb

from investordb.db import connect
from investordb.fetch.common import FetchRun

URL = "https://ares.gov.cz/ekonomicke-subjekty-v-be/rest/ekonomicke-subjekty/{ico}"

ICOS_SQL = """
select ico from (
    select ico from raw.jerrs_entity where ico is not null
    union
    select lpad(registry_id, 8, '0') from core.legal_entity where registry = 'CZ-ICO' and registry_id ~ '^[0-9]+$'
) all_icos
where %(refresh)s or ico not in (select ico from raw.ares_subject where fetched_at > now() - interval '30 days')
order by ico
"""


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--refresh", action="store_true")
    args = parser.parse_args()
    with FetchRun("cz-ares", "investordb.fetch.ares", {"refresh": args.refresh}, min_interval=0.25) as run, connect() as conn:
        icos = [r[0] for r in conn.execute(ICOS_SQL, {"refresh": args.refresh})]
        print(f"fetching {len(icos)} IČOs from ARES")
        for ico in icos:
            f = run.get(URL.format(ico=ico), headers={"Accept": "application/json"}, name=f"{ico}.json")
            payload = f.json() if f.ok else None
            with conn.transaction():
                conn.execute(
                    """insert into raw.ares_subject (ico, http_status, payload, fetched_at, fetch_run_id)
                       values (%s, %s, %s, now(), %s)
                       on conflict (ico) do update set http_status = excluded.http_status, payload = excluded.payload,
                           fetched_at = excluded.fetched_at, fetch_run_id = excluded.fetch_run_id""",
                    (ico, f.status or 0, Jsonb(payload) if payload is not None else None, run.id))
            run.rows += 1
        print(f"done: {run.rows} records")
    return 0


if __name__ == "__main__":
    sys.exit(main())
