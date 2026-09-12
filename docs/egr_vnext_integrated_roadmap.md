# EGR vNext 开发—数据—实验—论文四线统一路线图

- **版本**：v1.0
- **日期**：2026-09-12
- **目标投稿**：Knowledge-Based Systems（KBS）
- **文档状态**：总体路线图；用于约束后续设计、开发、实验和写作
- **适用范围**：EGR 圆锥曲线求解项目的 vNext 迭代

> 本文档记录已经对齐的研究定义、四条工作线的依赖关系、阶段性交付物与验收门槛。它不把历史实验结果升级为最终证据，也不以当前实现完成度限制目标方法。

---

## 1. 研究总纲

EGR 是一个面向圆锥曲线问题的独立、可执行、progress-aware 神经符号求解框架。它以 query-conditioned 双层状态表示问题，通过 selector 预测高层 theorem model，由 Grounder 和 Applicator 完成参数绑定及共享符号算子执行，并通过 Residual State Entropy（RSE）衡量从当前状态到成功求解的剩余工作量与路径可达难度。系统允许多条经过验证的正确路径，以最终答案正确且全过程可执行作为端到端成功标准。LLM integration 是重要扩展验证，而不是 EGR 成立的前提。

### 1.1 中心研究问题

> Can conic-section problem solving be reformulated as a state-conditioned process of theorem-model selection, executable symbolic transition, and residual-entropy-guided control?

### 1.2 扩展研究问题

> Can the executable intermediate capabilities of EGR improve the reliability of LLM mathematical reasoning?

### 1.3 固定研究边界

1. 80 个 ID 是高层 theorem schemas，不是不可分解的底层计算原语。
2. 多个 theorem schemas 可以复用相同的 symbolic primitives。
3. Selector 只预测高层 theorem model ID。
4. Grounder 初期采用确定性约束、简单排序和有限回溯。
5. 人类自然语言解答是 reference rationale，不是唯一 gold path。
6. 正确答案只用于离线终态验收和评价，不参与测试时的选择、绑定、搜索或停止。
7. AbstractState 可以从 28 维基线升级为 query-conditioned 结构化表示。
8. 数学语义状态与推理控制历史分开保存。
9. RSE 是核心理论对象；normalized remaining steps 只是简化基线。
10. Standalone EGR 是论文主线；LLM augmentation 是扩展实验。
11. 当前实证范围限定于圆锥曲线；跨领域迁移只作为架构潜力讨论。
12. 重建的可执行轨迹数据是内部训练与评测基础，不作为当前论文的独立数据资源贡献。

### 1.4 当前阶段明确不做的事情

- 不直接用现有 `models` 顺序继续训练最终 selector。
- 不把搜索尚未发现成功续接的动作自动标成负样本。
- 不让 AnswerExtractor 继续承担实质性求解。
- 不把剩余步数回归直接称为正式 RSE。
- 不在 standalone solver 尚未稳定前把 LLM 实验提升为主线。
- 不基于单一 Conic10K 实验声称跨数学领域通用性。
- 不把历史 smoke test、局部样本或不一致协议下的指标写成 KBS 最终结果。

---

## 2. 当前基线与 vNext 起点

以下信息只用于确定工程起点，不构成最终论文结果。

| 对象 | 当前仓库状态 | vNext 判断 |
| --- | --- | --- |
| Theorem universe | 80 个定义 ID；当前运行时注册 56 个 | 先统一 contract，再分批完成和验证 80 个 schema |
| 训练数据 | 7,757 题；5,359 条非空 `models`；20,226 个模型步骤；79 个出现过的 ID | `models` 是由自然语言过程派生的 weak sequence，不能直接视为严格执行顺序 |
| SymbolicState | 以字符串、字典和列表保存实体、方程、参数、关系、坐标、约束及模型历史 | 需要规范化语义状态、控制历史、来源与一致性检查 |
| AbstractState | 当前为 28 维手工向量 | 保留为 baseline；主方法升级为 query-conditioned 结构化表示 |
| TheoremModel | `can_apply()` + in-place `apply()` | 升级为可绑定、事务化、有显式 delta 和 postcondition 的 action contract |
| StateSequenceBuilder | 可以沿给定 ID 序列生成状态，但允许 skipped/failed 后继续 | 不能用于可信监督；必须阻断不可达后缀并验证每条 transition |
| Selector | 80 分类 hard-label 模型 | 改为 set-supervised schema selection；按 problem 划分数据 |
| Entropy | 启发式完整度或 normalized remaining steps | 作为基线；正式目标改为 solution-graph-derived RSE |
| ReasoningEngine | 以 completeness、重试和 max steps 为主要控制 | 改为 selector—grounder—applicator—RSE—AnswerReady 闭环 |
| AnswerExtractor | 仍调用 SymbolicSolver 完成变量、表达式和几何量求解 | 将求解迁移到 theorem application / primitives；extractor 只读、规范化、验证 |
| 历史实验 | 多种局部协议，指标口径不一致 | 仅作为诊断；vNext 统一重跑 |

