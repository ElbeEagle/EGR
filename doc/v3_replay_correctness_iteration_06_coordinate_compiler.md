# V3 Replay Correctness Iteration 06: Coordinate Equation Compiler

## Objective

Build a reusable coordinate/vector condition compiler instead of adding answer-specific theorem executors.

The compiler lowers structured geometry facts into auditable EquationConstraint facts and keeps source fact IDs in provenance.

## Implemented Rules

- right angle -> vector dot product equals zero;
- perpendicular line segments -> direction dot product equals zero;
- parallel line segments -> direction cross product equals zero;
- midpoint -> two coordinate equations;
- point distance -> squared-distance equation;
- requested dot product -> coordinate dot-product equation;
- vector scale relation -> two component equations;
- point on a constructed line -> determinant equals zero.

Ordinary participating points can receive on-demand coordinate variables. Named foci, vertices, centers, intersections, feet, tangent points, and midpoint targets remain owned by their semantic construction rules.

Conic focus and vertex coordinates can use unresolved parameter coordinates, such as (c, 0), before the parameter value is known.

## End-to-End Example

ID 1106 now follows this chain:

1. Model 5 creates the symbolic hyperbola standard form.
2. The asymptote point gives b2/a2 = 3.
3. RightFocus(C)=F gives F=(c,0).
4. Angle FPO=90 degrees compiles to a dot-product equation and resolves c=4.
5. Parameter-square closure resolves c2=16.
6. Model 12 plus exact elimination resolves a2=4 and b2=12.
7. The final standard equation is verified as correct.

## Benchmark

Input: data/train_with_models_v3_candidate.json

Sequence field: models_v3_executable

| Metric | i14 | i18 | Delta |
| --- | ---: | ---: | ---: |
| Rows | 5355 | 5355 | 0 |
| Applied steps | 8025 | 8093 | +68 |
| Sequence success | 664 | 670 | +6 |
| Answer correct | 244 | 245 | +1 |
| Selector usable | 232 | 233 | +1 |
| Answer incorrect | 2 | 2 | 0 |
| Unparsed fact atoms | 3717 | 3648 | -69 |
| Conflict steps | 0 | 0 | 0 |

No previously correct answer regressed, no successful sequence was lost, and no new incorrect answer was introduced.

Across successful exported trajectories, 35 rows contain compiled coordinate equations. The most frequent compiled rule is point distance.

## Engineering Corrections During Dry Run

An early on-demand coordinate version caused 88 conflicts because midpoint targets were assigned symbolic coordinates before model 54 produced them. Ownership was tightened, and model 54 was changed to avoid overwriting an already-known midpoint coordinate. The final i18 run has zero conflicts.

## Current Boundary

Equation generation is no longer the only blocker. Most newly generated systems contain multiple unknown coordinates with quadratic or bilinear terms. ExactEliminationClosure currently supports:

- exact multivariate linear systems;
- exact single-variable quadratic equations.

It does not yet solve general multivariate polynomial systems. Therefore free coordinate variables improve theorem applicability and state reachability more than final-answer correctness.

The next high-leverage module is a conservative multivariate quadratic eliminator with branch and positivity control. Adding more coordinate grammar before that solver exists will have diminishing returns.

## Artifacts

- src/theorems_v2/coordinate_equation_compiler.py
- outputs/theorems_v2/v3_replay_executable_i18_summary.json
- outputs/theorems_v2/v3_replay_executable_i18_diagnostics.jsonl
- outputs/theorems_v2/v3_executable_i18_trajectories.jsonl
- outputs/theorems_v2/v3_executable_i18_selector_usable_trajectories.jsonl