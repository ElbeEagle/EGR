# Round 2 Integration Error Audit

Generated at: `2026-05-19T06:34:24+00:00`
Before: `outputs/evaluation/protocol_200_smoke/samples.jsonl`
After: `outputs/evaluation/main_integration_200/samples.jsonl`

## Headline

- Final answer accuracy: 5/200 (2.5%) -> 21/200 (10.5%); delta +16 samples.
- Reasoning success: 147/200 (73.5%) -> 130/200 (65.0%); delta -17 samples.
- Wrong -> correct: 18; correct -> wrong: 2.
- Reasoning success -> reasoning failure: 35; reasoning failure -> success: 18.
- Model sequence changed for 0/200 samples; num_steps changed for 0 samples.
- Diagnostic: all theorem traces and step counts are identical, so the reasoning-success delta comes from post-trace answer extraction / result.success behavior, not changed model selection.

## Final-Correct Transition Matrix

| before | after | count |
| --- | --- | --- |
| wrong | wrong | 177 |
| wrong | correct | 18 |
| correct | correct | 3 |
| correct | wrong | 2 |


## Reasoning-Success Transition Matrix

| before | after | count |
| --- | --- | --- |
| success | success | 112 |
| failure | failure | 35 |
| success | failure | 35 |
| failure | success | 18 |


## Failure-Reason Transition Matrix

| before | after | count |
| --- | --- | --- |
| answer_mismatch | answer_mismatch | 96 |
| answer_mismatch | max_steps | 33 |
| max_steps | max_steps | 24 |
| answer_mismatch | none | 13 |
| max_steps | answer_mismatch | 13 |
| no_model | no_model | 11 |
| max_steps | none | 5 |
| none | none | 3 |
| none | max_steps | 2 |


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
| Equation | 43 | 24 | 34 | 10 | 0 | 7 | 7 | 2 | 7 | 0 |
| Eccentricity | 40 | 31 | 35 | 4 | 1 | 5 | 4 | 0 | 4 | 0 |
| Coordinate | 11 | 1 | 2 | 1 | 0 | 2 | 2 | 1 | 2 | 0 |
| Range | 16 | 14 | 10 | -4 | 0 | 2 | 2 | 4 | 2 | 0 |
| Value | 71 | 64 | 40 | -24 | 2 | 3 | 1 | 24 | 3 | 2 |
| Area | 6 | 3 | 2 | -1 | 0 | 0 | 0 | 1 | 0 | 0 |
| Distance | 7 | 6 | 3 | -3 | 0 | 0 | 0 | 3 | 0 | 0 |
| Length | 6 | 4 | 4 | 0 | 2 | 2 | 0 | 0 | 0 | 0 |


## By Curve Type

| curve_type | n | before_success | after_success | success_delta | before_correct | after_correct | correct_delta | success_regressions | accuracy_gains | accuracy_regressions |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Parabola | 56 | 46 | 19 | -27 | 2 | 1 | -1 | 29 | 1 | 2 |
| Hyperbola | 72 | 57 | 62 | 5 | 2 | 12 | 10 | 1 | 10 | 0 |
| Circle | 5 | 1 | 4 | 3 | 0 | 0 | 0 | 0 | 0 | 0 |
| Ellipse | 58 | 40 | 42 | 2 | 1 | 8 | 7 | 3 | 7 | 0 |
| Other | 9 | 3 | 3 | 0 | 0 | 0 | 0 | 2 | 0 | 0 |


## Top Accuracy-Gain Samples

