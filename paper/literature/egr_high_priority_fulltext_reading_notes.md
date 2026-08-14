# EGR High-Priority Fulltext Reading Notes

Last updated: 2026-07-09

Source: Zotero My Library -> `AI4Math` -> `Math-Reasoning` and `Neuro-Symbolic`.

Method: I used Zotero local API fulltext index for the 31 papers in the high-priority reading queue. All 31 papers had indexed full text available. This document is a first fulltext-index-based close reading pass: it summarizes each paper's assumptions, core work, claims, main results, and value for EGR writing. It does not copy long passages from the papers.

EGR lens:

> Reliable mathematical reasoning should be modeled as state-conditioned theorem-model prediction and executable symbolic state transition, with process-level diagnostics for selection, applicability, execution, termination, and extraction.

## 1. Overall Synthesis / 总体结论

### CN

这 31 篇高优先级论文共同支撑了 EGR 的五个关键叙事：

1. **最终答案准确率不够**：CogMath、StepCo、Error Classification、PARC、Step-KTO 等工作都说明，数学推理需要过程级诊断，不能只看 final answer accuracy。
2. **文本推理链不等于可靠数学推理**：CoMAT、Tree of Thoughts、PedCoT、Safe 等工作都承认 CoT 有用，但其步骤仍可能不忠实、不可验证或难以定位错误。
3. **神经生成与符号执行应分工**：PAL、PoT、MATHSENSEI、Logic-LM、SymCode、NeuroProlog、AXIOM 都把 LLM 从“独立求解器”降为“生成/规范化/选择模块”，把执行交给程序、CAS、solver、Prolog 或 formal verifier。
4. **数学推理可以被建模为状态/动作/搜索过程**：LeanDojo、Neural Theorem Proving、AlphaGeometry、AlphaGeometry2 都支持把数学推理看作 proof state 或 geometric state 上的 action selection/search。
5. **表示接口是核心贡献，不是工程细节**：Intermediate Languages Matter、Logic-LM、Declarative MWP Solver、UDfSolver 等工作都说明，中间语言、状态表示、符号接口会显著影响推理可靠性。

对 EGR 来说，最强的借鉴不是“再做一个更强的 LLM 数学模型”，而是把这些路线收束为一句话：

> EGR replaces unconstrained reasoning text with state-conditioned executable theorem-model transitions.

### EN

The 31 high-priority papers support five key narratives for EGR:

1. **Final-answer accuracy is insufficient**: CogMath, StepCo, Error Classification, PARC, Step-KTO, and related works show that mathematical reasoning needs process-level diagnostics.
2. **Textual reasoning chains are not reliable mathematical reasoning**: CoMAT, Tree of Thoughts, PedCoT, and Safe recognize that CoT helps, but its steps may remain unfaithful, unverifiable, or hard to localize.
3. **Neural generation and symbolic execution should be separated**: PAL, PoT, MATHSENSEI, Logic-LM, SymCode, NeuroProlog, and AXIOM turn LLMs into generators, canonicalizers, or selectors, while execution is delegated to programs, CAS, solvers, Prolog, or formal verifiers.
4. **Mathematical reasoning can be modeled as state/action/search**: LeanDojo, Neural Theorem Proving, AlphaGeometry, and AlphaGeometry2 support viewing reasoning as action selection or search over proof/geometric states.
5. **Representation is a central contribution**: Intermediate Languages Matter, Logic-LM, the declarative MWP solver, and UDfSolver all show that the intermediate language, state representation, and symbolic interface strongly affect reliability.

For EGR, the most useful synthesis is not to build "another stronger math LLM", but to make a sharper paradigm claim:

> EGR replaces unconstrained reasoning text with state-conditioned executable theorem-model transitions.

## 2. Per-Paper Reading Notes / 逐篇精读笔记

### 01. CoMAT: Chain of Mathematically Annotated Thought Improves Mathematical Reasoning

Fulltext source: Zotero key `XW3KDRD4`; indexed full text about 87k characters.

- Premise / 前提假设:
  CN: CoT 能提升数学推理，但自然语言推理链可能不忠实、含混，最终答案未必从中间步骤逻辑推出。符号化中间表达可以减少这种含混性。
  EN: CoT improves math reasoning, but natural-language reasoning chains can be unfaithful or ambiguous. Symbolic intermediate representation can reduce that ambiguity.
- Core work / 核心工作:
  CN: 提出 CoMAT，将数学推理拆成 Symbolic Conversion 和 Reasoning Execution 两阶段；不依赖外部 solver，而是在 LLM 内完成符号化和执行。
  EN: CoMAT decomposes reasoning into Symbolic Conversion and Reasoning Execution, keeping symbolic reasoning inside the LLM rather than using an external solver.
- Core claim / 核心论点:
  CN: 数学推理需要比自然语言 CoT 更结构化的中间表示；符号化思维链能提高 faithfulness 和 verifiability。
  EN: Mathematical reasoning needs more structured intermediate representations than natural-language CoT; mathematically annotated thoughts improve faithfulness and verifiability.
- Main results / 主要结果:
  CN: 在多模型、多语言、多数据集上优于传统 CoT；全文索引中报告 MMLU-Redux(MATH) 和 GaoKao MCQ 等任务有数个百分点提升。
  EN: It outperforms traditional CoT across several models, languages, and benchmarks, with reported gains on MMLU-Redux(MATH), GaoKao MCQ, and other tasks.
- EGR value / 对 EGR 的价值:
  CN: 可支撑 EGR 的“文本 thought 不够，数学中间单元需要结构化”论点。但 EGR 要进一步强调：CoMAT 仍是 LLM 内部符号化，EGR 是外部可执行 theorem-model transition。
  EN: It supports EGR's claim that textual thoughts are insufficient. EGR should go further by stressing that its intermediate unit is not internal symbolic prose, but an externally executable theorem-model transition.

### 02. CogMath: Assessing LLMs' Authentic Mathematical Ability from a Human Cognitive Perspective

Fulltext source: Zotero key `NQIJFS82`; indexed full text about 85k characters.

- Premise / 前提假设:
  CN: 仅用总体答案准确率衡量 LLM 数学能力会高估模型能力，因为模型可能在理解、求解或总结阶段隐藏失败。
  EN: Overall answer accuracy overestimates LLM mathematical ability because failures can occur in comprehension, solving, or summarization stages.
- Core work / 核心工作:
  CN: 构建 CogMath，从人类认知视角把数学推理拆成 problem comprehension、problem solving、solution summarization 三阶段和九个细粒度维度。
  EN: CogMath evaluates mathematical ability through three cognitive stages and nine fine-grained dimensions.
- Core claim / 核心论点:
  CN: 数学能力必须被拆成多个阶段和维度评估，不能只看最终答案。
  EN: Mathematical ability must be evaluated across multiple stages and dimensions, not only final answers.
- Main results / 主要结果:
  CN: 在三个 benchmark 上，七个主流 LLM 的数学能力被约 30%-40% 高估；CoT/ICL 未必真正提升数学能力本身。
  EN: Across three benchmarks, seven mainstream LLMs are reported to be overestimated by about 30%-40%; CoT/ICL do not necessarily improve authentic mathematical proficiency.
