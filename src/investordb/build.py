"""Run the automated checks (V1, V3-V7) over every loaded dossier, score it, and rebuild core.investor_card.

    uv run python -m investordb.build

Order of a full refresh: load_dossiers -> fetch.ares -> fetch.ruz -> fetch.nbs -> fetch.evidence -> build.

Checks written to core.check_result (passed true/false, or null when not applicable):
  V1  registry match: a Czech/Slovak legal entity exists in ARES / RÚZ / NBS / JERRS under a matching name
      and is not dissolved
  V3  quote match: share of evidence quotes found on the re-fetched page (fetch.evidence)
  V4  activity: latest fund event or investment on/after the window start, its evidence verified,
      and no evidence published long before the event it reports
  V5  consistency: a "latest fund size" capital value matches a listed fund
  V6  plausibility: ticket <= capital, sane magnitudes
  V7  de-duplication: no other publishable record shares an IČO or website domain
Confidence = 0.30 identity + 0.30 verified activity + 0.25 quote-match rate + 0.15 plausibility/consistency.
A record is published when decision = include, status = active, pilot is publishable and confidence >= 0.6.
"""

import datetime as dt
import re
import sys
import unicodedata
import urllib.parse
from collections import defaultdict

from rapidfuzz import fuzz

from investordb.db import connect
from investordb.load_dossiers import ACTIVITY_WINDOW_START

PUBLISH_THRESHOLD = 0.6
PUBLISHABLE_PILOTS = {"cz-vc", "sk-reference"}
ACTIVITY_EVENTS = {"first_close", "final_close", "launch", "commitment"}
NAME_NOISE = re.compile(
    r"osoba rizikov[eé]ho kapit[aá]lu|spr[aá]vca podlimitn[yý]ch rizikov[yý]ch fondov|investi[cč]n[ií] spole[cč]nost|"
    r"investi[cč]n[yý] fond s premenliv[yý]m z[aá]kladn[yý]m imanim|s\.?\s?r\.?\s?o\.?|a\.?\s?s\.?|spol\.|k\.?s\.?|"
    r"v\.?o\.?s\.?|j\.?\s?s\.?\s?a\.?|sicav|sicar|se\b|druzstvo|z\.?\s?s\.?|o\.?\s?p\.?\s?s\.?|k\.s\.i\.l\.",
    re.I)


def norm_name(name: str) -> str:
    name = unicodedata.normalize("NFKD", name or "").encode("ascii", "ignore").decode().lower()
    name = NAME_NOISE.sub(" ", name)
    return re.sub(r"[^a-z0-9]+", " ", name).strip()


def domain(url: str | None) -> str | None:
    if not url:
        return None
    host = urllib.parse.urlsplit(url if "//" in url else "https://" + url).netloc.lower()
    return host.removeprefix("www.") or None


def load(conn):
    q = lambda sql, *a: conn.execute(sql, a).fetchall()
    data = {
        "investors": q("""select investor_id, investor_key, pilot, decision, investor_type, website, name, is_corporate,
                                 is_public, is_accelerator, hq_country, rule_codes from core.investor"""),
        "entities": q("""select investor_id, name, registry, case when registry_id ~ '^[0-9]+$'
                                then lpad(registry_id, 8, '0') else registry_id end, role from core.legal_entity"""),
        "ares": {r[0]: r[1:] for r in q("""select ico, http_status, payload->>'obchodniJmeno', payload->>'datumZaniku'
                                           from raw.ares_subject""")},
        "ruz": {r[0]: r[1] for r in q("select ico, payload->>'nazovUJ' from raw.ruz_unit where payload is not null")},
        "nbs": {r[0]: r[1] for r in q("""select nbs_id, name from raw.nbs_entity
                                         where snapshot_date = (select max(snapshot_date) from raw.nbs_entity)""")},
        "jerrs": {r[0]: r[1] for r in q("select distinct on (ico) ico, name from raw.jerrs_entity order by ico, snapshot_date desc")},
        "evidence": q("""select e.evidence_id, e.investor_id, e.url, e.source_class, e.published_on, c.quote_found
                         from core.evidence e
                         left join lateral (
                             select quote_found from core.evidence_check c
                             where c.url = e.url and c.quote_sha256 = encode(sha256(convert_to(e.quote, 'UTF8')), 'hex')
                             order by checked_at desc limit 1) c on true"""),
        "facts": q("""select f.investor_id, f.field, f.value, f.method, f.as_of,
                             (select array_agg(e.url order by e.evidence_id) from core.fact_evidence fe
                              join core.evidence e using (evidence_id) where fe.fact_id = f.fact_id)
                      from core.fact f"""),
        "funds": q("select investor_id, name, size_amount, currency, event, event_date, evidence_id from core.fund"),
        "investments": q("select investor_id, company, announced_on, round, evidence_id from core.investment"),
    }
    return data


