# Module 1: 状态构建与更新指南

**版本**: v1.0  
**日期**: 2026-01-15  
**目的**: 定义题目状态的标准化表示和更新机制

---

## 📋 概述

本文档定义了数学问题状态的**双层表示机制**和**状态转换规则**。状态是推理系统的核心数据结构，记录了问题求解过程中的所有已知信息。

### 术语说明

- **AbstractState**：抽象状态（类型名）- 粗粒度的离散特征表示
- **SymbolicState**：符号状态（类型名）- 细粒度的符号信息表示
- **StateConstructor**：状态构造器（类名）- 负责构建和更新状态的工具类
- **construct**：构建（动词）- 从输入生成状态的过程

### 核心设计理念

1. **双层表示**：粗粒度抽象 + 细粒度符号，兼顾建模和推理
2. **信息累积**：状态只增不减，记录完整推理历史
3. **标准化接口**：统一的构建和更新方法
4. **可追溯性**：每一步变化都有明确记录

---

## 🏗️ 双层状态架构

### 架构图

```
┌────────────────────────────────────────────────┐
│         AbstractState (抽象状态)                │
│  - 有限离散特征空间                             │
│  - 用于模型选择和状态索引                        │
│  - 可哈希、可向量化                             │
│                                                │
│  特征维度：                                     │
│  • curve_type: 曲线类型 (4种)                  │
│  • query_type: 查询类型 (10种)                 │
│  • has_parameters: 已知参数集合                │
│  • has_equation: 是否有方程                    │
│  • has_focus_info: 是否有焦点                  │
│  • ... (共11个布尔特征)                        │
│  • completeness_score: 完整度 (0.0-1.0)       │
│  • reasoning_depth: 推理深度                   │
└────────────────────────────────────────────────┘
                    ↕ 抽象/具体化
┌────────────────────────────────────────────────┐
│         SymbolicState (符号状态)                │
│  - 存储所有具体信息                             │
│  - 用于精确推理和模型应用                        │
│  - 支持符号计算                                 │
│                                                │
│  数据字段：                                     │
│  • entities: 实体声明 {G: 'Hyperbola'}         │
│  • equations: 方程列表 [...]                   │
│  • parameters: 参数字典 {a: 2, b: 'm'}         │
│  • geometric_relations: 几何关系 [...]         │
│  • coordinates: 坐标信息 {F: (c, 0)}          │
│  • constraints: 约束条件 ['m>0']               │
└────────────────────────────────────────────────┘
```

### 为什么需要两层？

| 需求 | AbstractState | SymbolicState |
|------|--------------|---------------|
| 建立 P(model\|state) | ✅ 有限状态空间 | ❌ 无限状态 |
| 精确推理 | ❌ 信息不完整 | ✅ 完整信息 |
| 状态索引 | ✅ 可哈希 | ❌ 难哈希 |
| 模型应用 | ❌ 无法计算 | ✅ 支持符号推理 |

**结论**：两层互补，缺一不可。

---

## 📐 SymbolicState 详细定义

### 数据结构

