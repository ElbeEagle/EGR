# EGR Related Work Synthesis v2

Last updated: 2026-07-09

Source: Zotero `AI4Math` -> `Math-Reasoning` and `Neuro-Symbolic`, 64 title-deduplicated top-level papers. This synthesis is organized by how the papers can serve EGR writing, not by publication year.

## 1. Current Mainstream Routes / 当前领域主流路线

| Route | Count in Zotero pool | What the route says | How EGR should respond |
|---|---:|---|---|
| LLM reasoning paths / 文本推理路径 | 7 | CoT variants, Tree/Markov reasoning, guided exploration, and multi-paradigm reasoning improve generated reasoning paths but keep the unit mostly textual. | EGR should say it changes the reasoning unit from text/thought to executable theorem-model transition. |
| Process supervision and verification / 过程监督与验证 | 10 | Step-level feedback, correction, verifiers, error classification, and metacognitive evaluation show final-answer accuracy is insufficient. | EGR should expose selection, applicability, execution, termination, and extraction as separate observable decisions. |
| Program/tool execution / 程序与工具执行 | 5 | PAL/PoT and tool-augmented systems show the value of delegating exact computation to executable tools. | EGR should differentiate theorem-model execution from arbitrary code or external tool calls. |
| Symbolic/formal execution / 符号与形式执行 | 11 | Logic/symbolic/code/formal-language systems show that LLM proposals become more reliable when checked by solvers or verifiers. | EGR should define each theorem model as precondition plus symbolic transition. |
| Formal state/action reasoning / 形式化 state-action 推理 | 3 | LeanDojo and formal-theorem work expose proof states, premise/tactic selection, and verified search. | EGR should borrow state/action/search language while staying conic-specific. |
| Geometry neuro-symbolic reasoning / 几何神经符号推理 | 3 | AlphaGeometry-style systems show neural guidance plus symbolic geometry deduction can solve hard geometry problems. | EGR should position conic sections as analytic-geometry theorem-action reasoning, not a toy domain. |
| Representation and NeSy frameworks / 表示与神经符号框架 | 10 | NeSy framework papers show that representation, interfaces, and integration principles determine reliability. | EGR should make its dual-state and selector/applicator boundary explicit. |
| Data, RL, scaling, benchmarks / 数据、强化学习、扩展与基准 | 14 | Data synthesis, post-training, reward modeling, and benchmarks improve or measure LLM math ability. | EGR should use them as baselines/context while emphasizing process controllability rather than only SOTA accuracy. |
| Prior work / 前序工作 | 1 | Prior text-diagram/function solvers explain the local lineage. | EGR should show continuity but separate its conic theorem-action contribution. |

## 2. EGR Positioning / EGR 应如何定位

CN: EGR 不应被写成“又一个提升数学准确率的 LLM 方法”，也不应被写成泛泛的 neuro-symbolic hybrid。更强的定位是：EGR 把数学解题的基本推理单元从 token/thought/program text 提升为 state-conditioned executable theorem-model transition。selector 解决“当前状态下下一步选择什么数学模型”，applicator 解决“该模型是否适用以及如何符号执行”，entropy/terminal extractor 解决“何时停止并如何从 terminal symbolic state 抽取答案”。

EN: EGR should not be framed as just another LLM method for higher math accuracy, nor as a generic neuro-symbolic hybrid. Its sharper position is to change the reasoning unit from token/thought/program text to state-conditioned executable theorem-model transition. The selector answers which mathematical model should be chosen under the current state; the applicator answers whether it is applicable and how it symbolically transforms the state; entropy and terminal extraction answer when to stop and how to ground the final answer in the terminal symbolic state.

Suggested slogan: `From next-token prediction to next-model transition.`

## 3. Which Papers Support Which EGR Claims / 论点-引用映射

### 3.1. Introduction: text-chain reasoning improves LLM math but leaves mathematical validity implicit.

- CN 用法: 用于避免空泛地说 “LLM 数学不好”；更准确的说法是：文本链式推理有帮助，但适用性、执行结果和终止条件仍隐含。
- EN use: Avoid the vague claim that LLMs are simply bad at math; instead say textual reasoning helps but leaves applicability, execution, and termination implicit.
- Candidate citations / 可用论文: 03 Active Prompting with Chain-of-Thought for Large Language Models; 05 Chain-of-Reasoning: Towards Unified Mathematical Reasoning in Large Language Models via a Multi-Paradigm Perspective; 17 Knowledge-Centered Dual-Process Reasoning for Math Word Problems With Large Language Models; 22 MARGE: Improving Math Reasoning with Guided Exploration; 24 Markov Chain of Thought for Efficient Mathematical Reasoning; 36 Specialized Mathematical Solving by a Step-By-Step Expression Chain Generation; 40 Tree of Thoughts: Deliberate Problem Solving with Large Language Models

