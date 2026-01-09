# EGR-SCG: 基于信息熵的符号-约束图框架

> **Entropy-Guided Reasoning with Symbol-Constraint Graph**
> 
> 本文档定义了用于圆锥曲线问题求解的符号-约束图（SCG）框架，以及基于信息熵的推理评估方法。

---

## 一、研究动机

### 1.1 核心问题

在数学问题求解（Math Problem Solving）中，现有方法通常缺乏显式的指标来：
1. **判断可解性**：题目能否求解？
2. **指导推理方向**：题目该朝着哪个方向进行推理求解？
3. **评估求解进度**：当前求解步骤距离最终答案还有多远？

### 1.2 核心思想

将数学问题求解建模为**信息熵减过程**：
- **初始状态**：已知条件包含有限信息，信息熵较高（不确定性大）
- **求解过程**：通过推理步骤逐步增加信息量，降低信息熵
- **终止条件**：信息熵降到0，问题完全确定，得到答案

```
初始状态 ──[推理步骤1]──> 中间状态1 ──[推理步骤2]──> ... ──> 答案
   H₀                      H₁ < H₀                        H = 0
```

### 1.3 参考工作

本框架受 **HGR (Hologram Reasoning)** 启发，HGR 使用异构属性图（Hologram）表示几何问题：
- **Vertices**: 几何基元（点、线、角等）
- **Edges**: 几何关系（平行、垂直、相似等）
- **Attributes**: 数学属性 + 视觉属性

我们在此基础上：
1. 适配圆锥曲线问题的特点
2. 引入**显式的信息熵**作为状态评估指标
3. 使用**信息增益**指导推理方向选择

---

## 二、符号-约束图（SCG）定义

### 2.1 形式化定义

符号-约束图定义为四元组：

$$\mathcal{G} = (\mathcal{V}, \mathcal{E}, \mathcal{A}, \mathcal{H})$$

| 组件 | 符号 | 定义 | 对应Conic10K元素 |
|------|------|------|-----------------|
| 对象节点集 | $\mathcal{V}$ | 数学对象/变量 | 20个Concept |
| 关系边集 | $\mathcal{E}$ | 对象间的关系 | 94个Operators |
| 属性集 | $\mathcal{A}$ | 具体值、表达式、约束 | fact_expressions中的值 |
| 熵状态集 | $\mathcal{H}$ | 每个节点的确定程度 | 新增，用于信息熵计算 |

### 2.2 对象节点（Object Node）

对象节点代表问题中的数学对象，对应Conic10K的**Concept**：

```python
class ObjectNode:
    """对象节点 - 对应Conic10K的Concept"""
    
    id: str              # 符号名，如 "G", "m", "F1"
    type: str            # 类型，如 "Ellipse", "Number", "Point"
    attributes: Dict     # 属性值字典
    entropy: float       # 局部熵（确定程度），范围[0, 1]
    is_query: bool       # 是否是求解目标
```

**节点类型（20个Concept）**：

| 类别 | Concept | 说明 |
|------|---------|------|
| 圆锥曲线 | Ellipse, Hyperbola, Parabola, Circle, ConicSection | 曲线对象 |
| 几何元素 | Point, Line, LineSegment, Ray, Curve | 基本几何元素 |
| 其他对象 | Angle, Triangle, Vector | 角、三角形、向量 |
| 数值类型 | Number, Real | 数值变量 |
| 特殊常量 | Origin, xAxis, yAxis, axis | 坐标系元素 |

**节点的熵状态分级**：

| 等级 | 状态 | entropy值 | 含义 |
|------|------|-----------|------|
| 0 | determined | 0.0 | 已知具体数值 |
| 1 | derivable | 0.25 | 可从当前约束直接推出 |
| 2 | constrained | 0.5 | 有约束但不能直接求出 |
| 3 | typed | 0.75 | 只知道类型 |
| 4 | unknown | 1.0 | 完全未知 |

### 2.3 关系边（Relation Edge）

关系边代表对象之间的关系，对应Conic10K的**Operator**：

```python
class RelationEdge:
    """关系边 - 对应Conic10K的Operator"""
    
    id: str                # 边的唯一标识
    operator: str          # 操作符名，如 "Expression", "Focus"
    arguments: List[str]   # 参与的节点ID列表
    result: Optional[str]  # 结果节点ID（如果有）
    value: Any             # 等式右边的值/表达式
    is_used: bool          # 是否已被使用/消耗
```

**边的类型（主要Operator分类）**：

