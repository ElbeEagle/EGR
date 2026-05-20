# Round 2 Integration Error Audit

Generated at: `2026-05-19T07:00:23+00:00`
Before: `outputs/evaluation/round2_eval_500/samples.jsonl`
After: `outputs/evaluation/round2_main_integration_500/samples.jsonl`

## Headline

- Final answer accuracy: 34/500 (6.8%) -> 47/500 (9.4%); delta +13 samples.
- Reasoning success: 319/500 (63.8%) -> 337/500 (67.4%); delta +18 samples.
- Wrong -> correct: 13; correct -> wrong: 0.
- Reasoning success -> reasoning failure: 0; reasoning failure -> success: 18.
- Model sequence changed for 10/500 samples; num_steps changed for 4 samples.

## Final-Correct Transition Matrix

| before | after | count |
| --- | --- | --- |
| wrong | wrong | 453 |
| correct | correct | 34 |
| wrong | correct | 13 |


## Reasoning-Success Transition Matrix

| before | after | count |
| --- | --- | --- |
| success | success | 319 |
| failure | failure | 163 |
| failure | success | 18 |


## Failure-Reason Transition Matrix

| before | after | count |
| --- | --- | --- |
| answer_mismatch | answer_mismatch | 283 |
| max_steps | max_steps | 133 |
| none | none | 34 |
| no_model | no_model | 30 |
| max_steps | none | 11 |
| no_model | answer_mismatch | 4 |
| max_steps | answer_mismatch | 3 |
| answer_mismatch | none | 2 |


## Query-Type Transition Matrix

| before | after | count |
| --- | --- | --- |
| Value | Value | 159 |
| Equation | Equation | 131 |
| Eccentricity | Eccentricity | 83 |
| Range | Range | 38 |
| Area | Area | 27 |
| Coordinate | Coordinate | 27 |
| Distance | Distance | 22 |
| Length | Length | 13 |


## Num-Steps Delta Distribution

| before | after | count |
| --- | --- | --- |
| delta | 0 | 496 |
| delta | 8 | 3 |
| delta | 15 | 1 |


## By Query Type

| query_type | n | before_success | after_success | success_delta | before_correct | after_correct | correct_delta | success_regressions | accuracy_gains | accuracy_regressions |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Value | 159 | 93 | 106 | 13 | 4 | 17 | 13 | 0 | 13 | 0 |
| Area | 27 | 10 | 11 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| Coordinate | 27 | 4 | 4 | 0 | 3 | 3 | 0 | 0 | 0 | 0 |
| Distance | 22 | 12 | 12 | 0 | 2 | 2 | 0 | 0 | 0 | 0 |
| Eccentricity | 83 | 71 | 71 | 0 | 7 | 7 | 0 | 0 | 0 | 0 |
| Equation | 131 | 103 | 107 | 4 | 11 | 11 | 0 | 0 | 0 | 0 |
| Length | 13 | 9 | 9 | 0 | 3 | 3 | 0 | 0 | 0 | 0 |
| Range | 38 | 17 | 17 | 0 | 4 | 4 | 0 | 0 | 0 | 0 |


## By Curve Type

| curve_type | n | before_success | after_success | success_delta | before_correct | after_correct | correct_delta | success_regressions | accuracy_gains | accuracy_regressions |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Parabola | 148 | 52 | 66 | 14 | 3 | 15 | 12 | 0 | 12 | 0 |
| Hyperbola | 177 | 135 | 139 | 4 | 14 | 14 | 0 | 0 | 0 | 0 |
| Circle | 11 | 9 | 9 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| Ellipse | 143 | 117 | 117 | 0 | 17 | 18 | 1 | 0 | 1 | 0 |
| Other | 21 | 6 | 6 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |


## Top Accuracy-Gain Samples

