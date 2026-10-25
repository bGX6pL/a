# Task A pilot results: VC investors in Czechia, Slovakia as reference

Snapshot date 2026-10-25; "active" = dated investment or fund close since 2024-10-25. Plan and rules:
[task-a-plan.md](task-a-plan.md). Every number below is regenerated from Postgres by
`uv run python -m investordb.metrics` into [pilot-metrics.md](pilot-metrics.md), which also lists every
published record with its source and date.

The pilot ran in two rounds: a first build under the original rules, an independent review, then
corrections plus a second screening pass under the revised rules and a second independent review.

## Summary

- **191 candidates screened** from public sources: 99 Czech VC candidates, 52 Slovak candidates and a
  random sample of 40 of the 406 Czech §15 sub-threshold fund managers.
- **33 investors published** (29 Czech, 4 Slovak). Each has type, sector and stage focus (100%), ticket
  size (79%) and capital (82%) or an explicit *not disclosed*, and a dated, source-linked proof of
  investing since 2024-10-25. Every filled value links to a verbatim quote.
- **Automated verification:** all 1,102 quotes on retrievable pages were found again on the live page
  (one URL could not be fetched); the Czech/Slovak legal entities of every included record match
  ARES / RÚZ / NBS.
- **Measured precision (independent review):**

  | | Round 1 (rules v1) | Round 2 (rules v2) |
  |---|---|---|
  | Published records judged correct | **83%** (25/30; CI 66–93%) | **100%** (28/28; CI 88–100%) |
  | Activity evidence correct | 83% | 100% |
  | Capital correct | 64% | 80% |
  | Ticket / stage / sector correct | 91% / 93% / 97% | 88% / 93% / 100% |
  | Excluded records that were active in-scope VCs | 10% (2/20) | 0% (0/12; CI 0–24%) |

  Every one of the 33 published records has been reviewed and judged correct in its latest round
  (28 in round 2, 5 unchanged since round 1).
