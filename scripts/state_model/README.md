# State-Model Training Data Generator

Module 3 训练数据生成器

---

## 📁 文件说明

### `generate_train_state_model.py`
**主要功能**: 生成包含完整状态向量的训练数据

**输入**: `data/train_with_models_1_100.json`  
**输出**: `data/train_state_model.json`

**核心流程**:
1. 加载数据集（63个有模型序列的样本）
2. 使用 `StateSequenceBuilder` 构建状态转换序列
3. 提取成功的转换（status='success', step > 0）
4. 保存包含 28维状态向量 的训练数据
5. 输出统计报告和验证结果

### `example_load_training_data.py`
**主要功能**: 演示如何加载和使用训练数据

**用途**: Module 3 训练时的数据加载参考

---

## 📊 输出数据格式

### `data/train_state_model.json` 结构

```json
{
  "total_samples": 52,          // 有效样本数
  "total_transitions": 135,     // 总训练样本数
  "model_usage_statistics": {
    "total_models_used": 29,
    "model_counts": {
      "7": 14,
      "5": 13,
      ...
    }
  },
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
            "has_directrix_info": false,
            "has_vertex_info": false,
            "reasoning_depth": 1
          },
          "state_vector": [0.0, 1.0, 0.0, ..., 0.8, 0.1]  // 28维
        }
      ]
    }
  ]
}
```

---

## 🎯 训练样本格式

每个训练样本是一个 `(state_vector, model_id)` 对：

- **state_vector**: 28维浮点数特征向量
  - [0:5] 曲线类型 one-hot (椭圆/双曲线/抛物线/圆/未知)
  - [5:15] 查询类型 one-hot (离心率/方程/坐标/距离/...)
  - [15:26] 信息特征 (11个布尔特征，归一化)
  - [26:28] 完整度和推理深度

- **model_id**: 整数，范围 [0, 79]，表示应用的模型

---

## 📈 数据统计

### 当前生成结果

```
总样本数: 52
总训练样本数: 135
平均每样本: 2.60 个转换
使用的模型数: 29/80
```

### Top 10 高频模型

| 模型ID | 模型名 | 使用次数 | 占比 |
|--------|--------|---------|------|
| 7 | Parabola_Equation_Standard_Right | 14 | 10.4% |
| 5 | Hyperbola_Equation_Standard_X | 13 | 9.6% |
| 13 | Eccentricity_Formula | 10 | 7.4% |
| 29 | Parabola_Directrix | 8 | 5.9% |
| 3 | Ellipse_Equation_Standard_X | 8 | 5.9% |
| 62 | Vector_Collinear_Condition | 8 | 5.9% |
| 1 | Hyperbola_Definition | 7 | 5.2% |
| 56 | Triangle_Area_Formula | 6 | 4.4% |
| 21 | Hyperbola_Asymptote | 5 | 3.7% |
| 2 | Parabola_Definition | 5 | 3.7% |

---

## 🚀 使用方法

### 1. 生成训练数据

```bash
cd /Users/ebeleagel/Documents/GitHub/EGR
python scripts/state_model/generate_train_state_model.py
```

### 2. 验证数据加载

```bash
python scripts/state_model/example_load_training_data.py
```

### 3. 在 Module 3 中使用

```python
import json

# 加载数据
with open('data/train_state_model.json') as f:
    data = json.load(f)

# 提取训练样本
X = []  # 特征
y = []  # 标签

for sample in data['sample_results']:
    for trans in sample['transitions']:
        X.append(trans['state_vector'])  # 28维
        y.append(trans['model_id'])      # 0-79

# X: [135, 28]
# y: [135]
```

---

## ✅ 数据质量保证

生成脚本包含自动验证：

- ✅ 有训练样本 (135个)
- ✅ 状态向量维度=28且一致
- ✅ 模型ID范围有效 [0, 79]
- ✅ 完整度范围有效 [0, 1]

---

## 📝 注意事项

1. **状态向量维度**: 28维，不是30维（见 `AbstractState.to_vector()`）
2. **只包含成功转换**: `status='success'` 且 `step > 0`
3. **类别不平衡**: 高频模型占比较大，训练时可能需要加权
4. **数据规模**: 135个样本相对较小，适合初步训练

---

## 🔗 相关文档

- `doc/module3_training_data_constructor.md` - Module 3 设计文档
- `dev_logs/stage2.3_integration_report.md` - 集成测试报告
- `src/state/abstract_state.py` - AbstractState 定义

---

**生成时间**: 2026-01-19  
**维护者**: EGR Team
