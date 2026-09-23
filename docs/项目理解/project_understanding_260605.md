# 梳理EGR研究规划方向

> 你是 /Users/ebeleagel/Documents/GitHub/EGR 的 AAAI2027 研究规划与开发方向梳理 thread。
>
> 默认用中文交流。当前任务不是马上改代码、不是继续堆准确率，而是先从研究型项目的整体叙述逻辑出发，重新理解 EGR 的宏观目标、当前进展、证据链、短板，并帮助我调整下一阶段开发重心。
>
> 工作目录：
> /Users/ebeleagel/Documents/GitHub/EGR
>
> 重要约束：
> - 先阅读、理解、梳理，不要一上来改代码。
> - 不要 commit，不要 push，不要 git reset / restore / checkout -- / clean。
> - 不要改 `.env`，不要输出任何 secret/token/key。
> - 不要把 final answer accuracy、reasoning success、theorem-selection accuracy、entropy correlation 混成一个指标。
> - 当前研究目标是 AAAI2027 投稿，因此开发重心要服务研究思路和叙述逻辑，而不是只围绕某个短期准确率反复 patch。
> - 如果文档和代码/实验 artifact 冲突，优先以 repo 当前事实源为准，并明确指出冲突。
>
> 你首先要自己完成项目理解，然后再和我讨论方案。第一轮请不要给空泛建议，而是产出一个结构化理解报告。
>
> 请优先阅读这些文件：
>
> 1. 总体 思路 / handoff / 开发进展
> - doc/project_workflow.md、doc/创新点+论文思路.md、
> - dev_logs/aaai2027/integration_handoff.md
> - dev_logs/aaai2027/round2_integration_handoff.md
> - dev_logs/aaai2027/round2_integration_error_audit_handoff.md
> - dev_logs/aaai2027/round2_eval_slice_report_handoff.md
> - dev_logs/aaai2027/round2_solver_hardening_handoff.md
> - dev_logs/aaai2027/round2_entropy_correctness_join_handoff.md
>
> 2. 核心代码入口
> - src/state/abstract_state.py
> - src/state/symbolic_state.py
> - src/state/state_constructor.py
> - src/theorems/theorem_library.py
> - src/reasoning/reasoning_engine.py
> - src/reasoning/model_selector.py
> - src/reasoning/answer_extractor.py
> - src/solver/symbolic_solver.py
> - src/reasoning/entropy_estimator.py
> - src/entropy/
> - src/evaluation/protocol.py
>
> 3. 关键实验结果
> - outputs/evaluation/main_integration_200/summary.json
> - outputs/evaluation/round2_main_integration_200/summary.json
> - outputs/evaluation/round2_main_integration_500/summary.json
> - outputs/evaluation/round2_main_integration_full/summary.json
> - outputs/evaluation/round2_main_delta_200/summary.md
> - outputs/evaluation/round2_main_delta_500/summary.md
> - outputs/entropy/round2_correctness_join/report.md
>
> 研究方法
> 项目采用神经符号混合框架。
> 第一层是双层状态表示：
> src/state/symbolic_state.py: SymbolicState 保存实体、方程、参数、几何关系、坐标和约束，用于精确符号推理。
> src/state/abstract_state.py: AbstractState 把符号状态转成神经网络输入。代码里实际是 28 维向量，不是部分文档里写的 15 维。
> src/state/state_constructor.py: 负责解析 fact_expressions，标准化方程，并自动提取部分基础参数。
> 第二层是定理模型库：
> model/conic_model_ids.json 定义了 80 个模型。
> src/theorems/theorem_library.py 当前实际注册了 52/80 个模型。
> 每个模型都有 can_apply() 和 apply()，例如双曲线标准方程提参、渐近线公式、离心率公式等。
> 第三层是神经模型选择器：
> src/selector/model_selector.py 是一个 MLP：28 -> 64 -> 128 -> 64 -> 80，输出 P(model | state)。
> v2 训练数据 data/train_state_model_v2.json 有 12460 个状态转移样本。
> checkpoint 显示 v2 最佳验证 Top-1 为约 57.1%。
> 第四层是推理引擎：
> src/reasoning/reasoning_engine.py 管理推理循环。
> src/reasoning/model_selector.py 支持 neural_top1、neural_topk、three_layer_entropy。
> src/reasoning/entropy_estimator.py 当前的 H(S) 主要是启发式估计，不是真正训练出的状态熵网络。
>
> 总体理解
> 这个项目的本质是：用 Conic10K 的形式化表达和推理过程，把圆锥曲线解题拆成“可解释的定理动作序列”，再用最大熵/信息增益思想指导动作选择。它的研究价值不在于黑盒答题，而在于让数学推理过程可控、可解释、可追踪，并尝试用熵作为“解题进度”和“选择不确定性”的统一度量。
> 我希望你围绕以下研究主线理解项目：
>
> EGR 的叙述逻辑不是“单纯做一个准确率 patch 系统”，而是：
>
> 1. 双层 state 建模
>    - SymbolicState 表示显式几何/代数事实。
>    - AbstractState 表示神经 selector 可消费的状态特征。
>    - 需要解释为什么这种 state abstraction 对定理级推理有意义。
>
> 2. Theorem models 的构建与实现
>    - 每个 theorem/model 是一个可检查前提、可应用到 SymbolicState 的 reasoning action。
>    - 需要梳理 theorem library 当前覆盖了什么、缺什么，以及它在论文叙述中承担什么角色。
>
> 3. Model selector 的实现
>    - selector 输出 theorem-action 的概率分布 P(y | S)。
>    - 它是神经部分，但不能把 theorem-selection accuracy 当成最终任务成功。
>    - 需要梳理 selector 当前证据能支持什么，不能支持什么。
>
> 4. Model application 层面的 symbolic solver
>    - symbolic solver / answer extractor 负责把 state 中可提取的答案算出来。
>    - 它不是主叙述的全部，但对 final answer accuracy 很关键。
>    - 需要区分“推理路径选择”和“最终答案抽取/比较”的角色。
>
> 5. Entropy / H(S) 的初步实现
>    - entropy 当前主要是 remaining-step / process supervision 方向的 proxy。
>    - 不能直接声称它预测 final answer correctness。
>    - 需要梳理它在 EGR 叙述中应该放在什么位置：机制证据、progress signal、InfoGain，还是 future work。
>
> 6. 总体 solver 框架
>    - ReasoningEngine 如何组织 state construction、selector、model application、answer extraction。
>    - 当前系统已经有一个完整但不成熟的闭环。
>    - 下一阶段应该围绕“研究叙述闭环 + 关键证据链”推进，而不是无边界修补。
>
> 第一轮输出请包含这些部分：
>
> # 1. Project Understanding
> 用中文解释你理解的 EGR 是什么：研究问题、核心假设、系统组成、为什么适合 AAAI2027。
>
> # 2. Research Narrative Draft
> 给出一条可投稿论文的叙述主线，说明：
> - problem setting 是什么；
> - 为什么 theorem-action sequence 是合理建模；
> - dual-state representation 解决什么问题；
> - selector / entropy / symbolic solver 分别承担什么角色；
> - final answer accuracy 为什么仍是主指标。
>
> # 3. Current Progress Map
> 按模块列出当前进展：
> - state modeling
> - theorem library
> - model selector
> - reasoning engine
> - symbolic solver / answer extractor
> - entropy estimator
> - evaluation protocol
> 每个模块写：已有内容、已有证据、主要短板。
>
> # 4. Evidence and Metric Boundary
> 明确列出当前能支持的 claim 和不能支持的 claim。
> 特别注意：
> - final answer accuracy 是 gating metric；
> - reasoning success 是过程指标；
> - theorem-selection top-k 是辅助诊断；
> - entropy 目前不能被包装成 answer-correctness evidence。
>
> # 5. Development Direction Adjustment
> 基于 AAAI2027 目标，给出下一阶段开发重心排序。
> 不要只说“继续提高准确率”，而要说明哪些工作服务于研究叙述闭环，哪些只是局部性能 patch。
>
> # 6. Proposed Work Packages
> 把下一阶段拆成 4-6 个 work packages。
> 每个 package 包含：
> - 目标
> - 为什么对论文叙述重要
> - 需要读/改的文件
> - 预期 artifact
> - 验收标准
> - 风险
>
> # 7. Discussion Questions for Me
> 最后给我 5-8 个具体问题，帮助我决定研究 framing 和下一阶段优先级。
>
> 注意：
> - 第一轮不要改代码。
> - 如果你认为需要新增规划文档，可以先建议文件名和目录，但先不要创建，等我确认。
> - 回答要具体，引用 repo 中的文件和实验 artifact。
> - 不要声称没有验证过的结论。