---

## 3. 目标系统的正式结构

### 3.1 总体执行链

```text
Problem facts + query
        ↓
Initial SymbolicState + AbstractState
        ↓
Selector: P(theorem schema | state, query)
        ↓
Top-k theorem schemas
        ↓
Grounder: schema → bound action instance
        ↓
Applicator: precondition → symbolic primitives → state delta → postcondition
        ↓
Successor SymbolicState + rebuilt AbstractState
        ↓
RSE estimation and successor ranking
        ↓
AnswerReady ∧ low-RSE ?
   ├── no: continue / backtrack
   └── yes: terminal extraction and internal validation
        ↓
Predicted answer
        ↓
Offline gold-equivalence evaluation
```

### 3.2 双层状态与控制上下文

状态统一写为：

\[
S_t=\left(S_t^{\mathrm{sem}},S_t^{\mathrm{ctrl}}\right).
\]

- \(S_t^{\mathrm{sem}}\)：实体、曲线、方程、参数、坐标、约束、已推导事实、query 与 unresolved subgoals。
- \(S_t^{\mathrm{ctrl}}\)：已尝试动作、成功动作、绑定、失败原因、状态哈希、路径深度、累计代价和回溯信息。

同一数学语义状态应具有稳定的 canonical hash。控制历史不能改变数学真值，但可以帮助避免循环和重复尝试。

### 3.3 Theorem schema 与 bound action

高层 theorem schema 定义为：

\[
M_i=
\left(
\mathrm{pre}_i,
\mathrm{ground}_i,
\mathrm{program}_i,
\mathrm{post}_i
\right),
\]

其中：

- `pre`：声明所需对象、类型、关系和约束；
- `ground`：从 SymbolicState 中绑定具体数学对象；
- `program`：调用共享 symbolic primitives 的确定性程序；
- `post`：验证输出状态满足预期数学性质。

实际执行动作写为：

\[
a_t=(M_i,\theta_t),
\]

其中 \(\theta_t\) 是变量、点、直线、曲线或表达式绑定。

### 3.4 Transition contract

每次应用必须产生结构化结果：

```text
TransitionResult
├── status: applied | inapplicable | failed | no_op | conflict
├── model_id
├── binding
├── precondition_evidence
├── state_before_hash
├── state_delta
├── state_after_hash
├── postcondition_evidence
├── primitive_trace
└── error_code / diagnostics
```

基本不变量：

1. 失败不能污染原状态；
2. 成功必须产生可验证的非空 delta；
3. 重复执行应幂等，或因 `no_op` 被拒绝；
4. 新事实不得与已有事实冲突；
5. 每个结构化结果必须记录来源模型和参数绑定；
6. `applied` 不等于 `productive`，query relevance 与 RSE reduction 另行判断。

### 3.5 Residual State Entropy

令 \(\Pi^+(S,q)\) 为从当前状态出发、经过可执行 theorem transitions、最终到达内部验证通过且答案正确终态的完成轨迹集合。令 \(\pi_0\) 是当前可执行高层 theorem IDs 上的最大熵参考策略，\(C(\tau)\) 是路径代价。定义：

\[
Z_\beta(S,q)=
\sum_{\tau\in\Pi^+(S,q)}
P_{\pi_0}(\tau\mid S,q)
\exp[-\beta C(\tau)],
\]

\[
H_{\mathrm{RSE}}(S,q)
=
-\log\left(Z_\beta(S,q)+\varepsilon\right).
\]

RSE 的完整条件记为：

\[
H_{\mathrm{RSE}}
(S,q\mid\mathcal M,\pi_0,B,c),
\]

其中 \(\mathcal M\) 是 theorem pool，\(B\) 是搜索预算，\(c\) 是动作代价。

RSE reduction 为：

\[
\Delta H(S,a)
=
H_{\mathrm{RSE}}(S,q)
-H_{\mathrm{RSE}}(T(S,a),q).
\]

当动作成本不相同时，候选排序还必须显式扣除即时成本。

### 3.6 终止与成功定义

测试时的过程终止条件：

\[
\mathrm{Stop}(S_t,q)=
\mathbf 1[
H_{\mathrm{RSE}}(S_t,q)\le\epsilon_H
\land
\mathrm{AnswerReady}(S_t,q)
].
\]

`max_steps`、重复状态检测和 no-progress guard 是安全边界，不是目标状态定义。

完整评价分为：

1. **Transition-valid**：每一步均可执行并通过 postcondition；
2. **Query-resolved**：终态可以独立导出候选答案；
3. **Answer-correct**：候选答案与 gold answer 数学等价；
4. **Verified solution**：同时满足以上三项。

---

