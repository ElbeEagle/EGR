# EGR Terminology and Notation Ledger

> Status: provisional terminology lock for the KBS working draft. **Reasoning model** is used according to the current author decision; its final English name will be reviewed with the supervisor.

## 1. Canonical terminology

| Canonical term | Working definition | Avoid or restrict |
|---|---|---|
| **EGR** | A standalone executable and progress-aware neuro-symbolic solver for conic-section problems. | Do not define EGR primarily as an LLM plugin. |
| **reasoning model (RM)** | A high-level, mathematically meaningful domain schema with precondition, grounding, symbolic program, and postcondition. | Do not use `model` alone. Do not imply that an RM is a neural network. |
| **reasoning-model library** | The finite collection of 80 conic-section RMs available to the solver. | `model pool` may remain in code/history but is not preferred prose. |
| **RM ID** | Identifier of a high-level reasoning model; the Selector's prediction target. | It is not a primitive operation or a fully bound executable action. |
| **bound action** | An executable RM instance paired with concrete object/variable bindings. | Do not equate it with an RM ID. |
| **binding** | Mapping from an RM's formal roles to points, lines, curves, variables, or expressions in the current state. | Do not describe binding as answer prediction. |
| **symbolic primitive** | A reusable deterministic operation for algebra, geometry, normalization, constraint solving, or equivalence checking. | Do not present 80 RMs as 80 unrelated primitive implementations. |
| **Selector** | A learned policy that ranks high-level RM IDs from the query-conditioned AbstractState. | Do not call it an answer predictor or let it predict gold answers. |
| **Grounder** | The component that instantiates a selected RM with concrete bindings under symbolic constraints. | Do not merge grounding silently into the Selector. |
| **symbolic Applicator** | The component that checks preconditions, runs the primitive program transactionally, produces a state delta, and checks postconditions. | `executor` may be explanatory prose, but Applicator is the component name. |
| **semantic state** | The mathematical content currently known: objects, equations, parameters, relations, constraints, derived facts, query, and unresolved subgoals. | Do not mix search failures or retry history into mathematical truth. |
| **SymbolicState** | The executable implementation of the semantic state. | Do not use it as a loose name for the whole controller state. |
| **control context** | Attempted actions, successful actions, bindings, failure codes, state hashes, depth, costs, and backtracking information. | It does not change the mathematical meaning of the semantic state. |
| **AbstractState** | A query-conditioned neural representation derived from the semantic state and a limited control summary. | The current 28-dimensional vector is a baseline, not the final definition. |
| **state transition** | A verified update from one semantic state to another through a bound action. | A predicted RM that is not applied is not a transition. |
| **state delta** | The explicit mathematical facts added or refined by a successful transition. | A successful transition must not be an unrecorded in-place mutation. |
| **reference path** | A verified executable interpretation seeded from a human-written rationale. | Do not call it the unique gold path. |
| **solution graph** | A graph or partial-order structure containing verified transitions and successful continuations. | Do not assume an incomplete graph contains all valid solutions. |
| **verified valid-action set** | RM IDs or bound actions verified to be executable and to retain a successful continuation from the current state. | Do not label undiscovered alternatives as negative. |
| **Residual State Entropy (RSE)** | A goal-conditioned negative-log reachability potential induced by successful executable trajectories under a stated reference policy, budget, and cost. | Do not define it as remaining steps, generic uncertainty, or answer-correctness probability. |
| **RSE reduction** | Difference between current-state RSE and successor-state RSE, optionally adjusted by action cost. | Do not call every non-empty transition progress. |
| **AnswerReady** | A structural predicate indicating that the query can be resolved from the current semantic state without another substantive reasoning step. | It is not equivalent to low RSE or gold-answer correctness. |
| **terminal state** | A state satisfying the stopping contract and supporting answer extraction. | A maximum-step or no-progress stop is an unresolved state, not a successful terminal state. |
| **answer extractor** | A read-only component that locates, normalizes, and internally validates an answer already supported by the terminal state. | It must not perform hidden substantive solving. |
| **verified solution** | A trajectory with valid transitions, a resolved query, and a gold-equivalent final answer. | Final-answer correctness alone is insufficient. |
| **LLM augmentation** | A controlled extension that supplies RM guidance, grounded execution, or EGR traces to an LLM. | Do not present it as the definition of EGR. |

## 2. Notation

| Symbol | Meaning |
|---|---|
| (x=(F,q)) | A problem with initial facts/constraints (F) and query (q). |
| (S_t^{\mathrm{sem}}) | Semantic state after (t) accepted transitions. |
| (C_t) | Control context at step (t). |
| (S_t^{\mathrm{abs}}=\phi(S_t^{\mathrm{sem}},q,\bar C_t)) | Query-conditioned AbstractState; (\bar C_t) is a permitted control summary. |
| (\mathcal M=\{M_1,\ldots,M_K\}) | Reasoning-model library; currently (K=80). |
| (M_i=(\mathrm{pre}_i,\mathrm{ground}_i,\mathrm{program}_i,\mathrm{post}_i)) | High-level RM contract. |
| (a_t=(M_i,\theta_t)) | Bound action with binding (\theta_t). |
| (T(S_t^{\mathrm{sem}},a_t)) | Transactional symbolic transition. |
| (\Delta_t) | State delta produced by an accepted action. |
| (A^+(S_t,q)) | Verified valid-action set for the current state and query. |
| (p_\theta(M_i\mid S_t^{\mathrm{abs}},q)) | Selector distribution over RM IDs. |
| (\Pi^+(S,q)) | Verified successful completion trajectories from ((S,q)). |
| (H_{\mathrm{RSE}}(S,q\mid\mathcal M,\pi_0,B,c)) | Formal RSE under library, reference policy, budget, and action cost. |
| (\Delta H(S,a)) | RSE reduction caused by action (a). |
| (\hat a=\mathrm{Extract}(S_T,q)) | Predicted answer extracted from terminal state (S_T). |

## 3. Terminology decisions still open

1. **Reasoning model** is the current provisional English term recommended by the supervisor. Candidate alternatives, including `theorem-action schema`, remain deferred.
2. Legacy code and data may use `theorem model`, `model ID`, or `models`. These names describe historical artifacts and must not silently determine the final paper definition.
3. Because `reasoning model` can also refer to a trained language model, the manuscript must use the full term or `RM` for domain schemas and use `Selector`, `RSE estimator`, `neural network`, or `LLM` for learned components.
4. Use **neuro-symbolic** consistently; do not alternate with `neural-symbolic` unless required by a cited title.

## 4. Style rule

Define each technical term once, then reuse the canonical term. Prefer a plain-language explanation before the formal name, and avoid strings of three or more hyphenated modifiers.
