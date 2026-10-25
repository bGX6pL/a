# Task A plan: a reliable database of private-market investors

Snapshot date for all rules below: **2026-10-25**. Activity window: **24 months** (since 2024-10-25).
Background research: [reports/Investor data sources and competitors.md](../reports/Investor%20data%20sources%20and%20competitors.md).

## 1. What the database promises

1. Every published record is a **real investor that demonstrably invests in private companies** —
   not a service provider, platform, shell or random company.
2. Every field the task requires (type, sector focus, typical investments, ticket size, total capital)
   is either filled with a value **backed by a cited public source and a date**, or explicitly marked
   *not publicly disclosed*. Nothing is filled from guesswork.
3. Every record cites at least one **dated proof of investing** from the last 24 months.
4. Only publicly available data is used; every dataset is reproducible by a fetch script, lives in
   Postgres and can be exported to other databases (`investordb.export`).
5. Precision beats breadth: when in doubt a candidate stays in the *unverified* pool rather than the
   published set.

## 2. Unit of record

- **Investor** = the entity that decides to put capital into companies: the management firm (GP)
  for funds, the family office, the individual angel, or the private investment holding.
- **Fund vehicles are child records**, linked to their manager, never separate investors. (The SEC
  shows ~13.5 PE funds per adviser; without this rule counts inflate more than tenfold.)
- **Legal entities** (management companies, fund SICAVs, GP companies) are identifiers of the
  investor, with registry IDs (IČO, LEI, regulator ID). One brand → one investor record.

## 3. Investor types (closed set)

| Type | Definition | Typical evidence |
|---|---|---|
| `vc` | Pooled or dedicated capital invested as minority equity / convertibles in early- and growth-stage private companies. Flags: `corporate` (CVC arm), `public` (state-backed, invests directly), `accelerator` (programme that takes equity) | Fund close, portfolio page, round announcements |
| `pe` | Funds investing in mature private companies, typically majority / buyout or large growth minority | Fund close, acquisitions |
| `family_office` | Entity managing the wealth of one (SFO) or several (MFO) families that invests directly in private companies | Deal announcements naming the FO, LP lists |
| `angel` | Natural person investing own money directly in startups, in a professional capacity | ≥2 independent dated deal mentions |
| `angel_network` | Club / syndicate through which angels invest (the network organises, members invest) | Network-announced deals |
| `private_investor` | Large private investor or private investment holding investing its principals' own capital directly (not via third-party funds) | Annual reports, deal announcements |

A record has one primary type; mixed models (e.g. a group running funds *and* investing own
capital) get the type of the dominant activity plus `secondary_types`.

## 4. Who is in: inclusion rules (all must hold)