```python
@dataclass
class SymbolicState:
    """
    符号状态：存储问题的所有具体信息
    """
    # ===== 字段1: 实体声明 =====
    entities: Dict[str, str] = field(default_factory=dict)
    """
    实体声明字典
    
    格式：{实体名: 实体类型}
    例如：{'G': 'Hyperbola', 'm': 'Number', 'A': 'Point', 'F': 'Point'}
    
    常见实体类型：
    - 曲线：Ellipse, Hyperbola, Parabola, Circle
    - 几何：Point, Line, LineSegment, Ray, Triangle
    - 数值：Number, Real, Angle
    - 其他：Vector, Origin, Axis
    """
    
    # ===== 字段2: 方程列表 =====
    equations: List[str] = field(default_factory=list)
    """
    方程/表达式列表
    
    格式：符号化的方程字符串
    例如：
    - 'Expression(G) = (x^2/4 - y^2/m^2 = 1)'
    - 'Expression(OneOf(Asymptote(G))) = (5*x - 2*y = 0)'
    - 'y^2 = 4*x'
    
    注意：
    - 保持原始形式，便于模式匹配
    - 不要随意简化或变换
    """
    
    # ===== 字段3: 参数字典 =====
    parameters: Dict[str, Any] = field(default_factory=dict)
    """
    参数值字典（核心字段！）
    
    格式：{参数名: 参数值}
    例如：
    - {'a': 2, 'b': 'm', 'c': 'sqrt(5)'}
    - {'a^2': 4, 'b^2': 'm^2'}
    - {'e': 'sqrt(2)'}
    
    值的类型：
    - 数值：2, 3.14
    - 符号：'m', 'a', 'b'
    - 表达式：'sqrt(5)', 'm/2', 'sqrt(a^2 + b^2)'
    
    关键原则：
    ✅ 能算出具体值就算（如 a=2）
    ✅ 算不出保持符号形式（如 b='m'）
    ✅ 同时保留 a^2 和 a（如 a^2=4, a=2）
    """
    
    # ===== 字段4: 几何关系 =====
    geometric_relations: List[str] = field(default_factory=list)
    """
    几何关系列表
    
    格式：描述性的关系字符串
    例如：
    - 'Distance(P, F1) + Distance(P, F2) = 2*a'
    - 'IsPerpendicular(AB, xAxis)'
    - 'Intersection(L1, L2) = P'
    - 'a^2 = 4'
    - '渐近线: y = ±(m/2)x'
    
    用途：
    - 记录模型应用产生的关系
    - 便于人工检查推理过程
    """
    
    # ===== 字段5: 坐标信息 =====
    coordinates: Dict[str, Tuple] = field(default_factory=dict)
    """
    坐标字典
    
    格式：{点名: (x坐标, y坐标)}
    例如：
    - {'F': ('c', 0)}
    - {'A': (1, '1/4')}
    - {'P': ('x', 'y')}
    
    注意：坐标可以是符号或数值
    """
    
    # ===== 字段6: 约束条件 =====
    constraints: List[str] = field(default_factory=list)
    """
    约束条件列表
    
    格式：不等式或逻辑条件
    例如：
    - 'm > 0'
    - 'a > b'
    - 'b > 0'
    - 'e < 1'  (椭圆)
    - 'e > 1'  (双曲线)
    """
    
    # ===== 字段7: 元信息（可选）=====
    applied_models: List[int] = field(default_factory=list)
    """
    已应用的模型ID列表（用于调试和可视化）
    """
    
    def copy(self) -> 'SymbolicState':
        """
        深拷贝状态
        
        注意：必须深拷贝，否则会相互影响
        """
        return SymbolicState(
            entities=self.entities.copy(),
            equations=self.equations.copy(),
            parameters=self.parameters.copy(),
            geometric_relations=self.geometric_relations.copy(),
            coordinates={k: v for k, v in self.coordinates.items()},
            constraints=self.constraints.copy(),
            applied_models=self.applied_models.copy()
        )
```

### 字段使用规范

#### entities 字段

**规则**：
1. 从 `fact_expressions` 的类型声明中提取
2. 格式：`实体名: 类型`
3. 只添加不删除

**示例**：
```python
# fact_expressions: "G: Hyperbola;m: Number;A: Point;B: Point"
state.entities = {
    'G': 'Hyperbola',
    'm': 'Number',
    'A': 'Point',
    'B': 'Point'
}
```

#### equations 字段

**规则**：
1. 存储所有形如 `Expression(...)` 的方程
2. 保持原始形式，便于模式匹配
3. 新方程追加到列表末尾

**示例**：
```python
state.equations = [
    'Expression(G) = (x^2/4 - y^2/m^2 = 1)',
    'Expression(OneOf(Asymptote(G))) = (5*x - 2*y = 0)',
    'Expression(Asymptote(G)) = (y = pm*(m/2)*x)',  # 模型应用后新增
]
```

#### parameters 字段（最重要！）

**规则**：
1. 存储所有已知或推导出的参数值
2. 优先存储具体数值
3. 无法计算时保持符号形式
4. 同时保留原始和简化形式（如 a^2 和 a）