### 3.2. Process-level reliability matters more than final answer accuracy alone.

- CN 用法: 用于支撑 selection accuracy、applicability rate、transition correctness、termination accuracy、extraction correctness 和 failure attribution。
- EN use: Use this to justify selection accuracy, applicability rate, transition correctness, termination accuracy, extraction correctness, and failure attribution.
- Candidate citations / 可用论文: 07 CogMath: Assessing LLMs’ Authentic Mathematical Ability from a Human Cognitive Perspective; 10 Enhancing Mathematical Reasoning in LLMs by Stepwise Correction; 11 Error Classification of Large Language Models on Math Word Problems: A Dynamically Adaptive Framework; 14 Forward-Backward Reasoning in Large Language Models for Mathematical Verification; 18 LLMs can Find Mathematical Reasoning Mistakes by Pedagogical Chain-of-Thought; 29 Metacognitive Capabilities of LLMs: An Exploration in Mathematical Problem Solving; 33 Premise-Augmented Reasoning Chains Improve Error Identification in Math reasoning with LLMs; 37 Step Guided Reasoning: Improving Mathematical Reasoning using Guidance Generation and Step Reasoning; 38 Step-KTO: Optimizing Mathematical Reasoning through Stepwise Binary Feedback; 39 Step-by-Step Correction of LLM-based Math Word Problems Solutions

### 3.3. Neural proposal and symbolic execution should be separated.

- CN 用法: 用于支撑 selector/applicator 分离，并与 PAL、PoT、Logic-LM、SymCode、NeuroProlog、symbolic solver 路线比较。
- EN use: Use this to motivate selector/applicator separation and compare EGR with PAL, PoT, Logic-LM, SymCode, NeuroProlog, and symbolic-solver routes.
- Candidate citations / 可用论文: 06 CoMAT: Chain of Mathematically Annotated Thought Improves Mathematical Reasoning; 08 Diverse Multi-tool Aggregation with Large Language Models for Enhanced Math Reasoning; 09 Empowering Multi-step Reasoning across Languages via Program-Aided Language Models; 12 FLAIR: Steering LLM Mathematical Problem Solving based on A Fuzzy-Logic-AssIsted Reasoner; 20 Learning to Reason Deductively: Math Word Problem Solving as Complex Relation Extraction; 21 Let's Reason Formally: Natural-Formal Hybrid Reasoning Enhances LLM's Math Capability; 23 MATHSENSEI: A Tool-Augmented Large Language Model for Mathematical Reasoning; 31 PAL: Program-aided Language Models; 34 Program of Thoughts Prompting: Disentangling Computation from Reasoning for Numerical Reasoning Tasks; 35 Safe: Enhancing Mathematical Reasoning in Large Language Models via Retrospective Step-aware Formal Verification; 47 AXIOM: A Trust-First Neuro-Symbolic Execution Architecture for Verifiable Mathematical Reasoning; 48 Advanced Weakly-Supervised Formula Exploration for Neuro-Symbolic Mathematical Reasoning

### 3.4. Mathematical reasoning can be modeled as state/action, premise/tactic, or theorem-model selection.

- CN 用法: 用于把 EGR 的 `P(M_t | S_t)` 与 proof state、premise/tactic selection、formal proof search 联系起来。
- EN use: Use this to connect EGR's `P(M_t | S_t)` with proof states, premise/tactic selection, and formal proof search.
- Candidate citations / 可用论文: 19 LeanDojo: Theorem Proving with Retrieval-Augmented Language Models; 32 Position: Formal Mathematical Reasoning—A New Frontier in AI; 55 Neural Theorem Proving: Generating and Structuring Proofs for Formal Verification

### 3.5. Representation and neural-symbolic interface design are core to reliable reasoning.

