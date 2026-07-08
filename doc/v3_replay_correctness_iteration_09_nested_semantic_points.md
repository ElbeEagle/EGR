# V3 Replay Correctness Iteration 09: Nested Semantic Points and Directrix Macros

## Objective

Improve abstract natural-language sequence replay without adding answer-specific
rules.  This iteration targets two repeated representation gaps:

- facts refer to semantic points such as `Center(H)`, `Focus(G)`, and
  `RightFocus(G)` instead of declared point symbols;
- model 29 derives a directrix expression, but model 2 still cannot bind a
  directrix when the problem did not assign that line a name.

## Implementation

The geometry adapter now materializes nested semantic point references used in
point-on-curve and distance facts.  The virtual point is linked to its owning
curve through `CenterPointOf`, `FocusOf`, and, when explicit, `FocusSideOf`.
Existing geometry closure then supplies coordinates; coordinate compilation and
exact polynomial elimination remain responsible for solving values.

The quantity closure now materializes `Directrix(G)` as a typed line and adds a
`DirectrixOf` relation only when no named directrix already exists.  This avoids
ambiguous duplicate bindings.

Macro helper search adds the auditable priority hint `model 2 -> model 29`.
The hint changes search order only.  Model 29 is still applied provisionally,
and its state is committed only if model 2 subsequently succeeds.

## Full benchmark

Input: `data/train_with_models_v3_candidate.json`

Sequence field: `models_v3_observed`

| Metric | i21 macro | i22 macro | Delta |
| --- | ---: | ---: | ---: |
| Rows | 5,355 | 5,355 | 0 |
| Applied steps | 8,723 | 9,021 | +298 |
| Complete sequences | 845 | 956 | +111 |
| Complete sequence rate | 15.78% | 17.85% | +2.07 pp |
| Correct answers | 270 | 297 | +27 |
| Selector-usable trajectories | 241 | 277 | +36 |
| Unparsed fact atoms | 3,531 | 3,222 | -309 |

Model 2 first failures decrease from 610 to 359.  The run commits 265 model-29
support applications.  The post-benchmark fallback cleanup removes eight
duplicate adapter-error reports without changing parsed state or answer metrics.

## Incorrect-answer audit

Rows 887 and 1834 are the previously confirmed bad labels.

Row 3743 is newly evaluable.  It gives `y^2 = 2*p*x`, point `(2,-3)`, point-to-
focus distance 5, and `p > 0`.  Under the repository and Conic10K convention,
the focus is `(p/2,0)`, so

```text
(2 - p/2)^2 + 9 = 25
```

has the unique positive solution `p=12`.  The stored answer is 6, which uses a
different `y^2=4px` parameter convention.  The implementation deliberately
keeps the project-wide convention and records this row for data audit.

## Representative new solutions

- A circle center constrained to lie on a parabola now obtains the circle
  center coordinate, compiles point-on-conic membership, solves `p`, and
  verifies the directrix.
- A point with known distance to `Focus(G)` on a parabola now materializes the
  unique focus, compiles distance and conic equations, and uses quadrant facts
  to select the coordinate branch.
- An observed `[7, 2, 29]` chain can execute without a named directrix: model 29
  is a support action for model 2, and the later observed model 29 is idempotent.

## Remaining boundary

The largest unresolved group remains eccentricity.  These rows commonly need
constraints from `OneOf(Focus/Asymptote)`, vector relations, length ratios,
circle tangency, or geometric extrema.  Those forms require explicit branch and
quantity semantics and should not be handled by guessing a semantic point.

## Artifacts

- `src/theorems_v2/geometry_raw_adapter.py`
- `src/theorems_v2/quantity_closure.py`
- `src/theorems_v2/macro_applicator.py`
- `tests/test_theorems_v2_coordinate_compiler_unittest.py`
- `tests/test_theorems_v2_replay_benchmark_unittest.py`
- `outputs/theorems_v2/v3_replay_observed_macro_i22_summary.json`
- `outputs/theorems_v2/v3_replay_observed_macro_i22_diagnostics.jsonl`
- `outputs/theorems_v2/v3_observed_macro_i22_selector_usable_trajectories.jsonl`

