# Module 0: 模型库开发指南

**版本**: v1.0  
**日期**: 2026-01-15  
**目的**: 定义80个定理模型的标准化实现规范

---

## 📋 概述

本文档定义了圆锥曲线推理系统中**80个定理模型**的标准化实现规范。每个模型代表一个数学定理或推理规则，用于将当前问题状态转换为新状态。

### 核心设计原则

1. **输入输出明确**：每个模型有清晰的输入要求和输出保证
2. **状态转换函数化**：模型 = 纯函数，S_{t+1} = Model(S_t)
3. **信息增量原则**：模型只添加新信息，不删除旧信息
4. **模板化实现**：相似模型使用统一模板，降低复杂度

---

## 🏗️ 模型库架构

### 模型分类体系

根据功能将80个模型分为22个类别：

| 类别 | ID范围 | 数量 | 代表性模型 |
|------|--------|------|-----------|
| 曲线定义 | 0-2 | 3 | 椭圆定义、双曲线定义 |
| 标准方程 | 3-10 | 8 | 各曲线标准方程 |
| 参数关系 | 11-15 | 5 | a²=b²+c²、离心率公式 |
| 焦半径与通径 | 16-20 | 5 | 焦半径公式、通径 |
| 渐近线 | 21-24 | 4 | 渐近线方程 |
| 第二定义与准线 | 25-29 | 5 | 第二定义、准线 |
| 焦点三角形 | 30-32 | 3 | 面积、周长 |
| 抛物线焦点弦 | 33-36 | 4 | 焦点弦性质 |
| 参数方程与切线 | 37-40 | 4 | 切线方程 |
| 韦达定理 | 41-43 | 3 | 根与系数关系 |
| 点差法 | 44-46 | 3 | 中点弦问题 |
| 三角形定理 | 47-49 | 3 | 余弦定理、正弦定理 |
| 弦长公式 | 50-51 | 2 | 弦长计算 |
| 距离与坐标 | 52-55 | 4 | 两点距离、斜率 |
| 三角形面积 | 56-58 | 3 | 面积公式 |
| 向量运算 | 59-62 | 4 | 点积、垂直条件 |
| 不等式 | 63-64 | 2 | 基本不等式 |
| 判别式 | 65-67 | 3 | Δ与交点关系 |
| 特殊定理 | 68-71 | 4 | 中位线、内切圆 |
| 直线方程 | 72-74 | 3 | 点斜式、截距式 |
| 圆相关 | 75-76 | 2 | 圆的方程、切线 |
| 高级技巧 | 77-79 | 3 | 齐次化、换元 |

---

## 📐 模型标准定义格式

每个模型必须包含以下组成部分：

### 1. 模型元信息

```python
class TheoremModel:
    id: int                    # 模型唯一ID (0-79)
    name: str                  # 英文名称，如 "Hyperbola_Asymptote"
    chinese_name: str          # 中文名称，如 "双曲线渐近线"
    description: str           # 功能描述
    formula: str               # 数学公式（LaTeX格式）
    category: str              # 所属类别
```

### 2. 前置条件（Preconditions）

**定义**：应用该模型需要满足的条件，在SymbolicState中检查。

**格式**：
```python
preconditions: List[PreconditionRule]

class PreconditionRule:
    type: str                  # 条件类型
    check_func: callable       # 检查函数
    error_msg: str             # 不满足时的提示
```

**条件类型**：
- `entity_exists`: 某个实体必须存在
- `has_equation_pattern`: 必须有符合某模式的方程
- `param_exists`: 某个参数必须已知
- `relation_exists`: 某个几何关系必须存在

### 3. 输出规格（Output Specification）

**定义**：应用模型后会向SymbolicState添加什么信息。

**格式**：
```python
outputs: List[OutputRule]

class OutputRule:
    target: str                # 目标字段: 'parameters', 'equations', 'relations'
    keys: List[str]            # 添加的键名
    value_type: str            # 值类型: 'numeric', 'symbolic', 'equation'
```

### 4. 状态转换函数（Transform Function）

**签名**：
```python
def transform_model_X(state: SymbolicState) -> SymbolicState:
    """
    模型X的状态转换函数
    
    Args:
        state: 当前SymbolicState（会被修改）
    
    Returns:
        修改后的SymbolicState（同一个对象）
    
    注意：不要创建新对象，直接修改传入的state
    """
```

