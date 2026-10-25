# Cost of expanding the database worldwide

Estimate as of 2026-10-25. Prices: Claude API list prices from platform.claude.com/docs/en/about-claude/pricing
(Opus 5.5 $4 / $20 per million input / output tokens, Sonnet 5.5 $2 / $10, Haiku 5.5 $0.10 / $0.50;
Batch API −50%; web search $10 per 1,000 searches; web fetch free apart from tokens). Labour at CEE
rates (analyst €35–60/h, engineer €500–700/day). Everything is a range; the central case is in **bold**.

## 1. What the pilot measured (inputs to the model)

| Quantity | Pilot value | Source |
|---|---|---|
| Curated-list candidates per published VC | 2.0 (62 → 31, Czech association, research seed and news) | `docs/pilot-metrics.md` §1, §4 |
| Registry-label candidates per real active VC | ~20 (ČNB §15: 2/40; NBS registered managers: 2/41) | §5 |
| CVCA roster candidates per published VC | ~10 (8/84) | §4 |
| Evidence items per included record | 8.6 (CZ), 14.6 (SK) | database, `core.evidence` |
| Distinct pages per record | ~4–8 | database |
| Extracted text per page | mean 10.4k characters (median 6.7k) ≈ 3k tokens | `core.evidence_check.text_chars` |
| Quotes re-found by script | 790 / 791 | §3 |
| Published records with ticket / capital filled | 78% / 69% | §2 |
| Analyst-agent time | ~1.5 agent-minutes per screened candidate (230 agent-minutes for 154 dossiers, run in parallel) | `data/curated/pilot_costs.json` |
| Review time | ~1 agent-minute per record (51 agent-minutes for 50 reviews); a person needs ~8 minutes | `data/curated/pilot_costs.json` |
| Raw record precision before review | 83% (25/30), capital field 64% | `pilot-metrics.md` §7 |

The pilot used LLM research agents for the analyst step. At scale the same step is done as a fixed
pipeline (scripts fetch pages, a model extracts with verbatim quotes, scripts verify), which is cheaper
and more repeatable; the unit costs below are for that pipeline.

## 2. Volumes worldwide

| | Low | **Central** | High | Basis |
|---|---|---|---|---|
| Published active investors | 21,000 | **32,000** | 47,000 | plan §8 (VC, CVC, PE, family offices, angel networks and visible angels, private investors) |
| Candidates found by discovery | 150,000 | **200,000** | 250,000 | registries (SEC ADV + Form D, Companies House, ESMA, ~30 national regulators), associations, LP lists, news; pilot funnel 2:1 for curated lists, 20:1 for registry labels |
| Candidates left after automated pre-screen (no website, wrong strategy codes, obvious trading / real-estate names, duplicates) | 50,000 | **65,000** | 80,000 | ~2 full dossiers per published record, as in the pilot's curated path |

## 3. Unit costs per candidate

| Step | How | Tokens / calls | Cost per candidate |
|---|---|---|---|
| Pre-screen of every candidate | registry record + homepage text, Haiku 5.5 batch | ~5k in, 0.3k out | $0.0003 |
| Activity search | 3–5 searches for dated deals / fund closes | 3–5 searches | $0.03–0.05 |
| Extraction with verbatim quotes | ~8 pages × 3k tokens, Opus 5.5 batch | ~25k in, 3k out | ~$0.08 (Sonnet 5.5: ~$0.04) |
| Semantic check of each claim (does the quote support the field?) | second model, Sonnet 5.5 batch | ~10 claims × 1.5k | ~$0.02 |
| Script checks (fetch, quote match, registry, dates, plausibility, de-dup) | own code | — | compute only |

## 4. First-year cost

The pilot's raw record precision was 83% (25/30 reviewed) — below the 95% target — so review cannot
be a light 10% sample in year 1. The central case uses what worked in the pilot: an independent LLM
reviewer on every record (it found all the errors reported in `pilot-metrics.md` §7 in ~1 agent-minute
per record), with humans adjudicating every flagged record and auditing a random 10% of the rest.
The high case is full human review.

| Item | Low | **Central** | High | Notes |
|---|---|---|---|---|
| LLM + search | €10k | **€18k** | €30k | §3 × candidates, ×2 for retries and re-runs |
| LLM second review of every published record | €3k | **€5k** | €8k | ~30k tokens per record, Sonnet 5.5 / Opus 5.5 batch |
| Human QA | €60k | **€95k** | €250k | central: 32k records × (30% flagged × 10 min + 10% audit × 8 min) ≈ 2,000 h at ~€45/h; high: every record reviewed by a person (47k × 8 min); regional language skills needed |
| Source connectors | €40k | **€70k** | €140k | ~40 sources (SEC, UK, ESMA, GLEIF, ~30 national registers, main LP disclosures) at 2–5 days each; CAPTCHA'd registers need licensed machine access (e.g. WS JERRS) or manual imports |
| Core platform | €50k | **€75k** | €105k | orchestration, quote-anchored extraction, cross-border entity resolution, review UI, monitoring: 100–150 days |
| Legal | €10k | **€20k** | €30k | GDPR legitimate-interest assessment and notices for natural persons (angels), terms-of-use review per source |
| Infrastructure | €5k | **€7k** | €10k | Postgres, crawler, ~1 TB raw page archive, backups |
| **Total, year 1** | **€180k** | **€290k** | **€575k** | 6–9 months with 3–4 people |

Per published record: about **€9** in the central case (range €4–27).

## 5. Running cost per year

| Item | **Central** | Notes |
|---|---|---|
| Annual re-verification | €10k LLM + €45k QA | every record's activity re-checked each year (active-investor counts fell ~15% a year in 2021–2025); humans only on changed or flagged records |
| Connector maintenance | €30k | ~20% of build per year; registers change formats |
| Infrastructure | €7k | |
| **Total per year** | **≈ €90k** (range €65–150k) | about €3 per record per year |

## 6. What drives the estimate

- **Human QA dominates.** Precision targets (≥95% for VC/PE records) are met by review, not by more
  model calls. The rules tightened after the pilot (no fund launches as activity, final closes only as
  fund size, dominant-activity typing, local-investment scope) already let the scripts catch 2/5 of the
  wrong records and 5/8 of the capital errors without a person; every further error class moved into
  the automated checks cuts the human share.
- **Registry labels are cheap discovery but expensive noise.** At 5% precision (§15 list, NBS register)
  a registry-only approach would need ~20 screens per record; the cheap automated pre-screen is what
  keeps this affordable.
- **Access, not compute, is the risk.** CAPTCHAs (ČNB JERRS), bot blocks, paywalled news and
  JavaScript-only pages limit what scripts can re-verify. Budget for licensed APIs where they exist.
- **Comparison.** Commercial licences cost about $20k–125k per seat per year and forbid redistribution
  (research report); a year-1 build of ~€290k produces an open, source-cited dataset the owner controls.
