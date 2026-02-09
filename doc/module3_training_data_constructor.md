# Module 3: 训练数据构造器与模型选择网络

**版本**: v1.2  
**日期**: 2026-01-20  
**更新**: 神经网络实现完成 ✅ | 训练数据已生成 ✅  
**目的**: 训练神经网络学习 P(model | state)，实现自动模型选择

---

## ✅ 数据准备状态

**训练数据已生成**: `data/train_state_model.json` (142KB)

```
✓ 总样本数: 52
✓ 总训练样本数: 135
✓ 状态向量维度: 28维
✓ 模型ID范围: 0-79
✓ 数据质量验证: 全部通过
```

**生成脚本**: `scripts/state_model/generate_train_state_model.py`  
**加载示例**: `scripts/state_model/example_load_training_data.py`  
**详细文档**: `scripts/state_model/README.md`

---

## 📋 概述

本模块实现**模型选择神经网络**，这是EGR系统的核心：从当前状态预测应该选择哪个定理模型。

### 核心思想

```
人类标注的模型序列 (63样本)
    ↓
状态序列构建 (StateSequenceBuilder)
    ↓
提取成功转换 (135个训练样本)
    ↓ [✅ 已完成]
训练数据 train_state_model.json (28维 × 135个)
    ↓ [✅ 已完成]
训练神经网络 P(model | state)
    ↓ [可开始训练]
推理引擎的模型选择能力
```

---

## 🚀 快速开始

### 加载训练数据

```python
import json

# 加载数据
with open('data/train_state_model.json') as f:
    data = json.load(f)

# 提取训练样本
X = [trans['state_vector'] for sample in data['sample_results'] 
     for trans in sample['transitions']]
y = [trans['model_id'] for sample in data['sample_results'] 
     for trans in sample['transitions']]

print(f"训练样本数: {len(X)}")  # 135
print(f"特征维度: {len(X[0])}")  # 28
```

### 数据统计

```python
# 查看模型分布
from collections import Counter
model_counts = Counter(y)
print(f"使用的模型数: {len(model_counts)}/80")
print(f"Top 5高频模型: {model_counts.most_common(5)}")
```

---

## 🎯 核心目标

### 功能目标

1. ~~**数据提取**: 从状态序列提取训练样本~~ ✅ 已完成
2. **网络训练**: 训练最大熵分类器 P(Y|X)
3. **模型部署**: 保存并验证训练好的模型

### 性能目标

- **Top-1准确率**: > 25% （基线，数据量较小）
- **Top-3准确率**: > 40%
- **Top-5准确率**: > 50%

### 理论目标

- 实现最大熵原理下的定理选择
- 为后续三层熵架构奠定基础

---

## 📥 输入

### 主要输入

**文件**: `data/train_state_model.json` (Stage 2.3产出)

**数据结构**:
```json
{
  "total_samples": 52,
  "total_transitions": 135,
  "sample_results": [
    {
      "sample_id": 0,
      "problem": "题目文本...",
      "transitions": [
        {
          "step": 1,
          "model_id": 5,
          "model_name": "Hyperbola_Equation_Standard_X",
          "status": "success",
          "abstract_state": {
            "curve_type": "hyperbola",
            "query_type": "length",
            "param_count": 4,
            "completeness_score": 0.800,
            "has_focus_info": true,
            "has_asymptote_info": false,
            "reasoning_depth": 1
          },
          "state_vector": [0.0, 1.0, 0.0, ..., 0.8, 0.1]
        }
      ]
    }
  ]
}
```

### 可用数据规模

- 总样本数: 52
- **有效训练样本**: 135 (status='success')
- 平均每样本: ~2.6个训练点
- 使用的模型数: 29/80

---

## 📤 输出

### 1. 训练数据集

**文件**: `data/train_state_model.json` (已生成)

**格式**: 详见输入部分，数据已经是可用的训练格式

**提取训练样本**:
```python
# 从 train_state_model.json 提取 (state_vector, model_id) 对
X = []  # 特征
y = []  # 标签

for sample in data['sample_results']:
    for trans in sample['transitions']:
        X.append(trans['state_vector'])  # 28维
        y.append(trans['model_id'])      # 0-79
```

### 2. 训练好的模型

**文件**: `models/model_selector.pth`

**内容**: PyTorch模型权重（神经网络参数）

### 3. 评估报告

**文件**: `outputs/training_metrics.json`

**内容**:
```json
{
  "train_accuracy": 0.35,
  "val_accuracy": 0.28,
  "top3_accuracy": 0.45,
  "top5_accuracy": 0.52,
  "loss_curve": [...]
}
```

---

## 🏗️ 模块架构

### 三个核心组件