**示例**：
```python
# 初始状态（从方程提取）
state.parameters = {
    'a^2': '4',      # 从 x^2/4 提取
    'b^2': 'm^2',    # 从 y^2/m^2 提取
    'a': '2',        # sqrt(4) = 2
    'b': 'm'         # sqrt(m^2) = m
}

# 应用参数关系后
state.parameters = {
    'a^2': '4',
    'b^2': 'm^2',
    'a': '2',
    'b': 'm',
    'c': 'sqrt(4 + m^2)',  # 新增：c^2 = a^2 + b^2
}

# 应用离心率公式后
state.parameters = {
    'a^2': '4',
    'b^2': 'm^2',
    'a': '2',
    'b': 'm',
    'c': 'sqrt(4 + m^2)',
    'e': 'sqrt(4 + m^2)/2'  # 新增：e = c/a
}
```

**关键原则**：
- ✅ 可以有多个版本的同一参数（如 a^2 和 a）
- ✅ 新参数只添加，不覆盖旧参数
- ✅ 保持符号形式便于后续推理
- ❌ 不要删除已有参数

---

## 🎨 AbstractState 详细定义

### 数据结构

```python
@dataclass
class AbstractState:
    """
    抽象状态：有限离散的特征表示
    """
    # ===== 维度1: 曲线类型 (4种) =====
    curve_type: CurveType
    """
    曲线类型枚举
    
    取值：
    - CurveType.ELLIPSE: 椭圆
    - CurveType.HYPERBOLA: 双曲线
    - CurveType.PARABOLA: 抛物线
    - CurveType.CIRCLE: 圆
    - CurveType.UNKNOWN: 未知
    
    提取规则：从 entities 中查找曲线类型实体
    """
    
    # ===== 维度2: 查询类型 (10种) =====
    query_type: QueryType
    """
    查询目标类型枚举
    
    取值：
    - ECCENTRICITY: 求离心率
    - EQUATION: 求方程
    - COORDINATE: 求坐标
    - DISTANCE: 求距离
    - LENGTH: 求长度
    - RANGE: 求范围
    - VALUE: 求参数值
    - ANGLE: 求角度
    - AREA: 求面积
    - EXPRESSION: 求表达式
    
    提取规则：从 query_expressions 关键词匹配
    """
    
    # ===== 维度3: 信息特征 (11个布尔特征) =====
    has_equation: bool = False
    """是否有曲线方程"""
    
    has_parameters: Set[str] = field(default_factory=set)
    """
    已知参数集合
    
    例如：{'a', 'b', 'c', 'e', 'm'}
    注意：只记录参数名，不记录值
    """
    
    has_focus_info: bool = False
    """是否有焦点相关信息"""
    
    has_vertex_info: bool = False
    """是否有顶点信息"""
    
    has_point_on_curve: bool = False
    """是否有曲线上的点"""
    
    has_asymptote_info: bool = False
    """是否有渐近线信息"""
    
    has_directrix_info: bool = False
    """是否有准线信息"""
    
    has_tangent_info: bool = False
    """是否有切线信息"""
    
    has_distance_constraint: bool = False
    """是否有距离约束"""
    
    has_angle_constraint: bool = False
    """是否有角度约束"""
    
    has_perpendicular: bool = False
    """是否有垂直关系"""
    
    # ===== 维度4: 完整度得分 (连续值) =====
    completeness_score: float = 0.0
    """
    信息完整度得分 (0.0 - 1.0)
    
    计算规则：
    - 0.0: 信息几乎为空
    - 0.5: 信息约半完整
    - 1.0: 信息完全，可求解
    
    估算方法：见 _estimate_completeness()
    """
    
    # ===== 维度5: 推理深度 (整数) =====
    reasoning_depth: int = 0
    """
    推理步数
    
    - 0: 初始状态
    - 1: 应用1个模型后
    - 2: 应用2个模型后
    - ...
    """
    
    def to_vector(self) -> List[float]:
        """
        转换为特征向量（用于神经网络）
        
        返回：长度约30的浮点数列表
        
        向量组成：
        - [0:5]   曲线类型 one-hot (5维)
        - [5:15]  查询类型 one-hot (10维)
        - [15:26] 信息特征 (11维)
        - [26:28] 完整度和深度 (2维)
        """
        vector = []
        
        # 1. 曲线类型 one-hot
        curve_types = [CurveType.ELLIPSE, CurveType.HYPERBOLA, 
                       CurveType.PARABOLA, CurveType.CIRCLE, 
                       CurveType.UNKNOWN]
        curve_one_hot = [1.0 if self.curve_type == ct else 0.0 
                        for ct in curve_types]
        vector.extend(curve_one_hot)
        
        # 2. 查询类型 one-hot
        query_types = list(QueryType)
        query_one_hot = [1.0 if self.query_type == qt else 0.0 
                        for qt in query_types]
        vector.extend(query_one_hot)
        
        # 3. 信息特征
        vector.extend([
            float(self.has_equation),
            float(self.has_focus_info),
            float(self.has_vertex_info),
            float(self.has_point_on_curve),
            float(self.has_asymptote_info),
            float(self.has_directrix_info),
            float(self.has_tangent_info),
            float(self.has_distance_constraint),
            float(self.has_angle_constraint),
            float(self.has_perpendicular),
            float(len(self.has_parameters)) / 10.0  # 归一化
        ])
        
        # 4. 完整度和深度
        vector.extend([
            self.completeness_score,
            min(self.reasoning_depth / 10.0, 1.0)  # 归一化
        ])
        
        return vector
    
    def to_hash(self) -> str:
        """
        计算状态哈希（用于索引）
        
        注意：不包含 reasoning_depth，使相同信息状态有相同哈希
        """
        import hashlib
        import json
        
        state_dict = {
            'curve_type': self.curve_type.value,
            'query_type': self.query_type.value,
            'has_equation': self.has_equation,
            'has_parameters': sorted(list(self.has_parameters)),
            'has_focus_info': self.has_focus_info,
            'has_vertex_info': self.has_vertex_info,
            'has_point_on_curve': self.has_point_on_curve,
            'has_asymptote_info': self.has_asymptote_info,
            'has_directrix_info': self.has_directrix_info,
            'has_tangent_info': self.has_tangent_info,
            'has_distance_constraint': self.has_distance_constraint,
            'has_angle_constraint': self.has_angle_constraint,
            'has_perpendicular': self.has_perpendicular,
            'completeness_level': round(self.completeness_score * 4) / 4
        }
        
        state_str = json.dumps(state_dict, sort_keys=True)
        return hashlib.md5(state_str.encode()).hexdigest()
```