<details><summary>5 previous messages</summary>

> 我会先做只读梳理：先查已有记忆里关于 EGR 的历史上下文，再按你列的文件读取 repo 当前事实源。不会改文件、不会 commit/push，也不会触碰 `.env`。
>
> 我先核对文件存在性、行数和关键摘要，重点看你指定的 handoff、代码入口和 summary artifact。接下来只会跑 `wc`/`sed`/`jq`/`rg` 这类只读命令。
>
> 初步看到一个需要仔细核对的点：`main_integration_200/summary.json` 当前摘要看起来已经不是记忆里旧的 5/200 baseline，而是 21/200。我要用文件名逐个抽取关键指标，避免把不同 run 混在一起。
>
> 当前 artifact 给出的主线已经比较清楚：Round 2 在 200 样本上从 10.5% 到 16.5%，500 样本从 6.8% 到 9.4%，full 是 453/7624=5.94%；但剩余错误大量是 `answer_mismatch`，这说明接下来不能只看 selector 或 reasoning success。接下来我会读文档和代码入口，确认系统层面的真实实现。
>
> 代码事实确认了一个文档/用户描述差异：`model/conic_model_ids.json` 是 80 个模型，但当前 `TheoremLibrary` 实际加载 56 个，不是旧描述里的 52 个。这个会在报告里标成 repo 当前事实源。
> </details>