- EGR value / 对 EGR 的价值:
  CN: 强力支撑 EGR 的 process-level evaluation：selection、execution、termination、extraction 应分别评估。
  EN: Strong support for EGR's process-level evaluation: selection, execution, termination, and extraction should be measured separately.

### 03. Enhancing Mathematical Reasoning in LLMs by Stepwise Correction

Fulltext source: Zotero key `59SU9ZNS`; indexed full text about 101k characters.

- Premise / 前提假设:
  CN: Best-of-N 只是重复采样并评分，可能重复相同错误；真正需要的是识别错误步骤并修正。
  EN: Best-of-N sampling can repeat the same mistakes; reliable reasoning requires identifying and revising incorrect steps.
- Core work / 核心工作:
  CN: 提出 StepCo，在验证和修订之间迭代，用 process-supervised verifier 找出错误步骤并指导 LLM 修正。
  EN: StepCo alternates verification and revision using a process-supervised verifier to locate and revise erroneous steps.
- Core claim / 核心论点:
  CN: 数学推理改进应从“选择一条完整路径”转向“定位并修复局部错误步骤”。
  EN: Math reasoning improvement should shift from selecting a whole path to localizing and repairing erroneous steps.
- Main results / 主要结果:
  CN: 使用 GPT-4o 时，StepCo 在八个数据集平均达到 94.1% accuracy，比 Best-of-N 高 2.4 点，并减少 77.8% token 消耗。
  EN: With GPT-4o, StepCo reports 94.1 average accuracy across eight datasets, +2.4 over Best-of-N, with 77.8% fewer tokens.
- EGR value / 对 EGR 的价值:
  CN: 支撑 EGR 的“错误应定位到 transition level”论点。EGR 可把 repair signal 设计为：选错 model、不可 apply、执行错误、终止错误。
  EN: Supports transition-level failure localization. EGR can define repair signals for wrong model selection, failed applicability, wrong execution, and wrong termination.

### 04. Error Classification of Large Language Models on Math Word Problems

Fulltext source: Zotero key `X67RQWLU`; indexed full text about 102k characters.

- Premise / 前提假设:
  CN: 只提高 accuracy 会忽略错误模式；静态错误分类无法覆盖模型能力提升后出现的新错误。
  EN: Improving accuracy alone ignores error patterns; static error taxonomies cannot capture evolving failures as models improve.
- Core work / 核心工作:
  CN: 构建 MWPES-300K，覆盖 15 个 LLM、4 个 MWP 数据集、304,865 个错误样本，并提出动态自适应错误分类框架。
  EN: The paper builds MWPES-300K with 304,865 error samples across 15 LLMs and four MWP datasets, and proposes a dynamic error classification framework.
- Core claim / 核心论点:
  CN: 错误类型随数据集复杂度和模型能力变化而变化，错误分析本身应动态更新。
  EN: Error patterns evolve with dataset complexity and model capability, so error analysis should be dynamically updated.
- Main results / 主要结果:
  CN: 发现数据集特征显著影响错误模式；基于错误模式的 Error-Aware Prompting 可提升数学推理表现。
  EN: Dataset characteristics shape error patterns; Error-Aware Prompting improves reasoning by incorporating common error patterns.
- EGR value / 对 EGR 的价值:
  CN: 可支撑 EGR 的 failure attribution 表：selection / applicability / execution / termination / extraction 不是装饰，而是必要诊断结构。
  EN: Supports EGR's failure-attribution table: selection, applicability, execution, termination, and extraction are necessary diagnostic categories.

### 05. FLAIR: Steering LLM Mathematical Problem Solving based on A Fuzzy-Logic-AssIsted Reasoner

Fulltext source: Zotero key `NMI988FA`; indexed full text about 99k characters.

- Premise / 前提假设:
  CN: 固定推理策略或静态 heuristic 无法适应不同中间状态；数学求解需要根据当前状态动态选择后续动作。
  EN: Fixed reasoning strategies cannot adapt to different intermediate states; math solving requires state-conditioned action choice.
- Core work / 核心工作:
  CN: 用 fuzzy memberships 描述中间状态，用参数化 fuzzy rules 激活后续 actions，并用 RL 调整规则参数。
  EN: FLAIR characterizes intermediate states with fuzzy memberships, activates actions through parameterized fuzzy rules, and tunes rules with RL.
- Core claim / 核心论点:
  CN: 数学推理可被写成 generation-verification-revision 的闭环控制过程。
  EN: Mathematical reasoning can be framed as a generation-verification-revision control loop over intermediate states.
- Main results / 主要结果:
  CN: 全文强调 adaptive state-aware reasoning 相比固定策略更有效；具体增益依赖模型和数据集。
  EN: The paper argues that adaptive state-aware reasoning improves over fixed strategies, with gains varying by model and dataset.
- EGR value / 对 EGR 的价值:
  CN: FLAIR 对 EGR 最有价值的是叙事结构：closed-loop controller。EGR 不需要模仿 fuzzy logic，而应强调 selector/applicator/entropy 的闭环控制。
  EN: Its value for EGR is the closed-loop controller narrative. EGR need not imitate fuzzy logic; it should highlight selector/applicator/entropy as a closed reasoning loop.

### 06. Forward-Backward Reasoning in LLMs for Mathematical Verification

Fulltext source: Zotero key `A53BDS2C`; indexed full text about 67k characters.

- Premise / 前提假设:
  CN: 只用 forward reasoning 选择答案会饱和；候选答案还应通过反向一致性检查。
  EN: Forward reasoning alone saturates; candidate answers should also be checked by backward consistency.
- Core work / 核心工作:
  CN: 提出 FOBAR：给定候选答案后，遮盖题目中的一个数，让 LLM 反推该数，并结合 forward/backward reasoning 进行验证。
  EN: FOBAR masks a number in the question and asks the LLM to infer it given a candidate answer, combining forward and backward reasoning.
- Core claim / 核心论点:
  CN: 数学答案的可靠性可以通过反向约束验证增强。
  EN: Mathematical answer reliability can be improved through backward constraint verification.
- Main results / 主要结果:
  CN: 在六个数学数据集和三个 LLM 上优于 Self-Consistency 和 Self-Verification。
  EN: It outperforms Self-Consistency and Self-Verification on six math datasets and three LLMs.
- EGR value / 对 EGR 的价值:
  CN: 支撑 EGR 的 terminal extraction / answer verification：终态不只生成答案，还应能反向满足原始条件。
  EN: Supports EGR's terminal extraction and answer verification: terminal answers should be checked against original constraints.

### 07. LLMs can Find Mathematical Reasoning Mistakes by Pedagogical Chain-of-Thought

Fulltext source: Zotero key `P993QP49`; indexed full text about 58k characters.

- Premise / 前提假设:
  CN: LLM 自纠错的前提是能发现错误；简单 prompting 下，LLM 对数学推理错误的识别不稳定。
  EN: Self-correction requires mistake detection, but simple prompting is unreliable for detecting math reasoning mistakes.
