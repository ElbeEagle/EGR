# AAAI2027 Claims and Evidence Matrix

This document maps paper claims to current evidence, missing experiments, and paper-safe wording. It should be treated as the claim boundary file for the AAAI2027 draft.

## Evidence Boundary

Current repo outputs are preliminary and sometimes inconsistent. They can motivate the paper plan, but final claims require a unified evaluation run.

Rules:

1. Do not claim state-of-the-art.
2. Do not report final accuracy without saying it is preliminary unless it comes from the final unified protocol.
3. Do not merge theorem selection, reasoning success, and final answer accuracy.
4. Mark missing cells as `TODO: fill after unified evaluation`.
5. LLM augmentation is a planned experiment until actual LLM baseline and LLM+EGR results exist.

## Claim Matrix

| ID | Claim | Paper-safe wording now | Current evidence | Missing evidence | Status |
| --- | --- | --- | --- | --- | --- |
| C1 | EGR formalizes conic-section solving as a theorem-action sequence. | "We formulate conic-section problem solving as a sequential decision process over executable theorem actions." | `SymbolicState`, `AbstractState`, `TheoremLibrary`, `ReasoningEngine`; 56/80 registered models by runtime audit. | Final audit of theorem coverage and unsupported IDs. | Supported as method claim. |
| C2 | Symbolic execution provides controllability and interpretability. | "Each executed step is guarded by `can_apply` and updates a symbolic state, allowing the reasoning trace to be inspected." | `can_apply/apply`, `applied_models`, reasoning trace fields. | Case studies showing correct and failed traces. | Supported, needs examples. |
| C3 | Neural policy provides theorem selection probabilities. | "A neural policy estimates `P(Y|X)` over theorem actions from a fixed-dimensional abstract state." | `MaxEntropyClassifier` 28 -> 64 -> 128 -> 64 -> 80; `predict()` returns probabilities and entropy. | Final theorem-step Top-1/3/5 on a frozen split. | Supported as mechanism; performance TODO. |
| C4 | `H(S)` is a useful solving-progress signal. | "In current repo logs, learned state entropy correlates with normalized remaining steps." | Learned entropy validation Pearson 0.837/Spearman 0.849; correlation summary Pearson 0.833/Spearman 0.859. | Validate under final split and relate to success/failure. | Promising, not final. |
| C5 | Information gain improves reasoning search. | "A preliminary 50-sample ablation suggests full EGR reduces average steps relative to neural-only variants while preserving final answer accuracy." | `main_search_ablation_50`: neural_rule avg steps 4.62, full_egr avg steps 4.30; both final answer 26%. | Larger ablation with confidence intervals and learned entropy variant. | Preliminary. |
| C6 | EGR improves final answer accuracy over baselines. | `TODO: fill after unified evaluation`. | Preliminary `main_integration_200`: 21/200 = 10.5%; ablation 50: full_egr 26%. | Frozen train/dev/test protocol, answer normalization, baseline comparison. | Not established. |
| C7 | EGR helps LLMs on hard math reasoning. | "We evaluate whether EGR traces and theorem candidates can serve as structured assistance for LLMs." | No current LLM baseline found. | Direct LLM baseline, LLM+theorem candidates, LLM+EGR trace/verifier. | Planned only. |
| C8 | The system is scalable to the full Conic10K theorem universe. | "The framework is designed around an 80-ID theorem-action universe, with 56 currently registered models in this checkout." | Current `TheoremLibrary()` runtime count 56/80. | Implement/audit remaining models or write as limitation. | Partially supported. |

## Current Evidence Inventory

### Architecture Evidence

| Evidence | What it supports | Citation in paper |
| --- | --- | --- |
| `src/state/symbolic_state.py` | Fine-grained symbolic execution state | Method: Dual-layer state |
| `src/state/abstract_state.py` | 28-dimensional neural input state | Method: Abstract state |
| `src/theorems/theorem_library.py` | Registered theorem actions and executable model interface | Method: Theorem library |
| `src/selector/model_selector.py` | `P(Y|X)` and `H(Y|X)` implementation | Method: Policy and prediction entropy |
| `src/reasoning/model_selector.py` | `neural_topk` and `three_layer_entropy` scoring | Method: Integrated scoring |
| `src/reasoning/entropy_estimator.py` | Heuristic/learned entropy and InfoGain | Method: State entropy |
| `src/reasoning/reasoning_engine.py` | End-to-end reasoning loop and trace | Method: Algorithm |

### Metric Evidence

