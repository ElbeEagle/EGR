# Round2 Entropy Correctness Join

## Join Key Reliability

- Join key used: `entropy.problem_id == eval.sample_id`.
- Eval coverage: 33/200 (0.1650).
- Joined trajectory rows: 78.
- Entropy unique problem IDs: 1000.
- Duplicate eval sample IDs: 0.
- Train facts/query exact matches for joined IDs: 33/33.

Interpretation: the ID join is stable for matched samples, but coverage is low. Use this as a diagnostic slice, not as paper-level evidence that entropy predicts final correctness.

## Eval Outcome Coverage

- Full eval: final-answer accuracy 21/200 (0.1050); reasoning success 130/200 (0.6500).
- Joined subset: final-answer accuracy 3/33 (0.0909); reasoning success 25/33 (0.7576).
- Joined failure buckets: `{"answer_mismatch": 22, "correct": 3, "max_steps": 6, "no_model": 2}`.

## Model-Path Entropy Slice

- Model-path trajectories: 33 over 33 eval samples.
- Model-path executable rate: 12/33 (0.3636).
- Mean heuristic entropy delta: 0.26201515.
- Mean learned entropy delta: 0.58844714.

Selected model-path correlations are below. Positive labels are `true` for the named outcome.

| Outcome | Metric | n | Positive | Pearson | Spearman | Positive mean | Negative mean |
|---|---:|---:|---:|---:|---:|---:|---:|
| final_answer_correct | initial_heuristic_entropy | 33 | 3 | 0.12276071 | 0.25374408 | 0.80166667 | 0.78343333 |
| final_answer_correct | heuristic_entropy_delta | 33 | 3 | -2.892e-05 | 0.02217003 | 0.262 | 0.26201667 |
| final_answer_correct | initial_learned_entropy | 33 | 3 | -0.17063904 | -0.18822462 | 0.8345945 | 0.86899244 |
| final_answer_correct | learned_entropy_delta | 33 | 3 | -0.18734002 | -0.22149628 | 0.4510522 | 0.60218664 |
| reasoning_success | initial_heuristic_entropy | 33 | 25 | -0.17102384 | 0.10969521 | 0.78096 | 0.798 |
| reasoning_success | heuristic_entropy_delta | 33 | 25 | 0.24460673 | 0.31603232 | 0.28494 | 0.190375 |
| reasoning_success | initial_learned_entropy | 33 | 25 | -0.01810754 | -0.06684613 | 0.86527175 | 0.86772036 |
| reasoning_success | learned_entropy_delta | 33 | 25 | -0.013765 | -0.05200448 | 0.58664125 | 0.59409055 |

## Claim Boundary

Can claim now:
- A stable ID join is available for matched samples using `problem_id == sample_id`; train-data checks show these IDs map to the same facts/query for the joined subset.
- The current entropy slice covers 0.165 of the 200-sample end-to-end eval, so the join is useful as a diagnostic slice.
- Heuristic and learned entropy can be reported side by side against reasoning_success, final_answer_correct, and failure buckets on this joined slice.

Cannot claim now:
- Do not claim that remaining-step entropy predicts final answer correctness; the joined subset is small and final-correct positives are sparse.
- Do not claim end-to-end solver improvement from entropy; the estimator was not integrated into the reasoning engine.
- Do not interpret random/correct/model entropy trajectories as the actual solver trajectory unless the eval-applied sequence is separately reconstructed and validated.