已完成第一轮只读梳理；没有改代码、没有 commit/push。下面是基于当前 repo 文件和 artifact 的结构化理解报告。

# 1. Project Understanding

EGR 当前最准确的定位是：面向 Conic10K 圆锥曲线题的神经符号 theorem-action solver。它把解题过程建模成状态 `S_t` 上反复选择定理动作 `y_t`、执行 `T_y(S_t)`、更新状态并最终抽取答案的序贯决策问题。

核心假设是：数学推理不应只看最终答案，而应拆成可检查、可追踪、可学习的定理动作序列。`SymbolicState` 负责精确事实、方程、参数、关系、坐标和约束；`AbstractState` 把这些压成 28 维向量供 selector 使用，当前不是旧文档里的 15 维，见 [abstract_state.py](./src/state/abstract_state.py:141)。这很适合 AAAI2027 的点在于：它不是黑盒 answer generation，而是可解释神经符号推理、动作选择、状态不确定性和 symbolic execution 的结合。

当前 repo 事实：定理 universe 是 80 个 ID，但 `TheoremLibrary()` 运行时注册 56/80 个模型，不是部分旧说法的 52/80，见 [theorem_library.py](./src/theorems/theorem_library.py:26)。主性能仍低：round2 full valid 为 `453/7624 = 5.94%` final answer accuracy，不能支撑强性能 claim。

# 2. Research Narrative Draft

论文主线可以这样组织：

Problem setting：输入是形式化 facts 和 query，目标不是直接生成答案，而是在 80-ID theorem-action universe 中选择可执行动作序列，最终由 symbolic state 抽取答案。

Theorem-action sequence 合理性：Conic10K 本身有模型 ID / 推理步骤信号；`data/train_with_models_v2.json` 当前有 7,757 样本、5,359 个非空模型序列、20,226 个模型步骤。这个数据结构天然支持把解题建成 `S_0 -> y_0 -> S_1 -> ... -> answer`。

Dual-state representation 的作用：`SymbolicState` 保留可执行数学事实；`AbstractState` 抽象成固定 28 维向量，让 MLP selector 学习 `P(Y|S)`。这解决了“符号状态太复杂、神经模型不能直接消费”的问题。

Selector / entropy / solver 分工：selector 是定理动作策略 `P(Y|S)`，实现为 `28 -> 64 -> 128 -> 64 -> 80` 的 MLP，见 [model_selector.py](./src/selector/model_selector.py:13)。`H(S)` 当前应写成 remaining reasoning burden / progress proxy，不是严格 Shannon entropy，见 [learned_state_entropy.md](./docs/learned_state_entropy.md:5)。symbolic solver 和 answer extractor 是把推理结果落到 final answer 的关键工程层。

Final answer accuracy 仍是主指标：因为 AAAI 论文最终必须证明系统能解题。reasoning success、theorem top-k、entropy correlation 都是机制证据，不能替代 final answer accuracy。

# 3. Current Progress Map

State modeling：已有 `SymbolicState` + `AbstractState` + `StateConstructor`；当前 28 维向量明确，状态构造会标准化方程并自动提参。短板是 completeness 仍是启发式，状态抽象对复杂几何依赖、隐式约束和目标相关性表达不足。

Theorem library：当前注册 56/80；有 `can_apply()` / `apply()` 接口和批量 apply。短板是覆盖不完整，且覆盖分布不等价于 end-to-end usefulness；剩余 24 个不能盲目补，要按 failure slice 和 query/curve 影响排序。

Model selector：checkpoint `model_selector_v2.pth` 里 `best_val_acc = 0.5714`；但 integrated eval 上 theorem-selection diagnostic 很低，round2 full 为 Top-1 `0.1215`、Top-3 `0.2632`、Top-5 `0.3552`。这说明 supervised selector validation 和实际 trace-vs-gold evaluator 不是同一件事。

Reasoning engine：已形成完整闭环：构造状态、selector 选模型、`can_apply/apply`、更新 state、记录 trace、抽取答案，见 [reasoning_engine.py](./src/reasoning/reasoning_engine.py:100)。短板是终止/成功定义与答案抽取耦合，仍有 max_steps 和 no_model 问题。

