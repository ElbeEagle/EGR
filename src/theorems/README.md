# 定理库 (Theorem Library)

圆锥曲线数学定理的形式化实现

## 🚀 快速开始

```python
from src.theorems.theorem_library import get_theorem_library

# 获取定理库实例
lib = get_theorem_library()

# 查看所有定理
for tid, theorem in lib.theorems.items():
    print(f"{tid}: {theorem.name}")

# 使用定理
state = {
    'curve_type': 'Ellipse',
    'known_params': {'b': 3.0, 'c': 4.0}
}

# 获取可应用的定理
applicable = lib.get_applicable_theorems(state)
print(f"可应用 {len(applicable)} 个定理")

# 应用定理
theorem = lib.get_theorem('T1_ellipse_abc')
if theorem.check_applicable(state):
    new_state = theorem.apply(state)
    print(f"计算得到: a = {new_state['known_params']['a']}")
```

## 📚 已实现定理

### 椭圆相关
- **T1**: 椭圆参数关系 (a² = b² + c²)
- **T4**: 离心率公式 (e = c/a)
- **T5**: 标准方程参数提取
- **T7**: 焦点坐标
- **T9**: 椭圆定义

### 双曲线相关
- **T2**: 双曲线参数关系 (c² = a² + b²)
- **T4**: 离心率公式 (e = c/a)
- **T5**: 标准方程参数提取
- **T6**: 渐近线方程
- **T7**: 焦点坐标
- **T8**: 双曲线定义

### 抛物线相关
- **T3**: 抛物线参数与焦点
- **T10**: 抛物线定义

## 🧪 运行测试

```bash
cd /Users/ebeleagel/Documents/GitHub/EGR
python3 tests/test_theorem_library.py
```

## 📊 定理统计

- **已实现**: 10个基础定理
- **覆盖率**: 约65%的推理步骤
- **测试通过率**: 100%

## 🔧 定理结构

每个定理包含：
- **theorem_id**: 唯一标识符
- **name**: 定理名称
- **formula**: 数学公式
- **precondition**: 前置条件
  - curve_types: 适用曲线类型
  - required_info: 必需信息
- **output**: 输出定义
- **check_applicable**: 检查函数
- **apply**: 应用函数

## 📝 添加新定理

```python
# 1. 定义定理
new_theorem = Theorem(
    theorem_id="T11_new_theorem",
    name="新定理名称",
    description="定理描述",
    formula="数学公式",
    precondition=TheoremPrecondition(
        curve_types=[CurveType.ELLIPSE],
        required_info=['param1', 'param2']
    ),
    output=TheoremOutput(
        output_type='parameter',
        produces=['result']
    ),
    priority=TheoremPriority.BASIC,
    check_applicable=check_function,
    apply=apply_function
)

# 2. 注册到库
lib.register_theorem(new_theorem)
```

## 📖 参考

- [完整定理列表](../../doc/theorem_library_spec.md)
- [模块0完成报告](../../outputs/module0_completion_report.md)
- [项目工作流程](../../doc/phase1_project_workflow.md)

