"""Validate and load investor dossiers (data/curated/dossiers/<pilot>/<investor_key>.json) into core.*.

    uv run python -m investordb.load_dossiers                  # validate and load every dossier
    uv run python -m investordb.load_dossiers --check FILE...  # validate only, print problems

A dossier is the analyst's record of one screened candidate; the format is documented in
docs/dossier-format.md. Loading replaces the candidate's previous rows, so it is safe to re-run.
"""

import argparse
import datetime as dt
import json
import re
import sys
from pathlib import Path

import psycopg
from psycopg.types.json import Jsonb

from investordb.db import PROJECT_ROOT, connect

DOSSIER_DIR = PROJECT_ROOT / "data" / "curated" / "dossiers"
SNAPSHOT_DATE = dt.date(2026, 10, 25)
ACTIVITY_WINDOW_START = dt.date(2024, 10, 25)  # 24 months before the snapshot

PILOTS = {"cz-vc", "sk-reference", "cz-s15-sample"}
TYPES = {"vc", "pe", "family_office", "angel", "angel_network", "private_investor"}
DECISIONS = {"include", "exclude", "unverified"}
SECTORS = {
    "software_saas", "ai_data", "fintech", "healthtech", "biotech_life_sciences", "deeptech_hardware",
    "energy_climate", "mobility_logistics", "ecommerce_marketplaces", "consumer", "edtech",
    "proptech_construction", "agrifood", "industrial_manufacturing", "cybersecurity", "media_gaming",
    "impact_social", "defence_dualuse", "generalist",
}
STAGES = {"pre_seed", "seed", "series_a", "series_b", "growth", "buyout"}
METHODS = {"stated", "derived", "self_reported", "registry", "not_disclosed"}
# latest_fund_size = final close of the newest fund; interim_close = committed so far in a fund that is
# still raising (first / second close, "raised to date"). A target alone is never capital.
CAPITAL_BASES = {"aum", "latest_fund_size", "interim_close", "cumulative_fund_sizes", "balance_sheet",
                 "regulatory_filing"}
FUND_EVENTS = {"first_close", "interim_close", "final_close", "launch", "target", "commitment", "other"}
REGISTRIES = {"CZ-ICO", "SK-ICO", "LEI", "OTHER"}
ROLES = {"manager", "fund", "gp", "holding", "other"}
SOURCE_CLASSES = {"A", "B", "C", "D"}
FACT_FIELDS = ("sector_focus", "stage_focus", "geography_focus", "ticket_size", "capital")
RULE_CODE = re.compile(r"^(I[1-5]|E([1-9]|1[01])|S[12])$")  # S = real investor outside the pilot scope
KEY = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
CURRENCY = re.compile(r"^[A-Z]{3}$")


def parse_date(value, problems: list[str], where: str) -> dt.date | None:
    if value in (None, ""):
        return None
    try:
        d = dt.date.fromisoformat(value)
    except (TypeError, ValueError):
        problems.append(f"{where}: not an ISO date: {value!r}")
        return None
    if d > SNAPSHOT_DATE:
        problems.append(f"{where}: date {d} is after the snapshot date")
    return d


