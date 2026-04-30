# Entropy Estimator Worker Handoff

## Scope

Worker: Entropy Estimator

Editable scope used:
- `src/reasoning/entropy_estimator.py`
- `src/entropy/`
- `scripts/entropy/`
- `outputs/entropy/`
- `tests/test_entropy*.py`
- `dev_logs/aaai2027/entropy_estimator_handoff.md`

Forbidden files touched by this worker: none.

Note: the shared checkout already contains other workers' changes outside this scope. I did not revert or edit them.

## What Was Implemented

1. Entropy label schema
   - Schema version: `entropy-label-v1`.
   - Primary learned target: `normalized_remaining_steps = remaining_steps / sequence_length`.
   - Complementary target: `progress = 1 - normalized_remaining_steps`.
   - Baseline feature retained: `completeness_score`, explicitly marked as a heuristic baseline rather than final truth.
   - Path labels:
     - `model`: annotated model sequence from `data/train_with_models_v2.json`.
     - `correct`: subset of annotated paths that are fully executable by the current theorem library.
     - `random`: random implemented-model sequence with the same length as the annotated path.

2. Dataset builder
   - CLI: `python scripts/entropy/build_entropy_dataset.py`.
   - Reusable output: `outputs/entropy/entropy_dataset.jsonl`.
   - Summary output: `outputs/entropy/entropy_dataset_summary.json`.
   - Includes per-path timeout support to skip pathological theorem applications without blocking the worker.

3. Heuristic vs learned estimator interface
   - Existing heuristic estimator remains backward compatible.
   - Added learned-linear mode in `EntropyEstimator`.
   - Learned model file format is JSON with `weights` and `bias`.
   - Integration entry point:
     ```python
     from src.reasoning.entropy_estimator import EntropyEstimator
     estimator = EntropyEstimator.from_model_file("outputs/entropy/learned_entropy_estimator.json")
     entropy = estimator.estimate(abstract_state)
     ```

4. Learned estimator training
   - CLI: `python scripts/entropy/train_entropy_estimator.py`.
   - Lightweight ridge regression over `AbstractState.to_vector()` features.
   - Target: normalized remaining-step entropy.
   - Model output: `outputs/entropy/learned_entropy_estimator.json`.
   - Metrics output: `outputs/entropy/training_metrics.json`.

5. Trajectory and correlation reports
   - CLI: `python scripts/entropy/analyze_entropy_trajectories.py`.
   - One-shot pipeline: `python scripts/entropy/run_entropy_pipeline.py`.
   - Reports:
     - `outputs/entropy/trajectory_report.json`
     - `outputs/entropy/correlation_summary.json`

## Generated Evidence

Command used for the committed output slice:

```bash
python scripts/entropy/run_entropy_pipeline.py --max-samples 1000 --sample-timeout-seconds 0.5
```

Output slice:
- Entries: `11411`
- Trajectories: `2325`
- Skipped paths: `0`
- Path counts:
  - `model`: `4988` entries, `1000` trajectories
  - `correct`: `1435` entries, `325` trajectories
  - `random`: `4988` entries, `1000` trajectories

Training on `model` path entries:
- Selected training entries: `4988`
- Heuristic baseline vs target:
  - MAE: `0.28448212`
  - Pearson: `0.39034497`
  - Spearman: `0.44981156`
- Learned-linear validation vs target:
  - MAE: `0.15422646`
  - Pearson: `0.83736567`
  - Spearman: `0.84929542`

Trajectory report:
- Correct paths:
  - executable rate: `1.0`
  - avg heuristic entropy delta: `0.34574154`
  - avg learned entropy delta: `0.56455453`
  - learned monotonicity rate: `1.0`
- Model paths:
  - executable rate: `0.325`
  - avg heuristic entropy delta: `0.236772`
  - avg learned entropy delta: `0.58696003`
  - learned monotonicity rate: `0.99848929`
- Random paths:
  - executable rate: `0.015`
  - avg heuristic entropy delta: `0.078939`
  - avg learned entropy delta: `0.54205692`
  - learned monotonicity rate: `0.99935714`

Correlation summary over all generated entries:
- Heuristic entropy vs normalized remaining steps:
  - Pearson: `0.3484877`
  - Spearman: `0.44323723`