Symbolic solver / answer extractor：Round2 已修 Parabola/Value 的 exact-pattern，200 样本从 `21/200` 到 `33/200`，500 样本从 `34/500` 到 `47/500`。短板是 patch 偏 exact-pattern，full-valid 仍大量 `answer_mismatch`。

Entropy estimator：有 heuristic 和 learned-linear；label 是 normalized remaining steps，schema 明确说它是 primary learned `H(S)` target，见 [schema.py](./src/entropy/schema.py:62)。learned entropy 对 remaining steps 的验证强，但 correctness join 只有 `33/200` 覆盖、3 个 final-correct positives，不能声称预测答案正确性。

Evaluation protocol：`protocol.py` 已清楚分开 final answer、reasoning success、failure reason、theorem top-k，见 [protocol.py](./src/evaluation/protocol.py:172)。短板是最终 frozen split / official test protocol 还要定，200-sample 数字明显乐观。

# 4. Evidence and Metric Boundary

当前能支持的 claim：

- EGR 已实现一个不成熟但完整的 theorem-action neural-symbolic solver。
- 当前 state abstraction 是 28 维，不是 15 维。
- 当前 theorem library 是 56/80，不是 52/80。
- Learned `H(S)` 能较好拟合 normalized remaining steps：validation Pearson `0.837`、Spearman `0.849`。
- Round2 hardening 在 matched 200/500 上无正确性回退：200 是 `33/200 = 16.5%`，500 是 `47/500 = 9.4%`，见 [round2_integration_handoff.md](./dev_logs/aaai2027/round2_integration_handoff.md:113)。

不能支持的 claim：

- 不能说 EGR 已达到 60-80% 或 SOTA。
- 不能说 entropy 预测 final answer correctness；join report 明确禁止，见 [report.md](./outputs/entropy/round2_correctness_join/report.md:40)。
- 不能把 theorem-selection Top-k 当最终任务成功。
- 不能把 reasoning success 当 final answer accuracy。
- 不能说 entropy 已提升 end-to-end solver accuracy；当前 estimator 未真正作为主证据整合进 final eval。

Metric boundary：

- Final answer accuracy：gating metric。
- Reasoning success：过程是否推进/终止/可抽取的过程指标。
- Theorem-selection top-k：selector 诊断，不是 solver 成功。
- Entropy correlation：progress-signal 证据，不是 answer-correctness 证据。

# 5. Development Direction Adjustment

下一阶段不应继续无边界 patch 准确率，而应围绕“论文叙述闭环”排序：

1. 先冻结 evaluation protocol 和 claim table：明确 full-valid / official split / seed / max_steps / comparator。
2. 主攻 final-answer bottleneck：full-valid 仍主要是 `answer_mismatch` 和 `max_steps`，这直接卡 AAAI 主指标。
3. 做 theorem coverage audit：按 query/curve/failure slice 补最有影响的 theorem，不是机械补齐 80。
4. 解释 selector discrepancy：为什么 checkpoint Top-1 57.1%，但 integrated theorem diagnostic 只有约 12%。
5. 把 `H(S)` 保守升级为机制证据：先做 actual eval-applied trajectory entropy，再谈 InfoGain integration。
6. LLM augmentation 放在后置实验；没有 direct LLM vs LLM+EGR 证据前，不作为主 claim。

# 6. Proposed Work Packages

WP1：Evaluation & Claim Freeze
目标：冻结 AAAI 主评估协议和 claim/evidence matrix。
文件：`src/evaluation/protocol.py`、`scripts/evaluation/run_eval_slices.py`、`paper/aaai2027_claims_and_evidence.md`。
Artifact：`paper/egr_eval_protocol_freeze.md`、最终 metric table。
验收：每个指标有样本数、split、failure buckets、不可混用说明。
风险：过早冻结会限制后续 solver 改动，需要版本号。

WP2：Final Answer Error Taxonomy
目标：把 `answer_mismatch` 拆成表达式等价、抽取缺失、solver 不会算、比较器误判。
文件：`outputs/evaluation/round2_main_integration_full/summary.json`、`samples.jsonl` 如需补跑、`src/reasoning/answer_extractor.py`、`src/solver/symbolic_solver.py`。
Artifact：top failure taxonomy + regression test list。
验收：至少覆盖 full-valid 最大 3 类 query/failure bucket。
风险：exact-pattern patch 可能堆工程债。

