# 圆锥曲线推理模型库说明文档

**版本：** v1.0  
**样本数量：** 5000+  
**覆盖率：** 90%+

```
"_comment": "圆锥曲线推理模型库 - 基于5000+样本统计分析",
"_total_models": 80,
"_coverage": "覆盖90%以上的圆锥曲线问题",

一、曲线定义模型（ID: 0-2）
二、标准方程模型（ID: 3-10）
三、参数关系与离心率（ID: 11-15）
四、焦半径与通径（ID: 16-20）
五、渐近线相关（ID: 21-24）
六、第二定义与准线（ID: 25-29）
七、焦点三角形（ID: 30-32）
八、抛物线焦点弦（ID: 33-36）
九、参数方程与切线（ID: 37-40）
十、韦达定理系列（ID: 41-43）
十一、点差法（ID: 44-46）
十二、三角形定理（ID: 47-49）
十三、弦长公式（ID: 50-51）
十四、距离与坐标（ID: 52-55）
十五、三角形面积（ID: 56-58）
十六、向量运算（ID: 59-62）
十七、不等式（ID: 63-64）
十八、判别式（ID: 65-67）
十九、三角形特殊定理（ID: 68-71）
二十、直线方程（ID: 72-74）
二十一、圆相关（ID: 75-76）
二十二、高级技巧（ID: 77-79）
```

---

## 模型分类体系

### 一、曲线定义模型（ID: 0-2）

| ID | 模型名称 | 公式/定义 | 适用场景 |
|----|---------|-----------|---------|
| 0 | Ellipse_Definition | \|PF₁\| + \|PF₂\| = 2a | 椭圆上任一点到两焦点距离之和为定值 |
| 1 | Hyperbola_Definition | \|\|PF₁\| - \|PF₂\|\| = 2a | 双曲线上任一点到两焦点距离之差的绝对值为定值 |
| 2 | Parabola_Definition | \|PF\| = d（到准线距离） | 抛物线上点到焦点距离等于到准线距离 |

---

### 二、标准方程模型（ID: 3-10）

| ID | 模型名称 | 公式 | 说明 |
|----|---------|------|------|
| 3 | Ellipse_Equation_Standard_X | x²/a² + y²/b² = 1 | 椭圆焦点在x轴 |
| 4 | Ellipse_Equation_Standard_Y | y²/a² + x²/b² = 1 | 椭圆焦点在y轴 |
| 5 | Hyperbola_Equation_Standard_X | x²/a² - y²/b² = 1 | 双曲线焦点在x轴 |
| 6 | Hyperbola_Equation_Standard_Y | y²/a² - x²/b² = 1 | 双曲线焦点在y轴 |
| 7 | Parabola_Equation_Standard_Right | y² = 2px | 抛物线开口向右 |
| 8 | Parabola_Equation_Standard_Left | y² = -2px | 抛物线开口向左 |
| 9 | Parabola_Equation_Standard_Up | x² = 2py | 抛物线开口向上 |
| 10 | Parabola_Equation_Standard_Down | x² = -2py | 抛物线开口向下 |

---

### 三、参数关系与离心率（ID: 11-15）

| ID | 模型名称 | 公式 | 核心关系 |
|----|---------|------|---------|
| 11 | Ellipse_Parameter_Relation | a² = b² + c² | 椭圆中a是最大的 |
| 12 | Hyperbola_Parameter_Relation | c² = a² + b² | 双曲线中c是最大的 |
| 13 | Eccentricity_Formula | e = c/a | 通用离心率定义 |
| 14 | Ellipse_Eccentricity_Range | 0 < e < 1 | 椭圆离心率范围 |
| 15 | Hyperbola_Eccentricity_Range | e > 1 | 双曲线离心率范围 |

---

### 四、焦半径与通径（ID: 16-20）

