# EGR KBS Section Argument Map

> Status: initial paragraph-level map. Each paragraph has one primary job. Paragraph counts may be adjusted after figures, results, and KBS formatting requirements are fixed.

## A. Final presentation order

### Abstract — draft last

- **A1 Problem/gap:** reliable multi-step solving requires explicit mathematical decisions and executable state changes.
- **A2 Approach:** introduce EGR as query-conditioned RM selection, grounding, symbolic transition, and RSE control.
- **A3 Main standalone result:** report the decisive end-to-end comparison only after results are frozen.
- **A4 Mechanism evidence:** report one or two process-level findings that explain the result.
- **A5 Boundary/implication:** limit evidence to conic sections and present LLM augmentation as an extension.

### 1. Introduction

- **P1 Context:** explain why reliable mathematical problem solving requires more than final-answer generation.
- **P2 Research object:** derive the core difficulties from conic-section problem characteristics.
- **P3 Prior capability and gap:** synthesize generative, process-supervised, program-aided, and formal methods; identify the missing integrated executable loop.
- **P4 Modeling insight:** formulate solving as state-conditioned RM selection and symbolic state transition with multiple valid paths.
- **P5 Proposed response:** summarize dual-state representation, Selector, Grounder, Applicator, shared primitives, RSE, and terminal extraction in causal order.
- **P6 Study questions and contributions:** state bounded contributions, evaluation route, standalone priority, and domain boundary.

### 2. Related Work

- **RW1 Generative reasoning and process supervision:** intermediate reasoning helps, but textual steps do not by themselves expose applicability and symbolic effects.
- **RW2 Program/tool and neuro-symbolic execution:** executable tools improve computation; position RM execution against arbitrary programs and one-shot formalization.
- **RW3 Formal theorem guidance and geometry reasoning:** connect EGR with proof-state action selection and neural-guided symbolic geometry while distinguishing answer solving from general theorem proving.
- **RW4 Progress, value, uncertainty, and stopping:** separate action uncertainty, verifier/outcome scores, remaining-step proxies, and goal-conditioned RSE.
- **RW5 Domain-specific lineage:** explain the relation to prior function/relation-centric solvers and the conic-specific reasoning contribution.

### 3. Problem Formulation

- **PF1 Task and scope:** define (x=(F,q)), the conic domain, solver input, and required output.
- **PF2 Reasoning state:** define semantic state, control context, SymbolicState, AbstractState, and query conditioning.
- **PF3 Action hierarchy:** define RM, binding, bound action, symbolic primitive, and transition contract.
- **PF4 Multiple solutions:** define valid transition, reference path, solution graph, and verified valid-action set.
- **PF5 Residual progress:** define successful completion paths, formal RSE, conditioning variables, and RSE reduction.
- **PF6 Termination and success:** define AnswerReady, terminal extraction, unresolved exits, and verified solution.

### 4. EGR Method

- **M1 Overview:** walk through one complete EGR iteration and relate each component to the formulation.
- **M2 State construction:** explain how the initial SymbolicState and query-conditioned AbstractState are built and updated.
- **M3 RM library:** describe the 80 high-level RMs, category structure, shared primitives, and contract.
- **M4 Selector:** motivate state-conditioned RM ranking and describe set-supervised learning over (A^+(S,q)).
- **M5 Grounder:** explain deterministic constrained binding, ranking, and limited backtracking.
- **M6 Applicator:** describe transactional precondition checking, primitive execution, delta generation, postcondition checking, and failure codes.
- **M7 RSE controller:** distinguish graph target, learned estimator, successor scoring, action cost, and stopping use.
- **M8 Terminal extraction:** show that the extractor reads, normalizes, and validates an answer already supported by the terminal state.
- **M9 End-to-end algorithm/example:** align Algorithm 1 with the runtime and use one running conic example to show state, RM, binding, primitive trace, delta, RSE, and alternative paths.

### 5. Data and Evaluation Protocol