WP3：Theorem Coverage Audit
目标：决定剩余 24 个 theorem 哪些服务论文主线和主指标。
文件：`model/conic_model_ids.json`、`src/theorems/theorem_library.py`、`outputs/evaluation/*/by_model_id`。
Artifact：missing theorem priority table。
验收：每个候选 theorem 有影响样本、query/curve slice、预期收益。
风险：补 theorem 不一定提升 final answer，因为 bottleneck 可能在 extractor。

WP4：Selector Diagnostic Reconciliation
目标：解释 `best_val_acc=57.1%` 与 integrated Top-1 约 12% 的差异。
文件：`checkpoints/model_selector_v2.pth`、`data/train_state_model_v2.json`、`src/reasoning/model_selector.py`、`src/evaluation/protocol.py`。
Artifact：selector benchmark report。
验收：明确是 split、label construction、trace divergence、unsupported ID 还是 evaluator 口径导致。
风险：发现训练/评估泄漏或指标不可比，需要重训。

WP5：H(S) Evidence Upgrade
目标：把 entropy 从“好看的相关性”升级为可信 process-progress evidence。
文件：`src/entropy/`、`src/reasoning/entropy_estimator.py`、`scripts/entropy/join_entropy_correctness.py`。
Artifact：actual eval-applied entropy trajectories + learned/heuristic 对照。
验收：覆盖率显著高于当前 `33/200`，并明确不声称 answer correctness。
风险：entropy 可能只学到 depth shortcut，需要 ablation 去掉/扰动 depth。

WP6：AAAI Narrative Pack
目标：形成可投稿叙述骨架，不写过度 claim。
文件：`paper/aaai2027_paper_outline.md`、`paper/aaai2027_claims_and_evidence.md`、`docs/learned_state_entropy.md`。
Artifact：method section skeleton、claim boundary table、case-study plan。
验收：每个 claim 都能指到 code/artifact；TODO 不伪装成结论。
风险：论文故事过强而实验证据不足。

# 7. Discussion Questions for Me

1. AAAI2027 主 claim 你希望更偏 “可信神经符号 solver”，还是更偏 “H(S)/InfoGain 的推理进度建模”？
2. 最终主结果你想用 full valid `7624`，还是先定义 official dev/test split？
3. 你能接受 exact-pattern symbolic solver 作为当前阶段主提升路径吗，还是希望更偏一般化 theorem coverage？
4. `H(S)` 在论文里要放核心贡献，还是先放 mechanism evidence / ablation？
5. LLM augmentation 要纳入本篇主实验，还是作为 discussion / future work？
6. final answer accuracy 达到多少才进入 paper drafting：full-valid 10%、20%，还是先以 method paper 方式推进？
7. 下一轮开发是否优先做 `answer_mismatch` taxonomy，而不是继续补 theorem？
8. 是否需要我下一步先新增一个规划文档，比如 `dev_logs/aaai2027/research_direction_report.md`，把这份报告落盘？

> 0.首先明确一个重要的待完成任务，看起来你疏忽了。本研究要构建 state-model 的概率分布 P(Y|S) 作为 selector 定理动作策略 。当前数据集中，包含初始状态s0，以及model sequence。但是对每个题目数据，还需要在此基础上，额外补充构建s1, s2, ...。然后才能构建每个题目的s0-y0, s1-y1 , ... 这样的 state-model 数据。然后在这个数据的基础上再训练概率分布 P(Y|S) 。（请你仔细思考一下，给出可行的方案，即对训练集中的数据，补充出 初始状态s0 的后续状态）
>
> 1.AAAI2027 主 claim 更偏 “可信神经符号 solver”。
>
> 3.你能接受 exact-pattern symbolic solver 作为当前阶段主提升路径吗，还是希望更偏一般化 theorem coverage？把 answer_mismatch 拆成表达式等价、抽取缺失、solver 不会算、比较器误判。风险：exact-pattern patch 可能堆工程债。
> 对于这一点，我的理解是：将Conic-Section问题求解建模为一个 序列决策问题  决策包括2层 ：推理模型选择 selector  and  推理模型应用 application。你提到的exact-pattern patch可以被理解为是 推理模型应用 application 时涉及的工作。当然每个model里面会规定好它的application的流程和具体工作，会涉及一些exact-pattern patch。这些exact-pattern patch可以单独保存（比如放在symbolicsolver中或者合适的位置）
>
> 4.H(S) 在论文里要放核心贡献，因为它其实还有一个关键性的角色：作为theorem-action的终止条件。即H(S)满足一定条件（比如小于某个值）时，就认为题目求解达到目标状态，此时推理结束。不然缺少一个显示的指标来指示theorem-action的终止/成功定义（与另一个维度层面“答案抽取对比”相区别）。（当然，也可以加上一些额外的辅助机制，比如max_steps）
>
> 5.LLM augmentation 要纳入本篇主实验，当前是后续工作了。（思路：对比以下几种不同情况LLM的求解正确率  Only LLM、给定当前状态应用的model提示、嵌入 symbolic solver）
>
> 6.final answer accuracy 达到60%进入 paper drafting。但我其实也会同步进行paper描写的工作，因为整体思路已经非常明确了。
>
> 针对我上面提到的内容，我们再进行讨论，我觉得都讨论到位后再新增规划文档。
>