| sample_id | curve | query_type | before_failure | after_failure | before_steps | after_steps | expected | before_predicted | after_predicted | query |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2207 | Parabola | Value | answer_mismatch | none | 15 | 15 | 13 | Abs(LineSegmentOf(P,F)) | 13 | Abs(LineSegmentOf(P,F)) |
| 1788 | Ellipse | Value | answer_mismatch | none | 15 | 15 | 1 | k: Real | 1 | k |
| 7714 | Parabola | Value | max_steps | none | 15 | 15 | 8 | Abs(LineSegmentOf(A, B)) not found | 8 | Abs(LineSegmentOf(A, B)) |
| 7184 | Parabola | Value | max_steps | none | 15 | 15 | 6 | Min not found | 6 | Min(Abs(LineSegmentOf(P, A)) + Abs(LineSegmentOf(P, F))) |
| 6177 | Parabola | Value | max_steps | none | 15 | 15 | 6 | Abs(LineSegmentOf(P, F)) not found | 6 | Abs(LineSegmentOf(P, F)) |
| 5711 | Parabola | Value | max_steps | none | 15 | 15 | 7 | Min not found | 7 | Min(Abs(LineSegmentOf(P, A)) + Abs(LineSegmentOf(P, F))) |
| 3858 | Parabola | Value | max_steps | none | 15 | 15 | 6 | Min not found | 6 | Min(Abs(LineSegmentOf(P, A)) + Abs(LineSegmentOf(P, F))) |
| 3783 | Parabola | Value | max_steps | none | 15 | 15 | 4*sqrt(2) | Abs(LineSegmentOf(A, B)) not found | 4*sqrt(2) | Abs(LineSegmentOf(A, B)) |
| 2252 | Parabola | Value | max_steps | none | 15 | 15 | 2 | Slope not found | 2 | Slope(OverlappingLine(LineSegmentOf(A, B))) |
| 959 | Parabola | Value | max_steps | none | 15 | 15 | 9 | Min not found | 9 | Min(Abs(LineSegmentOf(P, A)) + Abs(LineSegmentOf(P, F))) |
| 852 | Parabola | Value | max_steps | none | 15 | 15 | p/y0 | Slope not found | p/y0 | Slope(LineOf(P, Q)) |
| 780 | Parabola | Value | max_steps | none | 15 | 15 | pm*1 | Slope not found | pm*1 | Slope(l) |
| 360 | Parabola | Value | max_steps | none | 15 | 15 | 2 | LineSegmentOf not found | 2 | LineSegmentOf(F, R) |


## Top Success-Regression Samples

_None._


## Correct-to-Wrong Samples

_None._


## Largest Model Usage Deltas

| model_id | before_usage | after_usage | delta |
| --- | --- | --- | --- |
| 1 | 344 | 392 | 48 |
| 65 | 277 | 262 | -15 |
| 42 | 79 | 88 | 9 |
| 29 | 989 | 981 | -8 |
| 63 | 195 | 188 | -7 |
| 43 | 130 | 136 | 6 |
| 56 | 222 | 228 | 6 |
| 54 | 53 | 55 | 2 |
| 14 | 2 | 1 | -1 |
| 62 | 1006 | 1005 | -1 |
| 0 | 296 | 296 | 0 |
| 2 | 74 | 74 | 0 |
| 9 | 15 | 15 | 0 |
| 13 | 394 | 394 | 0 |
| 19 | 2 | 2 | 0 |
| 21 | 98 | 98 | 0 |
| 24 | 79 | 79 | 0 |
| 47 | 15 | 15 | 0 |
| 53 | 51 | 51 | 0 |
| 75 | 45 | 45 | 0 |


## Solver-Hardening Priorities

| priority | area | evidence | suggested_next_step | sample_ids |
| --- | --- | --- | --- | --- |
| P1 | Preserve symbolic answer-extraction gains | 13 samples moved from wrong to correct; top query gains are {'Value': 13}. | Turn the top gain cases into regression tests before hardening adjacent solver paths. | ['360', '780', '852', '959', '1788', '2207', '2252', '3783', '3858', '5711'] |
| P2 | Stop repeated no-progress theorem loops | 158 failed after-run samples repeatedly apply one model; model 29 appears in 43. This is a solver-hardening target, not a new theorem-route delta. | Add or tune a no-progress guard after the answer-extraction regressions are covered. | ['5', '18', '78', '208', '262', '330', '380', '391', '421', '450'] |
| P2 | Reduce remaining successful-reasoning answer mismatches | 290 after-run samples still reason successfully but answer incorrectly; largest query bucket is Equation with 96. | After recovering success regressions, harden final answer extraction and comparison for the largest mismatch query buckets. | ['66', '380', '417', '465', '486', '551', '611', '657', '757', '832'] |