- **Registry labels are not investor filters:** only 5% of the ČNB §15 list ("osoba rizikového
  kapitálu") and of the NBS registered managers are active startup VCs.
- **Worldwide expansion:** about **€290k** in year 1 (range €180k–575k), then about €90k a year —
  [global-expansion-cost.md](global-expansion-cost.md).

## 1. What was done

| Step | How | Re-run with |
|---|---|---|
| Registers | ČNB JERRS (§15 list, 406; licensed investment companies, 62), ARES (every Czech IČO), NBS export (33,823 entities), RÚZ (Slovak entities with balance sheets), CVCA member profiles (84) | `investordb.fetch.jerrs / ares / nbs / ruz / cvca` |
| Candidates | CVCA members, desk-research seed list, deal news (CzechCrunch, Lupa, Forbes, Vestbee, The Recursive), SIH / EIF / NRI programme releases, co-investors seen in deals (second pass), the ČNB and NBS registers | dossiers record `discovered_via` |
| Dossiers | 191 JSON dossiers by analyst agents: legal entities, type, focus, ticket, capital, funds, investments, decision with rule codes, 1,090 evidence items with verbatim quotes | `investordb.load_dossiers` |
| Automated checks | V1 registry match, V3 quote re-found on the re-fetched page (numbers must match exactly), V4 dated activity in window (no launches, no year-only dates), V5 capital basis consistent with fund events, V6 plausibility, V7 de-duplication, M1 review gate | `investordb.fetch.evidence`, `investordb.build` |
| Independent review | 6 reviewer agents in two rounds: 58 published-record reviews (M1), 32 exclusion reviews (M2), protocol in [review-protocol.md](review-protocol.md) | `investordb.review sample / load` |
| Corrections | round-1 findings fixed under the revised rules; 18 further published records re-audited; 36 more Czech candidates screened | dossiers carry `[revision …]` notes |
| Metrics | funnel, completeness, verification, source precision, registry labels, Slovak recall, review accuracy per round | `investordb.metrics` |

The result table is `core.investor_card` (one row per investor; published = true for the 33). It is
exported with every other table by `uv run python -m investordb.export --verify` (PostgreSQL, CSV,
JSON Lines, Parquet, SQLite, DuckDB, MySQL and SQL Server scripts).

## 2. Who made it in, who did not

| | Czechia | Slovakia | ČNB §15 sample |
|---|---|---|---|
| Candidates | 99 | 52 | 40 |
| Published | **29** | **4** | (measurement only; 2 real VCs) |
| Out of VC scope: PE, debt, family offices, angel networks, private holdings (S1) | 42 | 3 | — |
| Out of the country (S2: no local office or no local deal) | 7 | 1 | — |
| Not company investors: real estate, trading, crypto (E3) / service firms (E1) | 4 / 2 | 17 / — | 15 / — |
| Funds-of-funds (E5) / debt (E4) | 2 / 2 | — / 1 | 1 / — |
| Inactive (E7, alone or with another code) | 9 | 18 | 1 |
| Unverifiable (E8) | 8 | 14 | 21 |

Slovakia is small and mostly state-funded: of 15 real Slovak VC investors only 4 have a verified
investment since October 2024 (VFF, SIH's direct-investment unit, Zero One Hundred, Seed Starter of
Slovenská sporiteľňa). Most SIH-backed funds ended their investment periods in 2023, and Neulogy's
latest dated deal is from September 2024 (now unverified).

## 3. Accuracy and what the review changed

**Round 1** found five wrong records and two classes of field error:

| Record | Error | Fix |
|---|---|---|
| Luminova Ventures | only a fund "opened to investors" | rule: launches are not activity (V4) → unverified |
| Neulogy Ventures | "Invested: 2025" turned into 2025-01-01; real deal 2024-09 | rule: no year-only dates (V4) → unverified |
| Aspire11 | late-stage / pre-IPO secondaries | rule: type by dominant activity → PE, out of the VC pilot |
| RockawayX | mainly a liquid-crypto hedge-fund manager | rule: type by dominant activity → E3 |
| United Founders | Prague office, but no Czech investments | rule: local office *and* local deal → S2 |
| Capital (8 records) | first closes, targets, raised-to-date amounts as fund size; public sizes marked not disclosed | `interim_close` basis; V5 requires a final close for "fund size" |
| Wrongly excluded | JSK Investments' VC fund (inside a PE group); Orbit (venture debt) | brand rule → own record; E4 covers venture debt |

The re-audit under the new rules also found that **Presto Ventures' recent deals and EUR 150m fund
belong to Tech Horizons**, a separate firm spun out of Presto in April 2025; Presto itself is now
inactive (E7), Tech Horizons is excluded as S2 (no Czech portfolio company yet).

**Round 2** reviewed every published record that was new, changed or not yet reviewed (28) and 12 new or
changed exclusions: no record-level error and no wrong exclusion. The remaining field errors (10 of 133
judged field values) are mostly **public figures left as *not disclosed***: capital 5 (older fund sizes
of DEPO and StartupYard, IP Lab's EIF commitment, JSK VC's internal capital, Budeto's backer money),
ticket 3 (ZAKA and Budeto ranges reported in the news; VFF's maximum includes follow-ons), stage 2
(i&i Bio, Tachles). Consistency checks cannot catch an omission; it needs a "search for older or
interim figures" step in extraction.

**After round 2** the flagged values were fixed from the reviewers' sources (8 of 10, each with a
verbatim quote): DEPO, IP Lab and JSK VC now show their committed capital as `interim_close`,
StartupYard its 2017 EUR 1m fund (marked as old), ZAKA its EUR 250–300k ticket, VFF its first ticket of
EUR 0.4–2m (up to 7m with follow-ons), and the stages of i&i Bio and Tachles are derived from their
cited deals. Budeto's two values stay *not disclosed*: its sources only say "mid hundreds of thousands"
and "high single-digit millions" of CZK, with no number that can be quoted. Capital is now filled for
82% of published records (70% before).

## 4. Which sources find real investors

| Source | Precision as a VC filter | Notes |
|---|---|---|
| Desk-research seed list (CZ) | 69% (11/16) | built from ecosystem reports |
| Deal news (CZ) | 33% (14/43) | best source of dated proof; every co-investor in a deal becomes a candidate, so precision falls as the net widens |
| Co-investor snowball / second pass (CZ) | 8–15% | mostly angels, family offices, private holdings and foreign funds |
| CVCA association | 11% of 84 members | full members are mostly PE; associates are law firms, auditors, banks |
| ČNB §15 list ("osoba rizikového kapitálu") | 5% (2/40; CI 1–17%) | 15 trading / crypto / real estate, 21 without public footprint; ≈20 active VCs among the 406 (CI 6–67) |
| NBS registered managers (SK) | 5% (2/41; CI 1–16%) | Slovak VC managers are registered under consulting codes (NACE 70.22), so an industry-code filter would miss them |

Recall against the hand-built Slovak reference set (15 real VCs, 4 active): deal news and co-investor
snowballing each find all 4 active ones; the SIH programme pages and the seed list find 3; the NBS
register finds 2 (10 of the 15 when inactive VCs are counted).

**Coverage in Czechia.** The second pass screened all 36 remaining names seen in deals and found only 3
more active VCs (Jet Venture 1, Moondust Ventures, Budeto) plus JSK's VC fund from the review; the rest
were angels, family offices, private holdings, foreign funds or inactive vehicles. 25 of today's 29
published Czech VCs (86%) were already found in the first pass, so the sources are close to exhausted
for institutional VCs with a public deal record. Remaining
gaps: investors that appear only in paywalled databases or not in any public deal, and the ~20 VCs the
§15 sample suggests exist among sub-threshold managers (most of which are among the 29 already).

## 5. Proof of investing per record

[pilot-metrics.md §8](pilot-metrics.md#8-published-records-and-their-proof-of-investing) lists all 33
published investors with the latest dated activity and its source, e.g.:

| Investor | Latest dated activity | Source |
|---|---|---|
| Credo Ventures | 2026-06-02 investment in Picogrid | lupa.cz |
| KAYA | 2026-10-06 Series A of Sensible Biotechnologies | own release |
| Inven Capital (ČEZ, corporate) | 2026-09-09 Wint Series D | prnewswire.com |
| JSK Investments VC Fund I | 2026-10-09 investment in MintNeuro | cc.cz |
| Slovak Investment Holding (public) | 2026-09-22 investment in VisionFlow | sih.sk |

Each record's full evidence (URL, publisher, publication date, quote, source class, retrieval and check
result) is in `core.evidence` and `core.evidence_check`.

## 6. Limits of this pilot

- **Analysts and reviewers were AI agents, not people.** Reviewers worked independently from the
  dossiers (round-2 reviewers did not see round-1 verdicts) and found real, specific errors, but their
  own accuracy has not been calibrated against a human. The review files are plain JSON
  (`data/curated/reviews/`); a person can confirm or overturn any verdict and re-run `review load`,
  `build` and `metrics`.
- **The fixes after round 2 have not been re-reviewed.** They were checked against the reviewers'
  notes and every new quote passes V3, but no third review round was run; Budeto's ticket and capital
  remain *not disclosed* although rough amounts are public in words.
- **Borderline calls flagged by reviewers:** SIH typed as public VC although most of its activity is
  guarantees and fund-of-funds; IP Lab Ventures' only portfolio stakes are nominal co-founder shares;
  Moondust so far invests its owners' money; Czech Founders VC now does follow-ons only.
- **Access:** web-search quotas ran out in several agent runs (later research relied on direct page
  fetches); ČNB JERRS shows a CAPTCHA after a few requests (two lists imported from earlier fetches,
  the rest need a browser download or the certificate-based WS JERRS); paywalls (CzechCrunch Insider,
  PitchBook) hide some deal dates.
- **Watch list:** Tech Horizons and United Founders become includes with their first Czech deal;
  StartGuide (SG Two), Neulogy, Luminova and PurposeTech with a dated close or deal.

## 7. Next steps

1. Add a "look for older or interim figures" step to extraction, so capital and ticket omissions are
   caught before review.
2. Human spot-check of 10–15 reviewer verdicts to calibrate the AI reviewers.
3. Request WS JERRS access (certificate) for the remaining ČNB lists.
4. First expansion step: Poland, Austria and Hungary (CEE first, where incumbents are weakest), at the
   unit costs in [global-expansion-cost.md](global-expansion-cost.md).
