# V3 Replay Correctness Iteration 05: Condition Equations

## Scope

This iteration extends the information-space-to-elimination bridge for high-confidence conic conditions. It does not add answer-specific rules.

Implemented condition patterns:

- distance between the two named foci -> focal half-distance squared;
- scaled relation between major/minor or real/imaginary axis lengths -> squared semi-axis ratio;
- a known non-origin point on an asymptote -> linked asymptote line and exact slope;
- exact simplification of squared radicals and squared products;
- implicit positivity of squared standard-form denominators for single-conic states.

The multi-conic case remains conservative to avoid ambiguous theorem bindings.

## Benchmark

Input: data/train_with_models_v3_candidate.json

Sequence field: models_v3_executable

| Metric | i11 | i14 | Delta |
| --- | ---: | ---: | ---: |
| Rows | 5355 | 5355 | 0 |
| Applied steps | 7795 | 8025 | +230 |
| Sequence success | 635 | 664 | +29 |
| Sequence success rate | 11.858% | 12.400% | +0.542 pp |
| Answer correct | 231 | 244 | +13 |
| Selector usable | 220 | 232 | +12 |
| Answer incorrect | 2 | 2 | 0 |
| Unparsed fact atoms | 3742 | 3717 | -25 |

No previously correct row regressed, and no new incorrect answer was introduced.

## Representative gains

- ID 1651: focal length plus imaginary/real axis ratio now resolves the standard hyperbola equation.
- ID 2109: point coordinates on an asymptote now resolve its slope and eccentricity.
- ID 4553: asymptote point plus focal length now resolves both semi-axis squares.
- ID 579: focus separation is now represented as an exact parameter equation, but its current executable sequence still omits model 12.

## Remaining blockers

1. Sequence-label dependency gaps: ID 579 has [5, 21]; the information chain needs parameter relation model 12 before the asymptote result can be numeric.
2. Coordinate-angle equations: ID 1106 now has the asymptote ratio, but the right-angle condition has not yet been translated into the focal parameter equation.
3. Multi-conic binding: theorem models still rely on unique automatic binding. The single-conic positivity improvement is deliberately disabled when it would introduce a new ambiguity.
4. VALUE_UNRESOLVED increased because more formerly GOAL_NOT_REACHED rows now execute and expose symbolic downstream gaps. This is reachability progress, not a correctness regression.

## Artifacts

- outputs/theorems_v2/v3_replay_executable_i14_summary.json
- outputs/theorems_v2/v3_replay_executable_i14_diagnostics.jsonl
- outputs/theorems_v2/v3_executable_i14_trajectories.jsonl
- outputs/theorems_v2/v3_executable_i14_selector_usable_trajectories.jsonl
- outputs/theorems_v2/v3_condition_equation_newly_solved_i14.json