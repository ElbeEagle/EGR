# Task

Main-thread integration for the EGR AAAI2027 first-wave subagents.

Date: 2026-04-28

# Subagents Completed

- eval-protocol: completed. Added unified evaluation schema, CLI, tests, and 200-sample baseline artifacts.
- symbolic-solver: completed. Added symbolic solver utilities, improved query parsing / answer extraction / comparison, and regression tests.
- theorem-audit: completed. Added model files and tests for missing model IDs 18, 27, 38, and 64.
- entropy-estimator: completed. Added entropy label schema, dataset pipeline, learned-linear estimator, trajectory reports, and tests.
- search-strategies: completed. Added standalone search strategy interface, ablation CLI, tests, and 50-sample smoke artifacts.

# Files Changed

Main-thread integration change:

- `src/theorems/theorem_library.py`
  - Registered theorem-audit models 18, 27, 38, and 64.

Subagent changes:

- `src/evaluation/`
- `scripts/evaluation/`
- `tests/test_evaluation_protocol.py`
- `src/solver/`
- `src/reasoning/query_parser.py`
- `src/reasoning/answer_extractor.py`
- `src/reasoning/answer_comparator.py`
- `tests/test_answer_extractor_symbolic_solver.py`
- `tests/test_solver_symbolic.py`
- `src/theorems/models/model_018.py`
- `src/theorems/models/model_027.py`
- `src/theorems/models/model_038.py`
- `src/theorems/models/model_064.py`
- `tests/test_theorem_missing_models.py`
- `src/reasoning/entropy_estimator.py`
- `src/entropy/`
- `scripts/entropy/`
- `tests/test_entropy_dataset.py`
- `tests/test_entropy_estimator.py`
- `src/reasoning/search.py`
- `scripts/experiments/`
- `tests/test_search_strategies.py`
- `dev_logs/aaai2027/*_handoff.md`
- `outputs/evaluation/`
- `outputs/entropy/`
- `outputs/experiments/`
- `outputs/reasoning/solver_smoke_50.json`

# New Interfaces

Evaluation:

- `src.evaluation.protocol`
- `scripts/evaluation/run_eval_protocol.py`

Symbolic solver:

- `src.solver.SymbolicSolver`

Entropy:

- `src.entropy.*`
- `scripts/entropy/build_entropy_dataset.py`
- `scripts/entropy/train_entropy_estimator.py`
- `scripts/entropy/analyze_entropy_trajectories.py`
- `scripts/entropy/run_entropy_pipeline.py`
- `EntropyEstimator.from_model_file(...)`

Search:

- `src.reasoning.search.SearchSelectorAdapter`
- `src.reasoning.search.default_ablation_strategies()`
- `scripts/experiments/run_search_ablation.py`

Theorem library:

- `TheoremLibrary` now loads 56 registered models.
- Newly registered IDs: 18, 27, 38, 64.

# Metrics Before / After

Baseline from eval-protocol, 200 samples, seed 42:

- Reasoning success: `147/200 = 0.7350`
- Final answer accuracy: `5/200 = 0.0250`
- Answer accuracy among successful reasoning: `5/147 = 0.0340`

After integration, unified protocol, 200 samples, seed 42:

- Reasoning success: `130/200 = 0.6500`
- Final answer accuracy: `21/200 = 0.1050`
- Answer accuracy among successful reasoning: `21/130 = 0.1615`
- Theorem selection diagnostic top-1/top-3/top-5: `0.1096 / 0.2701 / 0.3690`

After integration, unified protocol, 50 samples, seed 42:

- Reasoning success: `36/50 = 0.7200`
- Final answer accuracy: `13/50 = 0.2600`
- Answer accuracy among successful reasoning: `13/36 = 0.3611`

Search ablation smoke, 50 samples, seed 42:

- `rule_only`: reasoning `30/50 = 0.6000`, final accuracy `11/50 = 0.2200`, avg steps `3.72`
- `neural_only`: reasoning `43/50 = 0.8600`, final accuracy `13/50 = 0.2600`, avg steps `6.12`
- `neural_rule`: reasoning `43/50 = 0.8600`, final accuracy `13/50 = 0.2600`, avg steps `4.62`
- `full_egr`: reasoning `43/50 = 0.8600`, final accuracy `13/50 = 0.2600`, avg steps `4.30`

Entropy estimator slice:

- Dataset slice: `11411` labels, `2325` trajectories, `0` skipped paths.
- Learned-linear validation: MAE `0.15422646`, Pearson `0.83736567`, Spearman `0.84929542`.
- Heuristic baseline: MAE `0.28448212`, Pearson `0.39034497`, Spearman `0.44981156`.

# Tests Run

```bash
python -c "from src.theorems import TheoremLibrary; lib=TheoremLibrary(); print(len(lib)); print([m for m in [18,27,38,64] if lib.has_model(m)]); print(lib.get_available_models())"
```

Result: `56` registered models; IDs `18, 27, 38, 64` present.

```bash
python -m pytest tests/test_evaluation_*.py tests/test_answer_extractor*.py tests/test_solver*.py tests/test_theorem_*.py tests/test_entropy*.py tests/test_search*.py
```

Result: `49 passed`.

```bash
python scripts/evaluation/run_eval_protocol.py --num 50 --seed 42 --output-dir outputs/evaluation/main_integration_50
python scripts/evaluation/run_eval_protocol.py --num 200 --seed 42 --output-dir outputs/evaluation/main_integration_200
python scripts/experiments/run_search_ablation.py --num 50 --seed 42 --strategies all --output-dir outputs/experiments/main_search_ablation_50 --quiet
```

Result: completed and wrote artifacts.

```bash
git diff --check
python -m compileall src scripts
```

Result: passed.

# Known Risks

- Final answer accuracy improved substantially on the 200-sample protocol slice, but reasoning success dropped from `0.7350` to `0.6500`. This should be investigated before framing the change as an unqualified end-to-end improvement.
- The theorem-selection metric in the unified protocol is a trace-vs-gold-sequence diagnostic. It is not yet a publication-grade selector benchmark because reasoning traces can diverge from annotated model sequences.
- The learned entropy estimator is validated against remaining-step supervision, not final answer correctness. Do not claim answer-correctness correlation yet.
- Search ablation results are smoke-level. The 50-sample run confirms the interface and table format, not final AAAI evidence.
- New theorem models are now registered, but their actual impact on end-to-end accuracy still needs targeted error analysis.
- The symbolic solver is intentionally pattern-focused. Unsupported optimization/locus/tangent cases remain.

# Integration Notes

- No push was performed.
- No worktree was created.
- The only protected hot file edited by the main thread was `src/theorems/theorem_library.py` for model registration.
- `src/reasoning/reasoning_engine.py`, `src/reasoning/model_selector.py`, and `tex/icml2026.tex` were not modified.
- Keep `outputs/evaluation/main_integration_200/summary.json` as the current first-wave integrated benchmark artifact.

# Next Round Recommendations

1. Investigate the reasoning-success drop after symbolic-solver changes.
2. Add targeted eval slices for query types where accuracy improved: `Equation`, `Range`, `Coordinate`.
3. Join entropy reports with end-to-end answer correctness before making paper claims about `H(S)`.
4. Run 200-sample or larger search ablations after deciding whether repeated model application should be allowed.
5. Continue theorem-audit next candidates: 39, 45, 58, 67, 71.