| 类别 | Operators | 说明 |
|------|-----------|------|
| 表达式定义 | Expression, LocusEquation | 定义对象的数学表达式 |
| 属性获取 | Focus, Center, Vertex, Asymptote, Directrix | 获取曲线的特征元素 |
| 度量属性 | Eccentricity, Radius, Length, Area, Distance | 数值度量 |
| 几何关系 | PointOnCurve, Intersection, IsTangent, IsParallel | 对象间的几何关系 |
| 坐标相关 | Coordinate, XCoordinate, YCoordinate | 坐标信息 |
| 运算操作 | Abs, Sin, Cos, Tan, DotProduct, VectorOf | 数学运算 |

### 2.4 图结构示例

**问题**：双曲线 $\frac{x^2}{4} - \frac{y^2}{m^2} = 1$ (m>0) 的一条渐近线方程是 $5x-2y=0$，求 $m$

**fact_expressions**:
```
G: Hyperbola; m: Number; m>0; 
Expression(G) = (x^2/4 - y^2/m^2 = 1); 
Expression(OneOf(Asymptote(G))) = (5*x - 2*y = 0)
```

**SCG表示**：

```
┌─────────────────── Object Nodes ───────────────────┐
│                                                    │
│  ┌────────────────┐        ┌────────────────┐     │
│  │ G: Hyperbola   │        │ m: Number      │     │
│  │ entropy: 0.5   │        │ entropy: 1.0   │     │
│  │ attributes:    │        │ is_query: True │     │
│  │   a² = 4       │        │ value = ?      │     │
│  │   b² = m²      │        └───────┬────────┘     │
│  └───────┬────────┘                │              │
│          │                         │              │
└──────────┼─────────────────────────┼──────────────┘
           │                         │
┌──────────┼─────── Relation Edges ──┼──────────────┐
│          ▼                         ▼              │
│  ┌────────────────────────────────────────────┐   │
│  │ e1: Expression(G) = (x²/4 - y²/m² = 1)    │   │
│  │     involves: [G, m]                       │   │
│  │     is_used: False                         │   │
│  └────────────────────────────────────────────┘   │
│                                                   │
│  ┌────────────────────────────────────────────┐   │
│  │ e2: Expression(Asymptote(G)) = (5x-2y=0)  │   │
│  │     involves: [G]                          │   │
│  │     is_used: False                         │   │
│  └────────────────────────────────────────────┘   │
│                                                   │
│  ┌────────────────────────────────────────────┐   │
│  │ e3: m > 0                                  │   │
│  │     involves: [m]                          │   │
│  │     type: inequality                       │   │
│  └────────────────────────────────────────────┘   │
└───────────────────────────────────────────────────┘
```

---

## 三、信息熵计算

### 3.1 图的总熵定义

图的总信息熵定义为所有节点局部熵的加权和：

$$H(\mathcal{G}) = \sum_{v \in \mathcal{V}} H_{local}(v) \cdot w(v, q)$$

其中：
- $H_{local}(v)$ = 节点 $v$ 的局部熵
- $w(v, q)$ = 节点 $v$ 与查询目标 $q$ 的相关性权重

### 3.2 局部熵计算

节点的局部熵基于其**确定程度**和**约束覆盖度**：

$$H_{local}(v) = \text{status\_entropy}(v) \cdot \text{constraint\_factor}(v)$$

**状态熵**：

```python
def status_entropy(node: ObjectNode) -> float:
    """基于节点状态的熵"""
    status_map = {
        "determined": 0.0,
        "derivable": 0.25,
        "constrained": 0.5,
        "typed": 0.75,
        "unknown": 1.0
    }
    return status_map.get(node.status, 1.0)
```

**约束因子**：
```python
def constraint_factor(node: ObjectNode, graph: SCGraph) -> float:
    """基于约束数量的调整因子"""
    # 涉及该节点的约束数量
    num_constraints = len(graph.get_edges_involving(node.id))
    # 约束越多，熵越低
    return 1.0 / (1.0 + 0.1 * num_constraints)
```

### 3.3 相关性权重

相关性权重基于节点与查询目标的**图距离**：

$$w(v, q) = \frac{1}{\text{distance}(v, q) + 1}$$

```python
def relevance_weight(node_id: str, query_id: str, graph: SCGraph) -> float:
    """计算节点与查询目标的相关性权重"""
    if node_id == query_id:
        return 1.0
    
    # 计算最短路径距离
    distance = graph.shortest_path_length(node_id, query_id)
    
    if distance == float('inf'):
        return 0.1  # 不连通时给一个小权重
    
    return 1.0 / (distance + 1)
```

### 3.4 完整的熵计算