def validate(doc: dict, path: Path) -> list[str]:
    p: list[str] = []
    required = ["investor_key", "pilot", "name", "investor_type", "decision", "rule_codes", "evidence",
                "researched_on"]
    for k in required:
        if k not in doc:
            p.append(f"missing key {k}")
    if p:
        return p

    if not KEY.match(doc["investor_key"]):
        p.append(f"investor_key must be kebab-case: {doc['investor_key']!r}")
    if path.stem != doc["investor_key"]:
        p.append(f"file name {path.name} must equal investor_key")
    if doc["pilot"] not in PILOTS:
        p.append(f"pilot must be one of {sorted(PILOTS)}")
    if doc["investor_type"] is not None and doc["investor_type"] not in TYPES:
        p.append(f"investor_type must be null or one of {sorted(TYPES)}")
    if doc["decision"] not in DECISIONS:
        p.append(f"decision must be one of {sorted(DECISIONS)}")
    for code in doc["rule_codes"]:
        if not RULE_CODE.match(code):
            p.append(f"bad rule code {code!r}")
    parse_date(doc["researched_on"], p, "researched_on")

    ev_ids = set()
    dated_evidence = {}
    for i, e in enumerate(doc["evidence"]):
        where = f"evidence[{i}]"
        for k in ("id", "url", "source_class", "quote"):
            if not e.get(k):
                p.append(f"{where}: missing {k}")
        if e.get("id") in ev_ids:
            p.append(f"{where}: duplicate id {e.get('id')}")
        ev_ids.add(e.get("id"))
        if e.get("source_class") and e["source_class"] not in SOURCE_CLASSES:
            p.append(f"{where}: source_class must be A, B, C or D")
        if e.get("url") and not str(e["url"]).startswith(("http://", "https://")):
            p.append(f"{where}: url must be http(s)")
        if e.get("quote") and len(e["quote"]) > 400:
            p.append(f"{where}: quote longer than 400 characters")
        dated_evidence[e.get("id")] = parse_date(e.get("published_on"), p, f"{where}.published_on")

    def check_refs(refs, where):
        for r in refs if isinstance(refs, list) else [refs]:
            if r not in ev_ids:
                p.append(f"{where}: unknown evidence id {r!r}")

    for le in doc.get("legal_entities", []):
        if le.get("registry") not in REGISTRIES:
            p.append(f"legal entity {le.get('name')!r}: registry must be one of {sorted(REGISTRIES)}")
        if le.get("role") not in ROLES:
            p.append(f"legal entity {le.get('name')!r}: role must be one of {sorted(ROLES)}")
        if le.get("registry") in ("CZ-ICO", "SK-ICO") and not re.fullmatch(r"\d{6,8}", str(le.get("registry_id") or "")):
            p.append(f"legal entity {le.get('name')!r}: IČO must be 6-8 digits")

    for field in FACT_FIELDS:
        fact = doc.get(field)
        if fact is None:
            continue
        where = field
        if fact.get("method") not in METHODS:
            p.append(f"{where}: method must be one of {sorted(METHODS)}")
        if fact.get("method") != "not_disclosed":
            if fact.get("value") in (None, [], {}):
                p.append(f"{where}: value missing (use method not_disclosed if the source does not say)")
            if not fact.get("evidence"):
                p.append(f"{where}: needs at least one evidence id")
        check_refs(fact.get("evidence", []), where)
        value = fact.get("value")
        if field == "sector_focus" and value:
            for s in value:
                if s not in SECTORS:
                    p.append(f"sector_focus: unknown sector {s!r}")
        if field == "stage_focus" and value:
            for s in value:
                if s not in STAGES:
                    p.append(f"stage_focus: unknown stage {s!r}")
        if field == "ticket_size" and value:
            if not CURRENCY.match(str(value.get("currency", ""))):
                p.append("ticket_size: currency must be an ISO code")
            lo, hi = value.get("min"), value.get("max")
            if lo is not None and hi is not None and lo > hi:
                p.append("ticket_size: min > max")
        if field == "capital" and value:
            if not CURRENCY.match(str(value.get("currency", ""))):
                p.append("capital: currency must be an ISO code")
            if value.get("basis") not in CAPITAL_BASES:
                p.append(f"capital: basis must be one of {sorted(CAPITAL_BASES)}")
            if not isinstance(value.get("amount"), (int, float)):
                p.append("capital: amount must be a number")
            parse_date(value.get("as_of"), p, "capital.as_of")

    activity_dates = []
    for i, f in enumerate(doc.get("funds", [])):
        if f.get("event") not in FUND_EVENTS:
            p.append(f"funds[{i}]: event must be one of {sorted(FUND_EVENTS)}")
        if f.get("currency") and not CURRENCY.match(f["currency"]):
            p.append(f"funds[{i}]: currency must be an ISO code")
        check_refs(f.get("evidence"), f"funds[{i}]")
        d = parse_date(f.get("event_date"), p, f"funds[{i}].event_date")
        if d and f.get("event") in ("first_close", "interim_close", "final_close", "commitment"):
            activity_dates.append(d)  # a launch / "opened to investors" is not activity (plan 10a)
    for i, inv in enumerate(doc.get("investments", [])):
        if not inv.get("company"):
            p.append(f"investments[{i}]: missing company")
        if inv.get("currency") and not CURRENCY.match(inv["currency"]):
            p.append(f"investments[{i}]: currency must be an ISO code")
        check_refs(inv.get("evidence"), f"investments[{i}]")
        d = parse_date(inv.get("date"), p, f"investments[{i}].date")
        if d:
            activity_dates.append(d)

    if doc["decision"] == "include":
        if doc["investor_type"] is None:
            p.append("include: investor_type is required")
        if not any(c.startswith("I") for c in doc["rule_codes"]) or any(c.startswith("E") for c in doc["rule_codes"]):
            p.append("include: rule_codes must list the I-rules met and no E-rules")
        for field in FACT_FIELDS:
            if doc.get(field) is None:
                p.append(f"include: {field} must be present (value or method not_disclosed)")
        if not any(d and d >= ACTIVITY_WINDOW_START and not (d.month == 1 and d.day == 1) for d in activity_dates):
            p.append("include: needs a dated investment or fund close/commitment on/after 2024-10-25 (rule I3; "
                     "launches and 1 January year-only placeholders do not count)")
        if not doc.get("legal_entities"):
            p.append("include: at least one legal entity is required (rule I1)")
    elif doc["decision"] == "exclude":
        if not any(c.startswith(("E", "S")) for c in doc["rule_codes"]):
            p.append("exclude: rule_codes must name the E- or S-rule(s) that apply")
    return p


