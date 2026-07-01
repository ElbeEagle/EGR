# AAAI 2027 Overall Research Narrative

## 1. Paper Identity

### Recommended Title

> **Neuro-Symbolic Theorem Prediction and State Transition for Conic-Section Problem Solving**

这个标题直接表达论文的核心转向：数学求解不再被建模为一次性的答案生成，而是被建模为可执行 theorem model 驱动的状态转移过程。

### Alternative Titles

1. **EGR: Entropy-Guided Neural-Symbolic Model Prediction for Conic-Section Reasoning**
2. **Predict, Execute, and Terminate: Neural-Symbolic Model Transitions for Conic-Section Problem Solving**
3. **Executable Theorem-Model Prediction for Entropy-Guided Mathematical Reasoning**
4. **From Theorem Prediction to Symbolic Execution: Enhancing LLM Mathematical Reasoning with EGR**

标题选择建议：

- 首选标题最有 AAAI 风格，突出 paradigm shift 和方法机制。
- 标题 1 最稳健，方法名清楚，适合算法型论文。
- 标题 4 更突出 LLM enhancement，但容易弱化 EGR 本身作为 solver 的独立贡献。

### Method Name

保留项目已有名称：

> **EGR: Entropy-Guided Reasoner**

论文中的完整定义为：

> **EGR is an entropy-guided neural-symbolic model-transition solver.**

核心组件统一命名如下：

| Component | Recommended term | Role |
| --- | --- | --- |
| 双层状态 | Dual-Layer Reasoning State | 同时支撑神经预测与符号执行 |
| 神经模型选择器 | Neural Theorem-Model Selector | 预测下一步 theorem model |
| 符号应用器 | Symbolic Model Applicator | 检查并执行 theorem model |
| 状态熵 | State Entropy Estimator | 估计 residual solving progress |
| 神经控制 | Entropy-Guided Neural Controller | 决定继续预测或停止 |
| 答案抽取 | Terminal-State Answer Extractor | 从终态抽取并验证答案 |

### One-Sentence Thesis

> Instead of generating an answer directly, EGR solves a conic-section problem through entropy-controlled prediction and symbolic execution of theorem models, and exposes the resulting executable reasoning process as structured guidance for LLM mathematical reasoning.

中文含义：EGR 不直接生成答案，而是通过熵控制的 theorem-model 预测与符号执行完成圆锥曲线求解，并将这一可执行推理过程作为结构化接口增强 LLM 数学推理。

## 2. Central Research Question

论文需要围绕一个统一问题展开，而不是分别介绍 selector、applicator、entropy 和 answer extractor：

> **Can difficult mathematical problem solving be reformulated from direct answer generation into a neural-symbolic process of theorem-model prediction, executable state transition, and progress-aware termination, and can this process improve LLM mathematical reasoning?**

对应三个研究假设：

1. **Model-transition hypothesis**：圆锥曲线求解可以表示为一系列 theorem model 驱动的状态转移，而不是不可观察的答案映射。
2. **Neural-symbolic hypothesis**：神经 selector 负责在复杂状态中预测合适模型，符号 applicator 负责保证动作可执行并进行精确计算，二者优于各自单独工作。
3. **LLM enhancement hypothesis**：显式 theorem candidates 和 symbolic execution 能减少 LLM 的定理选择错误、无效推导和计算错误，从而提高高难数学题的最终答案正确率与推理有效性。

## 3. Core Paper Story

### 3.1 Problem: Direct Answer Generation Hides Mathematical Decisions

现有 LLM 数学求解通常将问题建模为：

```text
Problem -> Generated reasoning text -> Answer
```

这一建模把三个本质不同的问题混在一起：

1. 下一步应该使用哪个数学定理或模型；
2. 该模型在当前条件下是否适用，以及如何精确执行；
3. 当前推理是否已经完成，答案是否可从已有信息中确定。