- CN 用法: 用于支撑 dual-state 设计：`AbstractState` 服务预测，`SymbolicState` 服务精确执行。
- EN use: Use this to defend the dual-state design: `AbstractState` for prediction and `SymbolicState` for exact execution.
- Candidate citations / 可用论文: 30 Neural-Symbolic Architectural Axioms of Integration: A Manifesto; 45 A Comparative Study of Neurosymbolic AI Approaches to Interpretable Logical Reasoning; 50 Evaluating Neuro-Symbolic AI Architectures: Design Principles, Qualitative Benchmark, Comparative Analysis and Results; 52 Improving Rule-based Reasoning in LLMs using Neurosymbolic Representations; 53 Intermediate Languages Matter: Formal Languages and LLMs affect Neurosymbolic Reasoning; 56 Neuro-Symbolic AI in 2024: A Systematic Review; 58 Ontology-Guided Neuro-Symbolic Inference: Grounding Language Models with Mathematical Domain Knowledge; 59 Rethinking Reasoning in LLMs: Neuro-Symbolic Local RetoMaton Beyond CoT and ICL; 63 Toward a Clearer Characterization of Neuro-Symbolic Frameworks: A Brief Comparative Analysis; 64 Towards Learning to Reason: Comparing LLMs With Neuro-Symbolic on Arithmetic Relations in Abstract Reasoning

### 3.6. Geometry and theorem proving validate state-conditioned neural-symbolic reasoning.

- CN 用法: 用于支撑 conic-section 不是 toy domain，而是结构化几何概念与符号代数执行交汇的验证场景。
- EN use: Use this to defend conic sections as a testbed where structured geometry meets symbolic algebraic execution.
- Candidate citations / 可用论文: 46 A Neuro-Symbolic Approach for Reliable Proof Generation with LLMs: A Case Study in Euclidean Geometry; 51 Gold-medalist Performance in Solving Olympiad Geometry with AlphaGeometry2; 61 Solving olympiad geometry without human demonstrations

### 3.7. Data/RL/reward/tool systems inform baselines and ablations.

- CN 用法: 用于实验设计，但不要让 EGR 的主贡献变成单纯追求 accuracy。
- EN use: Use this for experimental design while keeping EGR's contribution process-oriented rather than accuracy-only.
- Candidate citations / 可用论文: 02 AceMath: Advancing Frontier Math Reasoning with Post-Training and Reward Modeling; 04 Augmenting Math Word Problems via Iterative Question Composing; 13 Fewer is More: Boosting Math Reasoning with Reinforced Context Pruning; 15 GRPO-LEAD: A Difficulty-Aware Reinforcement Learning Approach for Concise Mathematical Reasoning in Language Models; 16 Key-Point-Driven Data Synthesis with Its Enhancement on Mathematical Reasoning; 25 MathFusion: Enhancing Mathematical Problem-solving of LLM through Instruction Fusion; 28 MetaMath: Bootstrap Your Own Mathematical Questions for Large Language Models; 42 What Do Learning Dynamics Reveal About Generalization in LLM Mathematical Reasoning?; 43 WizardMath: Empowering Mathematical Reasoning for Large Language Models via Reinforced Evol-Instruct; 44 rStar-Math: Small LLMs Can Master Math Reasoning with Self-Evolved Deep Thinking

### 3.8. Surveys and position papers define terminology and field context.

- CN 用法: 用于 Related Work 开头，建立审稿人熟悉的领域路线图。
- EN use: Use this in Related Work openings to establish a reviewer-familiar map of the field.
- Candidate citations / 可用论文: 01 A Survey of Mathematical Reasoning in the Era of Multimodal Large Language Model: Benchmark, Method & Challenges; 26 Measuring Mathematical Problem Solving With the MATH Dataset; 27 Measuring Multimodal Mathematical Reasoning with MATH-Vision Dataset; 49 Artificial Intelligence for Mathematical Reasoning: An Integrated Survey of Language Models, Neuro-symbolic Systems, and Verified Discovery

### 3.9. Prior text-diagram/function solvers clarify continuity and novelty.

- CN 用法: 用于说明 EGR 与前序工作的连续性，但必须明确新贡献是 conic-specific theorem-action transition。
- EN use: Use this to show continuity with prior work while making clear that EGR's new contribution is conic-specific theorem-action transition.
- Candidate citations / 可用论文: 41 UDfSolver : Uniform representation and decoupled inference strategy for text-diagram function problems solving

## 4. Reverse Organization by EGR Paper Structure / 按 EGR 论文结构反向整理

### 4.1 Introduction / 引言

Use benchmark/survey papers, CoT/path-search papers, process-supervision papers, and symbolic/formal-execution papers to support three claims: math reasoning remains structurally hard; intermediate reasoning matters; and free-form text steps are insufficiently checkable.