> 你这个纠正是关键的。上一轮我把 selector 当成已有模块总结了，但没有把“从每题 `s0 + model sequence` 系统展开成 `s_t -> y_t` 训练数据”提升为核心待完成任务，这是疏忽。
> </details>

对，这个 `state-model` 数据构建应放到最高优先级。没有完整的 `s0-y0, s1-y1, ...`，`P(Y|S)` 只是名义上的 selector，训练对象并不扎实。

**0. 构建后续状态的可行方案**

当前训练集每题有：

```text
facts/query/answer + model sequence [y0, y1, ..., yT-1]
```

要补成：

```text
S0 --y0--> S1 --y1--> S2 ... --yT-1--> ST
```

建议做一个严格的 trajectory builder，核心流程是：

1. 用 `StateConstructor.construct_from_facts(...)` 构建初始 `SymbolicState S0` 和 `AbstractState A0`。
2. 对 gold model sequence 中第 `t` 个模型 `y_t`：
   - 先记录训练样本 `(A_t, y_t)`；
   - 查询 `TheoremLibrary.get_model(y_t)`；
   - 检查 `can_apply(S_t)`；
   - 执行 `apply(S_t)` 得到 `S_{t+1}`；
   - 用 `construct_from_symbolic_state(...)` 生成 `A_{t+1}`；
   - 保存 transition 元数据。
3. 如果 `model` 缺失、`can_apply=False`、`apply` 异常、或 state 没变化，要显式记录，不要静默跳过。

输出最好拆成两份：

```text
data/state_model/state_model_pairs_v3.jsonl
# 每行是一个 selector 训练样本:
# problem_id, step, state_vector, state_hash, label_model_id, status, metadata

data/state_model/state_trajectories_v3.jsonl
# 每行是一题完整 trajectory:
# problem_id, facts, query, model_sequence, states, transitions, terminal_status
```

关键是要有三种 dataset view：

- `strict_executable`：只保留当前 theorem library 可连续执行的 `(S_t, y_t)`，适合训练当前系统能执行的 selector。
- `gold_intended`：即使某步无法执行，也保留 `(S_t, y_t)` 作为 gold action 信号，但从该步之后不能生成可靠 `S_{t+1}`。
- `failure_audit`：专门统计 missing model / precondition failed / apply failed / no state change，指导 theorem/application 补全。

我建议主训练先用 `strict_executable`，否则 selector 学到的 action 可能当前 applicator 根本无法执行。`gold_intended` 可作为 theorem coverage roadmap。

另一个重要点：`P(Y|S)` 不一定只能训练 hard label。因为同一个 abstract state 可能对应多个合理 theorem action，尤其 28 维 state abstraction 是有损的。可以先用 hard-label cross entropy 做 behavioral cloning，再进一步把相同 `state_hash` 或相同 `state_vector` 的 label 聚合成 soft target：

```text
P_empirical(y | S) = count(S -> y) / sum_y count(S -> y)
```

这样更符合“概率分布”的叙述，而不是把任意一条 gold sequence 当唯一正确路径。

**1. 主 Claim 调整**

既然 AAAI2027 主 claim 更偏“可信神经符号 solver”，那叙述核心应是：

```text
Conic-section solving as theorem-action sequential decision:
selector chooses theorem action;
applicator executes symbolic transition;
H(S) estimates remaining reasoning burden and termination readiness;
answer extractor only finalizes answer from terminal state.
```

也就是说，EGR 的主线不是单纯 “entropy 很新”，而是一个可信 solver 框架，其中 `H(S)` 是让 solver 可控、可终止、可解释的核心机制。

**2. Selector/Application 的边界**

你对 exact-pattern patch 的理解是对的。它不应该被贬成“堆 patch”，而应该归入 application 层：

```text
selector: pi_theta(y | S)
application: T_y(S) -> S'
```

每个 theorem model 的 application 可以调用 symbolic utilities。比如：

```text
src/theorems/models/model_xxx.py
    can_apply()
    apply()

src/solver/symbolic_solver.py
    exact algebra / geometry helper
```

这样 exact-pattern 不是随便散落，而是 theorem action 的执行细节。需要避免的是把大量“定理应用逻辑”塞进 `AnswerExtractor`，因为那会让论文里 selector/application/answer extraction 的层次变混。

比较理想的边界是：