```python
def compute_graph_entropy(graph: SCGraph, query: str) -> float:
    """
    计算图的总信息熵
    
    Args:
        graph: 符号-约束图
        query: 查询目标（节点ID）
    
    Returns:
        entropy: 总信息熵值
    """
    total_entropy = 0.0
    
    for node in graph.nodes:
        # 局部熵
        local_h = status_entropy(node) * constraint_factor(node, graph)
        
        # 相关性权重
        weight = relevance_weight(node.id, query, graph)
        
        # 加权累加
        total_entropy += local_h * weight
    
    return total_entropy
```

### 3.5 熵的性质

1. **非负性**：$H(\mathcal{G}) \geq 0$
2. **单调递减性**（理想情况）：随着推理进行，熵应该单调递减
3. **终止条件**：当 $H(\mathcal{G}) = 0$ 时，问题完全确定
4. **可解性判断**：如果熵无法继续降低，可能条件不足

---

## 四、推理步骤的信息增益

### 4.1 信息增益定义

信息增益（Information Gain）定义为应用一个推理步骤后熵的减少量：

$$IG(\text{step}) = H(\mathcal{G}_{before}) - H(\mathcal{G}_{after})$$

### 4.2 推理步骤的分类

| 步骤类型 | 操作 | 预期IG | 示例 |
|---------|------|--------|------|
| **定理应用** | 应用圆锥曲线性质 | 高 | 双曲线渐近线公式 |
| **代入求解** | 用已知值代入表达式 | 高 | $\frac{m}{2} = \frac{5}{2} \Rightarrow m=5$ |
| **约束传播** | 从约束推导新约束 | 中 | $a^2=4, b^2=m^2 \Rightarrow c^2=4+m^2$ |
| **表达式化简** | 代数变换 | 低 | $\frac{x^2}{4} \rightarrow x^2/4$ |
| **辅助引入** | 引入辅助变量 | 负/零 | 设 $t = \sin\theta$ |

### 4.3 信息增益的计算

```python
def compute_information_gain(
    graph_before: SCGraph,
    graph_after: SCGraph,
    query: str
) -> float:
    """
    计算推理步骤的信息增益
    
    Args:
        graph_before: 执行前的图状态
        graph_after: 执行后的图状态
        query: 查询目标
    
    Returns:
        ig: 信息增益值
    """
    h_before = compute_graph_entropy(graph_before, query)
    h_after = compute_graph_entropy(graph_after, query)
    
    return h_before - h_after
```

### 4.4 多维度信息增益（细粒度版本）

$$IG = \alpha \cdot \Delta_{symbols} + \beta \cdot \Delta_{constraints} + \gamma \cdot \Delta_{relevance}$$

```python
def compute_detailed_information_gain(
    graph_before: SCGraph,
    graph_after: SCGraph,
    query: str,
    alpha: float = 1.0,
    beta: float = 0.5,
    gamma: float = 2.0
) -> float:
    """
    多维度信息增益计算
    """
    # 分量1: 符号确定度变化
    delta_symbols = 0
    for node_id in graph_after.node_ids:
        status_before = graph_before.get_node(node_id).status
        status_after = graph_after.get_node(node_id).status
        delta_symbols += status_level(status_before) - status_level(status_after)
    
    # 分量2: 有效约束变化
    new_constraints = graph_after.edges - graph_before.edges
    useful_new = sum(1 for c in new_constraints if involves_query(c, query))
    delta_constraints = useful_new
    
    # 分量3: 与query的距离变化
    dist_before = graph_before.distance_to_determined(query)
    dist_after = graph_after.distance_to_determined(query)
    delta_relevance = dist_before - dist_after
    
    # 加权求和
    ig = alpha * delta_symbols + beta * delta_constraints + gamma * delta_relevance
    
    return max(0, ig)  # 保证非负
```

### 4.5 实例演示

**问题**：双曲线渐近线求参数m

```
初始状态 S₀:
├── 节点: {G(H=0.5), m(H=1.0, is_query)}
├── 边: {e1, e2, e3}
├── 总熵 H(S₀) = 0.5×0.8 + 1.0×1.0 = 1.4

Step 1: 应用"双曲线渐近线定理"
├── 推导: 渐近线斜率 = ±m/2
├── 新增边: e4 = "slope(Asymptote(G)) = m/2"
├── m的约束增加: constraint_factor降低
├── 总熵 H(S₁) = 0.5×0.7 + 0.75×0.9 = 1.025
├── IG₁ = 1.4 - 1.025 = 0.375

Step 2: 从已知渐近线提取斜率
├── 推导: 5x-2y=0 → 斜率 = 5/2
├── 新增边: e5 = "given_slope = 5/2"
├── 总熵 H(S₂) = 0.5×0.6 + 0.5×0.8 = 0.7
├── IG₂ = 1.025 - 0.7 = 0.325

Step 3: 联立求解
├── 推导: m/2 = 5/2 → m = 5
├── m的状态: unknown → determined
├── 总熵 H(S₃) = 0.5×0.6 + 0.0×1.0 = 0.3
├── IG₃ = 0.7 - 0.3 = 0.4

最终: H → 0（m已确定，G的熵也因此降低）
总信息增益: IG₁ + IG₂ + IG₃ ≈ H(S₀)
```

