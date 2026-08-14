# EGR Annotated Bibliography

Last updated: 2026-07-07

This bibliography is an initial screening list for the AAAI 2027 EGR paper. It focuses on work that can support or sharpen the claim that reliable mathematical problem solving should be modeled as state-conditioned theorem-model prediction and executable symbolic state transition, rather than unconstrained next-token generation.

Selection scope: automatic math problem solving, LLM mathematical reasoning, process supervision, verifier-guided reasoning, tool/program-augmented reasoning, formal theorem proving, geometry problem solving, and neuro-symbolic reasoning.

Reading priority:

- High: directly useful for EGR's core positioning, related work, figures, baselines, or claims.
- Medium: useful for background, benchmark framing, or comparison.
- Background: useful mainly for broader context.

## A. LLM Mathematical Reasoning and Process Supervision

### 1. Chain-of-Thought Prompting Elicits Reasoning in Large Language Models

- Venue/year: NeurIPS 2022; arXiv 2022. Link: https://arxiv.org/abs/2201.11903
- Problem: Direct answer generation often fails on arithmetic, commonsense, and symbolic reasoning tasks that require intermediate steps.
- Method mechanism: Prompt LLMs with exemplars that include natural-language intermediate reasoning chains before the final answer.
- Citable point for EGR: Stepwise reasoning improves LLM mathematical performance, but the reasoning unit remains free-form text.
- EGR implication: Use CoT as the main contrast: CoT generates a chain of textual thoughts, while EGR executes a chain of theorem-model transitions.
- Figure/writing implication: Put CoT in the left branch of a paradigm figure: `Problem -> generated reasoning text -> Answer`.
- Priority: High.

### 2. Self-Consistency Improves Chain of Thought Reasoning in Language Models

- Venue/year: ICLR 2023; arXiv 2022. Link: https://arxiv.org/abs/2203.11171
- Problem: Greedy CoT decoding can select a brittle or locally plausible reasoning path.
- Method mechanism: Sample multiple reasoning paths and marginalize over final answers to select the most consistent answer.
- Citable point for EGR: Mathematical reasoning often admits multiple paths, and inference-time selection can improve reliability.
- EGR implication: EGR can absorb this idea at the action-path level: sample or rank theorem-model trajectories, not just text chains.
- Figure/writing implication: Use as evidence that path selection matters, then argue that EGR makes the path space executable and inspectable.
- Priority: Medium.

### 3. Large Language Models are Zero-Shot Reasoners

- Venue/year: NeurIPS 2022; arXiv 2022. Link: https://arxiv.org/abs/2205.11916
- Problem: Few-shot CoT depends on curated exemplars and may not generalize across tasks.
- Method mechanism: A simple trigger such as "Let's think step by step" elicits intermediate reasoning in zero-shot settings.
- Citable point for EGR: Stepwise reasoning behavior can be elicited, but it is still unconstrained by mathematical applicability conditions.
- EGR implication: Motivates replacing unconstrained step text with state-conditioned theorem models.
- Figure/writing implication: Mention under "prompting-based step generation" as an important but ungrounded baseline family.
- Priority: Medium.

### 4. Least-to-Most Prompting Enables Complex Reasoning in Large Language Models

- Venue/year: ICLR 2023; arXiv 2022. Link: https://arxiv.org/abs/2205.10625
- Problem: CoT can struggle when test problems are more complex than prompt exemplars.
- Method mechanism: Decompose a complex problem into simpler subproblems and solve them sequentially, using earlier answers as context for later steps.
- Citable point for EGR: Complex reasoning benefits from explicit decomposition and state reuse.
- EGR implication: Supports the view that mathematical solving is a state-evolving process rather than a single problem-to-answer mapping.
- Figure/writing implication: Use when explaining why EGR maintains `S_t` and updates it after each theorem action.
- Priority: Medium.

### 5. STaR: Bootstrapping Reasoning With Reasoning

