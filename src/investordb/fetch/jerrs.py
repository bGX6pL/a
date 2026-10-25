"""Fetch ČNB JERRS lists of fund managers and funds into raw.jerrs_entity.

    uv run python -m investordb.fetch.jerrs --date 2026-10-25
    uv run python -m investordb.fetch.jerrs --date 2026-10-25 --from-file s15_managers=saved.html ...

Lists (by their JERRS titles): §15 ZISIF sub-threshold managers, licensed investment companies,
investment companies managing qualified venture capital funds, foreign EuVECA funds, and investment
funds with legal personality.

JERRS answers repeated automated requests with a CAPTCHA. This script never tries to get past it:
it stops and asks for the list pages to be saved from a browser (open the list in JERRS, "Základní
seznamy", page size "nestránkovat", save the page) and passed with --from-file. The bulk,
machine-to-machine route is WS JERRS, which needs a commercial certificate from ČNB.
"""

import argparse
import datetime as dt
import html
import re
import sys
from pathlib import Path

from investordb.db import connect
from investordb.fetch.common import FetchRun, table_rows

BASE = "https://jerrs.cnb.cz/apljerrsdad/"
LISTS = {
    "s15_managers": "Osoby uvedené v § 15 odst. 1 ZISIF",
    "investment_companies": "Investiční společnosti a pobočky zahraničních investičních společností",
    "euveca_managers": "Investiční společnosti obhospodařující kvalifikované fondy rizikového kapitálu",
    "foreign_euveca_funds": "Zahraniční fondy srovnatelné s kvalifikovaným fondem rizikového kapitálu (EuVECA)",
    "funds_legal_personality": "Investiční fondy s právní osobností",
}
# Long JERRS titles continue after these prefixes; the others must match exactly.
PREFIX_TITLES = {"s15_managers", "euveca_managers"}


class CaptchaRequired(RuntimeError):
    pass


def check_captcha(text: str) -> None:
    if "CAPTCHA" in text:
        raise CaptchaRequired(
            "JERRS asked for a CAPTCHA. Save the list pages from a browser and re-run with --from-file KEY=PATH "
            f"(keys: {', '.join(LISTS)}), or use WS JERRS.")


def list_links(run: FetchRun, date: str) -> dict[str, str]:
    page = run.get(BASE + "JERRS.WEB15.BASIC_LISTINGS_RESPONSE", name=f"lists_{date}.html", data={
        "p_lang": "cz", "p_typ_sady": "SS", "p_DATUM": date, "p_hie": "HI", "p_rec_per_page": "108"})
    check_captcha(page.text())
    links = {}
    for href, label in re.findall(r'(?is)<a[^>]+href="([^"]+)"[^>]*>(.*?)</a>', page.text()):
        label = html.unescape(re.sub(r"<[^>]+>", "", label)).strip()
        for key, title in LISTS.items():
            if label == title or (key in PREFIX_TITLES and label.startswith(title)):
                links.setdefault(key, BASE + html.unescape(href))
    return links


def parse_list(markup: str) -> list[tuple]:
    records = []
    for cells, row in zip(table_rows(markup), re.findall(r"(?is)<tr[^>]*>(.*?)</tr>", markup)):
        if len(cells) >= 6 and re.fullmatch(r"\d{8}", cells[0]):
            card = re.search(r'href="(JERRS\.WEB10\.VIZITKA[^"]+)"', row)
            records.append((cells[0], cells[1], cells[2], cells[3], cells[4], cells[5],
                            BASE + html.unescape(card.group(1)) if card else None))
    return records


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--date", type=dt.date.fromisoformat, default=dt.date.today())
    parser.add_argument("--from-file", action="append", default=[], metavar="KEY=PATH",
                        help="use a list page saved from a browser instead of downloading it")
    args = parser.parse_args()
    jerrs_date = args.date.strftime("%d.%m.%Y")
    saved = dict(item.split("=", 1) for item in args.from_file)
    unknown = set(saved) - set(LISTS)
    if unknown:
        parser.error(f"unknown list key(s): {', '.join(sorted(unknown))}")

    params = {"date": args.date.isoformat(), "from_file": sorted(saved)}
    with FetchRun("cnb-jerrs", "investordb.fetch.jerrs", params, min_interval=2.0) as run, connect() as conn:
        pages = {}
        for key, path in saved.items():
            pages[key] = run.adopt(f"{BASE}JERRS.WEB15.BASIC_LISTINGS_RESPONSE_3?list={key}&p_DATUM={jerrs_date}", Path(path))
        if set(LISTS) - set(saved):
            try:
                links = list_links(run, jerrs_date)
                for key, url in links.items():
                    if key not in pages:
                        page = run.get(url, name=f"{key}_{args.date.isoformat()}.html", timeout=180)
                        check_captcha(page.text())
                        pages[key] = page
            except CaptchaRequired as e:
                print(f"stopped: {e}")
        for key, page in pages.items():
            records = [(args.date, key, *r, run.id) for r in parse_list(page.text("utf-8"))]
            with conn.transaction():
                conn.execute("delete from raw.jerrs_entity where snapshot_date = %s and list_name = %s", (args.date, key))
                with conn.cursor() as cur:
                    cur.executemany(
                        """insert into raw.jerrs_entity (snapshot_date, list_name, ico, name, street, city, zip, country,
                               card_url, fetch_run_id) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                           on conflict do nothing""", records)
            run.rows += len(records)
            print(f"{key}: {len(records)} entities")
        missing = set(LISTS) - set(pages)
        if missing:
            print(f"not fetched: {', '.join(sorted(missing))}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