---

## 五、定理匹配机制

### 5.1 基于规则的条件匹配（推荐方案）

不采用严格的图模式匹配，而是使用**规则条件**描述定理的适用性：

```python
class TheoremRule:
    """基于规则的定理表示"""
    
    name: str                      # 定理名称
    applicable_types: List[str]    # 适用的对象类型
    required_operators: List[str]  # 需要已知的操作符
    preconditions: List[Callable]  # 前置条件函数
    derive: Callable               # 推导函数
    info_gain_estimate: float      # 预估信息增益
```

### 5.2 定理示例

```python
# 双曲线渐近线公式
HYPERBOLA_ASYMPTOTE = TheoremRule(
    name="双曲线渐近线公式",
    applicable_types=["Hyperbola"],
    required_operators=["Expression"],
    preconditions=[
        lambda g, s: g.get_type(s) == "Hyperbola",
        lambda g, s: g.has_edge("Expression", s),
        lambda g, s: not g.has_edge("Asymptote", s),
    ],
    derive=lambda g, s: {
        "new_knowledge": f"Asymptote({s}) = y = ±(b/a)x",
        "new_edges": [("Asymptote", s, "y = ±(b/a)x")]
    },
    info_gain_estimate=1.5
)

# 椭圆离心率公式
ELLIPSE_ECCENTRICITY = TheoremRule(
    name="椭圆离心率公式",
    applicable_types=["Ellipse"],
    required_operators=["Expression"],
    preconditions=[
        lambda g, s: g.get_type(s) == "Ellipse",
        lambda g, s: g.has_edge("Expression", s),
    ],
    derive=lambda g, s: {
        "formula": "e = c/a = sqrt(1 - b²/a²)",
    },
    info_gain_estimate=1.0
)
```

### 5.3 定理匹配流程

```python
def find_applicable_theorems(
    graph: SCGraph, 
    theorems: List[TheoremRule]
) -> List[Tuple[TheoremRule, str]]:
    """
    找到所有可应用的定理
    
    Returns:
        List of (theorem, target_node_id)
    """
    applicable = []
    
    for theorem in theorems:
        for node in graph.nodes:
            # 类型匹配
            if node.type not in theorem.applicable_types:
                continue
            
            # 检查必需操作符
            has_required = all(
                graph.has_edge(op, node.id) 
                for op in theorem.required_operators
            )
            if not has_required:
                continue
            
            # 检查前置条件
            conditions_met = all(
                cond(graph, node.id) 
                for cond in theorem.preconditions
            )
            if not conditions_met:
                continue
            
            applicable.append((theorem, node.id))
    
    return applicable
```

### 5.4 定理库组织

```python
THEOREM_LIBRARY = {
    "Hyperbola": [
        TheoremRule("渐近线公式", ...),
        TheoremRule("离心率公式", ...),
        TheoremRule("焦点距离公式", ...),
    ],
    "Ellipse": [
        TheoremRule("离心率公式", ...),
        TheoremRule("焦点弦公式", ...),
    ],
    "Parabola": [
        TheoremRule("焦点公式", ...),
        TheoremRule("准线公式", ...),
    ],
    "General": [
        TheoremRule("距离公式", ...),
        TheoremRule("中点公式", ...),
    ]
}
```

---

## 六、推理算法

### 6.1 信息熵引导的推理