因此，即使最终文本看似合理，也无法明确定位错误来自 theorem selection、symbolic computation、termination，还是 answer extraction。

### 3.2 Reformulation: Solving as Model Prediction and State Transition

EGR 将圆锥曲线题表示为初始状态 `S_0`，将解题表示为：

```text
S_0 --M_0--> S_1 --M_1--> ... --M_{T-1}--> S_T --Extract--> answer
```

其中：

- `S_t` 是第 `t` 步的数学问题状态；
- `M_t` 是 selector 预测的 theorem model；
- `T_{M_t}` 是 applicator 执行的符号状态转移；
- `H(S_t)` 表示剩余求解负担或不确定性；
- `S_T` 是满足终止条件的 terminal state；
- answer extractor 从 `S_T` 中抽取并验证最终答案。

这使“数学推理”从自由文本生成转化为可学习决策与可执行计算的组合。

### 3.3 External Value: EGR as an Executable Reasoning Interface for LLMs

EGR 不应被叙述为替代 LLM，而应被叙述为向 LLM 提供两个关键接口：

1. **Decision interface**：selector 告诉 LLM 当前状态下优先考虑哪些 theorem models。
2. **Execution interface**：applicator 检查 LLM 或 selector 提出的模型，并返回确定性的 symbolic state transition。

完整 EGR 进一步提供 progress 和 termination 信号，使 LLM 不必独自承担定理检索、符号计算、推理停止和答案确定四项任务。

## 4. Problem Formulation

给定圆锥曲线问题：

`x = (F, q)`，其中 `F` 是已知事实与约束，`q` 是查询目标。

系统构造双层状态：

- `S_t^sym`：精确 SymbolicState；
- `S_t^abs = phi(S_t^sym, q, t)`：供神经模型使用的 AbstractState。

theorem-model action space 记为 `M = {M_1, ..., M_K}`。在第 `t` 步：

```text
p_theta(M | S_t^abs) = Selector_theta(S_t^abs)
```

对于候选 `M_t`，只有当：

```text
Applicable(M_t, S_t^sym) = 1
```

时，才执行确定性状态转移：

```text
S_{t+1}^sym = T_{M_t}(S_t^sym)
```

状态熵估计器给出：

```text
H_phi(S_t) = estimated residual solving uncertainty
```

信息增益为：

```text
IG(M_t, S_t) = H_phi(S_t) - H_phi(T_{M_t}(S_t))
```

神经预测终止条件定义为：

```text
Stop_neural(S_t, q) = [H_phi(S_t) <= epsilon_H] AND AnswerReady(S_t, q)
```

最终答案为：

```text
answer_hat = Extract(S_T^sym, q)
```

其中 extractor 同时执行答案规范化、符号等价判断或代回验证。

## 5. Method

### 5.1 Problem-to-State Construction

EGR 首先将输入问题转换为显式 reasoning state。state 不是文本摘要，而是当前已知数学信息、查询目标和推理进度的结构化表示。

这一设计承担两个作用：

1. 把 theorem selection 从“根据整道题猜模型”转化为条件决策 `p(M | S_t)`；
2. 为 symbolic execution 提供可更新、可检查的数学环境。

### 5.2 Dual-Layer Reasoning State

#### SymbolicState

保存精确的几何对象、方程、参数、坐标、关系和约束，用于：

- theorem applicability checking；
- symbolic computation；
- state transition；
- answer extraction and validation。

#### AbstractState

将 `SymbolicState` 映射为固定维度神经表示，用于：

- theorem-model prediction；
- state entropy estimation；
- progress-aware decision making。

双层状态不是两个独立表示，而是通过 `phi` 持续同步：符号层保证精确性，抽象层保证可学习性。

### 5.3 Neural Theorem-Model Selector

selector 学习状态与下一 theorem model 的条件分布：

```text
p_theta(M_t | S_t^abs)
```

其任务不是预测最终答案，而是回答：

> Given the current reasoning state, which mathematical model should be executed next?

