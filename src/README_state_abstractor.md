# 状态抽象器使用指南

将原始的 fact_expressions 转换为结构化状态

---

## 🚀 快速开始

```python
from src.state_abstractor import create_state_abstractor

# 创建抽象器
abstractor = create_state_abstractor()

# 抽象一个问题
facts = "G: Ellipse;Expression(G) = (x^2/4 + y^2/3 = 1)"
query = "Eccentricity(G)"

state = abstractor.abstract(facts, query)

# 查看结果
print(f"曲线类型: {state.curve_type.value}")
print(f"查询类型: {state.query_type.value}")
print(f"已知参数: {state.known_params}")
print(f"完整度: {state.completeness:.2f}")
```

---

## 📊 状态结构

### AbstractState 字段说明

| 字段 | 类型 | 说明 | 示例 |
|------|------|------|------|
| `curve_type` | CurveType | 曲线类型 | Ellipse/Hyperbola/Parabola |
| `query_type` | QueryType | 查询类型 | eccentricity/equation/distance |
| `has_equation` | bool | 是否有方程 | True/False |
| `has_focus` | bool | 是否有焦点 | True/False |
| `known_params` | Dict | 已知参数 | {'a': 2.0, 'b': 1.73} |
| `completeness` | float | 完整度 (0-1) | 0.75 |
| `state_hash` | str | 状态哈希 | "ELL_EQ_AB_ECCENT" |

---

## 🔧 高级用法

### 1. 转换为字典（用于定理库）

```python
state = abstractor.abstract(facts, query)
state_dict = state.to_dict()

# 传递给定理库
from src.theorems.theorem_library import get_theorem_library
lib = get_theorem_library()
applicable_theorems = lib.get_applicable_theorems(state_dict)
```

### 2. 批量处理

```python
import json

with open('Conic10K/conic10k/train.json', 'r') as f:
    data = json.load(f)

states = []
for item in data[:100]:
    state = abstractor.abstract(
        item['fact_expressions'],
        item['query_expressions']
    )
    states.append(state)

print(f"成功处理 {len(states)} 个问题")
```

### 3. 统计分析

```python
from collections import Counter

# 统计曲线类型分布
curve_types = Counter(s.curve_type.value for s in states)
print("曲线类型分布:")
for ctype, count in curve_types.items():
    print(f"  {ctype}: {count}")

# 统计查询类型分布
query_types = Counter(s.query_type.value for s in states)
print("\n查询类型分布:")
for qtype, count in query_types.items():
    print(f"  {qtype}: {count}")
```

---

## 📖 完整示例

### 示例1：椭圆问题

```python
facts = "G: Ellipse;Expression(G) = (x^2/4 + y^2/3 = 1)"
query = "Eccentricity(G)"

state = abstractor.abstract(facts, query)

print(f"""
问题分析:
  曲线: {state.curve_type.value}
  目标: {state.query_type.value}
  
已知信息:
  有方程: {state.has_equation}
  参数: a={state.known_params.get('a', '?')}, 
        b={state.known_params.get('b', '?')}
  
状态评估:
  完整度: {state.completeness:.0%}
  状态ID: {state.state_hash}
""")
```

输出：
```
问题分析:
  曲线: Ellipse
  目标: eccentricity
  
已知信息:
  有方程: True
  参数: a=2.0, b=1.73
  
状态评估:
  完整度: 50%
  状态ID: ELL_EQ_AB_ECCENT
```

### 示例2：双曲线+渐近线

```python
facts = "G: Hyperbola;m: Number;m>0;Expression(G) = (x^2/4 - y^2/m^2 = 1);Expression(OneOf(Asymptote(G))) = (5*x - 2*y = 0)"
query = "m"

state = abstractor.abstract(facts, query)

print(f"""
问题分析:
  曲线: {state.curve_type.value}
  目标: 求参数 {query}
  
已知信息:
  有方程: {state.has_equation}
  有渐近线: {state.has_asymptote}
  约束: {', '.join(state.constraints)}
  
状态评估:
  完整度: {state.completeness:.0%}
""")
```

---

## 🎯 与定理库集成

