"""Draw the manual-review samples and load reviewers' verdicts.

    uv run python -m investordb.review sample --m1 30 --m2 15   # writes data/curated/reviews/<sample>/_sample.json
    uv run python -m investordb.review load                     # loads data/curated/reviews/**/*.json into core.review

M1: published records (does each record hold up against its sources?).
M2: excluded / unverified candidates of the publishable pilots and the registry samples (was any
    real active VC wrongly left out?).
Samples are reproducible: records are ordered by md5(investor_key || sample name).

Review file (one per record): data/curated/reviews/<sample>/<investor_key>.json
{"investor_key", "sample", "reviewer", "reviewed_on", "verdict": "correct|incorrect|unsure",
 "checks": {"real_entity", "invests_in_companies", "active_24m", "type_correct", "decision_correct": true|false|null,
            "sector_focus", "stage_focus", "ticket_size", "capital", "activity_evidence":
            "correct|incorrect|unverifiable|not_applicable"},
 "notes": "..."}
"""

import argparse
import json
import sys
from pathlib import Path

from psycopg.types.json import Jsonb

from investordb.db import PROJECT_ROOT, connect

REVIEW_DIR = PROJECT_ROOT / "data" / "curated" / "reviews"
VERDICTS = {"correct", "incorrect", "unsure"}
BOOL_CHECKS = ["real_entity", "invests_in_companies", "active_24m", "type_correct", "decision_correct"]
FIELD_CHECKS = ["sector_focus", "stage_focus", "ticket_size", "capital", "activity_evidence"]
FIELD_VALUES = {"correct", "incorrect", "unverifiable", "not_applicable"}


def draw(conn, name: str, where: str, n: int) -> list[str]:
    return [r[0] for r in conn.execute(
        f"select investor_key from core.investor where {where} order by md5(investor_key || %s) limit %s", (name, n))]


def cmd_sample(args) -> int:
    with connect() as conn:
        m1 = draw(conn, args.name + ":m1", "published", args.m1)
        m2 = draw(conn, args.name + ":m2",
                  "decision <> 'include' and pilot in ('cz-vc', 'sk-reference', 'cz-s15-sample')", args.m2)
    out = REVIEW_DIR / args.name
    out.mkdir(parents=True, exist_ok=True)
    (out / "_sample.json").write_text(json.dumps({"m1": m1, "m2": m2}, indent=2), encoding="utf-8")
    print(f"M1: {len(m1)} published records, M2: {len(m2)} excluded/unverified -> {out.relative_to(PROJECT_ROOT)}")
    return 0


def validate(doc: dict) -> list[str]:
    p = [f"missing {k}" for k in ("investor_key", "sample", "reviewer", "reviewed_on", "verdict", "checks") if k not in doc]
    if p:
        return p
    if doc["verdict"] not in VERDICTS:
        p.append(f"verdict must be one of {sorted(VERDICTS)}")
    for k in BOOL_CHECKS:
        if doc["checks"].get(k) not in (True, False, None):
            p.append(f"checks.{k} must be true, false or null")
    for k in FIELD_CHECKS:
        if doc["checks"].get(k) not in FIELD_VALUES:
            p.append(f"checks.{k} must be one of {sorted(FIELD_VALUES)}")
    return p


def cmd_load(args) -> int:
    files = [f for f in sorted(REVIEW_DIR.rglob("*.json")) if not f.name.startswith("_")]
    bad = 0
    with connect() as conn:
        conn.execute("delete from core.review")
        for f in files:
            doc = json.loads(f.read_text(encoding="utf-8"))
            problems = validate(doc)
            if problems:
                bad += 1
                print(f"INVALID {f.relative_to(PROJECT_ROOT)}: {'; '.join(problems)}")
                continue
            conn.execute(
                """insert into core.review (investor_key, sample, reviewer, reviewed_on, verdict, checks, notes)
                   values (%s, %s, %s, %s, %s, %s, %s)
                   on conflict (investor_key, sample, reviewer) do update set verdict = excluded.verdict,
                       checks = excluded.checks, notes = excluded.notes, reviewed_on = excluded.reviewed_on""",
                (doc["investor_key"], doc["sample"], doc["reviewer"], doc["reviewed_on"], doc["verdict"],
                 Jsonb(doc["checks"]), doc.get("notes")))
    print(f"{len(files) - bad} reviews loaded, {bad} invalid")
    return 1 if bad else 0


def cmd_check(args) -> int:
    bad = 0
    for f in args.files:
        problems = validate(json.loads(f.read_text(encoding="utf-8")))
        print(f"{f}: {'OK' if not problems else 'INVALID: ' + '; '.join(problems)}")
        bad += bool(problems)
    return 1 if bad else 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("sample")
    s.add_argument("--name", default="review-2026-10")
    s.add_argument("--m1", type=int, default=30)
    s.add_argument("--m2", type=int, default=15)
    sub.add_parser("load")
    c = sub.add_parser("check")
    c.add_argument("files", nargs="+", type=Path)
    args = parser.parse_args()
    return {"sample": cmd_sample, "load": cmd_load, "check": cmd_check}[args.cmd](args)


if __name__ == "__main__":
    sys.exit(main())