| sample_id | curve | query_type | before_failure | after_failure | before_steps | after_steps | expected | before_predicted | after_predicted | query |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 5645 | Hyperbola | Value | answer_mismatch | none | 1 | 1 | pm*2 | sqrt(2) | pm*2 | a |
| 2811 | Hyperbola | Value | answer_mismatch | none | 15 | 15 | -9 | m: Number | -9 | m |
| 221 | Hyperbola | Value | answer_mismatch | none | 15 | 15 | -8 | m: Number | -8 | m |
| 2841 | Hyperbola | Range | answer_mismatch | none | 15 | 15 | (-oo, -4)+(1, +oo) | b^2 - 4*a*c | (-oo, -4)+(1, +oo) | Range(k) |
| 926 | Ellipse | Range | answer_mismatch | none | 15 | 15 | (1, 3/2)+(3/2, 2) | sqrt(sqrt(2-a)^2 - sqrt(a-1)^2)/sqrt(2-a) | (1, 3/2)+(3/2, 2) | Range(a) |
| 6851 | Ellipse | Equation | answer_mismatch | none | 1 | 1 | x^2/16+y^2/7=1 | 4 | x^2/16+y^2/7=1 | Expression(C) |
| 6365 | Ellipse | Equation | answer_mismatch | none | 1 | 1 | y^2/4+x^2=1 | a | x^2+y^2/4=1 | Expression(G) |
| 5332 | Hyperbola | Equation | answer_mismatch | none | 1 | 1 | y^2=-36*(x-4) | 3 | y^2=-36*(x-4) | Expression(H) |
| 3501 | Ellipse | Equation | answer_mismatch | none | 1 | 1 | x^2/15+y^2/10=1 | 2 | x^2/15+y^2/10=1 | Expression(G1) |
| 1651 | Hyperbola | Equation | answer_mismatch | none | 1 | 1 | x^2/4-y^2=1 | b | x^2/4-y^2=1 | Expression(G) |
| 1324 | Ellipse | Equation | answer_mismatch | none | 1 | 1 | x^2/9+y^2/7=1 | b | x^2/9+y^2/7=1 | Expression(C) |
| 6302 | Hyperbola | Eccentricity | answer_mismatch | none | 1 | 1 | 2 | Eccentricity not found | 2 | Eccentricity(G) |
| 2710 | Hyperbola | Eccentricity | answer_mismatch | none | 1 | 1 | sqrt(10) | Eccentricity not found | sqrt(10) | Eccentricity(G) |
| 1830 | Hyperbola | Equation | max_steps | none | 15 | 15 | x^2/6-y^2/6=1 |  | x^2/6-y^2/6=1 | Expression(G) |
| 7246 | Ellipse | Eccentricity | max_steps | none | 15 | 15 | sqrt(3)/2 x^2/9-y^2/3=1 |  | sqrt(3)/2 x^2/9-y^2/3=1 | Eccentricity(H);Expression(G) |
| 1269 | Ellipse | Eccentricity | max_steps | none | 15 | 15 | sqrt(2)/2 | Eccentricity not found | sqrt(2)/2 | Eccentricity(G) |
| 4551 | Parabola | Coordinate | max_steps | none | 15 | 15 | (7/4, pm*sqrt(7)/2) | Coordinate(P) not found | (7/4, pm*sqrt(7)/2) | Coordinate(P) |
| 2840 | Hyperbola | Coordinate | max_steps | none | 15 | 15 | (pm*5,0) | Coordinate(G) not found | (pm*5, 0) | Coordinate(Focus(G)) |


## Top Success-Regression Samples

