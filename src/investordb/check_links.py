"""Re-fetch every evidence URL stored in the database and record the outcome in meta.link_check.

Collects all `url` and `evidence_urls` columns in the ref and core schemas.

    uv run python -m investordb.check_links                  # every URL
    uv run python -m investordb.check_links --stale-days 30  # only URLs not checked in the last 30 days

Set HTTP_USER_AGENT in .env to identify yourself (sec.gov rejects anonymous clients).
"""

import argparse
import sys
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor

from psycopg import sql

from investordb.db import connect, settings

URL_COLUMNS_SQL = """
select table_schema, table_name, column_name, data_type
from information_schema.columns
where table_schema in ('ref', 'core') and column_name in ('url', 'evidence_urls')
  and data_type in ('text', 'ARRAY')
"""


def collect_urls(conn, stale_days: int | None) -> list[str]:
    parts = []
    for schema, table, column, data_type in conn.execute(URL_COLUMNS_SQL).fetchall():
        expr = sql.SQL("unnest({})") if data_type == "ARRAY" else sql.SQL("{}")
        parts.append(sql.SQL("select {} as url from {}").format(
            expr.format(sql.Identifier(column)), sql.Identifier(schema, table)))
    if not parts:
        return []
    query = sql.SQL("select distinct url from ({}) u where url like 'http%%' and url not like '%%.invalid%%'").format(
        sql.SQL(" union all ").join(parts))
    if stale_days is not None:
        query += sql.SQL(
            " and not exists (select 1 from meta.link_check c where c.url = u.url"
            " and c.checked_at > now() - make_interval(days => %s))"
        )
        return [r[0] for r in conn.execute(query, (stale_days,))]
    return [r[0] for r in conn.execute(query)]


def check(url: str, user_agent: str) -> tuple[str, int | None, str | None, str | None]:
    request = urllib.request.Request(url, headers={"User-Agent": user_agent, "Accept": "*/*"})
    try:
        with urllib.request.urlopen(request, timeout=25) as response:
            response.read(65536)
            return url, response.status, response.geturl(), None
    except urllib.error.HTTPError as e:
        return url, e.code, e.geturl(), None
    except Exception as e:  # DNS failures, timeouts, TLS errors
        return url, None, None, f"{type(e).__name__}: {e}"[:500]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--stale-days", type=int, help="skip URLs checked successfully within this many days")
    parser.add_argument("--workers", type=int, default=8)
    args = parser.parse_args()
    user_agent = settings().get("HTTP_USER_AGENT") or "investor-db-link-check/0.1"

    with connect() as conn:
        urls = collect_urls(conn, args.stale_days)
        print(f"checking {len(urls)} URLs")
        with ThreadPoolExecutor(args.workers) as pool:
            results = list(pool.map(lambda u: check(u, user_agent), urls))
        with conn.cursor() as cur:
            cur.executemany(
                "insert into meta.link_check (url, http_status, final_url, error) values (%s, %s, %s, %s)", results
            )
    broken = [r for r in results if r[1] is None or r[1] >= 400]
    for url, status, _, error in broken:
        print(f"  {status or 'ERR'}  {url}  {error or ''}")
    print(f"{len(results) - len(broken)} ok, {len(broken)} failing (403/429 often means bot protection, not a dead page)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
