# Round 2 Integration Error Audit

Generated at: `2026-05-19T07:00:23+00:00`
Before: `outputs/evaluation/main_integration_200/samples.jsonl`
After: `outputs/evaluation/round2_main_integration_200/samples.jsonl`

## Headline

- Final answer accuracy: 21/200 (10.5%) -> 33/200 (16.5%); delta +12 samples.
- Reasoning success: 130/200 (65.0%) -> 140/200 (70.0%); delta +10 samples.
- Wrong -> correct: 12; correct -> wrong: 0.
- Reasoning success -> reasoning failure: 0; reasoning failure -> success: 10.
- Model sequence changed for 1/200 samples; num_steps changed for 0 samples.

## Final-Correct Transition Matrix

| before | after | count |
| --- | --- | --- |
| wrong | wrong | 167 |
| correct | correct | 21 |
| wrong | correct | 12 |


## Reasoning-Success Transition Matrix

| before | after | count |
| --- | --- | --- |
| success | success | 130 |
| failure | failure | 60 |
| failure | success | 10 |


## Failure-Reason Transition Matrix

| before | after | count |
| --- | --- | --- |
| answer_mismatch | answer_mismatch | 107 |
| max_steps | max_steps | 49 |
| none | none | 21 |
| no_model | no_model | 11 |
| max_steps | none | 10 |
| answer_mismatch | none | 2 |


## Query-Type Transition Matrix

| before | after | count |
| --- | --- | --- |
| Value | Value | 71 |
| Equation | Equation | 43 |
| Eccentricity | Eccentricity | 40 |
| Range | Range | 16 |
| Coordinate | Coordinate | 11 |
| Distance | Distance | 7 |
| Area | Area | 6 |
| Length | Length | 6 |


## Num-Steps Delta Distribution

| before | after | count |
| --- | --- | --- |
| delta | 0 | 200 |


## By Query Type

| query_type | n | before_success | after_success | success_delta | before_correct | after_correct | correct_delta | success_regressions | accuracy_gains | accuracy_regressions |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Value | 71 | 40 | 50 | 10 | 3 | 15 | 12 | 0 | 12 | 0 |
| Area | 6 | 2 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| Coordinate | 11 | 2 | 2 | 0 | 2 | 2 | 0 | 0 | 0 | 0 |
| Distance | 7 | 3 | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| Eccentricity | 40 | 35 | 35 | 0 | 5 | 5 | 0 | 0 | 0 | 0 |
| Equation | 43 | 34 | 34 | 0 | 7 | 7 | 0 | 0 | 0 | 0 |
| Length | 6 | 4 | 4 | 0 | 2 | 2 | 0 | 0 | 0 | 0 |
| Range | 16 | 10 | 10 | 0 | 2 | 2 | 0 | 0 | 0 | 0 |


## By Curve Type

| curve_type | n | before_success | after_success | success_delta | before_correct | after_correct | correct_delta | success_regressions | accuracy_gains | accuracy_regressions |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Parabola | 56 | 19 | 29 | 10 | 1 | 12 | 11 | 0 | 11 | 0 |
| Circle | 5 | 4 | 4 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| Ellipse | 58 | 42 | 42 | 0 | 8 | 9 | 1 | 0 | 1 | 0 |
| Hyperbola | 72 | 62 | 62 | 0 | 12 | 12 | 0 | 0 | 0 | 0 |
| Other | 9 | 3 | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |


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
| 54 | 13 | 14 | 1 |
| 62 | 405 | 404 | -1 |
| 0 | 163 | 163 | 0 |
| 1 | 94 | 94 | 0 |
| 2 | 20 | 20 | 0 |
| 9 | 11 | 11 | 0 |
| 13 | 211 | 211 | 0 |
| 14 | 1 | 1 | 0 |
| 21 | 53 | 53 | 0 |
| 24 | 30 | 30 | 0 |
| 29 | 459 | 459 | 0 |
| 42 | 21 | 21 | 0 |
| 43 | 30 | 30 | 0 |
| 47 | 15 | 15 | 0 |
| 53 | 22 | 22 | 0 |
| 56 | 92 | 92 | 0 |
| 63 | 72 | 72 | 0 |
| 65 | 101 | 101 | 0 |
| 75 | 7 | 7 | 0 |
| 78 | 10 | 10 | 0 |


## Solver-Hardening Priorities

| priority | area | evidence | suggested_next_step | sample_ids |
| --- | --- | --- | --- | --- |
| P1 | Preserve symbolic answer-extraction gains | 12 samples moved from wrong to correct; top query gains are {'Value': 12}. | Turn the top gain cases into regression tests before hardening adjacent solver paths. | ['360', '780', '852', '1788', '2207', '2252', '3783', '3858', '5711', '6177'] |
| P2 | Stop repeated no-progress theorem loops | 68 failed after-run samples repeatedly apply one model; model 29 appears in 19. This is a solver-hardening target, not a new theorem-route delta. | Add or tune a no-progress guard after the answer-extraction regressions are covered. | ['208', '380', '391', '529', '551', '657', '725', '757', '805', '840'] |
| P2 | Reduce remaining successful-reasoning answer mismatches | 107 after-run samples still reason successfully but answer incorrectly; largest query bucket is Value with 35. | After recovering success regressions, harden final answer extraction and comparison for the largest mismatch query buckets. | ['96', '265', '391', '593', '665', '772', '1148', '1350', '1356', '1821'] |

