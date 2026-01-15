# Module 1: 状态抽象与转换机制设计

**日期**: 2026-01-13  
**作者**: EGR Team  
**状态**: 设计完成，待实施

---

## 📋 任务概述

基于已完成的模型库（80个模型）和数据标注（models字段），设计并实现：
1. **状态抽象机制**：将复杂的fact_expressions抽象为有限的结构化状态
2. **状态转换机制**：定义模型应用后状态如何更新
3. **训练数据构建**：为每个样本生成完整的状态序列 (S0, S1, S2, ..., Sn)

---

## 🎯 核心设计理念

### 双层状态表示

```
┌─────────────────────────────────────────┐
│  粗粒度抽象状态 (AbstractState)          │
│  - 用于状态聚类和索引                     │
│  - 有限离散的特征空间                     │
│  - 可哈希、可向量化                       │
│                                          │
│  维度：                                   │
│  - 曲线类型 (4种)                        │
│  - 查询类型 (10种)                       │
│  - 信息类别 (11个布尔特征)               │
│  - 完整度得分 (0-1)                      │
│  - 推理深度 (步数)                       │
└─────────────────────────────────────────┘
              ↕ 双向映射
┌─────────────────────────────────────────┐
│  细粒度符号状态 (SymbolicState)          │
│  - 用于精确推理和模型应用                 │
│  - 存储所有具体信息                       │
│  - 支持符号计算                          │
│                                          │
│  内容：                                   │
│  - 实体声明 {G: Hyperbola, m: Number}   │
│  - 方程列表                              │
│  - 参数值字典                            │
│  - 几何关系列表                          │
│  - 坐标信息                              │
└─────────────────────────────────────────┘
```

### 为什么需要双层表示？

| 层次 | 用途 | 优势 |
|------|------|------|
| **AbstractState** | 模型选择、状态索引 | 有限状态空间，可以建立状态->模型的概率分布 |
| **SymbolicState** | 精确推理、符号计算 | 保留完整信息，支持复杂的模型应用 |

---

## 🔧 状态转换的本质

### 核心发现

通过分析数据集，我们发现：

**模型应用 = 信息增量**

```python
新状态 = 旧状态 + 模型输出的新信息

S₁ = S₀ ⊕ apply_model(M_i, S₀)
```

### 具体例子：ID=2的题目

**初始状态 S0:**
```
fact_expressions: 
  - G: Hyperbola
  - m: Number, m>0
  - Expression(G) = (x^2/4 - y^2/m^2 = 1)
  - Expression(OneOf(Asymptote(G))) = (5*x - 2*y = 0)

query: m
models: [5, 21]
```

**状态转换过程:**

```
S0 (初始):
  实体: {G: Hyperbola, m: Number}
  方程: [x^2/4 - y^2/m^2 = 1, 渐近线5x-2y=0]
  参数: {}
  ↓ 应用 Model 5 (Hyperbola_Equation_Standard_X)

S1 (提取参数):
  实体: {G: Hyperbola, m: Number}
  方程: [x^2/4 - y^2/m^2 = 1, 渐近线5x-2y=0]
  参数: {a^2: 4, b^2: m^2, a: 2, b: m}  ← 新增！
  关系: [a^2=4, b^2=m^2]                ← 新增！
  ↓ 应用 Model 21 (Hyperbola_Asymptote)

S2 (得到渐近线方程):
  实体: {G: Hyperbola, m: Number}
  方程: [..., 渐近线y = ±(m/2)x]        ← 新增！
  参数: {a: 2, b: m, a^2: 4, b^2: m^2}
  关系: [..., 渐近线方程: y = ±(m/2)x]  ← 新增！
  ↓ 比较两个渐近线方程

结论: m/2 = 5/2 → m = 5
```

### 另一个例子：ID=4的题目

**models: [5, 22, 19, 24, 13]**

```
S0 → Model 5  → S1 (提取双曲线参数 a, b)
S1 → Model 22 → S2 (焦点到渐近线距离 = b)
S2 → Model 19 → S3 (通径 = 2b²/a)
S3 → Model 24 → S4 (推导出 a = b)
S4 → Model 13 → S5 (计算 e = c/a = √2)
```

---

## 🏗️ 实现架构