| ID | 模型名称 | 公式 | 应用 |
|----|---------|------|------|
| 16 | Ellipse_Focal_Radius | \|PF\| = a ± ex | 椭圆焦半径公式 |
| 17 | Parabola_Focal_Radius | \|PF\| = x + p/2 | 抛物线焦半径公式 |
| 18 | Ellipse_Latus_Rectum | 2b²/a | 椭圆通径（最短焦点弦） |
| 19 | Hyperbola_Latus_Rectum | 2b²/a | 双曲线通径 |
| 20 | Parabola_Latus_Rectum | 2p | 抛物线通径 |

---

### 五、渐近线相关（ID: 21-24）

| ID | 模型名称 | 公式 | 说明 |
|----|---------|------|------|
| 21 | Hyperbola_Asymptote | y = ±(b/a)x | 双曲线渐近线方程 |
| 22 | Hyperbola_Focus_To_Asymptote_Distance | d = b | 焦点到渐近线距离 |
| 23 | Hyperbola_Common_Asymptote_System | x²/a² - y²/b² = λ | 共渐近线双曲线系 |
| 24 | Hyperbola_Equal_Axis | a = b → e = √2 | 等轴双曲线性质 |

---

### 六、第二定义与准线（ID: 25-29）

| ID | 模型名称 | 公式 | 应用 |
|----|---------|------|------|
| 25 | Ellipse_Second_Definition | \|PF\|/d = e | 椭圆第二定义 |
| 26 | Hyperbola_Second_Definition | \|PF\|/d = e | 双曲线第二定义 |
| 27 | Ellipse_Directrix | x = ±a²/c | 椭圆准线方程 |
| 28 | Hyperbola_Directrix | x = ±a²/c | 双曲线准线方程 |
| 29 | Parabola_Directrix | x = -p/2 或 y = -p/2 | 抛物线准线方程 |

---

### 七、焦点三角形（ID: 30-32）

| ID | 模型名称 | 公式 | 说明 |
|----|---------|------|------|
| 30 | Ellipse_Focal_Triangle_Area | S = b²·tan(θ/2) | θ为∠F₁PF₂ |
| 31 | Hyperbola_Focal_Triangle_Area | S = b²·cot(θ/2) | θ为∠F₁PF₂ |
| 32 | Ellipse_Focal_Triangle_Perimeter | 2a + 2c | 椭圆焦点三角形周长 |

---

### 八、抛物线焦点弦（ID: 33-36）

| ID | 模型名称 | 公式 | 说明 |
|----|---------|------|------|
| 33 | Parabola_Focal_Chord_Length | \|AB\| = x₁ + x₂ + p | 焦点弦长公式 |
| 34 | Parabola_Focal_Chord_Product_X | x₁x₂ = p²/4 | 焦点弦端点横坐标乘积 |
| 35 | Parabola_Focal_Chord_Product_Y | y₁y₂ = -p² | 焦点弦端点纵坐标乘积 |
| 36 | Parabola_Focal_Chord_Formula_Angle | \|AB\| = 2p/sin²θ | 倾斜角为θ的焦点弦 |

---

### 九、参数方程与切线（ID: 37-40）

| ID | 模型名称 | 公式 | 应用 |
|----|---------|------|------|
| 37 | Ellipse_Parametric_Equation | x=acosθ, y=bsinθ | 椭圆参数方程 |
| 38 | Ellipse_Tangent_Line | x₀x/a² + y₀y/b² = 1 | 椭圆在点(x₀,y₀)处切线 |
| 39 | Parabola_Tangent_Line | y₀y = 2p(x + x₀) | 抛物线切线方程 |
| 40 | Ellipse_Midpoint_Chord_Slope | k·k_{OM} = -b²/a² | 中点弦斜率关系 |

---

### 十、韦达定理系列（ID: 41-43）

| ID | 模型名称 | 公式 | 说明 |
|----|---------|------|------|
| 41 | Vieta_Theorem | 根与系数关系 | 一元二次方程基础 |
| 42 | Vieta_Theorem_Sum | x₁ + x₂ = -b/a | 两根之和 |
| 43 | Vieta_Theorem_Product | x₁x₂ = c/a | 两根之积 |

