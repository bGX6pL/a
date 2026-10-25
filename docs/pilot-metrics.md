# Pilot metrics

Generated 2026-10-25 19:22 UTC by `uv run python -m investordb.metrics` from the Postgres database. Snapshot date 2026-10-25, activity window from 2024-10-25.

## 1. Screening outcome

| Pilot | Candidates | Included | Published | Excluded | Unverified |
|---|---|---|---|---|---|
| cz-vc | 99 | 29 | 29 | 62 | 8 |
| sk-reference | 52 | 4 | 4 | 34 | 14 |
| cz-s15-sample | 40 | 2 | 0 | 17 | 21 |

Exclusion reasons (a record can carry several):

| Pilot | Code | Records |
|---|---|---|
| cz-s15-sample | E3 | 15 |
| cz-s15-sample | E5 | 1 |
| cz-s15-sample | E7 | 1 |
| cz-s15-sample | E8 | 21 |
| cz-vc | E1 | 2 |
| cz-vc | E3 | 4 |
| cz-vc | E4 | 2 |
| cz-vc | E5 | 2 |
| cz-vc | E7 | 9 |
| cz-vc | E8 | 8 |
| cz-vc | S1 | 42 |
| cz-vc | S2 | 7 |
| sk-reference | E10 | 2 |
| sk-reference | E2 | 1 |
| sk-reference | E3 | 17 |
| sk-reference | E4 | 1 |
| sk-reference | E6 | 1 |
| sk-reference | E7 | 18 |
| sk-reference | E8 | 14 |
| sk-reference | S1 | 3 |
| sk-reference | S2 | 1 |

## 2. Field completeness of published records

Published records: **33** (CZ 29, SK 4); flags: corporate 6, public 3, accelerator 2.

| Field | Filled | By method | Not disclosed |
|---|---|---|---|
| Sector focus | 100% |  |  |
| Stage focus | 100% |  |  |
| Geography focus | 97% |  |  |
| Ticket size | 76% | stated 23, self_reported 1, derived 1 | 8 |
| Capital / AUM | 70% | stated 22, derived 1 | 10 |

Capital basis: interim_close 8, aum 6, latest_fund_size 5, balance_sheet 3, cumulative_fund_sizes 1.

## 3. Evidence and automated verification

| Measure | Value |
|---|---|
| Evidence items (all pilots) | 1090 |
| Source class mix (CZ+SK pilots) | A 12%, B 46%, C 35%, D 7% |
| Pages retrieved by script | 100% |
| Quotes found verbatim/fuzzy on retrieved pages (V3) | 100% (1089/1089; 95% CI 100–100%) |
| Quotes on pages a script cannot retrieve (JS, paywall, bot block) | 1 |

Automated checks on included records (passed / failed / not applicable):

| Check | Passed | Failed | n/a |
|---|---|---|---|
| V1 | 32 | 0 | 3 |
| V3 | 35 | 0 | 0 |
| V4 | 35 | 0 | 0 |
| V5 | 12 | 1 | 22 |
| V6 | 31 | 0 | 4 |
| V7 | 33 | 0 | 2 |

## 4. Discovery sources: how many candidates each produced and how many survived

Candidates = screened records that name the source in `discovered_via`.

| Pilot | Source | Candidates | Published | Precision as a VC filter |
|---|---|---|---|---|
| cz-vc | news | 43 | 14 | 33% |
| cz-vc | second-pass | 36 | 3 | 8% |
| cz-vc | cvca | 35 | 9 | 26% |
| cz-vc | co-investor snowball | 20 | 3 | 15% |
| cz-vc | research-seed | 16 | 11 | 69% |
| cz-vc | review-correction | 1 | 1 | 100% |
| cz-vc | eif-portfolio | 1 | 0 | 0% |
| sk-reference | nbs-register | 41 | 2 | 5% |
| sk-reference | research-seed | 19 | 3 | 16% |
| sk-reference | news | 14 | 4 | 29% |
| sk-reference | slovca | 10 | 2 | 20% |
| sk-reference | sih-programmes | 9 | 3 | 33% |
| sk-reference | co-investor snowball | 6 | 4 | 67% |
| sk-reference | startup-report-slovensko | 3 | 1 | 33% |
| sk-reference | eif-portfolio | 2 | 0 | 0% |

Against the full CVCA roster (84 members, 57 of them associates — mostly law firms, auditors, banks and advisers screened out by their CVCA category without a dossier), CVCA membership is a VC filter with **11%** precision (9/84).

## 5. Registry labels as filters

| Register | Screened | Active startup VC | Any company investor (incl. inactive, PE, FO) | Unverifiable |
|---|---|---|---|---|
| ČNB §15 list ('osoba rizikového kapitálu'), random sample of 406 | 40 | 5% (2/40; 95% CI 1–17%) | 10% | 52% |
| NBS registered AIF managers / self-managed AIFs (SK, all) | 41 | 5% (2/41; 95% CI 1–16%) | 29% | 27% |

Extrapolated to the full §15 list of 406: about **20** active startup VC managers (95% CI 6–67).

