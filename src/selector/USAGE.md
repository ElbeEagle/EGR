# 模型选择器使用指南

## 🚀 快速开始

### 1. 安装依赖

```bash
cd /Users/ebeleagel/Documents/GitHub/EGR
pip install torch numpy
```

### 2. 运行测试（推荐先运行）

```bash
python scripts/selector/test.py
```

这会测试：
- ✅ 数据加载
- ✅ 模型创建
- ✅ 前向传播
- ✅ 小规模训练（5 epochs）

### 3. 完整训练

```bash
python scripts/selector/train.py
```

训练配置：
- 数据: `data/train_state_model.json` (135样本)
- Epochs: 100
- Batch size: 16
- 学习率: 0.001
- Early stopping: 20 epochs patience

预计用时：1-2分钟（CPU）

### 4. 查看结果

训练完成后：
```bash
# 模型权重
ls -lh checkpoints/model_selector.pth

# 训练报告
cat outputs/selector/training_metrics.json
```

## 📝 使用示例

### 示例1: 训练模型

```python
from src.selector import train_model

# 使用默认配置训练
model, history = train_model()

# 查看训练历史
print(f"最佳验证Top-1准确率: {max(history['val_acc']):.3f}")
print(f"最佳验证Top-3准确率: {max(history['val_top3_acc']):.3f}")
print(f"最佳验证Top-5准确率: {max(history['val_top5_acc']):.3f}")
```

### 示例2: 加载模型并推理

```python
import torch
from src.selector import MaxEntropyClassifier

# 创建模型
model = MaxEntropyClassifier()

# 加载权重
checkpoint = torch.load('checkpoints/model_selector.pth')
model.load_state_dict(checkpoint['model_state_dict'])
model.eval()

# 准备输入（28维状态向量）
state_vector = torch.randn(28)

# 推理
probs, best_model, entropy = model.predict(state_vector)

print(f"预测的最优模型ID: {best_model}")
print(f"该模型的概率: {probs[best_model]:.4f}")
print(f"预测熵 H(Y|X): {entropy:.4f}")
```

### 示例3: 获取Top-K候选

```python
import torch
from src.selector import MaxEntropyClassifier

# 加载模型
model = MaxEntropyClassifier()
checkpoint = torch.load('checkpoints/model_selector.pth')
model.load_state_dict(checkpoint['model_state_dict'])
model.eval()

# 输入状态
state_vector = torch.randn(28)

# 获取Top-5候选
top_k_probs, top_k_ids = model.get_top_k(state_vector, k=5)

print("Top-5候选模型:")
for i, (prob, model_id) in enumerate(zip(top_k_probs, top_k_ids)):
    print(f"  Rank {i+1}: Model {model_id.item()} (概率={prob.item():.4f})")
```

### 示例4: 自定义训练配置

```python
from src.selector import train_model

model, history = train_model(
    data_path='data/train_state_model.json',
    num_epochs=50,              # 减少轮数
    batch_size=8,               # 更小的batch
    learning_rate=0.0005,       # 更小的学习率
    use_class_weights=True,     # 使用类别权重
    patience=15,                # 更早的early stopping
    save_path='checkpoints/my_model.pth',
    device='cpu'                # 或 'cuda'
)
```

### 示例5: 评估已训练的模型

```python
from src.selector import evaluate_model

metrics = evaluate_model(
    model_path='checkpoints/model_selector.pth',
    data_path='data/train_state_model.json'
)

print("评估结果:")
print(f"  Loss: {metrics['loss']:.4f}")
print(f"  Top-1 Acc: {metrics['top1_acc']:.3f}")
print(f"  Top-3 Acc: {metrics['top3_acc']:.3f}")
print(f"  Top-5 Acc: {metrics['top5_acc']:.3f}")
```

### 示例6: 批量推理

```python
import torch
from src.selector import MaxEntropyClassifier

# 加载模型
model = MaxEntropyClassifier()
checkpoint = torch.load('checkpoints/model_selector.pth')
model.load_state_dict(checkpoint['model_state_dict'])
model.eval()

# 批量输入（例如8个状态）
batch_states = torch.randn(8, 28)

# 批量推理
probs, best_models, avg_entropy = model.predict(batch_states)

print(f"批量大小: {batch_states.shape[0]}")
print(f"输出概率分布shape: {probs.shape}")  # [8, 80]
print(f"最优模型IDs: {best_models}")          # [8]
print(f"平均预测熵: {avg_entropy:.4f}")
```

## 🔧 高级用法

### 使用类别权重处理不平衡

```python
from src.selector import train_model

# 开启类别权重
model, history = train_model(
    use_class_weights=True  # 对低频模型增加权重
)
```

### 手动控制训练循环