### 文件结构

```
src/
├── state_abstractor.py        # 状态抽象器
│   ├── class SymbolicState    # 细粒度符号状态
│   ├── class AbstractState    # 粗粒度抽象状态
│   └── class StateAbstractor  # 抽象器主类
│
└── theorems/
    ├── theorem_library.py     # 定理库（80个模型）
    │   ├── class TheoremModel # 单个模型定义
    │   └── class TheoremLibrary # 模型库管理
    │
    └── model_transforms.py    # 各模型的状态转换函数
        ├── _transform_model_0()
        ├── _transform_model_1()
        └── ...

scripts/
└── data/
    └── build_state_sequences.py  # 构建状态序列的脚本
```

### 关键类设计

#### 1. SymbolicState（符号状态）

```python
@dataclass
class SymbolicState:
    # 实体声明
    entities: Dict[str, str]  # {name: type}
    # 例如: {'G': 'Hyperbola', 'm': 'Number', 'A': 'Point'}
    
    # 方程/表达式
    equations: List[str]
    # 例如: ['Expression(G) = (x^2/4 - y^2/m^2 = 1)', ...]
    
    # 参数值
    parameters: Dict[str, Any]  
    # 例如: {'a': 2, 'b': 'm', 'c': 'sqrt(a^2 + b^2)'}
    
    # 几何关系
    geometric_relations: List[str]
    # 例如: ['IsPerpendicular(AB, xAxis)', 'Distance(F, Asymptote) = b']
    
    # 坐标信息
    coordinates: Dict[str, Tuple]
    # 例如: {'F': ('c', 0), 'A': (1, 1/4)}
    
    # 约束条件
    constraints: List[str]
    # 例如: ['m > 0', 'a > b', 'b > 0']
```

#### 2. AbstractState（抽象状态）

```python
@dataclass
class AbstractState:
    # 维度1: 曲线类型（4种）
    curve_type: CurveType  # Ellipse, Hyperbola, Parabola, Circle
    
    # 维度2: 查询类型（10种）
    query_type: QueryType  # eccentricity, equation, coordinate, ...
    
    # 维度3: 已知信息（位向量）
    has_equation: bool
    has_parameters: Set[str]  # {a, b, c, e, ...}
    has_focus_info: bool
    has_vertex_info: bool
    has_point_on_curve: bool
    has_asymptote_info: bool
    has_directrix_info: bool
    has_tangent_info: bool
    has_distance_constraint: bool
    has_angle_constraint: bool
    has_perpendicular: bool
    
    # 维度4: 完整度（0.0-1.0）
    completeness_score: float
    
    # 维度5: 推理深度
    reasoning_depth: int
    
    def to_vector(self) -> List[float]:
        """转换为特征向量（用于神经网络）"""
        # 返回约30维的特征向量
        
    def to_hash(self) -> str:
        """计算状态哈希（用于索引）"""
        # 返回MD5哈希
```

#### 3. TheoremModel（定理模型）

```python
@dataclass
class TheoremModel:
    id: int                      # 模型ID (0-79)
    name: str                    # 模型名称
    description: str             # 描述
    category: str                # 类别
    
    preconditions: List[str]     # 前置条件
    outputs: List[str]           # 输出信息
    transform_func: callable     # 状态转换函数
    
    def can_apply(self, state: SymbolicState) -> bool:
        """检查是否可应用"""
        
    def apply(self, state: SymbolicState) -> SymbolicState:
        """应用模型，返回新状态"""
```

---

## 📊 状态空间规模估算

### 理论状态空间

```
状态数 = 曲线类型 × 查询类型 × 信息组合 × 完整度等级
      = 4 × 10 × 2^11 × 5
      ≈ 409,600 种状态
```

### 实际状态空间（基于数据分析）

| 数据集 | 理论状态数 | 实际出现 | 占比 |
|--------|-----------|---------|------|
| Conic10K (10000样本) | 409,600 | ~5,000-8,000 | 1.2%-2.0% |
| 前100样本 | 409,600 | ~150-200 | 0.05% |

**结论**：实际状态空间非常稀疏！大部分理论状态不会出现。

### 状态聚类