---

## 🔧 模型实现规范

### 通用实现模板

所有模型遵循以下统一模板：

```python
def _transform_model_X(self, state: SymbolicState):
    """
    模型X：<模型中文名>
    
    前置条件：
      - <条件1>
      - <条件2>
    
    输入：
      - <从state中提取什么>
    
    输出：
      - parameters: <添加哪些键>
      - equations: <添加什么方程>
      - geometric_relations: <添加什么关系>
    
    示例：
      输入: <具体例子>
      输出: <具体结果>
    """
    # ===== 步骤1: 检查前置条件 =====
    if not self._check_precondition_X(state):
        return  # 不满足条件，不做任何修改
    
    # ===== 步骤2: 提取输入信息 =====
    input_1 = self._extract_input_1(state)
    input_2 = self._extract_input_2(state)
    
    # ===== 步骤3: 执行计算 =====
    output = self._compute_output(input_1, input_2)
    
    # ===== 步骤4: 更新状态（增量添加）=====
    # 4.1 添加参数
    state.parameters['new_param'] = output
    
    # 4.2 添加方程（如果有）
    state.equations.append(f"Expression(...) = {output}")
    
    # 4.3 添加几何关系
    state.geometric_relations.append(f"new_param = {output}")
    
    # ===== 步骤5: 添加元信息（可选）=====
    state.applied_models.append(self.id)  # 记录应用了哪个模型
```

### 关键规范

#### ✅ 必须遵守的原则

1. **只增不减**：只能向state添加信息，不能删除或修改已有信息
2. **幂等性**：重复应用同一模型不应产生错误
3. **无副作用**：不依赖外部状态，只操作传入的state参数
4. **容错处理**：输入不满足条件时安静返回，不抛异常

#### ❌ 禁止的操作

1. 删除 `state.parameters` 中的键
2. 修改已有参数的值（除非明确是求精确值）
3. 清空列表字段
4. 依赖全局变量

### 符号计算规范

对于参数值的表示：

```python
# ✅ 推荐：保持符号形式
state.parameters['c'] = "sqrt(a^2 + b^2)"

# ✅ 推荐：数值结果
state.parameters['a'] = 2

# ✅ 推荐：混合表达式
state.parameters['e'] = "sqrt(2)*a/a"  # 可简化为 "sqrt(2)"

# ⚠️ 注意：避免Python对象
# 不要直接用 sympy.Symbol 对象，用字符串表示
```

**简化原则**：
- 优先保持符号形式，便于后续推理
- 能化简的尽量化简（如 `a/a = 1`）
- 数值结果优于符号（如能算出 `a=2`，不要只写 `a^2=4`）

---

## 📚 80个模型详细规格

### 类别1：曲线定义模型 (ID 0-2)

#### Model 0: Ellipse_Definition

**中文名**：椭圆定义

**公式**：$|PF_1| + |PF_2| = 2a$

**前置条件**：
```python
preconditions = [
    EntityExists('Ellipse'),
    EntityExists('Point', name='P'),
    RelationExists('Focus'),  # 必须有焦点信息
]
```

**输入**：
- `entities['G']`: Ellipse类型
- `entities['P']`: Point类型，在椭圆上
- 焦点 F1, F2

**输出**：
```python
outputs = {
    'geometric_relations': [
        "Distance(P, F1) + Distance(P, F2) = 2*a"
    ]
}
```

**实现**：
```python
def _transform_ellipse_definition(self, state: SymbolicState):
    # 查找椭圆实体
    ellipse = None
    for name, type_ in state.entities.items():
        if type_ == 'Ellipse':
            ellipse = name
            break
    
    if not ellipse:
        return
    
    # 添加定义关系
    state.geometric_relations.append(
        f"Distance(P, F1) + Distance(P, F2) = 2*a"
    )
```

**应用场景**：
- 题目给出椭圆上的点P和焦点
- 需要建立距离关系来求解

---

#### Model 1: Hyperbola_Definition

**中文名**：双曲线定义

**公式**：$||PF_1| - |PF_2|| = 2a$

**前置条件**：
```python
preconditions = [
    EntityExists('Hyperbola'),
    EntityExists('Point', name='P'),
    RelationExists('Focus'),
]
```

