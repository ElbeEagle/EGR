# Round2 Entropy Correctness Join Handoff

## Task

Worker: `entropy-correctness-join`

Scope:
- Join existing entropy trajectories with end-to-end eval correctness where stable keys allow.
- Analyze heuristic/learned entropy against `reasoning_success`, `final_answer_correct`, and failure buckets.
- Keep entropy evidence separate from final-answer correctness claims.

No reasoning-engine integration was performed.

## Files Changed

Added:
- `scripts/entropy/join_entropy_correctness.py`
- `outputs/entropy/round2_correctness_join/correctness_join_summary.json`
- `outputs/entropy/round2_correctness_join/trajectory_join_rows.csv`
- `outputs/entropy/round2_correctness_join/sample_model_rows.csv`
- `outputs/entropy/round2_correctness_join/path_type_summary.csv`
- `outputs/entropy/round2_correctness_join/outcome_metric_correlations.csv`
- `outputs/entropy/round2_correctness_join/failure_reason_summary.csv`
- `outputs/entropy/round2_correctness_join/report.md`
- `dev_logs/aaai2027/round2_entropy_correctness_join_handoff.md`

Forbidden files were not edited.

## Join-Key Reliability

Join key used:
- `outputs/entropy/entropy_dataset.jsonl`: `problem_id`
- `outputs/evaluation/main_integration_200/samples.jsonl`: `sample_id`
- Conservative join: `problem_id == sample_id`

Join key rejected:
- `sample_index`, because it is local to the filtered entropy slice of non-empty model-sequence samples and is not a stable global eval key.

Reliability checks:
- Eval samples: `200`, unique sample IDs: `200`, duplicate eval IDs: `0`.
- Entropy entries: `11,411`, trajectories: `2,325`, unique problem IDs: `1,000`.
- Joined eval samples: `33/200 = 16.50%`.
- Joined entropy entries: `385`.
- Joined trajectory rows: `78`.
- Train-data facts/query validation: `200/200` eval IDs present and exact-matched in `data/train_with_models_v2.json`; joined subset exact-matched `33/33`.

Interpretation:
- The ID key is stable for matched samples.
- Coverage is low because the current entropy dataset is a 1,000-sample non-empty-model slice, while the 200-sample eval includes many IDs outside that slice and samples with empty annotated model sequences.
- All correctness correlations below are diagnostic and underpowered.

## Main Numbers

Full 200-sample eval:
- Final-answer accuracy: `21/200 = 10.50%`.
- Reasoning success: `130/200 = 65.00%`.
- Failure buckets: `answer_mismatch=109`, `correct=21`, `max_steps=59`, `no_model=11`.

Joined 33-sample subset:
- Final-answer accuracy: `3/33 = 9.09%`.
- Reasoning success: `25/33 = 75.76%`.
- Failure buckets: `answer_mismatch=22`, `correct=3`, `max_steps=6`, `no_model=2`.

Model-path joined entropy trajectories:
- Trajectories: `33` over `33` eval samples.
- Path executable: `12/33 = 36.36%`.
- Mean heuristic entropy delta: `0.26201515`.
- Mean learned entropy delta: `0.58844714`.

Correct-path joined trajectories:
- Trajectories: `12`; all are executable by construction.
- Final-answer-correct samples among these trajectories: `2/12`.
- Mean heuristic entropy delta: `0.35570833`.
- Mean learned entropy delta: `0.58468298`.

Random-path joined trajectories:
- Trajectories: `33`.
- Path executable: `0/33`.
- Mean heuristic entropy delta: `0.08798485`.
- Mean learned entropy delta: `0.53564069`.

## Entropy vs Correctness / Reasoning Success

Model-path selected correlations:

| Outcome | Metric | n | positives | Pearson | Spearman | positive mean | negative mean |
|---|---:|---:|---:|---:|---:|---:|---:|
| `final_answer_correct` | initial heuristic entropy | 33 | 3 | `0.12276071` | `0.25374408` | `0.80166667` | `0.78343333` |
| `final_answer_correct` | heuristic entropy delta | 33 | 3 | `-0.00002892` | `0.02217003` | `0.26200000` | `0.26201667` |
| `final_answer_correct` | initial learned entropy | 33 | 3 | `-0.17063904` | `-0.18822462` | `0.83459450` | `0.86899244` |
| `final_answer_correct` | learned entropy delta | 33 | 3 | `-0.18734002` | `-0.22149628` | `0.45105220` | `0.60218664` |
| `reasoning_success` | initial heuristic entropy | 33 | 25 | `-0.17102384` | `0.10969521` | `0.78096000` | `0.79800000` |
| `reasoning_success` | heuristic entropy delta | 33 | 25 | `0.24460673` | `0.31603232` | `0.28494000` | `0.19037500` |
| `reasoning_success` | initial learned entropy | 33 | 25 | `-0.01810754` | `-0.06684613` | `0.86527175` | `0.86772036` |
| `reasoning_success` | learned entropy delta | 33 | 25 | `-0.01376500` | `-0.05200448` | `0.58664125` | `0.59409055` |

