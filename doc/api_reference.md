# EGR API Reference

**版本**: v1.0  
**最后更新**: 2026-01-18  
**状态**: 40/80 模型已实现 (50%)

---

## 快速开始

### 安装
```bash
pip install torch numpy scipy sympy
```

### 5分钟示例
```python
from src.state import StateConstructor
from src.theorems import TheoremLibrary

# 1. 创建定理库和构造器
library = TheoremLibrary()
constructor = StateConstructor(theorem_library=library)

# 2. 构建状态
abstract_state, symbolic_state = constructor.construct_from_facts(
    fact_expressions="G: Hyperbola;Expression(G) = (x^2/3 - y^2 = 1)",
    query_expressions="Length(ImageinaryAxis(G))",
    reasoning_depth=0
)

# 3. 应用模型
model = library.get_model(12)  # Hyperbola_Parameter_Relation
if model.can_apply(symbolic_state):
    model.apply(symbolic_state)
    print(f"参数: {symbolic_state.parameters}")
```

---

## 核心数据结构

### SymbolicState
符号状态 - 存储问题的所有具体信息
```python
from src.state import SymbolicState

state = SymbolicState(
    entities={'G': 'Hyperbola', 'A': 'Point'},
    equations=['Expression(G) = (x^2/4 - y^2/9 = 1)'],
    parameters={'a': '2', 'b': '3'},
    geometric_relations=['LeftFocus(G) = F1'],
    coordinates={},
    applied_models=[5, 12]
)
```

### AbstractState
抽象状态 - 用于神经网络的特征表示
```python
from src.state import AbstractState, CurveType, QueryType

state = AbstractState(
    curve_type=CurveType.HYPERBOLA,
    query_type=QueryType.LENGTH,
    has_equation=True,
    has_parameters={'a', 'b'},
    completeness_score=0.75,
    reasoning_depth=1
)
```

---

## 状态管理模块

### StateConstructor
状态构造器 - 从题目构建状态

#### 初始化
```python
from src.state import StateConstructor
from src.theorems import TheoremLibrary

constructor = StateConstructor(theorem_library=None)  # 可选：传入定理库启用自动参数提取
```

#### construct_from_facts()
从题目构建初始状态
```python
abstract_state, symbolic_state = constructor.construct_from_facts(
    fact_expressions="G: Ellipse;Expression(G) = (x^2/4 + y^2/3 = 1)",
    query_expressions="Eccentricity(G)",
    reasoning_depth=0
)
```
**参数**:
- `fact_expressions` (str): 题目事实表达式
- `query_expressions` (str): 查询表达式
- `reasoning_depth` (int): 推理深度，默认0

**返回**: `Tuple[AbstractState, SymbolicState]`

#### construct_from_symbolic_state()
从符号状态重新构建抽象状态（用于模型应用后更新）
```python
abstract_state = constructor.construct_from_symbolic_state(
    symbolic_state=symbolic_state,
    query_expressions="Eccentricity(G)",
    reasoning_depth=1
)
```
**参数**:
- `symbolic_state` (SymbolicState): 符号状态
- `query_expressions` (str): 查询表达式
- `reasoning_depth` (int): 推理深度

**返回**: `AbstractState`

---

### EquationNormalizer
方程标准化器 - 将非标准形式转换为标准形式

#### 初始化
```python
from src.state import EquationNormalizer

normalizer = EquationNormalizer()
```

#### normalize_fact_expressions()
标准化完整的fact_expressions
```python
normalized = normalizer.normalize_fact_expressions(
    "G: Parabola;Expression(G) = (y = x^2/4)"
)
# 输出: "G: Parabola;Expression(G) = (x^2 = 4*y)"
```

#### normalize_equation()
标准化单个方程
```python
normalized = normalizer.normalize_equation("y = x^2/4")
# 输出: "x^2 = 4*y"
```

**支持的转换**:
- `y = x²/4` → `x² = 4*y`
- `x²/3 - y² = 1` → `x²/3 - y²/1 = 1`
- `4x² + 9y² = 36` → `x²/9 + y²/4 = 1`

---

## 定理库模块

### TheoremLibrary
定理库管理器 - 管理80个定理模型

#### 初始化
```python
from src.theorems import TheoremLibrary

library = TheoremLibrary()  # 自动加载所有已实现的模型
```

#### get_model()
根据ID获取模型
```python
model = library.get_model(13)  # 获取离心率公式模型
print(f"模型名称: {model.name}")  # Eccentricity_Formula
```
**参数**: `model_id` (int) - 模型ID (0-79)  
**返回**: `TheoremModel` 或 `None`

#### get_all_models()
获取所有已注册的模型
```python
models = library.get_all_models()
print(f"已实现: {len(models)}/80 模型")
```
**返回**: `Dict[int, TheoremModel]`