## 4. 贡献层级与证据契约

| 层级 | 计划贡献 | 必需证据 | 禁止提前声称 |
| --- | --- | --- | --- |
| C1 | 将圆锥曲线求解建模为 state-conditioned executable theorem transition | 正式定义、算法、完整执行案例、与 direct generation / program prediction 的清楚区别 | “首次把数学推理表示为状态转移” |
| C2 | Query-conditioned 双层状态与 grounded symbolic application | 状态消融、transition validity、state aliasing 分析、执行 trace | “固定 28 维向量本身具有通用性” |
| C3 | Set-supervised theorem schema selector | Verified action sets、无泄漏 problem split、Valid@k、端到端增益 | “复现唯一 gold sequence 就代表正确推理” |
| C4 | Goal-conditioned RSE 及其 ranking / termination 机制 | 图上目标、估计误差、校准、排序、终止与端到端消融 | “remaining steps 就是 Shannon entropy”或“RSE 预测答案正确性” |
| C5 | 完整 standalone EGR solver | 冻结协议下的 final-answer accuracy、verified solution rate、效率与错误分析 | SOTA、60%+ 或其他尚未运行的结果 |
| C6 | EGR 对 LLM 的模块化增强 | Direct LLM 与多个 EGR 接口的受控比较、correction/harm、原始输出 | “EGR 已被证明可增强所有 LLM” |

核心贡献的叙述顺序固定为：

1. state-conditioned executable theorem-transition formulation；
2. dual-layer state and grounded symbolic execution；
3. goal-conditioned Residual State Entropy；
4. standalone conic solver and optional LLM reasoning interface。

---

## 5. 四条工作线

### 5.1 开发线

目标是把现有原型重构为语义稳定、可验证、可训练的 solver runtime。

主要工作包：

- D1：状态、动作、绑定、delta 和 transition contract；
- D2：公共 symbolic primitive library；
- D3：80 个 theorem schemas 的契约化与稳定实现；
- D4：确定性 Grounder 与有限回溯；
- D5：query-conditioned AbstractState；
- D6：set-supervised Selector；
- D7：RSE target builder、estimator、ranking 和 termination；
- D8：严格 AnswerReady、terminal extractor 和 answer comparator；
- D9：端到端 search / reasoning engine 与审计日志。

### 5.2 数据线

目标是从原始问题和 weak rationale 建立内部 verified transition / solution graph 数据层。

主要工作包：

- A1：冻结原始 Conic10K problem-level split 与数据 provenance；
- A2：审计 80 个 schema 的语义、粒度、频次和当前实现状态；
- A3：以原始 `models` 为 seed，重建 reference rationale path；
- A4：执行并验证每个 bound transition；
- A5：搜索局部替代动作与成功续接，构建 partial-order solution graph；
- A6：区分 verified positive、verified negative 与 unknown；
- A7：生成 selector、Grounder、RSE 和终止训练视图；
- A8：自动全量验证与分层人工审计。

### 5.3 实验线

目标是用一个冻结、可复现的协议分别回答选择、执行、进度、终止、答案和 LLM 增强问题。

主要工作包：

- E1：动作库与 Grounder conformance；
- E2：theorem selection；
- E3：transition validity 与 progress-producing rate；
- E4：RSE estimation、ranking 和 stopping；
- E5：standalone end-to-end solving；
- E6：组件消融与 search efficiency；
- E7：错误类型与 case study；
- E8：LLM augmentation；
- E9：统计检验、置信区间和复现实验包。

### 5.4 论文线

目标是让论文结构与系统真实接口、数据生成逻辑和最终证据同步演进。

主要工作包：

- P1：research canon、术语表、claim–evidence matrix；
- P2：问题背景、gap 与 conic testbed 论证；
- P3：Problem Formulation 与正式定义；
- P4：Method、算法、状态追踪实例与动作分类表；
- P5：Dataset / internal annotation / protocol；
- P6：Standalone Results、RSE Analysis 和 Ablation；
- P7：LLM Augmentation；
- P8：Limitations、generalization boundary 与 conclusion；
- P9：KBS 全文一致性、引用、图表和语言清理。

---

## 6. 四线统一里程碑