def registry_check(entities, d) -> tuple[bool | None, str, list[str]]:
    checked, verified, notes, ids = 0, 0, [], []
    for _, name, registry, rid, _ in entities:
        ids.append(f"{registry}:{rid}")
        if registry not in ("CZ-ICO", "SK-ICO") or not rid:
            continue
        candidates = []
        if registry == "CZ-ICO":
            ares = d["ares"].get(rid)
            if ares and ares[0] == 200:
                if ares[2]:
                    notes.append(f"{rid} dissolved {ares[2]}")
                    checked += 1
                    continue
                candidates.append(ares[1])
            candidates.append(d["jerrs"].get(rid))
        else:
            candidates += [d["ruz"].get(rid), d["nbs"].get(rid)]
        candidates = [c for c in candidates if c]
        checked += 1
        if not candidates:
            notes.append(f"{rid} not found in fetched registers")
            continue
        score = max(fuzz.token_set_ratio(norm_name(name), norm_name(c)) for c in candidates)
        if score >= 80:
            verified += 1
        else:
            notes.append(f"{rid} name mismatch ({name!r} vs {candidates[0]!r}, {score:.0f})")
    if not checked:
        return None, "no Czech/Slovak registry ID to check", ids
    return verified > 0, f"{verified}/{checked} entities verified" + (f"; {'; '.join(notes)}" if notes else ""), ids