- Venue/year: arXiv 2022. Link: https://arxiv.org/abs/2203.14465
- Problem: Human-written rationales are expensive, but rationale supervision helps reasoning.
- Method mechanism: Iteratively generate rationales, filter by correct answers, fine-tune, and repeat.
- Citable point for EGR: Intermediate reasoning traces can be bootstrapped and used as learning signals.
- EGR implication: EGR trajectories could similarly be bootstrapped from solver traces, but with stronger action/state validation than answer-filtered rationales.
- Figure/writing implication: Mention as background for training on process traces.
- Priority: Medium.

### 6. Training Verifiers to Solve Math Word Problems

- Venue/year: arXiv 2021. Link: https://arxiv.org/abs/2110.14168
- Problem: Large language models still struggle with robust multi-step math word problem solving.
- Method mechanism: Generate many candidate solutions and use a trained verifier to rank solution correctness; introduces GSM8K.
- Citable point for EGR: Verification improves math reasoning and scales differently from plain finetuning.
- EGR implication: EGR internalizes verification through `can_apply/apply` and terminal extraction rather than only judging final completions.
- Figure/writing implication: Use in motivation for separating generation, verification, and answer selection.
- Priority: High.

### 7. Measuring Mathematical Problem Solving With the MATH Dataset

- Venue/year: NeurIPS 2021 dataset track; arXiv 2021. Link: https://arxiv.org/abs/2103.03874
- Problem: Mathematical problem solving remains difficult for models even with large scale and step-by-step solutions.
- Method mechanism: Builds MATH, a competition-level dataset with full solutions; evaluates model scaling.
- Citable point for EGR: Pure scaling is not enough for difficult mathematical reasoning; algorithmic advances are needed.
- EGR implication: Supports the claim that EGR should be presented as an algorithmic/neuro-symbolic reasoning interface, not only a larger model or prompt.
- Figure/writing implication: Cite in the introduction when stating that math reasoning remains structurally hard.
- Priority: High.

### 8. Let's Verify Step by Step

- Venue/year: ICLR 2024; arXiv 2023. Link: https://arxiv.org/abs/2305.20050
- Problem: Outcome supervision gives only final-answer feedback and misses errors inside multi-step reasoning.
- Method mechanism: Compare outcome supervision with process supervision using step-level labels; release PRM800K.
- Citable point for EGR: Process supervision can outperform outcome supervision for challenging math problems.
- EGR implication: Strong support for EGR's process-level evaluation: model selection, applicability, state transition, termination, and answer extraction should be measured separately.
- Figure/writing implication: Add an error taxonomy figure that separates selection, execution, termination, and extraction failures.
- Priority: High.

### 9. Math-Shepherd: Verify and Reinforce LLMs Step-by-step without Human Annotations

- Venue/year: ACL 2024; arXiv 2023. Link: https://arxiv.org/abs/2312.08935
- Problem: Human step-level process labels are expensive.
- Method mechanism: Automatically construct process-wise supervision and train process reward models for verification and reinforcement learning.
- Citable point for EGR: Step-level reward signals can guide mathematical reasoning without fully manual annotation.
- EGR implication: EGR's `H(S)` and information gain can be positioned as structured process signals, not generic uncertainty scores.
- Figure/writing implication: Use when motivating progress-aware selection and termination control.
- Priority: High.

### 10. Premise-Augmented Reasoning Chains Improve Error Identification in Math Reasoning with LLMs

- Venue/year: ICML 2025, PMLR 267. Link: https://proceedings.mlr.press/v267/mukherjee25a.html
- Problem: Linear CoT chains can be verbose and hard to verify because dependencies between steps are implicit.
- Method mechanism: Convert linear reasoning chains into premise-augmented DAGs with explicit premise links for each step.
- Citable point for EGR: Mathematical step verification improves when each step is tied to its premises.
- EGR implication: EGR's state-conditioned transition is stronger than premise links alone: each theorem model has preconditions, execution, and state update.
- Figure/writing implication: Draw the EGR trace as a dependency graph over states/facts, not only a linear solution.
- Priority: High.