- `TheoremModel.apply()`：负责把一个定理动作显式应用到 state。
- `SymbolicSolver`：负责通用符号计算、几何表达式化简、坐标/距离/斜率求解。
- `AnswerExtractor`：只负责从当前 state 读出 query 对应答案，尽量不承担新的推理步骤。

**3. H(S) 作为终止条件**

这个补充非常重要。`H(S)` 不只是 evidence，也应该是 solver 的 termination signal。

建议把终止定义成两层：

```text
process termination:
H_phi(S_t, q) <= tau_H
or max_steps reached
or no-progress guard triggered

evaluation correctness:
Extract(S_t, q) == gold answer
```

这样能清楚地区分：

- `H(S)`：系统内部认为“推理状态足够接近目标状态”；
- answer comparison：评估时才知道最终答案是否正确。

训练上，`H(S)` 可以继续用 normalized remaining steps，但还要派生 terminal label：

```text
terminal_ready = 1 if remaining_steps == 0 else 0
```

验证时调阈值 `tau_H`，看：

- premature stop rate：过早终止比例；
- terminal precision：终止时是否真的可抽取正确答案；
- avg steps：是否减少无效推理；
- final answer accuracy：最终主指标。

我会建议 `H(S)` 终止条件不要单独使用，而是：

```text
if H(S) <= tau_H and answer_extractor can return non-empty answer:
    stop
else:
    continue until max_steps/no-progress
```

这能避免 state entropy 低但答案仍不可抽取的情况。

**4. 新优先级**

基于你这轮补充，我会把下一阶段改成：

1. `WP0`: 重新构建 / 审计 state-model trajectory dataset。
2. `WP1`: 训练并验证真正的 `P(Y|S)` selector。
3. `WP2`: 明确 selector/application/answer extraction 三层边界。
4. `WP3`: 训练或校准 `H(S)`，把它用于终止条件。
5. `WP4`: full-valid answer_mismatch taxonomy，服务 60% final accuracy。
6. `WP5`: LLM augmentation 保留为后续实验，不进入当前主线。

这里最急的是 WP0。因为没有可信的 `S_t -> y_t` 数据，selector、H(S)、termination 和 paper 方法叙述都会悬空。

**5. 我建议下一步先讨论两个决定**

1. 构建 `S_t` 时，遇到 gold model 当前无法执行，要不要保留这一步作为 selector 训练 label？
   - 我的建议：保留在 `gold_intended`，但主训练先用 `strict_executable`。

2. `H(S)` 终止条件是先训练在 gold trajectory 的 `remaining_steps/T` 上，还是直接构造 terminal-ready binary head？
   - 我的建议：先保留 scalar `H(S)`，再从它校准 `tau_H`；后续可加 binary terminal head。

> 好的。那现在其实是有两个最重要的工作内容：
> 1.构建完整的后续状态： s0-y0, s1-y1, ...
> 2.Selector/Application 边界梳理重构
> 比较理想的边界是：
> TheoremModel.apply()：负责把一个定理动作显式应用到 state。
> SymbolicSolver：负责通用符号计算、几何表达式化简、坐标/距离/斜率求解。
> AnswerExtractor：只负责从当前 state 读出 query 对应答案，尽量不承担新的推理步骤。
>
> 我们先讨论第一个工作。对于你提到的 构建后续状态的可行方案 做一个严格的 trajectory builder。但目前的数据集中只有s0，后续的s1,s2,...都没有。同时因为完整的后续状态： s0-y0, s1-y1, ...会被用来训练selector，因此构建出来的后续状态一定要保证是准确无误的。（我的观点是：构建后续的SymbolicState即可，每一步的定理模型应用后，SymbolicState的变化应该就对应着fact_expressions内容的变化。而fact_expressions的变化的内容应该是有限的可确定的。要么是多了一个条件，要么是多了一个变量，要么是某个变量参数的值被更新了。所以我觉得可行的方式就是分析这些题目数据，然后总结出常见的state在应用一个model后，state会新增/变化哪些内容。然后这个工作我们这里相当于是预先总结完成。然后在后续构建好的solver中，applicator其实就是在完成这个工作。因此我们现在来总结并完成，即生成了完整的后续状态及state-model训练对，同时也有助于实现applicator）
> 请你根据我的观点，思考一个可行的构建出准确无误的后续状态的方案。（理论上靠人力来完成是可行的，但是资源和时间暂不允许。但是部分的人力来参与核对验证是可以被接受的）

对，你这个方向是可行的，但要把目标从“自动猜出后续状态”改成“用可审计的 theorem transition spec 生成后续状态”。否则 `s1, s2...` 会把错误悄悄注入 selector 训练集。

我建议方案如下。

**核心原则**

不要让 trajectory builder 自己发明状态变化。它只做三件事：