- Core work / 核心工作:
  CN: 提出 Pedagogical Chain-of-Thought，用教学原则设计 prompts、多阶段交互和评分机制，引导模型识别数学推理错误。
  EN: PedCoT uses pedagogical prompt principles, multi-stage interaction, and grading to guide mistake detection.
- Core claim / 核心论点:
  CN: 错误检测需要明确的检查结构，而不是泛泛要求模型“检查一下”。
  EN: Mistake detection requires structured checking, not a vague request to "check your answer".
- Main results / 主要结果:
  CN: 全文索引显示该方法在数学错误识别任务中优于简单 prompting，并强调教育式分解对 mistake localization 的价值。
  EN: The fulltext indicates that PedCoT improves mathematical mistake detection over simple prompting and highlights pedagogical decomposition.
- EGR value / 对 EGR 的价值:
  CN: 可支持 EGR 的 trace diagnosis：每个 theorem-model transition 都应有可检查依据，而不是依赖 LLM 自我反思。
  EN: Supports EGR's trace diagnosis: each theorem-model transition should expose checkable grounds, instead of relying on generic LLM reflection.

### 08. LeanDojo: Theorem Proving with Retrieval-Augmented Language Models

Fulltext source: Zotero key `NDL89MZG`; indexed full text about 113k characters.

- Premise / 前提假设:
  CN: 形式化定理证明需要在 proof state 下选择 premise/tactic；LLM 需要可交互、可复现的 theorem-proving 环境。
  EN: Formal theorem proving requires premise/tactic choices under proof states; LLMs need an interactive, reproducible proving environment.
- Core work / 核心工作:
  CN: 构建 LeanDojo，提供 Lean 环境、数据、premise annotation，并提出 retrieval-augmented prover ReProver。
  EN: LeanDojo provides a Lean environment, data, premise annotations, and retrieval-augmented prover ReProver.
- Core claim / 核心论点:
  CN: 检索相关 premise 并在 proof state 中生成 tactic，是 LLM theorem proving 的关键。
  EN: Retrieving relevant premises and generating tactics under proof states is central to LLM theorem proving.
- Main results / 主要结果:
  CN: 全文强调 ReProver 在 Lean theorem proving 上提升 proof search 能力，并提升可复现性。
  EN: The paper reports improved proof search in Lean and emphasizes reproducibility for theorem-proving research.
- EGR value / 对 EGR 的价值:
  CN: 可支撑 EGR 的 `P(M_t | S_t)`：selector 与 theorem/premise/tactic selection 属于同一类 state-conditioned action policy。
  EN: Supports EGR's `P(M_t | S_t)`: the selector is a state-conditioned action policy analogous to premise/tactic selection.

### 09. Let's Reason Formally: Natural-Formal Hybrid Reasoning Enhances LLM's Math Capability

Fulltext source: Zotero key `UMFBQ2IA`; indexed full text about 78k characters.

- Premise / 前提假设:
  CN: 纯自然语言推理和纯形式语言推理各有瓶颈；RL 难以补足 base model 中缺乏的形式化知识。
  EN: Pure natural-language and pure formal-language reasoning have different bottlenecks; RL may not inject missing formal knowledge into a base model.
- Core work / 核心工作:
  CN: 提出 NFL-HR，将自然语言 QA 问题对齐为形式语言中的 existence theorem，并用 formal reasoner 和 answer extraction 连接输入/输出格式。
  EN: NFL-HR aligns natural-language QA problems with existence theorems in formal language, uses a formal reasoner, and extracts answers back.
- Core claim / 核心论点:
  CN: 自然语言数学推理可以通过形式语言专家知识增强，但关键是处理 NL-FL 输入/输出格式鸿沟。
  EN: Natural-language math reasoning can be enhanced by formal-language expertise, but the key is bridging NL-FL format gaps.
- Main results / 主要结果:
  CN: 在 MATH-500 和 AMC 上分别达到 89.80% 和 84.34%，比 NL baseline 高约 4.6 和 4.82 个百分点。
  EN: Reports 89.80% on MATH-500 and 84.34% on AMC, improving over the NL baseline by about 4.60 and 4.82 points.
- EGR value / 对 EGR 的价值:
  CN: 支撑 EGR 的 dual-interface 设计：自然语言问题需要转成可执行的中间状态，但答案还要回到原问题查询。
  EN: Supports EGR's dual-interface design: natural-language problems need executable intermediate states, and final answers must map back to the query.

### 10. MATHSENSEI: A Tool-Augmented Large Language Model for Mathematical Reasoning

Fulltext source: Zotero key `QYD82P5Z`; indexed full text about 82k characters.

- Premise / 前提假设:
  CN: 复杂数学题常需要外部知识、程序执行和符号方程求解；不同工具的组合和顺序会影响结果。
  EN: Complex math problems require external knowledge, program execution, and symbolic equation solving; tool combinations and sequences matter.
- Core work / 核心工作:
  CN: 构建 MATHSENSEI，组合知识检索、Python 生成/执行、代码修正、WolframAlpha 和 solution generator。
  EN: MATHSENSEI combines knowledge retrieval, Python generation/execution, code refinement, WolframAlpha, and solution generation.
- Core claim / 核心论点:
  CN: tool-augmented LLM 对复杂数学更有价值，且题目越复杂、知识需求越高，工具收益越明显。
  EN: Tool-augmented LLMs are more valuable for complex math; tool benefits grow with problem complexity and knowledge demands.
- Main results / 主要结果:
  CN: 在 MATH 上比 GPT-3.5-turbo + CoT 高 13.5%；对简单 GSM8K 收益较小，对复杂任务收益更大。
  EN: Reports 13.5% improvement over GPT-3.5-turbo + CoT on MATH; benefits are smaller on GSM8K and larger on complex tasks.
- EGR value / 对 EGR 的价值:
  CN: 可作为 EGR baseline 类别：tool-augmented LLM。EGR 应强调自己不是多工具拼接，而是定理模型 action space。
  EN: Useful as a baseline family. EGR should emphasize that it is not generic tool chaining, but a theorem-model action space.

### 11. Measuring Mathematical Problem Solving With the MATH Dataset

Fulltext source: Zotero key `DLPVE96H`; indexed full text about 85k characters.

- Premise / 前提假设:
  CN: 数学问题求解是衡量 problem-solving 能力的重要场景，不同于简单 plug-and-chug 计算。
  EN: Mathematical problem solving is a key testbed for problem-solving ability, distinct from plug-and-chug calculation.
- Core work / 核心工作:
  CN: 提出 MATH 数据集，包含 12,500 个竞赛级数学题和 step-by-step solutions，并提供 AMPS 预训练语料。
  EN: Introduces MATH with 12,500 competition-level problems and step-by-step solutions, plus AMPS pretraining data.
- Core claim / 核心论点:
  CN: 仅靠扩大 Transformer 规模不足以解决高难数学推理，需要新的算法突破。
  EN: Scaling Transformers alone is insufficient for difficult mathematical reasoning; algorithmic advances are needed.