Reading:
- No stable final-answer-correctness signal should be claimed. There are only `3` final-correct positives in the joined model-path subset.
- Heuristic entropy delta has a small positive association with `reasoning_success` in this slice, but this is not final-answer correctness and should not be overinterpreted.
- Learned entropy remains primarily validated against normalized remaining-step supervision, not answer correctness.

## Failure Buckets

Model-path means by failure bucket:

| Failure bucket | n | reasoning success | executable rate | heuristic delta mean | learned delta mean |
|---|---:|---:|---:|---:|---:|
| `answer_mismatch` | 22 | 22 | `0.36363636` | `0.28806818` | `0.60513067` |
| `correct` | 3 | 3 | `0.66666667` | `0.26200000` | `0.45105220` |
| `max_steps` | 6 | 0 | `0.33333333` | `0.20366667` | `0.62361592` |
| `no_model` | 2 | 0 | `0.00000000` | `0.15050000` | `0.50551445` |

Reading:
- Failure-bucket means are useful for debugging but not claim-grade because buckets are small, especially `correct` and `no_model`.
- `answer_mismatch` can have strong entropy reduction and reasoning success, reinforcing that process/trajectory progress is not equivalent to final answer correctness.

## Paper-Claim Boundary

Can claim now:
- A stable join exists for matched samples via `problem_id == sample_id`.
- Current entropy outputs can be joined to a diagnostic subset of end-to-end eval results.
- The joined subset supports reporting heuristic/learned entropy statistics side by side with `reasoning_success`, `final_answer_correct`, and failure buckets.
- The evidence reinforces the need to separate remaining-step/process supervision from final-answer correctness.

Cannot claim now:
- Do not claim learned `H(S)` predicts final answer correctness.
- Do not claim entropy improves end-to-end solver accuracy.
- Do not treat `reasoning_success` or entropy reduction as answer-correctness evidence.
- Do not treat `model`/`correct`/`random` entropy trajectories as the actual eval solver trajectory. The eval-applied sequence would need separate reconstruction and validation.

## Commands Run

```bash
git status --short
sed -n '1,220p' dev_logs/aaai2027/entropy_estimator_handoff.md
rg --files outputs/entropy src/entropy scripts/entropy dev_logs/aaai2027 outputs/evaluation/main_integration_200
sed -n '1,220p' outputs/evaluation/main_integration_200/summary.json
sed -n '1,5p' outputs/entropy/entropy_dataset.jsonl
sed -n '1,3p' outputs/evaluation/main_integration_200/samples.jsonl
sed -n '1,260p' src/entropy/schema.py
sed -n '1,320p' src/entropy/dataset.py
sed -n '1,260p' src/entropy/reporting.py
jq '.[0] | keys' data/train_with_models_v2.json
jq '.[0:3] | map({id, models, fact_expressions, query_expressions, answer})' data/train_with_models_v2.json
jq -s '[.[].sample_id] | {count:length, unique:(unique|length), min:min, max:max, first10:.[0:10]}' outputs/evaluation/main_integration_200/samples.jsonl
jq -s '[.[].problem_id] | {count:length, unique:(unique|length), min:min, max:max, first10:.[0:10]}' outputs/entropy/entropy_dataset.jsonl
python3 scripts/entropy/join_entropy_correctness.py
jq '{reliability:.join_key.reliability, joined:.joined_eval_subset, eval:.eval_overall}' outputs/entropy/round2_correctness_join/correctness_join_summary.json
cat outputs/entropy/round2_correctness_join/path_type_summary.csv
python3 -m py_compile scripts/entropy/join_entropy_correctness.py
git status --short -- scripts/entropy/join_entropy_correctness.py outputs/entropy/round2_correctness_join dev_logs/aaai2027/round2_entropy_correctness_join_handoff.md
```

## Validation

Passed:
- `python3 scripts/entropy/join_entropy_correctness.py`
- `python3 -m py_compile scripts/entropy/join_entropy_correctness.py`
- Generated summary/report inspected for expected `33/200` join coverage and explicit claim boundary.

## Integration Notes

- This is analysis-only. Do not wire learned entropy into `src/reasoning/reasoning_engine.py` from this handoff.
- If the main thread wants claim-grade entropy-correctness evidence, next step is to build/evaluate entropy trajectories for the actual eval-applied solver traces or regenerate the entropy dataset over the full eval sample set, then repeat this join with higher coverage.
