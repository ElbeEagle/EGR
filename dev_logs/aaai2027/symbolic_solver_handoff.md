# Symbolic Solver Handoff

## Scope

This worker improved query parsing, answer extraction, and lightweight symbolic solving for high-frequency final-answer failures. The changes are limited to the symbolic-solver allowlist:

- `src/reasoning/query_parser.py`
- `src/reasoning/answer_extractor.py`
- `src/reasoning/answer_comparator.py`
- `src/solver/__init__.py`
- `src/solver/symbolic_solver.py`
- `tests/test_answer_extractor_symbolic_solver.py`
- `tests/test_solver_symbolic.py`
- `dev_logs/aaai2027/symbolic_solver_handoff.md`

No selector, theorem library, reasoning engine, paper, checkpoint, or raw data file was intentionally modified.

## What Changed

- Added a `src/solver/` module with exact SymPy-backed helpers for axis-aligned conics, expression assignment parsing, line slope extraction, ranges, distances, coordinates, and focused parameter solving.
- Extended `QueryParser` to support multi-query strings, top-level function argument parsing, nested functions beyond the previous one-regex case, and algebraic expressions such as `b/a`.
- Reworked `AnswerExtractor` to route `Expression`, `Equation`, `Range`, `Coordinate`, `Distance`, `Area`, `Abs`, and multi-query requests through structured solver paths before falling back.
- Improved `answer_comparator` for coordinate tuples, simple set-valued answers, normalized expression strings, and scalar-multiple equation equivalence.
- Added 29 focused tests covering solver primitives and answer-extractor regressions.

## Newly Supported Query Patterns

- `Expression(G)` / `Expression(C)` for centered ellipse and hyperbola equations when parameters can be inferred from focal length, eccentricity, shared focus, point-on-curve, or focal-chord constraints.
- `Expression(Asymptote(G))` for centered hyperbolas, including cases where `a` is inferred from a shared parabola focus.
- `Eccentricity(G)` for direct conic equations such as `x^2 + 4*y^2 = 16`.
- `Range(a)` / `Range(k)` for denominator-sign constraints in centered conic equations, including ellipse positivity with circle-case exclusion and hyperbola opposite-sign ranges.
- `Coordinate(P)` for a point on a standard parabola with known distance to its focus.
- `Coordinate(Focus(G))` and `Distance(Focus(G), Directrix(G))` for standard parabolas.
- Direct coordinate distance and triangle area from known coordinates.
- Multi-query outputs such as `Eccentricity(H);Expression(G)`.

## Still Unsupported / Partial

- Optimization queries such as `Max(Length(...))`, `Min(Distance(...))`, and `Max(x1^2+2*y1)` remain mostly unsupported.
- Slope/inclination queries are only handled when the exact relation is already present.
- Complex geometry requiring theorem-level construction, e.g. chord midpoint constraints, tangent locus equations, and general triangle/foci distance derivations, is not implemented here.
- Some formal facts are currently lost by `StateConstructor` because it does not retain expressions such as `XCoordinate(P)=4`, `In(e,(1,2))`, or some object equalities; this solver does not modify `StateConstructor` by design.

## Metrics

Existing repo report before this worker:

- `outputs/reasoning/batch_test_report.json`: 200 samples, reasoning success `147/200 = 73.5%`, final answer accuracy `5/200 = 2.5%`.

Same 50-sample smoke command before/after this worker:

- Before: `0/50 = 0.0%` final answer accuracy, reasoning success `39/50 = 78.0%`.
- After: `13/50 = 26.0%` final answer accuracy, reasoning success `36/50 = 72.0%`.
- After by query type on the 50-sample smoke:
  - `Equation`: `6/9 = 66.7%`
  - `Range`: `2/4 = 50.0%`
  - `Coordinate`: `1/2 = 50.0%`
  - `Value`: `3/18 = 16.7%`
  - `Eccentricity`: `1/11 = 9.1%`
  - `Distance`: `0/5 = 0.0%`

The smoke report was written to `outputs/reasoning/solver_smoke_50.json`.

## Tests Run

```bash
python -m pytest tests/test_answer_extractor*.py tests/test_solver*.py
```

Result: `29 passed`.

```bash
python scripts/reasoning/batch_test.py --num 50 --seed 42 --output outputs/reasoning/solver_smoke_50.json
```

Result: `13/50` final answer correct, `26.0%` final answer accuracy.

## Known Risks

- The new solver is intentionally narrow and exact-pattern based. It should return `not found` for unsupported cases, but generated intermediate relations from other future workers may expose new symbolic forms that need small adapters.
- `answer_comparator` now accepts scalar-multiple equation equivalence and coordinate component equivalence. This is useful for conic equations but should be reviewed by the eval-protocol worker before being used as the only publication metric.
- The `LeftVertex/RightFocus` parabola derivation follows the current formal annotation behavior observed in the regression sample; integration should verify this convention against theorem-audit notes.

## Integration Notes

- This worker did not touch forbidden files. I checked the protected diff set with:

```bash
git diff --name-only -- src/selector src/theorems src/reasoning/model_selector.py src/reasoning/reasoning_engine.py src/theorems/theorem_library.py tex/icml2026.tex
```

The command produced no output.

- The shared checkout already contains unrelated modified/untracked files from other workers, including entropy/evaluation/search/theorem-audit paths. Do not attribute those to this symbolic-solver worker during integration.