```
1. TrainingDataExtractor        (数据提取器)
   └─> 从状态序列提取训练样本
   
2. MaxEntropyClassifier         (最大熵分类器)
   └─> 神经网络: P(model | state)
   
3. ModelSelectorTrainer         (训练器)
   └─> 训练、验证、保存模型
```

---

## 🔧 功能规格

### 组件1: TrainingDataExtractor

**功能**: 提取训练样本

**输入**: `data/train_state_model.json` (已生成)  
**输出**: 训练数据列表 `[(X, y), ...]`

**核心逻辑**:
```python
def load_training_data(data_path='data/train_state_model.json'):
    with open(data_path) as f:
        data = json.load(f)
    
    X, y = [], []
    
    for sample in data['sample_results']:
        for trans in sample['transitions']:
            # 状态向量已经在数据中
            X.append(trans['state_vector'])  # 28维
            y.append(trans['model_id'])      # 0-79
    
    return X, y
```

**数据特点**:
- ✅ 已过滤：只包含 `status='success'` 的转换
- ✅ 已排除：初始状态 (step=0)
- ✅ 状态向量已生成：28维浮点数列表

---

### 组件2: MaxEntropyClassifier

**功能**: 神经网络模型 P(model | state)

**网络架构**:
```
输入层:  28维 (state_vector)
隐藏层1: 64维 + ReLU
隐藏层2: 128维 + ReLU + Dropout(0.1)
隐藏层3: 64维 + ReLU
输出层:  80维 (模型概率分布)
激活:    Softmax
```

**前向传播**:
```python
def forward(state_vector):
    # state_vector: [batch, 28]
    x = F.relu(fc1(state_vector))      # [batch, 64]
    x = F.relu(fc2(x))                 # [batch, 128]
    x = F.dropout(x, p=0.1)
    x = F.relu(fc3(x))                 # [batch, 64]
    logits = fc4(x)                    # [batch, 80]
    probs = F.softmax(logits, dim=-1)  # [batch, 80]
    return probs
```

**损失函数**: CrossEntropyLoss (等价于最大似然 = 最大熵)

---

### 组件3: ModelSelectorTrainer

**功能**: 训练管理

**训练流程**:
```python
1. 数据划分: train(80%) / val(20%)
2. 训练循环:
   - Epoch: 100-200
   - Batch size: 16
   - Optimizer: Adam (lr=0.001)
   - Early stopping: patience=20
3. 评估指标:
   - Top-1, Top-3, Top-5 准确率
   - 损失曲线
4. 模型保存: 保存最佳验证准确率的模型
```

---

## 🎨 实现方案

### 方案A: 全80分类 + 推理时Mask（当前阶段）⭐

**训练阶段**:
```python
# 标准80分类，不做特殊处理
model = MaxEntropyClassifier(input_dim=28, output_dim=80)
loss = CrossEntropyLoss(probs, true_model_id)

# 训练数据: 135个(state_vector, model_id)对
# - state_vector: 28维
# - model_id: 0-79范围
# - 实际使用的模型: 29个
```

**推理阶段** (后续Module 4实现):
```python
def select_model(symbolic_state, abstract_state):
    # 1. 神经网络预测
    state_vector = abstract_state.to_vector()
    probs = classifier(state_vector)  # [80]
    
    # 2. 前置条件筛选 (规则约束)
    valid_models = []
    for model_id in range(80):
        model = library.get_model(model_id)
        if model and model.can_apply(symbolic_state):
            valid_models.append(model_id)
    
    # 3. Mask + 归一化
    masked_probs = torch.zeros(80)
    masked_probs[valid_models] = probs[valid_models]
    
    if masked_probs.sum() > 0:
        masked_probs = masked_probs / masked_probs.sum()
    
    # 4. 选择最高概率
    best_model = masked_probs.argmax().item()
    
    return best_model, masked_probs
```

**优点**:
- ✅ 实现简单，训练时无需改动
- ✅ 数据充分利用（135个样本全用于80分类）
- ✅ 结合规则（can_apply）和学习（神经网络）
- ✅ 符合渐进式开发思路

---

### 方案B: 两阶段架构（后续优化）

**适用场景**: 数据量增大后，候选模型筛选成为瓶颈时

**实现思路**:
```python
# 第一阶段: 规则筛选
candidates = rule_based_filter(state)  # 10-15个候选

# 第二阶段: 神经网络排序（只对候选集）
candidate_probs = classifier(state_vector)[candidates]
best_model = candidates[candidate_probs.argmax()]
```

**改进点**:
- 更高效（只计算候选集）
- 更符合实际推理流程
- 需要更多训练数据支持

