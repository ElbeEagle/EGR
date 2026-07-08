# V3 Replay Correctness Iteration 08: Auditable Macro Applicator

## Objective

Treat the stored theorem sequence as the abstract order of the natural-language
solution.  A selected theorem may transactionally apply redundant supporting
theorems before the requested theorem, while the externally visible sequence
and selector label remain unchanged.

## Semantics

`MacroApplicatorV2` first attempts the requested theorem directly.  On a
retryable failure it considers, in order:

1. declared theorem dependencies;
2. concrete producers of currently missing predicates;
3. other uniquely applicable concrete theorems.

Every helper chain is provisional.  It is committed only when the originally
requested theorem becomes `APPLIED` or `ALREADY_KNOWN`; otherwise the input
state and original failure are returned unchanged.  Successful helper actions
are exported as `support_applications` with binding, evidence, delta, and
provenance.

This keeps `models_v3_observed` aligned to the text while making omitted
low-level steps executable and auditable.

## Performance hardening

Global helper search initially reran the full geometry, quantity, coordinate,
and elimination closure for nearly every candidate.  The final implementation:

- enriches a trial state once per requested macro action;
- rejects helper candidates through their matcher before invoking applicator;
- retries the requested theorem only after its matcher becomes non-empty;
- exposes `apply_enriched()` so helper application does not repeat the same
  pre-application closure.

On the first 500 observed sequences, these changes preserve identical metrics
and reduce assisted benchmark time from about 104 seconds to 67.5 seconds.

## Full benchmark

Input: `data/train_with_models_v3_candidate.json`

Sequence field: `models_v3_observed`

| Metric | Direct apply | Macro apply | Delta |
| --- | ---: | ---: | ---: |
| Rows | 5,355 | 5,355 | 0 |
| Applied steps | 7,580 | 8,723 | +1,143 |
| Complete sequences | 597 | 845 | +248 |
| Complete sequence rate | 11.15% | 15.78% | +4.63 pp |
| Correct answers | 228 | 270 | +42 |
| Selector-usable trajectories | 204 | 241 | +37 |
| Incorrect answers | 1 | 2 | +1 known bad label |

The two incorrect rows are the previously confirmed dataset errors 887 and
1834.  Row 1834 becomes evaluable only after macro support model 12 unlocks its
stored model 28.  No new mathematical regression was found.

The macro run committed 1,137 support applications.  The dominant helpers are:

| Helper model | Count |
| ---: | ---: |
| 12 | 509 |
| 11 | 371 |
| 5 | 110 |
| 3 | 34 |
| 78 | 30 |
| 7 | 21 |
| 9 | 20 |

This distribution supports the hypothesis that natural-language solutions
frequently omit conic parameter relations and standard-form recognition while
still using their consequences.

## Current boundary

Macro application improves reachability more than numeric resolution.
`GOAL_NOT_REACHED` decreases from 2,405 to 1,885, while `VALUE_UNRESOLVED`
increases from 440 to 905.  The next bottleneck is therefore solving or
compiling the newly reached symbolic constraints, not adding still more global
helper actions.

The remaining first failures are led by models 2, 3, 5, 7, and 1.  Frequent
missing inputs include `ExpressionPolynomial`, `LineNormalFormOf`,
`PointPositionOf`, point-line distance requests, and intersection facts.  Such
facts generally require parser/compiler improvements or explicit macro
templates; unrelated theorem saturation cannot manufacture them safely.

## Artifacts

- `src/theorems_v2/macro_applicator.py`
- `src/theorems_v2/geometry_closure.py`
- `src/theorems_v2/schema.py`
- `src/theorems_v2/replay_benchmark.py`
- `scripts/theorems_v2/run_v3_replay_benchmark.py`
- `outputs/theorems_v2/v3_replay_observed_direct_i21_summary.json`
- `outputs/theorems_v2/v3_replay_observed_macro_i21_summary.json`
- `outputs/theorems_v2/v3_observed_macro_i21_selector_usable_trajectories.jsonl`

