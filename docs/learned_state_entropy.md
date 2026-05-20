# Learned State Entropy H(S) for EGR

## 1. 核心定位

EGR 中第二层 `H(S)` 应被定义为 **state-level residual reasoning uncertainty**，即当前符号状态距离目标答案还剩多少定理级推理工作。它不是严格的信息论解空间熵，因为圆锥曲线题同时包含连续变量、符号表达式、等价变形、隐式约束和多条可行推理路径，真实解空间分布几乎不可直接计算。

更适合论文和系统实现的定义是：

$$
H_\phi(S_t, q) \in [0, 1],
$$

其中 `S_t` 是当前推理状态，`q` 是查询目标，$H_\phi(S_t, q)$ 表示从当前状态到目标可确定状态的剩余推理不确定性。值越大，说明当前状态距离可解状态越远；值越小，说明已知信息越接近足以提取答案。

在 EGR 中，`H(S)` 的作用不是替代 theorem selector，而是提供一个可量化的进度函数：

$$
\operatorname{InfoGain}(y; S_t)
= H_\phi(S_t, q) - H_\phi(S_{t+1}^{(y)}, q),
$$

其中

$$
S_{t+1}^{(y)} = T_y(S_t)
$$

表示在当前状态上应用定理动作 `y` 后得到的新状态。这样，每个 theorem action 的价值可以被解释为它减少了多少剩余推理工作。



## 2. 为什么不直接计算真实 Shannon 熵

严格的信息论状态熵可写成：

$$
H_{\text{true}}(S_t)
= -\int p(z \mid S_t, q)\log p(z \mid S_t, q)\,dz,
$$

其中 `z` 表示满足当前条件并与目标相关的潜在解变量或中间符号。这个定义理论上优雅，但在 EGR 当前场景中难以落地，原因包括：

- `z` 的空间既有离散对象，也有连续参数和符号表达式。
- 不同表达式可能数学等价，但字符串形式不同。
- 部分约束只能通过定理动作逐步显式化，初始状态中并没有完整可解的约束系统。
- 同一问题可能存在多条合法推理路径，路径长度和中间状态不唯一。
- 精确计算可行域体积或后验分布需要强符号求解器，成本高且不稳定。

因此，论文中应避免声称 EGR 精确估计解空间 Shannon entropy。更严谨的说法是：EGR learns a state-entropy proxy for residual theorem-level uncertainty。



## 3. 可接近真实熵的结构化近似

如果希望让 `H(S)` 更接近“解空间缩小”的直觉，可以构造结构化近似：

$$
H_{\text{struct}}(S_t, q)
= \alpha U_q(S_t)
+ \beta D(S_t)
+ \gamma C_{\text{unresolved}}(S_t)
+ \delta R_q(S_t)
- \eta K_q(S_t),
$$

其中：

- `U_q(S_t)`：与查询目标相关的未确定符号数量。
- `D(S_t)`：近似自由度，例如未知量数量减去有效约束数量。
- `C_unresolved(S_t)`：尚未被利用或尚不能闭合的约束数量。
- `R_q(S_t)`：当前已知事实到查询目标的图距离或依赖距离。
- `K_q(S_t)`：已推导出的、与查询目标相关的有效知识数量。

该方案可以基于 Symbol-Constraint Graph 实现。图中节点表示变量、曲线对象、参数和查询目标，边表示方程、几何关系、定理约束和依赖关系。节点可以分为：

| 状态 | 含义 | 局部不确定性 |
| --- | --- | ---: |
| `determined` | 已知具体值或可直接提取答案 | 0.00 |
| `derivable` | 当前约束下可直接推出 | 0.25 |
| `constrained` | 有约束但尚不能直接确定 | 0.50 |
| `typed` | 只知道类型 | 0.75 |
| `unknown` | 基本未知 | 1.00 |

结构化近似适合作为 heuristic baseline 或 learned model 的辅助特征，但不建议作为唯一主方法。原因是手写权重和状态分类容易引入任务偏置，且很难覆盖所有 Conic10K 推理形态。



## 4. 推荐主路线：监督学习 H(S)

最适合当前 EGR 论文和系统实现的方案是 learned `H(S)`。训练数据来自已有专家定理序列：