- Learned entropy vs normalized remaining steps:
  - Pearson: `0.83254101`
  - Spearman: `0.85925063`
- Answer correctness:
  - Not available in this dataset-derived report. Do not claim answer-correctness correlation yet.

## What Supports Paper Claims

Supported cautiously:
- `H(S)` can now be treated as a trainable state-progress estimator rather than only `1 - completeness_score`.
- Learned entropy has much stronger correlation with remaining-step supervision than the current heuristic baseline on the generated slice.
- Correct/model/random trajectories are now comparable under the same schema and report format.
- The report shows that executable correct paths have clearer entropy reduction than random paths under the heuristic baseline.

## What Does Not Yet Support Paper Claims

Not supported yet:
- No answer-correctness correlation claim. `answer_correct` is unavailable in `train_with_models_v2.json`-derived labels.
- No final end-to-end solver improvement claim. This worker did not integrate the estimator into `reasoning_engine.py`.
- No theorem-selector improvement claim. The learned estimator predicts state-progress entropy, not `P(Y|X)`.
- No full-dataset claim. A full unbounded pipeline was attempted but was too slow without per-path timeout/progress. The produced evidence is a reproducible 1000-sample slice.

## Commands Run

```bash
git status --short
sed -n '1,260p' agent_prompt/04_entropy_estimator_agent.md
rg -n "EGR|Entropy|entropy|Conic10K|reasoning_engine" /Users/ebeleagel/.codex/memories/MEMORY.md
sed -n '47,106p' /Users/ebeleagel/.codex/memories/MEMORY.md
sed -n '1,220p' /Users/ebeleagel/.codex/memories/rollout_summaries/2026-04-24T06-55-34-28qd-egr_project_analysis_aaai2027_parallel_workflow.md
sed -n '1,260p' src/reasoning/entropy_estimator.py
sed -n '1,320p' src/state/abstract_state.py
sed -n '1,320p' src/state/state_sequence_builder.py
sed -n '1,260p' 'docs/Three-layer entropy.md'
sed -n '1,260p' 'docs/状态表示+3层熵.md'
sed -n '1,320p' 'handbook/符号约束图/entropy_modeling_conic_doc.md'
jq 'length, .[0], .[1]' data/train_with_models_v2.json
jq '.total_samples, .total_transitions, (.sample_results | length), .sample_results[0], .sample_results[1]' data/train_state_model_v2.json
python -m pytest tests/test_entropy*.py
python scripts/entropy/run_entropy_pipeline.py --max-samples 20
python scripts/entropy/run_entropy_pipeline.py
kill <full-pipeline-pid>
python scripts/entropy/run_entropy_pipeline.py --max-samples 1000
kill <slow-pipeline-pid>
python scripts/entropy/run_entropy_pipeline.py --max-samples 1000 --sample-timeout-seconds 0.5
jq '{entry_count, trajectory_count, path_type_counts, skipped_path_count, by_path_type}' outputs/entropy/entropy_dataset_summary.json
jq '.' outputs/entropy/training_metrics.json
jq '{trajectory_count, by_path_type}' outputs/entropy/trajectory_report.json
jq '.' outputs/entropy/correlation_summary.json
wc -l outputs/entropy/entropy_dataset.jsonl
python -m compileall src/entropy scripts/entropy src/reasoning/entropy_estimator.py
git status --short
```

## Tests

Passed:

```bash
python -m pytest tests/test_entropy*.py
```

Result: `6 passed`.

Passed:

```bash
python -m compileall src/entropy scripts/entropy src/reasoning/entropy_estimator.py
```

Result: no compile errors.

## Integration Notes

Recommended next integration step:
- Integration thread can load `outputs/entropy/learned_entropy_estimator.json` through `EntropyEstimator.from_model_file(...)`.
- Replace or compare the existing heuristic `H(S)` only inside an integration-owned branch/thread, because `src/reasoning/reasoning_engine.py` and `src/reasoning/model_selector.py` are forbidden for this worker.

Suggested evaluation before paper claim:
- Join entropy trajectories with end-to-end reasoning results that contain final answer correctness.
- Report correlations separately for:
  - remaining steps,
  - path executability/process success,
  - final answer correctness.
- Keep heuristic and learned estimators side-by-side in all tables until learned `H(S)` has end-to-end evidence.