| 里程碑 | 主要依赖 | 开发线 | 数据线 | 实验线 | 论文线 | 退出门槛 |
| --- | --- | --- | --- | --- | --- | --- |
| M0 概念与协议冻结 | 当前共识 | 固定核心接口草案 | 固定数据 provenance 与标签语义 | 定义指标和拆分原则 | Canon、argument map、claim matrix | 所有核心术语只有一个定义，旧定义被明确降级 |
| M1 Transition vertical slice | M0 | 完成新 contract、state delta、primitive pilot、Grounder pilot | 构建少量可信完整轨迹 | contract / transition 单元验证 | 写出正式定义、一个完整 state-trace example | 一个代表性多步问题可在无 extractor 求解的条件下完整通过 |
| M2 80-schema executable layer | M1 | 分批完成 theorem schemas 与公共 primitives | 建立 schema inventory、测试案例和 binding 模板 | 每个 schema 的正例、负例、边界例与 no-op 检查 | 形成 theorem taxonomy 与 applicator 方法节 | 80/80 有 contract；注册必须以测试通过为前提 |
| M3 Internal verified graph | M2 | 稳定 trajectory builder 与 graph builder | 重建 reference path、替代路径、positive/negative/unknown | 数据质量审计、split leakage 检查 | 写 internal annotation protocol，不声称新 benchmark | 无 silent skip；不可达后缀不进入训练；审计门槛通过 |
| M4 State、Selector 与 RSE | M3 | AbstractState v2；set selector；RSE targets/estimator | 生成冻结训练视图 | 28D/structured、hard/set、proxy/RSE 对照 | 完成 selector 与 RSE 方法节 | Dev 协议冻结；所有模型选择指标基于 verified action set |
| M5 Standalone EGR integration | M4 | 完整推理循环、回溯、终止、纯提取器 | 保存真实 rollout 与失败轨迹 | 端到端 smoke、错误分类、回归测试 | Algorithm 1、系统图和 case study | 训练/推理/评价无 gold leakage；结果可重复 |
| M6 Frozen standalone evaluation | M5 | 仅修复预注册问题；冻结代码版本 | 冻结 manifests 和 hashes | 主结果、消融、分层分析、统计检验 | 填写 Results，不再使用历史指标 | 所有主表来自同一协议；claim matrix 全部有证据或降级 |
| M7 LLM augmentation | M6 | 暴露稳定 guidance / execution / verification 接口 | 保存 prompts、responses、traces | Direct LLM 与 EGR variants 对比 | 单独扩展实验节 | 固定模型、prompt、预算；报告 correction 与 harm |
| M8 KBS submission package | M6，M7 可选完成 | 发布复现入口与版本信息 | 数据使用说明与内部资源边界 | 最终图表、附录、artifact index | 全文重构、引用核验、投稿检查 | 方法、代码、实验、论文四线完全一致 |

### 6.1 关键依赖路径

```text
M0 Formal specification
  → M1 Transition contract and vertical slice
  → M2 Executable theorem layer
  → M3 Verified trajectories and solution graphs
  → M4 Structured state + Selector + RSE
  → M5 Standalone EGR
  → M6 Frozen evaluation
  → M7 LLM augmentation
  → M8 KBS submission
```

论文线从 M0 开始同步推进，但 Results 只能在 M6 后写成确定结论。Selector 与 RSE 可在 M3 数据冻结后并行开发；LLM 实验不能提前替代 standalone evaluation。

---

## 7. 阶段实施细则

### M0：固化 EGR vNext 规范

#### 开发

- 定义 `TheoremSchema`、`ActionBinding`、`StateDelta`、`TransitionResult` 和 `AnswerReadyResult`。
- 明确 semantic state、control context、AbstractState 和 query 的边界。
- 明确所有失败状态与 error codes。
- 决定兼容旧 `TheoremModel.apply()` 的迁移适配层，不一次性破坏全部模型。

#### 数据

- 建立 source problem、weak model sequence、reference path、verified graph 四层 provenance。
- 冻结“positive / negative / unknown”的定义。
- 冻结 problem-level split；禁止 transition-level random split。

#### 实验

- 先定义 metric，再开发 evaluator。
- Final answer accuracy、verified solution rate、reasoning completion、transition validity 与 selector Valid@k 分开报告。

#### 论文

- 新建 KBS claim–evidence matrix；AAAI 草稿只作为素材来源。
- 明确 RSE 的完整条件和术语边界。
- 将“next token vs next model”保留为概念对照，不写成对所有 LLM 的绝对判断。

#### Gate M0

- 概念规范、标签规范、评价规范互不冲突。
- 所有后续数据 schema 都能指向正式定义。

### M1：Transition contract 与代表性 vertical slice

#### 开发

- 将 in-place apply 包装为事务化执行：在副本上执行，通过 postcondition 后提交。
- 建立统一 delta 操作，例如 `add_entity`、`add_equation`、`set_parameter`、`add_relation`、`add_coordinate`、`add_constraint` 和 `set_query_result`。
- 参数写入必须处理 new / equivalent / conflict 三种情况。
- 建立第一批公共 primitives：表达式解析与规范化、等价判断、方程求解、代入消元、曲线参数恢复和基础解析几何。
- 选取一条“参数恢复—几何关系—query result”的代表性圆锥曲线多步路径完成端到端迁移。

#### 数据

- 为 vertical slice 手工核验初始状态、每个 binding、delta、后置条件与最终答案。
- 同时生成 reference path 和至少一个可交换/替代路径案例。

#### 实验