### 完整求解流程

```python
from src.state_abstractor import create_state_abstractor
from src.theorems.theorem_library import get_theorem_library

# 初始化
abstractor = create_state_abstractor()
lib = get_theorem_library()

# 问题
facts = "G: Ellipse;Expression(G) = (x^2/4 + y^2/3 = 1)"
query = "Eccentricity(G)"

# Step 1: 抽象状态
state = abstractor.abstract(facts, query)
print(f"初始完整度: {state.completeness:.2f}")

# Step 2: 查找可用定理
state_dict = state.to_dict()
applicable = lib.get_applicable_theorems(state_dict)
print(f"可用定理: {[t.name for t in applicable]}")

# Step 3: 应用定理
for theorem in applicable:
    if theorem.check_applicable(state_dict):
        state_dict = theorem.apply(state_dict)
        print(f"应用 {theorem.name}")
        print(f"  新参数: {list(state_dict['known_params'].keys())}")

# Step 4: 提取答案
if 'eccentricity' in state_dict['known_params']:
    print(f"\n答案: e = {state_dict['known_params']['eccentricity']:.4f}")
```

---

## 📊 覆盖范围

### 支持的曲线类型
- ✅ Ellipse (椭圆)
- ✅ Hyperbola (双曲线)
- ✅ Parabola (抛物线)
- ✅ Circle (圆)

### 支持的查询类型
- ✅ eccentricity (离心率)
- ✅ equation (方程)
- ✅ coordinate (坐标)
- ✅ distance (距离)
- ✅ range (范围)
- ✅ length (长度)
- ✅ area (面积)
- ✅ value (参数值)

### 支持的信息提取
- ✅ 方程识别
- ✅ 焦点信息
- ✅ 渐近线信息
- ✅ 参数提取（标准方程）
- ✅ 几何关系识别
- ✅ 约束条件提取

---

## ⚙️ 配置选项

### 自定义参数名称

```python
abstractor = create_state_abstractor()

# 扩展参数集合
abstractor.param_names.update({'r', 'theta', 'phi'})
```

### 获取统计信息

```python
stats = abstractor.get_statistics()
print(f"""
处理统计:
  总数: {stats['total_abstracted']}
  失败: {stats['failed_count']}
  成功率: {stats['success_rate']*100:.1f}%
""")
```

---

## 🐛 调试技巧

### 查看原始表达式

```python
state = abstractor.abstract(facts, query)

# 查看原始输入（用于调试）
print(f"原始Facts: {state.raw_facts}")
print(f"原始Query: {state.raw_query}")
```

### 检查解析结果

```python
state = abstractor.abstract(facts, query)

# 详细检查
print("信息标记:")
print(f"  has_equation: {state.has_equation}")
print(f"  has_focus: {state.has_focus}")
print(f"  has_asymptote: {state.has_asymptote}")

print("\n已知参数:")
for key, value in state.known_params.items():
    print(f"  {key} = {value}")

print(f"\n约束条件: {state.constraints}")
```

---

## 🧪 测试

### 运行单元测试

```bash
cd /Users/ebeleagel/Documents/GitHub/EGR
python3 tests/test_state_abstractor.py
```

### 运行集成测试

```bash
python3 tests/test_integration_state_theorem.py
```

---

## 📚 相关文档

- [完整报告](../../outputs/module1_completion_report.md)
- [定理库文档](theorem_library.md)
- [项目工作流程](../../doc/phase1_project_workflow.md)

---

## 💡 常见问题

### Q: 为什么有些参数是'symbolic'？
A: 表示该参数已声明但没有具体数值，需要通过定理推导获得。

### Q: 完整度是如何计算的？
A: 基于启发式规则：有方程(30%) + 有焦点(20%) + 参数数量(40%) + 查询相关(10%)

### Q: 状态哈希有什么用？
A: 用于快速索引和去重相似的问题状态。

### Q: 覆盖率96%，剩下4%是什么？
A: 主要是一些特殊格式的方程或非标准表达式，可以通过扩展解析规则来支持。

---

**更新时间**: 2026-01-08  
**版本**: v1.0