CN draft: 近年来，CoT、路径搜索、过程监督、奖励模型和数学专用后训练显著提升了 LLM 数学推理能力。然而，这些方法大多仍把推理过程表示为自然语言 token 序列、thought 字符串、程序片段或一次性符号翻译。相关评测与过程监督研究表明，最终答案正确率并不能揭示推理失败来自数学原理选择、符号执行、终止判断还是答案抽取。EGR 因此将圆锥曲线求解重构为当前状态条件下的 theorem-model prediction and execution。

EN draft: Recent work on CoT-style prompting, reasoning-path search, process supervision, reward modeling, and math-specific post-training has substantially improved LLM mathematical reasoning. However, most methods still represent reasoning as natural-language token sequences, thought strings, program fragments, or one-shot symbolic translations. Evaluation and process-supervision studies show that final-answer accuracy alone cannot identify whether a failure comes from mathematical principle selection, symbolic execution, termination, or answer extraction. EGR therefore reformulates conic-section solving as theorem-model prediction and execution conditioned on the current problem state.

### 4.2 Related Work / 相关工作

Organize by route, not chronology: LLM reasoning paths; process supervision and verification; program/tool execution; symbolic/formal execution; formal theorem proving and geometry; neuro-symbolic representation frameworks. End each subsection with the precise limitation that EGR addresses.

CN draft: 与 PAL/PoT 等程序增强方法相比，EGR 的执行单元不是任意代码，而是带有前置条件和状态转移函数的 theorem model。与 Logic-LM、SymCode、NeuroProlog 等符号执行方法相比，EGR 不是一次性翻译为外部形式，而是在求解过程中反复进行 state-conditioned theorem-model transition。与 LeanDojo、AlphaGeometry 等形式化/几何推理系统相比，EGR 面向圆锥曲线解析几何问题，将定理选择、代数执行、状态熵控制和 terminal extraction 放在同一个可检查求解循环中。

EN draft: Compared with program-augmented methods such as PAL and PoT, EGR does not execute arbitrary code; it executes theorem models with explicit preconditions and state-transition functions. Compared with symbolic-execution methods such as Logic-LM, SymCode, and NeuroProlog, EGR is not a one-shot translation into an external formalism; it repeatedly performs state-conditioned theorem-model transitions during solving. Compared with formal or geometry reasoning systems such as LeanDojo and AlphaGeometry, EGR targets conic-section analytic geometry, where theorem selection, algebraic execution, entropy-based continuation, and terminal extraction are integrated into one checkable solving loop.

### 4.3 Method Motivation / 方法动机

Use process-supervision and symbolic-execution papers to justify four decompositions: selector vs executor, abstract state vs symbolic state, transition vs text, terminal extraction vs answer generation.

- `P(M_t | S_t)` is a theorem-model policy, not an answer predictor.
- `can_apply/apply` is the mathematical validity gate, not a post-hoc verifier.
- `H(S)` estimates residual solving burden/continuation need, not final correctness probability.
- Terminal extraction grounds the answer in the symbolic state, rather than trusting generated text.

### 4.4 Experiments / 实验

- Baselines: direct LLM, CoT/path-search, PAL/PoT-like execution, tool-augmented math systems, symbolic-solver systems, formal/symbolic verifier systems where applicable, and rule-only theorem search.
- Ablations: no applicator, no entropy/continuation control, no terminal extractor, no dual-state representation, greedy selector vs search/reranking.
- Metrics: final answer accuracy, theorem-model selection accuracy, applicability rate, transition correctness, trajectory success, termination accuracy, extraction correctness, information gain, and failure attribution.
- Diagnostics: use process-supervision papers to justify why transition-level metrics should appear before or alongside final answer tables.

### 4.5 Figures / 图设计

Figure 1: Paradigm contrast. Left: `Problem -> generated reasoning text -> answer`. Right: `S_t -> predict M_t -> can_apply/apply -> S_{t+1} -> terminal extraction`.

Figure 2: Related-work map. X-axis: text-only generation to executable symbolic grounding. Y-axis: final-answer supervision to explicit process/state supervision. Place CoT/Tree on upper-left, PAL/PoT/tool systems on lower-right, Logic-LM/SymCode/NeuroProlog/LeanDojo/AlphaGeometry/EGR on upper-right.

Figure 3: EGR step anatomy. Show `AbstractState`, selector, theorem-model pool, `SymbolicState`, applicator, entropy delta, and terminal extractor.