**输出**：
```python
outputs = {
    'geometric_relations': [
        "Abs(Distance(P, F1) - Distance(P, F2)) = 2*a"
    ]
}
```

---

#### Model 2: Parabola_Definition

**中文名**：抛物线定义

**公式**：$|PF| = d$（到准线距离）

**前置条件**：
```python
preconditions = [
    EntityExists('Parabola'),
    EntityExists('Point', name='P'),
    RelationExists('Focus'),
]
```

**输出**：
```python
outputs = {
    'geometric_relations': [
        "Distance(P, Focus) = Distance(P, Directrix)"
    ]
}
```

---

### 类别2：标准方程模型 (ID 3-10)

#### Model 3: Ellipse_Equation_Standard_X

**中文名**：椭圆标准方程（焦点在x轴）

**公式**：$\frac{x^2}{a^2} + \frac{y^2}{b^2} = 1$，其中 $a > b$

**前置条件**：
```python
preconditions = [
    EntityExists('Ellipse'),
    HasEquationPattern(r'x\^2/(\w+)\s*\+\s*y\^2/(\w+)\s*=\s*1'),
]
```

**输入**：
- 方程形式：`x^2/A + y^2/B = 1`
- 需要满足：A > B（焦点在x轴）

**输出**：
```python
outputs = {
    'parameters': {
        'a^2': 'A的值',
        'b^2': 'B的值',
        'a': 'sqrt(A)',
        'b': 'sqrt(B)'
    },
    'geometric_relations': [
        'a^2 = A',
        'b^2 = B',
        '焦点在x轴'
    ]
}
```

**实现**：
```python
def _transform_ellipse_standard_x(self, state: SymbolicState):
    # 从方程中提取参数
    for eq in state.equations:
        if 'x^2' in eq and 'y^2' in eq and '=' in eq:
            # 匹配模式 x^2/A + y^2/B = 1
            match = re.search(
                r'x\^2/([^\s\+]+).*?y\^2/([^\s=]+)',
                eq
            )
            if match:
                a_squared_str = match.group(1)
                b_squared_str = match.group(2)
                
                # 添加参数
                state.parameters['a^2'] = a_squared_str
                state.parameters['b^2'] = b_squared_str
                
                # 尝试计算具体值
                try:
                    a_sq_val = eval(a_squared_str)
                    state.parameters['a'] = f"sqrt({a_sq_val})"
                    # 如果是完全平方数，进一步简化
                    if int(a_sq_val**0.5)**2 == a_sq_val:
                        state.parameters['a'] = str(int(a_sq_val**0.5))
                except:
                    state.parameters['a'] = f"sqrt({a_squared_str})"
                
                # 同理处理b
                try:
                    b_sq_val = eval(b_squared_str)
                    state.parameters['b'] = f"sqrt({b_sq_val})"
                    if int(b_sq_val**0.5)**2 == b_sq_val:
                        state.parameters['b'] = str(int(b_sq_val**0.5))
                except:
                    state.parameters['b'] = f"sqrt({b_squared_str})"
                
                # 添加关系
                state.geometric_relations.append(f"a^2 = {a_squared_str}")
                state.geometric_relations.append(f"b^2 = {b_squared_str}")
                state.geometric_relations.append("焦点在x轴")
                
                break
```

**应用场景**：
- 题目给出椭圆标准方程
- 需要提取参数a, b用于后续计算

---

#### Model 5: Hyperbola_Equation_Standard_X

**中文名**：双曲线标准方程（焦点在x轴）

**公式**：$\frac{x^2}{a^2} - \frac{y^2}{b^2} = 1$

**前置条件**：
```python
preconditions = [
    EntityExists('Hyperbola'),
    HasEquationPattern(r'x\^2/(\w+)\s*-\s*y\^2/(\w+)\s*=\s*1'),
]
```

**输入**：
- 方程形式：`x^2/A - y^2/B = 1`

**输出**：
```python
outputs = {
    'parameters': {
        'a^2': 'A',
        'b^2': 'B',
        'a': 'sqrt(A)',
        'b': 'sqrt(B)'
    },
    'geometric_relations': [
        'a^2 = A',
        'b^2 = B',
        '焦点在x轴'
    ]
}
```

**实现**：类似Model 3，但匹配减号