#### apply_model_sequence()
批量应用模型序列
```python
success_count = library.apply_model_sequence(
    symbolic_state=symbolic_state,
    model_ids=[5, 12, 13]
)
print(f"成功应用: {success_count}/3 模型")
```
**参数**:
- `symbolic_state` (SymbolicState): 符号状态
- `model_ids` (List[int]): 模型ID列表

**返回**: `int` - 成功应用的模型数量

---

### TheoremModel
定理模型基类 - 所有模型的父类

#### can_apply()
检查模型是否可应用
```python
model = library.get_model(12)
if model.can_apply(symbolic_state):
    print("模型可应用")
```
**参数**: `state` (SymbolicState) - 符号状态  
**返回**: `bool`

#### apply()
应用模型（直接修改状态）
```python
model.apply(symbolic_state)  # 原地修改symbolic_state
```
**参数**: `state` (SymbolicState) - 符号状态  
**返回**: `None` - 直接修改传入的状态

---

## 已实现模型索引

**当前状态**: 40/80 模型 (50%)  
**成功率**: 72.0%

### 按类别分类

| 类别 | 已实现 | 总数 | 模型ID |
|------|--------|------|--------|
| 曲线定义 | 3 | 3 | 0, 1, 2 |
| 标准方程 | 8 | 8 | 3, 4, 5, 6, 7, 8, 9, 10 |
| 参数关系 | 3 | 5 | 11, 12, 13, 14 |
| 焦半径通径 | 2 | 5 | 16, 17, 19 |
| 渐近线 | 3 | 4 | 21, 22, 24 |
| 准线 | 1 | 5 | 29 |
| 焦点三角形 | 1 | 3 | 32 |
| 韦达定理 | 3 | 3 | 41, 42, 43 |
| 点差法 | 1 | 3 | 46 |
| 三角形定理 | 2 | 3 | 47, 57 |
| 距离坐标 | 2 | 4 | 53, 54 |
| 三角形面积 | 1 | 3 | 56 |
| 向量运算 | 2 | 4 | 61, 62 |
| 不等式 | 1 | 2 | 63 |
| 判别式 | 1 | 3 | 65 |
| 三角形特殊 | 1 | 4 | 70 |
| 圆相关 | 1 | 2 | 75 |
| 高级技巧 | 2 | 3 | 78, 79 |

### 按曲线类型分类

**椭圆** (7个): 0, 3, 4, 11, 13, 14, 16, 32  
**双曲线** (9个): 1, 5, 6, 12, 19, 21, 22, 24, 46  
**抛物线** (7个): 2, 7, 8, 9, 10, 17, 29  
**通用几何** (10个): 47, 53, 54, 56, 57, 61, 62, 63, 70, 75  
**代数工具** (5个): 41, 42, 43, 65, 78, 79

**详细模型文档**: 参见 [model/conic_model_reference.md](../model/conic_model_reference.md)

---

## 完整使用流程

### 示例：求双曲线虚轴长
```python
from src.state import StateConstructor
from src.theorems import TheoremLibrary

# 1. 初始化
library = TheoremLibrary()
constructor = StateConstructor(theorem_library=library)

# 2. 构建初始状态
abstract, symbolic = constructor.construct_from_facts(
    fact_expressions="G: Hyperbola;Expression(G) = (x^2/3 - y^2 = 1)",
    query_expressions="Length(ImageinaryAxis(G))",
    reasoning_depth=0
)

print(f"初始完整度: {abstract.completeness_score}")
print(f"初始参数: {symbolic.parameters}")

# 3. 应用模型序列
model_ids = [5, 12]  # 双曲线标准方程 → 参数关系
for model_id in model_ids:
    model = library.get_model(model_id)
    if model.can_apply(symbolic):
        model.apply(symbolic)
        print(f"✓ 应用模型 {model_id}: {model.chinese_name}")

# 4. 查看结果
print(f"最终参数: {symbolic.parameters}")
print(f"几何关系: {symbolic.geometric_relations}")
```

---

## 常见问题

### Q: 如何知道哪些模型已实现？
```python
library = TheoremLibrary()
print(f"已实现: {list(library.models.keys())}")
```

### Q: 如何判断模型是否应用成功？
```python
before = len(symbolic_state.applied_models)
model.apply(symbolic_state)
after = len(symbolic_state.applied_models)
success = (after > before)
```

### Q: 状态构造器是否自动提取参数？
是的，传入 `theorem_library` 参数时会自动应用标准方程模型（3-10）提取基本参数。

---

## 术语表

- **SymbolicState**: 符号状态，存储所有具体信息
- **AbstractState**: 抽象状态，用于神经网络的特征表示
- **TheoremModel**: 定理模型，封装数学定理的应用逻辑
- **completeness_score**: 完整度评分，反映问题求解进度 (0-1)
- **reasoning_depth**: 推理深度，已应用的模型数量
- **fact_expressions**: 题目事实表达式，描述已知条件
- **query_expressions**: 查询表达式，描述求解目标

---

**文档版本**: v1.0  
**维护**: EGR Team  
**最后更新**: 2026-01-18