- **D1 Dataset and split:** describe Conic10K scope, problem types, query types, provenance, and problem-level split.
- **D2 Weak supervision issue:** explain why natural-language `models` sequences cannot be treated as exact execution order.
- **D3 Internal reconstruction:** describe reference-path verification, alternative continuation search, solution graphs, positive/negative/unknown labels, and audit.
- **D4 Training views:** specify inputs and labels for the Selector, Grounder, RSE estimator, and stopping controller.
- **D5 Baselines:** define rule/uniform search, 28D hard-label, 28D set-supervised, structured-state selector, RSE variants, full EGR, and comparable external methods.
- **D6 Metrics and reproducibility:** define answer, process, RSE, efficiency, subgroup, statistical, and artifact-reporting protocols.

### 6. Standalone Results

- **R1 End-to-end evidence:** answer the main solver question with final-answer accuracy and verified solution rate.
- **R2 Selection evidence:** evaluate valid-action ranking, set supervision, structured state, calibration, and long-tail RMs.
- **R3 Execution evidence:** report grounding success, transition validity, conflict/no-op rates, and RM/primitive coverage.
- **R4 Component and efficiency evidence:** isolate Grounder, Applicator, structured state, RSE ranking, RSE stopping, backtracking, and costs.
- **R5 Heterogeneity and failures:** analyze curve/query type, depth, path multiplicity, initial RSE, and phase-specific error buckets.

### 7. RSE Analysis

- **E1 Target validity:** compare estimated RSE with graph-derived targets and simpler proxies.
- **E2 Ranking role:** test whether successful or lower-cost successors receive lower RSE than invalid or dead-end successors.
- **E3 Stopping role:** compare fixed depth, AnswerReady only, RSE only, and the joint stopping rule.
- **E4 Trajectory interpretation:** show RSE along successful, failed, alternative, and perturbed trajectories using the running example.

### 8. LLM Augmentation

- **L1 Protocol:** define the four controlled LLM conditions, equal information/budget rules, and no-gold-leakage boundary.
- **L2 Main comparison:** report answer and executable-step outcomes across LLM families.
- **L3 Mechanism analysis:** distinguish the effects of RM guidance and grounded execution using correction, harm, adoption, ignore, and misuse rates.
- **L4 Boundary:** explain where EGR helps, where the LLM ignores or misuses it, and why these results do not redefine EGR as an LLM method.

### 9. Discussion and Limitations

- **DI1 Central meaning:** interpret what state-conditioned executable reasoning changes relative to direct answer generation.
- **DI2 Relation to prior work:** explain the precise advance beyond textual paths, generic programs, and formal proof guidance.
- **DI3 RSE meaning:** discuss RSE as solver- and goal-conditioned residual difficulty, not human cognition or answer confidence.
- **DI4 Limitations:** cover RM-library dependence, Grounder coverage, incomplete solution graphs, RSE approximation, and conic-specific scope.
- **DI5 Transfer boundary:** identify what is architecturally reusable and what must be rebuilt for another mathematical domain.

### 10. Conclusion

- **C1 Synthesis:** restate the formulation, executable architecture, RSE role, and decisive standalone evidence.
- **C2 Boundary and implication:** close with the conic-specific evidence boundary and the broader potential of state-conditioned executable reasoning.

## B. Cross-section control rules

1. Use the same running conic example in Problem Formulation, Method, RSE Analysis, and the case study.
2. Introduction poses questions that Results explicitly answer; Results must not introduce an unmotivated central claim.
3. Related Work establishes capability and remaining gap; it must not become a list of systems that lack EGR.
4. Method explains what the system does and why; Results alone state how well it works.
5. Each major claim appears with different functions only: introduce, define, demonstrate, interpret, and synthesize.
6. Quantitative language remains a placeholder until the relevant experiment is frozen.

## C. Drafting order

1. Problem Formulation
2. EGR Method
3. Data and Evaluation Protocol
4. Standalone Results and RSE Analysis structure
5. Related Work
6. Introduction
7. Discussion and Conclusion
8. Abstract and title