---

### 类别3：参数关系模型 (ID 11-15)

#### Model 11: Ellipse_Parameter_Relation

**中文名**：椭圆参数关系

**公式**：$a^2 = b^2 + c^2$

**前置条件**：
```python
preconditions = [
    EntityExists('Ellipse'),
    # a, b, c 中至少有两个已知
    Or([
        And([ParamExists('a'), ParamExists('b')]),
        And([ParamExists('a'), ParamExists('c')]),
        And([ParamExists('b'), ParamExists('c')]),
    ])
]
```

**输入**：
- `parameters['a']`, `parameters['b']`, `parameters['c']` 中的任意两个

**输出**：
```python
# 根据已知参数，计算缺失的参数
outputs = {
    'parameters': {
        # 三选一
        'c': 'sqrt(a^2 - b^2)',  # 若已知a, b
        'b': 'sqrt(a^2 - c^2)',  # 若已知a, c
        'a': 'sqrt(b^2 + c^2)',  # 若已知b, c
    },
    'geometric_relations': [
        'a^2 = b^2 + c^2'
    ]
}
```

**实现**：
```python
def _transform_ellipse_parameter_relation(self, state: SymbolicState):
    params = state.parameters
    
    # 情况1: 已知a和b，求c
    if 'a' in params and 'b' in params:
        a_val = params['a']
        b_val = params['b']
        
        # 符号计算
        params['c'] = f"sqrt({a_val}^2 - {b_val}^2)"
        
        # 尝试数值简化
        try:
            a_num = eval(a_val)
            b_num = eval(b_val)
            c_num = (a_num**2 - b_num**2)**0.5
            if c_num == int(c_num):
                params['c'] = str(int(c_num))
            else:
                params['c'] = f"sqrt({int(a_num**2 - b_num**2)})"
        except:
            pass
        
        state.geometric_relations.append(
            f"c = sqrt({a_val}^2 - {b_val}^2)"
        )
    
    # 情况2: 已知a和c，求b
    elif 'a' in params and 'c' in params:
        a_val = params['a']
        c_val = params['c']
        params['b'] = f"sqrt({a_val}^2 - {c_val}^2)"
        state.geometric_relations.append(
            f"b = sqrt({a_val}^2 - {c_val}^2)"
        )
    
    # 情况3: 已知b和c，求a
    elif 'b' in params and 'c' in params:
        b_val = params['b']
        c_val = params['c']
        params['a'] = f"sqrt({b_val}^2 + {c_val}^2)"
        state.geometric_relations.append(
            f"a = sqrt({b_val}^2 + {c_val}^2)"
        )
```

---

#### Model 12: Hyperbola_Parameter_Relation

**中文名**：双曲线参数关系

**公式**：$c^2 = a^2 + b^2$

**注意**：与椭圆不同！双曲线中c最大。

**实现**：类似Model 11，但公式改为 $c^2 = a^2 + b^2$

---

#### Model 13: Eccentricity_Formula

**中文名**：离心率公式

**公式**：$e = \frac{c}{a}$

**前置条件**：
```python
preconditions = [
    ParamExists('c'),
    ParamExists('a'),
]
```

**输入**：
- `parameters['c']`
- `parameters['a']`

**输出**：
```python
outputs = {
    'parameters': {
        'e': 'c/a'
    },
    'geometric_relations': [
        'e = c/a'
    ]
}
```

**实现**：
```python
def _transform_eccentricity_formula(self, state: SymbolicState):
    if 'c' not in state.parameters or 'a' not in state.parameters:
        return
    
    c_val = state.parameters['c']
    a_val = state.parameters['a']
    
    # 符号形式
    state.parameters['e'] = f"{c_val}/{a_val}"
    
    # 尝试数值计算
    try:
        c_num = eval(c_val)
        a_num = eval(a_val)
        e_num = c_num / a_num
        
        # 常见离心率值的简化
        if abs(e_num - 0.5) < 1e-6:
            state.parameters['e'] = "1/2"
        elif abs(e_num - 2**0.5) < 1e-6:
            state.parameters['e'] = "sqrt(2)"
        elif abs(e_num - 3**0.5 / 2) < 1e-6:
            state.parameters['e'] = "sqrt(3)/2"
        else:
            state.parameters['e'] = str(e_num)
    except:
        pass
    
    state.geometric_relations.append(f"e = {c_val}/{a_val}")
```