- Main results / 主要结果:
  CN: 即使大模型和数学预训练能提升表现，MATH accuracy 仍较低；论文明确指出 scaling is not currently solving MATH。
  EN: Even with large models and math pretraining, accuracy remains low; the paper argues that scaling is not currently solving MATH.
- EGR value / 对 EGR 的价值:
  CN: 强力支撑 EGR 的选题动机：数学推理需要结构化算法，而不是只靠大模型 scale。
  EN: Strong motivation for EGR: math reasoning needs structured algorithms beyond model scaling.

### 12. Metacognitive Capabilities of LLMs: An Exploration in Mathematical Problem Solving

Fulltext source: Zotero key `WSNF4XPK`; indexed full text about 115k characters.

- Premise / 前提假设:
  CN: LLM 可能具有某种“元认知知识”，即能识别题目需要哪些技能/步骤。
  EN: LLMs may possess metacognitive knowledge, such as naming the skills or procedures needed for a task.
- Core work / 核心工作:
  CN: 让 LLM 给数学题打 skill labels，再聚类为粗粒度 skill families；推理时根据 skill 选择相关 exemplars。
  EN: The method asks LLMs to assign skill labels, clusters them, and retrieves skill-matched exemplars at inference time.
- Core claim / 核心论点:
  CN: 显式识别“当前题需要什么技能”可以提升数学推理。
  EN: Explicitly identifying the skill needed by the current problem can improve math reasoning.
- Main results / 主要结果:
  CN: 在 GSM8K 和 MATH 上，skill-based exemplar selection 提升多个强 LLM 的准确率。
  EN: Skill-based exemplar selection improves accuracy on GSM8K and MATH for several strong LLMs.
- EGR value / 对 EGR 的价值:
  CN: 可支撑 EGR 的 selector：模型选择本质上类似“当前状态需要什么数学技能/定理模型”。
  EN: Supports EGR's selector: theorem-model selection is analogous to identifying the mathematical skill needed by the current state.

### 13. PAL: Program-aided Language Models

Fulltext source: Zotero key `YPTJGGN2`; indexed full text about 86k characters.

- Premise / 前提假设:
  CN: LLM 擅长把问题分解成步骤，但在执行算术、符号计算或逻辑细节时容易出错。
  EN: LLMs are good at decomposition but often make arithmetic, symbolic, or logical execution errors.
- Core work / 核心工作:
  CN: PAL 让 LLM 生成程序作为中间推理步骤，把执行交给 Python interpreter。
  EN: PAL makes LLMs generate programs as intermediate reasoning steps and delegates execution to a Python interpreter.
- Core claim / 核心论点:
  CN: LLM 应负责理解和程序生成，确定性解释器应负责执行。
  EN: LLMs should handle interpretation and program generation, while deterministic interpreters handle execution.
- Main results / 主要结果:
  CN: 在 13 个数学、符号和算法推理任务上，PAL 优于更大模型的 CoT；在 GSM8K 上 CODEX+PAL 比 PaLM-540B+CoT 高约 15 个点。
  EN: Across 13 reasoning tasks, PAL outperforms CoT with larger models; CODEX+PAL beats PaLM-540B+CoT by about 15 points on GSM8K.
- EGR value / 对 EGR 的价值:
  CN: 是 EGR “predict-and-execute” 叙事的核心先例。EGR 的差异是执行 theorem model，而不是执行任意程序。
  EN: A core predecessor for EGR's predict-and-execute story. EGR differs by executing theorem models rather than arbitrary programs.

### 14. Position: Formal Mathematical Reasoning - A New Frontier in AI

Fulltext source: Zotero key `VXC57ZI4`; indexed full text about 73k characters.

- Premise / 前提假设:
  CN: 形式化数学推理是评估 AI 可靠推理能力的重要前沿，因为它要求可验证、无歧义、可组合的证明过程。
  EN: Formal mathematical reasoning is a frontier for AI because it demands verifiable, unambiguous, compositional proof processes.
- Core work / 核心工作:
  CN: 作为 position paper，系统论证 formal mathematical reasoning 的研究价值、挑战和路线，包括 autoformalization、proof search、verified reasoning 等。
  EN: As a position paper, it argues for the importance, challenges, and research directions of formal mathematical reasoning, including autoformalization, proof search, and verified reasoning.
- Core claim / 核心论点:
  CN: 真正可靠的数学 AI 需要从答案生成走向可验证推理过程。
  EN: Reliable mathematical AI must move from answer generation to verifiable reasoning processes.
- Main results / 主要结果:
  CN: 该文主要贡献是 field positioning，而非单一 benchmark 结果。
  EN: Its main contribution is field positioning rather than a single benchmark result.
- EGR value / 对 EGR 的价值:
  CN: 可帮助 EGR 借用 formal reasoning 的严谨语言，但 EGR 必须说明自己不是通用 theorem prover，而是 conic-section theorem-action solver。
  EN: Helps EGR borrow rigorous language from formal reasoning, while clarifying that EGR is not a general theorem prover but a conic-section theorem-action solver.

### 15. Premise-Augmented Reasoning Chains Improve Error Identification in Math reasoning with LLMs

Fulltext source: Zotero key `Q3YU3IE6`; indexed full text about 82k characters.

- Premise / 前提假设:
  CN: 线性 CoT 的依赖关系不显式，导致错误步骤难以验证和定位。
  EN: Linear CoT hides dependencies, making erroneous steps hard to verify and localize.
- Core work / 核心工作:
  CN: 构建 PARC，把 reasoning chain 扩展为带 premise links 的 dependency DAG。
  EN: PARC augments reasoning chains with premise links, turning them into dependency-aware DAGs.
- Core claim / 核心论点:
  CN: 每一步推理都应说明依赖哪些前提；显式 premise 能提升错误识别。
  EN: Each reasoning step should expose its premises; explicit premise links improve error identification.
- Main results / 主要结果:
  CN: 全文和 PMLR 页面报告 PARC 能显著提升错误识别，幅度约 6-16 个百分点。
  EN: The paper reports substantial improvements in error identification, around 6-16 absolute points.
- EGR value / 对 EGR 的价值:
  CN: 直接支撑 EGR 的 precondition + state transition 设计。EGR 比 PARC 更进一步：不仅记录 premise，还执行 theorem action。
  EN: Directly supports EGR's precondition plus state-transition design. EGR goes beyond premise links by executing theorem actions.

### 16. Program of Thoughts Prompting

Fulltext source: Zotero key `5BJKB53Z`; indexed full text about 56k characters.

- Premise / 前提假设:
  CN: 自然语言 CoT 混合了推理和计算，导致算术和符号执行错误。
  EN: Natural-language CoT mixes reasoning and computation, causing arithmetic and symbolic execution errors.
- Core work / 核心工作:
  CN: PoT 让模型输出可执行程序，把计算交给 interpreter，从而把“思考”与“执行”解耦。
  EN: PoT makes the model output executable programs and delegates computation to an interpreter, separating reasoning from execution.
- Core claim / 核心论点:
  CN: 数值推理中，执行应由确定性运行时完成，而非由语言模型在文本中完成。
  EN: In numerical reasoning, execution should be done by a deterministic runtime, not by an LLM inside prose.
