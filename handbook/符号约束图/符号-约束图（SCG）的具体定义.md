这两个问题问得非常好，直指核心。让我深入思考并给出更具体的回答。

---

## 一、符号-约束图（SCG）的具体定义

### 1.1 图的形式化定义

符号-约束图是一个**二部图（Bipartite Graph）**：

$$\mathcal{G} = (\mathcal{V}_s, \mathcal{V}_c, \mathcal{E})$$

| 组件            | 定义       | 说明                 |
| --------------- | ---------- | -------------------- |
| $\mathcal{V}_s$ | 符号节点集 | 所有声明的变量/对象  |
| $\mathcal{V}_c$ | 约束节点集 | 所有约束/关系/等式   |
| $\mathcal{E}$   | 边集       | 符号与约束的关联关系 |

### 1.2 节点的属性

**符号节点** $v_s \in \mathcal{V}_s$：

```python
SymbolNode = {
    "name": str,           # 符号名，如 "G", "m", "F1"
    "type": Concept,       # 类型，如 Hyperbola, Number, Point
    "status": Status,      # determined | derivable | constrained | unknown
    "value": Optional,     # 如果已确定，存储具体值
    "is_query": bool,      # 是否是求解目标
}
```

**约束节点** $v_c \in \mathcal{V}_c$：

```python
ConstraintNode = {
    "id": int,
    "type": ConstraintType,  # definition | property | relation | inequality
    "expression": str,       # 原始表达式，如 "Expression(G) = (...)"
    "operator": str,         # 主操作符，如 "Expression", "Focus", "Distance"
    "is_used": bool,         # 是否已被使用/消耗
    "is_satisfiable": bool,  # 是否可满足
}
```

### 1.3 边的定义

边 $e = (v_s, v_c)$ 表示**符号 $v_s$ 出现在约束 $v_c$ 中**。

边的属性：
```python
Edge = {
    "symbol": SymbolNode,
    "constraint": ConstraintNode,
    "role": str,  # "subject" | "object" | "parameter"
    # 例如在 "Focus(G) = F1" 中，G是subject，F1是object
}
```

### 1.4 具体示例

让我用一个实际例子来展示：

```
题目：双曲线 x²/4 - y²/m² = 1 (m>0) 的一条渐近线方程是 5x-2y=0，求m

fact_expressions:
  c1: "G: Hyperbola"
  c2: "m: Number"  
  c3: "m > 0"
  c4: "Expression(G) = (x^2/4 - y^2/m^2 = 1)"
  c5: "Expression(OneOf(Asymptote(G))) = (5*x - 2*y = 0)"

query: "m"
```

**构建的符号-约束图：**

```
符号节点 V_s:                    约束节点 V_c:
┌──────────────┐               ┌─────────────────────────────┐
│ G: Hyperbola │───────────────│ c1: G: Hyperbola            │
│ status: part │               │ type: declaration           │
└──────────────┘               └─────────────────────────────┘
       │                                    
       │                       ┌─────────────────────────────┐
       ├───────────────────────│ c4: Expression(G) = (...)   │
       │                       │ type: definition            │
       │                       │ involves: {G, m}            │
       │                       └─────────────────────────────┘
       │                                    │
       │                                    │
┌──────────────┐                           │
│ m: Number    │───────────────────────────┘
│ status: unk  │               
│ is_query: T  │───────────────┌─────────────────────────────┐
└──────────────┘               │ c3: m > 0                   │
       │                       │ type: inequality            │
       │                       └─────────────────────────────┘
       │
       │                       ┌─────────────────────────────┐
       └───────────────────────│ c5: Asymptote(G) = (...)    │
                               │ type: property              │
                               │ involves: {G, m}            │
                               └─────────────────────────────┘
```

### 1.5 构建符号-约束图的好处

| 好处             | 说明                                      | 应用场景 |
| ---------------- | ----------------------------------------- | -------- |
| **可解性判断**   | 如果query符号与任何约束都不连通，则不可解 | 早期筛选 |
| **推理方向指导** | 从query符号出发，沿边找相关约束           | 搜索剪枝 |
| **瓶颈识别**     | 高度数的符号是关键变量                    | 优先求解 |
| **依赖分析**     | 可以分析符号间的依赖关系                  | 求解顺序 |
| **熵计算基础**   | 图的结构特征可以用于熵计算                | 状态评估 |

### 1.6 构建算法