通过相似性聚类，可以将5000-8000个状态压缩到：
- **500-1000个代表性状态类别**
- 每个类别对应一个"状态原型"
- 建立 状态类别 → 模型 的概率分布

---

## 🚀 实施方案

### Phase 1: 核心框架实现（已完成）

✅ **状态抽象器** (`src/state_abstractor.py`)
- SymbolicState 类
- AbstractState 类
- StateAbstractor 类
- 解析fact_expressions的逻辑

✅ **定理库框架** (`src/theorems/theorem_library.py`)
- TheoremModel 类
- TheoremLibrary 类
- 前10个关键模型的实现

### Phase 2: 完善定理库（进行中）

🔄 **需要补充的70个模型**

优先级：
1. **高频模型**（20个）- 覆盖80%的问题
   - ✅ Model 0-2: 曲线定义
   - ✅ Model 5, 11-13: 参数关系
   - ✅ Model 21-22: 渐近线
   - 🔄 Model 41-43: 韦达定理
   - 🔄 Model 44: 点差法
   - 🔄 Model 47: 余弦定理
   - 🔄 Model 50-51: 弦长公式
   - 🔄 Model 17: 抛物线焦半径
   - 🔄 ...

2. **中频模型**（30个）
3. **低频模型**（30个）

### Phase 3: 构建训练数据（下一步）

**脚本**: `scripts/data/build_state_sequences.py`

**输入**: `data/train_with_models_1_100.json`

**输出**: `data/train_with_state_sequences_1_100.json`

**每个样本的输出格式**:
```json
{
  "id": 2,
  "text": "...",
  "fact_expressions": "...",
  "query_expressions": "...",
  "models": [5, 21],
  "state_sequence": [
    {
      "step": 0,
      "abstract_state": {
        "curve_type": "Hyperbola",
        "query_type": "value",
        "has_equation": true,
        "has_parameters": [],
        "has_asymptote_info": true,
        "completeness_score": 0.4,
        "reasoning_depth": 0,
        "state_hash": "a3f2e1...",
        "state_vector": [0, 0, 1, 0, ...]
      },
      "symbolic_state": {
        "entities": {"G": "Hyperbola", "m": "Number"},
        "equations": ["..."],
        "parameters": {},
        "geometric_relations": ["..."]
      },
      "applied_model": 5,
      "model_name": "Hyperbola_Equation_Standard_X"
    },
    {
      "step": 1,
      "abstract_state": {
        "curve_type": "Hyperbola",
        "query_type": "value",
        "has_equation": true,
        "has_parameters": ["a", "b"],
        "has_asymptote_info": true,
        "completeness_score": 0.6,
        "reasoning_depth": 1,
        "state_hash": "b4e3f2...",
        "state_vector": [0, 0, 1, 0, ...]
      },
      "symbolic_state": {
        "entities": {"G": "Hyperbola", "m": "Number"},
        "equations": ["..."],
        "parameters": {"a": 2, "b": "m", "a^2": 4, "b^2": "m^2"},
        "geometric_relations": ["...", "a^2=4", "b^2=m^2"]
      },
      "applied_model": 21,
      "model_name": "Hyperbola_Asymptote"
    },
    {
      "step": 2,
      "abstract_state": {
        "curve_type": "Hyperbola",
        "query_type": "value",
        "has_equation": true,
        "has_parameters": ["a", "b"],
        "has_asymptote_info": true,
        "completeness_score": 0.9,
        "reasoning_depth": 2,
        "state_hash": "c5f4e3...",
        "state_vector": [0, 0, 1, 0, ...]
      },
      "symbolic_state": {
        "entities": {"G": "Hyperbola", "m": "Number"},
        "equations": ["...", "渐近线y = ±(m/2)x"],
        "parameters": {"a": 2, "b": "m"},
        "geometric_relations": ["...", "渐近线方程: y = ±(m/2)x"]
      }
    }
  ],
  "num_steps": 2,
  "initial_completeness": 0.4,
  "final_completeness": 0.9
}
```

### Phase 4: 状态分布分析

**脚本**: 在 `build_state_sequences.py` 中包含

**输出**: `outputs/state_distribution_analysis.json`

**分析内容**:
1. 唯一状态数量
2. 每种状态出现的频率
3. **状态 → 模型的转移概率**（这是训练目标！）
4. 最常见的状态
5. 最常见的转移路径