### 完整度估算方法

```python
def _estimate_completeness(
    symbolic_state: SymbolicState, 
    query_expressions: str
) -> float:
    """
    估计信息完整度
    
    核心思想：根据启发式规则评分
    
    评分规则：
    1. 有方程 → +0.3
    2. 每个已知参数 → +0.1 (最多+0.4)
    3. 有查询相关的关键信息 → +0.2
    4. 有几何关系 → +0.1
    
    总分：min(各项之和, 1.0)
    """
    score = 0.0
    
    # 规则1: 有方程
    if len(symbolic_state.equations) > 0:
        score += 0.3
    
    # 规则2: 已知参数
    param_count = len(symbolic_state.parameters)
    score += min(param_count * 0.1, 0.4)
    
    # 规则3: 查询相关信息
    query_type = classify_query(query_expressions)
    if has_query_related_info(symbolic_state, query_type):
        score += 0.2
    
    # 规则4: 几何关系
    if len(symbolic_state.geometric_relations) > 0:
        score += 0.1
    
    return min(score, 1.0)

def has_query_related_info(state: SymbolicState, query_type: QueryType) -> bool:
    """
    判断是否有查询相关的关键信息
    """
    if query_type == QueryType.ECCENTRICITY:
        # 求离心率：需要 c 和 a
        params = state.parameters.keys()
        return ('c' in params and 'a' in params) or \
               ('a' in params and 'b' in params)
    
    elif query_type == QueryType.EQUATION:
        # 求方程：需要足够的参数
        return len(state.parameters) >= 2
    
    elif query_type == QueryType.COORDINATE:
        # 求坐标：需要相关点的信息
        return len(state.coordinates) > 0 or \
               any('Coordinate' in rel for rel in state.geometric_relations)
    
    # ... 其他查询类型
    
    return False
```

---

## 🔨 状态构建流程

### 从 fact_expressions 初始化

**输入**：`fact_expressions` 字符串

**输出**：`(AbstractState, SymbolicState)` 元组

**流程**：

