# Selector训练脚本

## 脚本说明

### train_selector.py - 训练脚本
完整训练MaxEntropyClassifier模型选择器

**用法**:
```bash
python scripts/selector/train_selector.py
```

**功能**:
- 加载训练数据（135样本）
- 训练神经网络（100 epochs，Early stopping）
- 评估Top-1/3/5准确率
- 保存最佳模型到 `checkpoints/model_selector.pth`
- 生成训练报告到 `outputs/selector/training_metrics.json`

**预计用时**: 1-2分钟（CPU），30-60秒（MPS/GPU）

---

### test_selector.py - 功能测试脚本
测试模型选择器的所有功能

**用法**:
```bash
python scripts/selector/test_selector.py
```

**测试内容**:
1. 数据加载测试
2. 模型创建测试
3. 前向传播测试
4. 小规模训练测试（5 epochs）

**推荐**: 在完整训练前先运行此脚本验证环境

---

## 快速开始

```bash
# 1. 安装依赖
pip install torch numpy

# 2. 测试功能（推荐）
python scripts/selector/test_selector.py

# 3. 完整训练
python scripts/selector/train_selector.py
```

---

**相关文档**: 
- `src/selector/README.md` - 详细技术文档
- `src/selector/USAGE.md` - 使用指南