$$
S_0 \xrightarrow{y_0} S_1 \xrightarrow{y_1}
\cdots
\xrightarrow{y_{T-1}} S_T.
$$

对每个中间状态 $S_t$ 构造监督标签：

$$
r_t = T - t,
$$

$$
\tilde{H}(S_t) = \frac{T-t}{T},
$$

$$
\operatorname{progress}(S_t) = 1 - \tilde{H}(S_t) = \frac{t}{T}.
$$

模型学习：

$$
h_\phi(S_t, q) \rightarrow [0,1],
$$

基础损失为：

$$
\mathcal{L}_{\text{mse}}
= \frac{1}{N}\sum_{i,t}
\left(h_\phi(S_{i,t}, q_i) - \tilde{H}_{i,t}\right)^2.
$$

这个定义把 `H(S)` 变成 “归一化剩余定理步数” 的可学习参数/指标。它与 EGR 的 theorem-action formulation 一致，也能直接服务 InfoGain 计算。



## 5. 标签设计的增强版本

仅使用 `remaining_steps / T` 是一个好的起点，但它有两个风险：一是模型可能过度依赖 `reasoning_depth`；二是专家路径不一定是最短或最优路径。建议逐步扩展为三类标签。

### 5.1 Gold-Suffix Remaining

沿专家序列构造标签：

$$
\tilde{H}_{\text{gold}}(S_t)
= \frac{T-t}{T}.
$$

优点是简单、稳定、易复现。缺点是学习到的是专家路径剩余长度，而不是当前状态的真实最短可解距离。

### 5.2 Executable Shortest Remaining

从当前状态 `S_t` 出发，在当前 theorem library 中运行受限搜索，估计到目标状态或可提取正确答案状态的最短剩余步数：

$$
d^*(S_t, q)
= \min_{\tau}
|\tau|
\quad
\text{s.t.}\quad
\operatorname{Extract}(T_\tau(S_t), q)=a^*.
$$

归一化标签：

$$
\tilde{H}_{\text{oracle}}(S_t)
= \min\left(1, \frac{d^*(S_t, q)}{d_{\max}}\right).
$$

如果搜索无法找到可行补全路径，可以标记为 unknown 或赋予高熵标签。这个标签更接近“真实剩余推理工作”，但计算成本更高，适合在 dev/test 子集或缓存后的训练集中使用。

### 5.3 Contrastive Path Label

为同一初始问题构造三类路径：

- `gold/correct path`：专家或可执行正确路径。
- `model path`：模型预测路径。
- `random path`：随机可用 theorem 路径。

希望正确路径上的状态熵下降更稳定，随机路径或错误路径的熵下降更弱。可以加入排序约束：

$$
\mathcal{L}_{\text{rank}}
= \max\left(0,
m + H_\phi(S_{t+1}^{+}) - H_\phi(S_{t+1}^{-})
\right),
$$

其中 `S_{t+1}^+` 是正确或高质量转移后的状态，`S_{t+1}^-` 是随机或失败转移后的状态，`m` 是 margin。

## 6. 模型结构路线

### 6.1 Baseline：Linear / Ridge Estimator

输入：

$$
x_t = \operatorname{vec}(S_t^{abs}, q) \in \mathbb{R}^{28}.
$$

模型：

$$
H_\phi(S_t, q)
= \operatorname{clip}_{[0,1]}(w^\top x_t + b).
$$

优点：

- 可解释，训练稳定。
- 适合作为论文 baseline。
- 方便和 heuristic entropy 对比。

缺点：

- 表达力弱。
- 难以捕捉状态特征之间的非线性交互。
- 容易把 `reasoning_depth` 当作捷径。

### 6.2 推荐主模型：MLP State Entropy Estimator

主模型建议使用轻量 MLP：

$$
H_\phi(S_t, q)
= \sigma\left(f_\phi(x_t)\right),
$$

其中：

$$
f_\phi: \mathbb{R}^{d} \rightarrow \mathbb{R}.
$$

推荐输入包括：

- `AbstractState.to_vector()`：曲线类型、查询类型、信息特征、完整度、深度。
- query-conditioned features：查询目标是否已被直接约束、目标相关参数数量。
- state-transition features：已应用模型数量、重复模型标记、当前状态新增事实数量。
- 可选的 ablation 输入：去掉 `reasoning_depth` 的版本，用于证明模型不是只学步数。

