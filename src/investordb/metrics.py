"""Compute the pilot metrics from Postgres and write docs/pilot-metrics.md.

    uv run python -m investordb.metrics

Run after load_dossiers, the fetchers, build and review load. Every number in the output is
recomputed from the database, so the file can be regenerated at any time.
"""

import datetime as dt
import math
import sys
from collections import Counter, defaultdict

from investordb.db import PROJECT_ROOT, connect

OUT = PROJECT_ROOT / "docs" / "pilot-metrics.md"
S15_LIST_SIZE_SQL = "select count(*) from raw.jerrs_entity where list_name = 's15_managers' and snapshot_date = (select max(snapshot_date) from raw.jerrs_entity where list_name = 's15_managers')"


def wilson(k: int, n: int, z: float = 1.96) -> tuple[float, float]:
    if n == 0:
        return 0.0, 0.0
    p = k / n
    centre = (p + z * z / (2 * n)) / (1 + z * z / n)
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / (1 + z * z / n)
    return max(0.0, centre - half), min(1.0, centre + half)


def pct(k: int, n: int) -> str:
    return f"{100 * k / n:.0f}%" if n else "–"


def ci(k: int, n: int) -> str:
    lo, hi = wilson(k, n)
    return f"{pct(k, n)} ({k}/{n}; 95% CI {100 * lo:.0f}–{100 * hi:.0f}%)" if n else "–"


def table(headers: list[str], rows: list[list]) -> str:
    lines = ["| " + " | ".join(headers) + " |", "|" + "---|" * len(headers)]
    lines += ["| " + " | ".join("" if v is None else str(v) for v in r) + " |" for r in rows]
    return "\n".join(lines)


def source_of(tag: str) -> str:
    return "co-investor snowball" if tag.startswith("co-investor") else tag


