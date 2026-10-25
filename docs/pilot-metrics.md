# Pilot metrics

Generated 2026-10-25 16:08 UTC by `uv run python -m investordb.metrics` from the Postgres database. Snapshot date 2026-10-25, activity window from 2024-10-25.

## 1. Screening outcome

| Pilot | Candidates | Included | Published | Excluded | Unverified |
|---|---|---|---|---|---|
| cz-vc | 62 | 31 | 31 | 31 | 0 |
| sk-reference | 52 | 5 | 5 | 33 | 14 |
| cz-s15-sample | 40 | 2 | 0 | 17 | 21 |

Exclusion reasons (a record can carry several):

| Pilot | Code | Records |
|---|---|---|
| cz-s15-sample | E3 | 15 |
| cz-s15-sample | E5 | 1 |
| cz-s15-sample | E7 | 1 |
| cz-s15-sample | E8 | 21 |
| cz-vc | E1 | 4 |
| cz-vc | E3 | 1 |
| cz-vc | E4 | 2 |
| cz-vc | E7 | 3 |
| cz-vc | S1 | 24 |
| sk-reference | E10 | 2 |
| sk-reference | E2 | 1 |
| sk-reference | E3 | 16 |
| sk-reference | E4 | 1 |
| sk-reference | E6 | 1 |
| sk-reference | E7 | 18 |
| sk-reference | E8 | 14 |
| sk-reference | S1 | 3 |
| sk-reference | S2 | 1 |

## 2. Field completeness of published records

Published records: **36** (CZ 31, SK 5); flags: corporate 6, public 3, accelerator 1.

| Field | Filled | By method | Not disclosed |
|---|---|---|---|
| Sector focus | 100% |  |  |
| Stage focus | 100% |  |  |
| Geography focus | 100% |  |  |
| Ticket size | 78% | stated 26, self_reported 1, derived 1 | 8 |
| Capital / AUM | 69% | stated 24, derived 1 | 11 |

Capital basis: latest_fund_size 20, aum 5.

## 3. Evidence and automated verification

| Measure | Value |
|---|---|
| Evidence items (all pilots) | 791 |
| Source class mix (CZ+SK pilots) | A 14%, B 48%, C 30%, D 8% |
| Pages retrieved by script | 100% |
| Quotes found verbatim/fuzzy on retrieved pages (V3) | 100% (790/791; 95% CI 99–100%) |
| Quotes on pages a script cannot retrieve (JS, paywall, bot block) | 0 |

Automated checks on included records (passed / failed / not applicable):

| Check | Passed | Failed | n/a |
|---|---|---|---|
| V1 | 35 | 0 | 3 |
| V3 | 37 | 1 | 0 |
| V4 | 38 | 0 | 0 |
| V5 | 18 | 1 | 19 |
| V6 | 35 | 0 | 3 |
| V7 | 36 | 0 | 2 |

## 4. Discovery sources: how many candidates each produced and how many survived

Candidates = screened records that name the source in `discovered_via`.

| Pilot | Source | Candidates | Published | Precision as a VC filter |
|---|---|---|---|---|
| cz-vc | cvca | 34 | 8 | 24% |
| cz-vc | news | 19 | 16 | 84% |
| cz-vc | research-seed | 16 | 13 | 81% |
| cz-vc | co-investor snowball | 1 | 0 | 0% |
| cz-vc | eif-portfolio | 1 | 0 | 0% |
| sk-reference | nbs-register | 41 | 2 | 5% |
| sk-reference | research-seed | 19 | 4 | 21% |
| sk-reference | news | 14 | 5 | 36% |
| sk-reference | slovca | 10 | 3 | 30% |
| sk-reference | sih-programmes | 9 | 4 | 44% |
| sk-reference | co-investor snowball | 6 | 4 | 67% |
| sk-reference | startup-report-slovensko | 3 | 2 | 67% |
| sk-reference | eif-portfolio | 2 | 1 | 50% |

Against the full CVCA roster (84 members, 57 of them associates — mostly law firms, auditors, banks and advisers screened out by their CVCA category without a dossier), CVCA membership is a VC filter with **10%** precision (8/84).

## 5. Registry labels as filters

| Register | Screened | Active startup VC | Any company investor (incl. inactive, PE, FO) | Unverifiable |
|---|---|---|---|---|
| ČNB §15 list ('osoba rizikového kapitálu'), random sample of 406 | 40 | 5% (2/40; 95% CI 1–17%) | 10% | 52% |
| NBS registered AIF managers / self-managed AIFs (SK, all) | 41 | 5% (2/41; 95% CI 1–16%) | 29% | 29% |

Extrapolated to the full §15 list of 406: about **20** active startup VC managers (95% CI 6–67).

## 6. Recall of discovery sources against the Slovak reference set

Reference set: 5 published (active) Slovak VC investors, and 16 real Slovak VC investors when inactive ones (E7) are counted too.

| Source | Finds (active) | Recall (active) | Finds (all real VCs) | Recall (all real VCs) |
|---|---|---|---|---|
| research-seed | 4 | 80% | 13 | 81% |
| news | 5 | 100% | 10 | 62% |
| nbs-register | 2 | 40% | 10 | 62% |
| sih-programmes | 4 | 80% | 9 | 56% |
| slovca | 3 | 60% | 6 | 38% |
| co-investor snowball | 4 | 80% | 5 | 31% |
| startup-report-slovensko | 2 | 40% | 3 | 19% |
| eif-portfolio | 1 | 20% | 1 | 6% |

## 7. Independent review

| Measure | Value |
|---|---|
| M1 record precision (published records judged correct) | – |
| M1 unsure | 0 |
| M2 wrongly excluded (excluded/unverified judged to be an active VC) | – |

M1 accuracy by check:

| Check | Accuracy | Unverifiable / null | n/a |
|---|---|---|---|
| sector_focus | – | 0 | 0 |
| stage_focus | – | 0 | 0 |
| ticket_size | – | 0 | 0 |
| capital | – | 0 | 0 |
| activity_evidence | – | 0 | 0 |
| real_entity | – | 0 |  |
| invests_in_companies | – | 0 |  |
| active_24m | – | 0 |  |
| type_correct | – | 0 |  |
| decision_correct | – | 0 |  |