```python
def construct_from_facts(
    fact_expressions: str,
    query_expressions: str,
    reasoning_depth: int = 0
) -> Tuple[AbstractState, SymbolicState]:
    """
    从 fact_expressions 构建初始状态
    """
    # ===== 步骤1: 解析 fact_expressions =====
    symbolic_state = parse_fact_expressions(fact_expressions)
    
    # ===== 步骤2: 提取抽象特征 =====
    abstract_state = construct_abstract_features(
        symbolic_state,
        query_expressions,
        reasoning_depth
    )
    
    return abstract_state, symbolic_state
```

### 步骤1：解析 fact_expressions

```python
def parse_fact_expressions(fact_expressions: str) -> SymbolicState:
    """
    解析 fact_expressions 字符串
    
    输入格式：
    "G: Hyperbola;m: Number;m>0;Expression(G) = (x^2/4 - y^2/m^2 = 1)"
    
    解析规则：
    1. 按分号分割成单个 fact
    2. 识别 fact 类型（实体声明、方程、关系、约束）
    3. 分配到对应字段
    """
    state = SymbolicState()
    
    # 分割 facts
    facts = fact_expressions.split(';')
    
    for fact in facts:
        fact = fact.strip()
        if not fact:
            continue
        
        # 类型1: 实体声明 "G: Hyperbola"
        if re.match(r'^(\w+):\s*(\w+)$', fact):
            match = re.match(r'^(\w+):\s*(\w+)$', fact)
            name, type_ = match.groups()
            state.entities[name] = type_
        
        # 类型2: 方程 "Expression(...) = ..."
        elif 'Expression' in fact and '=' in fact:
            state.equations.append(fact)
        
        # 类型3: 坐标 "Coordinate(A) = (1, 2)"
        elif 'Coordinate' in fact:
            match = re.match(r'Coordinate\((\w+)\)\s*=\s*\(([^)]+)\)', fact)
            if match:
                point_name = match.group(1)
                coords_str = match.group(2)
                coords = tuple(c.strip() for c in coords_str.split(','))
                state.coordinates[point_name] = coords
        
        # 类型4: 几何关系 "Distance(...)", "IsPerpendicular(...)"
        elif any(kw in fact for kw in ['Distance', 'IsPerpendicular', 
                                        'IsTangent', 'Intersection', 
                                        'PointOnCurve']):
            state.geometric_relations.append(fact)
        
        # 类型5: 约束条件 "m > 0"
        elif any(op in fact for op in ['>', '<', '>=', '<=']):
            state.constraints.append(fact)
    
    return state
```

### 步骤2：构建抽象特征

