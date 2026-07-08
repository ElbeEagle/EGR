# V3 Replay Correctness Iteration 07: Polynomial Elimination

## Objective

Extend exact elimination from linear systems and single-variable quadratics to conservative small multivariate quadratic systems.

The implementation does not use floating-point approximation and does not choose a branch without explicit sign evidence.

## Method

The polynomial eliminator normalizes supported EquationConstraint expressions into exact degree-two polynomials over Fraction coefficients.

For each target variable it:

1. treats linear, square, and bilinear monomials as elimination columns;
2. eliminates all monomials not involving the target through exact row operations;
3. obtains target-only linear or quadratic equations;
4. intersects root sets from all target-only constraints;
5. applies Positive, Negative, NonNegative, and NonPositive facts;
6. writes a value only when one admissible exact root remains.

Unsupported degree, irrational coefficients outside exact simplification, or multiple admissible roots remain unresolved.

## Information-Space Additions

- PointOnCurve(point, conic) now compiles to a numeric conic-membership equation when the standard form is available.
- Quadrant(point) is parsed into x/y coordinate sign facts.
- Right/left/up/down parabola orientation contributes a nonnegative or nonpositive axial-coordinate constraint.
- Polynomial elimination runs only when coordinate equations or direct symbol constraints are present.

## Representative Chain

For ID 7104:

- parabola membership: y2 = 8x;
- focus distance: (x - 2)2 + y2 = 9;
- eliminate y2: x2 + 4x - 5 = 0;
- right-opening parabola requires x >= 0;
- roots are 1 and -5, so x = 1 is uniquely admissible.

For ID 7571 the same process gives x = 4 and y2 = 48. Quadrant 4 selects y = -4sqrt(3).

## Benchmark

Input: data/train_with_models_v3_candidate.json

Sequence field: models_v3_executable

| Metric | i18 | i20 | Delta |
| --- | ---: | ---: | ---: |
| Rows | 5355 | 5355 | 0 |
| Applied steps | 8093 | 8094 | +1 |
| Sequence success | 670 | 670 | 0 |
| Answer correct | 245 | 263 | +18 |
| Selector usable | 233 | 238 | +5 |
| Answer incorrect | 2 | 2 | 0 |
| Unparsed fact atoms | 3648 | 3531 | -117 |
| Conflict steps | 0 | 0 | 0 |

Answer accuracy among evaluable rows is 99.25%.

No previously correct answer regressed, no successful sequence was lost, and no new incorrect answer was introduced.

The first unrestricted i19 run took about 75 seconds. Entry-point gating reduced i20 to about 57 seconds with identical correctness metrics.

## Newly Solved Pattern

All 18 newly correct rows are parabola point-condition problems. They cover:

- recovering p or the complete standard equation from a point;
- recovering x or y from point-on-parabola plus focus distance;
- recovering a full coordinate with quadrant-based branch selection.

Only 5 of the 18 become selector-usable trajectories. Most remaining rows contain a model 2 NO_MATCH in the stored sequence even though closure reaches the correct answer. This is now primarily a sequence-label repair issue.

## Current Boundary

The eliminator supports total polynomial degree at most two with rational coefficients after exact simplification.

It does not yet support:

- cubic or higher-degree systems;
- general algebraic-number coefficient fields;
- inequality propagation beyond direct sign facts;
- symbolic resultants for systems whose elimination raises degree;
- enumerating multiple geometric branches as explicit alternative states.

The next highest-leverage action is to repair theorem sequences for the newly solved closure cases, especially repeated [7, 2, 29] and [7, 2, 17] patterns.

## Artifacts

- src/theorems_v2/polynomial_elimination.py
- outputs/theorems_v2/v3_replay_executable_i20_summary.json
- outputs/theorems_v2/v3_replay_executable_i20_diagnostics.jsonl
- outputs/theorems_v2/v3_executable_i20_trajectories.jsonl
- outputs/theorems_v2/v3_executable_i20_selector_usable_trajectories.jsonl
- outputs/theorems_v2/v3_polynomial_elimination_newly_solved_i20.json