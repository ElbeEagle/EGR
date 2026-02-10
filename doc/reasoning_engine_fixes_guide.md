# 推理引擎修复指南

**版本**: v1.1  
**日期**: 2026-02-10

---

## 新增组件

### QueryParser - 查询表达式解析器

将query字符串解析为结构化对象。

```python
from src.reasoning import QueryParser

parser = QueryParser()

# 简单值
parsed = parser.parse("m")
# ParsedQuery(operation='Value', target='m')

# 单层函数
parsed = parser.parse("Eccentricity(G)")
# ParsedQuery(operation='Eccentricity', target='G')

# 嵌套函数
parsed = parser.parse("Length(MajorAxis(G))")
# ParsedQuery(operation='Length', nested_operation='MajorAxis', nested_target='G')
```

### AnswerExtractor - 答案提取器

从SymbolicState中提取query对应的答案。

```python
from src.reasoning import AnswerExtractor

extractor = AnswerExtractor()
answer = extractor.extract(symbolic_state, "Length(MajorAxis(G))")
# answer = 4 (2*a)
```

**支持的查询类型**:

| 查询类型 | 示例 | 提取逻辑 |
|---------|------|---------|
| Value | `"m"` | parameters[m] |
| Eccentricity | `"Eccentricity(G)"` | e=c/a 或直接查找 |
| Length | `"Length(MajorAxis(G))"` | 2a, 2b, 2p |
| Equation | `"Equation(Asymptote(G))"` | 从equations查找 |
| Coordinate | `"Coordinate(A)"` | 从coordinates查找 |
| Distance | `"Distance(A,B)"` | 从geometric_relations查找 |
| Area | `"Area(Triangle)"` | 计算或查找 |
| Angle | `"Angle(F1PF2)"` | 从geometric_relations查找 |

---

## 修改的接口

### ReasoningEngine.__init__()

新增参数:
- `completeness_threshold`: 默认从0.95改为 **0.99**
- `min_steps`: 新增，默认 **1**（至少推理1步）

```python
engine = ReasoningEngine(
    library, selector, constructor,
    completeness_threshold=0.99,  # 提高阈值
    min_steps=1                   # 强制至少推理1步
)
```

### ModelSelector.select()

新增自动排除已应用模型：
```python
model, info = selector.select(
    symbolic_state=symbolic_state,
    abstract_state=abstract_state,
    top_k=10,
    excluded_models=None  # 自动从symbolic_state.applied_models获取
)
```

### TheoremModel.apply()

返回类型从 `None` 改为 `bool`:
```python
def apply(self, state) -> bool:
    """返回True表示成功，False表示失败"""
    try:
        # 模型逻辑...
        state.applied_models.append(self.model_id)
        return True
    except Exception:
        return False
```

推理引擎兼容旧模型（返回None视为True）。

### StateConstructor.update_abstract_state()

新增便利方法:
```python
new_abstract = constructor.update_abstract_state(
    symbolic_state,      # 更新后的符号状态
    old_abstract_state   # 旧的抽象状态（用于获取depth）
)
```
