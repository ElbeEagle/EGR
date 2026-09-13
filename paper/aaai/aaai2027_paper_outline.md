# AAAI2027 EGR Paper Outline

This document is a paper-writing scaffold for the AAAI2027 EGR submission. It is intentionally evidence-bounded: current numbers are treated as preliminary repo logs, and any missing or unstable result is marked as `TODO: fill after unified evaluation`.

## 1. Read-First Audit

### Confirmed Current Repo Facts

| Item | Current fact | Source |
| --- | --- | --- |
| Project | EGR, Entropy-Guided Reasoning for Conic10K conic-section math reasoning | `PROJECT_STATUS.md`, `doc/project_workflow.md`, code |
| Data scope | `data/train_with_models_v2.json` has 7,757 samples, 5,359 samples with non-empty model sequences, and 20,226 annotated model steps | local JSON audit |
| State training data | `data/train_state_model_v2.json` records 5,359 samples and 12,460 executable/generated transitions | local JSON audit |
| Symbolic state | Stores entities, equations, parameters, geometric relations, coordinates, constraints, and applied model history | `src/state/symbolic_state.py` |
| Abstract state | Converts the symbolic state into a 28-dimensional vector: 5 curve-type one-hot, 10 query-type one-hot, 11 information features, completeness, depth | `src/state/abstract_state.py` |
| Theorem library | `TheoremLibrary()` currently registers 56/80 models | local Python audit of `src/theorems/theorem_library.py` |
| Neural selector | `MaxEntropyClassifier`: 28 -> 64 -> 128 -> 64 -> 80, outputting `P(Y|X)` and prediction entropy `H(Y|X)` | `src/selector/model_selector.py` |
| Reasoning selector | Supports `neural_top1`, `neural_topk`, and `three_layer_entropy` strategies | `src/reasoning/model_selector.py` |
| State entropy | `EntropyEstimator` supports a heuristic estimator and a loaded learned-linear estimator; InfoGain is `H(S_t)-H(S_{t+1})` | `src/reasoning/entropy_estimator.py` |
| Reasoning engine | Builds states, selects theorem actions, applies symbolic transformations, updates state, extracts answers, and records traces | `src/reasoning/reasoning_engine.py` |

### Preliminary Metrics Found in the Repo

These are useful for planning, not final paper claims.

| Metric family | Current value | Source | Paper status |
| --- | ---: | --- | --- |
| External selector report, small sample | Top-1 9/18 = 50.0%, Top-3 15/18 = 83.3%, Top-5 16/18 = 88.9% | `outputs/selector/evaluation_results.json` | Historical/small-sample only |
| Old selector training report | Best val Top-1 40.7%, Top-3 66.7%, Top-5 77.8% | `outputs/selector/training_metrics.json` | Historical model log |
| Main integration 200 | Reasoning success 130/200 = 65.0%, final answer accuracy 21/200 = 10.5% | `outputs/evaluation/main_integration_200/summary.json` | Current preliminary integration result |
| Main integration 200 theorem hits | 374 labeled steps, Top-1 10.96%, Top-3 27.01%, Top-5 36.90% | `outputs/evaluation/main_integration_200/summary.json` | Needs diagnosis before paper use |
| Protocol 200 smoke | Reasoning success 147/200 = 73.5%, final answer accuracy 5/200 = 2.5% | `outputs/evaluation/protocol_200_smoke/summary.json` | Smoke result, not final |
| Batch reports | `batch_test_report.json` and `batch_test_report_v2.json` are identical; both report 5/200 = 2.5% final answer accuracy | `outputs/reasoning/` | Historical/duplicated output |
| Search ablation 50 | rule-only final answer 22%, neural-only 26%, neural+rule 26%, full EGR 26%; full EGR reduces average steps vs neural+rule | `outputs/experiments/main_search_ablation_50/ablation_summary.json` | Preliminary 50-sample result |
| Entropy estimator | Learned entropy validation Pearson 0.837, Spearman 0.849 vs normalized remaining steps | `outputs/entropy/training_metrics.json` | Promising entropy module evidence |
| Entropy correlation | Learned entropy Pearson 0.833 and Spearman 0.859 vs normalized remaining steps over 11,411 entries | `outputs/entropy/correlation_summary.json` | Strong but needs paper protocol |
| Entropy trajectory | Correct paths show learned entropy delta 0.565 with monotonicity 1.0 over 325 trajectories | `outputs/entropy/trajectory_report.json` | Good analysis candidate |