---

### 类别5：渐近线模型 (ID 21-24)

#### Model 21: Hyperbola_Asymptote

**中文名**：双曲线渐近线

**公式**：$y = \pm \frac{b}{a}x$

**前置条件**：
```python
preconditions = [
    EntityExists('Hyperbola'),
    ParamExists('a'),
    ParamExists('b'),
]
```

**输入**：
- `parameters['a']`
- `parameters['b']`

**输出**：
```python
outputs = {
    'equations': [
        'Expression(Asymptote(G)) = (y = pm*(b/a)*x)'
    ],
    'geometric_relations': [
        '渐近线: y = ±(b/a)x'
    ]
}
```

**实现**：
```python
def _transform_hyperbola_asymptote(self, state: SymbolicState):
    if 'a' not in state.parameters or 'b' not in state.parameters:
        return
    
    a_val = state.parameters['a']
    b_val = state.parameters['b']
    
    # 添加渐近线方程
    asymptote_eq = f"y = pm*({b_val}/{a_val})*x"
    state.equations.append(
        f"Expression(Asymptote(G)) = ({asymptote_eq})"
    )
    
    state.geometric_relations.append(
        f"渐近线: y = ±({b_val}/{a_val})x"
    )
```

---

### 类别10：韦达定理 (ID 41-43)

#### Model 41: Vieta_Theorem

**中文名**：韦达定理（根与系数关系）

**公式**：对于 $Ax^2 + Bx + C = 0$
- $x_1 + x_2 = -\frac{B}{A}$
- $x_1 \cdot x_2 = \frac{C}{A}$

**前置条件**：
```python
preconditions = [
    HasEquationPattern(r'(\w+)\*x\^2\s*\+\s*(\w+)\*x\s*\+\s*(\w+)\s*=\s*0')
]
```

**输入**：
- 二次方程：`A*x^2 + B*x + C = 0`

**输出**：
```python
outputs = {
    'parameters': {
        'x1_plus_x2': '-B/A',
        'x1_times_x2': 'C/A'
    },
    'geometric_relations': [
        'x1 + x2 = -B/A',
        'x1 * x2 = C/A'
    ]
}
```

**实现**：
```python
def _transform_vieta_theorem(self, state: SymbolicState):
    # 查找二次方程
    for eq in state.equations:
        # 匹配形如 A*x^2 + B*x + C = 0
        match = re.match(
            r'([^\*]+)\*x\^2\s*\+\s*([^\*]+)\*x\s*\+\s*([^\s=]+)\s*=\s*0',
            eq
        )
        if match:
            A, B, C = match.groups()
            A, B, C = A.strip(), B.strip(), C.strip()
            
            # 应用韦达定理
            state.parameters['x1_plus_x2'] = f"-({B})/({A})"
            state.parameters['x1_times_x2'] = f"({C})/({A})"
            
            state.geometric_relations.append(f"x1 + x2 = -({B})/({A})")
            state.geometric_relations.append(f"x1 * x2 = ({C})/({A})")
            
            break
```

---

## 🎯 实现优先级

### 第一批（极高频，20个模型）

必须首先实现，覆盖80%的题目：

| ID | 模型名 | 优先级 | 预计工作量 |
|----|--------|-------|-----------|
| 0-2 | 三大定义 | ⭐⭐⭐⭐⭐ | 1小时 |
| 5 | 双曲线标准方程 | ⭐⭐⭐⭐⭐ | 30分钟 |
| 11-13 | 参数关系、离心率 | ⭐⭐⭐⭐⭐ | 1小时 |
| 21 | 渐近线 | ⭐⭐⭐⭐ | 30分钟 |
| 41-43 | 韦达定理 | ⭐⭐⭐⭐⭐ | 1小时 |
| 44 | 点差法 | ⭐⭐⭐⭐ | 1小时 |
| 47 | 余弦定理 | ⭐⭐⭐⭐ | 30分钟 |
| 50-51 | 弦长公式 | ⭐⭐⭐⭐ | 1小时 |
| 17 | 抛物线焦半径 | ⭐⭐⭐ | 30分钟 |
| 53-55 | 距离、斜率 | ⭐⭐⭐ | 1小时 |