```python
def build_scg(fact_expressions: str, query_expressions: str) -> SCGraph:
    """
    从fact_expressions构建符号-约束图
    """
    graph = SCGraph()
    
    # Step 1: 解析fact_expressions，分号分隔
    facts = fact_expressions.split(";")
    
    for fact in facts:
        fact = fact.strip()
        
        # Step 2: 判断是声明还是约束
        if ":" in fact and "=" not in fact:
            # 声明语句: "G: Hyperbola"
            name, concept = parse_declaration(fact)
            graph.add_symbol_node(name, concept)
            graph.add_constraint_node(fact, type="declaration")
            graph.add_edge(name, fact)
            
        elif ">" in fact or "<" in fact or ">=" in fact or "<=" in fact:
            # 不等式约束: "m > 0"
            symbols = extract_symbols(fact)
            graph.add_constraint_node(fact, type="inequality")
            for sym in symbols:
                graph.add_edge(sym, fact)
                
        else:
            # 等式/关系约束: "Expression(G) = (...)"
            symbols = extract_symbols(fact)
            operator = extract_main_operator(fact)
            graph.add_constraint_node(fact, type="relation", operator=operator)
            for sym in symbols:
                graph.add_edge(sym, fact)
    
    # Step 3: 标记query符号
    query_symbols = extract_symbols(query_expressions)
    for sym in query_symbols:
        if sym in graph.symbol_nodes:
            graph.symbol_nodes[sym].is_query = True
    
    return graph
```

---

## 二、推理步骤信息增益的量化

这是更核心的问题。让我从两个层面来回答：

### 2.1 如何判断"定理能否用上"

**核心思想：定理 = 模式匹配规则**

每个定理可以形式化为：

$$\text{Theorem} = (\text{Preconditions}, \text{Conclusion}, \text{Context})$$

| 组件          | 说明                | 示例（双曲线渐近线定理）         |
| ------------- | ------------------- | -------------------------------- |
| Preconditions | 前置条件/模式       | 存在双曲线G，且知道Expression(G) |
| Conclusion    | 结论/推导出的新知识 | Asymptote(G)的表达式             |
| Context       | 适用的上下文        | 曲线类型 = Hyperbola             |

**定理匹配算法：**

```python
class Theorem:
    def __init__(self, name, preconditions, conclusion, context):
        self.name = name
        self.preconditions = preconditions  # 需要满足的条件
        self.conclusion = conclusion        # 能推导出的新知识
        self.context = context              # 适用条件
    
    def can_apply(self, graph: SCGraph) -> Tuple[bool, Dict]:
        """
        检查定理是否可以应用于当前图
        
        Returns:
            (可否应用, 变量绑定)
        """
        # 1. 检查上下文：是否存在所需类型的符号
        for required_type in self.context:
            if not graph.has_symbol_of_type(required_type):
                return False, {}
        
        # 2. 模式匹配：检查前置条件
        bindings = self.match_preconditions(graph)
        if bindings is None:
            return False, {}
        
        # 3. 检查结论是否已知（避免重复推导）
        if self.conclusion_already_known(graph, bindings):
            return False, {}
        
        return True, bindings
    
    def apply(self, graph: SCGraph, bindings: Dict) -> SCGraph:
        """
        应用定理，返回新的图状态
        """
        new_graph = graph.copy()
        new_constraint = self.instantiate_conclusion(bindings)
        new_graph.add_derived_constraint(new_constraint)
        return new_graph
```

**具体的定理库示例：**

```python
# 双曲线渐近线定理
HYPERBOLA_ASYMPTOTE = Theorem(
    name="双曲线渐近线公式",
    preconditions=[
        PatternExists("G: Hyperbola"),
        PatternExists("Expression(G) = (x^2/A - y^2/B = 1)")
    ],
    conclusion="Asymptote(G) = (y = ±sqrt(B/A) * x)",
    context=["Hyperbola"]
)

# 椭圆离心率公式
ELLIPSE_ECCENTRICITY = Theorem(
    name="椭圆离心率公式",
    preconditions=[
        PatternExists("G: Ellipse"),
        PatternExists("Expression(G) = (x^2/A + y^2/B = 1)"),
        PatternKnown("a^2 = max(A, B)"),
        PatternKnown("c^2 = |A - B|")
    ],
    conclusion="Eccentricity(G) = c/a",
    context=["Ellipse"]
)

# 抛物线焦点公式
PARABOLA_FOCUS = Theorem(
    name="抛物线焦点公式", 
    preconditions=[
        PatternExists("G: Parabola"),
        PatternExists("Expression(G) = (y^2 = 4*p*x)")
    ],
    conclusion="Focus(G) = (p, 0)",
    context=["Parabola"]
)
```

