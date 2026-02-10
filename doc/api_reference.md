# EGR API Reference

**版本**: v1.2  
**最后更新**: 2026-02-09  
**状态**: 40/80 模型已实现 (50%) | Module 3 完成 ✅ | Module 4 阶段1 完成 ✅

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

## 模型选择器模块 (Module 3)

### MaxEntropyClassifier
神经网络模型选择器 - P(model | state) 分类器

#### 初始化
```python
from src.selector import MaxEntropyClassifier

model = MaxEntropyClassifier(
    input_dim=28,      # 状态向量维度
    output_dim=80,     # 模型数量
    hidden_dims=(64, 128, 64),
    dropout_rate=0.1
)
```

#### predict()
推理接口 - 预测最优模型并计算不确定性
```python
import torch

state_vector = torch.randn(28)  # 28维状态向量
probs, best_model, entropy = model.predict(state_vector)

# 返回值:
# - probs: [80] 模型概率分布
# - best_model: 最优模型ID (int)
# - entropy: H(Y|X) 预测熵 (float)
```

**参数**: `state_vector` (Tensor) - [batch, 28] 或 [28] 状态向量  
**返回**: `Tuple[Tensor, int/Tensor, float]` - (概率分布, 最优模型ID, 预测熵)

#### get_top_k()
获取Top-K候选模型
```python
top_k_probs, top_k_ids = model.get_top_k(state_vector, k=5)

# Top-5候选模型
for i, (prob, model_id) in enumerate(zip(top_k_probs, top_k_ids)):
    print(f"Rank {i+1}: Model {model_id.item()} (prob={prob.item():.3f})")
```

**参数**:
- `state_vector` (Tensor) - [batch, 28] 或 [28] 状态向量
- `k` (int) - 返回前k个候选

**返回**: `Tuple[Tensor, Tensor]` - (Top-K概率, Top-K模型ID)

---

### train_model()
训练模型选择器
```python
from src.selector import train_model

model, history = train_model(
    data_path='data/train_state_model.json',
    num_epochs=100,
    batch_size=16,
    learning_rate=0.001,
    use_class_weights=False,
    patience=20,
    save_path='checkpoints/model_selector.pth',
    device=None  # 自动检测 CPU/MPS/CUDA
)
```

**参数**:
- `data_path` (str) - 训练数据路径
- `num_epochs` (int) - 训练轮数，默认100
- `batch_size` (int) - 批大小，默认16
- `learning_rate` (float) - 学习率，默认0.001
- `use_class_weights` (bool) - 是否使用类别权重
- `patience` (int) - Early stopping耐心值
- `save_path` (str) - 模型保存路径
- `device` (str) - 训练设备，None为自动检测

**返回**: `Tuple[MaxEntropyClassifier, Dict]` - (训练好的模型, 训练历史)

**训练历史**:
```python
{
    'train_loss': [...],
    'train_acc': [...],
    'val_loss': [...],
    'val_acc': [...],       # Top-1准确率
    'val_top3_acc': [...],  # Top-3准确率
    'val_top5_acc': [...]   # Top-5准确率
}
```

---

### load_training_data()
加载训练数据
```python
from src.selector import load_training_data

X, y = load_training_data('data/train_state_model.json')

# X: List[List[float]] - 状态向量列表 (每个28维)
# y: List[int] - 模型ID列表 (0-79)

print(f"训练样本数: {len(X)}")
print(f"特征维度: {len(X[0])}")
```

**参数**: `data_path` (str) - 数据文件路径  
**返回**: `Tuple[List[List[float]], List[int]]` - (状态向量, 模型ID)

---

### prepare_dataloaders()
准备训练和验证DataLoader
```python
from src.selector import prepare_dataloaders

train_loader, val_loader = prepare_dataloaders(
    state_vectors=X,
    model_ids=y,
    train_ratio=0.8,
    batch_size=16,
    shuffle=True,
    seed=42
)
```

