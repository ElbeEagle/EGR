# AAAI2027 EGR Experiment Plan

This plan defines the experiments needed before the AAAI2027 paper can make performance claims. The key principle is metric separation: theorem selection, reasoning process success, final answer accuracy, entropy trajectory quality, and LLM augmentation must be reported independently.

## 1. Evaluation Protocol

### Required Protocol Decisions

| Decision | Default choice | Rationale |
| --- | --- | --- |
| Dataset | Conic10K-derived local data from `data/train_with_models_v2.json` plus any official dev/test split if available | Avoid mixing training logs and evaluation logs. |
| Split | TODO: define frozen train/dev/test or use official split | Current reports use sampled subsets and are not enough for final claims. |
| Theorem universe | 80 Conic10K model IDs, with implemented subset explicitly reported | Avoid hiding unsupported theorem IDs. |
| Implemented models | Runtime audit of `TheoremLibrary()` at evaluation time | Current count is 56/80. |
| Answer comparator | Use the repo answer comparator and document normalization rules | Final answer accuracy depends on expression equivalence. |
| Max steps | Keep fixed per experiment, e.g. 15 or 20 | Required for fair comparison. |
| Random seed | Fixed and reported | Required for ablation reproducibility. |

### Standard Output Schema

Every run should save:

```json
{
  "run_id": "TODO",
  "timestamp": "TODO",
  "dataset_path": "TODO",
  "split": "TODO",
  "sample_count": "TODO",
  "implemented_theorem_count": "TODO",
  "strategy": "rule_only | neural_only | neural_rule | full_egr | llm | llm_egr",
  "max_steps": "TODO",
  "top_k": "TODO",
  "lambda_weights": "TODO",
  "theorem_selection": {
    "labeled_steps": "TODO",
    "top1": "TODO",
    "top3": "TODO",
    "top5": "TODO"
  },
  "reasoning_process": {
    "success_count": "TODO",
    "success_rate": "TODO",
    "avg_steps": "TODO",
    "failure_reasons": "TODO"
  },
  "final_answer": {
    "correct_count": "TODO",
    "accuracy": "TODO",
    "invalid_or_unparsed_rate": "TODO"
  },
  "entropy": {
    "pearson_remaining_steps": "TODO",
    "spearman_remaining_steps": "TODO",
    "monotonicity_rate": "TODO",
    "avg_info_gain": "TODO"
  }
}
```

## 2. Main Experiments

### E1. Theorem Selection Accuracy

Question:

> Does `P(Y|X)` select gold theorem actions from abstract states?

Metrics:

- Top-1 accuracy.
- Top-3 accuracy.
- Top-5 accuracy.
- Coverage by theorem ID.
- Accuracy on implemented vs unsupported theorem IDs.

Current evidence:

- Small selector report: 18 steps, Top-1 50.0%, Top-3 83.3%, Top-5 88.9%.
- Integrated main 200: 374 labeled steps, Top-1 10.96%, Top-3 27.01%, Top-5 36.90%.

Required action:

- Re-run theorem selection under one frozen protocol.
- Diagnose why integrated theorem hits are much lower than the small selector report.

Paper table:

| Split | Labeled steps | Top-1 | Top-3 | Top-5 | Unsupported gold ID rate |
| --- | ---: | ---: | ---: | ---: | ---: |
| Dev | TODO: fill after unified evaluation | TODO | TODO | TODO | TODO |
| Test | TODO: fill after unified evaluation | TODO | TODO | TODO | TODO |

### E2. Reasoning Process Success

Question:

> Can the system keep making executable theorem transitions and reach a terminal state?

Metrics:

- Reasoning success rate.
- `max_steps` failure rate.
- `no_model` failure rate.
- Average steps.
- Average steps among successful processes.

Important boundary:

Reasoning success is not final answer accuracy. It only measures process completion or valid extraction under the evaluator.

Paper table:

| Strategy | Process success | Avg steps | Max-step failures | No-model failures |
| --- | ---: | ---: | ---: | ---: |
| rule_only | TODO | TODO | TODO | TODO |
| neural_only | TODO | TODO | TODO | TODO |
| neural_rule | TODO | TODO | TODO | TODO |
| full_egr | TODO | TODO | TODO | TODO |

### E3. Final Answer Accuracy

Question:

> Does EGR produce the correct final answer?

Metrics:

- Overall final answer accuracy.
- Accuracy by query type: equation, value, eccentricity, coordinate, distance, length, range, area.
- Accuracy by curve type: ellipse, hyperbola, parabola, circle, other.
- Invalid answer or extraction failure rate.
- Answer mismatch categories.

Current evidence:

- `main_integration_200`: 21/200 = 10.5%.
- `protocol_200_smoke`: 5/200 = 2.5%.
- `main_search_ablation_50/full_egr`: 13/50 = 26.0%.

Required action:

- Choose one official evaluation protocol and one answer comparator.
- Report confidence intervals or at least sample counts.
- Do not present the current 50-sample 26% as final.

Paper table:

| Method | Overall | Equation | Value | Eccentricity | Coordinate | Other |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| rule_only | TODO | TODO | TODO | TODO | TODO | TODO |
| neural_rule | TODO | TODO | TODO | TODO | TODO | TODO |
| full_egr | TODO | TODO | TODO | TODO | TODO | TODO |
| direct LLM | TODO | TODO | TODO | TODO | TODO | TODO |
| LLM+EGR | TODO | TODO | TODO | TODO | TODO | TODO |

### E4. Search and Entropy Ablation

Question:

> Which part of the EGR scoring function matters?