### 2.2 如何量化信息增益

**关键洞察：信息增益 = 对目标的"距离减少"**

我提出一个**可计算的信息增益公式**：

$$IG(\text{step}) = \alpha \cdot \Delta_{symbols} + \beta \cdot \Delta_{constraints} + \gamma \cdot \Delta_{relevance}$$

其中：

| 分量                   | 定义                | 计算方法                |
| ---------------------- | ------------------- | ----------------------- |
| $\Delta_{symbols}$     | 确定的符号数量      | 统计status变化的符号    |
| $\Delta_{constraints}$ | 有效约束的增加      | 新约束数 - 消耗的约束数 |
| $\Delta_{relevance}$   | 与query的相关性变化 | 基于图距离的度量        |

**具体实现：**

```python
def compute_information_gain(
    graph_before: SCGraph, 
    theorem: Theorem,
    graph_after: SCGraph,
    query_symbol: str
) -> float:
    """
    计算应用一个定理的信息增益
    """
    
    # === 分量1: 符号确定度变化 ===
    delta_symbols = 0
    for sym in graph_after.symbol_nodes:
        status_before = graph_before.get_status(sym)
        status_after = graph_after.get_status(sym)
        
        # 状态等级: unknown=4, typed=3, constrained=2, derivable=1, determined=0
        delta_symbols += (status_level(status_before) - status_level(status_after))
    
    # === 分量2: 约束有效性变化 ===
    new_constraints = graph_after.constraints - graph_before.constraints
    useful_new = sum(1 for c in new_constraints if involves_query(c, query_symbol))
    delta_constraints = useful_new
    
    # === 分量3: 与query的图距离变化 ===
    dist_before = graph_before.shortest_path_to_determined(query_symbol)
    dist_after = graph_after.shortest_path_to_determined(query_symbol)
    delta_relevance = dist_before - dist_after
    
    # === 加权求和 ===
    alpha, beta, gamma = 1.0, 0.5, 2.0  # 可调参数
    ig = alpha * delta_symbols + beta * delta_constraints + gamma * delta_relevance
    
    return max(0, ig)  # 信息增益不能为负（或设为负表示无效步骤）
```

### 2.3 实际量化示例

让我用具体例子演示信息增益的计算：

```
问题：双曲线 x²/4 - y²/m² = 1 (m>0)，渐近线 5x-2y=0，求m

初始图 G₀:
├── 符号: {G(Hyperbola, constrained), m(Number, unknown, is_query)}
├── 约束: {c1, c2, c3, c4, c5}
├── query到determined的距离: ∞ (m未确定)
```

**Step 1: 应用"双曲线渐近线定理"**

```
定理匹配:
├── 前置条件: G是双曲线 ✓，Expression(G)已知 ✓
├── 结论: 推导出渐近线表达式 y = ±(m/2)x

状态变化:
├── 新增约束: c6 = "Asymptote(G) = (y = ±(m/2)x)"
├── m的关联约束: +1 (c6涉及m)

信息增益计算:
├── Δ_symbols = 0 (m仍是unknown)
├── Δ_constraints = 1 (有用的新约束)
├── Δ_relevance = 1 (m到确定值的路径缩短了)
└── IG₁ = 1.0×0 + 0.5×1 + 2.0×1 = 2.5
```

**Step 2: 解析已知渐近线方程**

```
操作: 从 5x-2y=0 提取斜率 5/2

状态变化:
├── 新增约束: c7 = "given_slope = 5/2"
├── c7是确定值

信息增益计算:
├── Δ_symbols = 0
├── Δ_constraints = 1
├── Δ_relevance = 0.5 (提供了可比较的值)
└── IG₂ = 0 + 0.5 + 1.0 = 1.5
```

**Step 3: 联立求解 m/2 = 5/2**

```
操作: 代入求解

状态变化:
├── m: unknown → determined (m = 5)
├── 消耗约束: c6, c7

信息增益计算:
├── Δ_symbols = 4 (unknown到determined差4级)
├── Δ_constraints = 0 (消耗2个，无新增)
├── Δ_relevance = ∞→0 = 很大
└── IG₃ = 4.0 + 0 + ∞ → 非常高
```

### 2.4 更本质的量化思路：基于"可解性"的熵

让我提出一个更本质的量化方法：