### 11. MathScale: Scaling Instruction Tuning for Mathematical Reasoning

- Venue/year: ICML 2024, PMLR 235. Link: https://proceedings.mlr.press/v235/tang24k.html
- Problem: Open LLMs need higher-quality math reasoning data and broader evaluation across math word problem datasets.
- Method mechanism: Build a concept graph from topics/knowledge points, generate MathScaleQA with two million question-answer pairs, and evaluate with MWPBench.
- Citable point for EGR: Data scaling improves LLM math ability, but the paper still frames reasoning largely as question-answer generation.
- EGR implication: EGR can use concept/theorem structure more explicitly than instruction-tuning data generation.
- Figure/writing implication: Cite as representative data-scaling baseline/context, not as a direct methodological competitor.
- Priority: Medium.

### 12. Minerva: Solving Quantitative Reasoning Problems with Language Models

- Venue/year: arXiv 2022. Link: https://arxiv.org/abs/2206.14858
- Problem: General LMs struggle with quantitative science and math reasoning.
- Method mechanism: Further pretrain a large model on technical content and evaluate on math/science benchmarks.
- Citable point for EGR: Domain-specific technical data improves quantitative reasoning but does not provide explicit symbolic state control.
- EGR implication: Helps position EGR against model-scale/domain-pretraining approaches.
- Figure/writing implication: Include under "model scaling and domain pretraining" in related work.
- Priority: Medium.

### 13. Llemma: An Open Language Model For Mathematics

- Venue/year: arXiv 2023. Link: https://arxiv.org/abs/2310.10631
- Problem: Open base models have limited mathematical capability.
- Method mechanism: Continue pretraining Code Llama on mathematical papers, web data, and code; release math-oriented models and data.
- Citable point for EGR: Math-specific LMs can be strong foundations for theorem/tool use, but are still not themselves symbolic solvers.
- EGR implication: A math LLM can serve as EGR's selector or guide, while EGR handles applicability and state transition.
- Figure/writing implication: Mention as a potential backbone rather than a complete reasoning framework.
- Priority: Medium.

### 14. DeepSeekMath: Pushing the Limits of Mathematical Reasoning in Open Language Models

- Venue/year: arXiv 2024. Link: https://arxiv.org/abs/2402.03300
- Problem: Open math LMs lag behind frontier systems on competition-level math.
- Method mechanism: Pretrain on 120B math-related tokens and apply GRPO to improve mathematical reasoning.
- Citable point for EGR: Reinforcement learning and math-specific data can strongly improve final answer accuracy.
- EGR implication: EGR should not compete only on "bigger math model"; it should emphasize controllable intermediate decisions and symbolic execution.
- Figure/writing implication: Use as a strong LLM baseline family in experiments.
- Priority: Medium.

### 15. DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning

- Venue/year: arXiv 2025. Link: https://arxiv.org/abs/2501.12948
- Problem: LLM reasoning can be improved through RL, but generated reasoning may be long, hard to read, or weakly grounded.
- Method mechanism: Train reasoning models with large-scale reinforcement learning, cold-start data, and distillation.
- Citable point for EGR: Reasoning has become a training objective in itself, not merely prompt engineering.
- EGR implication: EGR can be positioned as a complementary structured interface for reasoning models: the LLM proposes theorem actions, the symbolic layer validates and executes.
- Figure/writing implication: In the introduction, distinguish "longer internal reasoning" from "externally checkable theorem-model transition".
- Priority: Medium.

## B. Program, Tool, and Solver-Grounded Reasoning

### 16. PAL: Program-aided Language Models