- Main results / 主要结果:
  CN: 在多个 numerical reasoning benchmark 上优于 CoT 类方法，尤其适合复杂计算。
  EN: It improves over CoT-style methods on several numerical reasoning benchmarks, especially for computation-heavy tasks.
- EGR value / 对 EGR 的价值:
  CN: 支撑 EGR 的 select/execute 分离。但 EGR 要强调 theorem-model executor 比程序执行更贴合数学原理选择。
  EN: Supports EGR's select/execute separation. EGR should stress that theorem-model execution better captures mathematical principle selection than generic code execution.

### 17. Safe: Enhancing Mathematical Reasoning in LLMs via Retrospective Step-aware Formal Verification

Fulltext source: Zotero key `XPVZUZZQ`; indexed full text about 74k characters.

- Premise / 前提假设:
  CN: 数学推理可靠性不仅要求最终答案正确，还要求每个中间步骤可被形式验证。
  EN: Reliable math reasoning requires not only correct final answers, but formally checkable intermediate steps.
- Core work / 核心工作:
  CN: 使用 retrospective step-aware formal verification 检查和改进 LLM 数学推理步骤。
  EN: Uses retrospective step-aware formal verification to check and improve LLM mathematical reasoning steps.
- Core claim / 核心论点:
  CN: formal verification 应进入推理过程内部，而不是只在最终答案后做判断。
  EN: Formal verification should enter the reasoning process, not only judge the final answer.
- Main results / 主要结果:
  CN: 全文索引显示该方法在 ACL 2025 数学推理任务中通过步骤级形式验证提升可靠性。
  EN: The fulltext indicates improved reliability on ACL 2025 math reasoning tasks through step-level formal verification.
- EGR value / 对 EGR 的价值:
  CN: 可支撑 EGR 的 applicator：`can_apply/apply` 是过程内验证机制，不是后处理。
  EN: Supports EGR's applicator: `can_apply/apply` is an in-process verification mechanism, not post-processing.

### 18. Step Guided Reasoning

Fulltext source: Zotero key `LPJBHT5B`; indexed full text about 73k characters.

- Premise / 前提假设:
  CN: LLM 在多步数学推理中需要更明确的步骤指导，而不是只依赖自由生成。
  EN: LLMs need explicit step guidance in multi-step math reasoning rather than unconstrained generation.
- Core work / 核心工作:
  CN: 通过 guidance generation 和 step reasoning 改进数学推理过程。
  EN: Improves reasoning through guidance generation and step-wise reasoning.
- Core claim / 核心论点:
  CN: 中间步骤的质量可以通过显式 guidance 改善。
  EN: The quality of intermediate steps can be improved by explicit guidance.
- Main results / 主要结果:
  CN: 全文索引显示该方法在数学推理 benchmark 上提升表现，并强调 step guidance 的作用。
  EN: The fulltext reports improved math reasoning performance and highlights the value of step guidance.
- EGR value / 对 EGR 的价值:
  CN: 可支撑 EGR selector 的引导作用：下一步不是生成任意文本，而是选择可执行 theorem model。
  EN: Supports EGR's selector as a guidance mechanism: the next step is not arbitrary text but an executable theorem model.

### 19. Step-KTO: Optimizing Mathematical Reasoning through Stepwise Binary Feedback

Fulltext source: Zotero key `7JVRALZR`; indexed full text about 65k characters.

- Premise / 前提假设:
  CN: 只用 outcome-level feedback 会忽略推理链内部质量；步骤级二元反馈可以让模型更可靠。
  EN: Outcome-level feedback ignores internal reasoning quality; stepwise binary feedback can make reasoning more reliable.
- Core work / 核心工作:
  CN: 提出 Step-KTO，把 outcome-level 和 process-level binary feedback 结合进 alignment/training。
  EN: Step-KTO combines outcome-level and process-level binary feedback in alignment/training.
- Core claim / 核心论点:
  CN: 不只要优化最终结果，还要优化整个 reasoning trajectory。
  EN: We should optimize the whole reasoning trajectory, not only final outcomes.
- Main results / 主要结果:
  CN: 在数学推理 benchmark 上提升中间步骤质量，并保持或提升最终答案准确率。
  EN: It improves intermediate reasoning quality while maintaining or improving final answer accuracy.
- EGR value / 对 EGR 的价值:
  CN: 可启发 EGR 的训练信号：每个 transition 可以有 binary validity feedback。
  EN: Inspires EGR training signals: each transition can receive binary validity feedback.

### 20. Tree of Thoughts: Deliberate Problem Solving with Large Language Models

Fulltext source: Zotero key `HQEF6LB7`; indexed full text about 56k characters.

- Premise / 前提假设:
  CN: token-level left-to-right generation 不适合需要探索、回溯、lookahead 的问题。
  EN: Token-level left-to-right generation is insufficient for tasks requiring exploration, backtracking, and lookahead.
- Core work / 核心工作:
  CN: ToT 把中间单元从 token 扩展为 thought，并在 thought tree 上搜索、自评、回溯。
  EN: ToT expands the intermediate unit from tokens to thoughts and searches over a tree with self-evaluation and backtracking.
- Core claim / 核心论点:
  CN: 问题求解需要在比 token 更大的中间单元上做 deliberate search。
  EN: Problem solving requires deliberate search over units larger than tokens.
- Main results / 主要结果:
  CN: 在 Game of 24 中，GPT-4 + CoT 只解出约 4%，ToT 达到约 74%。
  EN: On Game of 24, GPT-4 with CoT solves about 4%, while ToT reaches about 74%.
- EGR value / 对 EGR 的价值:
  CN: 是 EGR 标语的直接对照：ToT 从 token 到 thought，EGR 从 thought 到 executable theorem model。
  EN: Directly supports EGR's slogan: ToT moves from token to thought; EGR moves from thought to executable theorem model.

### 21. UDfSolver: Uniform Representation and Decoupled Inference Strategy for Text-Diagram Function Problems Solving

Fulltext source: Zotero key `N3JRKGF8`; indexed full text about 92k characters.

- Premise / 前提假设:
  CN: 多类型函数题难点在于类型差异、图文复合输入和特定函数结构；统一表示与解耦推理有助于泛化。
  EN: Function problems are hard due to type diversity, text-diagram inputs, and type-specific structures; uniform representation and decoupled inference improve generality.
- Core work / 核心工作:
  CN: 提出 URM 和 DIS，覆盖六类函数题，把 procedural inference 与 function meta-model inference 分开。
  EN: Introduces URM and DIS for six function categories, separating procedural inference from function meta-model inference.
- Core claim / 核心论点:
  CN: 统一表示和解耦推理能提升数学求解系统的准确性、通用性、可解释性和扩展性。
  EN: Uniform representation and decoupled inference improve accuracy, generality, explainability, and extensibility.
- Main results / 主要结果:
  CN: 在六类 TDF 问题和三个 benchmark 上优于既有方法；全文也强调教育场景下需要 explainability 和 transparency。
  EN: It outperforms prior methods across six TDF categories and three benchmarks, and emphasizes explainability and reasoning transparency.