selector 可以输出 Top-1 动作，也可以输出 Top-k candidates 供 applicator、搜索策略或 LLM 使用。

### 5.4 Symbolic Model Applicator

每个 theorem model 定义为：

```text
M_i = (pre_i, trans_i)
```

其中：

- `pre_i(S)` 是显式 applicability condition；
- `trans_i(S)` 是确定性 symbolic transition。

applicator 接收 `(S_t^sym, M_t)`，执行：

1. 检查模型是否适用于当前状态；
2. 执行符号计算；
3. 将新事实、方程或参数写入状态；
4. 返回 `S_{t+1}^sym` 和可审计 transition record。

这一层将概率性的神经预测转换为确定性的数学执行结果。

### 5.5 State Entropy and Neural Continuation Control

`H(S)` 建模的不是答案类别熵，而是当前状态距离可解终态的 residual solving uncertainty。

它承担三个功能：

1. **Progress estimation**：估计当前问题已经解决到什么程度；
2. **Candidate ranking**：优先选择能够带来更高 information gain 的 theorem model；
3. **Neural continuation control**：决定 selector 是否需要继续预测下一模型。

论文中统一使用：

> `H(S)` controls the termination of neural model prediction.

不使用：

> `H(S)` proves the termination of the whole algorithm.

前者描述可学习控制机制，后者是需要独立数学证明的算法终止性命题。

### 5.6 Terminal-State Answer Extractor

当状态满足 neural stopping 与 answer-ready 条件后，answer extractor：

1. 根据 query type 定位目标变量或表达式；
2. 从 terminal SymbolicState 中求值或整理表达式；
3. 进行规范化、等价性判断或代回验证；
4. 输出最终答案以及对应 reasoning trace。

extractor 的意义是将“停止预测”与“答案已经确定”连接起来，避免把低熵状态直接等同于正确答案。

### 5.7 End-to-End Reasoning Algorithm

```text
Input problem (F, q)
    -> construct S_0^sym and S_0^abs
    -> estimate H(S_0)
    -> predict theorem candidates p(M | S_0^abs)
    -> check applicability and evaluate candidate transitions
    -> select and execute M_0
    -> obtain S_1^sym and rebuild S_1^abs
    -> repeat until entropy-controlled answer-ready state
    -> extract and validate final answer
```

## 6. Claimed Contributions

论文贡献建议锁定为以下四点：

1. **State-transition and model-prediction formulation**  
   We reformulate conic-section problem solving as sequential theorem-model prediction and executable state transition, replacing direct answer generation with an explicit mathematical decision process.

2. **Dual-state neural-symbolic execution**  
   We introduce a dual-layer state representation that couples a learnable AbstractState with an exact SymbolicState, enabling neural theorem selection and deterministic symbolic computation in one closed loop.

3. **Entropy-guided neural control**  
   We develop a learned state entropy that estimates residual solving progress, ranks candidate transitions through information gain, and determines when neural model prediction should terminate.

4. **Structured enhancement of LLM mathematical reasoning**  
   We expose EGR's selector and applicator as modular interfaces for LLMs, showing that theorem-model guidance and symbolic execution improve difficult mathematical reasoning beyond direct LLM generation.

贡献之间的逻辑关系必须保持为：

```text
new formulation
    -> requires dual state and selector/applicator
    -> requires entropy to control iterative prediction
    -> produces reusable structure that enhances LLMs
```

## 7. Experimental Story

实验不是三个孤立任务，而是依次回答三个层次的问题：

1. EGR 能否完成数学求解？
2. 核心 model-prediction 机制是否有效？
3. 这种机制能否作为模块增强 LLM？

### 7.1 Experiment I: End-to-End Answer Solving

**Research question**：EGR 是否比直接生成答案的方法更准确地解决圆锥曲线问题？

比较方法：

- representative closed/open LLMs；
- rule-based symbolic solver；
- neural selector only；
- EGR without entropy；
- full EGR。