| Output file | Key numbers | How to use |
| --- | --- | --- |
| `outputs/selector/evaluation_results.json` | 18 predictions, Top-1 50.0%, Top-3 83.3%, Top-5 88.9% | Mention only as small historical selector check, not final. |
| `outputs/selector/training_metrics.json` | Best val Top-1 40.7%, Top-3 66.7%, Top-5 77.8% | Historical selector training log. |
| `outputs/evaluation/main_integration_200/summary.json` | Reasoning success 65.0%, final answer 10.5%, integrated theorem Top-1 10.96% | Main preliminary integration result; needs diagnosis. |
| `outputs/evaluation/protocol_200_smoke/summary.json` | Reasoning success 73.5%, final answer 2.5% | Smoke result; demonstrates protocol variance. |
| `outputs/experiments/main_search_ablation_50/ablation_summary.json` | full_egr final 26%, avg steps 4.30; neural_rule final 26%, avg steps 4.62; rule_only final 22% | Preliminary ablation table candidate. |
| `outputs/entropy/training_metrics.json` | Learned entropy val Pearson 0.837, Spearman 0.849, MAE 0.154 | Strong entropy module evidence. |
| `outputs/entropy/correlation_summary.json` | Learned entropy Pearson 0.833, Spearman 0.859 over 11,411 entries | Strong entropy correlation evidence. |
| `outputs/entropy/trajectory_report.json` | Correct path learned entropy delta 0.565, monotonicity 1.0 over 325 trajectories | Entropy trajectory figure/table candidate. |

## Claim-by-Experiment Requirements

| Claim | Required experiment | Minimum acceptance for paper | Notes |
| --- | --- | --- | --- |
| C1, C2 | Theorem-library audit and executable trace examples | Clear count of implemented models and examples of valid `can_apply/apply` transitions | This is a method/engineering claim, not accuracy. |
| C3 | Theorem selection on frozen labeled steps | Top-1/3/5 with sample count, split, and unsupported-ID handling | Must explain discrepancy between small selector check and integrated evaluator. |
| C4 | Entropy regression and trajectory analysis | Correlation with remaining steps, monotonicity, success/failure comparison | Report heuristic and learned separately. |
| C5 | Search ablation | rule-only vs neural-only vs neural+rule vs full EGR, same split and same answer comparator | Include average steps and failure distribution. |
| C6 | Main Conic10K evaluation | Final answer accuracy, reasoning success, parse/extraction failure, by query type | Do not use process success as answer accuracy. |
| C7 | LLM augmentation | direct LLM vs LLM+EGR candidates vs LLM+EGR trace/verifier | Keep prompts fixed; report invalid/parse rate. |

## Paper-Safe Current Statements

Allowed now:

- "The current checkout implements 56 of the 80 theorem-action IDs in the Conic10K-derived action universe."
- "The abstract neural state is a 28-dimensional vector derived from symbolic state features."
- "The learned entropy estimator correlates with normalized remaining steps in current repo logs, with Pearson correlation above 0.83 in the available entropy reports."
- "Preliminary ablations suggest entropy-guided scoring can reduce the number of reasoning steps without changing 50-sample final answer accuracy, but larger unified evaluation is required."

Not allowed now:

- "EGR achieves state-of-the-art accuracy."
- "EGR solves Conic10K at 60-80% final answer accuracy."
- "The theorem selector reaches 88.9% Top-5 in the final evaluation."
- "EGR improves LLM high-difficulty reasoning."
- "The theorem library fully covers all 80 models."

## Table Placeholders for the Paper

### Table: Main Result

| Method | Theorem Top-1 | Theorem Top-5 | Reasoning success | Final answer accuracy |
| --- | ---: | ---: | ---: | ---: |
| Rule-only symbolic | TODO: fill after unified evaluation | TODO | TODO | TODO |
| Neural policy only | TODO | TODO | TODO | TODO |
| Neural + rule filtering | TODO | TODO | TODO | TODO |
| Full EGR | TODO | TODO | TODO | TODO |
| Direct LLM | TODO | TODO | TODO | TODO |
| LLM + EGR | TODO | TODO | TODO | TODO |

### Table: Current Preliminary Evidence

| Evidence | Value | Caveat |
| --- | ---: | --- |
| `main_integration_200` final answer | 10.5% | Preliminary, protocol needs fixing. |
| `main_integration_200` reasoning success | 65.0% | Process metric, not answer accuracy. |
| `main_search_ablation_50` full EGR final answer | 26.0% | Small sample. |
| Learned entropy validation Pearson | 0.837 | Against normalized remaining steps, not answer correctness. |
