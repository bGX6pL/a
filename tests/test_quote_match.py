"""Unit test for the evidence quote matcher (investordb.fetch.evidence.match).

    uv run python tests/test_quote_match.py
"""

import sys

from investordb.fetch.evidence import match

PAGE = """
<p>Prague-based Example Ventures has announced the final close of its second fund at
€45 million, backed by the European Investment Fund.</p>
<p>Fond investuje do&nbsp;startupů částky od 200&nbsp;000 do 1,5 milionu eur.</p>
"""
TEXT = PAGE.replace("<p>", " ").replace("</p>", " ").replace("&nbsp;", " ")

CASES = [
    # (quote, expected)
    ("Prague-based Example Ventures has announced the final close of its second fund at €45 million", True),
    ("prague-based example ventures has announced the final close of its second fund at €45 million", True),  # case
    ("Fond investuje do startupů částky od 200 000 do 1,5 milionu eur.", True),          # nbsp vs space
    ("Prague based Example Ventures announced the final close of its second fund at €45 million", True),  # small edits
    ("Prague-based Example Ventures has announced the final close of its second fund at €48 million", False),  # number changed
    ("Fond investuje do startupů částky od 200 000 do 2,5 milionu eur.", False),          # number changed
    ("Example Ventures invests EUR 5-20 million in buyouts of manufacturing companies.", False),  # invented
]


def main() -> int:
    failures = [(q, exp, match(q, TEXT)) for q, exp in CASES if match(q, TEXT)[0] != exp]
    for q, exp, got in failures:
        print(f"FAIL expected {exp}, got {got}: {q}")
    print("quote matcher OK" if not failures else f"{len(failures)} failure(s)")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
