"""Re-fetch every evidence URL cited in dossiers and check that each quote is really on the page (V2, V3).

    uv run python -m investordb.fetch.evidence            # URLs without a check in the last 7 days
    uv run python -m investordb.fetch.evidence --all

Raw pages are stored under data/raw/web-evidence/<date>/ and logged in meta.fetched_file. Text is
extracted from HTML or PDF, normalised (Unicode NFKC, case, quotes, dashes, whitespace) and the quote
is searched exactly, then fuzzily (rapidfuzz partial ratio ≥ 90, to tolerate markup splitting a
sentence) with the extra condition that the matched passage contains exactly the quote's numbers.
Results go to core.evidence_check.
"""

import argparse
import hashlib
import re
import sys
import unicodedata
from collections import defaultdict

from rapidfuzz import fuzz

from investordb.db import connect
from investordb.fetch.common import FetchRun, html_to_text, pdf_to_text

FUZZY_THRESHOLD = 90.0
PUNCT = str.maketrans({"‘": "'", "’": "'", "‚": "'", "“": '"', "”": '"', "„": '"',
                       "«": '"', "»": '"', "–": "-", "—": "-", "−": "-", " ": " ",
                       " ": " ", " ": " "})

PENDING_SQL = """
select e.url, array_agg(distinct e.quote)
from core.evidence e
where %(all)s or not exists (
    select 1 from core.evidence_check c
    where c.url = e.url and c.quote_sha256 = encode(sha256(convert_to(e.quote, 'UTF8')), 'hex')
      and c.checked_at > now() - interval '7 days')
group by e.url order by e.url
"""


def normalise(text: str) -> str:
    text = unicodedata.normalize("NFKC", text).translate(PUNCT).casefold()
    return re.sub(r"\s+", " ", text).strip()


def page_text(fetched) -> str:
    kind = (fetched.content_type or "").lower()
    if "pdf" in kind or fetched.body[:5] == b"%PDF-":
        return pdf_to_text(fetched.body)
    if "json" in kind:
        return fetched.text("utf-8")
    return html_to_text(fetched.text())


NUMBER = re.compile(r"\d+(?:[.,\s]\d{3})*(?:[.,]\d+)?")


def numbers(text: str) -> list[str]:
    return [re.sub(r"[.,\s]", "", n) for n in NUMBER.findall(text)]


def match(quote: str, text: str) -> tuple[bool, float]:
    """Exact match, or a fuzzy match whose passage contains exactly the quote's numbers.

    The number rule matters: amounts and dates are the facts being verified, and a fuzzy score alone
    accepts a quote whose figures were changed.
    """
    q, t = normalise(quote), normalise(text)
    if not q or not t:
        return False, 0.0
    if q in t:
        return True, 1.0
    alignment = fuzz.partial_ratio_alignment(q, t)
    score = alignment.score if alignment else 0.0
    if score < FUZZY_THRESHOLD:
        return False, round(score / 100, 3)
    passage = t[alignment.dest_start:alignment.dest_end]
    return numbers(q) == numbers(passage), round(score / 100, 3)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--all", action="store_true", help="re-check every URL")
    args = parser.parse_args()
    stats = defaultdict(int)
    with FetchRun("web-evidence", "investordb.fetch.evidence", {"all": args.all}, min_interval=1.0) as run, connect() as conn:
        pending = conn.execute(PENDING_SQL, {"all": args.all}).fetchall()
        print(f"checking {len(pending)} URLs")
        for url, quotes in pending:
            f = run.get(url, timeout=45, retries=2)
            text, error = "", f.error
            if f.ok:
                try:
                    text = page_text(f)
                except Exception as e:  # broken PDFs and the like
                    error = f"text extraction failed: {type(e).__name__}: {e}"[:500]
            rows = []
            for quote in quotes:
                found, similarity = match(quote, text) if text else (False, 0.0)
                stats["found" if found else ("fetch_failed" if not f.ok else "not_found")] += 1
                rows.append((url, hashlib.sha256(quote.encode()).hexdigest(), f.status, f.fetched_file_id, len(text),
                             found if f.ok else None, similarity, error))
            with conn.transaction(), conn.cursor() as cur:
                cur.executemany(
                    """insert into core.evidence_check (url, quote_sha256, http_status, fetched_file_id, text_chars,
                           quote_found, similarity, error) values (%s, %s, %s, %s, %s, %s, %s, %s)""", rows)
            run.rows += 1
    print(", ".join(f"{k}: {v}" for k, v in sorted(stats.items())) or "nothing to check")
    return 0


if __name__ == "__main__":
    sys.exit(main())