**参数**:
- `state_vectors` (List[List[float]]) - 状态向量列表
- `model_ids` (List[int]) - 模型ID列表
- `train_ratio` (float) - 训练集比例，默认0.8
- `batch_size` (int) - 批大小，默认16
- `shuffle` (bool) - 是否打乱数据
- `seed` (int) - 随机种子

**返回**: `Tuple[DataLoader, DataLoader]` - (训练集, 验证集)

---

### 使用示例：完整训练流程

```python
from src.selector import train_model, MaxEntropyClassifier
import torch

# 1. 训练模型
print("开始训练...")
model, history = train_model(
    data_path='data/train_state_model.json',
    num_epochs=100,
    save_path='checkpoints/model_selector.pth'
)

print(f"最佳Top-1准确率: {max(history['val_acc']):.3f}")
print(f"最佳Top-3准确率: {max(history['val_top3_acc']):.3f}")

# 2. 加载模型推理
model = MaxEntropyClassifier()
checkpoint = torch.load('checkpoints/model_selector.pth')
model.load_state_dict(checkpoint['model_state_dict'])
model.eval()

# 3. 推理
from src.state import StateConstructor, TheoremLibrary

library = TheoremLibrary()
constructor = StateConstructor(theorem_library=library)

abstract, symbolic = constructor.construct_from_facts(
    fact_expressions="G: Hyperbola;Expression(G) = (x^2/3 - y^2 = 1)",
    query_expressions="Length(ImageinaryAxis(G))",
    reasoning_depth=0
)

# 获取状态向量
state_vector = torch.tensor(abstract.to_vector(), dtype=torch.float32)

# 预测
probs, best_model, entropy = model.predict(state_vector)

print(f"推荐模型: {best_model}")
print(f"预测概率: {probs[best_model]:.4f}")
print(f"预测熵 H(Y|X): {entropy:.4f}")

# 应用模型
recommended = library.get_model(best_model)
if recommended and recommended.can_apply(symbolic):
    recommended.apply(symbolic)
    print(f"✓ 成功应用模型 {best_model}: {recommended.chinese_name}")
```

---

## 推理引擎模块 (Module 4)

### ReasoningEngine
自动推理引擎 - 完整的问题求解器

#### 初始化
```python
from src.reasoning import ReasoningEngine, ModelSelector
from src.selector import MaxEntropyClassifier
from src.theorems import TheoremLibrary
from src.state import StateConstructor
import torch

# 加载组件
library = TheoremLibrary()
constructor = StateConstructor(theorem_library=library)

# 加载神经网络
neural_network = MaxEntropyClassifier()
checkpoint = torch.load('checkpoints/model_selector.pth')
neural_network.load_state_dict(checkpoint['model_state_dict'])
neural_network.eval()

# 创建选择器
selector = ModelSelector(
    neural_network=neural_network,
    theorem_library=library,
    strategy='neural_topk'  # 'neural_top1' 或 'neural_topk'
)

# 创建引擎
engine = ReasoningEngine(
    theorem_library=library,
    model_selector=selector,
    state_constructor=constructor,
    max_steps=20,
    completeness_threshold=0.95
)
```

**参数**:
- `max_steps` (int) - 最大推理步数，默认20
- `completeness_threshold` (float) - 完整度阈值，默认0.95
- `verbose` (bool) - 是否打印详细日志，默认True

#### solve()
求解数学问题
```python
result = engine.solve(
    facts="G: Hyperbola; Expression(G) = (x^2/3 - y^2 = 1)",
    query="Equation(Asymptote(G))"
)

# 结果
if result.success:
    print(f"答案: {result.answer}")
    print(f"步数: {result.num_steps}")
    print(f"模型序列: {result.model_names}")
    print(f"耗时: {result.elapsed_time:.2f}s")
else:
    print(f"失败: {result.failure_reason}")
```

**参数**:
- `facts` (str) - 事实表达式
- `query` (str) - 查询表达式
- `reasoning_depth` (int) - 初始推理深度，默认0

**返回**: `ReasoningResult` - 推理结果对象

---

### ModelSelector
模型选择器 - 结合神经网络和规则的选择策略