### Inconsistencies and Risks

1. Older documents still say the theorem library has 40/80 or 52/80 models; current runtime audit shows 56/80.
2. Older documents sometimes describe `AbstractState` as 15-dimensional, but current `to_vector()` returns 28 dimensions.
3. Selector metrics differ sharply by evaluation context: the small external selector report is high, while integrated theorem-step hits in `main_integration_200` are low. The paper must not present one as the other.
4. Reasoning success is not final answer accuracy. Some reports mark a reasoning process as successful even when the extracted answer mismatches gold.
5. The current end-to-end answer accuracy is not yet publication-ready. All strong performance claims require unified evaluation and error analysis.
6. Related work citations are not populated. The paper draft should use topic placeholders only until references are verified.

## 2. Core Story Line

The paper should not be framed as "we beat LLMs" or "we reach SOTA" at this stage. The safer and stronger story is:

> EGR treats hard conic-section problem solving as an executable theorem-action process. A symbolic layer guarantees that every step is a traceable mathematical operation, while neural components estimate theorem-selection probabilities, state uncertainty, and information gain. This gives a controllable neural-symbolic reasoning framework that can solve parts of Conic10K directly and can also expose structured intermediate reasoning for LLM-based high-difficulty math assistance.

The story has two levels:

1. Concrete algorithm contribution: a neural-symbolic theorem-action solver for high-difficulty Conic10K problems.
2. Paradigm contribution: an interpretable, controllable, and verifiable reasoning scaffold that can complement LLMs on hard math reasoning rather than replacing LLMs with another black-box answerer.

## 3. Paper Claims

Paper claims should be staged by evidence strength.

| Claim level | Paper-safe claim | Evidence status |
| --- | --- | --- |
| Core method claim | EGR formalizes conic-section solving as state-action-transition reasoning over theorem actions. | Supported by code architecture and theorem library. |
| Interpretability claim | EGR records theorem sequences, state transitions, and entropy traces, making the reasoning process inspectable. | Supported by `ReasoningResult`, selector info, entropy reports. |
| Entropy-module claim | Learned state entropy correlates with normalized remaining reasoning steps in current repo logs. | Supported by entropy outputs, needs protocol wording. |
| Efficiency/process claim | The full EGR scoring can reduce average reasoning steps compared with neural-only variants in a 50-sample preliminary ablation. | Preliminary only. |
| Performance claim | EGR improves final answer accuracy on Conic10K. | Not yet established; TODO after unified evaluation. |
| LLM augmentation claim | EGR provides structured theorem/action traces that can improve LLM high-difficulty reasoning. | No current evidence; design experiment only. |

## 4. Proposed Title and Abstract Direction

Working title:

> Entropy-Guided Neural-Symbolic Reasoning for Conic Section Problem Solving

Alternative:

> Theorem-Action Entropy Guidance for Interpretable Conic Section Reasoning

Abstract should emphasize:

1. Conic10K is a high-difficulty mathematical reasoning setting.
2. EGR decomposes solutions into executable theorem actions.
3. The method separates symbolic execution from neural uncertainty modeling.
4. Three distinct quantities are used: `P(Y|X)`, `H(S)`, `InfoGain`, and `H(Y|X)`.
5. Results are TODO until unified evaluation.

