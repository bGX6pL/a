"""Fetch CVCA (Czech PE & VC association) member profiles into raw.cvca_member.

    uv run python -m investordb.fetch.cvca

Firm-level fields only (fund size, investment type, ticket, sectors, geography, website); contact
persons and e-mail addresses on the profiles are deliberately not stored.
"""

import datetime as dt
import html
import re
import sys

from psycopg.types.json import Jsonb

from investordb.db import connect
from investordb.fetch.common import FetchRun, html_to_text

LIST_PAGES = {
    "full": "https://cvca.cz/clenstvi/radni-clenove/",
    "associate": "https://cvca.cz/clenstvi/pridruzeni-clenove/",
}
# Labels used on CVCA profile pages, in page order; the text up to the next label is the value.
LABELS = [
    "Adresa", "Kontaktní osoba", "Informace o společnosti", "Objem prostředků ve správě", "Typ investic",
    "Preferovaná výše jedné investice", "Preferovaná odvětví", "Geografické zaměření", "Portfolio",
    "Popis činnosti", "Služby",
]
DROP = {"Kontaktní osoba", "Adresa"}  # personal data / not needed


def profile_fields(text: str) -> dict[str, str]:
    pattern = "|".join(map(re.escape, LABELS))
    parts = re.split(f"({pattern})", text)
    fields = {}
    for label, value in zip(parts[1::2], parts[2::2]):
        value = re.sub(r"\s+", " ", value).strip(" :")
        if label not in DROP and value and label not in fields:
            fields[label] = re.sub(r"\S+@\S+", "[e-mail removed]", value)[:2000]
    return fields


def main() -> int:
    today = dt.date.today()
    with FetchRun("cvca", "investordb.fetch.cvca", min_interval=1.0) as run, connect() as conn:
        rows = []
        for member_class, url in LIST_PAGES.items():
            page = run.get(url, name=f"members_{member_class}.html").text()
            links = dict.fromkeys(re.findall(r'<a[^>]+href="(https://cvca\.cz/[a-z0-9\-]+/)"[^>]*>\s*(?:Read More|Více)', page, re.I))
            for link in links:
                detail = run.get(link)
                markup = detail.text()
                title = re.search(r"(?is)<h1[^>]*>(.*?)</h1>", markup)
                name = html.unescape(re.sub(r"<[^>]+>", "", title.group(1))).strip() if title else link
                main = re.search(r"(?is)<(article|main)\b.*?</\1>", markup)
                text = html_to_text(main.group(0) if main else markup)
                posted = re.search(r"\b(\d{1,2})\.\s?(\d{1,2})\.\s?(\d{4})\b", text)
                websites = [w for w in re.findall(r"\b(?:https?://)?(?:www\.)[a-z0-9\-\.]+\.[a-z]{2,}\b", text, re.I)
                            if "cvca" not in w.lower()]
                rows.append((today, link, member_class, name.replace("​", ""), websites[0] if websites else None,
                             dt.date(int(posted.group(3)), int(posted.group(2)), int(posted.group(1))) if posted else None,
                             Jsonb(profile_fields(text)), run.id))
        with conn.transaction():
            conn.execute("delete from raw.cvca_member where fetched_on = %s", (today,))
            with conn.cursor() as cur:
                cur.executemany(
                    """insert into raw.cvca_member (fetched_on, url, member_class, name, website, posted_on, profile,
                           fetch_run_id) values (%s, %s, %s, %s, %s, %s, %s, %s)""", rows)
        run.rows = len(rows)
        print(f"CVCA: {len(rows)} member profiles")
    return 0


if __name__ == "__main__":
    sys.exit(main())