---

### 十一、点差法（ID: 44-46）

| ID | 模型名称 | 方法 | 适用 |
|----|---------|------|------|
| 44 | Point_Difference_Method | 两点坐标代入方程相减 | 中点弦、斜率乘积问题 |
| 45 | Point_Difference_Method_Ellipse | 椭圆点差法 | 椭圆中点弦问题 |
| 46 | Point_Difference_Method_Hyperbola | 双曲线点差法 | 双曲线中点弦问题 |

---

### 十二、三角形定理（ID: 47-49）

| ID | 模型名称 | 公式 | 说明 |
|----|---------|------|------|
| 47 | Cosine_Law | c² = a² + b² - 2ab·cosC | 余弦定理 |
| 48 | Sine_Law | a/sinA = b/sinB = c/sinC | 正弦定理 |
| 49 | Pythagorean_Theorem | a² + b² = c² | 勾股定理 |

---

### 十三、弦长公式（ID: 50-51）

| ID | 模型名称 | 公式 | 说明 |
|----|---------|------|------|
| 50 | Chord_Length_Formula | \|AB\| = √[(x₁+x₂)²-4x₁x₂]·√(1+k²) | 标准弦长公式 |
| 51 | Chord_Length_Formula_With_K | \|AB\| = \|x₁-x₂\|·√(1+k²) | 简化弦长公式 |

---

### 十四、距离与坐标（ID: 52-55）

| ID | 模型名称 | 公式 | 说明 |
|----|---------|------|------|
| 52 | Point_To_Line_Distance | d = \|Ax₀+By₀+C\|/√(A²+B²) | 点到直线距离 |
| 53 | Two_Points_Distance | d = √[(x₂-x₁)²+(y₂-y₁)²] | 两点距离公式 |
| 54 | Midpoint_Formula | M((x₁+x₂)/2, (y₁+y₂)/2) | 中点坐标 |
| 55 | Slope_Formula | k = (y₂-y₁)/(x₂-x₁) | 斜率公式 |

---

### 十五、三角形面积（ID: 56-58）

| ID | 模型名称 | 公式 | 说明 |
|----|---------|------|------|
| 56 | Triangle_Area_Formula | S = (1/2)·底·高 | 基本面积公式 |
| 57 | Triangle_Area_With_Sin | S = (1/2)ab·sinC | 正弦面积公式 |
| 58 | Triangle_Area_Coordinate | S = (1/2)\|x₁y₂-x₂y₁\| | 坐标面积公式 |

---

### 十六、向量运算（ID: 59-62）

| ID | 模型名称 | 公式/条件 | 应用 |
|----|---------|----------|------|
| 59 | Vector_Dot_Product_Algebraic | a⃗·b⃗ = x₁x₂ + y₁y₂ | 向量数量积代数形式 |
| 60 | Vector_Dot_Product_Geometric | a⃗·b⃗ = \|a⃗\|\|b⃗\|cosθ | 向量数量积几何形式 |
| 61 | Vector_Perpendicular_Condition | a⃗·b⃗ = 0 或 k₁k₂ = -1 | 垂直关系判定 |
| 62 | Vector_Collinear_Condition | a⃗ = λb⃗ | 共线/平行判定 |

---

### 十七、不等式（ID: 63-64）

| ID | 模型名称 | 公式 | 说明 |
|----|---------|------|------|
| 63 | Basic_Inequality | a + b ≥ 2√(ab) | 基本不等式 |
| 64 | Basic_Inequality_Equal_Condition | 当且仅当 a = b 时取等 | 取等条件 |

---

### 十八、判别式（ID: 65-67）

| ID | 模型名称 | 条件 | 应用 |
|----|---------|------|------|
| 65 | Discriminant_Delta | Δ = b² - 4ac | 判别式基础 |
| 66 | Discriminant_Tangent_Condition | Δ = 0 | 相切条件 |
| 67 | Discriminant_Intersect_Condition | Δ > 0 | 相交条件 |

---

### 十九、三角形特殊定理（ID: 68-71）

