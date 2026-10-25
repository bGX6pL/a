# Task A pilot results: VC investors in Czechia, Slovakia as reference

Snapshot date 2026-10-25; "active" = dated investment or fund close since 2024-10-25. Plan and rules:
[task-a-plan.md](task-a-plan.md). Every number below is regenerated from Postgres by
`uv run python -m investordb.metrics` into [pilot-metrics.md](pilot-metrics.md), which also lists every
published record with its source and date.

## Summary

- **154 candidates screened** from public sources: 62 Czech VC candidates, 52 Slovak candidates and a
  random sample of 40 of the 406 Czech §15 sub-threshold fund managers.
- **30 investors published** (26 Czech, 4 Slovak). Each has type, sector and stage focus (100%), ticket
  size (80%) and capital (67%) or an explicit *not disclosed*, and a dated, source-linked proof of
  investing since 2024-10-25. Every filled value links to a verbatim quote.
- **Automated verification:** 790 of 791 quotes were found again on their live pages, all cited pages
  were retrievable, and the Czech/Slovak legal entities of every included record matched ARES / RÚZ / NBS.
- **Measured precision (independent review of 30 published records): 83%** (25/30, 95% CI 66–93%).
  Field accuracy: sector 97%, stage 93%, ticket 91%, activity evidence 83%, **capital 64%**.
  Wrongly excluded: 2 of 20 reviewed exclusions (10%, both policy borderlines).
- After the review gate and the rules tightened from its findings, the published set is 24
  reviewer-confirmed records plus 6 unreviewed: **≈97% expected precision**.