```python
from src.selector import (
    load_training_data,
    prepare_dataloaders,
    MaxEntropyClassifier,
    Trainer
)
import torch

# 1. 加载数据
X, y = load_training_data('data/train_state_model.json')
train_loader, val_loader = prepare_dataloaders(X, y, batch_size=16)

# 2. 创建模型
model = MaxEntropyClassifier()

# 3. 创建训练器
trainer = Trainer(
    model=model,
    device='cpu',
    learning_rate=0.001,
    use_class_weights=False
)

# 4. 训练
history = trainer.fit(
    train_loader=train_loader,
    val_loader=val_loader,
    num_epochs=100,
    patience=20,
    save_path='checkpoints/model_selector.pth'
)

# 5. 查看历史
import matplotlib.pyplot as plt
plt.plot(history['train_loss'], label='Train Loss')
plt.plot(history['val_loss'], label='Val Loss')
plt.legend()
plt.savefig('loss_curve.png')
```

### 在推理引擎中使用（Module 4集成）

```python
import torch
from src.selector import MaxEntropyClassifier

class ReasoningEngine:
    def __init__(self):
        # 加载模型选择器
        self.classifier = MaxEntropyClassifier()
        checkpoint = torch.load('checkpoints/model_selector.pth')
        self.classifier.load_state_dict(checkpoint['model_state_dict'])
        self.classifier.eval()
    
    def select_model(self, symbolic_state, abstract_state):
        """
        选择下一个要应用的模型
        
        结合神经网络预测和规则约束
        """
        # 1. 神经网络预测概率分布
        state_vector = torch.tensor(
            abstract_state.to_vector(), 
            dtype=torch.float32
        )
        probs, _, H_Y_X = self.classifier.predict(state_vector)
        
        # 2. 规则筛选可应用的模型
        valid_models = []
        for model_id in range(80):
            model = self.theorem_library.get_model(model_id)
            if model and model.can_apply(symbolic_state):
                valid_models.append(model_id)
        
        # 3. Mask不可用模型，重新归一化
        valid_tensor = torch.tensor(valid_models)
        masked_probs = torch.zeros(80)
        masked_probs[valid_tensor] = probs[valid_tensor]
        
        if masked_probs.sum() > 0:
            masked_probs = masked_probs / masked_probs.sum()
        else:
            # 如果没有可用模型，返回None
            return None
        
        # 4. 选择概率最高的模型
        best_model = masked_probs.argmax().item()
        
        return best_model, masked_probs[best_model].item(), H_Y_X
```

## 📊 预期性能

### 当前数据规模（135样本）

```
训练集 (108样本):
  - Top-1: ~25-35%
  - Top-3: ~45-55%
  - Top-5: ~55-65%

验证集 (27样本):
  - Top-1: ~20-30%
  - Top-3: ~40-50%
  - Top-5: ~50-60%
```

### 为什么准确率不高？

1. **数据量小**: 135样本 vs 80类别
2. **类别不平衡**: 29个模型有数据，51个模型无数据
3. **任务难度**: 多类别分类本身就有挑战

### 实际价值

即使Top-1准确率较低，仍然非常有用：

1. **缩小搜索空间**:
   - Top-5准确率~50% → 只需搜索5个候选（6.25%搜索空间）
   - 比随机选择（1.25%）提升4倍

2. **概率先验**:
   - 提供80个模型的概率分布
   - 用于信息增益计算

3. **与规则结合**:
   - 神经网络 + can_apply规则
   - 准确率会显著提升

4. **不确定性度量**:
   - H(Y|X)量化预测置信度
   - 用于三层熵架构的Layer 3

## ❓ 常见问题

### Q1: 训练需要GPU吗？

**A**: 不需要。数据量小（135样本），CPU训练1-2分钟即可。如果有GPU，设置`device='cuda'`可以更快。

### Q2: 如何增加训练数据？

**A**: 
1. 标注更多Conic10K样本的模型序列
2. 更新 `data/train_state_model.json`
3. 重新运行 `python scripts/selector/train.py`

### Q3: 模型文件多大？

**A**: ~60KB（参数量~15,000，fp32存储）

### Q4: 可以并行训练多个模型吗？

**A**: 可以。使用不同的`save_path`保存不同配置的模型，然后对比性能。

### Q5: 训练中断了怎么办？

**A**: 最佳模型会在训练过程中保存到`checkpoints/model_selector.pth`。重新运行会从头开始，但已保存的最佳模型不会丢失。

### Q6: 如何可视化训练过程？

**A**: 训练历史保存在返回的`history`字典中，可以用matplotlib绘制：

```python
import matplotlib.pyplot as plt

model, history = train_model()

plt.figure(figsize=(12, 4))

# 损失曲线
plt.subplot(1, 2, 1)
plt.plot(history['train_loss'], label='Train')
plt.plot(history['val_loss'], label='Val')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.legend()
plt.title('Loss Curve')

# 准确率曲线
plt.subplot(1, 2, 2)
plt.plot(history['val_acc'], label='Top-1')
plt.plot(history['val_top3_acc'], label='Top-3')
plt.plot(history['val_top5_acc'], label='Top-5')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.legend()
plt.title('Accuracy Curve')

plt.savefig('training_curves.png')
```

## 📚 相关文档

- **模块详细文档**: `src/selector/README.md`
- **完成报告**: `dev_logs/module3_training_completion.md`
- **Module 3规格**: `doc/module3_training_data_constructor.md`

---

**最后更新**: 2026-01-20  
**维护者**: EGR Team
