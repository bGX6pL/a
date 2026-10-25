# Review protocol (M1 / M2)

Purpose: measure how accurate the pipeline's records are. The reviewer did not build the records and
is expected to look for errors; finding them is the point of the exercise.

Samples are drawn reproducibly by `uv run python -m investordb.review sample` into
`data/curated/reviews/<sample>/_sample.json`:

- **M1** — published records: does each record hold up?
- **M2** — excluded / unverified candidates: was an active VC wrongly left out?

## Per record

1. Read the dossier `data/curated/dossiers/<pilot>/<investor_key>.json` (rules: [task-a-plan.md](task-a-plan.md)).
2. Open the cited evidence URLs **and** the investor's own website (portfolio / news / about). Where
   possible look for one newer or contradicting public source (news about the fund, deals after the
   cited one, a change of strategy).
3. Answer the checks below, then the verdict. Write short notes for every `false` / `incorrect`.

| Check | Values | Meaning |
|---|---|---|
| `real_entity` | true / false / null | A real, identifiable organisation (or person in a professional capacity) |
| `invests_in_companies` | true / false / null | Puts equity/quasi-equity into private companies |
| `active_24m` | true / false / null | At least one investment or fund event by this investor dated on/after 2024-10-25 (check the event date, not just the article date) |
| `type_correct` | true / false / null | Primary type (vc, pe, ...) and flags (corporate, public, accelerator) are right; in the pilot country |
| `decision_correct` | true / false / null | Include / exclude / unverified is right under the rules (M2: false = an active in-scope VC was wrongly left out) |
| `sector_focus`, `stage_focus`, `ticket_size`, `capital` | correct / incorrect / unverifiable / not_applicable | `correct`: supported by the cited source and not contradicted by a newer one. `incorrect`: wrong, unsupported by its quote, misattributed (e.g. a round size presented as the investor's ticket, a fund target presented as fund size, a manager-group AUM presented as the fund), outdated where a newer figure is public, or a value is public but the record says not disclosed. `unverifiable`: the sources cannot be opened. `not_applicable`: marked not disclosed and you also found nothing public, or the field is not filled for an exclusion |
| `activity_evidence` | same values | The cited activity evidence really shows this investor's investment / fund event on the stated date |

**Verdict** (record level): `correct` when real_entity, invests_in_companies, active_24m, type_correct
and decision_correct all hold (M2: when the exclusion is right); `incorrect` when any of them fails;
`unsure` when you cannot decide. Field-level errors do not flip the verdict; they are counted separately.

## Output

One file per record: `data/curated/reviews/<sample>/<investor_key>.json`

```json
{
  "investor_key": "credo-ventures",
  "sample": "review-2026-10",
  "reviewer": "independent-reviewer-A",
  "reviewed_on": "2026-10-25",
  "verdict": "correct",
  "checks": {
    "real_entity": true, "invests_in_companies": true, "active_24m": true, "type_correct": true,
    "decision_correct": true, "sector_focus": "correct", "stage_focus": "correct",
    "ticket_size": "correct", "capital": "incorrect", "activity_evidence": "correct"
  },
  "notes": "capital: USD 88m is the Fund V first close; final close not confirmed."
}
```

Validate with `uv run python -m investordb.review check <files>`; load all with
`uv run python -m investordb.review load`. A human reviewer can edit any file (set `reviewer` to their
name) and re-run `review load` and `metrics`.