推荐损失：

$$
\mathcal{L}
= \mathcal{L}_{\text{mse}}
+ \lambda_{\text{mono}}\mathcal{L}_{\text{mono}}
+ \lambda_{\text{rank}}\mathcal{L}_{\text{rank}}.
$$

其中 monotonicity loss 只在 gold/correct executable path 上使用：

$$
\mathcal{L}_{\text{mono}}
= \frac{1}{M}\sum_{i,t}
\max\left(0, H_\phi(S_{i,t+1}) - H_\phi(S_{i,t})\right).
$$

它鼓励专家路径上的熵非递增，即有效推理应降低剩余不确定性。

### 6.3 高级版本：Graph Entropy Estimator

长期可以把 `SymbolicState` 转成 Symbol-Constraint Graph，并用 GNN 预测 `H(S)`：

$$
H_\phi(S_t, q)
= \operatorname{Readout}_{q}\left(\operatorname{GNN}_\phi(G_t)\right).
$$

该方案表达力最强，也最接近结构化数学状态，但实现成本较高，需要稳定的图构造、节点/边类型 schema、query-conditioned readout 和更复杂的训练流程。建议作为后续增强或 future work，而不是第一版论文主实现。

## 7. 推理时如何使用 H(S)

推理阶段不应只计算当前状态的 `H(S_t)`，而要对候选 theorem action 做状态模拟：

```text
for y in candidate_theorems:
    if can_apply(y, S_t):
        S_next = apply(y, copy(S_t))
        IG(y) = H(S_t) - H(S_next)
        Score(y) = lambda_1 * P(y | S_t) + lambda_2 * IG(y)
```

更完整的决策公式为：

$$
\operatorname{Score}(y; S_t)
= \lambda_1 \pi_\theta(y \mid S_t)
+ \lambda_2
\left[
H_\phi(S_t, q) - H_\phi(T_y(S_t), q)
\right]
+ \lambda_3 R(y, S_t),
$$

其中 `R(y, S_t)` 可以表示 rule validity、重复惩罚、路径长度惩罚或 prediction confidence calibration。若使用 `H(Y|X)`，更适合将其作为状态级置信度门控，而不是同一状态下对所有候选动作的常数扣分：

$$
c(S_t)
= 1 - \frac{H_\theta(Y \mid S_t)}{\log |\mathcal{A}_{valid}(S_t)|}.
$$

然后：

$$
\operatorname{Score}(y; S_t)
= \lambda_1 c(S_t)\pi_\theta(y \mid S_t)
+ \lambda_2 \operatorname{InfoGain}(y; S_t).
$$

## 8. 预期效果与实验验证

如果 learned `H(S)` 成立，应观察到以下效果。

### 8.1 Progress Correlation

`H(S)` 应与 normalized remaining steps 正相关：

$$
\rho\left(H_\phi(S_t), \frac{T-t}{T}\right) > 0.
$$

报告指标：

- Pearson correlation。
- Spearman correlation。
- MAE / RMSE。
- depth-ablated version 的相关性。

### 8.2 Trajectory Monotonicity

在正确或专家路径上，熵应整体下降：

$$
H_\phi(S_0) \ge H_\phi(S_1) \ge \cdots \ge H_\phi(S_T).
$$

报告指标：

$$
\operatorname{MonoRate}
= \frac{1}{T}\sum_{t=0}^{T-1}
\mathbf{1}\left[H_\phi(S_{t+1}) \le H_\phi(S_t)\right].
$$

### 8.3 Path Quality Separation

正确路径的信息增益应高于随机路径或错误路径：

$$
\mathbb{E}_{y \sim \tau^+}
\left[\operatorname{InfoGain}(y)\right]
>
\mathbb{E}_{y \sim \tau^-}
\left[\operatorname{InfoGain}(y)\right].
$$

报告指标：

- correct/model/random path 的平均 entropy delta。
- correct vs failed path 的 `InfoGain` 分布。
- failure bucket 下的初始熵、最终熵、熵下降量。

### 8.4 Search Efficiency and Answer Accuracy

最终需要通过 ablation 证明 `H(S)` 不只是分析指标，也能改善搜索：