- 验证相同输入和 action binding 产生确定性等价状态。
- 验证失败、异常、no-op 均不改变原状态。
- 验证 extractor 在移除求解逻辑后仍能从终态读出答案。

#### 论文

- 按 Definition—Process—Example—Algorithm 组织第一个完整案例。
- 用该案例同时检验符号、图示和伪代码是否表达同一过程。

#### Gate M1

- 一个完整多步问题能够生成可审计 trace，并通过答案等价验证。
- trace 中每个新事实都能追溯到 theorem schema、binding 和 primitive。

### M2：公共 symbolic primitives 与 80 个 theorem schemas

#### 开发

- 将 80 个 schema 按数学职责分类：曲线识别与标准化、参数关系、焦点/准线/离心率、切线/弦/渐近线、坐标与向量、距离与面积、代数与判别式、不等式与优化、答案相关归约。
- 每个 schema 先写 contract，再写实现。
- 相同运算必须调用公共 primitive，不在各模型中复制正则、求解和格式化逻辑。
- 移除宽泛异常吞噬；使用显式失败类型。
- 修复模型重复写 `applied_models`、松散 `can_apply`、字符串-only delta 与循环应用问题。

#### 数据

- 对每个 schema 建立来源、数学定义、适用曲线、query 类型、参数角色和已知边界。
- 统计每个 ID 在 weak sequence 中的题目数和步骤数，只用于排优先级，不用于证明语义正确。
- 对存在粒度重叠的 schema 建立 equivalence / specialization / composition 关系。

#### 实验

- 每个 schema 至少覆盖：一个正例、一个前置条件反例、一个重复执行例和一个边界例。
- 对共享 primitives 做独立单元测试和数学等价测试。
- 报告 schema coverage，不把“代码文件存在”当作“模型可执行”。

#### 论文

- 给出 theorem schema 的正式定义、分类表和代表性示例。
- 说明高层 schema 与底层 primitives 的分层，避免把 80 个动作写成 80 个互不相关的规则补丁。

#### Gate M2

- 80/80 schema 均有明确 contract。
- 只有通过 contract tests 的 schema 才能注册为 executable。
- AnswerExtractor 不再包含应属于 theorem application 的核心推理逻辑。

### M3：内部 verified trajectories 与 solution graphs

#### 开发

- 重写 trajectory builder：任何 missing / inapplicable / failed / no-op transition 都会阻断该 reference 后缀，不能继续把后续标签绑定到未变化状态。
- 保存 state snapshot、delta 和 canonical hash。
- 实现局部替代动作枚举、受限成功续接搜索和 graph merge。
- 根据 read/write dependency 与交换性检验建立 partial order。

#### 数据

建议的内部版本化视图：

```text
data/egr_vnext/
├── manifest.json
├── problems.jsonl
├── transitions.jsonl
├── solution_graphs.jsonl
├── selector_examples.jsonl
├── rse_targets.jsonl
└── audit_report.json
```

以上是建议新增路径，实施前可根据现有数据目录约定调整。

每条 transition 至少保存：

```text
problem_id, split, source_step,
model_id, binding,
precondition_evidence,
state_before_hash, state_delta, state_after_hash,
postcondition_evidence,
status, label_status,
source_provenance, verifier_version
```

标签含义：

- `verified_positive`：存在经过验证的正确续接；
- `verified_negative`：已证明不可应用、矛盾、失败或进入验证死路；
- `unknown`：搜索预算内未证明成功或失败，训练时默认屏蔽。

自然语言过程的作用：

- 提供 theorem candidates；
- 提供部分依赖顺序；
- 提供 reference rationale preference；
- 不直接决定唯一 next action。

#### 质量审计

- 100% 运行 schema、hash、delta、postcondition 和终态自动验证。
- 对所有 conflict、no-op、顺序不一致和多绑定样本人工复核。
- 按 theorem ID、曲线类型、query 类型、轨迹长度与模型频次分层抽样。
- 在生产构建前冻结人工审计规模和接受阈值。
- 对审计中发现的系统性错误先修 contract，再重新生成，不对输出 JSON 做局部手工修补。

#### 实验

- 报告 reference path executable rate、transition verification rate、unknown rate、alternative-path discovery rate 和 graph size 分布。
- 验证同题所有派生状态只存在于同一个 split。

#### 论文

- 将其写成 method-supporting annotation pipeline，而不是新的公开 benchmark。
- 明确 Conic10K 原始字段与 EGR 派生字段。

#### Gate M3

- 不存在 silent skip 或失败后继续构造“伪后续状态”。
- 未验证动作不进入正标签，unknown 不进入负标签。
- 所有训练视图可追溯回原题和 verifier 版本。

### M4：AbstractState v2、set-supervised Selector 与 RSE

#### AbstractState v2

