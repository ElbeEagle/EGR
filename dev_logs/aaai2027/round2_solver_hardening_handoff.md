# Round 2 Solver Hardening Handoff

Date: 2026-05-19

Subagent: `solver-hardening`

## Scope

Worked in the shared checkout only. No worktree, commit, push, reset, restore,
checkout, clean, unstage, `.env`, secret, selector, theorem-library, reasoning
engine, or paper changes were made.

## What Changed

- Added focused regression coverage for the two primary correct-to-wrong cases:
  - `360`: `LineSegmentOf(F, R) -> 2`
  - `2252`: `Slope(OverlappingLine(LineSegmentOf(A, B))) -> 2`
- Extended `AnswerExtractor` routing for:
  - `LineSegmentOf(...)`
  - `Slope(...)`
  - `Min(...)` / `Max(...)`
  - `AngleOf(...)`
  - algebraic expressions containing `Abs(LineSegmentOf(...))`
- Added narrow SymPy-backed solver support for common Parabola/Value failures:
  - line segment length from explicit line-curve intersections
  - parabola chord slope from midpoint
  - parabola chord length from midpoint
  - parabola point-to-focus distance from `XCoordinate` / `YCoordinate`
  - parabola point-to-focus distance from distance to the axis
  - focus-chord slope from midpoint-directrix distance
  - reflected minimum `Min(|PA| + |PF|)` via distance from fixed point to directrix
  - the `360` midpoint/projection/angle construction as a formal-geometry pattern
- Preserved formal facts previously dropped by `StateConstructor`:
  - unmatched coordinate forms such as `XCoordinate(P)=4`
  - nested coordinate facts such as `Coordinate(OneOf(Focus(G))) = (0, 2)`
  - `IsChordOf(...)`

## Files Updated

- `src/reasoning/answer_extractor.py`
- `src/solver/symbolic_solver.py`
- `src/state/state_constructor.py`
- `tests/test_answer_extractor_symbolic_solver.py`
- `tests/test_solver_symbolic.py`

## Validation

```bash
python -m pytest tests/test_answer_extractor*.py tests/test_solver*.py
```

Result: `46 passed`.

```bash
python -m py_compile src/reasoning/answer_extractor.py src/reasoning/query_parser.py src/reasoning/answer_comparator.py src/solver/symbolic_solver.py src/state/state_constructor.py
```

Result: passed.

```bash
python scripts/evaluation/run_eval_protocol.py --num 200 --seed 42 --output-dir outputs/evaluation/round2_solver_smoke
```

Result artifacts:

- `outputs/evaluation/round2_solver_smoke/report.json`
- `outputs/evaluation/round2_solver_smoke/summary.json`
- `outputs/evaluation/round2_solver_smoke/samples.jsonl`
- `outputs/evaluation/round2_solver_smoke/summary.csv`

`git diff --check` passed.

Forbidden-scope diff check produced no output:

```bash
git diff --name-only -- src/reasoning/reasoning_engine.py src/reasoning/model_selector.py src/theorems src/selector tex/icml2026.tex
```

## Metrics

Comparison baseline: `outputs/evaluation/main_integration_200/summary.json`

| metric | main integration 200 | solver hardening smoke | delta |
| --- | ---: | ---: | ---: |
| Final answer correct | 21/200 | 33/200 | +12 |
| Final answer accuracy | 10.5% | 16.5% | +6.0 pp |
| Reasoning success | 130/200 | 140/200 | +10 |
| Reasoning success rate | 65.0% | 70.0% | +5.0 pp |
| Answer accuracy among successful reasoning | 16.15% | 23.57% | +7.42 pp |

Sample-level final-answer transitions vs `main_integration_200`:

- wrong -> correct: `12`
- correct -> correct: `21`
- correct -> wrong: `0`
- wrong -> wrong: `167`

Sample-level reasoning-success transitions vs `main_integration_200`:

- failure -> success: `10`
- success -> success: `130`
- success -> failure: `0`
- failure -> failure: `60`

Recovered / newly correct samples:

- `360`: `LineSegmentOf(F, R)`, `LineSegmentOf not found -> 2`
- `780`: `Slope(l)`, `Slope not found -> pm*1`
- `852`: `Slope(LineOf(P, Q))`, `Slope not found -> p/y0`
- `1788`: `k`, `k: Real -> 1`
- `2207`: `Abs(LineSegmentOf(P,F))`, unevaluated expression -> `13`
- `2252`: `Slope(OverlappingLine(LineSegmentOf(A, B)))`, `Slope not found -> 2`
- `3783`: `Abs(LineSegmentOf(A, B))`, `not found -> 4*sqrt(2)`
- `3858`: `Min(Abs(LineSegmentOf(P, A)) + Abs(LineSegmentOf(P, F)))`, `not found -> 6`
- `5711`: same `Min` pattern, `not found -> 7`
- `6177`: `Abs(LineSegmentOf(P, F))`, `not found -> 6`
- `7184`: same `Min` pattern, `not found -> 6`
- `7714`: `Abs(LineSegmentOf(A, B))`, `not found -> 8`

Original round2 accuracy gains preserved:

- Kept `18/18` cases from `outputs/evaluation/round2_error_audit/accuracy_gain_top20.csv`
- Lost `0/18`

## Risk / Notes

- The patch is intentionally exact-pattern based. Unsupported optimization and
  tangent/chord variants still return `not found`.
- `StateConstructor` now preserves more formal coordinate/chord facts as
  geometric relations. This improved answer extraction without changing theorem
  routes; theorem-selection step counts and top-k metrics stayed unchanged.
- This does not weaken final-answer correctness. The eval gains come from exact
  answers, and there were no final-answer or reasoning-success regressions in
  the 200-sample comparison.
