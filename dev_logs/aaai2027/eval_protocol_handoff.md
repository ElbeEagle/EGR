# Eval Protocol Handoff

## Task

Build a unified evaluation protocol for the AAAI2027 first-wave EGR work without changing reasoning behavior.

## Branch / Worktree

- Shared checkout: `/Users/ebeleagel/Documents/GitHub/EGR`
- No worktree created.
- No push performed.

## Files Changed

- `src/evaluation/__init__.py`
- `src/evaluation/protocol.py`
- `scripts/evaluation/run_eval_protocol.py`
- `tests/test_evaluation_protocol.py`
- `outputs/evaluation/baseline_200.json`
- `outputs/evaluation/protocol_200_smoke/report.json`
- `outputs/evaluation/protocol_200_smoke/summary.json`
- `outputs/evaluation/protocol_200_smoke/samples.jsonl`
- `outputs/evaluation/protocol_200_smoke/summary.csv`
- `dev_logs/aaai2027/eval_protocol_handoff.md`

## Forbidden Files

This worker did not modify the forbidden files:

- `src/reasoning/reasoning_engine.py`
- `src/reasoning/model_selector.py`
- `src/theorems/`
- `src/selector/`
- `tex/icml2026.tex`
- checkpoints
- raw data files

`git status --short` shows other parallel-worker changes outside this scope, including `src/reasoning/entropy_estimator.py`, `src/entropy/`, `src/theorems/models/model_*.py`, `tests/test_theorem_missing_models.py`, `outputs/reasoning/solver_smoke_50.json`, `dev_logs/aaai2027/theorem_audit_handoff.md`, and `dev_logs/aaai2027/theorem_audit_report.md`. They were not touched by this worker.

## New Interfaces

### Python library

`src.evaluation.protocol` provides:

- `build_sample_report(sample, result, final_answer_correct, exception=None)`
- `summarize_samples(samples)`
- `build_eval_report(samples, run_metadata=None, selector_report=None)`
- `write_eval_artifacts(report, output_dir)`
- `detect_curve_type(facts)`
- `detect_query_type(query)`
- `compute_trace_selection_metrics(trace, label_sequence)`

### CLI

```bash
python scripts/evaluation/run_eval_protocol.py \
  --num 200 \
  --seed 42 \
  --output-dir outputs/evaluation/protocol_200_smoke
```

The CLI reuses `scripts/reasoning/batch_test.py:init_engine` and `load_test_data`, then only records and aggregates outputs. It does not change the reasoning engine, selector, theorem library, or dataset.

## Sample-Level Schema

Each sample report uses schema version `egr_eval_protocol_v1` and includes:

- `sample_id`
- `facts`
- `query`
- `expected_answer`
- `predicted_answer`
- `final_answer_correct`
- `reasoning_success`
- `failure_reason`
- `reasoning_failure_reason`
- `raw_failure_reason`
- `applied_model_sequence`
- `applied_model_names`
- `model_level_trace`
- `theorem_selection`
- `curve_type`
- `query_type`
- `num_steps`
- `elapsed_time`

`failure_reason` is final-outcome oriented:

- `None` for final-answer-correct samples.
- `answer_mismatch` for reasoning-successful but final-answer-wrong samples.
- normalized reasoning failures such as `max_steps`, `no_model`, `apply_failed`, `exception`, or `other`.

`reasoning_failure_reason` only records failed reasoning cases, so downstream analysis can separate process failure from answer mismatch.

## Summary Schema

`summary.json` contains:

- `overall`: total samples, reasoning success count/rate, final answer correct count/accuracy, answer accuracy among successful reasoning, average elapsed time, theorem-selection top-k counts/rates.
- `theorem_selection`: top-1/top-3/top-5 theorem selection metrics over labeled trace steps.
- `by_curve_type`
- `by_query_type`
- `by_failure_reason`
- `failure_reason_distribution`
- `reasoning_failure_reason_distribution`
- `model_id_usage`
- `by_model_id`
- `model_id_failure_distribution`
- `external_selector_report` when an existing selector report is available.

`summary.csv` flattens overall, curve, query, failure-reason, and model-id groups for direct table loading.

## Commands Run

```bash
python -m pytest tests/test_evaluation_protocol.py
python scripts/evaluation/run_eval_protocol.py --num 5 --seed 42 --output-dir outputs/evaluation/protocol_5_smoke
rm -rf outputs/evaluation/protocol_5_smoke
python scripts/evaluation/run_eval_protocol.py --num 200 --seed 42 --output-dir outputs/evaluation/protocol_200_smoke
python scripts/reasoning/batch_test.py --num 200 --seed 42 --output outputs/evaluation/baseline_200.json
python -m pytest tests/test_evaluation_*.py
git status --short
```

## Baseline Numbers

From `outputs/evaluation/protocol_200_smoke/summary.json`:

- Total samples: `200`
- Reasoning success: `147/200 = 0.7350`
- Final answer correct: `5/200 = 0.0250`
- Answer accuracy among successful reasoning cases: `5/147 = 0.0340`
- Theorem selection labeled trace steps: `374`
- Theorem selection top-1: `41/374 = 0.1096`
- Theorem selection top-3: `101/374 = 0.2701`
- Theorem selection top-5: `138/374 = 0.3690`
- Failure reason distribution:
  - `answer_mismatch`: `142`
  - `max_steps`: `42`
  - `no_model`: `11`
- Reasoning failure reason distribution:
  - `max_steps`: `42`
  - `no_model`: `11`

The legacy batch report written to `outputs/evaluation/baseline_200.json` matches the same core end-to-end baseline:

- Reasoning success: `147/200 = 73.5%`
- Final answer correct: `5/200 = 2.5%`
- Answer accuracy among successful reasoning cases: `3.4%`

Existing external selector report included in the protocol summary:

- Total predictions: `18`
- Top-1: `9/18 = 0.5000`
- Top-3: `15/18 = 0.8333`
- Top-5: `16/18 = 0.8889`

## Known Risks

- The per-run theorem-selection metric compares each run trace step to the sample `models` sequence from `data/train_with_models_v2.json`. If the current reasoning path diverges from the annotated process, step-index alignment is only an approximate diagnostic. The metric is useful for protocol smoke testing and error slicing, but should not be sold as the final selector benchmark without a stricter state-transition label join.
- Samples with empty `models` sequences have no theorem-selection labels and are excluded from top-k denominators.
- The existing external selector report has only 18 predictions, so it is included as prior artifact context, not as a publication-grade selector score.
- `answer_mismatch` is intentionally counted as a final-outcome failure reason even when reasoning succeeded. Use `reasoning_failure_reason_distribution` when analyzing process failures only.
- No behavior changes were made to the reasoning loop, selector, theorem models, or answer comparator.

## Integration Notes

- Search and solver workers can read `outputs/evaluation/protocol_200_smoke/summary.json` or `summary.csv` for consistent group-level metrics.
- For future ablations, keep the sample-level schema stable and add strategy metadata under `run`.
- If the main thread wants publication-grade theorem-selection accuracy, add an integration step that evaluates the selector directly on `data/train_state_model_v2.json` transitions with stable sample/transition IDs.