---

## 📈 预期成果

### 数据规模（Conic10K全集）

```
原始数据:        10,000 个样本
处理后:
  - 状态序列数:   ~60,000 个状态（平均每题6步）
  - 唯一状态数:   ~5,000-8,000 个
  - 训练样本数:   ~50,000 个 (状态, 模型) 对
```

### 状态 → 模型 的概率分布

这是后续模型训练的**核心数据**！

```python
P(model_id | state_hash) = count(state → model) / count(state)

例如：
state_hash="a3f2e1..." (双曲线，有方程，无参数值) →
  model 5: 0.85   # 提取参数
  model 21: 0.10  # 直接用渐近线
  model 12: 0.05  # 其他
```

### 质量指标

| 指标 | 目标值 | 说明 |
|------|--------|------|
| 状态覆盖率 | >95% | 数据集中的样本能被成功抽象 |
| 状态转换正确率 | >90% | 应用模型后状态更新正确 |
| 完整度单调性 | >85% | completeness_score 随步数递增 |
| 状态去重率 | ~60% | 不同题目会经过相同状态 |

---

## 🧪 测试与验证

### 单元测试

```python
# 1. 测试状态抽象
def test_state_abstraction():
    # 验证fact_expressions能正确解析
    # 验证抽象状态的各个维度
    
# 2. 测试状态转换
def test_state_transformation():
    # 验证每个模型的应用逻辑
    # 验证参数提取的正确性
    
# 3. 测试状态序列构建
def test_sequence_building():
    # 用已知答案的样本验证
    # 检查状态序列的合理性
```

### 可视化验证

```python
# 状态转换可视化
S0 → [Model 5] → S1 → [Model 21] → S2
     ↓               ↓               ↓
  方程 only      +参数a,b        +渐近线方程
  完整度=0.4     完整度=0.6      完整度=0.9
```

---

## ⏱️ 时间估算

| 任务 | 预计时间 | 状态 |
|------|---------|------|
| Phase 1: 核心框架 | 1天 | ✅ 完成 |
| Phase 2: 完善定理库 (80个模型) | 3-4天 | 🔄 进行中 |
| Phase 3: 构建训练数据 | 1天 | ⏳ 待开始 |
| Phase 4: 数据分析与验证 | 1天 | ⏳ 待开始 |
| **总计** | **6-7天** | |

---

## 🎯 下一步行动

### 立即可做（今天）

1. **补充高频模型**（20个）
   - 优先实现：韦达定理、点差法、余弦定理、弦长公式
   - 这些模型覆盖80%的题目

2. **运行测试**
   - 用前10个样本测试状态序列构建
   - 检查状态转换的正确性

3. **完善状态抽象器**
   - 增强参数提取逻辑
   - 处理更多边界情况

### 本周内完成

4. **完成全部80个模型**
5. **在train_with_models_1_100.json上构建完整状态序列**
6. **生成状态分布分析报告**

### 后续工作

7. **扩展到Conic10K全集**（~10,000样本）
8. **开始模型训练**（使用状态序列数据）

---

## 📝 备注

### 设计权衡

1. **为什么用双层状态？**
   - 粗粒度：有限状态空间，便于建模
   - 细粒度：保留完整信息，支持精确推理

2. **为什么不直接用fact_expressions作为状态？**
   - fact_expressions是字符串，无限状态空间
   - 无法建立状态→模型的概率分布
   - 不利于神经网络处理

3. **状态哈希冲突怎么办？**
   - 使用MD5哈希，冲突概率极低
   - 如果出现冲突，状态向量会作为区分

### 潜在问题

1. **模型应用的前置条件检查**
   - 当前实现较简化
   - 需要增强前置条件的逻辑判断

2. **符号计算的复杂性**
   - 当前参数值用字符串表示（如 "sqrt(a^2 + b^2)"）
   - 后续可能需要集成符号计算库（如SymPy）

3. **状态序列的长度**
   - 目前平均6步
   - 有些复杂题目可能需要10+步
   - 需要设置合理的最大步数限制

---

**最后更新**: 2026-01-13  
**下次更新**: Phase 2完成后