- Venue/year: ICML 2023; arXiv 2022. Link: https://arxiv.org/abs/2211.10435
- Problem: LLMs can decompose problems but often make arithmetic or logical mistakes in executing steps.
- Method mechanism: Let the LLM generate executable programs and delegate computation to a Python runtime.
- Citable point for EGR: A useful division of labor is neural decomposition plus symbolic/external execution.
- EGR implication: PAL is a close predecessor for "predict then execute", but EGR's action space is theorem models over symbolic states rather than arbitrary code.
- Figure/writing implication: Add PAL/PoT in a comparison table: execution target = program runtime; EGR execution target = theorem-model state transition.
- Priority: High.

### 17. Program of Thoughts Prompting

- Venue/year: TMLR/ICML workshop line; arXiv 2022. Link: https://arxiv.org/abs/2211.12588
- Problem: CoT mixes reasoning and computation in natural-language thoughts.
- Method mechanism: Express reasoning as executable programs and offload computation to an external interpreter.
- Citable point for EGR: Disentangling computation from reasoning improves numerical reasoning.
- EGR implication: EGR extends the disentanglement from "reasoning vs computation" to "theorem selection vs symbolic execution vs terminal extraction".
- Figure/writing implication: Use this to justify the modular decomposition of EGR.
- Priority: High.

### 18. Toolformer: Language Models Can Teach Themselves to Use Tools

- Venue/year: NeurIPS 2023; arXiv 2023. Link: https://arxiv.org/abs/2302.04761
- Problem: LMs struggle with tasks where simple external tools are better, such as arithmetic or lookup.
- Method mechanism: Train LMs to decide which API to call, when to call it, with which arguments, and how to incorporate the result.
- Citable point for EGR: Tool-use decisions can be learned and integrated into language modeling.
- EGR implication: EGR's selector is a specialized tool/action policy where each tool is a theorem model with mathematical preconditions.
- Figure/writing implication: Compare "API call" and "theorem-model transition" as two forms of external grounding.
- Priority: Medium.

### 19. ReAct: Synergizing Reasoning and Acting in Language Models

- Venue/year: ICLR 2023; arXiv 2022. Link: https://arxiv.org/abs/2210.03629
- Problem: Reasoning traces and external actions are often studied separately.
- Method mechanism: Interleave natural-language reasoning traces with task-specific actions and observations.
- Citable point for EGR: Interleaving reasoning and action improves interpretability and task success.
- EGR implication: EGR can be framed as a mathematically constrained ReAct-like loop: state, theorem-action, symbolic observation/update.
- Figure/writing implication: In diagrams, show the observation as a new symbolic state, not free text.
- Priority: Medium.

### 20. Tree of Thoughts: Deliberate Problem Solving with Large Language Models

- Venue/year: NeurIPS 2023; arXiv 2023. Link: https://arxiv.org/abs/2305.10601
- Problem: Left-to-right token generation is weak for tasks requiring exploration, lookahead, and backtracking.
- Method mechanism: Search over coherent text units called thoughts, with self-evaluation and backtracking.
- Citable point for EGR: Reasoning needs search over intermediate units larger than tokens.
- EGR implication: EGR's next unit is not a thought string but an executable theorem model; search can be over symbolic states and theorem actions.
- Figure/writing implication: Use "from token to thought to theorem model" as a compact progression in related work.
- Priority: High.

### 21. Solving Math Word Problems by Combining Language Models With Symbolic Solvers

- Venue/year: arXiv 2023. Link: https://arxiv.org/abs/2304.09102
- Problem: PAL-style procedural code is less effective for declarative algebra problems.
- Method mechanism: Incrementally formalize word problems into variables and equations, then solve using a symbolic solver.
- Citable point for EGR: Declarative, incremental representations can be better interfaces to symbolic solvers than raw programs.
- EGR implication: Strong support for EGR's symbolic state representation and stepwise formal updates.
- Figure/writing implication: Cite in the section describing why `SymbolicState` should be explicit and persistent.
- Priority: High.

### 22. Logic-LM: Empowering Large Language Models with Symbolic Solvers for Faithful Logical Reasoning