- 输入必须 query-conditioned。
- 表示对象、关系、约束、可用参数、unresolved subgoals 与 theorem readiness。
- 控制历史只保存必要摘要，例如最近动作、失败动作、重复状态和累计成本。
- 28 维向量保留为 `handcrafted-28D` baseline。
- 主编码器可以采用结构化图、集合或混合特征，但不能丢失精确执行所需的 SymbolicState。

#### Selector

正动作集合记为 \(A^+(S)\)。基础 set loss：

\[
\mathcal L_{\mathrm{set}}
=
-\log\sum_{m\in A^+(S)}p_\theta(m\mid S,q).
\]

- Selector 预测 schema ID，不预测 gold answer。
- Grounder 在 symbolic constraints 下产生 binding。
- 如果同一个 ID 只有部分 binding 合法，内部监督仍保存完整 bound actions。
- 可按成功续接成本为多个正动作设置 soft preference。

#### RSE

- 从冻结 solution graph 计算有限预算下的 \(Z_\beta\) 与 RSE target。
- 第一版 \(\pi_0\) 在可执行高层 schema IDs 上均匀分布。
- 第一版成本采用 unit theorem step；后续扩展为 primitive count 或实测时间。
- 对 incomplete graph 给出 lower/upper bound 或 unknown mask，不伪装成精确真值。
- 训练 query-conditioned RSE estimator，并与 remaining steps、shortest distance、heuristic completeness 和 prediction entropy 比较。

#### 实验

Selector：

- Valid@1、Valid@3、Valid@5；
- Mean rank to any valid action；
- coverage 与长尾 schema 表现；
- calibration；
- 28D vs structured、hard-label vs set-supervised。

RSE：

- 对 graph-derived target 的 MAE / rank correlation / calibration；
- 正动作与负动作 successor 的 RSE ordering accuracy；
- 真实 rollout 上的 RSE reduction；
- 对 depth feature 的 shortcut ablation；
- low-RSE 下 AnswerReady precision。

#### 论文

- Selector 章节使用集合监督，不再使用唯一 gold action 叙述。
- RSE 章节明确其是 maximum-entropy path prior 诱导的 negative-log reachability potential，而不是普通 Shannon state entropy。

#### Gate M4

- 数据拆分以 problem 为单位，无中间状态泄漏。
- Selector 的所有正确性判断都相对于 verified valid action set。
- RSE 的理论目标、图上计算和神经估计三者定义一致。

### M5：Standalone EGR 闭环

#### 开发

每步执行：

1. 构造/更新 query-conditioned state；
2. Selector 生成 Top-k schemas；
3. Grounder 产生候选 bindings；
4. Applicator 事务化模拟 transition；
5. 过滤 inapplicable、failed、conflict、no-op；
6. 根据 selector score、RSE successor 和 action cost 排序；
7. 提交一个 transition，必要时有限回溯；
8. 更新 semantic/control state；
9. 检查 low-RSE 与 AnswerReady；
10. 仅从 terminal state 提取答案。

#### 安全与失败处理

- 状态哈希防循环；
- 同 schema 不因“曾使用”被永久禁止，binding 和 delta 决定是否重复；
- `max_steps` 和 no-progress 是安全停止，必须报告为非正常终止；
- 正确答案字符串不能进入运行时决策；
- 任何异常都记录 phase-specific failure code。

#### 实验

- 在小型冻结 dev slice 上先做端到端回归；
- 每次结果同时保存 selection、binding、primitive、delta、RSE、termination 和 extraction trace；
- 首先解决最大失败桶，不按单个题目堆无归纳性的补丁。

#### 论文

- Algorithm 1 必须逐项对应真实 runtime。
- Case study 同时展示正确路径、可替代路径和失败路径。

#### Gate M5

- 端到端运行无 gold leakage。
- AnswerExtractor 只做读取、规范化和验证。
- 同一配置重复运行产生可复现结果。

### M6：冻结 standalone 实验

#### 主比较组

1. Rule / uniform executable search；
2. 28D hard-label selector；
3. 28D set-supervised selector；
4. Structured-state set-supervised selector；
5. EGR without RSE；
6. EGR with RSE ranking only；
7. EGR with RSE termination only；
8. Full EGR。

如加入外部 solver 或 neural-symbolic baseline，必须保证输入信息与任务定义可比。

#### 主指标

- Final answer accuracy；
- Verified solution rate；
- Transition validity；
- Valid theorem action Top-k；
- Grounding success；
- AnswerReady precision / recall；
- Premature-stop / over-reasoning rate；
- 平均 theorem steps、primitive cost、回溯次数和运行时间；
- Invalid / unparsed answer rate。

#### 分层分析

- 椭圆、双曲线、抛物线、圆；
- value、equation、coordinate、distance、length、area、range、optimization 等 query；
- 单步与多步；
- 高频与长尾 theorem schemas；
- 唯一路径与多路径；
- 不同初始 RSE 区间。