- **Registry labels are not investor filters:** only 5% of the ČNB §15 list ("osoba rizikového
  kapitálu") and of the NBS registered managers are active startup VCs.
- **Worldwide expansion:** about **€290k** in year 1 (range €180k–575k), then about €90k a year —
  [global-expansion-cost.md](global-expansion-cost.md).

## 1. What was done

| Step | How | Re-run with |
|---|---|---|
| Registers | ČNB JERRS (§15 list, 406; licensed investment companies, 62), ARES (583 Czech IČOs), NBS export (33,823 entities), RÚZ (71 Slovak entities with balance sheets), CVCA member profiles (84) | `investordb.fetch.jerrs / ares / nbs / ruz / cvca` |
| Candidates | CVCA members, desk-research seed list, deal news (CzechCrunch, Lupa, Forbes, Vestbee, The Recursive), SIH / EIF / NRI programme releases, co-investors seen in deals, the ČNB and NBS registers | dossiers record `discovered_via` |
| Dossiers | 154 JSON dossiers by analyst agents, one per candidate: legal entities, type, focus, ticket, capital, funds, investments, decision with rule codes, 791 evidence items with verbatim quotes | `investordb.load_dossiers` |
| Automated checks | V1 registry match, V3 quote re-found on the re-fetched page (numbers must match exactly), V4 dated activity in window, V5 capital is a final close, V6 plausibility, V7 de-duplication, confidence score | `investordb.fetch.evidence`, `investordb.build` |
| Independent review | 3 reviewer agents: 30 published records (M1), 20 exclusions (M2), protocol in [review-protocol.md](review-protocol.md) | `investordb.review sample / load` |
| Metrics | funnel, completeness, verification, source precision, registry labels, Slovak recall, review accuracy | `investordb.metrics` |

The result table is `core.investor_card` (one row per investor; published = true for the 30). It is
exported with every other table by `uv run python -m investordb.export --verify` (PostgreSQL, CSV,
JSON Lines, Parquet, SQLite, DuckDB, MySQL and SQL Server scripts).

## 2. Who made it in, who did not

| | Czechia | Slovakia | ČNB §15 sample |
|---|---|---|---|
| Candidates | 62 | 52 | 40 |
| Included (rules I1–I5) | 31 | 5 | 2 |
| Published after checks and review | **26** | **4** | (measurement only) |
| Out of VC scope (PE, debt, family office, private holdings: S1/S2) | 24 | 4 | — |
| Not company investors (real estate, trading, crypto: E3) / service firms (E1) | 1 / 4 | 16 / — | 15 / — |
| Inactive (E7, alone or with another code) | 3 | 18 | 1 |
| Unverifiable (E8) | 0 | 14 | 21 |

Slovakia is small and mostly state-funded: of 16 real Slovak VC investors only 4 have a verified
investment since October 2024 (VFF, SIH's direct-investment unit, Zero One Hundred, Seed Starter of
Slovenská sporiteľňa); most SIH-backed funds ended their investment periods in 2023, and Neulogy's
latest dated deal turned out to be September 2024.

## 3. Accuracy (independent review)

| Measure | Result |
|---|---|
| Published records that hold up (real, invests, active, right type, right decision) | **83%** (25/30; 95% CI 66–93%) |
| Excluded records that were in fact active in-scope VCs | 10% (2/20; 95% CI 3–30%) |
| Field accuracy | sector 97%, stage 93%, ticket 91%, activity evidence 83%, capital 64% |
| Real entity / invests in companies | 100% / 100% |

The five wrong records and what they teach:

| Record | Error | Now caught by |
|---|---|---|
| Luminova Ventures | only a fund "opened to investors", no close or deal | V4 (launch no longer counts) |
| Neulogy Ventures | "Invested: 2025" turned into 2025-01-01; the real deal was 2024-09 | V4 (year-only dates ignored) |
| Aspire11 | late-stage / pre-IPO secondaries, not VC | dominant-activity type rule + review |
| RockawayX | mainly a liquid-crypto hedge-fund manager with a VC sleeve | dominant-activity type rule + review |
| United Founders | Prague office, but no Czech investments | local-investment scope rule + review |

The weakest field is **capital**: first closes, targets and amounts raised so far were published as fund
sizes (5 cases), and public fund sizes were marked *not disclosed* (3). V5 now accepts a "fund size" only
when it is a final close and otherwise publishes the figure with its real basis (first close, launch,
target); it catches 5 of the 8 capital errors without a person. All rule changes are in the plan,
section [10a](task-a-plan.md#10a-revisions-after-the-pilot).

## 4. Which sources find real investors

| Source | Precision as a VC filter | Notes |
|---|---|---|
| Deal news (CZ) | 63% (12/19) | best source of dated proof; Czech outlets are mostly free |
| Desk-research seed list (CZ) | 75% (12/16) | built from ecosystem reports |
| CVCA association | 10% of 84 members (24% of those screened) | full members are mostly PE; associates are law firms, auditors, banks |
| ČNB §15 list ("osoba rizikového kapitálu") | 5% (2/40; CI 1–17%) | 15 trading / crypto / real estate, 21 without any public footprint; ≈20 active VCs among the 406 (CI 6–67) |
| NBS registered managers (SK) | 5% (2/41; CI 1–16%) | Slovak VC managers are registered under consulting codes (NACE 70.22), so an industry-code filter would miss them |

Recall against the hand-built Slovak reference set (16 real VCs, 4 active): deal news and co-investor
snowballing each find all 4 active ones; the SIH programme pages and the seed list find 3; the NBS
register finds 2 (10 of the 16 when inactive VCs are counted). No single source is enough; news plus
programme lists plus snowballing covers the set.

Estimated coverage in Czechia: 26 published plus about 10 further likely-active VCs named by the
analysts but not yet screened (the shared web-search budget ran out during the run), plus JSK
Investments' VC fund from M2. That puts this single pass at **about 65–75%** of the Czech active VC
universe, consistent with the 30–50 estimated before the pilot.

## 5. Proof of investing per record

[pilot-metrics.md §8](pilot-metrics.md#8-published-records-and-their-proof-of-investing) lists all 30
published investors with the latest dated activity and its source, e.g.:

| Investor | Latest dated activity | Source |
|---|---|---|
| Credo Ventures | 2026-06-02 investment in Picogrid | lupa.cz |
| KAYA | 2026-10-07 Series A of Sensible Biotechnologies | cc.cz |
| Inven Capital (ČEZ, corporate) | 2026-09-09 Wint Series D | prnewswire.com |
| Slovak Investment Holding (public) | 2026-09-22 investment in VisionFlow | sih.sk |

Each record's full evidence (URL, publisher, publication date, quote, source class, retrieval and check
result) is in `core.evidence` and `core.evidence_check`.

## 6. Limits of this pilot

- **Analysts and reviewers were AI agents, not people.** The reviewers worked independently from the
  dossiers and found real, specific errors, but their own accuracy has not been calibrated against a
  human. The review files are plain JSON (`data/curated/reviews/`); a person can confirm or overturn
  any verdict and re-run `review load` and `metrics`.
- **Six published records were outside the review sample** (J&T Ventures, KAYA, N1, Presto Ventures,
  Seed Starter ČS, Tilia Impact Ventures); the 97% figure assumes they err at the sample rate.
- **Search budget:** the agents' shared web-search quota ran out midway, so later dossiers relied on
  direct fetches of known sites; discovery is incomplete (section 4).
- **Access:** ČNB JERRS showed a CAPTCHA after a few requests; two list pages fetched before it are
  imported, the other lists need a browser download or the certificate-based WS JERRS. Paywalls
  (CzechCrunch Insider) and bot blocks limit some sources.
- **Two policy calls remain open:** whether venture debt counts as VC activity (Orbit Capital) and how
  to treat a VC fund inside a PE group (JSK Investments). The plan now decides both; the dossiers have
  not yet been redone.

## 7. Next steps

1. Redo the five incorrect and three borderline records under the revised rules, and screen the ~25
   named but unscreened Czech candidates (fresh search budget needed).
2. Human spot-check of 10–15 reviewer verdicts to calibrate the AI reviewer.
3. Request WS JERRS access (certificate) for the remaining ČNB lists.
4. Then the first expansion step: Poland, Austria and Hungary (CEE first, where incumbents are weakest),
   at the unit costs in [global-expansion-cost.md](global-expansion-cost.md).