## 5. Detailed Paper Structure

### Abstract

Content:
- Problem: hard conic-section reasoning requires multi-step symbolic derivation and robust action selection.
- Method: EGR, a neural-symbolic framework with theorem actions and entropy-guided scoring.
- Evidence: TODO final main result, TODO theorem selection result, TODO entropy result, TODO LLM augmentation result.
- Boundary: no SOTA claim unless final evaluation supports it.

### 1. Introduction

Recommended logic:

1. High-difficulty mathematical reasoning is not only answer generation; it requires selecting valid intermediate operations.
2. LLMs are flexible but can produce unverifiable or inconsistent derivations; symbolic solvers are exact but need effective search guidance.
3. Conic10K is a representative hard setting because problems combine geometric concepts, algebraic constraints, and multi-step theorem use.
4. EGR bridges the two sides by turning reasoning into theorem-action sequences over a dual-layer state.
5. The symbolic layer checks applicability and executes transformations; the neural layer estimates action probabilities and uncertainty.
6. The three-layer entropy framework provides the unifying control signal.
7. Contributions:
   - A neural-symbolic theorem-action formulation for Conic10K.
   - A dual-layer state and formal theorem library with executable state transitions.
   - A three-layer entropy decision framework: policy probability, state information gain, and prediction-entropy penalty.
   - An evaluation plan covering theorem selection, reasoning process success, final answer accuracy, entropy trajectory quality, and LLM+EGR augmentation.

### 2. Related Work

Do not invent citations. Use the following topic slots:

1. Neural-symbolic reasoning for mathematical problem solving. Citation TODO.
2. Automated theorem proving and search-guided symbolic reasoning. Citation TODO.
3. Mathematical reasoning with LLMs and verifier/solver augmentation. Citation TODO.
4. Entropy, uncertainty, and information gain in sequential decision making. Citation TODO.
5. Conic10K and geometry/math reasoning datasets. Citation TODO.

### 3. Problem Formulation

Define:

- Input problem `x = (F, q)`, where `F` is fact expressions and `q` is query expression.
- Symbolic state `s_t^sym` stores exact objects, equations, parameters, relations, coordinates, constraints.
- Abstract state `s_t^abs = phi(s_t^sym, q, t) in R^28`.
- Action `y_t in A`, where `A` is the 80-ID theorem action universe and `A_impl` is the currently implemented subset.
- Transition `s_{t+1}^sym = T_{y_t}(s_t^sym)` is valid only if `can_apply_{y_t}(s_t^sym)=1`.
- Goal: produce answer `a_hat = Extract(s_T^sym, q)` and trace `tau=(y_1,...,y_T)`.

### 4. Method

#### 4.1 Dual-Layer State

Explain why two states are needed:
- `SymbolicState`: exact execution, traceability, can_apply/apply.
- `AbstractState`: fixed neural input and lightweight progress features.

Current vector detail:
- Curve type: 5 one-hot dimensions.
- Query type: 10 one-hot dimensions.
- Information features: 11 dimensions.
- Completeness score and normalized depth: 2 dimensions.
- Total: 28 dimensions.

#### 4.2 Theorem Action Library

Define each theorem action as:

`a_i = (pre_i, trans_i, name_i)`.

- `pre_i(s)=1` iff action is executable.
- `trans_i(s)` adds derived parameters, equations, or relations.
- Current implementation: 56/80 registered theorem models.
- Paper wording: "we build toward an 80-action theorem universe and currently instantiate TODO/80 after final audit" until submission.

#### 4.3 Theorem Selection Policy `P(Y|X)`

Formalization:

`pi_theta(y_t | s_t^abs) = softmax(f_theta(s_t^abs))_y`.

Training:

`\mathcal{L}_{policy} = - \sum_t log pi_theta(y_t^* | s_t^abs)`.

Paper boundary:
- This is the theorem selection policy, not final answer prediction.
- Report Top-1/Top-3/Top-5 theorem-step accuracy separately.

