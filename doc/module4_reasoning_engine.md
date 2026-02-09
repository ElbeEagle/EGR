# Module 4: 推理引擎开发指南

**版本**: v1.0  
**日期**: 2026-02-09  
**状态**: 规划中  
**目标**: 实现基于神经网络的自动推理引擎

---

## 📋 目录

- [当前项目状态](#当前项目状态)
- [Module 4核心目标](#module-4核心目标)
- [技术架构](#技术架构)
- [实现路线图](#实现路线图)
- [API设计](#api设计)
- [测试策略](#测试策略)
- [性能目标](#性能目标)

---

## 当前项目状态

### ✅ 已完成的模块

#### Module 0: 定理模型库
- ✅ 40/80 模型实现（50%）
- ✅ 统一模型接口（BaseModel）
- ✅ 定理库（TheoremLibrary）
- ✅ can_apply()前置条件检查

**文件位置**:
- `src/theorems/theorem_library.py`
- `src/theorems/models/` (40个模型)

---

#### Module 1: 状态管理
- ✅ 符号状态（SymbolicState）
- ✅ 抽象状态（AbstractState）- 28维向量
- ✅ 状态构造器（StateConstructor）
- ✅ 状态序列构建器（StateSequenceBuilder）

**核心功能**:
```python
# 构造初始状态
constructor = StateConstructor(theorem_library)
abstract, symbolic = constructor.construct_from_facts(
    fact_expressions="...",
    query_expressions="..."
)

# 构建推理序列
builder = StateSequenceBuilder(library, constructor)
transitions = builder.build_sequence(
    fact_expressions="...",
    query_expressions="...",
    model_ids=[5, 21, 13]  # 人工标注的模型序列
)
```

**文件位置**:
- `src/state/symbolic_state.py`
- `src/state/abstract_state.py`
- `src/state/state_constructor.py`
- `src/state/state_sequence_builder.py`

---

#### Module 3: 模型选择神经网络
- ✅ MaxEntropyClassifier（28→64→128→64→80）
- ✅ 训练数据生成器（135样本）
- ✅ 完整训练流程（Early stopping）
- ✅ 训练完成：**Top-5准确率88.9%** ⭐

**核心功能**:
```python
from src.selector import MaxEntropyClassifier
import torch

# 加载模型
model = MaxEntropyClassifier()
checkpoint = torch.load('checkpoints/model_selector.pth')
model.load_state_dict(checkpoint['model_state_dict'])
model.eval()

# 推理
state_vector = torch.tensor(abstract_state.to_vector(), dtype=torch.float32)
probs, best_model, entropy = model.predict(state_vector)

# Top-K候选
top_k_probs, top_k_ids = model.get_top_k(state_vector, k=5)
```

**性能指标**:
- Top-1准确率: 50.0%
- Top-3准确率: 83.3%
- Top-5准确率: 88.9%
- 参数量: 23,632
- 推理速度: <2ms/预测

**文件位置**:
- `src/selector/model_selector.py`
- `src/selector/data_loader.py`
- `src/selector/trainer.py`
- `checkpoints/model_selector.pth`

---

### 📊 可用资源

**数据集**:
- `data/train_with_models_v2.json` - 完整训练数据（含人工标注序列）
- `data/train_state_model.json` - 135个状态-模型训练样本
- Conic10K数据集

**模型权重**:
- `checkpoints/model_selector.pth` - 训练好的模型选择器

**工具脚本**:
- `scripts/state_model/generate_train_state_model.py` - 生成训练数据
- `scripts/selector/train_selector.py` - 训练模型
- `scripts/selector/evaluate_selector.py` - 评估模型

---

## Module 4核心目标

### 主要任务

实现**自动推理引擎**，能够：
1. 接收数学问题（facts + query）
2. 自动选择定理模型
3. 迭代应用模型推导
4. 输出最终解答

### 核心能力

```python
engine = ReasoningEngine()
result = engine.solve(
    facts="G: Ellipse; Expression(G) = (x^2/4 + y^2 = 1)",
    query="Length(MajorAxis(G))"
)
# result.answer = 4
# result.steps = [Model 3, Model 11, Model 13, ...]
# result.success = True
```

### 设计原则

1. **模块化**: 各组件解耦，便于测试和优化
2. **可扩展**: 支持多种选择策略（Top-1, Top-K, 三层熵）
3. **可调试**: 记录完整推理过程
4. **鲁棒性**: 处理失败情况（回溯、超时）

---

## 技术架构

### 系统架构图

```
┌─────────────────────────────────────────────────────────┐
│                   ReasoningEngine                       │
│  ┌───────────────────────────────────────────────────┐ │
│  │  推理循环 (while not complete):                    │ │
│  │    1. ModelSelector.select()   ← 神经网络        │ │
│  │    2. TheoremLibrary.apply()   ← 定理库          │ │
│  │    3. StateConstructor.update() ← 状态管理       │ │
│  └───────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────┘
         ↓                ↓                  ↓
    ┌─────────┐     ┌──────────┐      ┌──────────┐
    │ Module 3│     │ Module 0 │      │ Module 1 │
    │  神经网络│     │  定理库  │      │  状态管理│
    └─────────┘     └──────────┘      └──────────┘
```

### 核心组件

#### 1. ReasoningEngine（主引擎）
```python
class ReasoningEngine:
    def __init__(self, 
                 theorem_library: TheoremLibrary,
                 model_selector: ModelSelector,
                 state_constructor: StateConstructor,
                 max_steps: int = 20):
        """初始化推理引擎"""
        
    def solve(self, facts: str, query: str) -> ReasoningResult:
        """求解问题"""
        
    def _is_complete(self, state: AbstractState) -> bool:
        """判断是否完成"""
        
    def _extract_answer(self, state: SymbolicState) -> Any:
        """提取答案"""
```

**职责**:
- 推理循环控制
- 状态完整性判断
- 解答提取
- 步数限制

---

#### 2. ModelSelector（模型选择器）
```python
class ModelSelector:
    def __init__(self, 
                 neural_network: MaxEntropyClassifier,
                 theorem_library: TheoremLibrary,
                 strategy: str = 'neural_top1'):
        """初始化选择器"""
        
    def select(self, 
               symbolic_state: SymbolicState, 
               abstract_state: AbstractState) -> BaseModel:
        """选择下一个模型"""
        
    def _neural_top1_strategy(self, ...) -> BaseModel:
        """策略1: 神经网络Top-1 + can_apply"""
        
    def _neural_top_k_strategy(self, ...) -> List[BaseModel]:
        """策略2: 神经网络Top-K + can_apply"""
        
    def _three_layer_entropy_strategy(self, ...) -> BaseModel:
        """策略3: 三层熵架构（高级）"""
```

**职责**:
- 神经网络推理
- 规则过滤（can_apply）
- 多种选择策略
- 置信度评估

---

#### 3. ReasoningResult（结果对象）
```python
@dataclass
class ReasoningResult:
    success: bool                    # 是否成功
    answer: Any                      # 答案
    steps: List[str]                 # 应用的模型序列
    states: List[AbstractState]      # 状态序列
    reasoning_trace: List[Dict]      # 详细推理过程
    elapsed_time: float              # 耗时
    num_steps: int                   # 步数
```

---

## 实现路线图

### 阶段1: 基础推理引擎（核心，必须）

**目标**: 最小可用版本（MVP）

**任务列表**:
- [ ] 实现 `ReasoningEngine` 类骨架
- [ ] 实现 `ModelSelector` 基础版（Top-1策略）
- [ ] 实现 `ReasoningResult` 数据结构
- [ ] 实现状态完整性判断
- [ ] 实现解答提取逻辑
- [ ] 单元测试

**预期成果**:
- 能在简单问题上运行
- 成功率预期: 20-30%

**代码位置**: `src/reasoning/`

---

### 阶段2: 增强与优化（推荐）

**目标**: 提升成功率和鲁棒性

**任务列表**:
- [ ] Top-K策略（尝试多个候选）
- [ ] 回溯机制（死路退回）
- [ ] 超时保护
- [ ] 性能优化（缓存、并行）
- [ ] 日志和可视化
- [ ] 批量测试脚本

**预期成果**:
- 成功率提升到: 40-60%
- 失败案例可调试

---

### 阶段3: 三层熵架构（高级，可选）

**目标**: 完整实现论文方法

**Layer 1**: P(Y|X) - ✅ 已完成（MaxEntropyClassifier）

**Layer 2**: 信息增益 InfoGain
```python
class EntropyEstimator(nn.Module):
    """状态熵估计器 H(S)"""
    def __init__(self, input_dim=28):
        # 28 → 64 → 32 → 1
        
    def forward(self, state_vector: Tensor) -> float:
        """估计状态熵值"""
        
def compute_info_gain(current_state, next_state) -> float:
    """InfoGain = H(S_current) - H(S_next)"""
    H_current = entropy_estimator(current_state.to_vector())
    H_next = entropy_estimator(next_state.to_vector())
    return H_current - H_next
```

**Layer 3**: 综合评分
```python
def compute_score(model_id, state):
    # Layer 1: P(Y|X)
    p_y_x = neural_network.predict(state)[model_id]
    
    # Layer 2: InfoGain
    next_state = simulate_apply(model_id, state)
    info_gain = compute_info_gain(state, next_state)
    
    # Layer 3: H(Y|X)
    _, _, h_y_x = neural_network.predict(state)
    
    # 综合评分
    score = λ1 * p_y_x + λ2 * info_gain - λ3 * h_y_x
    return score
```

**任务列表**:
- [ ] 训练熵估计器 H(S)
- [ ] 实现信息增益计算
- [ ] 实现综合评分函数
- [ ] 超参数调优（λ1, λ2, λ3）
- [ ] 对比实验

**预期成果**:
- 成功率目标: 60-80%
- 论文级别系统

---

## API设计

### 基础接口

```python
from src.reasoning import ReasoningEngine, ModelSelector
from src.theorems import TheoremLibrary
from src.state import StateConstructor
from src.selector import MaxEntropyClassifier
import torch

# 1. 初始化组件
library = TheoremLibrary()
constructor = StateConstructor(theorem_library=library)

# 加载神经网络
neural_network = MaxEntropyClassifier()
checkpoint = torch.load('checkpoints/model_selector.pth')
neural_network.load_state_dict(checkpoint['model_state_dict'])
neural_network.eval()

# 创建模型选择器
selector = ModelSelector(
    neural_network=neural_network,
    theorem_library=library,
    strategy='neural_top1'  # 或 'neural_topk', 'three_layer_entropy'
)

# 创建推理引擎
engine = ReasoningEngine(
    theorem_library=library,
    model_selector=selector,
    state_constructor=constructor,
    max_steps=20
)

# 2. 求解问题
result = engine.solve(
    facts="G: Ellipse; Expression(G) = (x^2/4 + y^2 = 1)",
    query="Length(MajorAxis(G))"
)

# 3. 查看结果
if result.success:
    print(f"答案: {result.answer}")
    print(f"步数: {result.num_steps}")
    print(f"模型序列: {result.steps}")
else:
    print(f"失败原因: {result.failure_reason}")
```

### 批量测试接口

```python
from src.reasoning import ReasoningTester

tester = ReasoningTester(engine)
results = tester.test_dataset(
    dataset_path='data/test_set.json',
    num_samples=100
)

# 生成报告
tester.generate_report(
    results=results,
    output_path='outputs/reasoning_report.json'
)
```

---

## 测试策略

### 单元测试

**测试文件**: `tests/reasoning/test_reasoning_engine.py`

```python
def test_reasoning_engine_init():
    """测试引擎初始化"""
    
def test_is_complete():
    """测试完整性判断"""
    
def test_extract_answer():
    """测试答案提取"""
    
def test_model_selector_top1():
    """测试Top-1选择策略"""
    
def test_model_selector_topk():
    """测试Top-K选择策略"""
```

### 集成测试

**简单问题**（3-5步）:
```
问题: 椭圆 x^2/4 + y^2 = 1 的长轴长度
期望: 4
步骤: Model 3 → Model 11 → 答案
```

**中等问题**（5-10步）:
```
问题: 双曲线的渐近线方程
期望: y = ±(b/a)x
步骤: Model 5 → Model 21 → ...
```

**困难问题**（10+步）:
```
问题: 涉及多个定理的综合题
需要: 回溯、多次尝试
```

### 性能测试

**指标**:
- 成功率（按难度分层）
- 平均步数
- 平均耗时
- Top-K命中率
- 回溯次数

**基准数据集**:
- Conic10K测试集（100题）
- 分层采样（简单/中等/困难）

---

## 性能目标

### 阶段1目标（基础版）

| 指标 | 目标值 | 说明 |
|------|--------|------|
| 简单问题成功率 | 40-60% | 3-5步问题 |
| 平均步数 | ≤10 | 不超过max_steps |
| 推理速度 | <1秒/题 | CPU环境 |

### 阶段2目标（优化版）

| 指标 | 目标值 | 说明 |
|------|--------|------|
| 整体成功率 | 50-70% | 全部问题 |
| 中等问题成功率 | 60-80% | 5-10步 |
| Top-5命中率 | >80% | 验证模型选择器 |

### 阶段3目标（完整版）

| 指标 | 目标值 | 说明 |
|------|--------|------|
| 整体成功率 | 60-80% | Conic10K |
| 困难问题成功率 | 40-60% | 10+步 |
| 论文可发表 | ✓ | 达到SOTA水平 |

---

## 开发规范

### 文件组织

```
src/reasoning/
├── __init__.py
├── reasoning_engine.py      # 主引擎
├── model_selector.py         # 模型选择器
├── reasoning_result.py       # 结果数据结构
└── entropy_estimator.py      # 熵估计器（阶段3）

scripts/reasoning/
├── test_reasoning.py         # 测试脚本
└── benchmark.py              # 性能测试

tests/reasoning/
├── test_engine.py
├── test_selector.py
└── test_integration.py

outputs/reasoning/
├── test_results.json         # 测试结果
├── benchmark_report.json     # 性能报告
└── failure_cases.json        # 失败案例
```

### 代码风格

- 遵循PEP 8
- 类型注解（typing）
- 详细文档字符串
- 单元测试覆盖率 >80%

### 日志记录

```python
import logging

logger = logging.getLogger('reasoning_engine')

# 推理过程日志
logger.info(f"Step {i}: Selected Model {model_id}")
logger.debug(f"State vector: {state.to_vector()}")
logger.warning(f"Model {model_id} failed, trying next")
logger.error(f"Max steps reached without solution")
```

---

## 参考文档

- **Module 3文档**: `doc/module3_training_data_constructor.md`
- **API参考**: `doc/api_reference.md`
- **项目工作流**: `doc/project_workflow.md`
- **三层熵理论**: `docs/Three-layer entropy.md`

---

## 常见问题

### Q1: 如何判断状态是否完整？
```python
def is_complete(state: AbstractState) -> bool:
    return state.completeness_score >= 0.95  # 阈值可调
```

### Q2: 如何处理模型应用失败？
- 策略1: 尝试Top-K中的下一个候选
- 策略2: 回溯到上一步
- 策略3: 记录失败并继续

### Q3: 如何提取答案？
```python
def extract_answer(symbolic_state: SymbolicState) -> Any:
    # 从symbolic_state中查找query对应的值
    query_obj = symbolic_state.get_object_by_name(query_name)
    if hasattr(query_obj, 'value'):
        return query_obj.value
    # 或计算表达式
```

### Q4: 三层熵架构是否必须？
- 基础版不需要（只用P(Y|X)）
- 追求高性能时实现
- 论文发表需要

---

## 更新日志

### v1.0 (2026-02-09)
- 初始版本
- 完成Module 1-3总结
- 制定Module 4开发计划

---

**作者**: EGR Team  
**最后更新**: 2026-02-09  
**状态**: 准备开始实现 🚀