**核心观察：** 信息增益本质上是**让query从"不可解"变得"更可解"的程度**

定义**可解性得分**：

$$\text{Solvability}(q, \mathcal{G}) = \begin{cases}
1 & \text{if } q \text{ is determined} \\
\frac{|\text{constraints involving } q|}{|\text{free variables in path to } q|} & \text{otherwise}
\end{cases}$$

那么：

$$IG(\text{step}) = \text{Solvability}(q, \mathcal{G}_{after}) - \text{Solvability}(q, \mathcal{G}_{before})$$

**直观理解：**
- 约束越多，分子越大
- 自由变量越少，分母越小
- 两者都让可解性提高

### 2.5 实用的判断策略

对于"如何判断定理能否用上"，我建议使用**多层筛选策略**：

```
Layer 1: 类型匹配（快速筛选）
├── 当前图中有哪些曲线类型？
├── 定理适用于哪些类型？
└── 交集非空才继续

Layer 2: 模式匹配（精确匹配）
├── 定理的前置条件能否在图中找到匹配？
├── 使用图的子图匹配算法
└── 找到绑定才继续

Layer 3: 效用评估（收益判断）
├── 应用定理后，信息增益是多少？
├── IG > threshold 才值得应用
└── 优先选择IG最大的
```

```python
def select_best_theorem(graph: SCGraph, theorems: List[Theorem], query: str) -> Theorem:
    """
    选择最佳的下一步定理
    """
    candidates = []
    
    for theorem in theorems:
        # Layer 1: 类型匹配
        if not type_compatible(graph, theorem):
            continue
        
        # Layer 2: 模式匹配
        can_apply, bindings = theorem.can_apply(graph)
        if not can_apply:
            continue
        
        # Layer 3: 效用评估
        graph_after = theorem.apply(graph, bindings)
        ig = compute_information_gain(graph, theorem, graph_after, query)
        
        candidates.append((theorem, bindings, ig))
    
    # 选择信息增益最大的
    if not candidates:
        return None
    
    candidates.sort(key=lambda x: x[2], reverse=True)
    return candidates[0][0], candidates[0][1]
```

---

## 三、综合视角：信息熵与图结构的统一

现在让我把两个问题统一起来：

### 基于图的熵定义

$$H(\mathcal{G}) = \sum_{v_s \in \mathcal{V}_s} H_{local}(v_s) \cdot w(v_s, q)$$

其中：
- $H_{local}(v_s)$ = 符号$v_s$的局部熵（基于其状态和关联约束）
- $w(v_s, q)$ = 符号$v_s$与query $q$的相关性权重

**局部熵计算：**

$$H_{local}(v_s) = \log\left(\frac{\text{degree}(v_s) + 1}{\text{determined\_neighbors}(v_s) + 1}\right) \cdot \text{status\_factor}(v_s)$$

**相关性权重：**

$$w(v_s, q) = \frac{1}{\text{graph\_distance}(v_s, q) + 1}$$

### 推理过程可视化

```
初始图                    应用定理1                  应用定理2                 求解完成
   
  G ──── c4 ──── m         G ──── c4 ──── m          G ──── c4 ──── m          G ──── c4 ──── m=5
  │              │         │      │       │          │      │       │          │      │       │
  │              │   =>    │      c6      │    =>    │      c6 ═══ c7    =>    │      │       │
  c1             c3        c1     │       c3         c1     │       c3         c1             c3
                           渐近线公式              斜率匹配            确定m

H = 5.0                  H = 3.5                   H = 2.0                   H = 0
                         IG₁ = 1.5                 IG₂ = 1.5                 IG₃ = 2.0
```

---

## 四、总结与下一步

### 关于你的问题的直接回答：

**Q1: 图的节点和边具体是什么？**
- 节点 = 符号节点（变量）+ 约束节点（关系/等式）
- 边 = 符号出现在约束中的关系
- 是一个二部图结构

**Q2: 推理步骤能量化吗？如何判断定理能否用上？**
- **能量化**：通过$IG = \alpha \Delta_{symbols} + \beta \Delta_{constraints} + \gamma \Delta_{relevance}$
- **定理匹配**：三层筛选（类型匹配 → 模式匹配 → 效用评估）

### 下一步建议：

1. **实现原型**：我可以帮你实现一个简单的SCG构建器和熵计算器
2. **验证假设**：在Conic10K的子集上验证"熵随推理单调递减"
3. **构建定理库**：基于Conic10K的94个operators构建定理规则

你想先从哪个方向开始？