```python
def entropy_guided_reasoning(
    initial_graph: SCGraph,
    query: str,
    theorems: List[TheoremRule],
    max_steps: int = 100
) -> Tuple[SCGraph, List[Dict]]:
    """
    信息熵引导的推理过程
    
    Args:
        initial_graph: 初始SCG
        query: 查询目标
        theorems: 定理库
        max_steps: 最大步数
    
    Returns:
        final_graph: 最终图状态
        trajectory: 推理轨迹
    """
    graph = initial_graph
    trajectory = []
    
    for step in range(max_steps):
        current_entropy = compute_graph_entropy(graph, query)
        
        # 终止条件：熵为0或query已确定
        if current_entropy == 0 or graph.get_node(query).status == "determined":
            break
        
        # 找到所有可应用的定理
        candidates = find_applicable_theorems(graph, theorems)
        
        if not candidates:
            break  # 无可用定理
        
        # 评估每个候选的信息增益
        evaluated = []
        for theorem, target in candidates:
            new_graph = apply_theorem(graph, theorem, target)
            ig = compute_information_gain(graph, new_graph, query)
            evaluated.append((theorem, target, new_graph, ig))
        
        # 选择信息增益最大的
        evaluated.sort(key=lambda x: x[3], reverse=True)
        best_theorem, best_target, new_graph, best_ig = evaluated[0]
        
        # 记录轨迹
        trajectory.append({
            "step": step + 1,
            "theorem": best_theorem.name,
            "target": best_target,
            "information_gain": best_ig,
            "entropy_before": current_entropy,
            "entropy_after": compute_graph_entropy(new_graph, query)
        })
        
        graph = new_graph
    
    return graph, trajectory
```

### 6.2 算法流程图

```
┌─────────────────────────────────────────────────────────────────┐
│                   信息熵引导推理流程                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  输入: fact_expressions, query_expressions                      │
│                    ↓                                            │
│  ┌─────────────────────────────────────────────┐               │
│  │         构建初始 SCG                         │               │
│  │  - 解析符号声明 → 节点                       │               │
│  │  - 解析约束条件 → 边                         │               │
│  │  - 初始化熵状态                              │               │
│  └─────────────────────────────────────────────┘               │
│                    ↓                                            │
│  ┌─────────────────────────────────────────────┐               │
│  │         计算当前熵 H(G)                      │               │
│  └─────────────────────────────────────────────┘               │
│                    ↓                                            │
│            H(G) == 0? ──Yes──> 输出答案                         │
│                │                                                │
│               No                                                │
│                ↓                                                │
│  ┌─────────────────────────────────────────────┐               │
│  │         查找可用定理                         │               │
│  │  - 类型匹配                                  │               │
│  │  - 前置条件验证                              │               │
│  └─────────────────────────────────────────────┘               │
│                    ↓                                            │
│           有可用定理? ──No──> 求解失败                          │
│                │                                                │
│               Yes                                               │
│                ↓                                                │
│  ┌─────────────────────────────────────────────┐               │
│  │         计算各定理的信息增益                  │               │
│  │  IG = H(G_before) - H(G_after)              │               │
│  └─────────────────────────────────────────────┘               │
│                    ↓                                            │
│  ┌─────────────────────────────────────────────┐               │
│  │         选择 IG 最大的定理并应用             │               │
│  │  - 更新图结构                                │               │
│  │  - 更新熵状态                                │               │
│  └─────────────────────────────────────────────┘               │
│                    ↓                                            │
│               返回循环                                          │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 七、与HGR的对比

| 维度 | HGR Hologram | EGR-SCG |
|------|-------------|---------|
| **领域** | 平面几何 | 圆锥曲线 |
| **节点** | 几何基元 | 数学对象(Concept) |
| **边** | 几何关系 | 操作符关系(Operator) |
| **属性** | 数学属性 + 视觉属性 | 值 + 熵状态 |
| **定理匹配** | 图模式匹配(VF3) | 规则条件匹配 |
| **模型选择** | DQN (隐式reward) | 信息增益 (显式熵) |
| **可解释性** | 定理序列 | 定理序列 + 熵变化轨迹 |

**EGR-SCG的创新点**：
1. **显式信息熵**：量化求解进度
2. **信息增益指导**：优化推理方向选择
3. **简化的定理匹配**：无需子图模式，降低设计成本
4. **可解性判断**：通过熵是否能降到0判断

---

## 八、待研究问题

1. **熵计算的精确性**：如何更准确地估计节点的局部熵？
2. **信息增益的准确预测**：是否可以用神经网络学习预测？
3. **定理库的完备性**：如何确保定理库覆盖所有情况？
4. **与强化学习的结合**：用IG作为reward训练策略网络

---

## 参考文献

1. HGR: Hologram Reasoning for Solving Algebra Problems with Geometry Diagrams
2. Conic10K: A Challenging Math Problem Understanding and Reasoning Dataset (EMNLP 2023)
3. GeoDRL: Deep Reinforcement Learning for Geometry Problem Solving
4. Inter-GPS: Interpretable Geometry Problem Solving

---

*文档版本: v1.0*
*最后更新: 2025年*