核心指标：

- final answer accuracy；
- symbolic equivalence accuracy；
- invalid/unresolved rate；
- accuracy by curve type；
- accuracy by query type。

该实验支撑“EGR 是有效 solver”，但不能单独解释性能来自哪个组件。

### 7.2 Experiment II: Theorem-Model Prediction

**Research question**：在任意中间状态下，EGR selector 是否比 LLM 更准确地预测下一 theorem model？

输入必须是统一的 state information，输出是 theorem-model ID 或 Top-k candidates。

比较方法：

- LLM prompted with serialized state；
- LLM prompted with state and theorem catalog；
- learned EGR selector；
- EGR selector with applicability filtering；
- EGR selector with entropy/information-gain ranking。

核心指标：

- Top-1 / Top-3 / Top-5 accuracy；
- mean reciprocal rank；
- executable candidate rate；
- progress-producing candidate rate；
- accuracy by reasoning depth and theorem type。

该实验直接证明把数学推理建模为 `p(M | S)` 的价值。

### 7.3 Experiment III: LLM Augmentation

**Research question**：selector 与 applicator 分别通过什么机制提升 LLM 数学推理？

建议至少设置四个条件：

| Condition | Mechanism | What the LLM receives/uses |
| --- | --- | --- |
| Direct LLM | 无外部结构 | 原始题目 |
| LLM + Model Selector | 决策增强 | 每一步的 Top-k theorem models |
| LLM + Symbolic Applicator | 执行增强 | LLM 提议模型，applicator 检查并返回 state transition |
| LLM + Full EGR | 决策、执行与停止增强 | selector + applicator + entropy controller + extractor |

核心指标：

- final answer accuracy；
- theorem-selection accuracy；
- executable-step rate；
- symbolic computation error rate；
- correction rate：Direct LLM 错、增强后正确；
- harm rate：Direct LLM 对、增强后错误；
- average reasoning steps and token cost。

关键分析：

- `LLM + selector` 的提升说明错误主要来自“下一步做什么”；
- `LLM + applicator` 的提升说明错误主要来自“如何正确执行”；
- `LLM + full EGR` 的额外提升说明 progress/termination 和 answer extraction 也具有独立价值。

### 7.4 Required Ablations

为支撑完整方法，需要增加以下消融：

1. Single state vs dual-layer state；
2. selector only vs selector + applicability；
3. selector + applicator vs full EGR；
4. without `H(S)` vs entropy stopping only vs information-gain ranking only vs full entropy control；
5. learned `H(S)` vs heuristic progress；
6. answer extraction without vs with symbolic validation。

### 7.5 Analysis and Case Studies

至少提供：

1. 一条成功轨迹：theorem models、state changes、`H(S)` 和最终答案；
2. 一条 Direct LLM 失败但 LLM + selector 成功的案例；
3. 一条 LLM 计算错误但 applicator 修正的案例；
4. 一条 `H(S)` 避免过早停止或无效继续推理的案例；
5. theorem selection、symbolic execution、termination、answer extraction 四类错误分解。

## 8. Main Tables and Figures

### Figures

- **Figure 1**：EGR overall architecture，突出 `predict -> execute -> transition -> estimate -> stop -> extract`。
- **Figure 2**：Dual-layer state 与 selector/applicator 的数据流。
- **Figure 3**：successful reasoning trajectory，展示 theorem actions 与 `H(S)` 下降。
- **Figure 4**：LLM augmentation interfaces，分别展示 selector guidance 和 applicator execution。

### Tables

- **Table 1**：dataset、theorem-model space 和任务统计。
- **Table 2**：EGR 与多个 LLM 的 final answer accuracy。
- **Table 3**：EGR selector 与多个 LLM 的 theorem-model prediction accuracy。
- **Table 4**：LLM augmentation 主结果。
- **Table 5**：method ablation，尤其是 dual state、symbolic applicability 和 entropy。
- **Table 6**：按 curve/query/reasoning depth 的细粒度结果与错误分析。