## 6. Recall of discovery sources against the Slovak reference set

Reference set: 4 published (active) Slovak VC investors, and 15 real Slovak VC investors when inactive ones (E7) are counted too.

| Source | Finds (active) | Recall (active) | Finds (all real VCs) | Recall (all real VCs) |
|---|---|---|---|---|
| research-seed | 3 | 75% | 12 | 80% |
| nbs-register | 2 | 50% | 10 | 67% |
| news | 4 | 100% | 9 | 60% |
| sih-programmes | 3 | 75% | 8 | 53% |
| slovca | 2 | 50% | 5 | 33% |
| co-investor snowball | 4 | 100% | 5 | 33% |
| startup-report-slovensko | 1 | 25% | 2 | 13% |

## 7. Independent review

### Round `review-2026-10` — first build, rules v1 (before the post-pilot revisions)

| Measure | Value |
|---|---|
| M1 record precision (published records judged correct) | 83% (25/30; 95% CI 66–93%) |
| M1 unsure | 0 |
| M2 wrongly excluded active investors (decision wrong, and the reviewer found it invests and is active) | 10% (2/20; 95% CI 3–30%) |
| M2 other decision errors (e.g. unverified that could be decided) | 1 |

M1 accuracy by check:

| Check | Accuracy | Unverifiable / null | n/a |
|---|---|---|---|
| sector_focus | 97% (29/30; 95% CI 83–99%) | 0 | 0 |
| stage_focus | 93% (28/30; 95% CI 79–98%) | 0 | 0 |
| ticket_size | 91% (20/22; 95% CI 72–97%) | 0 | 8 |
| capital | 64% (14/22; 95% CI 43–80%) | 0 | 8 |
| activity_evidence | 83% (25/30; 95% CI 66–93%) | 0 | 0 |
| real_entity | 100% (30/30; 95% CI 89–100%) | 0 |  |
| invests_in_companies | 100% (29/29; 95% CI 88–100%) | 1 |  |
| active_24m | 93% (28/30; 95% CI 79–98%) | 0 |  |
| type_correct | 93% (28/30; 95% CI 79–98%) | 0 |  |
| decision_correct | 83% (25/30; 95% CI 66–93%) | 0 |  |

Findings of this round that the current automated checks catch without a human (once a record is fixed it no longer fails a check, so this is read against the first build after the round):

| Finding | Caught automatically | Records |
|---|---|---|
| Record judged incorrect | 2/5 | aspire11, luminova-ventures, neulogy-ventures, rockawayx, united-founders |
| Capital field incorrect | 0/8 | czech-founders-vc, jic-ventures, purple-ventures, lighthouse-ventures, tachles-vc, tensor-ventures, united-founders, zaka-vc |
| Activity evidence incorrect | 3/5 | luminova-ventures, neulogy-ventures, purposetech, startupyard, y-soft-ventures |

Reviewer findings:

- `aspire11` (incorrect): type/decision: not a VC in the pilot's sense. Its own website (www.aspire11cap.com - exists, the dossier says no website) describes Eternals as 'Direct investments in late-stage and pre-IPO technology companies'; the other sleeve (Tribes, 20-25%) is a fund-of-funds (E5). Observed portfolio is mature global companies (Databricks at USD 190bn valuation, Revolut via an intermediary vehicle per the Partners leaflet, Vinted, VAST Data, Baseten); the EUR 20m Vinted stake (Lupa 2026-06-23) followed Vinted's April 2026 EUR 880m secondary share sale - Vinted raised no primary capital - so it is very likely a secondary purchase. Pension-capital (Rentea ALTUF) late-stage/pre-IPO minority stakes = 'large growth minority' in mature companies -> pe per plan s.3, i.e. S1 for the VC pilot; also no Czech portfolio company found. sector_focus: the leaflet list (agri, engineering, automotive, logistics, IT, hi-tech) is contradicted by the actual 2026 portfolio (fintech, AI/data infra, e-commerce). Ticket EUR 10-30m (leaflet) and capital EUR 515m (own site: '€515M Inaugural fund') are supported. Minor: e7 is a Lupa article by Iva Brejlová, not an Aspire11-authored release (class C, not B).
- `czech-founders-vc` (correct): Homepage confirms pre-seed, EUR 50-350k, CEE, Prague and Bratislava offices; Merchantee (Reflex-led CZK 30m seed extension, CzechCrunch 2026-06-09) verified. capital: a value is public but the record says not disclosed - CzechCrunch 2022-09-07: the AIF raised EUR 10m (~CZK 250m) from 45 founders (target doubled from 5m to 10m and fully raised a month earlier). Sector derived from 3 software/AI companies; the 31-company portfolio is mostly software/AI, so accepted.
- `ip-lab-ventures` (correct): EIF release 2026-09-24 verified: ~EUR 27m NRP commitment to IP Lab Ventures Fund I, target >EUR 50m (Lupa: up to EUR 40m); no close, so capital not_disclosed is acceptable. Ticket up to EUR 1m per Lupa 2026-09-23 (team presentation). stage_focus: marked 'derived' but cited e7/e9 contain no rounds or stage - pre_seed/seed is inferred from the tech-transfer mandate, unsupported by its quotes. I2 is thin: Lupa says IP Lab takes a stake for a financial contribution and 'is part of' MendelFOLD; EIF only says the team 'helped launch' spin-offs; no dated portfolio investment.
- `jic-ventures` (correct): capital: EUR 16m (= CZK 400m) is the fundraising TARGET, not a fund size. CzechCrunch 2026-04-07: 'Fond cílí na velikost 400 milionů korun' and 'aktuálně má již alokovaných 320 milionů korun'; e15 2026-04-07: 'JIC Ventures cílí na celkový objem 400 milionů korun'; JIC's own release adds the fund 'has not yet reached its final close'. No close at 400m found since. Recording 16m as latest_fund_size is a target presented as fund size (committed was ~CZK 320m at launch). Other fields OK: ticket up to EUR 1m stated (JIC, e15, CC); pre-seed/seed stated; FaceUp Series A participation confirmed by JIC release 2026-05-19 (USD 5m is the whole round, labelled as such). public flag: defensible (initiated by public agency JIC, Region is LP) but note public money is only ~10-15% of the fund.
- `purple-ventures` (correct): Brno office, pre-seed/seed, EUR 250-400k initial ticket confirmed on homepage; Kilde (E15 2025-10-27), Fether Labs (Euro.cz 2026-05-27) and Rightcharge rounds verified. capital: CZK 700m is the amount raised to date (Finance.cz 2026-03-12) in a still-open raise toward the EUR 40m target (fundraising to end in 2026); an interim close is presented as latest_fund_size.
- `lighthouse-ventures` (correct): capital: record says not disclosed, but the Fund I (Lighthouse Seed Fund) size is public: Lupa.cz 2019-06-06 'Fond Lighthouse aktuálně operuje s 23 miliony eur' (other 2019 reports: ~CZK 600m incl. EUR 15m via CZFoF/EIF). Fund II (started 2024 per homepage) size is unpublished, so at minimum the Fund I size should have been recorded (funds entry has size null). Other fields verified on lhv.vc: 'B2B Software of various verticals, Fintech, AI', 'From €200k to €1m Investment in a single startup', 'Idea / Seed', Prague offices. Ranketta EUR 1m pre-seed led by LHV (Nov 2025) and Merchantee extension participation (CC 2026-06-09) confirmed.
- `luminova-ventures` (incorrect): active/decision: the only dated event is the fund 'newly opened to investors' (Lupa 2026-01-21; own release: the fund 'is being established' and is 'already working with a pre-selected portfolio') - a fundraising launch, not a first close or an investment, so I3 is not met. No dated deal by Luminova found (searches return nothing). invests_in_companies: unproven - the 7 Israeli portfolio companies are undated and appear to come via the 'strategic partnership' with Awz Global; DeepKeep's seed (May 2024) was led by Awz Ventures and its later investor was OurCrowd (Jan 2026), with no mention of Luminova. Should be unverified (E8), not published. activity_evidence: e8 (DeepKeep page) has no date and does not show a Luminova investment. Ticket/capital not disclosed and nothing public found. Stage 'derived' from the portfolio companies' current stages, which are not Luminova's entry rounds, but consistent with 'Cílí na ranější fáze'.
- `neulogy-ventures` (incorrect): active_24m/activity_evidence: the only in-window event is StratifAI dated '2025-01-01', a placeholder made up from the portfolio label 'Invested: 2025'. The dated public record says Neulogy co-led StratifAI's EUR 1.5m pre-seed announced 2024-09-02 (Signalbase; LinkedIn post), i.e. before the window; StratifAI's next round (EUR 12.5m, 2025-09-30, Picus/Alven) lists existing investors Debiopharm, Arve Capital and C. Haarburger but not Neulogy (GenomeWeb/360Dx, TU Dresden). All other portfolio pages show 2023 or earlier, BeIT/BiteBerry 2024; searches found no 2025-2026 deal or fund close. The EIF list showing an investment period to 14/03/2027 avoids E7 but is not a dated I3 event. decision: under 'precision beats breadth' and I3 this should be unverified, not published - the analyst noted the conflict yet included it. Fields: ticket EUR 200k-3m and EUR 65m AUM are on the own about-us page (AUM undated); sector/stage acceptable.
- `purposetech` (correct): activity_evidence: none of the cited events is a dated in-window investment or fund close. Fund I closed Sep/Oct 2024 (Vestbee 2024-09-25, AIN 2024-10-11) - before 2024-10-25; PT Capital (2026-02-10) is only an announcement of a fund still raising (max EUR 10m, first EUR 4m to be invested from autumn 2026), not a first close; eNOugh and Tingit have no date (Tingit Aug 2024, pre-window). active_24m is still true by inference: 5 investments at the Fund I close (Vestbee 2024-09-25) vs 11 by 2026-02-10 (CzechCrunch) and 13 on the website now, so >=6 new investments fell in the window. Ticket EUR 0.5-1m is PT Capital's planned ticket (fund II not yet investing), while Fund I wrote ~EUR 25-250k tickets (Vestbee profile; CZK 60m over 11-13 companies) - supported by the cited source but describes the next fund, not observed activity. Capital: 'necelych 60 milionu korun' for Fund I supported.
- `rockawayx` (incorrect): type_correct: RockawayX is a ~USD 2bn multi-strategy digital-asset firm whose dominant activity is liquid crypto: Liquid Opportunities long/short fund (Cayman), Market Neutral fund (Liechtenstein), vault curation, validator/infrastructure; in 2026 it acquired hedge fund Relayer Capital and is raising a USD 150m hedge fund (cryptobriefing). The VC arm (VC II USD 125m, which itself buys liquid tokens and other funds) is a minority. Under plan s.3 the primary type follows the dominant activity (E3 crypto trading), with vc at most secondary, so inclusion in the VC pilot is wrong. Fields: VC II USD 125m close Q1 2025 verified (not the 2bn AUM); OnRe USD 5m Series A co-lead and Silhouette pre-seed lead verified.
- `startupyard` (correct): Equity-taking accelerator in Prague; accelerator flag right; Ydoca CZK 500k (CzechCrunch 2025-02-14, verified) keeps it active. ticket_size: min EUR 25k is wrong - FAQ: every startup gets a EUR 45k in-kind convertible note, optionally +EUR 25k cash (total 70k); a 25k-only ticket does not exist (record mixes the cash component with the total-note max). activity_evidence: the latest item (CaseLens, 2026-04-30) is an interview post that shows no investment, amount or batch; the date is the post date and the investment is inferred from the FAQ; CaseLens is Yerevan-based per PitchBook.
- `tachles-vc` (correct): Team page lists Tel Aviv, Prague and Atlanta offices; both managing partners Czech; Boost.space EUR 3m round (CzechCrunch 2025-10-09) names Tachles VC - Czech activity in window. capital: CZK 500m is the closed 'first phase' (CzechCrunch 2024-06-13) of a fund that remained open to further investors - a first close presented as latest_fund_size.
- `tensor-ventures` (correct): capital: EUR 20m is Fund I (opened 2017, 'invested EUR 18.5 million into 20 startups' per Quantum Insider 2024-10-14), labelled latest_fund_size, but a newer fund exists - the Tensor Ventures Co-investment Fund / second fund launched Oct 2024 with a EUR 20m EIF (NPO/RRF) commitment, target EUR 50m, which is the vehicle currently investing. The record keeps only the 50m target and ignores the EIF EUR 20m commitment, so the capital basis/as-of is wrong. stage_focus: seed + series_a from the website, but the current fund is stated as pre-seed ('zhruba 50 startupu ve fazi pre-seed', Lupa 2024-05-14; CC 2024-05-15) and two of the four recorded deals are pre-seed (QurieGen, Valka.ai) - pre_seed missing. Ticket EUR 250k-1m is CVCA 2020 self-reported (labelled as such); no newer stated figure found. Activity: led Pointee seed (CC 2026-04-15) and Repsense (2025-12-17) - confirmed. Office: GP/fund in Luxembourg, Czech contact in Praha-Karlin; team Czech - in scope.
- `united-founders` (incorrect): decision_correct: pilot scope requires an office AND investment activity in Czechia. Fund is a Luxembourg entity (E15 2026-06-07), managing partner Paris-based; all named deals are foreign (AMI Labs FR, Oligoplus FR, Peak Quantum DE, Wonderful IL); Horky (E15 2026-06-07): no Czech investment yet, one 'very likely' this year. Only Czech links: Prague advisory s.r.o., a Prague partner, mostly CZ/SK LPs. ticket_size: EUR 300k-1m contradicted by own site (initial EUR 100k-1m, follow-on up to 2m) and E15 four days later (EUR 150k-1m). capital: EUR 30m is the first close (Sifted, Nov 2025) and still the interim amount in June 2026 with fundraising open ~1 more year toward the EUR 80m target - not a fund size.
- `y-soft-ventures` (correct): Brno CVC of Y Soft; IoT/Industry 4.0/cyber focus and Robotwin in portfolio confirmed on ysoft.com/ventures. activity_evidence: the stated date 2025-09-11 is a later CzechCrunch article date ('letos'); the EUR 1.25m pre-seed with Y Soft Ventures was announced by 2 July 2025 (EIT Jumpstarter; seedtable lists 2025-06) - still inside the window, so active_24m holds. Corporate flag kept, but note fund II has outside LPs (Frolik, Livesport ~25% of two funds, Soitron founders). No closed fund size or ticket public (only old targets).
- `zaka-vc` (correct): Prague-registered fund vehicle and Prague office (site lists Silicon Valley/London/Prague/Bratislava); Vetstor pre-seed (Apr 2025) and EUR 1m round (CzechCrunch 2025-12-09: 'Ty' = Zaka VC and Purple Ventures) verified; Readmio Feb 2026 also seen (Vestbee). capital: EUR 10.5m is the June 2024 first closing of a EUR 15m-target fund (tech.eu 2024-07-19 'first closing') presented as latest_fund_size; the investor's own site now states fund size '17M' (Fund 1: 17M, 8M invested, 46 companies). Ticket: nothing public per startup (EUR 130k is the LP minimum).
- `abris-capital` (correct): S1 holds: control/buyout PE, EUR 30-75m tickets, 'Control investments' (strategy page verified). Also S2: Warsaw-based, focus Poland/Romania, no Czech office found. Capital: the record says not_disclosed, but the CVCA profile cited in the analyst notes publicly lists Fund III EUR 502m and Fund II EUR 450m (class D, 2020). It could have been filled as self_reported, so it is marked incorrect (minor; exclusion unaffected).
- `aetna-investments-management` (correct): E3 confirmed on aetnainvestments.sk: global macro strategy on world capital markets (economic cycle / Minsky); no private-company or startup investing.
- `aimc` (correct): Exclusion holds (E3/E7; E10 is a reasonable group-overlap code). The manager's only fund, Across Heritage Fund, mainly holds tradable securities and has been in liquidation since 2026-04-30 (RÚZ). Its small non-tradable stakes are in IPM GF vehicles, not startups. No VC activity found.
- `emun-investicni-spolecnost` (correct): Exclusion holds. E1 is roughly right; E5 fits its private-markets product better. EMUN launched Emun Global Unicorns in Oct 2025 (e15.cz and cc.cz, 2025-10-16; >CZK 200m, mostly EMUN and family-office clients), an evergreen fund buying exposure to late-stage unicorns (OpenAI, SpaceX, Revolut, Anthropic, Databricks...). Per cc.cz it invests 'through funds or platforms' that hold the stakes, i.e. indirectly / fund-of-funds, not as a VC writing primary tickets. No direct startup investing by EMUN found.
- `ipm-growth` (correct): E7 holds. CB Insights lists IPM Growth deals up to Hilo EV (seed, 2022-06-14); earlier InoBat 2020, Wildcat Discovery 2019, Tachyum 2018; HQ London. IPM Group did join InoBat's Series C (release dated 2024-12-20, inside the window), but InoBat is majority-owned by IPM Holding / Marián Boček (IPM co-founder and an IPM Growth MD), so this is a captive group stake (E6), not independent VC activity. Tachyum's Oct-2025 Series C names no investor. Correction to the notes: the InfraPartners link is not spurious; 2018 Tachyum coverage (HPCwire, CB Insights) calls IPM Growth the VC arm of InfraPartners Management LLP, with Adrian Vyčítal joining Tachyum's board. Possible S2 (London HQ).
- `jpt-investment` (incorrect): Should be decided EXCLUDE (E3), not unverified. Public evidence is enough. In the fund's RÚZ 2025 statements (attachment 12109229, already cited), the EUR 6.75m of shares sit in note table 4 'Cenné papiere na obchodovanie' (trading securities), with realised gains/losses on shares, broker and exchange fees ('Burzové odplaty', 'Odplaty obchodníkom s cennými papiermi'), and USD/CAD positions. Long-term financial assets / participations are nil. This is a listed-securities portfolio of a single-shareholder vehicle (possible E6 too), not private-company investing. Not a wrongly excluded VC.
- `jsk-investments` (incorrect): Wrongly excluded. JSK runs a dedicated VC fund: JSK Investments Venture Capital Fund I, a ČNB-supervised SICAV sub-fund with its own site (jskinvestments.ventures) and its own team (Investment Director Petra Cihlářová, analyst) at Klimentská 46, Praha 1. It invests early stage to Series B in health and frontier tech, from EUR 300k initial tickets, with a EUR 20m target (EUR 10m internal) and 'capital managed independently' from the PE strategy. Portfolio: inTouch, Elin.ai, iSono Health, Vetstor (2025-12), Lightly, Andromeda Surgical (Series A, 2026), MintNeuro (2026-10-09). The S1 ground 'private investor with own capital' is factually wrong: the SICAV takes qualified-investor money (min EUR 125k; cc.cz 'Investujte jako Simona Kijonková'). The VC arm meets the vc definition and should be included, as CVC arms are (vc + flag). Counter-view: by target capital the PE fund (EUR 100m) dominates, which would give pe + S1. Even then, type private_investor is wrong. Fields: sector, stage and ticket are public on the VC fund site, but the record says not disclosed.
- `orbit-capital` (incorrect): Wrongly excluded under the written rules. Orbit is a Prague/Warsaw manager typed vc, with an equity portfolio (Booksy, Mews, Preply, Rohlik) that satisfies I2. E4 covers debt-ONLY lenders, and Orbit runs a growth-equity fund too. E7 needs no activity in 24 months, but Orbit closed Growth Debt II twice in the window (first close 2025-05-27, second close EUR 107m 2026-07-02); I3 counts fund closes. It is also deploying in Czechia: Sloneek round co-led with VFF (2026-06-16), IAG, and a debt tranche in Jutro Medical's Series A extension (Dec 2025). This is a policy-dependent call: if the pilot decides venture-debt-only activity is out of scope, it becomes correct. No new growth-equity deal since 2024-10-25 was found (the equity team page lists no deal staff). Capital: EUR 107m is an interim (second) close of the DEBT fund, paired with the EQUITY ticket; marked incorrect.
- `s15-19147830` (correct): E3 confirmed: en1re.cz offers real-estate-secured investments and development financing; no private-company equity found.
- `s15-21125929` (correct): E3 confirmed on mfinvestments.cz: actively managed value equity fund writing short puts; 2026-06-29 allocation 90% US / 10% Europe, 45% cash; started 2026-03-23; CZK 0.5m AUM (2026-09-24). No private-company investing.
- `wood-and-company` (correct): Exclusion holds, but E1 alone is incomplete. WOOD runs a 'Venture Investments' unit (wood.cz/sluzby/venture-investments: dozens of companies, tens of millions EUR; Pilulka, Snuggs, Rohlik, Fruitisimo, Eseye, LutherOne) and has held direct startup stakes. Its latest direct deals found are 2023 (Caplight: Aireen VC round Jun 2023, Snuggs Feb 2023, Window Holding buyout Aug 2023). Snuggs' Feb 2025 round names only TripleB. Venture activity now appears to be client products and fund-of-funds allocations (WOOD Venture One certificates, as reported). Better codes: E7 for the direct book + E5/E2, with no dated direct investment on/after 2024-10-25.

