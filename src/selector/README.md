# 模型选择器模块 (Model Selector Module)

## 📋 概述

本模块实现基于最大熵原理的定理选择神经网络，学习 **P(model | state)** 概率分布。

## 🎯 核心功能

1. **MaxEntropyClassifier**: 80分类神经网络
2. **数据加载器**: 从 `train_state_model.json` 加载训练数据
3. **训练器**: 完整的训练、验证、Early stopping流程
4. **评估器**: Top-1/3/5准确率计算

## 🏗️ 模块结构

```
src/selector/
├── __init__.py           # 模块入口
├── data_loader.py        # 数据加载和预处理
├── model_selector.py     # MaxEntropyClassifier网络
└── trainer.py           # 训练器（Trainer类、训练函数）
```

## 🚀 快速开始

### 1. 安装依赖

```bash
pip install torch numpy
```

### 2. 测试功能

```bash
python scripts/selector/test_selector.py
```

这会运行：
- 数据加载测试
- 模型创建测试
- 前向传播测试
- 小规模训练测试（5 epochs）

### 3. 完整训练

```bash
python scripts/selector/train_selector.py
```

训练配置：
- Epochs: 100
- Batch size: 16
- Learning rate: 0.001
- Early stopping patience: 20

### 4. 查看结果

训练完成后：
- **模型权重**: `checkpoints/model_selector.pth`
- **训练报告**: `outputs/selector/training_metrics.json`

## 📊 数据格式

### 输入数据

**文件**: `data/train_state_model.json`

**结构**:
```json
{
  "total_samples": 52,
  "total_transitions": 135,
  "sample_results": [
    {
      "sample_id": 0,
      "transitions": [
        {
          "step": 1,
          "model_id": 5,
          "status": "success",
          "state_vector": [0.0, 1.0, ..., 0.8],  // 28维
          "abstract_state": {...}
        }
      ]
    }
  ]
}
```

### 训练样本提取

从JSON中提取所有 `status='success'` 的转换：
- **X**: `state_vector` (28维浮点数列表)
- **y**: `model_id` (0-79整数)

当前数据规模：
- 总样本数: 135
- 使用的模型数: 29/80
- 训练集: 108 (80%)
- 验证集: 27 (20%)

## 🧠 模型架构

### MaxEntropyClassifier

```
输入层:  [28]
  ↓ Linear + ReLU
隐藏层1: [64]
  ↓ Linear + ReLU
隐藏层2: [128]
  ↓ Dropout(0.1)
隐藏层3: [64]
  ↓ Linear + ReLU
输出层:  [80]
  ↓ Softmax
概率分布: P(model | state)
```

**参数量**: ~15,000

### 损失函数

```python
loss = CrossEntropyLoss(logits, true_model_id)
```

等价于最大似然估计 = 最大熵学习

## 📈 性能指标

### 预期结果（当前135样本）

- **Top-1准确率**: 20-30%
- **Top-3准确率**: 40-50%
- **Top-5准确率**: 50-60%

### 预期结果（未来10k样本）

- **Top-1准确率**: 50-60%
- **Top-3准确率**: 70-80%
- **Top-5准确率**: 80%+

### 实际价值

即使Top-1准确率较低，仍有重要价值：
1. **搜索空间缩小**: Top-5将搜索从80个候选缩小到5个 (6.25%)
2. **与规则结合**: 推理时用 `can_apply()` 过滤后准确率会提升
3. **概率先验**: 为信息增益计算提供先验分布

## 🔧 API使用

### 训练模型

```python
from src.selector import train_model

model, history = train_model(
    data_path='data/train_state_model.json',
    num_epochs=100,
    batch_size=16,
    learning_rate=0.001,
    save_path='checkpoints/model_selector.pth'
)
```

### 加载模型并推理

```python
import torch
from src.selector import MaxEntropyClassifier

# 加载模型
model = MaxEntropyClassifier()
checkpoint = torch.load('checkpoints/model_selector.pth')
model.load_state_dict(checkpoint['model_state_dict'])
model.eval()

# 推理
state_vector = torch.tensor([...], dtype=torch.float32)  # 28维
probs, best_model, entropy = model.predict(state_vector)

print(f"最优模型: {best_model}")
print(f"预测熵 H(Y|X): {entropy:.4f}")
print(f"Top-5概率: {probs.topk(5)}")
```

### 获取Top-K候选

```python
top_k_probs, top_k_ids = model.get_top_k(state_vector, k=5)

for i, (prob, model_id) in enumerate(zip(top_k_probs, top_k_ids)):
    print(f"Rank {i+1}: Model {model_id} (prob={prob:.3f})")
```

## 🔗 与三层熵架构的关系

本模块实现**第一层：策略学习 P(Y|X)**