## 9. Paper Structure

### 1. Introduction

1. LLM 数学推理的主要问题不只是知识不足，而是 theorem decision、symbolic execution 和 termination 被混在自由生成中。
2. 圆锥曲线是合适场景，因为其求解依赖明确的对象属性、定理模型和多步符号计算。
3. 提出核心转向：from answer generation to theorem-model prediction and state transition。
4. 简述 EGR 闭环。
5. 强调 EGR 既是独立 solver，也是 LLM reasoning interface。
6. 列出四项贡献。

### 2. Related Work

1. LLM mathematical reasoning；
2. neural-symbolic mathematical solvers；
3. theorem prediction and automated theorem proving；
4. verifier/tool-augmented LLM reasoning；
5. uncertainty、entropy and progress estimation。

### 3. Problem Formulation

定义 problem、dual state、theorem model、transition、state entropy、terminal state 和 answer。

### 4. EGR Method

1. framework overview；
2. problem-to-state construction；
3. dual-layer reasoning state；
4. neural theorem-model selector；
5. symbolic model applicator；
6. entropy-guided neural controller；
7. terminal-state answer extractor；
8. end-to-end algorithm。

### 5. EGR-Augmented LLM Reasoning

1. selector integration；
2. applicator integration；
3. full EGR integration；
4. interaction protocol and outputs。

### 6. Experiments

1. setup and baselines；
2. end-to-end answer solving；
3. theorem-model prediction；
4. LLM augmentation；
5. ablations；
6. entropy and trajectory analysis；
7. case studies and error analysis。

### 7. Conclusion

回到统一结论：显式 model prediction、symbolic state transition 和 progress-aware termination 构成了一种比直接 answer generation 更可控、更可解释，也更适合增强 LLM 的数学求解范式。

## 10. Abstract Blueprint

摘要按照以下五句组织：

1. **Problem**：LLMs directly generate mathematical solutions without explicitly separating theorem selection, symbolic execution, and reasoning termination.
2. **Reformulation**：We formulate conic-section problem solving as sequential theorem-model prediction and symbolic state transition.
3. **Method**：EGR combines a dual-layer state, neural theorem-model selector, executable symbolic applicator, learned state entropy, and terminal-state answer extractor.
4. **LLM value**：The selector and applicator further serve as modular reasoning interfaces that guide and verify LLM mathematical problem solving.
5. **Results**：Experiments demonstrate superior answer accuracy, theorem-model prediction, executable reasoning, and consistent gains when integrating EGR with diverse LLMs.

## 11. Terminology Lock

| Use consistently | Avoid or qualify |
| --- | --- |
| theorem model | 混用 theorem/rule/operator 而不定义 |
| theorem-model prediction | 把 selector 写成 answer predictor |
| symbolic model applicator | 仅称 calculator，弱化 state transition |
| state transition | 只说 reasoning step 而不说明状态变化 |
| residual solving uncertainty | 将 `H(S)` 写成 answer correctness probability |
| neural continuation/termination control | 将 `H(S)` 写成算法终止性证明 |
| terminal-state answer extraction | 将低熵直接等同于正确答案 |
| LLM reasoning enhancement | 没有接口与实验定义的笼统 augmentation |

## 12. Final Narrative Anchor

后续所有章节、图表和实验应围绕下面这条因果链展开：

> Direct answer generation obscures the mathematical decisions required for reliable problem solving. EGR makes these decisions explicit by representing a problem as a state, predicting the next theorem model from an abstract state, executing it over a symbolic state, estimating the remaining solving uncertainty to control neural continuation, and extracting the answer only from a terminal state. Because the selector and applicator are modular, executable interfaces, the same framework can guide and correct LLM mathematical reasoning.

任何不能服务这条因果链的模块描述或实验结果，都不应占据论文主线。