## 8. Published records and their proof of investing

| Investor | HQ | Sectors | Stages | Ticket | Capital | Latest dated activity (source) | Confidence |
|---|---|---|---|---|---|---|---|
| BUDETO (accelerator) | CZ | ai_data, software_saas | pre_seed, seed | not disclosed | not disclosed | 2026-05-01 — [investment: CircuitNinja (pre_seed)](https://www.budeto.xyz/llms.txt) | 1.000 |
| Credo Ventures | CZ | generalist | pre_seed, seed | USD 1m–5m (stated) | USD 88m latest_fund_size (stated) | 2026-06-02 — [investment: Picogrid](https://www.lupa.cz/aktuality/ceske-credo-ventures-investovalo-do-americkeho-startupu-ktery-vyviji-technologie-pro-pentagon/) | 1.000 |
| Czech Founders VC | CZ | software_saas, ai_data | pre_seed | EUR 50k–350k (stated) | EUR 10m latest_fund_size (stated) | 2026-06-09 — [investment: Merchantee (seed)](https://cc.cz/resi-jeden-z-nejvetsich-problemu-evropskych-e-shopu-kvituje-investor-cesi-ziskali-dalsi-desitky-milionu/) | 1.000 |
| DEPO Ventures | CZ | defence_dualuse, deeptech_hardware, fintech, industrial_manufacturing, energy_climate | pre_seed | EUR 250k–500k (stated) | not disclosed | 2026-08-26 — [fund commitment: DEPO Ventures One SCSp (NRI 'Fond Ukrajina' commitment)](https://www.businessinfo.cz/clanky/nri-dokoncila-vyber-venture-kapitaloveho-fondu-pro-program-fond-ukrajina/) | 1.000 |
| i&i Bio | CZ | biotech_life_sciences, healthtech | pre_seed, seed | EUR 150k–2m (stated) | EUR 53m interim_close (stated) | 2025-12-17 — [investment: T-CURX (series_a)](https://www.inibio.eu/news/t-curx-announces-%2420m-series-a-first-closing-led-by-biomedvc-to-fund-pipeline-of-clinical-stage-car-t-programs-and-advance-proprietary-non-viral-in-vivo-car-t-platform) | 0.850 |
| Inven Capital (corporate) | CZ | energy_climate | series_b, growth | EUR 2m–30m (stated) | EUR 500m aum (stated) | 2026-09-09 — [investment: Wint (series_d)](https://www.prnewswire.com/news-releases/wint-raises-36-million-in-series-d-funding-to-scale-ai-powered-water-intelligence-globally-302873443.html) | 1.000 |
| IP Lab Ventures | CZ | ai_data, deeptech_hardware, mobility_logistics, biotech_life_sciences, cybersecurity, industrial_manufacturing | pre_seed | EUR ?–1m (stated) | not disclosed | 2026-09-24 — [fund commitment: IP Lab Ventures Fund I](https://www.eif.org/press/all/first-czech-technology-transfer-fund-focused-on-ai-applications-to-invest-nearly-eur50-million-in-research-commercialisation) | 1.000 |
| J&T Ventures (corporate) | CZ | generalist | pre_seed, seed, series_a | EUR 300k–3m (stated) | EUR 120m aum (stated) | 2026-06-12 — [investment: Definic (formerly Nordics) (seed)](https://cc.cz/nakup-it-sluzeb-v-korporacich-je-casto-nefunkcni-hlasi-do-jejich-reseni-investuje-i-ceska-sporitelna/) | 1.000 |
| Jet Venture 1 | CZ | industrial_manufacturing, software_saas, ai_data | seed, series_a | EUR 1m–2m (stated) | EUR 30m interim_close (stated) | 2026-09-17 — [investment: AppNava](https://cc.cz/brnenska-startupova-ofenziva-miliardar-igor-fait-a-spol-investovali-behem-mesice-pres-150-milionu/) | 1.000 |
| JIC Ventures (public) | CZ | deeptech_hardware, software_saas | pre_seed, seed | EUR ?–1m (stated) | CZK 320m interim_close (stated) | 2026-05-19 — [investment: FaceUp (series_a)](https://www.jic.cz/en/about-us/pro-media/prvni-investice-noveho-fondu-jic-ventures-miri-do) | 1.000 |
| JSK Investments Venture Capital Fund I | CZ | healthtech, ai_data, deeptech_hardware, energy_climate | seed, series_a | EUR 300k–? (stated) | not disclosed | 2026-10-09 — [investment: MintNeuro](https://www.jskinvestments.cz/cs/media/jsk-investments-sicav-a-s-investuje-do-britskeho-vyvojare-cipu-pro-neurotechnologie-mint-neuro) | 1.000 |
| KAYA | CZ | generalist | pre_seed, seed, series_a | USD 1m–3m (stated) | USD 500m aum (stated) | 2026-10-06 — [investment: Sensible Biotechnologies (series_a)](https://cc.cz/velka-jizda-ze-slovenska-absolventi-oxfordu-chteji-zmenit-lecbu-rakoviny-od-investoru-ted-ziskali-miliardu/) | 1.000 |
| Lighthouse Ventures | CZ | software_saas, fintech, ai_data | pre_seed, seed | EUR 200k–1m (stated) | EUR 23m aum (stated) | 2026-06-09 — [investment: Merchantee (seed)](https://cc.cz/resi-jeden-z-nejvetsich-problemu-evropskych-e-shopu-kvituje-investor-cesi-ziskali-dalsi-desitky-milionu/) | 1.000 |
| Look AI Ventures | CZ | ai_data | pre_seed, seed | EUR 250k (stated) | not disclosed | 2026-09-22 — [investment: Embodied AI](https://lookai.vc/look-ai-ventures-backs-embodied-ai-robots-manufacturing/) | 1.000 |
| Moondust Ventures | CZ | healthtech, biotech_life_sciences | pre_seed, seed, series_a | not disclosed | not disclosed | 2026-06-18 — [investment: SOMAREALITY (series_a)](https://www.mdventures.cz/blog/somareality-raises-eu3m-to-redefine-cognitive-measurement-through-eye-tracking-technology) | 1.000 |
| N1 (formerly Nation 1) | CZ | ai_data, healthtech, deeptech_hardware | pre_seed, seed | USD 100k–1m (stated) | USD 60m aum (stated) | 2025-07-03 — [investment: Liki24 (series_a)](https://www.vestbee.com/insights/articles/liki24-secures-9) | 0.850 |
| Purple Ventures | CZ | healthtech, energy_climate, media_gaming, cybersecurity | pre_seed, seed | EUR 250k–400k (stated) | CZK 700m interim_close (stated) | 2026-09-07 — [investment: Rightcharge (follow_on)](https://www.soulmatesventures.com/rightcharge-follow-on-round/) | 1.000 |
| Reflex Capital | CZ | software_saas | seed, series_a | EUR 1m–2m (stated) | EUR 22m latest_fund_size (stated) | 2026-06-09 — [investment: Merchantee (seed)](https://cc.cz/resi-jeden-z-nejvetsich-problemu-evropskych-e-shopu-kvituje-investor-cesi-ziskali-dalsi-desitky-milionu/) | 1.000 |
| Rockaway Ventures | CZ | ecommerce_marketplaces, mobility_logistics, media_gaming, cybersecurity, defence_dualuse, energy_climate, proptech_construction | seed, series_a | not disclosed | EUR 55m latest_fund_size (stated) | 2026-02-24 — [investment: ValkaAI (pre_seed)](https://cc.cz/tvori-avatary-kteri-zvladnou-zive-komentovat-sportovni-zapasy-ted-ziskal-rekordni-investici/) | 1.000 |
| Seed Starter České spořitelny (corporate) | CZ | fintech | pre_seed, seed | EUR 200k–1m (stated) | CZK 200m balance_sheet (stated) | 2026-06-12 — [investment: Definic (formerly Nordics) (seed)](https://cc.cz/nakup-it-sluzeb-v-korporacich-je-casto-nefunkcni-hlasi-do-jejich-reseni-investuje-i-ceska-sporitelna/) | 1.000 |
| Soulmates Ventures | CZ | energy_climate, mobility_logistics, edtech, healthtech, agrifood, impact_social | pre_seed, seed, series_a | EUR ?–3m (stated) | EUR 62m aum (stated) | 2026-09-07 — [investment: Rightcharge (follow_on)](https://www.soulmatesventures.com/rightcharge-follow-on-round/) | 1.000 |
| Spinoffy | CZ | ai_data, cybersecurity, industrial_manufacturing, deeptech_hardware, energy_climate | pre_seed, seed | not disclosed | not disclosed | 2026-10-14 — [investment: DiagnostiQS](https://cc.cz/v-cesku-zakotvil-startup-s-top-mozky-ma-novou-investici-na-ktere-se-podili-i-petr-kellner-mladsi/) | 1.000 |
| Springtide Ventures (corporate) | CZ | software_saas, cybersecurity, ai_data | seed, series_a, series_b, growth | USD 1m–10m (stated) | not disclosed | 2025-01-07 — [investment: ThreatMark](https://cc.cz/chrani-desitky-milionu-bankovnich-uctu-ted-brnensky-threatmark-nabira-pres-pul-miliardy/) | 1.000 |
| StartupYard (accelerator) | CZ | ai_data, cybersecurity, deeptech_hardware | pre_seed, seed | EUR 45k–70k (stated) | not disclosed | 2025-02-14 — [investment: Ydoca (pre_seed)](https://cc.cz/live/petkrat-rychlejsi-vyberova-rizeni-do-cesko-slovenske-ai-platformy-ydoca-investovali-depo-ventures-a-startupyard/) | 1.000 |
| Tachles VC | CZ | cybersecurity, software_saas, ai_data | seed, series_a | not disclosed | CZK 500m interim_close (stated) | 2025-10-09 — [investment: Boost.space](https://cc.cz/cesi-delaji-poradek-v-datech-pro-firmy-ve-vice-nez-140-zemich-sveta-ted-zaujali-i-miliardare-igora-faita/) | 1.000 |
| Tensor Ventures | CZ | ai_data, deeptech_hardware, biotech_life_sciences, energy_climate | pre_seed, seed, series_a | EUR 250k–1m (self_reported) | EUR 20m interim_close (stated) | 2026-04-15 — [investment: Pointee (seed)](https://cc.cz/nasadit-ai-je-hracka-ale-uridit-ji-peklo-hlasi-cesky-startup-ktery-na-to-ziskal-desitky-milionu/) | 0.850 |
| Tilia Impact Ventures | CZ | impact_social, energy_climate, healthtech, edtech | pre_seed, seed | EUR 300k–1.2m (stated) | EUR 26m interim_close (stated) | 2026-05-19 — [investment: FaceUp (series_a)](https://cc.cz/byl-to-studentsky-projekt-ted-uz-ma-hodnotu-pres-pul-miliardy-nabidky-na-odkup-odmitame-hlasi-cesi/) | 1.000 |
| Y Soft Ventures (corporate) | CZ | deeptech_hardware, industrial_manufacturing, cybersecurity | pre_seed, seed | not disclosed | not disclosed | 2025-07-02 — [investment: RoboTwin (pre_seed)](https://eitjumpstarter.eu/robotwin-secures-1-million-eur/) | 1.000 |
| ZAKA VC | CZ | healthtech, biotech_life_sciences, industrial_manufacturing | pre_seed, seed | not disclosed | EUR 17m interim_close (stated) | 2025-12-09 — [investment: Vetstor (seed)](https://cc.cz/vedla-miliardovou-sit-zverimexu-po-rodicovske-hlida-zdravi-mazlicku-desitky-milionu-ted-ma-i-od-kijonkove/) | 1.000 |
| Seed Starter Slovenskej sporiteľne (corporate) | SK | generalist | pre_seed, seed | EUR 200k–1m (stated) | EUR 5m balance_sheet (stated) | 2026-04-09 — [investment: TrollWall AI](https://www.sih.sk/aktuality/ai-proti-nenavisti-na-internete-startup-trollwall-ai-ziskal-investiciu-vo-vyske-800-000-eur) | 1.000 |
| Slovak Investment Holding (public) | SK | ai_data, software_saas, fintech, deeptech_hardware | seed | EUR 280k–1.4m (derived) | EUR 15m balance_sheet (stated) | 2026-09-22 — [investment: VisionFlow](https://www.sih.sk/aktuality/sih-investuje-1-4-miliona-eur-do-visionflow-slovensky-startup-vyvija-softverovu-datovu-infrastrukturu-pre-umelu-inteligenciu) | 1.000 |
| Venture to Future Fund (public) | SK | generalist | seed, series_a, series_b | EUR 400k–7m (stated) | EUR 55.7m cumulative_fund_sizes (derived) | 2026-05-19 — [investment: FaceUp](https://forbes.cz/jic-ventures-investuje-do-faceup-cesky-startup-ziskal-pres-110-milionu-korun-na-globalni-expanzi/) | 1.000 |
| Zero One Hundred | SK | software_saas, ai_data, healthtech, proptech_construction | pre_seed, seed | not disclosed | EUR 23m latest_fund_size (stated) | 2026-02-05 — [investment: Readmio](https://vestbee.com/insights/articles/readmio-secures-1-m) | 1.000 |