#### 统计与复现

- 报告样本数、置信区间和预先定义的统计检验；
- 固定 seed、split manifest、代码 commit、模型 checkpoint 和配置；
- 每次运行保存逐题 JSONL 与聚合 JSON/CSV；
- 输出目录按 `dataset / method / split / run_id` 分层；
- 任何 metadata、comparator 或 label 修复后必须重跑并重生成报告。

#### Paper gate

- Final answer accuracy 是主结果，但不能替代过程可靠性指标。
- 60% 可保留为工程目标，不在结果生成前写成论文事实或方法有效性的唯一判据。
- 所有历史结果与 vNext 结果明确隔离。

### M7：LLM augmentation

#### 受控条件

1. Direct LLM；
2. LLM + EGR theorem candidates；
3. LLM + grounded symbolic execution；
4. LLM + full EGR trace / controller；
5. 可选：LLM proposes, EGR verifies。

#### 公平性

- 使用相同原题、答案格式要求和预算；
- EGR 不泄漏 gold sequence 或 gold answer；
- 保存完整 prompts、responses、tool traces 和解析失败；
- 模型版本、日期、temperature 和 token budget 全部冻结。

#### 指标

- Final answer accuracy；
- Executable-step rate；
- Invalid-output rate；
- Correction rate；
- Harm rate；
- EGR 被采纳、忽略或误用的比例；
- 按初始 RSE 和题目类型分层的增益。

#### Gate M7

- LLM 结果不用于反向掩盖 standalone solver 的失败。
- 只有多个条件在同一协议中完成后，才声称 EGR 可以增强 LLM。

### M8：KBS 论文重构

#### 推荐章节职责

1. **Introduction**：三类决策耦合、圆锥曲线挑战、中心问题和贡献。
2. **Related Work**：数学推理、neural-symbolic solving、theorem/proof guidance、progress/value/uncertainty、conic solving。
3. **Problem Formulation**：状态、theorem schema、bound action、transition、solution graph、RSE 与成功定义。
4. **EGR Method**：双层状态、selector、Grounder、Applicator、primitives、RSE controller、terminal extractor。
5. **Data and Evaluation Protocol**：Conic10K、内部派生标注、split、baselines、metrics。
6. **Standalone Results**：答案、过程、效率和消融。
7. **RSE Analysis**：估计质量、ranking、termination、轨迹与 case study。
8. **LLM Augmentation**：独立扩展实验。
9. **Discussion and Limitations**：action-library dependence、graph incompleteness、domain boundary、human-progress 仅为动机。
10. **Conclusion**：回到 state-conditioned executable reasoning。

#### 写作风格

- 采用 Definition—Process—Example—Algorithm/Table 闭环。
- 从圆锥曲线问题特征推导方法，不从“使用了某个神经网络”开始。
- 区分结构能力与技术能力：前者来自状态—转换结构，后者来自具体 selector、Grounder 和 primitives。
- 每个方法 claim 都必须能指向代码、数据 artifact 或实验表。
- “LLM: next token; EGR: next model”只作简洁直觉，不替代严格 related-work 比较。

#### 计划图表

- Figure 1：Direct generation 与 EGR executable transition paradigm；
- Figure 2：单步 theorem schema—Grounder—primitive—delta；
- Figure 3：Reference path、multiple valid paths 与 partial-order solution graph；
- Figure 4：RSE 定义、轨迹与 stopping；
- Figure 5：LLM augmentation interfaces；
- Table 1：80 个 theorem schemas 的分类与 primitive 复用；
- Table 2：数据、split 和内部 verified annotation 统计；
- Table 3：standalone 主结果；
- Table 4：selector / grounding / transition 分层结果；
- Table 5：RSE 与组件消融；
- Table 6：LLM augmentation；
- Table 7：错误类型。

---

## 8. 数据与实验的不可违反规则

1. 原始 Conic10K、weak model sequences、verified trajectories 与实验 rollouts 必须分层保存。
2. 数据版本必须包含 schema version、verifier version、source hash 和 split。
3. 同一 problem 的全部状态、transition 和替代路径必须位于同一 split。
4. `unknown` 不得自动转为 negative。
5. Gold answer 不得出现在 selector、Grounder、RSE estimator 或 stopping 的运行时输入中。
6. 只有内部独立导出答案后，离线 evaluator 才能访问 gold answer。
7. Transition success 必须以 delta 和 postcondition 为证据，不能只看 `apply()` 是否返回 `True`。
8. Answer correctness 与 reasoning validity 必须分别统计。
9. RSE 必须注明 theorem pool、reference policy、budget 和 cost definition。
10. 修改标签、比较器、评估协议或 theorem semantics 后，受影响的所有报告必须重新生成。

---

## 9. 主要风险与控制方式