#### select()
选择下一个要应用的模型
```python
model, info = selector.select(
    symbolic_state=symbolic_state,
    abstract_state=abstract_state,
    top_k=5
)

if model:
    print(f"选中: {model.name}")
    print(f"置信度: {info['predicted_confidence']:.3f}")
```

**策略**:
- `neural_top1`: 神经网络Top-1 + can_apply过滤（快速）
- `neural_topk`: 神经网络Top-K + can_apply过滤（可靠）

---

### ReasoningResult
推理结果数据结构

**关键属性**:
```python
result.success              # bool - 是否成功
result.answer              # Any - 答案
result.num_steps           # int - 推理步数
result.model_sequence      # List[int] - 模型ID序列
result.model_names         # List[str] - 模型名称序列
result.completeness_scores # List[float] - 完整度变化
result.elapsed_time        # float - 耗时（秒）
result.reasoning_trace     # List[Dict] - 详细追踪
```

**方法**:
```python
result.get_summary()  # 获取简要总结
result.to_dict()      # 转换为字典（可序列化）
```

---

### 完整使用示例

```python
from src.reasoning import ReasoningEngine, ModelSelector
from src.selector import MaxEntropyClassifier
from src.theorems import TheoremLibrary
from src.state import StateConstructor
import torch

# 1. 初始化
library = TheoremLibrary()
constructor = StateConstructor(theorem_library=library)

neural_network = MaxEntropyClassifier()
checkpoint = torch.load('checkpoints/model_selector.pth')
neural_network.load_state_dict(checkpoint['model_state_dict'])
neural_network.eval()

selector = ModelSelector(neural_network, library, strategy='neural_topk')
engine = ReasoningEngine(library, selector, constructor, max_steps=15)

# 2. 求解问题
result = engine.solve(
    facts="G: Ellipse; Expression(G) = (x^2/4 + y^2 = 1)",
    query="Length(MajorAxis(G))"
)

# 3. 分析结果
print(result.get_summary())

if result.success:
    print(f"\n推理路径:")
    for i, (model_name, score) in enumerate(
        zip(result.model_names, result.completeness_scores[1:]), 1
    ):
        print(f"  {i}. {model_name} → 完整度={score:.2f}")
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

### Q: 如何使用模型选择器？
```python
from src.selector import MaxEntropyClassifier
import torch

# 加载模型
model = MaxEntropyClassifier()
checkpoint = torch.load('checkpoints/model_selector.pth')
model.load_state_dict(checkpoint['model_state_dict'])

# 获取状态向量（28维）
state_vector = torch.tensor(abstract_state.to_vector(), dtype=torch.float32)

# 推理
probs, best_model, entropy = model.predict(state_vector)
```

### Q: 如何训练模型选择器？
运行训练脚本：
```bash
python scripts/selector/train_selector.py
```
或使用API：
```python
from src.selector import train_model
model, history = train_model()
```

### Q: 如何使用推理引擎？
```python
from src.reasoning import ReasoningEngine, ModelSelector
# 初始化（见上文）
result = engine.solve(
    facts="G: Hyperbola; Expression(G) = (x^2/3 - y^2 = 1)",
    query="Equation(Asymptote(G))"
)
print(result.get_summary())
```

### Q: 推理引擎支持哪些选择策略？
- `neural_top1`: 只尝试Top-1（快速）
- `neural_topk`: 尝试Top-K直到成功（可靠）

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

**文档版本**: v1.2  
**维护**: EGR Team  
**最后更新**: 2026-02-09

---

## 更新日志

### v1.2 (2026-02-09)
- ✅ 新增 Module 4 推理引擎API
- ✅ ReasoningEngine接口
- ✅ ModelSelector接口
- ✅ ReasoningResult数据结构
- ✅ 完整使用示例

### v1.1 (2026-01-20)
- ✅ 新增 Module 3 模型选择器API
- ✅ MaxEntropyClassifier接口
- ✅ train_model, load_training_data等训练接口
- ✅ 完整使用示例

### v1.0 (2026-01-18)
- 初始版本
- 状态管理模块API
- 定理库模块API
- 40个模型索引