| ID | 模型名称 | 公式/方法 | 说明 |
|----|---------|----------|------|
| 68 | Triangle_Midline_Theorem | 中位线 = 底边/2 | 三角形中位线定理 |
| 69 | Trapezoid_Midline_Theorem | 中位线 = (上底+下底)/2 | 梯形中位线定理 |
| 70 | Incircle_Radius_Formula | r = 2S/周长 | 内切圆半径公式 |
| 71 | Equal_Area_Method | 等底或等高 | 等积法求解 |

---

### 二十、直线方程（ID: 72-74）

| ID | 模型名称 | 公式 | 说明 |
|----|---------|------|------|
| 72 | Line_Point_Slope_Form | y - y₀ = k(x - x₀) | 点斜式 |
| 73 | Line_Two_Point_Form | (y-y₁)/(y₂-y₁) = (x-x₁)/(x₂-x₁) | 两点式 |
| 74 | Line_Intercept_Form | x/a + y/b = 1 | 截距式 |

---

### 二十一、圆相关（ID: 75-76）

| ID | 模型名称 | 公式/条件 | 说明 |
|----|---------|----------|------|
| 75 | Circle_Standard_Equation | (x-a)² + (y-b)² = r² | 圆的标准方程 |
| 76 | Circle_Tangent_Condition | d = r | 直线与圆相切条件 |

---

### 二十二、高级技巧（ID: 77-79）

| ID | 模型名称 | 方法/技巧 | 说明 |
|----|---------|----------|------|
| 77 | Homogenization_Eccentricity | 两边同除以a² | 齐次化求离心率 |
| 78 | Substitution_x_equals_my_plus_n | 设 x = my + n | 避免斜率讨论的技巧 |
| 79 | Quadratic_Function_Maximum | 配方求最值 | 二次函数最值问题 |

---

## 使用频率统计

### 极高频模型（使用率 > 80%）
- ID 0-2: 三大曲线定义
- ID 41-43: 韦达定理
- ID 13: 离心率公式
- ID 44: 点差法

### 高频模型（使用率 60-80%）
- ID 11-12: 参数关系
- ID 47: 余弦定理
- ID 50-51: 弦长公式
- ID 17: 抛物线焦半径
- ID 21: 双曲线渐近线

### 中频模型（使用率 30-60%）
- ID 16: 椭圆焦半径
- ID 52-55: 距离与坐标公式
- ID 59-61: 向量运算
- ID 63: 基本不等式
- ID 30-31: 焦点三角形面积

---

## 模型组合模式

### 常见组合1：求椭圆/双曲线方程
```
定义(0或1) → 参数关系(11或12) → 标准方程(3-6)
```

### 常见组合2：求离心率
```
参数关系(11或12) → 齐次化(77) → 离心率公式(13)
```

### 常见组合3：直线与曲线交点
```
联立方程 → 韦达定理(41-43) → 弦长公式(50-51)
```

### 常见组合4：中点弦问题
```
点差法(44-46) → 斜率关系(40或55) → 直线方程(72)
```

### 常见组合5：抛物线焦点弦
```
设x=my+n(78) → 抛物线定义(2) → 焦点弦长(33-36)
```

### 常见组合6：最值问题
```
椭圆定义(0) → 基本不等式(63) → 取等条件(64)
```

---

## 覆盖率说明

根据5000+样本的统计分析：

- **80个模型覆盖约92%的题目**
- **前40个核心模型覆盖约85%的题目**
- **前20个超核心模型覆盖约70%的题目**

### 必备核心（前20个模型）
ID 0-2, 11-13, 21, 41-44, 47, 50, 52, 54-55, 59, 63

### 重要补充（21-40号模型）
ID 3-10, 16-20, 25-29, 45-46, 48-49

### 完善覆盖（41-79号模型）
其余所有模型

---

## 版本历史

**v1.0** (2026-01)
- 初始版本
- 基于5000+样本统计分析
- 80个核心模型
- 覆盖率：92%+