| 风险 | 可能后果 | 控制方式 |
| --- | --- | --- |
| Weak sequence 顺序错误 | Selector 和 RSE 学到伪轨迹 | 以执行验证和 partial-order graph 重建监督 |
| 80 个 schema 粒度不一致 | 动作标签混合 theorem、strategy 与 primitive | 建立 ontology、primitive 分层和 composition 关系 |
| AbstractState aliasing | 同向量对应不同数学状态与动作 | Query-conditioned structured state；28D 仅作 baseline |
| Grounder 多绑定 | 同一 ID 的正确与错误实例混淆 | 保存 bound action；符号过滤、排序和有限回溯 |
| 搜索图不完备 | 合法动作被误标为负例 | positive / negative / unknown 三分；unknown masking |
| RSE 术语被质疑 | 理论贡献失去可信度 | 明确 negative-log reachability / path prior 定义并设置强基线 |
| RSE 只学 depth | 高相关但无真实状态理解 | 去 depth、打乱 depth、跨路径与 successor-ranking 消融 |
| Applicator 只写字符串 | 后续状态无法消费 | 强制 structured delta 和 postcondition |
| Extractor 偷做求解 | 方法层级与实验结论失真 | 将求解迁移到 primitives / theorem actions，extractor 纯化 |
| Broad can_apply 导致循环 | 高 reasoning success、低答案正确率 | productive check、state hash、RSE、no-op rejection |
| 长尾 theorem coverage | 总体求解被少数缺失动作阻断 | 按依赖与频次分批，但最终以 80-schema contract 为门槛 |
| LLM 增强引入伤害 | 平均准确率掩盖个体退化 | 同时报 correction rate 与 harm rate |
| 论文先于证据 | 方法叙述与代码事实分离 | Claim–evidence matrix 和 milestone gates |

---

## 10. 建议的第一批代码工作

路线图完成后，第一批实现不应直接批量补齐剩余 theorem files，也不应立即重训 selector。建议先完成一个小而完整的 vertical slice：

1. 定义 `ActionBinding`、`StateDelta` 与 `TransitionResult`；
2. 为旧 `TheoremModel` 增加兼容适配层，保证失败不污染状态；
3. 实现 canonical state diff、no-op 与 conflict 检测；
4. 抽取第一组共享 symbolic primitives；
5. 迁移一条代表性多步圆锥曲线路径并添加 contract tests；
6. 用该路径验证 trajectory、selector label、RSE target 和 terminal extraction 的最小闭环。

建议涉及的候选文件将在实施前再次核对，预计包括：

- `src/theorems/base_model.py`；
- `src/theorems/theorem_library.py`；
- `src/state/symbolic_state.py`；
- `src/state/state_sequence_builder.py`；
- `src/solver/` 下的公共 primitives；
- 新增 transition contract tests。

第一批代码的退出门槛不是“新增了多少代码”，而是：

> 一个真实问题可以通过正式 theorem-action contract 产生逐步可验证的 SymbolicState，最终答案由终态直接读取，并且完整 trace 可同时用于数据构建、selector 监督、RSE 目标和论文案例。

---

## 11. 路线图维护规则

- 本路线图与旧文档冲突时，以本文的 vNext 概念边界为准；历史文档保留为开发记录，不静默改写。
- 每个 milestone 开始前建立具体任务清单和 acceptance tests。
- 任何核心定义变化，必须先更新 research canon、数据 schema 和 claim–evidence matrix，再修改代码或论文。
- 任何实验结果只有同时具备配置、逐题输出、聚合报告和代码版本时，才能进入论文。
- 每完成一个 milestone，更新“事实、证据、风险、下一步”，而不是只更新完成百分比。

---

## 12. 当前状态

- [x] 完成研究目标与核心概念对齐；
- [x] 完成开发—数据—实验—论文四线总体路线图；
- [ ] M0：形成 EGR vNext formal specification 与新 claim–evidence matrix；
- [ ] M1：实现 transition contract vertical slice；
- [ ] M2：完成公共 primitives 与 80-schema executable layer；
- [ ] M3：构建内部 verified solution graphs；
- [ ] M4：训练 structured set-selector 与 RSE；
- [ ] M5：完成 standalone EGR；
- [ ] M6：冻结并运行主实验；
- [ ] M7：完成 LLM augmentation；
- [ ] M8：完成 KBS 投稿包。

---

## 13. 主要依据文档

- `paper/aaai2027_overall_research_narrative.md`
- `paper/aaai2027_initial_draft_latex.txt`
- `paper/aaai2027_claims_and_evidence.md`
- `paper/aaai2027_experiment_plan.md`
- `docs/project_understanding_260605.md`
- `doc/project_workflow.md`
- `doc/创新点+论文思路.md`
- `docs/learned_state_entropy.md`
- `dev_logs/aaai2027/theorem_audit_report.md`
- `docs/style_ref/Yu 2026 - theoretical review.pdf`
