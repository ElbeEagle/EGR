# Module 4 阶段2: 回溯机制与批量测试

**版本**: v1.0  
**日期**: 2026-02-10

---

## 新增功能

### 1. 回溯机制

模型apply失败时不再终止推理，而是自动重试。

```python
engine = ReasoningEngine(
    ...,
    max_retries_per_step=3  # 每步最多重试3次
)
```

**行为**:
- apply返回False → 排除该模型，从Top-K中选下一个
- 连续2步都无法选到可用模型 → 提前终止
- 所有重试失败 → 跳过该步，继续下一步

### 2. 答案比较器

数值化比较预测答案和标准答案。

```python
from src.reasoning.answer_comparator import compare_answers

compare_answers(predicted="sqrt(3)/2", expected="0.866")  # True
compare_answers(predicted=4, expected="4")                 # True
compare_answers(predicted="1/2", expected="0.5")           # True
```

**支持格式**: 整数、小数、分数、sqrt、pm、基本运算

### 3. 尽力提取答案

即使completeness未达标，只要应用了模型就尝试提取答案。

### 4. 批量测试脚本

```bash
python scripts/reasoning/batch_test.py --num 200 --seed 42
```

**输出**: `outputs/reasoning/batch_test_report.json`

---

## 性能基准 (200样本)

| 指标 | 值 |
|------|------|
| 推理成功率 | 73.5% |
| 答案正确率 | 2.5% |
| 平均步数 | 8.2 |
| 速度 | 965题/秒 |

**按曲线**: Ellipse 69% / Hyperbola 79% / Parabola 82%  
**按查询**: Value 90% / Range 88% / Distance 86% / Eccentricity 78%

---

## 已知瓶颈

1. **答案提取**: 92/142个错误是因为参数含变量字母（符号推理）
2. **模型覆盖**: 40/80模型已实现，约50%题涉及未实现模型
3. **推理路径**: 35个数值可算但值不对（模型选择/应用链路错误）
