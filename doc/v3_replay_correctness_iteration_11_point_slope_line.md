# V3 Replay Correctness Iteration 11: Point-Slope Line Closure

## Scope

This deliberately small iteration adds one deterministic geometry rule:

```text
PointOnCurve(P, l) + PointPositionOf(P) + SlopeOf(l)
-> LineNormalFormOf(l)
```

The generated line is `m*x - y + (y0-m*x0)=0`.  Closure runs only when the
line has exactly one currently known incident point; two-known-point lines
remain owned by the existing endpoint rule.  No inclination conversion,
asymptote branch choice, or answer-specific template is included.

## Fixed 500-row evaluation

The baseline is the first 500 rows from the i24 diagnostics.  The new run uses
the same rows and assisted observed sequence.

| Metric | Baseline | Point-slope closure | Delta |
| --- | ---: | ---: | ---: |
| Complete sequences | 102 (20.40%) | 104 (20.80%) | +2 |
| Correct answers | 21 (4.20%) | 21 (4.20%) | 0 |
| Selector usable | 20 (4.00%) | 20 (4.00%) | 0 |
| Evaluable accuracy | 21/21 (100%) | 21/21 (100%) | no regression |

Rows 126 and 487 newly replay completely.  Neither reaches a newly supported
final answer, so the next missing constraints lie downstream of model 78.

## Artifacts

- `src/theorems_v2/geometry_closure.py`
- `tests/test_theorems_v2_constructed_geometry_unittest.py`
- `outputs/theorems_v2/stage_line_point_slope_500_summary.json`
- `outputs/theorems_v2/stage_line_point_slope_500_diagnostics.jsonl`