### 完整架构

```
Layer 1: 策略学习 (本模块) ✅
  └─> P(model | state) - 最大熵分类器
  
Layer 2: 路径规划 (Module 4)
  └─> InfoGain = H(S_t) - H(S_{t+1})
  └─> 熵估计器: H(S)
  
Layer 3: 置信度加权 (Module 4)
  └─> Score = λ₁·P(Y|X) + λ₂·InfoGain - λ₃·H(Y|X)
  └─> H(Y|X) = -Σ P(y|x) log P(y|x)
```

### 输出接口

为后续模块准备：
- ✅ **P(Y|X)**: 80维概率分布
- ✅ **H(Y|X)**: 预测熵（不确定性度量）
- ✅ **Top-K**: 候选模型列表

## 📝 训练日志示例

```
======================================================================
开始训练 MaxEntropy Model Selector
======================================================================
训练轮数: 100
Early stopping patience: 20
学习率: 0.001
设备: cpu
保存路径: checkpoints/model_selector.pth
======================================================================
Epoch   1/100 | Train Loss: 4.3826 Acc: 0.093 | Val Loss: 4.3513 Top1: 0.111 Top3: 0.259 Top5: 0.370
Epoch  10/100 | Train Loss: 3.7542 Acc: 0.157 | Val Loss: 3.8214 Top1: 0.148 Top3: 0.333 Top5: 0.444
Epoch  20/100 | Train Loss: 3.2156 Acc: 0.213 | Val Loss: 3.4125 Top1: 0.185 Top3: 0.407 Top5: 0.519
  → 保存最佳模型 (Val Top-1 Acc: 0.185)
...
Early stopping at epoch 45
最佳验证准确率: 0.222 (Epoch 32)

======================================================================
训练完成!
======================================================================
总用时: 12.34秒
最佳Epoch: 32
最佳验证Top-1准确率: 0.222
最终验证Top-3准确率: 0.444
最终验证Top-5准确率: 0.556
======================================================================
```

## 🧪 测试

### 单元测试

```bash
# 测试数据加载
python -m src.selector.data_loader

# 测试模型
python -m src.selector.model_selector

# 测试训练
python -m src.selector.train
```

### 集成测试

```bash
python scripts/selector/test_selector.py
```

## 🔮 后续优化

### 短期

1. **类别不平衡处理**: 加权损失函数
2. **超参数调优**: 学习率、网络深度、Dropout
3. **数据增强**: 增加训练样本数量

### 中期

1. **更多训练数据**: 扩展到10k样本
2. **两阶段架构**: 规则筛选 + 神经网络排序
3. **Transformer架构**: 替代MLP

### 长期

1. **强化学习**: 基于推理成功率优化
2. **元学习**: 少样本适应新题型
3. **可解释性**: 注意力机制

## 📚 参考文档

- **项目工作流程**: `doc/project_workflow.md`
- **Module 3文档**: `doc/module3_training_data_constructor.md`
- **三层熵理论**: `docs/Three-layer entropy.md`
- **API参考**: `doc/api_reference.md`

## 📄 文件说明

### 核心代码

- `__init__.py`: 模块入口，导出主要接口
- `data_loader.py`: 数据加载、DataLoader创建、类别权重计算
- `model_selector.py`: MaxEntropyClassifier定义
- `trainer.py`: Trainer类、训练主函数、评估函数

### 脚本

- `scripts/selector/train_selector.py`: 完整训练脚本
- `scripts/selector/test_selector.py`: 功能测试脚本

### 输出

- `checkpoints/model_selector.pth`: 训练好的模型权重
- `outputs/selector/training_metrics.json`: 训练报告

## ❓ 常见问题

### Q1: 为什么准确率不高？

**A**: 数据量小（135样本 vs 80类别），这是正常的。主要价值在于：
- Top-K缩小搜索空间
- 与规则系统结合
- 提供概率先验

### Q2: 如何处理未见过的模型？

**A**: 网络仍会输出80维概率分布，只是未见过的模型概率会很低。推理时结合 `can_apply()` 规则可以过滤掉不可用的模型。

### Q3: 如何增加训练数据？

**A**: 
1. 标注更多Conic10K样本的模型序列
2. 运行 `scripts/state_model/generate_train_state_model.py`
3. 重新训练

### Q4: 可以使用GPU训练吗？

**A**: 可以，设置 `device='cuda'` 即可。但当前数据量小，CPU已足够快。

## 📊 版本历史

- **v1.0** (2026-01-20): 初始版本
  - 实现MaxEntropyClassifier
  - 实现数据加载和训练流程
  - 支持Top-1/3/5评估
  - Early stopping
  - 模型保存/加载

---

**维护者**: EGR Team  
**最后更新**: 2026-01-20