| Variant | H(S) source | Expected use |
| --- | --- | --- |
| no entropy | none | 只用 `P(Y|X)` 或规则 |
| heuristic entropy | handcrafted | 验证手写进度函数 |
| linear entropy | ridge regressor | 当前可解释 learned baseline |
| MLP entropy | neural regressor | 推荐主模型 |
| MLP entropy without depth | ablation | 排除 depth shortcut |

报告指标：

- theorem selection Top-1/Top-3/Top-5。
- reasoning success。
- average steps。
- final answer accuracy。
- failure reason distribution。

论文中要保持边界：`H(S)` 首先是 mechanism evidence。只有当 final answer accuracy 或 average steps 在统一协议下改善时，才能声称它提升端到端推理效果。

## 9. 论文中的叙述逻辑

推荐在 Method 中这样组织：

1. EGR 将圆锥曲线求解形式化为 theorem-action state transition。
2. 符号层保证动作可执行，神经层给出 theorem policy `P(Y|S)`。
3. 仅有 policy 不足以判断一个动作是否真正推进求解，因此引入 state entropy `H(S)`。
4. `H(S)` 被定义为 residual theorem-level uncertainty，而不是严格解空间 Shannon entropy。
5. 用专家定理序列监督学习 `H(S)`，使它拟合归一化剩余推理步数。
6. 推理时通过模拟候选动作计算 InfoGain，选择最大程度降低 `H(S)` 的有效动作。
7. 实验分别验证 `H(S)` 的进度相关性、轨迹单调性、路径质量区分能力和搜索效率贡献。

可直接使用的英文表述：

> We define state entropy as a learned proxy for residual theorem-level uncertainty. Given a symbolic state and a query, the estimator predicts the normalized amount of theorem-action reasoning still required to reach an answer-determinable state. This formulation does not assume access to the true solution-space entropy; instead, it provides a tractable progress signal learned from annotated theorem-action trajectories.

第二段：

> During inference, EGR evaluates a candidate theorem action by simulating its symbolic transition and measuring the induced entropy reduction. The resulting information gain converts theorem application into a progress-aware decision problem, allowing the system to prefer actions that are both policy-plausible and expected to reduce the remaining solving burden.

## 10. 建议的落地步骤

短期实现：

1. 保留现有 heuristic entropy 和 learned-linear estimator 作为 baseline。
2. 新增 MLP `H(S)` estimator，输入 `AbstractState` 向量及 query-conditioned features。
3. 构建 depth ablation 数据版本，分别训练 with-depth 和 without-depth。
4. 在 gold/correct executable paths 上加入 monotonicity loss。
5. 增加 random/failed transition 的 contrastive ranking loss。
6. 输出统一报告：correlation、MAE、monotonicity、entropy delta、path separation。

中期实现：

1. 为每个 `S_t` 缓存候选 theorem transition 的 `H(S_next)`。
2. 比较 `heuristic / linear / MLP` 三种 InfoGain 在 search ablation 中的效果。
3. 将 entropy trajectory 与 final answer correctness join，避免只报告 process-level 指标。
4. 做 lambda sweep，确定 `P(Y|S)` 与 `InfoGain` 的最佳权重区间。

长期实现：

1. 构造 Symbol-Constraint Graph 表示。
2. 实现 query-conditioned graph entropy estimator。
3. 探索 action-conditioned delta predictor：

$$
\Delta H_\psi(S_t, y)
\approx H(S_t) - H(T_y(S_t)).
$$

这个模型可以避免对每个候选动作都执行完整 symbolic simulation，但应作为效率优化，而不是第一版核心定义。

## 11. 最终贡献表述

EGR 第二层 `H(S)` 的贡献可以概括为：

> EGR introduces a learned state-entropy estimator for theorem-action reasoning. Instead of attempting to compute intractable solution-space entropy, it learns residual reasoning uncertainty from annotated theorem trajectories. This estimator enables information-gain-based planning over executable symbolic transitions and provides a measurable progress signal for high-difficulty conic-section problem solving.

中文概括：

> `H(S)` 是 EGR 中最有潜力的核心机制：它把“当前状态离答案还有多远”从模糊直觉变成可监督学习、可验证、可用于搜索决策的数值信号。它既服务于论文中的理论叙述，也服务于系统中的路径规划与消融实验。