- EGR value / 对 EGR 的价值:
  CN: 是 EGR 的前序方法参照。EGR 应说明自己从“函数统一表示”推进到“圆锥曲线 theorem-model transition”。
  EN: A prior-method reference. EGR should explain its progression from uniform function representation to conic theorem-model transitions.

### 22. A Neuro-Symbolic Approach for Reliable Proof Generation with LLMs: A Case Study in Euclidean Geometry

Fulltext source: Zotero key `JTQV2CXK`; indexed full text about 57k characters.

- Premise / 前提假设:
  CN: LLM 在形式域和几何证明中容易生成 plausible text，但缺少严格演绎和符号验证。
  EN: LLMs generate plausible text in formal domains and geometry proofs, but lack rigorous deduction and symbolic verification.
- Core work / 核心工作:
  CN: 结合 analogical guidance 和 symbolic verifier；检索相似问题及证明，引导 LLM 生成证明，并由 verifier 反馈修正。
  EN: Combines analogical guidance and symbolic verification: retrieve analogous proofs, guide generation, and iteratively revise with verifier feedback.
- Core claim / 核心论点:
  CN: LLM 的生成能力需要结构化类比和验证器约束，才能生成可靠证明。
  EN: LLM generation needs analogical structure and verifier feedback to produce reliable proofs.
- Main results / 主要结果:
  CN: 在多个模型上把 proof accuracy 从 10%-44% 提升到 68%-96%。
  EN: Reports improving proof accuracy from 10%-44% to 68%-96% across evaluated models.
- EGR value / 对 EGR 的价值:
  CN: 支撑 EGR 在几何域中使用 neural proposal + symbolic verification 的合理性。EGR 的类比点是 theorem-model trajectory，而不是完整几何证明。
  EN: Supports EGR's neural proposal plus symbolic verification in geometry. EGR's counterpart is theorem-model trajectory rather than full Euclidean proof.

### 23. AXIOM: A Trust-First Neuro-Symbolic Execution Architecture for Verifiable Mathematical Reasoning

Fulltext source: Zotero key `PKMQPGAQ`; indexed full text about 48k characters.

- Premise / 前提假设:
  CN: prompt-in/text-out 的 LLM 接口无法区分 confident-right 与 confident-wrong；数学系统应优先避免 confident-wrong。
  EN: Prompt-in/text-out LLM interfaces cannot distinguish confident-right from confident-wrong; math systems should prioritize avoiding confident-wrong.
- Core work / 核心工作:
  CN: AXIOM 让 LLM 只做 canonicalizer，把自然语言重写为窄 schema，再由确定性 CAS pipeline 求解/验证/拒答。
  EN: AXIOM uses the LLM only as a canonicalizer, then routes schema-constrained input to deterministic CAS handlers that solve, verify, or abstain.
- Core claim / 核心论点:
  CN: trust-first 系统应把 abstain 作为一等输出，按数学模板 routing，并用 regression oracle 防止 lost-correct。
  EN: A trust-first system should treat abstain as first-class, route by mathematical templates, and use regression oracles to prevent lost-correct.
- Main results / 主要结果:
  CN: 全文报告四类 MATH 上累计 94.36% correctness，在 parseable 上 100% trust，并实现 zero confident-wrong。
  EN: Reports 94.36% cumulative correctness on four MATH categories, 100% trust on parseable records, and zero confident-wrong answers.
- EGR value / 对 EGR 的价值:
  CN: 对 EGR 的启发是 trust metric 和 abstain/continue 机制：如果状态不足或 theorem model 不适用，系统应继续推理或拒答，而非硬生成。
  EN: Inspires trust metrics and abstain/continue mechanisms for EGR: if the state is insufficient or a theorem model is inapplicable, the system should continue or abstain instead of forcing an answer.

### 24. Gold-medalist Performance in Solving Olympiad Geometry with AlphaGeometry2

Fulltext source: Zotero key `62DDQGKL`; indexed full text about 88k characters.

- Premise / 前提假设:
  CN: 几何推理需要领域语言、符号引擎、搜索和神经指导共同工作；语言覆盖率会限制系统能力。
  EN: Geometry reasoning needs a domain language, symbolic engine, search, and neural guidance; language coverage limits system capability.
- Core work / 核心工作:
  CN: AG2 扩展 AlphaGeometry 语言，支持移动对象、角/比例/距离的线性方程、非构造问题，改进 search、Gemini model、knowledge-sharing 和 symbolic engine。
  EN: AG2 extends the geometry language, supports object movement and linear equations over angles/ratios/distances, improves search, Gemini models, knowledge sharing, and the symbolic engine.
- Core claim / 核心论点:
  CN: 高水平几何推理依赖 formal language coverage、symbolic engine 和 learned search 的共同扩展。
  EN: High-level geometry reasoning depends on joint improvements in formal language coverage, symbolic engine, and learned search.
- Main results / 主要结果:
  CN: IMO 2000-2024 几何问题语言覆盖率从 66% 提升到 88%，总体解题率达到 84%，高于前版 54%。
  EN: Language coverage improves from 66% to 88% on IMO 2000-2024 geometry problems, and solving rate rises to 84% from 54%.
- EGR value / 对 EGR 的价值:
  CN: 强支撑 conic-section 题型选择：几何域需要专门状态语言和符号引擎。EGR 要把“圆锥曲线状态语言覆盖什么”写清楚。
  EN: Strong support for conic-section choice: geometry needs specialized state languages and symbolic engines. EGR should clarify what its conic state language covers.

### 25. Intermediate Languages Matter: Formal Languages and LLMs Affect Neurosymbolic Reasoning

Fulltext source: Zotero key `35N8EJKK`; indexed full text about 31k characters.

- Premise / 前提假设:
  CN: 神经符号 LLM 推理的成败不仅取决于 LLM 和 solver，也取决于中间形式语言。
  EN: Neurosymbolic LLM reasoning depends not only on the LLM and solver, but also on the intermediate formal language.
- Core work / 核心工作:
  CN: 比较四种 formal languages、三个数据集和七个 LLM，提出 intermediate language challenge。
  EN: Compares four formal languages across three datasets and seven LLMs, introducing the intermediate language challenge.
- Core claim / 核心论点:
  CN: 形式语言选择会影响 syntactic 和 semantic reasoning 能力。
  EN: Formal-language choice affects both syntactic and semantic reasoning.
- Main results / 主要结果:
  CN: 全文显示不同语言和模型组合导致推理效果显著变化，说明“接口设计”本身是关键变量。
  EN: Results show that different language-model combinations lead to substantial differences, making interface design a core factor.
- EGR value / 对 EGR 的价值:
  CN: 直接支撑 EGR 的 `AbstractState` / `SymbolicState` 双层状态：这不是 feature engineering，而是神经符号接口设计。
  EN: Direct support for EGR's `AbstractState` / `SymbolicState` split: it is not feature engineering, but neural-symbolic interface design.

### 26. Logic-LM: Empowering Large Language Models with Symbolic Solvers for Faithful Logical Reasoning