- Venue/year: EMNLP 2023; arXiv 2023. Link: https://arxiv.org/abs/2305.12295
- Problem: LLMs often fail on complex logical reasoning even when they appear fluent.
- Method mechanism: Translate natural language to symbolic formulations, run deterministic symbolic solvers, and refine based on solver errors.
- Citable point for EGR: LLM-to-symbolic-solver pipelines improve faithfulness by shifting inference to deterministic solvers.
- EGR implication: EGR differs by repeatedly selecting executable theorem models under evolving states instead of one-shot translation to logic.
- Figure/writing implication: Put Logic-LM in the "semantic parser + solver" region of a related-work map.
- Priority: High.

### 23. LINC: A Neurosymbolic Approach for Logical Reasoning by Combining Language Models with First-Order Logic Provers

- Venue/year: arXiv 2023. Link: https://arxiv.org/abs/2310.15164
- Problem: Prompting-only logical reasoning fails in subtle and unpredictable ways.
- Method mechanism: Use the LLM as a semantic parser from natural language to first-order logic; use an external theorem prover for deduction.
- Citable point for EGR: LLM and symbolic prover failures are distinct and complementary; modular neurosymbolic reasoning can improve reliability.
- EGR implication: Supports an EGR claim that LLMs should guide structured reasoning, not carry the entire reasoning burden.
- Figure/writing implication: Use as a comparison against EGR's domain-specific theorem-model executor.
- Priority: High.

### 24. Intermediate Languages Matter: Formal Languages and LLMs affect Neurosymbolic Reasoning

- Venue/year: arXiv 2025. Link: https://arxiv.org/abs/2509.04083
- Problem: Neurosymbolic LLM pipelines depend heavily on the intermediate formal language, but this factor is often overlooked.
- Method mechanism: Compare multiple formal languages and LLMs across neurosymbolic reasoning datasets.
- Citable point for EGR: The representation interface between natural language, neural models, and symbolic solvers is a central design choice.
- EGR implication: Direct support for the dual representation design: `AbstractState` for neural prediction and `SymbolicState` for exact execution.
- Figure/writing implication: Add a small interface figure showing why EGR has two state views instead of one flat prompt.
- Priority: High.

## C. Formal Theorem Proving and Geometry Problem Solving

### 25. HOList: An Environment for Machine Learning of Higher Order Logic Theorem Proving

- Venue/year: ICML 2019, PMLR 97. Link: https://proceedings.mlr.press/v97/bansal19a.html
- Problem: Higher-order theorem proving is a challenging environment for learning-guided reasoning.
- Method mechanism: Provide a HOL Light based environment, benchmark, and DeepHOL theorem prover.
- Citable point for EGR: Theorem proving can be framed as learning to act in a formal proof environment.
- EGR implication: EGR is not a full higher-order prover, but it similarly treats reasoning as state/action transitions with learned guidance.
- Figure/writing implication: Compare proof-state/tactic transitions with EGR symbolic-state/theorem-model transitions.
- Priority: High.

### 26. Generative Language Modeling for Automated Theorem Proving

- Venue/year: arXiv 2020. Link: https://arxiv.org/abs/2009.03393
- Problem: Automated theorem provers need to generate useful proof steps and terms.
- Method mechanism: Use transformer language models for tactic/proof generation in Metamath.
- Citable point for EGR: LMs can guide formal proof search, and generated steps can be accepted or rejected by a formal environment.
- EGR implication: EGR adopts a similar proposal-validation separation but in conic-section problem solving rather than formal proof libraries.
- Figure/writing implication: Place under "LM-guided formal proof search".
- Priority: Medium.

### 27. Proof Artifact Co-training for Theorem Proving with Language Models