1. 从 `s0` 构造当前 `SymbolicState`。
2. 查当前 model ID 对应的 transition spec / applicator。
3. 执行确定性 state delta，并记录证据、校验结果和失败原因。

也就是说，后续状态不是从数据里“预测”出来，而是由人工/半自动总结出的 theorem application rules 生成出来。

状态变化最好统一成有限 delta 类型：

```text
add_entity(name, type)
add_equation(expr)
set_parameter(key, value, source_model)
add_relation(expr)
add_coordinate(point, tuple)
add_constraint(expr)
derive_answer_candidate(query_expr, value)
```

其中 `set_parameter` 不应无条件覆盖旧值。更稳的是：

```text
if key 不存在: 写入
if key 存在且等价: 保留并记录 duplicate
if key 存在但不等价: 标记 conflict，停止该 trajectory 或降级
```

**一条 theorem action 的标准 contract**

每个 `TheoremModel.apply()` 最终都应该满足这个 contract：

```text
Input:
  SymbolicState S_t
  query q
  optional context from facts

Precondition:
  can_apply(S_t) == True

Output:
  SymbolicState S_{t+1}
  StateDelta list
  status: success | no_op | conflict | unsupported | exception
  evidence: which facts/params/equations were used
```

这样构建出来的训练对是：

```text
(A_t, y_t, S_t_hash, delta_status, problem_id, step)
```

selector 主训练只用 `status=success` 且无 conflict 的样本。

**如何低人力完成 transition spec**

不要一开始人工写 80 个完整 applicator。更现实的是三阶段：

第一阶段：自动统计模型使用频率和失败影响。
从 `data/train_with_models_v2.json` 统计每个 model ID 出现次数、所在 query type / curve type、前后邻接关系。优先处理高频和影响 final accuracy 的模型。

第二阶段：为高频 model 写 transition spec。
每个 spec 只回答：

```text
这个 model 在 SymbolicState 中需要什么？
应用后一定新增什么？
如果输入缺某个量，能不能通过 SymbolicSolver 计算？
不能算时如何 fail closed？
```

第三阶段：生成 trajectories，并用 audit 抽样核对。
每个生成的 `S_t -> y_t -> S_{t+1}` 都保留 delta。人工不用看完整 state，只看 delta 是否符合定理语义。

**准确性保障**

为了保证“准确无误”，我建议使用 conservative construction：

- 可以确定的状态才写入。
- 不能确定的，不生成后续状态，不拿去训练 selector。
- `no_op` 不进入训练，因为它会让 selector 学到无效 action。
- conflict 不进入训练，但进入 applicator debug list。
- 对每个 model ID 至少人工审核若干条 delta 样本，形成 verified spec。

这样训练集会变小，但质量高。对 selector 来说，高质量 `S_t -> y_t` 比大量可疑状态更重要。

**数据产物设计**

最终应生成四类 artifact：

```text
data/state_model/trajectory_v3.jsonl
# 每题一条完整或部分 trajectory

data/state_model/state_model_pairs_v3.jsonl
# selector 训练对: state_vector/state_hash -> model_id

data/state_model/transition_deltas_v3.jsonl
# 每步 delta，可审计

outputs/state_model/trajectory_build_report.md
# 覆盖率、失败原因、每个 model 的 success/no_op/conflict 统计
```

报告里要重点看：

```text
trajectory full executable rate
state-model pair count
model ID coverage
unsupported model count
conflict count
no-op count
top failed model IDs
manual audit queue
```

**和 applicator 的关系**

你说得对：这个工作本质上就是 applicator 的前置规范化。trajectory builder 不应该和 applicator 分裂成两套逻辑。

理想结构是：

```text
TheoremModel.apply()
  -> 调用 model-specific transition logic
  -> 调用 SymbolicSolver 做通用符号计算
  -> 返回 StateDelta

TrajectoryBuilder
  -> 只是按 gold model sequence 反复调用 apply()
  -> 保存 S_t, y_t, delta, S_{t+1}
```

所以这个任务同时服务两个目标：

1. 生成 selector 训练数据。
2. 反向逼出每个 theorem model 的准确 application 语义。

**关键判断**

我不建议直接用现有 `apply()` 全量生成训练集后就训练 selector。应该先做 build report。因为如果某些 `apply()` 只是粗略加关系、或者没有真正改变 state，训练出的 `s1, s2...` 会不可信。

下一步最合理的是先做一个只读/轻量 dry-run 规划：

```text
统计 model sequence 使用分布
检查当前 apply() 的 delta 行为
列出 top 20 model 的 transition spec 草案
定义 StateDelta schema
确定哪些 model 可进入 v1 strict_executable trajectory build
```

等这个 spec 讨论完，再写 trajectory builder。