Fulltext source: Zotero key `NLS7KG7U`; indexed full text about 77k characters.

- Premise / 前提假设:
  CN: LLM 看似具备逻辑推理能力，但复杂逻辑问题中会缺少 faithfulness；symbolic solver 可提供确定性推理。
  EN: LLMs appear to reason logically but lack faithfulness on complex logic; symbolic solvers provide deterministic inference.
- Core work / 核心工作:
  CN: LLM 先把自然语言问题翻译为 symbolic formulation，solver 执行推理，self-refinement 使用 solver error messages 修正形式化。
  EN: The LLM translates natural language into symbolic formulation; a solver performs inference; self-refinement uses solver errors to revise formulations.
- Core claim / 核心论点:
  CN: LLM + symbolic solver 可显著提升 faithful logical reasoning。
  EN: LLM plus symbolic solver can substantially improve faithful logical reasoning.
- Main results / 主要结果:
  CN: 五个逻辑推理数据集上，平均比 standard prompting 高 39.2%，比 CoT 高 18.4%。
  EN: On five logical reasoning datasets, it improves by 39.2% over standard prompting and 18.4% over CoT on average.
- EGR value / 对 EGR 的价值:
  CN: 支撑 EGR 的神经-符号分工，但 EGR 应强调自己不是一次性 semantic parsing，而是状态演化中的 repeated theorem-model transition。
  EN: Supports EGR's neural-symbolic division, while EGR should stress that it is repeated theorem-model transition rather than one-shot semantic parsing.

### 27. Neural Theorem Proving: Generating and Structuring Proofs for Formal Verification

Fulltext source: Zotero key `BKWH3V9M`; indexed full text about 49k characters.

- Premise / 前提假设:
  CN: LLM 生成代码和证明仍不能保证 formal correctness；形式化 proof generation 需要生成、结构化和验证共同工作。
  EN: LLM-generated code/proofs do not guarantee formal correctness; formal proof generation needs generation, structuring, and verification.
- Core work / 核心工作:
  CN: 提出 ProofSeek 类框架，包含语言模型训练、proof generation、verification module，并结合 SFT/RL。
  EN: Proposes a ProofSeek-style framework with model training, proof generation, verification, and SFT/RL.
- Core claim / 核心论点:
  CN: whole-proof generation 与 proof-step generation、formal verifier 需要结合。
  EN: Whole-proof generation, proof-step generation, and formal verifiers need to be combined.
- Main results / 主要结果:
  CN: 全文承认 benchmark 结果仍落后 SOTA，但展示了 real-world verification use case 和 formal proof pipeline 的可行性。
  EN: The paper notes that benchmark results remain behind SOTA, but demonstrates the practical utility of a formal proof-generation pipeline.
- EGR value / 对 EGR 的价值:
  CN: 可支撑 EGR 对 proof-like trajectory 的表述：生成 action 不够，还要被结构化并验证。
  EN: Supports EGR's proof-like trajectory framing: generated actions must be structured and verified.

### 28. NeuroProlog: Multi-Task Fine-Tuning for Neurosymbolic Mathematical Reasoning via the Cocktail Effect

Fulltext source: Zotero key `3DZ8JYKG`; indexed full text about 78k characters.

- Premise / 前提假设:
  CN: LLM 数学推理常生成流畅但逻辑不一致的答案；可执行 Prolog 程序能提供形式化约束和诊断。
  EN: LLM math reasoning often produces fluent but logically inconsistent answers; executable Prolog provides formal constraints and diagnostics.
- Core work / 核心工作:
  CN: 把数学文字题编译成 Prolog 程序，用 Cocktail training 联合优化 formula-to-rule、NL-to-program 和 program-answer alignment，并用 execution-guided decoding 修正。
  EN: Compiles MWPs into Prolog programs; Cocktail training jointly optimizes formula-to-rule, NL-to-program, and program-answer alignment; execution-guided decoding repairs errors.
- Core claim / 核心论点:
  CN: 统一符号表示空间中的多任务训练能产生正迁移，提升可组合推理和自修复能力。
  EN: Multi-task training in a unified symbolic representation space creates positive transfer and improves compositional reasoning and self-debugging.
- Main results / 主要结果:
  CN: 全文报告 Qwen-32B Cocktail 比 base 高 5.23 点，GPT-OSS-20B 高 3.43 点，Llama-3B 高 5.54 点；32B 下 correction rate 达 92.7%。
  EN: Reports gains of +5.23 for Qwen-32B, +3.43 for GPT-OSS-20B, +5.54 for Llama-3B, and 92.7% correction rate at 32B.
- EGR value / 对 EGR 的价值:
  CN: 支撑 EGR 的“统一 symbolic action/state 空间”训练价值。EGR 可考虑用 transition validity/error type 训练 selector。
  EN: Supports training in a unified symbolic action/state space. EGR could use transition validity and error types to train the selector.

### 29. Solving Math Word Problems by Combining Language Models With Symbolic Solvers

Fulltext source: Zotero key `TNLY6B5L`; indexed full text about 18k characters.

- Premise / 前提假设:
  CN: PAL 偏向 procedural problems；更难的代数文字题常需要 declarative reasoning，即先表达变量和方程关系。
  EN: PAL is biased toward procedural problems; harder algebra word problems often require declarative reasoning over variables and equations.
- Core work / 核心工作:
  CN: LLM 增量 formalize 文字题为变量和方程，再用 symbolic solver 求解。
  EN: An LLM incrementally formalizes word problems as variables and equations, then a symbolic solver solves them.
- Core claim / 核心论点:
  CN: 与外部工具接口时，declarative and incremental representations 对复杂数学题更合适。
  EN: Declarative and incremental representations are better interfaces to external tools for complex math problems.
- Main results / 主要结果:
  CN: 在 GSM8K 上接近 PAL；在更难的 ALGEBRA 数据集上比 PAL 高 20 个百分点。
  EN: Comparable to PAL on GSM8K and 20 points better than PAL on the harder ALGEBRA dataset.
- EGR value / 对 EGR 的价值:
  CN: 直接支撑 EGR 的 `SymbolicState`：数学状态应保存变量、方程、关系，而不是只生成程序。
  EN: Direct support for EGR's `SymbolicState`: mathematical state should store variables, equations, and relations, not only generated programs.

### 30. Solving Olympiad Geometry without Human Demonstrations

Fulltext source: Zotero key `29YALYRP`; indexed full text about 74k characters.

- Premise / 前提假设:
  CN: 奥林匹克几何证明需要在无限分支空间中搜索；人类形式证明数据稀缺，纯符号方法又依赖人工 heuristic。
  EN: Olympiad geometry requires search over an infinite branching space; human formal proof data are scarce, and symbolic systems depend on hand heuristics.
- Core work / 核心工作:
  CN: AlphaGeometry 用 synthetic data 训练语言模型，由 LM 提出辅助构造，symbolic deduction engine 验证并推进证明。
  EN: AlphaGeometry trains a language model on synthetic data; the LM proposes auxiliary constructions, and a symbolic deduction engine verifies and advances proofs.
