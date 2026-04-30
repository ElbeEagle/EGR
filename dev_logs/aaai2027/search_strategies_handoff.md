# Search Strategies Handoff

## Task

Implement a standalone search-strategy layer for AAAI2027 ablations without
modifying shared reasoning/theorem/paper hot files.

## Shared Checkout

- CWD: `/Users/ebeleagel/Documents/GitHub/EGR`
- No worktree created.
- No push performed.

## Files Changed By This Worker

- `src/reasoning/search.py`
- `scripts/experiments/run_search_ablation.py`
- `tests/test_search_strategies.py`
- `dev_logs/aaai2027/search_strategies_design.md`
- `dev_logs/aaai2027/search_strategies_handoff.md`
- `outputs/experiments/search_ablation_10_smoke/`

## Forbidden Files

This worker did not modify these protected files:

- `src/reasoning/reasoning_engine.py`
- `src/reasoning/model_selector.py`
- `src/theorems/theorem_library.py`
- `tex/icml2026.tex`

Verification command:

```bash
git status --short -- src/reasoning/reasoning_engine.py src/reasoning/model_selector.py src/theorems/theorem_library.py tex/icml2026.tex
```

Output was empty.

Current `git status --short` also shows other parallel-worker changes in solver,
answer parsing, entropy, theorem, and evaluation areas. They were not touched by
this worker.

## New Interfaces

`src/reasoning/search.py` provides:

- `SearchStrategyConfig`
- `SearchContext`
- `SearchCandidate`
- `SearchDecision`
- `SearchSelectorAdapter`
- `RuleOnlyStrategy`
- `NeuralOnlyStrategy`
- `NeuralRuleStrategy`
- `FullEGRStrategy`
- `default_ablation_strategies()`
- `normalize_strategy_name()`

The adapter exposes the existing `ReasoningEngine` selector protocol:

```python
select(symbolic_state, abstract_state, top_k=None, excluded_models=None)
    -> (selected_model, selection_info)
```

No main-loop integration was performed.

## Strategy Definitions

| Strategy | Meaning |
| --- | --- |
| `rule_only` | Fixed theorem-id order plus `can_apply`, no neural network |
| `neural_only` | Neural `P(Y|X)` order, no `can_apply` filtering or InfoGain in selection |
| `neural_rule` | Neural `P(Y|X)` order plus `can_apply` filtering |
| `full_egr` | Neural `P(Y|X)` plus `can_apply` plus `InfoGain - H(Y|X)` scoring |

All strategies emit candidate traces compatible with
`src.evaluation.protocol.compute_trace_selection_metrics()`.

## Experiment CLI

Entrypoint:

```bash
python scripts/experiments/run_search_ablation.py \
  --num 50 \
  --seed 42 \
  --strategies all \
  --checkpoint checkpoints/model_selector_v2.pth \
  --output-dir outputs/experiments/search_ablation_smoke
```

Outputs:

- Per strategy: `report.json`, `summary.json`, `samples.jsonl`, `summary.csv`
- Cross-strategy table: `ablation_summary.json`, `ablation_summary.csv`

The ablation table records strategy, seed, sample size, checkpoint, max steps,
top-k, lambda weights, reasoning success, final answer accuracy, answer
accuracy among successful reasoning cases, average steps, theorem-selection
diagnostics, entropy/search diagnostics, and failure distributions.

## Smoke Run

Command:

```bash
python scripts/experiments/run_search_ablation.py --num 10 --seed 42 --strategies all --output-dir outputs/experiments/search_ablation_10_smoke --quiet
```

Results:

| Strategy | Reasoning success | Final answer correct | Avg steps |
| --- | ---: | ---: | ---: |
| `rule_only` | `6/10 = 0.6000` | `2/10 = 0.2000` | `5.00` |
| `neural_only` | `8/10 = 0.8000` | `2/10 = 0.2000` | `7.50` |
| `neural_rule` | `8/10 = 0.8000` | `2/10 = 0.2000` | `5.30` |
| `full_egr` | `8/10 = 0.8000` | `2/10 = 0.2000` | `4.90` |

Artifact root:

- `outputs/experiments/search_ablation_10_smoke/`

This is only a smoke test, not a publication-grade result.

## Tests And Commands Run

```bash
python -m pytest tests/test_search*.py
python scripts/experiments/run_search_ablation.py --num 10 --seed 42 --strategies all --output-dir outputs/experiments/search_ablation_10_smoke --quiet
jq '.rows[] | {strategy: .strategy, reasoning_success_rate: .reasoning_success_rate, final_answer_accuracy: .final_answer_accuracy, avg_steps: .avg_steps}' outputs/experiments/search_ablation_10_smoke/ablation_summary.json
python -m pytest tests/test_search*.py tests/test_evaluation_protocol.py
python -m pytest tests/test_search*.py
git status --short
```

Final passing checks:

- `python -m pytest tests/test_search*.py`: `6 passed`
- `python -m pytest tests/test_search*.py tests/test_evaluation_protocol.py`: `10 passed`

One earlier test run failed because the dummy test probabilities did not put the
intended applicable model inside the top-k candidate window. The fixture was
fixed; no production code change was required for that failure.

## Known Risks

- The default adapter excludes `symbolic_state.applied_models` in addition to
  retry-local exclusions. Use `--allow-repeated-models` if the integration
  thread wants to mimic the current baseline more closely.
- `neural_only` still requires a registered theorem object to return a model;
  it does not use `can_apply` for selection, but it cannot apply model IDs that
  are absent from `TheoremLibrary`.
- `full_egr` uses the same scalar `H(Y|X)` convention as the existing prototype.
  Because it is constant across candidates within one step, it changes score
  scale but not within-step ranking.
- The smoke run used 10 samples. Full ablation should be rerun with the eval
  protocol sample size chosen by the main thread.

## Suggested Integration Patch

No protected-file patch is required for this worker's deliverable.

If the main thread later wants to run the new strategies through the standard
reasoning script, the safe integration point is to instantiate
`SearchSelectorAdapter` where `ModelSelector` is currently constructed, gated by
a CLI flag. That patch should be owned by the integration thread because it
would touch `src/reasoning/model_selector.py` callers or reasoning scripts.