Figure 4: Error taxonomy. Rows: selection, applicability, execution, termination, extraction. Columns: hidden in LLM text, observable in EGR trace, measurable metric, repair signal.

Figure 5: Conic-section testbed. Show how curve type, parameters, foci/directrices/eccentricity/tangent/asymptote/intersection facts enter symbolic state and condition theorem-model applicability.

## 5. Related Work Paragraphs Ready to Adapt / 可直接改写进论文的段落

### Paragraph A: LLM reasoning paths

EN: Chain-of-thought and its variants show that exposing intermediate reasoning improves LLM performance on mathematical tasks. Subsequent work explores active exemplar selection, multi-path search, Markov-style reasoning, guided exploration, and multi-paradigm reasoning. These methods demonstrate the value of intermediate reasoning units, but the units remain largely unconstrained text or thought strings. EGR takes a different step: each intermediate unit is an executable theorem model whose applicability and symbolic effect are defined with respect to the current problem state.

CN: CoT 及其变体表明，显式中间推理可以提升 LLM 在数学任务上的表现。后续工作进一步探索主动样例选择、多路径搜索、Markov 式推理、引导式探索和多范式推理。这些方法说明“中间推理单元”很重要，但这些单元大多仍是非约束的文本或 thought 字符串。EGR 的关键转向是：每个中间单元都是可执行 theorem model，其适用条件和符号效果都由当前问题状态决定。

### Paragraph B: Process supervision

EN: Process-supervision and verification studies show that final-answer correctness is too coarse for diagnosing mathematical reasoning. Step-level feedback, error classification, correction, and metacognitive evaluation all improve or reveal failures in generated reasoning paths. EGR operationalizes this process view at the mathematical-action level: it separately exposes theorem-model selection, applicability checking, symbolic transition, termination, and terminal extraction.

CN: 过程监督与验证相关研究表明，最终答案正确率过于粗糙，无法诊断数学推理过程。步骤级反馈、错误分类、纠错和元认知评测都能改进或揭示生成推理路径中的失败。EGR 将这种过程视角落实到数学 action 层面：分别暴露 theorem-model selection、applicability checking、symbolic transition、termination 和 terminal extraction。

### Paragraph C: Symbolic execution

EN: Program-aided and symbolic-solver-augmented methods delegate computation or deduction to external executable systems, improving reliability over pure prose reasoning. However, program text and one-shot symbolic translations do not fully capture the state-dependent theorem choices in conic-section solving. EGR therefore uses a theorem-model pool: each model specifies preconditions and a symbolic state-transition function, allowing the solver to predict and execute mathematical actions step by step.

CN: 程序增强和符号求解器增强方法把计算或演绎交给外部可执行系统，比纯文本推理更可靠。然而，程序文本或一次性符号翻译并不能充分刻画圆锥曲线求解中状态依赖的定理选择。EGR 因此使用 theorem-model pool：每个 model 都规定前置条件和符号状态转移函数，使求解器能够逐步预测并执行数学 action。

### Paragraph D: Geometry and formal reasoning

EN: Formal theorem proving and neuro-symbolic geometry systems show that learned models can guide symbolic reasoning in structured mathematical environments. LeanDojo and related work expose proof states and premise/tactic choices, while AlphaGeometry demonstrates the power of neural guidance plus symbolic deduction in geometry. EGR follows this state/action view but targets conic-section analytic geometry, where reliable solving requires theorem selection, algebraic transformation, progress estimation, and answer extraction over an evolving symbolic state.

CN: 形式化定理证明和神经符号几何系统说明，学习模型可以在结构化数学环境中指导符号推理。LeanDojo 等工作暴露 proof state 与 premise/tactic 选择，AlphaGeometry 则展示了神经指导与符号演绎结合在几何中的效果。EGR 延续这种 state/action 视角，但面向圆锥曲线解析几何：可靠求解需要在演化的符号状态上完成定理选择、代数变换、进度估计和答案抽取。

## 6. Immediate Revision Checklist / 立即修改清单

- Introduction: add the slogan `From next-token prediction to next-model transition`.
- Related Work: use the route-based structure above instead of a chronological list.
- Method: define theorem model as `precondition + symbolic transition`, not as a formula label.
- Experiments: add process-level metrics before the final accuracy table or immediately after it.
- Figures: draw the EGR step anatomy and related-work map before polishing low-level module diagrams.
- Claim boundary: do not claim EGR is a general theorem prover; claim it is a domain-specific executable neural-symbolic framework for conic-section problem solving.