| Code | Rule | How it is checked |
|---|---|---|
| **I1 Identity** | Exists as a verifiable entity: a legal entity in an official register (business register ID, LEI or financial-regulator register), or for a natural person ≥2 independent public sources showing professional investing | Registry lookup by ID (ARES, RÚZ, NBS, JERRS, GLEIF) |
| **I2 Invests in companies** | Makes equity or quasi-equity investments (shares, convertibles, SAFEs) in private operating companies; at least one named portfolio company | Portfolio page, deal announcement |
| **I3 Active** | ≥1 dated activity event within 24 months: a new investment, a fund (first or final) close, or a fund-level commitment with an open investment period | Dated evidence; `last_activity_date ≥ 2024-10-25` |
| **I4 Own or managed capital** | Invests its own or managed capital (not arranging other people's deals) | Business model on own website / registry purpose |
| **I5 Required fields addressed** | Type, sector focus and stage focus filled; ticket size and capital filled *or* marked not disclosed | Completeness check |

## 5. Who is out: exclusion rules (any one excludes, with a reason code)

| Code | Excluded | Examples |
|---|---|---|
| **E1** | Service providers | Advisers, M&A boutiques, law and audit firms, fund administrators, depositaries |
| **E2** | Intermediaries | Crowdfunding and investment platforms, brokers, placement agents (their investors may qualify; the platform does not) |
| **E3** | Non-company strategies | Real-estate, hedge / algorithmic trading, listed equities and bonds, crypto trading, commodities, UCITS and pension funds |
| **E4** | Debt-only lenders | Banks, direct lending and mezzanine-only funds (kept in a separate bucket, not published as investors) |
| **E5** | LP-only investors | Funds-of-funds and public LPs that do not invest directly in companies (EIF, NRB fund-of-funds) — used as *evidence sources* |
| **E6** | Captive vehicles | SPVs and holdings investing only in their own group or a single company |
| **E7** | Inactive | No activity in 24 months and no open investment period ("zombie") — kept with status `inactive`, not published as active |
| **E8** | Unverifiable | I1 or I2 cannot be shown from public sources — stays in the `unverified` pool |
| **E9** | Non-investing programmes | Accelerators / incubators that provide no capital, grant and guarantee schemes |
| **E10** | Duplicates | Fund vehicles and alternative legal entities merged into the investor record |
| **E11** | Private persons without professional footprint | Natural persons with no public professional-capacity investing record (GDPR: no profiling of private individuals) |

Pilot scope codes (the candidate *is* a real investor and keeps its type, but is outside a pilot):
**S1** — not the pilot's investor type (e.g. PE or debt in a VC pilot); **S2** — no office or activity
in the pilot country.

## 6. Fields and evidence standard

| Field | Content | Rule |
|---|---|---|
| `investor_type` (+ flags) | Section 3 | Must be supported by the investor's own description or a regulator status |
| `sector_focus` | From a closed list of 18 sectors + `generalist` | Stated by the investor, or derived from ≥3 portfolio companies |
| `stage_focus` | pre_seed, seed, series_a, series_b, growth, buyout | Stated, or derived from observed rounds |
| `geography_focus` | Countries / regions | Stated |
| `ticket_size` | min / max, currency | `stated` (investor or programme terms) or `derived` (from observed deals: round sizes the investor participated in, labelled as such) |
| `capital` | Amount, currency, basis (`aum`, `latest_fund_size`, `cumulative_fund_sizes`, `balance_sheet`, `regulatory_filing`), as-of date | Stated in a dated source; for regulated vehicles from filings / financial statements |
| `investments` | Company, date, round, round size | Each with its own dated evidence |
| `funds` | Vehicle, size, close date, status | Each with its own dated evidence |

**Every value is linked to evidence**: URL, publisher, publication date, retrieval timestamp, a
verbatim quote (≤300 characters) and a source class:

| Class | Source | Weight |
|---|---|---|
| **A** | Regulator / official register / statutory filing | Highest; proves identity and legal status |
| **B** | The investor's own publication (website, press release, annual report) | Proves stated focus, ticket, fund size |
| **C** | Independent media, LPs and fund-of-funds releases, co-investor announcements | Proves activity independently |
| **D** | Directories and self-reported profiles (association member pages, founder lists) | Discovery and fallback only; always labelled `self-reported` with its date |

When sources conflict, the newest A/B/C value wins and the conflict is recorded; D never overrides A–C.

## 7. How authenticity and classification are verified

Automated checks — scripts, re-runnable at any time:

| Check | What it proves |
|---|---|
| **V1 Registry match** | The legal entity exists and is active (ARES, RÚZ, NBS, JERRS, GLEIF) and its name matches |
| **V2 Evidence liveness** | Every cited URL is re-fetched; the raw copy and its SHA-256 are stored (`meta.fetched_file`) |
| **V3 Quote match** | The cited quote is actually present in the fetched page or PDF — the claim is in the source, not invented |
| **V4 Date check** | Evidence date parsed; activity evidence inside the 24-month window |
| **V5 Cross-source consistency** | Type / capital / ticket agree across sources; conflicts flagged |
| **V6 Plausibility** | Ticket ≤ fund size; fund and ticket sizes within ranges for the type and region; dates not in the future |
| **V7 De-duplication** | Same registry ID, LEI or website domain → one investor |

Manual verification — on a sample:

- **M1 Record review**: an independent reviewer opens the sources of a stratified random sample of
  published records and answers: real entity? invests in companies? active in 24 months? type right?
  Each field matches its source?
- **M2 Exclusion review**: a sample of excluded / unverified candidates is reviewed the same way to
  estimate wrongly rejected investors.
- **Metrics**: record precision = correct published records / reviewed published records;
  field accuracy per field; false-exclusion rate; recall against a hand-built reference set.
- **Confidence score** per record from evidence classes and passed checks; records under the
  threshold are not published.

## 8. What can be obtained from public sources: estimate

Basis: figures from the research report (NVCA/PitchBook 2026 Yearbook, SEC Form PF Q4 2025, Invest
Europe 2025, Deloitte 2024, FINTRX 2026, UNH CVR 2024, EBAN 2024, GCV 2025, Altrata 2025) combined with
the public-footprint gradient (institutions ≥80% visible, family offices 20–50%, angels ≤10%). These
are planning estimates; the pilot replaces the CEE assumptions with measured values.

| Type | Active universe (basis) | Publicly verifiable share | Expected records | Capital / AUM public | Expected precision |
|---|---|---|---|---|---|
| VC (institutional) | 7,000–12,000 firms: US ≈2,450 active (2,984 existing minus 18% zombies), Europe ≈1,000 (≈55% of Invest Europe's 1,854 PE+VC firms), rest of world assumed 1–2× US+Europe | 80–90% | **5,600–10,000** | US ≈100% via Form ADV; elsewhere 50–80% via fund-close releases | ≥95% |
| Corporate VC | 3,068 corporations investing (GCV 2025) | ~90% | **~2,700** | <20% (rarely disclosed) | ≥95% |
| PE | 5,000–8,000 firms (SEC: 2,047 registered PE advisers; ~7,000 worldwide per AIC, weak) | 85–90% | **4,300–7,000** | US via ADV; elsewhere 60–80% | ≥95% |
| Family offices | ≈8,030 SFOs + ≈3,000 MFOs; ~60% invest directly | 20–50% | **1,300–3,300** | 10–30% | ~85% |
| Angels and networks | 445,535 active US angels; 47,610 European angels in ~350 networks | ≤10%, limited further by GDPR rule E11 | **5,000–20,000** individuals + **~1,000** networks | <5% (personal wealth is not public) | ~80–85% |
| Large private investors | 556,850 UHNW individuals; direct investors unknown | low | **1,000–3,000** | 20–40% (group reports) | ~85% |
| **Total** | | | **≈21,000–47,000** | | |

Error band: ±10–15% on every count — published reference figures themselves disagree by 5–10%,
and curated databases miss ~15% of rounds. Activity decays ~15% a year, so the dataset needs an
annual re-verification cycle (`last_activity_date` drives it).

For comparison, incumbents count every cap-table name (PitchBook 423K–667K "investors", Crunchbase
~300K, Dealroom ~250K); the database here is deliberately smaller and stricter.

## 9. Pipeline

```
discovery ──► candidates ──► screening (I/E rules) ──► evidence & enrichment ──► automated checks V1–V7
                                                                                       │
                       published snapshot ◄── confidence threshold ◄── manual sample M1/M2
```

- **Discovery** (scripts): regulator registers (SEC ADV/Form D, ESMA, ČNB JERRS, NBS), association
  member lists, fund-of-funds commitment lists, deal news, co-investors seen in deals (snowball).
- **Evidence & enrichment**: per candidate, the investor's website and dated announcements. At scale
  this is LLM-assisted extraction that must return verbatim quotes; V3 rejects anything the source
  does not contain. In the pilot this step is done by analysts and recorded in JSON dossiers.
- Everything is stored in Postgres: `raw.*` (as fetched), `core.*` (investors, legal entities, funds,
  investments, facts, evidence, decisions, reviews), `meta.*` (fetch runs, files, link checks).

## 10. Pilot design: VC investors in Czechia, Slovakia as reference

**Scope**: investors of type `vc` (including CVC, public VC and investing accelerators) with an office
in the country and investment activity in it, active in the last 24 months.

**Steps**

1. **Registers** (scripts): ČNB JERRS lists (§15 sub-threshold managers, investment companies),
   ARES for every Czech IČO, NBS daily register export, RÚZ for every Slovak IČO, CVCA member profiles.
   JERRS answers repeated automated requests with a CAPTCHA; the fetcher stops there and imports list
   pages saved from a browser instead (production route: WS JERRS with a ČNB certificate).
2. **Candidates**: union of CVCA members, the research seed list, public LP releases (EIF, NRI, NPO,
   SIH), deal news and co-investors seen in dossiers.
3. **Dossiers**: for every candidate, a JSON dossier with legal entities, type, focus, ticket, capital,
   funds, investments and evidence quotes; inclusion decision with rule codes.
4. **Registry precision test**: a reproducible random sample (40) of the ČNB §15 list, which carries
   the legal label "osoba rizikového kapitálu" (venture-capital person) on ~400 entities, is screened
   to measure how many are real startup investors — i.e. how good a registry label is as a filter.
5. **Automated checks** V1–V7 over all dossiers.
6. **Manual review** (M1) of a random sample of included records and (M2) of excluded candidates.
7. **Slovakia reference set**: the complete, hand-built list of active Slovak VC investors, used to
   measure recall of the automated discovery sources.

**Measured outputs**: candidate → included funnel per source, record precision, field accuracy,
field completeness (share with stated ticket / capital), registry-label precision, Slovak recall,
time and cost per record.

## 10a. Revisions after the pilot

The independent review (results: [task-a-pilot-results.md](task-a-pilot-results.md)) showed where the
rules above were too loose. These changes apply from now on; the automated ones are in `investordb.build`.

| Finding in review | Rule change | Enforced by |
|---|---|---|
| Funds "opened to investors" and year-only portfolio labels counted as activity | **I3**: only dated investments, first/final closes and LP commitments count; a fund launch does not; a date must be at least month-precise in its source (1 January placeholders are ignored) | V4 (script) |
| First closes, targets and amounts raised so far were published as fund size (capital accuracy 64%) | **Capital basis** must state the close status; "latest fund size" means a final close; otherwise the record shows `first_close` / `target` / `launch` | V5 (script) |
| A public fund size (older fund, earlier year) was marked "not disclosed" | `not_disclosed` only after checking earlier funds; otherwise record the latest public figure with its date | analyst rule + review |
| A crypto / hedge-fund manager with a VC sleeve and a late-stage secondaries investor were typed `vc` | **Type by dominant activity**: crypto / hedge-dominant managers → E3 even with a VC sleeve; late-stage / pre-IPO / secondaries → `pe` | analyst rule + review |
| A fund with a Prague office but no Czech investments was in the Czech pilot | **Scope**: office in the country *and* at least one portfolio company or deal there; otherwise S2 | analyst rule + review |
| A separately branded VC fund inside a PE group was excluded with the group | **Brand rule**: a separately branded VC fund with its own team is its own investor record | analyst rule |
| Venture-debt fund closes treated inconsistently | **E4** covers debt-focused funds including venture debt, even with a legacy equity book (policy decision) | analyst rule |
| Reviewer-judged errors | A record judged incorrect is withheld until fixed | M1 gate (script) |

Calibration of section 8 from the pilot (Czech and Slovak VC):

| Planning assumption | Pilot measurement |
|---|---|
| Institutional VC: ≥80% publicly verifiable | Every active CZ/SK VC found had a website plus dated public deal evidence |
| Capital / AUM public for 50–80% outside the US | Filled for 82% of published records after the round-2 fixes; 64% of reviewed values right under rules v1, 80% under rules v2 (remaining errors were public figures missed, since fixed) |
| Ticket size public | Filled for 79%; 88–91% accurate |
| Precision ≥95% for VC | Round 1 (rules v1): 83% (25/30). Round 2 (rules v2, after corrections): 100% (28/28; CI 88–100%), 0/12 wrong exclusions. Capital 64% → 80%, activity evidence 83% → 100% |
| Registry labels as filters | ČNB §15 and NBS registered managers: 5% are active startup VCs → discovery seeds only |

## 11. Cost of worldwide expansion

Estimated from the pilot's measured volumes and unit costs, multiplied by the counts in section 8:
[global-expansion-cost.md](global-expansion-cost.md) — about **€290k** in year 1 (range €180k–575k)
and **€90k** a year afterwards in the central case.
