# EGR Claim–Evidence Matrix

> Status: initial evidence contract. Existing files show prototype components only; they do not establish vNext fidelity or final paper results. All quantitative result cells remain pending until the evaluation protocol is frozen and rerun.

## Status labels

- **Prototype:** related implementation or diagnostic artifact exists.
- **vNext required:** implementation/data must be rebuilt or extended.
- **Result pending:** no final KBS claim may be written in completed-result language.

## Claim matrix

| ID | Bounded claim | Code evidence | Data evidence | Required experiment and metric | Current result status |
|---|---|---|---|---|---|
| **C1** | Conic-section solving can be represented as query-conditioned executable RM transitions with multiple valid paths. | Prototype state and reasoning loop: `src/state/`, `src/theorems/`, `src/reasoning/reasoning_engine.py`, `src/reasoning/search.py`. A vNext transition contract and bound-action runtime are required. | Existing weak sequences: `data/train_with_models_v2.json`; verified reference paths and solution graphs are required. | Full executable trace examples; transition coverage; unique-path versus multi-path analysis; failure attribution. | **Prototype / vNext required / result pending** |
| **C2** | Query-conditioned dual-state representation and grounded symbolic application support accurate, auditable transitions. | Prototype: `src/state/symbolic_state.py`, `src/state/abstract_state.py`, `src/theorems/base_model.py`, `src/theorems/theorem_library.py`. Grounder, transactional delta, primitive trace, and postcondition support remain required. | Bound-action records with bindings, precondition evidence, deltas, primitive traces, and postcondition evidence are required. | Grounding success; transition validity; conflict/no-op rate; state-aliasing analysis; 28D versus structured-state ablation. | **Prototype / vNext required / result pending** |
| **C3** | Set-supervised RM selection is more appropriate than reproducing one annotated next ID. | Current hard-label selector: `src/selector/`; reasoning adapter: `src/reasoning/model_selector.py`. Set-supervised training and inference are required. | Verified (A^+(S,q)) sets with positive, negative, and unknown labels are required; splits must be problem-level. | Valid@1/3/5; mean rank to any valid action; coverage; calibration; long-tail performance; hard-label versus set-supervised ablation. | **Hard-label prototype / vNext required / result pending** |
| **C4** | Goal-conditioned RSE estimates residual solving difficulty and improves successor ranking and stopping. | Current baselines: `src/reasoning/entropy_estimator.py`, `src/entropy/`. Graph-derived RSE target construction and query-conditioned estimation are required. | Solution-graph-derived targets with stated (\pi_0), budget, cost, and incomplete-graph masks/bounds are required. | Target MAE/rank correlation/calibration; successor ordering accuracy; ranking gain; premature-stop and over-reasoning rates; comparison with remaining steps, completeness, shortest distance, and selector entropy. | **Heuristic/linear baseline only / vNext required / result pending** |
| **C5** | Full standalone EGR improves verified conic-section solving under a frozen, no-leakage protocol. | Prototype engine/search/extraction/evaluation: `src/reasoning/`, `src/evaluation/protocol.py`; scripts: `scripts/evaluation/`, `scripts/experiments/run_search_ablation.py`. Extractor must be made read-only and the runtime aligned with Algorithm 1. | Frozen problem-level train/dev/test split; verified transitions; test manifest; per-instance audit records. | Final-answer accuracy; verified solution rate; transition validity; grounding success; unresolved/invalid rate; theorem/primitive cost; backtracking; runtime; confidence intervals. | **Protocol prototype / final rerun required / result pending** |
| **C6** | RM guidance and grounded symbolic execution can provide complementary improvements to LLM reasoning. | A controlled LLM integration/evaluation path is still required; standalone components may be exposed only after their interfaces are stable. | Same frozen test problems; complete prompts, responses, tool traces, parsing failures, model versions, and budgets. | Direct LLM; LLM + RM candidates; LLM + grounded execution; LLM + full EGR; answer accuracy; executable-step rate; correction/harm rate; adoption/ignore/misuse rate; cost. | **Planned extension / result pending** |

## Claim discipline

1. C1–C5 form the standalone paper core; C6 is an extension.
2. Passing unit tests or registering an RM is not evidence of mathematical coverage or end-to-end effectiveness.
3. The rebuilt trajectory layer supports training and evaluation but is not claimed as an independent dataset contribution.
4. `Final-answer accuracy` is the primary task result; `verified solution rate` and process metrics determine whether the answer was reached through an executable path.
5. Any future sentence using `outperforms`, `improves`, `demonstrates`, `calibrated`, or `generalizes` must cite a completed row of experimental evidence.

## Evidence still missing before final drafting

- frozen vNext runtime and Algorithm 1 correspondence;
- 80/80 RM contract and conformance report;
- verified multi-path solution graphs and action sets;
- graph-derived RSE targets and estimator;
- frozen standalone results with uncertainty estimates;
- controlled LLM augmentation results;
- targeted literature support for conic-specific solving and RSE's search/control antecedents.