**升级路径**: 
- 当训练样本 > 500 时考虑
- 当推理速度成为瓶颈时考虑

---

## 🔗 与三层熵架构的关系

本模块实现**第一层：策略学习 P(Y|X)**

### 三层熵完整架构

```
Layer 1: 策略学习 (本模块)
  └─> P(model | state) - 最大熵分类器
  
Layer 2: 路径规划 (Module 4)
  └─> InfoGain = H(S_t) - H(S_{t+1})
  └─> 熵估计器: H(S)
  
Layer 3: 置信度加权 (Module 4)
  └─> Score = λ₁·P(Y|X) + λ₂·InfoGain - λ₃·H(Y|X)
  └─> H(Y|X) = -Σ P(y|x) log P(y|x)
```

### 为后续模块准备

- ✅ P(Y|X) 输出 → 用于 Layer 3 综合得分
- ✅ 状态向量化 → 为 H(S) 估计器准备输入格式
- ✅ 训练框架 → 可复用于熵估计器训练

---

## ✅ 验收标准

### 必须达成

- [x] 成功提取135个训练样本 ✅
- [x] 训练数据格式验证 ✅
- [x] 状态向量维度28维 ✅
- [x] 实现 `MaxEntropyClassifier` 网络 ✅
- [x] 实现完整训练流程（支持100+ epochs）✅
- [x] 实现Top-1/3/5准确率评估 ✅
- [x] 保存模型权重接口（`checkpoints/model_selector.pth`）✅
- [x] 生成评估报告接口（`outputs/selector/training_metrics.json`）✅
- [ ] 运行完整训练并达到性能目标（待用户运行）

### 可选增强

- [ ] 类别不平衡处理（加权损失）
- [ ] 超参数调优（学习率、网络深度）
- [ ] 可视化（损失曲线、混淆矩阵）
- [ ] 模型解释性分析

---

## 📂 文件结构

```
scripts/state_model/
├── generate_train_state_model.py    # 训练数据生成器（已完成）
├── example_load_training_data.py    # 数据加载示例（已完成）
└── README.md                         # 说明文档（已完成）

data/
└── train_state_model.json           # 训练数据（已生成，142KB）

src/training/                         # 待实现
├── __init__.py
├── data_loader.py                   # 数据加载器
├── model_selector.py                # MaxEntropyClassifier
└── train.py                         # ModelSelectorTrainer

models/                               # 待生成
└── model_selector.pth               # 训练好的模型

outputs/                              # 待生成
├── training_log.txt                 # 训练日志
└── training_metrics.json            # 评估结果

dev_logs/
└── module3_completion.md            # 完成报告
```

---

## 🧪 测试与验证

### 单元测试

```python
# 测试数据加载
def test_data_loading():
    X, y = load_training_data('data/train_state_model.json')
    assert len(X) == 135
    assert len(y) == 135
    assert all(len(x) == 28 for x in X)
    assert all(0 <= yi < 80 for yi in y)

# 测试模型前向传播
def test_model_forward():
    model = MaxEntropyClassifier(input_dim=28, output_dim=80)
    state_vector = torch.randn(1, 28)
    probs = model(state_vector)
    assert probs.shape == (1, 80)
    assert abs(probs.sum() - 1.0) < 1e-6

# 测试mask机制
def test_mask_and_normalize():
    probs = torch.tensor([0.1, 0.2, 0.3, 0.4])
    valid_models = [0, 2]
    masked = mask_and_normalize(probs, valid_models)
    assert masked[1] == 0  # 被mask掉
    assert masked[3] == 0
    assert abs(masked.sum() - 1.0) < 1e-6
```

### 集成测试

```python
# 端到端测试
def test_end_to_end():
    # 1. 数据加载
    X, y = load_training_data('data/train_state_model.json')
    
    # 2. 训练
    model = train_model(X, y, epochs=10)
    
    # 3. 推理
    test_state = torch.tensor(X[0], dtype=torch.float32).unsqueeze(0)
    probs = model(test_state)
    
    assert probs.max() > 0.1  # 至少有些置信度
    assert probs.shape == (1, 80)
```

---

## 📊 预期结果

### 训练曲线

```
Epoch 1:   Train Loss: 4.38, Val Acc: 8%
Epoch 20:  Train Loss: 3.12, Val Acc: 18%
Epoch 50:  Train Loss: 2.45, Val Acc: 25%
Epoch 100: Train Loss: 1.92, Val Acc: 28%  ← 最佳
Epoch 150: Train Loss: 1.65, Val Acc: 26%  (过拟合)
```

### 性能指标

```
训练集 (108样本):
  - Top-1: ~35%
  - Top-3: ~50%
  - Top-5: ~58%

验证集 (27样本):
  - Top-1: ~28%
  - Top-3: ~45%
  - Top-5: ~52%
```