**第一批总计**：约8-10小时

### 第二批（中频，30个模型）

实现后覆盖率提升到95%：

| ID范围 | 类别 | 预计工作量 |
|--------|------|-----------|
| 3-4, 6-10 | 其他标准方程 | 2小时 |
| 16, 18-20 | 焦半径、通径 | 2小时 |
| 22-24 | 渐近线相关 | 1小时 |
| 25-29 | 第二定义、准线 | 2小时 |
| 30-32 | 焦点三角形 | 1.5小时 |
| 33-36 | 抛物线焦点弦 | 2小时 |
| 37-40 | 参数方程、切线 | 2小时 |
| 45-46 | 点差法（椭圆、双曲线） | 1小时 |
| 48-49 | 正弦定理、勾股定理 | 1小时 |
| 52, 56-58 | 距离、面积 | 1.5小时 |
| 59-62 | 向量运算 | 2小时 |
| 63-64 | 不等式 | 1小时 |

**第二批总计**：约19小时

### 第三批（低频，30个模型）

完善覆盖率到98%+：

剩余30个模型，预计15小时。

---

## 📝 实现检查清单

每个模型实现后必须检查：

### ✅ 功能检查

- [ ] 前置条件检查正确
- [ ] 输入提取无误
- [ ] 输出格式符合规范
- [ ] 只添加信息，不删除信息
- [ ] 重复应用不出错

### ✅ 代码质量

- [ ] 有详细的docstring
- [ ] 有输入输出示例
- [ ] 变量命名清晰
- [ ] 异常情况有处理
- [ ] 符合PEP 8规范

### ✅ 测试验证

- [ ] 至少3个测试用例
- [ ] 覆盖典型场景
- [ ] 覆盖边界情况
- [ ] 测试通过率100%

---

## 🧪 测试用例格式

每个模型提供标准测试用例：

```python
def test_model_X():
    """测试模型X"""
    
    # 测试用例1：典型场景
    state1 = SymbolicState()
    state1.entities = {'G': 'Hyperbola', 'm': 'Number'}
    state1.equations = ['Expression(G) = (x^2/4 - y^2/m^2 = 1)']
    
    model = theorem_library.get_model(5)
    model.apply(state1)
    
    assert 'a' in state1.parameters
    assert state1.parameters['a'] == '2'
    assert 'b' in state1.parameters
    
    # 测试用例2：边界情况
    state2 = SymbolicState()
    # ... 设置状态 ...
    model.apply(state2)
    # ... 验证结果 ...
    
    # 测试用例3：不满足条件
    state3 = SymbolicState()
    # ... 缺少必要信息 ...
    model.apply(state3)
    # 应该不抛异常，只是不修改state
    assert len(state3.parameters) == 0
```

---

## 🔗 与Module 1的接口

模型库需要与状态构建模块配合：

### 接口约定

```python
# Module 0 提供：
class TheoremLibrary:
    def get_model(self, model_id: int) -> TheoremModel
    def apply_model(self, state: SymbolicState, model_id: int) -> SymbolicState
    def apply_model_sequence(self, state: SymbolicState, model_ids: List[int]) -> List[SymbolicState]

# Module 1 使用：
from src.theorems.theorem_library import TheoremLibrary
from src.state_constructor import StateConstructor

library = TheoremLibrary()
constructor = StateConstructor()

# 构建初始状态
abstract_state, symbolic_state = constructor.construct_from_facts(
    fact_expressions,
    query_expressions
)

# 应用模型
model = library.get_model(5)
model.apply(symbolic_state)

# 重新构建抽象特征
new_abstract = constructor.construct_from_symbolic_state(
    symbolic_state,
    query_expressions,
    reasoning_depth=1
)
```

---

## 📚 参考资料

### 模型定义来源

- `model/conic_model_descriptions.md`：80个模型的详细说明
- `model/conic_model_ids.json`：模型ID映射表

### 对象+操作符定义来源

- `model/object.json`：数据集中涉及的所有对象
- `model/operators.json`：数据集中涉及的所有操作符

### 数据集

- `data/train_with_models_1_100.json`：100个带models标注的样本
- 可以从中提取模型应用的实际案例

---

**最后更新**: 2026-01-15  
**维护者**: EGR Team  
**版本历史**: v1.0 初始版本