def main() -> int:
    with connect() as conn:
        d = load(conn)
        ev_by_inv = defaultdict(list)
        ev_by_id = {}
        for row in d["evidence"]:
            ev_by_inv[row[1]].append(row)
            ev_by_id[row[0]] = row
        facts = defaultdict(dict)
        for inv, field, value, method, as_of, urls in d["facts"]:
            facts[inv][field] = (value, method, as_of, urls or [])
        ents, funds, invs = defaultdict(list), defaultdict(list), defaultdict(list)
        for row in d["entities"]:
            ents[row[0]].append(row)
        for row in d["funds"]:
            funds[row[0]].append(row)
        for row in d["investments"]:
            invs[row[0]].append(row)

        # V7 inputs: shared IČOs / domains among publishable records
        owners = defaultdict(set)
        for inv_id, key, pilot, *_ in d["investors"]:
            if pilot in PUBLISHABLE_PILOTS:
                for _, _, registry, rid, _ in ents[inv_id]:
                    if rid:
                        owners[f"{registry}:{rid}"].add(key)
        site_owners = defaultdict(set)
        for inv_id, key, pilot, _, _, website, *_ in d["investors"]:
            if pilot in PUBLISHABLE_PILOTS and domain(website):
                site_owners[domain(website)].add(key)

        results, cards = [], []
        for (inv_id, key, pilot, decision, itype, website, name, corp, public, accel, country, rule_codes) in d["investors"]:
            checks = []
            v1, v1_detail, registry_ids = registry_check(ents[inv_id], d)
            checks.append(("V1", v1, v1_detail))

            evid = ev_by_inv[inv_id]
            checked = [e for e in evid if e[5] is not None]
            found = sum(1 for e in checked if e[5])
            rate = found / len(evid) if evid else 0.0
            checks.append(("V3", (found == len(evid)) if checked else None,
                           f"{found}/{len(evid)} quotes found on re-fetched pages ({len(evid) - len(checked)} pages not retrievable)"))

            events = [(f[5], f"fund {f[4]}: {f[1]}", f[6]) for f in funds[inv_id] if f[5] and f[4] in ACTIVITY_EVENTS]
            events += [(i[2], f"investment: {i[1]}" + (f" ({i[3]})" if i[3] else ""), i[4]) for i in invs[inv_id] if i[2]]
            events.sort(key=lambda e: e[0], reverse=True)
            last = events[0] if events else None
            status = "unknown" if not last else ("active" if last[0] >= ACTIVITY_WINDOW_START else "inactive")
            last_ev = ev_by_id.get(last[2]) if last else None
            activity_verified = bool(last_ev and last_ev[5] and last_ev[3] in "ABC")
            predating = [e for e in events if (ev := ev_by_id.get(e[2])) and ev[4] and ev[4] < e[0] - dt.timedelta(days=31)]
            checks.append(("V4", (status == "active" and activity_verified and not predating) if last else None,
                           f"last activity {last[0]} ({last[1]}); evidence {'verified' if activity_verified else 'not verified by script'}"
                           + (f"; {len(predating)} event(s) dated after their evidence" if predating else "") if last else "no dated activity"))

            capital = facts[inv_id].get("capital")
            ticket = facts[inv_id].get("ticket_size")
            cap_v = capital[0] if capital and isinstance(capital[0], dict) else None
            tic_v = ticket[0] if ticket and isinstance(ticket[0], dict) else None
            v5 = None
            if cap_v and cap_v.get("basis") == "latest_fund_size":
                sizes = [float(f[2]) for f in funds[inv_id] if f[2] is not None and f[3] == cap_v.get("currency")]
                v5 = any(abs(s - float(cap_v["amount"])) <= 0.05 * float(cap_v["amount"]) for s in sizes) if sizes else None
            checks.append(("V5", v5, "capital matches a listed fund" if v5 else ("no listed fund to compare" if v5 is None else "capital differs from every listed fund size")))

            problems = []
            if cap_v and not (1e5 <= float(cap_v.get("amount") or 0) <= 1e11):
                problems.append(f"capital {cap_v.get('amount')} outside 100k-100bn")
            if tic_v:
                lo, hi = tic_v.get("min"), tic_v.get("max")
                if lo is not None and lo < 1000:
                    problems.append(f"ticket min {lo} < 1,000")
                if cap_v and hi and tic_v.get("currency") == cap_v.get("currency") and hi > float(cap_v["amount"]):
                    problems.append("ticket max above capital")
            checks.append(("V6", not problems if (cap_v or tic_v) else None, "; ".join(problems) or "ok"))

            dups = sorted({k for rid in registry_ids for k in owners.get(rid, set())} | site_owners.get(domain(website), set()) - {key})
            dups = [k for k in dups if k != key]
            checks.append(("V7", not dups if pilot in PUBLISHABLE_PILOTS else None,
                           f"shares an IČO or domain with {', '.join(dups)}" if dups else "unique"))

            identity = 0.30 if v1 else (0.15 if v1 is None and any(e[3] in "AB" and e[5] for e in evid) else 0.0)
            activity = 0.30 if activity_verified and status == "active" else (0.15 if status == "active" else 0.0)
            sanity = 0.15 * (0.0 if (checks[4][1] is False or checks[3][1] is False) else 1.0)
            confidence = round(identity + activity + 0.25 * rate + sanity, 3)
            published = (decision == "include" and status == "active" and pilot in PUBLISHABLE_PILOTS
                         and confidence >= PUBLISH_THRESHOLD and checks[5][1] is not False)
            results += [(inv_id, code, passed, detail) for code, passed, detail in checks]

            def fv(field):
                f = facts[inv_id].get(field)
                return f[0] if f else None

            def first_url(field):
                f = facts[inv_id].get(field)
                return f[3][0] if f and f[3] else None

            cards.append((
                inv_id, key, pilot, name, itype,
                [n for n, on in (("corporate", corp), ("public", public), ("accelerator", accel)) if on],
                country, website, decision, rule_codes, status, last[0] if last else None, last[1] if last else None,
                last_ev[2] if last_ev else None, fv("sector_focus"), fv("stage_focus"), fv("geography_focus"),
                tic_v.get("min") if tic_v else None, tic_v.get("max") if tic_v else None,
                tic_v.get("currency") if tic_v else None, ticket[1] if ticket else None,
                cap_v.get("amount") if cap_v else None, cap_v.get("currency") if cap_v else None,
                cap_v.get("basis") if cap_v else None, cap_v.get("as_of") if cap_v else None,
                capital[1] if capital else None, first_url("sector_focus"), first_url("ticket_size"),
                first_url("capital"), registry_ids, v1, len(evid), found, confidence, published,
            ))
            conn.execute("update core.investor set last_activity_date = %s, status = %s, confidence = %s, published = %s "
                         "where investor_id = %s", (last[0] if last else None, status, confidence, published, inv_id))

        with conn.cursor() as cur:
            cur.execute("delete from core.check_result")
            cur.executemany("insert into core.check_result (investor_id, check_code, passed, detail) values (%s, %s, %s, %s)", results)
            cur.execute("delete from core.investor_card")
            cur.executemany(
                f"insert into core.investor_card values ({', '.join(['%s'] * len(cards[0]))}, now())" if cards else "select 1",
                cards)
        conn.commit()
        n_pub = sum(1 for c in cards if c[-1])
        print(f"{len(cards)} records checked, {n_pub} published")
    return 0


if __name__ == "__main__":
    sys.exit(main())
