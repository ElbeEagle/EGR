# Search Strategies Design

## Scope

This worker adds a standalone search-strategy layer for AAAI2027 ablation
experiments. It does not modify the main reasoning loop, model selector,
theorem library, answer extractor, checkpoints, raw data, or paper TeX.

## Strategy Interface

`src/reasoning/search.py` defines:

- `SearchStrategyConfig`: run metadata for strategy name, seed, sample size,
  checkpoint path, max steps, top-k, lambda weights, and repeated-model policy.
- `SearchContext`: inputs supplied at each decision point: symbolic state,
  abstract state, theorem library, optional neural network, optional state
  constructor, entropy estimator, device, top-k, lambda weights, and excluded
  model IDs.
- `SearchCandidate`: serializable candidate-level record for traces.
- `SearchDecision`: strategy output with `to_selection_info()` for
  `ReasoningEngine` compatibility.
- `SearchSelectorAdapter`: exposes any standalone strategy through the existing
  `select(symbolic_state, abstract_state, ...) -> (model, selection_info)`
  protocol.

The adapter is the integration seam: scripts can pass it into
`ReasoningEngine` without changing `src/reasoning/reasoning_engine.py`.

## Ablation Strategies

All strategies use the same top-k candidate budget and emit the same candidate
trace schema.

| Strategy | Neural P(Y|X) | can_apply filter | InfoGain | Selection rule |
| --- | --- | --- | --- | --- |
| `rule_only` | No | Yes | No | First applicable theorem in fixed theorem-id order |
| `neural_only` | Yes | No | No | Highest neural-probability available theorem |
| `neural_rule` | Yes | Yes | No | First applicable theorem in neural top-k order |
| `full_egr` | Yes | Yes | Yes | Maximize `lambda1 * P(Y|X) + lambda2 * InfoGain - lambda3 * H(Y|X)` |

`neural_only` records `can_apply` as diagnostics but does not use it for
selection. `full_egr` currently follows the existing prototype convention where
`H(Y|X)` is the distribution-level prediction entropy, so it affects absolute
score values but not candidate ranking within a single step.

## Experiment Entrypoint

`scripts/experiments/run_search_ablation.py` runs one or more strategies over
the same sampled dataset:

```bash
python scripts/experiments/run_search_ablation.py \
  --num 50 \
  --seed 42 \
  --strategies all \
  --checkpoint checkpoints/model_selector_v2.pth \
  --output-dir outputs/experiments/search_ablation_smoke
```

The script writes per-strategy eval protocol artifacts:

- `<output-dir>/<strategy>/report.json`
- `<output-dir>/<strategy>/summary.json`
- `<output-dir>/<strategy>/samples.jsonl`
- `<output-dir>/<strategy>/summary.csv`

It also writes a cross-strategy table:

- `<output-dir>/ablation_summary.json`
- `<output-dir>/ablation_summary.csv`

## JSON/CSV Schema

Per-strategy reports reuse `egr_eval_protocol_v1` and add run metadata:

- `strategy`
- `seed`
- `sample_size`
- `checkpoint_path`
- `max_steps`
- `top_k`
- `lambda_weights`
- `avoid_repeated_models`
- `selector_metadata`

The ablation table uses `egr_search_ablation_table_v1` rows with:

- strategy/config fields: `strategy`, `seed`, `sample_size`,
  `checkpoint_path`, `max_steps`, `top_k`, `lambda_1_p_y_x`,
  `lambda_2_info_gain`, `lambda_3_h_y_x`
- reasoning metrics: `reasoning_success_count`,
  `reasoning_success_rate`, `final_answer_correct_count`,
  `final_answer_accuracy`, `answer_accuracy_among_successful_reasoning`
- process metrics: `avg_steps`, `avg_steps_successful_reasoning`
- theorem-selection diagnostics: labeled step count and top-1/top-3/top-5
  accuracy from the eval protocol
- entropy/search diagnostics: average prediction entropy, info gain, and score
- failure distributions: final-outcome failures and reasoning-only failures

This keeps reasoning success and final answer accuracy separate for paper
tables.

## Integration Notes

- The main integration thread can later replace `ModelSelector` construction
  with `SearchSelectorAdapter` in a controlled patch if the standalone
  experiments prove useful.
- If repeated-model policy should exactly match the current baseline, run with
  `--allow-repeated-models`. The default excludes
  `symbolic_state.applied_models` plus retry-local exclusions to reduce loops.
- A future beam-search extension should use the same `SearchCandidate` and
  `SearchDecision` records, but this worker intentionally did not implement
  MCTS.