- Core claim / 核心论点:
  CN: 神经模型可以负责创造性搜索，符号引擎负责可靠演绎。
  EN: Neural models can guide creative search, while symbolic engines ensure reliable deduction.
- Main results / 主要结果:
  CN: 在 30 道 IMO-level geometry problems 中解出 25 道，超过此前方法的 10 道，接近平均 IMO gold medalist。
  EN: Solves 25 of 30 IMO-level geometry problems, outperforming the previous best method's 10 and approaching an average IMO gold medalist.
- EGR value / 对 EGR 的价值:
  CN: 是 EGR 最重要的几何神经符号先例。EGR 应对照说明：AlphaGeometry 预测构造并证明，EGR 预测 theorem model 并更新圆锥曲线 symbolic state。
  EN: The most important geometry neurosymbolic predecessor. EGR should contrast: AlphaGeometry predicts constructions for proof; EGR predicts theorem models to update conic symbolic states.

### 31. SymCode: A Neurosymbolic Approach to Mathematical Reasoning via Verifiable Code Generation

Fulltext source: Zotero key `QFMAC38N`; indexed full text about 63k characters.

- Premise / 前提假设:
  CN: prose-based math reasoning 容易产生未验证、算术不可靠、逻辑不透明的解答。
  EN: Prose-based math reasoning leads to unverified, arithmetically unsound, and opaque solutions.
- Core work / 核心工作:
  CN: SymCode 把数学解题重构为 SymPy 可验证代码生成，并加入 self-debugging loop。
  EN: SymCode reframes math solving as verifiable SymPy code generation with a self-debugging loop.
- Core claim / 核心论点:
  CN: 把推理从自然语言转成可执行 symbolic code，可把 opaque fallacies 转成 transparent programmatic errors。
  EN: Moving reasoning from prose to executable symbolic code converts opaque fallacies into transparent programmatic errors.
- Main results / 主要结果:
  CN: 在 MATH-500、OlympiadBench、AIME 等 benchmark 上最高带来约 13.6 个百分点提升；复杂任务中收益更明显。
  EN: Reports improvements up to about 13.6 points on MATH-500, OlympiadBench, AIME, with larger benefits on harder tasks.
- EGR value / 对 EGR 的价值:
  CN: 支撑 EGR 的核心论点：可靠性来自可执行表示和确定性反馈。EGR 可进一步说：theorem model 比 generic SymPy code 更能暴露数学原理选择。
  EN: Supports EGR's core claim that reliability comes from executable representation and deterministic feedback. EGR can add that theorem models expose mathematical-principle selection better than generic SymPy code.

## 3. How These Papers Should Serve EGR Writing / 对 EGR 写作的直接服务

### 3.1 Introduction Claims

CN:

- 引用 MATH、CogMath、StepCo、Error Classification：说明数学推理仍困难，final answer accuracy 会高估能力。
- 引用 CoMAT、ToT、PARC：说明中间过程重要，但 textual thought 仍不够可靠。
- 引用 AlphaGeometry / AlphaGeometry2：说明几何是神经符号推理的高价值场景。

EN:

- Cite MATH, CogMath, StepCo, and Error Classification to argue that mathematical reasoning remains hard and final-answer accuracy overestimates capability.
- Cite CoMAT, ToT, and PARC to argue that intermediate reasoning matters, but textual thoughts remain insufficiently reliable.
- Cite AlphaGeometry and AlphaGeometry2 to justify geometry as a high-value neural-symbolic reasoning domain.

### 3.2 Method Motivation Claims

CN:

- PAL / PoT / SymCode / NeuroProlog / Logic-LM 支撑 neural proposal + symbolic execution。
- LeanDojo / Neural Theorem Proving 支撑 state/action 或 premise/tactic selection。
- Intermediate Languages Matter / Declarative MWP Solver 支撑 EGR 的 dual-state representation。
- AXIOM 支撑 trust-first、abstain/continue 和 deterministic executor。

EN:

- PAL, PoT, SymCode, NeuroProlog, and Logic-LM support neural proposal plus symbolic execution.
- LeanDojo and Neural Theorem Proving support state/action or premise/tactic selection.
- Intermediate Languages Matter and the declarative MWP solver support EGR's dual-state representation.
- AXIOM supports trust-first design, abstain/continue behavior, and deterministic executors.

### 3.3 Experiment and Metric Design

CN:

EGR 的实验不应只有 final answer accuracy，应至少包含：

- theorem-model selection accuracy
- applicability rate
- symbolic transition correctness
- trajectory success rate
- termination accuracy
- extraction correctness
- information gain / entropy reduction
- failure attribution

EN:

EGR experiments should not report only final answer accuracy. They should include:

- theorem-model selection accuracy
- applicability rate
- symbolic transition correctness
- trajectory success rate
- termination accuracy
- extraction correctness
- information gain / entropy reduction
- failure attribution

### 3.4 Figure Design

CN:

- 图 1：From next-token prediction to next-model transition。
- 图 2：CoT/ToT/PAL/Logic-LM/LeanDojo/AlphaGeometry/EGR 的 related-work map。
- 图 3：EGR step anatomy：`S_t^abs -> selector -> theorem model -> can_apply/apply -> S_{t+1}^sym -> entropy/terminal extraction`。
- 图 4：error taxonomy：selection、applicability、execution、termination、extraction。
- 图 5：conic-section testbed：曲线类型、标准方程、焦点/准线/离心率/切线/渐近线/交点等 facts 如何进入 SymbolicState。

EN:

- Figure 1: From next-token prediction to next-model transition.
- Figure 2: Related-work map covering CoT, ToT, PAL, Logic-LM, LeanDojo, AlphaGeometry, and EGR.
- Figure 3: EGR step anatomy: `S_t^abs -> selector -> theorem model -> can_apply/apply -> S_{t+1}^sym -> entropy/terminal extraction`.
- Figure 4: Error taxonomy: selection, applicability, execution, termination, extraction.
- Figure 5: Conic-section testbed: how curve type, standard equation, foci, directrix, eccentricity, tangent, asymptote, and intersection facts enter `SymbolicState`.

## 4. Most Important Papers for Immediate Citation / 最优先引用对象

If the EGR draft can initially cite only a compact subset, prioritize:

1. MATH dataset - mathematical reasoning remains hard and needs algorithmic advances.
2. CogMath - final-answer accuracy overestimates mathematical ability.
3. StepCo or Step-KTO - step-level correction/feedback matters.
4. PARC - premise-aware steps improve error identification.
5. PAL - LLM proposes, interpreter executes.
6. PoT - disentangle computation from reasoning.
7. Logic-LM - LLM-to-symbolic-solver pipeline improves faithfulness.
8. Intermediate Languages Matter - representation/interface choice matters.
9. LeanDojo - theorem proving as state/action selection with retrieval.
10. AlphaGeometry - neural guidance plus symbolic geometry deduction.
11. AlphaGeometry2 - geometry language coverage and search matter.
12. SymCode or NeuroProlog - executable symbolic representation converts opaque reasoning errors into checkable errors.