- Venue/year: arXiv 2021. Link: https://arxiv.org/abs/2102.06203
- Problem: Formal theorem proving has scarce tactic-level training data.
- Method mechanism: Extract self-supervised proof artifacts from Lean kernel proof terms and co-train with tactic prediction.
- Citable point for EGR: Intermediate proof artifacts can provide useful supervision beyond final theorem success.
- EGR implication: EGR trajectories can be treated as proof/problem-solving artifacts for selector training and process evaluation.
- Figure/writing implication: Use when discussing training-data construction from solver traces.
- Priority: Medium.

### 28. HyperTree Proof Search for Neural Theorem Proving

- Venue/year: NeurIPS 2022; arXiv 2022. Link: https://arxiv.org/abs/2205.11491
- Problem: Neural theorem provers need search and online learning to improve beyond supervised proof imitation.
- Method mechanism: Combine transformer proving with HyperTree Proof Search and online training.
- Citable point for EGR: Search over proof states and learning from failed/unfinished search improves theorem proving.
- EGR implication: Supports extending EGR from greedy selection to beam/search over theorem-model trajectories ranked by information gain.
- Figure/writing implication: Add optional search wrapper around the selector-applicator loop in a method figure.
- Priority: Medium.

### 29. Thor: Wielding Hammers to Integrate Language Models and Automated Theorem Provers

- Venue/year: NeurIPS 2022; arXiv 2022. Link: https://arxiv.org/abs/2205.10893
- Problem: Premise selection is crucial and difficult for language-model-based theorem proving.
- Method mechanism: Integrate LMs with automated theorem prover "hammers" for premise selection and proof search.
- Citable point for EGR: Hybrid systems can use symbolic provers for hard selection/execution components that LMs handle poorly.
- EGR implication: Theorem-model selection in EGR can be positioned as a domain-specific counterpart to premise/tactic selection.
- Figure/writing implication: Cite when explaining why selector accuracy is a meaningful metric.
- Priority: Medium.

### 30. Draft, Sketch, and Prove

- Venue/year: ICLR 2023; arXiv 2022. Link: https://arxiv.org/abs/2210.12283
- Problem: Formalizing mathematical proofs is difficult; pure proof search can be inefficient.
- Method mechanism: Convert informal proofs into formal proof sketches and use them to guide automated provers.
- Citable point for EGR: Informal LLM reasoning can be useful if converted into structured guidance for symbolic proof engines.
- EGR implication: LLM-produced conic solution sketches could be converted into theorem-model trajectories rather than trusted as final answers.
- Figure/writing implication: Use in the "LLM as guide, symbolic layer as executor/checker" paragraph.
- Priority: Medium.

### 31. LeanDojo: Theorem Proving with Retrieval-Augmented Language Models

- Venue/year: NeurIPS 2023; arXiv 2023. Link: https://arxiv.org/abs/2306.15626
- Problem: Formal theorem proving with LLMs is hard to reproduce and bottlenecked by premise selection.
- Method mechanism: Open-source Lean environment, benchmark, premise annotations, and ReProver with retrieval-augmented theorem proving.
- Citable point for EGR: Proof assistants expose programmatic proof environments and fine-grained premise/action data for learning.
- EGR implication: EGR should emphasize its programmatic theorem-model environment and trajectory-level data as a reproducible reasoning substrate.
- Figure/writing implication: Put LeanDojo in a comparison table: proof assistant environment vs conic theorem-action environment.
- Priority: High.

### 32. AlphaGeometry: Solving Olympiad Geometry without Human Demonstrations

- Venue/year: Nature 2024. Links: https://www.nature.com/articles/s41586-023-06747-5 and https://deepmind.google/blog/alphageometry-an-olympiad-level-ai-system-for-geometry/
- Problem: Olympiad geometry requires rigorous reasoning but has scarce human formal proof data.
- Method mechanism: A neural language model guides a symbolic deduction engine through branching points; training data are generated synthetically.
- Citable point for EGR: A neuro-symbolic geometry system can outperform prior symbolic-only approaches by letting neural prediction guide symbolic deduction.
- EGR implication: This is the closest high-profile ancestor for EGR. EGR should position itself as bringing state-conditioned theorem-model transitions to conic-section analytic geometry, where steps include equation recognition, parameter recovery, theorem application, algebraic execution, termination, and answer extraction.
- Figure/writing implication: Draw AlphaGeometry and EGR side by side: "predict construct + symbolic deduction" vs "predict theorem model + symbolic state transition".
- Priority: High.