| sample_id | curve | query_type | before_failure | after_failure | before_steps | after_steps | expected | before_predicted | after_predicted | query |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2252 | Parabola | Value | none | max_steps | 15 | 15 | 2 | 2 | Slope not found | Slope(OverlappingLine(LineSegmentOf(A, B))) |
| 360 | Parabola | Value | none | max_steps | 15 | 15 | 2 | 2 | LineSegmentOf not found | LineSegmentOf(F, R) |
| 7714 | Parabola | Value | answer_mismatch | max_steps | 15 | 15 | 8 | 2 | Abs(LineSegmentOf(A, B)) not found | Abs(LineSegmentOf(A, B)) |
| 7184 | Parabola | Value | answer_mismatch | max_steps | 15 | 15 | 6 | 4 | Min not found | Min(Abs(LineSegmentOf(P, A)) + Abs(LineSegmentOf(P, F))) |
| 6407 | Parabola | Value | answer_mismatch | max_steps | 15 | 15 | 8 | 2 | Abs(LineSegmentOf(A, B)) not found | Abs(LineSegmentOf(A, B)) |
| 6177 | Parabola | Value | answer_mismatch | max_steps | 15 | 15 | 6 | 4 | Abs(LineSegmentOf(P, F)) not found | Abs(LineSegmentOf(P, F)) |
| 5824 | Parabola | Value | answer_mismatch | max_steps | 15 | 15 | 8 | 2 | Abs(LineSegmentOf(A, B)) not found | Abs(LineSegmentOf(A, B)) |
| 5711 | Parabola | Value | answer_mismatch | max_steps | 15 | 15 | 7 | 2 | Min not found | Min(Abs(LineSegmentOf(P, A)) + Abs(LineSegmentOf(P, F))) |
| 5515 | Parabola | Value | answer_mismatch | max_steps | 15 | 15 | 8/3 | 4 | Abs(LineSegmentOf(Q, F)) not found | Abs(LineSegmentOf(Q, F)) |
| 5080 | Ellipse | Value | answer_mismatch | max_steps | 15 | 15 | 16 | sqrt(4^2 - sqrt(7)^2)/4 | Perimeter not found | Perimeter(TriangleOf(A, B, F2)) |
| 4868 | Parabola | Value | answer_mismatch | max_steps | 15 | 15 | 2*sqrt(5)-1 | 2*(p/2 | Min not found | Min(Abs(LineSegmentOf(P, Q))) |
| 4606 | Parabola | Value | answer_mismatch | max_steps | 15 | 15 | 16/5 | 4 | Min not found | Min(d1 + d2) |
| 4119 | Parabola | Value | answer_mismatch | max_steps | 15 | 15 | 1/3 | 2*p/2 | Expression 'Abs(LineSegmentOf(A, F))/Abs(LineSegmentOf(B, F))' not found | Abs(LineSegmentOf(A, F))/Abs(LineSegmentOf(B, F)) |
| 3858 | Parabola | Value | answer_mismatch | max_steps | 15 | 15 | 6 | 2 | Min not found | Min(Abs(LineSegmentOf(P, A)) + Abs(LineSegmentOf(P, F))) |
| 3783 | Parabola | Value | answer_mismatch | max_steps | 15 | 15 | 4*sqrt(2) | 2 | Abs(LineSegmentOf(A, B)) not found | Abs(LineSegmentOf(A, B)) |
| 3576 | Parabola | Value | answer_mismatch | max_steps | 15 | 15 | pi/2 | 2*p/2 | AngleOf not found | AngleOf(M, O, N) |
| 3185 | Parabola | Value | answer_mismatch | max_steps | 15 | 15 | 3 | 4 | Abs(LineSegmentOf(Q, F)) not found | Abs(LineSegmentOf(Q, F)) |
| 2190 | Parabola | Value | answer_mismatch | max_steps | 15 | 15 | 1/2 | -1 | Expression '(Abs(LineSegmentOf(A, F))*Abs(LineSegmentOf(B, F)))/Abs(LineSegmentOf(A, B))' not found | (Abs(LineSegmentOf(A, F))*Abs(LineSegmentOf(B, F)))/Abs(LineSegmentOf(A, B)) |
| 2090 | Parabola | Value | answer_mismatch | max_steps | 15 | 15 | sqrt(3) | 2 | Slope not found | Slope(l) |
| 1933 | Parabola | Value | answer_mismatch | max_steps | 15 | 15 | 3/2 | 2 | Abs(LineSegmentOf(B, F)) not found | Abs(LineSegmentOf(B, F)) |


## Correct-to-Wrong Samples

| sample_id | curve | query_type | before_failure | after_failure | before_steps | after_steps | expected | before_predicted | after_predicted | query |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 360 | Parabola | Value | none | max_steps | 15 | 15 | 2 | 2 | LineSegmentOf not found | LineSegmentOf(F, R) |
| 2252 | Parabola | Value | none | max_steps | 15 | 15 | 2 | 2 | Slope not found | Slope(OverlappingLine(LineSegmentOf(A, B))) |


## Largest Model Usage Deltas

| model_id | before_usage | after_usage | delta |
| --- | --- | --- | --- |
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
| 54 | 13 | 13 | 0 |
| 56 | 92 | 92 | 0 |
| 62 | 405 | 405 | 0 |
| 63 | 72 | 72 | 0 |
| 65 | 101 | 101 | 0 |
| 75 | 7 | 7 | 0 |
| 78 | 10 | 10 | 0 |


## Solver-Hardening Priorities

| priority | area | evidence | suggested_next_step | sample_ids |
| --- | --- | --- | --- | --- |
| P0 | Protect previously correct samples | 2 samples changed from correct to wrong; these are direct regressions on the primary metric. | Start solver-hardening with these exact cases and add regression tests before broader extractor changes. | ['360', '2252'] |
| P0 | Recover reasoning-success regressions | 35 samples changed from reasoning success to reasoning failure; top bucket max_steps/Value/Parabola=23. model_sequence_changed=0/35, so this is post-trace extraction/result.success drift. | Replay this bucket through AnswerExtractor and restore coverage for high-frequency Parabola/Value forms without weakening final-answer checks. | ['360', '529', '780', '852', '1290', '1933', '2090', '2190', '2252', '3185'] |
| P1 | Preserve symbolic answer-extraction gains | 18 samples moved from wrong to correct; top query gains are {'Equation': 7, 'Eccentricity': 4, 'Value': 3, 'Range': 2}. | Turn the top gain cases into regression tests before hardening adjacent solver paths. | ['221', '926', '1269', '1324', '1651', '1830', '2710', '2811', '2840', '2841'] |
| P2 | Stop repeated no-progress theorem loops | 77 failed after-run samples repeatedly apply one model; model 29 appears in 25. This is a solver-hardening target, not a new theorem-route delta. | Add or tune a no-progress guard after the answer-extraction regressions are covered. | ['208', '360', '380', '391', '529', '551', '657', '725', '757', '780'] |
| P2 | Reduce remaining successful-reasoning answer mismatches | 109 after-run samples still reason successfully but answer incorrectly; largest query bucket is Value with 37. | After recovering success regressions, harden final answer extraction and comparison for the largest mismatch query buckets. | ['96', '265', '391', '593', '665', '772', '1148', '1350', '1356', '1788'] |