def insert_dossier(conn, doc: dict, path: Path) -> None:
    conn.execute("delete from core.investor where investor_key = %s", (doc["investor_key"],))
    flags = doc.get("flags") or {}
    investor_id = conn.execute(
        """insert into core.investor (investor_key, pilot, name, aliases, investor_type, secondary_types,
               is_corporate, is_public, is_accelerator, hq_country, website, decision, rule_codes, decision_note,
               discovered_via, co_investors_seen, analyst_notes, researched_on, dossier_path)
           values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
           returning investor_id""",
        (doc["investor_key"], doc["pilot"], doc["name"], doc.get("aliases", []), doc["investor_type"],
         doc.get("secondary_types", []), bool(flags.get("corporate")), bool(flags.get("public")),
         bool(flags.get("accelerator")), doc.get("hq_country"), doc.get("website"), doc["decision"],
         doc["rule_codes"], doc.get("decision_note"), doc.get("discovered_via", []),
         doc.get("co_investors_seen", []), doc.get("analyst_notes"), doc["researched_on"],
         path.relative_to(PROJECT_ROOT).as_posix()),
    ).fetchone()[0]

    ev = {}
    for e in doc["evidence"]:
        ev[e["id"]] = conn.execute(
            """insert into core.evidence (investor_id, local_id, url, publisher, published_on, source_class, quote, language)
               values (%s, %s, %s, %s, %s, %s, %s, %s) returning evidence_id""",
            (investor_id, e["id"], e["url"], e.get("publisher"), e.get("published_on") or None, e["source_class"],
             e["quote"], e.get("language")),
        ).fetchone()[0]

    for le in doc.get("legal_entities", []):
        conn.execute(
            "insert into core.legal_entity (investor_id, name, country, registry, registry_id, role) values (%s, %s, %s, %s, %s, %s)",
            (investor_id, le["name"], le.get("country"), le["registry"], le.get("registry_id"), le["role"]),
        )
    for field in FACT_FIELDS:
        fact = doc.get(field)
        if fact is None:
            continue
        value = fact.get("value")
        as_of = value.get("as_of") if isinstance(value, dict) else None
        fact_id = conn.execute(
            "insert into core.fact (investor_id, field, value, method, as_of) values (%s, %s, %s, %s, %s) returning fact_id",
            (investor_id, field, Jsonb(value) if value is not None else None, fact["method"], as_of or None),
        ).fetchone()[0]
        for ref in fact.get("evidence", []):
            conn.execute("insert into core.fact_evidence values (%s, %s) on conflict do nothing", (fact_id, ev[ref]))
    for f in doc.get("funds", []):
        conn.execute(
            """insert into core.fund (investor_id, name, size_amount, currency, event, event_date, evidence_id)
               values (%s, %s, %s, %s, %s, %s, %s)""",
            (investor_id, f.get("name") or "(unnamed fund)", f.get("size_amount"), f.get("currency"), f.get("event"),
             f.get("event_date") or None, ev.get(f.get("evidence"))),
        )
    for inv in doc.get("investments", []):
        conn.execute(
            """insert into core.investment (investor_id, company, company_country, announced_on, round, round_amount,
                   currency, evidence_id) values (%s, %s, %s, %s, %s, %s, %s, %s)""",
            (investor_id, inv["company"], inv.get("company_country"), inv.get("date") or None, inv.get("round"),
             inv.get("round_amount"), inv.get("currency"), ev.get(inv.get("evidence"))),
        )


def read(path: Path) -> tuple[dict | None, list[str]]:
    try:
        doc = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as e:
        return None, [f"cannot read JSON: {e}"]
    return doc, validate(doc, path)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--check", nargs="+", type=Path, metavar="FILE", help="validate these files without loading")
    args = parser.parse_args()

    if args.check:
        bad = 0
        for path in args.check:
            _, problems = read(path.resolve())
            print(f"{path}: {'OK' if not problems else 'INVALID'}")
            for prob in problems:
                print(f"  - {prob}")
            bad += bool(problems)
        return 1 if bad else 0

    files = sorted(DOSSIER_DIR.rglob("*.json"))
    loaded, invalid = 0, []
    with connect() as conn:
        for path in files:
            doc, problems = read(path)
            if problems:
                invalid.append((path, problems))
                continue
            try:
                with conn.transaction():
                    insert_dossier(conn, doc, path)
            except psycopg.Error as e:  # a constraint the validator does not know about yet
                invalid.append((path, [f"database rejected it: {e.diag.message_primary or e}"]))
                continue
            loaded += 1
        keys = [json.loads(p.read_text(encoding="utf-8")).get("investor_key") for p in files]
        removed = conn.execute("delete from core.investor where not (investor_key = any(%s))", (keys,)).rowcount
    for path, problems in invalid:
        print(f"INVALID {path.relative_to(PROJECT_ROOT)}")
        for prob in problems:
            print(f"  - {prob}")
    print(f"{loaded} dossiers loaded, {len(invalid)} invalid, {removed} removed (no longer on disk)")
    return 1 if invalid else 0


if __name__ == "__main__":
    sys.exit(main())