### 33. AlphaGeometry2: Gold-medalist Performance in Solving Olympiad Geometry

- Venue/year: arXiv 2025. Link: https://arxiv.org/abs/2502.03544
- Problem: Original AlphaGeometry had limited language coverage and search coverage for broader Olympiad geometry.
- Method mechanism: Extend the geometry language, improve search, use Gemini architecture, share knowledge across search trees, and move toward natural-language input.
- Citable point for EGR: Geometry-specific formal languages, symbolic engines, and neural guidance scale when representation and search are carefully designed.
- EGR implication: Strong support for EGR's claim that conic-section reasoning needs a domain-specific state/action language rather than only generic LLM generation.
- Figure/writing implication: Use as evidence that formal representation coverage is a first-class issue.
- Priority: High.

### 34. Inter-GPS: Interpretable Geometry Problem Solving with Formal Language and Symbolic Reasoning

- Venue/year: ACL 2021; arXiv 2021. Link: https://arxiv.org/abs/2105.04165
- Problem: Geometry problem solving needs text/diagram understanding and symbolic reasoning with axiomatic knowledge.
- Method mechanism: Parse text and diagrams into formal language, incorporate theorem knowledge as conditional rules, use a theorem predictor to infer theorem application sequences for a symbolic solver.
- Citable point for EGR: Geometry solving benefits from explicit theorem knowledge, formal language, symbolic step reasoning, and theorem sequence prediction.
- EGR implication: This is a direct related-work anchor. EGR can differentiate by focusing on conic-section analytic geometry, dual state representation, executable theorem-model pool, entropy-guided continuation, and terminal extraction.
- Figure/writing implication: Use as the main predecessor in the conic/geometry solver comparison table.
- Priority: High.

### 35. TheoremQA: A Theorem-driven Question Answering Dataset

- Venue/year: EMNLP 2023; arXiv 2023. Link: https://arxiv.org/abs/2305.12524
- Problem: LLMs may solve basic math benchmarks but still struggle with domain-specific theorem application.
- Method mechanism: Curate 800 questions over 350 theorems across math, physics, EE/CS, and finance; evaluate LLM and code models with CoT/PoT.
- Citable point for EGR: Theorem application is a distinct capability beyond generic math QA.
- EGR implication: Supports presenting EGR's selector as theorem-model prediction, not just answer prediction or formula retrieval.
- Figure/writing implication: Cite in the introduction when motivating "selecting the right mathematical principle" as a key decision.
- Priority: High.

## D. Neuro-symbolic and Iterative Reasoning Frameworks

### 36. Neuro-Symbolic Visual Reasoning: Disentangling "Visual" from "Reasoning"

- Venue/year: ICML 2020, PMLR 119. Link: https://proceedings.mlr.press/v119/amizadeh20a.html
- Problem: VQA advances often improve perception rather than reasoning, making reasoning hard to assess in isolation.
- Method mechanism: Decouple visual perception from reasoning using differentiable first-order logic.
- Citable point for EGR: Decoupling subcomponents makes reasoning behavior more measurable and interpretable.
- EGR implication: Analogous to EGR's separation of theorem selection, symbolic execution, termination, and extraction.
- Figure/writing implication: Cite in the motivation for diagnostic process metrics.
- Priority: Medium.

### 37. Closed Loop Neural-Symbolic Learning via Integrating Neural Perception, Grammar Parsing, and Symbolic Reasoning