def main() -> int:
    with connect() as conn:
        q = lambda sql, *a: conn.execute(sql, a).fetchall()
        inv = q("""select investor_key, pilot, decision, investor_type, rule_codes, discovered_via, status, published,
                          confidence, last_activity_date, is_corporate, is_public, is_accelerator from core.investor""")
        cards = {r[0]: r for r in q("""select investor_key, ticket_method, capital_method, capital_basis, sector_focus,
                                              stage_focus, geography_focus, evidence_count, evidence_verified
                                       from core.investor_card""")}
        evidence = q("""select i.pilot, e.source_class, c.quote_found, c.http_status
                        from core.evidence e join core.investor i using (investor_id)
                        left join lateral (select quote_found, http_status from core.evidence_check c
                            where c.url = e.url and c.quote_sha256 = encode(sha256(convert_to(e.quote, 'UTF8')), 'hex')
                            order by checked_at desc limit 1) c on true""")
        checks = q("""select c.check_code, c.passed, count(*) from core.check_result c join core.investor i using (investor_id)
                      where i.decision = 'include' group by 1, 2 order by 1, 2""")
        reviews = q("select investor_key, sample, verdict, checks, notes from core.review")
        s15_size = conn.execute(S15_LIST_SIZE_SQL).fetchone()[0]
        roster = dict(zip(("cvca", "cvca_assoc"), conn.execute(
            """select count(*), count(*) filter (where member_class = 'associate') from raw.cvca_member
               where fetched_on = (select max(fetched_on) from raw.cvca_member)""").fetchone()))

    out = [f"# Pilot metrics\n\nGenerated {dt.datetime.now(dt.timezone.utc):%Y-%m-%d %H:%M} UTC by "
           "`uv run python -m investordb.metrics` from the Postgres database. Snapshot date 2026-10-25, "
           "activity window from 2024-10-25.\n"]

    # 1. Overview
    rows = []
    for pilot in ("cz-vc", "sk-reference", "cz-s15-sample"):
        recs = [r for r in inv if r[1] == pilot]
        dec = Counter(r[2] for r in recs)
        rows.append([pilot, len(recs), dec["include"], sum(r[7] or False for r in recs), dec["exclude"], dec["unverified"]])
    out.append("## 1. Screening outcome\n\n" + table(["Pilot", "Candidates", "Included", "Published", "Excluded", "Unverified"], rows))
    codes = Counter()
    for r in inv:
        if r[2] != "include":
            for c in r[4]:
                if not c.startswith("I"):
                    codes[(r[1], c)] += 1
    out.append("\nExclusion reasons (a record can carry several):\n\n" + table(
        ["Pilot", "Code", "Records"], [[p, c, n] for (p, c), n in sorted(codes.items())]))

    # 2. Completeness of published records
    pub = [r for r in inv if r[7]]
    n = len(pub)
    method_counts = {f: Counter(cards[r[0]][i] for r in pub) for f, i in (("ticket", 1), ("capital", 2))}
    basis = Counter(cards[r[0]][3] for r in pub if cards[r[0]][3])
    out.append("\n## 2. Field completeness of published records\n\n" + f"Published records: **{n}** "
               f"(CZ {sum(r[1] == 'cz-vc' for r in pub)}, SK {sum(r[1] == 'sk-reference' for r in pub)}); "
               f"flags: corporate {sum(r[10] for r in pub)}, public {sum(r[11] for r in pub)}, accelerator {sum(r[12] for r in pub)}.\n")
    rows = [["Sector focus", pct(sum(bool(cards[r[0]][4]) for r in pub), n), "", ""],
            ["Stage focus", pct(sum(bool(cards[r[0]][5]) for r in pub), n), "", ""],
            ["Geography focus", pct(sum(bool(cards[r[0]][6]) for r in pub), n), "", ""]]
    for field in ("ticket", "capital"):
        m = method_counts[field]
        rows.append([f"{field.title()} size" if field == "ticket" else "Capital / AUM",
                     pct(n - m["not_disclosed"] - m[None], n),
                     ", ".join(f"{k} {v}" for k, v in m.most_common() if k not in ("not_disclosed", None)),
                     m["not_disclosed"]])
    out.append(table(["Field", "Filled", "By method", "Not disclosed"], rows))
    out.append("\nCapital basis: " + ", ".join(f"{k} {v}" for k, v in basis.most_common()) + ".")

    # 3. Evidence
    ev_pub_pilots = [e for e in evidence if e[0] in ("cz-vc", "sk-reference")]
    cls = Counter(e[1] for e in ev_pub_pilots)
    checked = [e for e in evidence if e[2] is not None]
    out.append("\n## 3. Evidence and automated verification\n\n" + table(
        ["Measure", "Value"],
        [["Evidence items (all pilots)", len(evidence)],
         ["Source class mix (CZ+SK pilots)", ", ".join(f"{k} {pct(v, len(ev_pub_pilots))}" for k, v in sorted(cls.items()))],
         ["Pages retrieved by script", pct(len(checked), len(evidence))],
         ["Quotes found verbatim/fuzzy on retrieved pages (V3)", ci(sum(bool(e[2]) for e in checked), len(checked))],
         ["Quotes on pages a script cannot retrieve (JS, paywall, bot block)", len(evidence) - len(checked)]]))
    out.append("\nAutomated checks on included records (passed / failed / not applicable):\n\n" + table(
        ["Check", "Passed", "Failed", "n/a"],
        [[code, d.get(True, 0), d.get(False, 0), d.get(None, 0)] for code, d in
         sorted({c: {p: k for cc, p, k in checks if cc == c} for c, _, _ in checks}.items())]))

    # 4. Discovery sources
    per_source = defaultdict(lambda: Counter())
    for r in inv:
        if r[1] not in ("cz-vc", "sk-reference"):
            continue
        for tag in set(map(source_of, r[5])):
            per_source[(r[1], tag)]["candidates"] += 1
            per_source[(r[1], tag)]["published"] += bool(r[7])
    out.append("\n## 4. Discovery sources: how many candidates each produced and how many survived\n\n"
               "Candidates = screened records that name the source in `discovered_via`.\n\n" + table(
        ["Pilot", "Source", "Candidates", "Published", "Precision as a VC filter"],
        [[p, s, c["candidates"], c["published"], pct(c["published"], c["candidates"])]
         for (p, s), c in sorted(per_source.items(), key=lambda kv: (kv[0][0], -kv[1]["candidates"]))]))
    if roster["cvca"]:
        cvca_pub = per_source[("cz-vc", "cvca")]["published"]
        out.append(f"\nAgainst the full CVCA roster ({roster['cvca']} members, {roster['cvca_assoc']} of them associates — "
                   f"mostly law firms, auditors, banks and advisers screened out by their CVCA category without a dossier), "
                   f"CVCA membership is a VC filter with **{pct(cvca_pub, roster['cvca'])}** precision ({cvca_pub}/{roster['cvca']}).")

    # 5. Registry labels
    s15 = [r for r in inv if r[1] == "cz-s15-sample"]
    s15_vc = sum(1 for r in s15 if r[2] == "include" and r[3] == "vc")
    s15_company = sum(1 for r in s15 if r[3] is not None)
    s15_unver = sum(1 for r in s15 if r[2] == "unverified")
    nbs = [r for r in inv if r[1] == "sk-reference" and "nbs-register" in r[5]]
    nbs_vc = sum(1 for r in nbs if r[7])
    lo, hi = wilson(s15_vc, len(s15))
    out.append("\n## 5. Registry labels as filters\n\n" + table(
        ["Register", "Screened", "Active startup VC", "Any company investor (incl. inactive, PE, FO)", "Unverifiable"],
        [[f"ČNB §15 list ('osoba rizikového kapitálu'), random sample of {s15_size}", len(s15), ci(s15_vc, len(s15)),
          pct(s15_company, len(s15)), pct(s15_unver, len(s15))],
         ["NBS registered AIF managers / self-managed AIFs (SK, all)", len(nbs), ci(nbs_vc, len(nbs)),
          pct(sum(1 for r in nbs if r[3] is not None), len(nbs)), pct(sum(1 for r in nbs if r[2] == 'unverified'), len(nbs))]]))
    if s15:
        out.append(f"\nExtrapolated to the full §15 list of {s15_size}: about **{round(s15_vc / len(s15) * s15_size)}** "
                   f"active startup VC managers (95% CI {round(lo * s15_size)}–{round(hi * s15_size)}).")

    # 6. Slovak recall
    ref = [r for r in inv if r[1] == "sk-reference" and r[7]]
    ref_all = [r for r in inv if r[1] == "sk-reference" and r[3] == "vc"
               and (r[7] or (r[2] == "exclude" and "E7" in r[4]))]
    sources = Counter(tag for r in ref for tag in set(map(source_of, r[5])))
    sources_all = Counter(tag for r in ref_all for tag in set(map(source_of, r[5])))
    out.append("\n## 6. Recall of discovery sources against the Slovak reference set\n\n"
               f"Reference set: {len(ref)} published (active) Slovak VC investors, and {len(ref_all)} real Slovak VC "
               "investors when inactive ones (E7) are counted too.\n\n" + table(
                   ["Source", "Finds (active)", "Recall (active)", "Finds (all real VCs)", "Recall (all real VCs)"],
                   [[s, sources[s], pct(sources[s], len(ref)), k, pct(k, len(ref_all))] for s, k in sources_all.most_common()]))

    # 7. Reviews
    m1 = [r for r in reviews if r[0] in {p[0] for p in pub}]
    m2 = [r for r in reviews if r[0] not in {p[0] for p in pub}]
    decided = [r for r in m1 if r[2] != "unsure"]
    out.append("\n## 7. Independent review\n\n" + table(
        ["Measure", "Value"],
        [["M1 record precision (published records judged correct)", ci(sum(r[2] == "correct" for r in decided), len(decided))],
         ["M1 unsure", sum(r[2] == "unsure" for r in m1)],
         ["M2 wrongly excluded (excluded/unverified judged to be an active VC)",
          ci(sum(r[3].get("decision_correct") is False for r in m2), len([r for r in m2 if r[3].get('decision_correct') is not None]))]]))
    field_rows = []
    for field in ("sector_focus", "stage_focus", "ticket_size", "capital", "activity_evidence"):
        vals = Counter(r[3].get(field) for r in m1)
        judged = vals["correct"] + vals["incorrect"]
        field_rows.append([field, ci(vals["correct"], judged), vals["unverifiable"], vals["not_applicable"]])
    for field in ("real_entity", "invests_in_companies", "active_24m", "type_correct", "decision_correct"):
        vals = Counter(r[3].get(field) for r in m1)
        field_rows.append([field, ci(vals[True], vals[True] + vals[False]), vals[None], ""])
    out.append("\nM1 accuracy by check:\n\n" + table(["Check", "Accuracy", "Unverifiable / null", "n/a"], field_rows))
    issues = [f"- `{r[0]}` ({r[2]}): {r[4]}" for r in reviews if r[2] != "correct" or any(
        v in ("incorrect", False) for v in r[3].values())]
    if issues:
        out.append("\nReviewer findings:\n\n" + "\n".join(issues))

    OUT.write_text("\n".join(out) + "\n", encoding="utf-8")
    print(f"wrote {OUT.relative_to(PROJECT_ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
