第二层 `H(S)` 我建议把它正式定义成：

> `H(S)` is a learned proxy for residual reasoning uncertainty: how much theorem-level work remains before the current symbolic state can determine the target answer.

中文就是：`H(S)` 不是“真实解空间 Shannon 熵”，而是“当前状态距离可求解状态还剩多少推理负担”的可学习代理量。

**1. 理论定位**
最稳的形式化是：

```text
S_t = 当前符号状态
q = 待求目标
τ* = 从 S_t 到答案状态的最短或最优推理补全路径
H(S_t) ≈ E[length(τ*) | S_t, q]
```

也就是说，`H(S)` 衡量的不是变量值域的大小，而是“从当前状态到答案还需要多少有效定理动作”。这更贴合 EGR，因为 EGR 的基本单位本来就是 theorem action。

因此推理中：

```text
InfoGain(y) = H(S_t) - H(S_{t+1})
```

含义就是：应用定理 `y` 后，预期剩余推理负担减少了多少。

**2. 最接近真实信息论熵的近似方案**
如果想尽量接近“解空间熵”，可以做一个 constraint-space approximation：

```text
H_csp(S) = entropy over possible assignments of query-relevant variables
```

实现上可以把状态转成符号约束图或 CSP：

- 节点：变量、曲线对象、参数、目标量。
- 边：方程、几何关系、定理约束、已知条件。
- 对每个 query-relevant 变量估计状态：unknown / typed / constrained / derivable / determined。
- 用自由度、有效约束数、query 距离、变量是否已定值来近似熵。

一个可操作公式：

```text
H_struct(S) =
  α · undetermined_query_symbols
+ β · degrees_of_freedom
+ γ · unresolved_constraints
+ δ · distance_to_query
- η · derived_query_relevant_facts
```

这比当前 heuristic 更接近“解空间缩小”的直觉，但它仍然不是严格 Shannon entropy，因为连续变量、符号表达式等价、约束可解性都很难精确处理。

**3. 最推荐的实现：监督学习 H(S)**
真正适合论文和系统的是 learned `H(S)`。

训练数据来自已有专家定理序列：

```text
problem i:
S_0 --y_0--> S_1 --y_1--> ... --y_{T-1}--> S_T
```

对每个状态构造标签：

```text
remaining_steps(S_t) = T - t
normalized_H(S_t) = (T - t) / T
progress(S_t) = t / T
```

模型学习：

```text
h_φ(S_t, q) -> [0, 1]
L_entropy = MSE(h_φ(S_t), normalized_remaining_steps)
```

这就是当前 learned-linear 的基本方向，但后续可以增强。

**4. 更强的标签设计**
只用 `remaining_steps / sequence_length` 有一个问题：模型可能偷学 `reasoning_depth`。因此建议做三个标签版本：

```text
H_step(S_t) = normalized remaining theorem steps
H_goal(S_t) = 1 - answer_extractability_score
H_oracle(S_t) = shortest remaining path length under executable theorem library
```

其中 `H_oracle` 最强：对当前状态运行受限 beam search，找到到达答案或 gold suffix 的最短可执行补全路径。这样 `H(S)` 就不是只复刻专家步骤，而是逼近“当前状态真实可解距离”。

**5. 模型结构**
可以分三档实现。

第一档，当前可落地：

```text
Linear / Ridge regressor over AbstractState.to_vector()
```

优点是可解释、稳定、容易做 ablation。缺点是表达力弱。

第二档，推荐论文主模型：

```text
MLP entropy estimator
input: AbstractState vector + query type + last action + candidate-action features
output: scalar H(S)
```

损失：

```text
L = MSE(H_pred, H_label)
  + λ_mono · max(0, H(S_{t+1}) - H(S_t))
```

加一个 monotonicity loss，鼓励专家路径上熵非递增。

第三档，后续增强：

```text
Graph Neural Network over Symbol-Constraint Graph
```

输入完整符号-约束图，输出 query-conditioned state entropy。这个最漂亮，但实现成本高，适合作为 future work 或高级版本。

**6. 推理时如何用**
推理阶段不要只算当前 `H(S)`，而是对候选定理做模拟：

```text
for y in candidate_theorems:
    if can_apply(y, S_t):
        S_next = apply(y, copy(S_t))
        IG(y) = H(S_t) - H(S_next)
        Score(y) = λ1 P(y|S_t) + λ2 IG(y)
```

这里 `H(S)` 的作用是把“定理是否有用”从局部规则判断变成可量化的进度判断。

**7. 预期效果**
如果 `H(S)` 做得好，应该看到四类效果：

1. 熵值随专家推理路径下降。
2. `H(S)` 与 remaining steps 高相关。
3. 正确路径的平均 `InfoGain` 高于错误路径或随机路径。
4. 在搜索中，full EGR 用更少步骤达到同等或更高最终答案准确率。

论文里最稳的贡献表述是：

> We learn a state-entropy estimator that maps symbolic reasoning states to residual theorem-level uncertainty. This estimator converts theorem application into an information-gain decision problem, enabling EGR to quantify reasoning progress and prefer transitions that maximally reduce remaining solving burden.

**8. 我建议的实现路线**
先不要直接上 GNN。最务实路线：

1. 保留当前 learned-linear 作为 baseline。
2. 新增 MLP `H(S)` estimator。
3. 标签从 `remaining_steps/T` 扩展为 `gold suffix remaining + executable shortest remaining`。
4. 加 monotonicity loss。
5. 做 ablation：no entropy / heuristic entropy / linear entropy / MLP entropy。
6. 报告：Pearson、Spearman、MAE、monotonicity、avg steps、final answer accuracy。

这样第二层 `H(S)` 就会从“一个启发式分数”变成论文里可以站住的核心方法模块。