### 为什么准确率不高？

1. **数据量小**: 135样本 vs 80类别
2. **类别不平衡**: 高频模型(5,21,13)多，低频模型少
3. **状态空间稀疏**: 相似状态可能有不同选择

### 实际价值

- ✅ **候选筛选**: Top-5准确率52% → 缩小搜索空间到5个候选
- ✅ **与规则结合**: mask后准确率会提升
- ✅ **可解释性**: 概率分布提供决策依据

---

## 🔮 后续扩展方向

### 短期（Module 4）

1. 实现熵估计器 H(S)
2. 实现综合得分 Score(Y)
3. 完整推理引擎

### 中期

1. 增加训练数据（标注更多样本）
2. 升级到方案B（两阶段架构）
3. 引入Transformer架构

### 长期

1. 强化学习优化（基于推理成功率）
2. 元学习（少样本适应新题型）
3. 可解释性增强（注意力机制）

---

## 📚 参考资料

### 理论基础

- `docs/Three-layer entropy.md`: 三层熵架构详解
- 最大熵原理: 交叉熵损失 = 最大似然 = 最大熵

### 实现参考

- `src/state/abstract_state.py`: `to_vector()` 方法（28维）
- `data/train_state_model.json`: 训练数据（已生成）
- `scripts/state_model/generate_train_state_model.py`: 数据生成脚本
- `scripts/state_model/example_load_training_data.py`: 数据加载示例

### 相关模块

- Module 0: 定理模型库 (`can_apply`机制)
- Module 1: 状态表示 (特征向量化，28维)
- Module 2: 状态序列构建 (训练数据生成，135个样本)

---

## 📊 当前进度

### 已完成 ✅

1. **训练数据生成**
   - 脚本: `scripts/state_model/generate_train_state_model.py`
   - 数据: `data/train_state_model.json` (142KB)
   - 样本数: 135个训练样本
   - 维度: 28维状态向量

2. **数据验证**
   - 状态向量维度一致性 ✓
   - 模型ID范围验证 ✓
   - 完整度范围验证 ✓
   - 数据加载示例 ✓

3. **文档**
   - 数据格式说明 ✓
   - 加载示例代码 ✓
   - 使用说明 ✓

### 待实现 📝

1. **运行训练**（用户操作）
   - 安装依赖: `pip install torch numpy`
   - 运行训练: `python scripts/selector/train_selector.py`
   - 预计用时: 1-2分钟（CPU）

2. **性能验证**
   - 检查Top-1/3/5准确率是否达标
   - 分析训练报告
   - 如需要可调整超参数重新训练

### 已完成 ✅ (2026-01-20)

1. **神经网络实现**
   - ✅ `src/selector/model_selector.py`: MaxEntropyClassifier类（245行）
   - ✅ `src/selector/data_loader.py`: 数据加载器（170行）
   - ✅ `src/selector/trainer.py`: 训练器（395行）
   - ✅ `src/selector/__init__.py`: 模块入口

2. **训练基础设施**
   - ✅ 完整训练/验证循环
   - ✅ Early stopping机制
   - ✅ Top-1/3/5评估
   - ✅ 类别权重支持
   - ✅ 模型保存/加载

3. **脚本与文档**
   - ✅ `scripts/selector/train_selector.py`: 完整训练脚本
   - ✅ `scripts/selector/test.py`: 功能测试脚本
   - ✅ `src/selector/README.md`: 详细文档（400行）
   - ✅ `src/selector/USAGE.md`: 使用指南（250行）
   - ✅ `dev_logs/module3_training_completion.md`: 完成报告（550行）

---

## 📦 交付物清单

### 核心代码（~810行）
- ✅ `src/selector/__init__.py`
- ✅ `src/selector/data_loader.py`
- ✅ `src/selector/model_selector.py`
- ✅ `src/selector/train.py`

### 脚本（~150行）
- ✅ `scripts/selector/train.py`
- ✅ `scripts/selector/test.py`

### 文档（~1200行）
- ✅ `src/selector/README.md`
- ✅ `src/selector/USAGE.md`
- ✅ `dev_logs/module3_training_completion.md`
- ✅ `MODULE3_SUMMARY.md`

### 配置
- ✅ `requirements.txt`
- ✅ `checkpoints/` 目录
- ✅ `outputs/selector/` 目录

---

**最后更新**: 2026-01-20  
**维护者**: EGR Team  
**版本历史**: 
- v1.2 (2026-01-20): 神经网络实现完成 ✅
- v1.1 (2026-01-19): 训练数据生成完成 ✅
- v1.0 (2026-01-18): 初始版本
