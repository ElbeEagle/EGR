# EGR KBS Manuscript Contract

> Status: initial working version for author review. This document fixes the paper's argument before full-section drafting. It does not treat unfinished implementations or planned results as established evidence.

## 1. Paper identity

- **Target venue:** Knowledge-Based Systems (KBS)
- **Paper type:** algorithmic research paper
- **Research object:** executable, progress-aware solving of conic-section problems
- **Primary system:** standalone EGR solver
- **Secondary extension:** EGR-assisted LLM reasoning
- **Empirical scope:** conic-section problems only

## 2. Central research question

> Can conic-section problem solving be formulated as a query-conditioned process of reasoning-model selection, grounded symbolic transition, and residual-entropy-guided control?

Secondary question:

> Can EGR's executable intermediate capabilities improve the reliability of LLM mathematical reasoning?

## 3. Working thesis

> EGR reformulates conic-section problem solving as query-conditioned selection and grounded execution of high-level reasoning models, and uses Residual State Entropy to connect local symbolic transitions with the remaining difficulty of reaching a verified answer.

The paper should establish this thesis through formal definitions, an executable solver, verified transition data, process-level evaluation, and end-to-end answer evaluation.

## 4. Why conic-section problems

Conic-section problems provide a controlled but non-trivial setting because they combine:

1. structured geometric objects and exact algebraic expressions;
2. a finite domain-knowledge inventory with combinatorial solution paths;
3. state-dependent applicability and object/parameter binding;
4. exact symbolic transformations and constraint preservation;
5. multiple valid action orders or alternative solution paths;
6. query-dependent progress and termination.

These properties make it possible to inspect theorem choice, binding, execution, progress, termination, and answer extraction separately.

## 5. Exact research gap

Existing generative, process-supervised, program-aided, and formal reasoning approaches provide important capabilities, but they do not jointly address the following conic-solving requirements in one executable loop:

- selecting a high-level mathematical reasoning model from the current state;
- grounding that model to concrete mathematical objects;
- executing it through reusable symbolic operations with explicit preconditions and postconditions;
- allowing multiple verified solution paths rather than enforcing one textual order;
- estimating the remaining goal-conditioned solving burden;
- separating process termination from terminal answer extraction and offline answer evaluation.

The gap is therefore a missing integrated reasoning formulation, not merely the absence of an EGR-named module.

## 6. Core causal chain

```text
Characteristics of conic-section problems
    -> state-dependent theorem choice, binding, exact execution, and stopping
    -> limitations of direct generation and fixed procedural rules
    -> query-conditioned state and high-level reasoning-model action space
    -> Selector -> Grounder -> symbolic Applicator -> successor state
    -> solution graph and set-supervised valid-action learning
    -> RSE-based successor ranking and continuation control
    -> answer extraction from a terminal symbolic state
    -> verified end-to-end solution and process-level diagnosis
```

## 7. Contribution hierarchy

- **C1 — Problem formulation:** formulate conic-section solving as state-conditioned executable reasoning-model transitions with multiple valid paths.
- **C2 — Executable reasoning architecture:** combine query-conditioned dual-state representation, reasoning-model selection, grounding, and shared symbolic primitives in one auditable loop.
- **C3 — Set-supervised selection:** train and evaluate the Selector against verified valid-action sets rather than a single reference action.
- **C4 — Residual State Entropy:** define a goal-conditioned residual difficulty measure and use its estimate for successor ranking and continuation control.
- **C5 — Standalone solver evidence:** evaluate final-answer correctness, verified solution rate, transition validity, efficiency, and failure modes under a frozen protocol.
- **C6 — LLM extension:** test whether reasoning-model guidance and grounded symbolic execution improve different LLMs without making LLM integration a prerequisite of EGR.

## 8. Success and evaluation boundary

A solution is successful only when:

1. every accepted transition is executable and passes its postcondition;
2. the terminal state resolves the query;
3. the extracted answer is mathematically equivalent to the gold answer.

The gold answer may be used to construct offline training/evaluation targets and to score the final output. It must not guide test-time selection, grounding, search, ranking, stopping, or extraction.

## 9. Fixed claim boundaries

- The 80 IDs are high-level **reasoning models**, not independent low-level calculation primitives.
- Human-written solutions are reference rationales, not unique gold paths.
- Rebuilt executable trajectories are internal training and evaluation infrastructure, not a standalone dataset contribution.
- Normalized remaining steps and heuristic completeness are RSE baselines, not the formal RSE definition.
- EGR is empirically validated for conic-section problems; cross-domain use is an architectural possibility, not a demonstrated result.
- LLM augmentation is reported only after the standalone solver is evaluated under the same no-leakage principle.

## 10. Evidence rule

Every final manuscript claim must point to at least one of the following: a formal definition, executable code path, verified data artifact, controlled experiment, quantitative result, or traceable case study. Planned outcomes must remain labeled as hypotheses or evidence requirements until results are frozen.