#### 4.4 State Entropy `H(S)` and Information Gain

State entropy is solving-progress uncertainty:

`H_phi(s_t) in [0,1]`.

Current implementations:
- Heuristic: completeness and coverage based.
- Learned-linear estimator: trained against normalized remaining steps.

Information gain:

`InfoGain(y_t) = H(s_t) - H(s_{t+1})`.

Paper boundary:
- `H(S)` is not the same as `H(Y|X)`.
- Entropy evidence should be reported as correlation, monotonicity, and success/failure separation, not as final answer accuracy.

#### 4.5 Prediction Entropy `H(Y|X)`

Prediction entropy:

`H(Y|X) = - \sum_y pi_theta(y|s_t) log pi_theta(y|s_t)`.

Role:
- Penalizes uncertain theorem-selection distributions.
- This term is a decision confidence penalty, not a separate learned target.

#### 4.6 Integrated Scoring

For executable candidate theorem `y`:

`Score(y) = lambda_1 pi_theta(y|s_t) + lambda_2 InfoGain(y) - lambda_3 H(Y|X)`.

Default repo weight in current experiments:

`lambda = (0.6, 0.3, 0.1)`.

#### 4.7 Reasoning Algorithm

Algorithm steps:

1. Construct `s_0^sym` and `s_0^abs` from facts and query.
2. Predict theorem distribution and prediction entropy.
3. Filter actions by `can_apply`.
4. Simulate candidate transitions and estimate `InfoGain`.
5. Select max-score theorem and apply it to `SymbolicState`.
6. Rebuild `AbstractState`, record trace, stop on answer extraction, no model, or max steps.

### 5. Experiments

Separate metrics:

1. Theorem selection accuracy: Top-1/Top-3/Top-5 on labeled theorem steps.
2. Reasoning process success rate: executable progress without early failure.
3. Final answer accuracy: exact or normalized answer match.
4. Entropy trajectory quality: correlation with remaining steps, monotonicity, delta, successful vs failed paths.
5. LLM baseline vs LLM+EGR: direct LLM, LLM with theorem candidates, LLM with EGR trace/verifier.

Tables:

- Table 1: Dataset and theorem-library audit.
- Table 2: Main Conic10K result.
- Table 3: Search/entropy ablation.
- Table 4: Entropy trajectory analysis.
- Table 5: LLM baseline and LLM+EGR.

All final result cells should initially be `TODO: fill after unified evaluation`.

### 6. Analysis

Recommended subsections:

1. Entropy as a progress signal.
2. Failure decomposition: theorem selection, symbolic execution, answer extraction, unsupported theorem, max-step loop.
3. Case study with theorem sequence and entropy trace.
4. LLM augmentation case study, only after evidence exists.

### 7. Conclusion

Emphasize:
- EGR provides a controllable neural-symbolic route for hard conic-section reasoning.
- The current method is an interpretable theorem-action solver and a structured assistant for LLM reasoning.
- Limitations: theorem library incompleteness, final answer accuracy, unified protocol, reference completion.

## 6. Terminology Lock

Use these terms consistently:

| Term | Meaning |
| --- | --- |
| `theorem action` | One formal model ID/action selected and executed by EGR |
| `theorem selection policy` | Neural distribution `P(Y|X)` over theorem actions |
| `state entropy` | `H(S)`, uncertainty/progress measure over solving state |
| `information gain` | `H(S_t)-H(S_{t+1})`, expected or simulated entropy reduction |
| `prediction entropy` | `H(Y|X)`, entropy of theorem-selection distribution |
| `reasoning success` | Process-level completion or valid answer extraction under the evaluator |
| `final answer accuracy` | Gold-answer correctness; must be reported separately from reasoning success |
| `LLM+EGR` | LLM reasoning assisted by EGR theorem candidates, traces, or verification |