```python
def construct_abstract_features(
    symbolic_state: SymbolicState,
    query_expressions: str,
    reasoning_depth: int
) -> AbstractState:
    """
    从符号状态构建抽象特征
    """
    abstract_state = AbstractState()
    
    # 特征1: 曲线类型
    abstract_state.curve_type = extract_curve_type(symbolic_state)
    
    # 特征2: 查询类型
    abstract_state.query_type = classify_query(query_expressions)
    
    # 特征3-13: 信息特征
    abstract_state.has_equation = len(symbolic_state.equations) > 0
    abstract_state.has_parameters = set(symbolic_state.parameters.keys())
    abstract_state.has_focus_info = check_has_focus(symbolic_state)
    abstract_state.has_vertex_info = check_has_vertex(symbolic_state)
    abstract_state.has_point_on_curve = check_has_point_on_curve(symbolic_state)
    abstract_state.has_asymptote_info = check_has_asymptote(symbolic_state)
    abstract_state.has_directrix_info = check_has_directrix(symbolic_state)
    abstract_state.has_tangent_info = check_has_tangent(symbolic_state)
    abstract_state.has_distance_constraint = check_has_distance(symbolic_state)
    abstract_state.has_angle_constraint = check_has_angle(symbolic_state)
    abstract_state.has_perpendicular = check_has_perpendicular(symbolic_state)
    
    # 特征14: 完整度
    abstract_state.completeness_score = _estimate_completeness(
        symbolic_state, 
        query_expressions
    )
    
    # 特征15: 深度
    abstract_state.reasoning_depth = reasoning_depth
    
    return abstract_state

def extract_curve_type(symbolic_state: SymbolicState) -> CurveType:
    """提取曲线类型"""
    for type_ in symbolic_state.entities.values():
        if type_ in ['Ellipse', 'ELLIPSE', 'ellipse']:
            return CurveType.ELLIPSE
        elif type_ in ['Hyperbola', 'HYPERBOLA', 'hyperbola']:
            return CurveType.HYPERBOLA
        elif type_ in ['Parabola', 'PARABOLA', 'parabola']:
            return CurveType.PARABOLA
        elif type_ in ['Circle', 'CIRCLE', 'circle']:
            return CurveType.CIRCLE
    return CurveType.UNKNOWN

def classify_query(query_expressions: str) -> QueryType:
    """分类查询类型"""
    query_lower = query_expressions.lower()
    
    if 'eccentricity' in query_lower:
        return QueryType.ECCENTRICITY
    elif 'equation' in query_lower or 'expression' in query_lower:
        return QueryType.EQUATION
    elif 'coordinate' in query_lower:
        return QueryType.COORDINATE
    elif 'distance' in query_lower:
        return QueryType.DISTANCE
    elif 'length' in query_lower:
        return QueryType.LENGTH
    elif 'range' in query_lower:
        return QueryType.RANGE
    elif 'angle' in query_lower:
        return QueryType.ANGLE
    elif 'area' in query_lower:
        return QueryType.AREA
    else:
        return QueryType.VALUE

def check_has_focus(symbolic_state: SymbolicState) -> bool:
    """检查是否有焦点信息"""
    # 方法1: 从方程中查找
    for eq in symbolic_state.equations:
        if 'Focus' in eq:
            return True
    
    # 方法2: 从几何关系中查找
    for rel in symbolic_state.geometric_relations:
        if 'Focus' in rel:
            return True
    
    return False

# 其他 check_has_* 函数类似...
```

---

## 🔄 状态更新机制

### 应用模型后更新

**关键原则**：
1. **SymbolicState 更新**：模型直接修改（见 Module 0）
2. **AbstractState 重新构建**：从更新后的 SymbolicState 重新提取特征

**流程**：

```python
def update_state_after_model(
    current_symbolic: SymbolicState,
    current_abstract: AbstractState,
    model: TheoremModel
) -> Tuple[AbstractState, SymbolicState]:
    """
    应用模型后更新状态
    """
    # ===== 步骤1: 应用模型，更新 SymbolicState =====
    # 注意：model.apply() 会直接修改 current_symbolic
    model.apply(current_symbolic)
    
    # ===== 步骤2: 从新的 SymbolicState 重新构建抽象特征 =====
    new_abstract = construct_abstract_features(
        current_symbolic,
        query_expressions,  # 查询不变
        reasoning_depth=current_abstract.reasoning_depth + 1  # 深度+1
    )
    
    return new_abstract, current_symbolic
```

### 状态序列构建

```python
def build_state_sequence(
    fact_expressions: str,
    query_expressions: str,
    model_ids: List[int],
    theorem_library: TheoremLibrary
) -> List[Tuple[AbstractState, SymbolicState]]:
    """
    构建完整的状态序列
    
    返回：[(S0, s0), (S1, s1), (S2, s2), ...]
    """
    # 初始化
    abstract_s0, symbolic_s0 = construct_from_facts(
        fact_expressions,
        query_expressions,
        reasoning_depth=0
    )
    
    states = [(abstract_s0, symbolic_s0)]
    current_symbolic = symbolic_s0
    
    # 逐步应用模型
    for i, model_id in enumerate(model_ids):
        model = theorem_library.get_model(model_id)
        
        # 应用模型（会修改 current_symbolic）
        model.apply(current_symbolic)
        
        # 重新构建抽象特征
        new_abstract = construct_abstract_features(
            current_symbolic,
            query_expressions,
            reasoning_depth=i + 1
        )
        
        # 注意：current_symbolic 是同一个对象，一直在累积信息
        states.append((new_abstract, current_symbolic))
    
    return states
```

---

## ✅ 实现规范

### 状态不变性原则

**SymbolicState**：
- ✅ 只增不减：只能添加信息，不能删除
- ✅ 幂等性：重复应用同一模型不出错
- ✅ 可追溯：保留 `applied_models` 记录