- Venue/year: ICML 2020, PMLR 119. Link: https://proceedings.mlr.press/v119/li20f.html
- Problem: Sparse rewards and missing symbolic error propagation slow neural-symbolic learning.
- Method mechanism: Use grammar as symbolic prior and a back-search algorithm to propagate errors through symbolic reasoning.
- Citable point for EGR: Closed-loop neural-symbolic systems benefit from explicit symbolic modules and feedback through reasoning steps.
- EGR implication: EGR should be described as a closed state-transition loop, not a one-shot module stack.
- Figure/writing implication: Add feedback arrows from applicator/terminal failure back to selector training or trajectory repair.
- Priority: Medium.

### 38. Scallop: A Language for Neurosymbolic Programming

- Venue/year: PLDI/OOPSLA line; arXiv 2023. Link: https://arxiv.org/abs/2304.04812
- Problem: Neurosymbolic applications need a language that combines flexible symbolic representation and trainable probabilistic reasoning.
- Method mechanism: Relational data model, Datalog-like logic programming, provenance semirings, and differentiable reasoning.
- Citable point for EGR: Symbolic representation language design affects data efficiency, interpretability, and generalization.
- EGR implication: EGR's theorem-model library can be described as a domain-specific neurosymbolic program rather than a collection of prompts.
- Figure/writing implication: Use when discussing representational design, not as a direct math solver baseline.
- Priority: Medium.

### 39. DOLPHIN: A Programmable Framework for Scalable Neurosymbolic Learning

- Venue/year: ICML 2025, PMLR 267. Link: https://proceedings.mlr.press/v267/naik25a.html
- Problem: Neurosymbolic learning struggles to scale to complex symbolic programs and large datasets.
- Method mechanism: Support neurosymbolic programs in Python, execute symbolic reasoning on CPU, and vectorize probabilistic computation/gradient propagation on GPU.
- Citable point for EGR: Practical neurosymbolic systems need scalable execution architectures, not only conceptual hybridization.
- EGR implication: If EGR grows beyond conic sections, execution scalability and vectorized selector training become important.
- Figure/writing implication: Mention in future-work/system scalability discussion.
- Priority: Background.

### 40. The CLRS Algorithmic Reasoning Benchmark

- Venue/year: ICML 2022, PMLR 162. Link: https://proceedings.mlr.press/v162/velickovic22a.html
- Problem: Algorithmic reasoning evaluation is fragmented and often task-specific.
- Method mechanism: Build a unified benchmark across classical algorithms with intermediate reasoning procedures.
- Citable point for EGR: Learning to execute algorithms is a recognized way to study reasoning beyond final outputs.
- EGR implication: Supports evaluating EGR not only by final answer accuracy but also by step/action/state trajectory quality.
- Figure/writing implication: Use when justifying process-level metrics and trajectory supervision.
- Priority: Medium.

## Reserve List for Later Expansion

These papers are not fully annotated above but may be useful in a second pass:

- FunSearch: program search with LLM-generated candidates and automatic evaluators. Useful for "LLM proposes, verifier evaluates" framing.
- NS-VQA: neural-symbolic VQA with explicit program execution. Useful for diagnostic interpretability analogies.
- DeepProbLog: probabilistic logic programming with neural predicates. Useful as background for differentiable neuro-symbolic reasoning.
- UniGeo: unified geometry problem solving. Useful for geometry solver baselines if the EGR experiments include diagram or geometry benchmarks.
- AlphaProof / IMO 2024 systems: useful if the introduction discusses recent frontier mathematical reasoning, but should be handled carefully because the target domain is formal proof rather than conic-section problem solving.

## High-Priority Reading Subset

For the next round of detailed reading and citation extraction, prioritize these 12:

1. Chain-of-Thought Prompting
2. Let's Verify Step by Step
3. Math-Shepherd
4. Premise-Augmented Reasoning Chains
5. PAL
6. Program of Thoughts
7. Tree of Thoughts
8. Solving Math Word Problems with Symbolic Solvers
9. Logic-LM
10. LeanDojo
11. AlphaGeometry
12. Inter-GPS