Strategies:

1. `rule_only`: deterministic or rule-ranked symbolic execution.
2. `neural_only`: neural theorem sequence without symbolic filtering where applicable.
3. `neural_rule`: `P(Y|X)` plus `can_apply`.
4. `full_egr`: `P(Y|X) + InfoGain - H(Y|X)`.
5. `full_egr_heuristic_entropy`: if needed, separate heuristic `H(S)`.
6. `full_egr_learned_entropy`: learned-linear `H(S)`.
7. Lambda sweeps: `(0.8,0.1,0.1)`, `(0.6,0.3,0.1)`, `(0.4,0.5,0.1)`, `(0.6,0.2,0.2)`.

Current evidence:

`outputs/experiments/main_search_ablation_50/ablation_summary.json`:

| Strategy | Reasoning success | Final answer accuracy | Avg steps |
| --- | ---: | ---: | ---: |
| rule_only | 60.0% | 22.0% | 3.72 |
| neural_only | 86.0% | 26.0% | 6.12 |
| neural_rule | 86.0% | 26.0% | 4.62 |
| full_egr | 86.0% | 26.0% | 4.30 |

Paper-safe interpretation:

This preliminary run suggests EGR-style scoring may improve process efficiency, but it does not yet show a final-answer accuracy gain over neural_rule.

### E5. Entropy Trajectory Quality

Question:

> Does `H(S)` behave like a progress signal?

Metrics:

- Pearson/Spearman vs normalized remaining steps.
- MAE/RMSE against normalized remaining-step target.
- Initial-to-final entropy delta.
- Monotonicity rate.
- Difference between correct/model/random paths.
- Correlation with final answer correctness, if available.

Current evidence:

- Learned-linear validation: Pearson 0.837, Spearman 0.849, MAE 0.154.
- Correlation summary over 11,411 entries: Pearson 0.833, Spearman 0.859.
- Correct paths: learned entropy delta 0.565, monotonicity 1.0 over 325 trajectories.

Paper figures:

1. Entropy vs normalized remaining steps scatter or calibration curve.
2. Average entropy trajectory for correct/model/random paths.
3. Case-study entropy trace aligned with theorem actions.

### E6. Error Analysis

Question:

> Where does EGR fail?

Required categories:

- Unsupported theorem ID.
- `can_apply` false negative.
- Wrong theorem selection.
- Apply executed but did not add useful information.
- Loop or repeated model.
- Max steps.
- Answer extraction failure.
- Answer normalization/equivalence failure.
- True mathematical gap.

Paper table:

| Error category | Count | Ratio | Example ID | Fix direction |
| --- | ---: | ---: | --- | --- |
| Unsupported theorem | TODO | TODO | TODO | TODO |
| Selection error | TODO | TODO | TODO | TODO |
| Symbolic execution gap | TODO | TODO | TODO | TODO |
| Answer extraction | TODO | TODO | TODO | TODO |
| Max steps loop | TODO | TODO | TODO | TODO |

## 3. LLM Baseline and LLM+EGR

### Motivation

The paper's second-level contribution is not that EGR replaces LLMs, but that EGR provides a controllable, structured, and verifiable reasoning aid for difficult math reasoning.

### Conditions

| Condition | Input to model | Output expected |
| --- | --- | --- |
| Direct LLM | Original problem text/facts/query | Final answer and optional concise derivation |
| LLM + theorem candidates | Original problem plus top-k EGR theorem candidates per step | Final answer and selected theorem sequence |
| LLM + EGR trace | Original problem plus EGR-produced theorem trace/state changes | Final answer, correction, or verification |
| LLM + EGR verifier | LLM proposes solution, EGR checks executable theorem steps where possible | Verified answer or failure reason |

### Metrics

- Final answer accuracy.
- Invalid output rate.
- Step executability rate.
- Theorem-sequence agreement with gold, if available.
- Correction rate: direct LLM wrong but LLM+EGR correct.
- Harm rate: direct LLM correct but LLM+EGR wrong.

### Prompt Boundary

Prompts should not leak gold theorem sequences or gold answers. EGR candidates/traces are allowed only when they are produced by the system under the same evaluation protocol.

### Paper Table

| Method | Final answer | Invalid rate | Step executability | Correction rate | Harm rate |
| --- | ---: | ---: | ---: | ---: | ---: |
| Direct LLM | TODO | TODO | TODO | TODO | TODO |
| LLM + theorem candidates | TODO | TODO | TODO | TODO | TODO |
| LLM + EGR trace | TODO | TODO | TODO | TODO | TODO |
| LLM + EGR verifier | TODO | TODO | TODO | TODO | TODO |

## 4. Minimal Reproducibility Checklist

Before writing final results:

- [ ] Freeze evaluation split and write split manifest.
- [ ] Runtime-audit `TheoremLibrary()` and save implemented model IDs.
- [ ] Save all command lines, seeds, model checkpoint paths, and lambda weights.
- [ ] Save both JSON and CSV summaries.
- [ ] Save per-sample JSONL for error analysis.
- [ ] Save entropy trajectory artifacts.
- [ ] Save LLM prompts and raw outputs if LLM experiments are run.
- [ ] Mark every table with sample count and whether it is preliminary or final.

## 5. Candidate Commands

These are candidate commands based on current repo structure and should be verified before final runs:

```bash
python scripts/reasoning/batch_test.py
python scripts/entropy/run_entropy_pipeline.py
python scripts/experiments/run_search_ablation.py --help
```

If a command is missing or has different arguments, inspect the script first and update this plan.