**AbstractState**：
- ✅ 无状态：每次从 SymbolicState 重新计算
- ✅ 单调性：`completeness_score` 应单调递增
- ✅ 一致性：相同 SymbolicState → 相同 AbstractState

### 测试检查清单

每个状态构建/更新函数必须通过：

```python
def test_state_construction():
    """测试状态构建"""
    
    # 测试1: 解析正确性
    fact_expr = "G: Hyperbola;m: Number;m>0;Expression(G) = (x^2/4 - y^2/m^2 = 1)"
    symbolic = parse_fact_expressions(fact_expr)
    
    assert 'G' in symbolic.entities
    assert symbolic.entities['G'] == 'Hyperbola'
    assert len(symbolic.equations) == 1
    assert 'm>0' in symbolic.constraints
    
    # 测试2: 构建抽象特征的正确性
    abstract = construct_abstract_features(symbolic, "m", 0)
    
    assert abstract.curve_type == CurveType.HYPERBOLA
    assert abstract.query_type == QueryType.VALUE
    assert abstract.has_equation == True
    assert 0.0 <= abstract.completeness_score <= 1.0
    
    # 测试3: 状态更新正确性
    model = theorem_library.get_model(5)
    model.apply(symbolic)
    
    assert 'a' in symbolic.parameters
    assert 'b' in symbolic.parameters
    
    new_abstract = construct_abstract_features(symbolic, "m", 1)
    assert 'a' in new_abstract.has_parameters
    assert new_abstract.completeness_score > abstract.completeness_score
```

---

## 📊 状态空间分析

### 理论状态数

```python
# AbstractState 的状态数：
状态数 = 曲线类型 × 查询类型 × 信息组合 × 完整度等级
      = 4 × 10 × 2^11 × 5
      ≈ 409,600 种
```

### 实际状态数（基于数据）

| 数据集 | 样本数 | 实际状态数 | 占比 |
|--------|-------|-----------|------|
| Conic10K | 10,000 | ~5,000-8,000 | 1.2%-2.0% |
| 前100样本 | 100 | ~150-200 | 0.05% |

**结论**：状态空间非常稀疏！

### 状态去重

**目的**：不同题目可能经过相同的中间状态

**方法**：使用 `AbstractState.to_hash()` 去重

```python
# 统计状态分布
state_counts = {}
for sample in dataset:
    for state in sample['state_sequence']:
        state_hash = state['abstract_state']['state_hash']
        state_counts[state_hash] = state_counts.get(state_hash, 0) + 1

# 结果示例：
# state_counts = {
#     'a3f2e1d4...': 15,  # 这个状态出现了15次
#     'b4e3f2d5...': 8,
#     ...
# }
```

---

## 🔗 与 Module 0 的接口

### 接口约定

```python
# Module 1 提供：
class StateConstructor:
    def construct_from_facts(
        self, 
        fact_expressions: str, 
        query_expressions: str,
        reasoning_depth: int = 0
    ) -> Tuple[AbstractState, SymbolicState]
    
    def construct_from_symbolic_state(
        self,
        symbolic_state: SymbolicState,
        query_expressions: str,
        reasoning_depth: int
    ) -> AbstractState

# Module 0 使用：
from src.state_constructor import StateConstructor, SymbolicState

constructor = StateConstructor()
abstract_state, symbolic_state = constructor.construct_from_facts(
    sample['fact_expressions'],
    sample['query_expressions']
)

# 应用模型后重新构建抽象特征
model.apply(symbolic_state)  # 修改 symbolic_state
new_abstract = constructor.construct_from_symbolic_state(
    symbolic_state,
    sample['query_expressions'],
    reasoning_depth=1
)
```

---

## 📚 参考资料

### 数据格式

- `data/train_with_models_1_100.json`：输入数据格式
- `handbook/Conic10K/object.json`：实体类型定义
- `handbook/Conic10K/operators.json`：操作符定义

### 相关文档

- `module0_model_library.md`：模型库规范
- `doc/创新点+论文思路.md`：整体设计思路

---

**最后更新**: 2026-01-15  
**维护者**: EGR Team  
**版本历史**: v1.0 初始版本
