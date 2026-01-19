# 圆锥曲线定理模型详细参考

**版本**: v1.0  
**最后更新**: 2026-01-18  
**已实现**: 40/80 模型 (50%)  
**成功率**: 72.0%

---

## 模型总览

### 按类别统计

| 类别 | 已实现 | 总数 | 完成率 |
|------|--------|------|--------|
| 曲线定义 | 3 | 3 | 100% |
| 标准方程 | 8 | 8 | 100% |
| 参数关系 | 3 | 5 | 60% |
| 焦半径通径 | 2 | 5 | 40% |
| 渐近线 | 3 | 4 | 75% |
| 准线 | 1 | 5 | 20% |
| 焦点三角形 | 1 | 3 | 33% |
| 韦达定理 | 3 | 3 | 100% |
| 点差法 | 1 | 3 | 33% |
| 三角形定理 | 2 | 3 | 67% |
| 距离坐标 | 2 | 4 | 50% |
| 三角形面积 | 1 | 3 | 33% |
| 向量运算 | 2 | 4 | 50% |
| 不等式 | 1 | 2 | 50% |
| 判别式 | 1 | 3 | 33% |
| 三角形特殊 | 1 | 4 | 25% |
| 圆相关 | 1 | 2 | 50% |
| 高级技巧 | 2 | 3 | 67% |

---

## 一、曲线定义模型 (ID: 0-2)

### Model 0: Ellipse_Definition (椭圆定义)

**数学定义**:
```
|PF₁| + |PF₂| = 2a
```
椭圆上任一点到两焦点距离之和为定值

**前置条件**:
- 存在 Ellipse 实体

**输出**:
- `geometric_relations`: 椭圆定义关系式

**适用场景**:
- 已知椭圆及其焦点
- 需要建立点到焦点的距离关系

---

### Model 1: Hyperbola_Definition (双曲线定义)

**数学定义**:
```
||PF₁| - |PF₂|| = 2a
```
双曲线上任一点到两焦点距离之差的绝对值为定值

**前置条件**:
- 存在 Hyperbola 实体

**输出**:
- `geometric_relations`: 双曲线定义关系式

**适用场景**:
- 已知双曲线及其焦点
- 需要建立点到焦点的距离关系

---

### Model 2: Parabola_Definition (抛物线定义)

**数学定义**:
```
|PF| = d（到准线距离）
```
抛物线上点到焦点距离等于到准线距离

**前置条件**:
- 存在 Parabola 实体

**输出**:
- `geometric_relations`: 抛物线定义关系式

**适用场景**:
- 已知抛物线焦点和准线
- 需要建立距离等式

---

## 二、标准方程模型 (ID: 3-10)

### Model 3: Ellipse_Equation_Standard_X (椭圆标准方程-焦点在x轴)

**标准方程**:
```
x²/a² + y²/b² = 1  (a > b > 0)
```

**前置条件**:
- 存在 Ellipse 实体
- 有标准方程 (焦点在x轴)

**输出**:
- `parameters`: a, b, a², b²

**适用场景**:
- 从方程提取椭圆参数
- 识别椭圆焦点位置

---

### Model 4: Ellipse_Equation_Standard_Y (椭圆标准方程-焦点在y轴)

**标准方程**:
```
y²/a² + x²/b² = 1  (a > b > 0)
```

**前置条件**:
- 存在 Ellipse 实体
- 有标准方程 (焦点在y轴)

**输出**:
- `parameters`: a, b, a², b²

**适用场景**:
- 从方程提取椭圆参数
- 焦点在y轴的情况

---

### Model 5: Hyperbola_Equation_Standard_X (双曲线标准方程-焦点在x轴)

**标准方程**:
```
x²/a² - y²/b² = 1  (a, b > 0)
```

**前置条件**:
- 存在 Hyperbola 实体
- 有标准方程 (焦点在x轴)

**输出**:
- `parameters`: a, b, a², b²

**适用场景**:
- 从方程提取双曲线参数
- 识别双曲线焦点位置

---

### Model 6: Hyperbola_Equation_Standard_Y (双曲线标准方程-焦点在y轴)

**标准方程**:
```
y²/a² - x²/b² = 1  (a, b > 0)
```

**前置条件**:
- 存在 Hyperbola 实体
- 有标准方程 (焦点在y轴)

**输出**:
- `parameters`: a, b, a², b²

**适用场景**:
- 从方程提取双曲线参数
- 焦点在y轴的情况

---

### Model 7: Parabola_Equation_Standard_Right (抛物线标准方程-开口向右)

**标准方程**:
```
y² = 2px  (p > 0)
```

**前置条件**:
- 存在 Parabola 实体
- 有标准方程 (开口向右)

**输出**:
- `parameters`: p, p/2
- `coordinates`: Focus, Directrix

**适用场景**:
- 从方程提取抛物线参数
- 开口向右的抛物线

---

### Model 8: Parabola_Equation_Standard_Left (抛物线标准方程-开口向左)

**标准方程**:
```
y² = -2px  (p > 0)
```

**前置条件**:
- 存在 Parabola 实体
- 有标准方程 (开口向左)

**输出**:
- `parameters`: p, p/2
- `coordinates`: Focus, Directrix

**适用场景**:
- 开口向左的抛物线

---

### Model 9: Parabola_Equation_Standard_Up (抛物线标准方程-开口向上)

**标准方程**:
```
x² = 2py  (p > 0)
```

**前置条件**:
- 存在 Parabola 实体
- 有标准方程 (开口向上)

**输出**:
- `parameters`: p, p/2
- `coordinates`: Focus, Directrix

**适用场景**:
- 开口向上的抛物线

---

### Model 10: Parabola_Equation_Standard_Down (抛物线标准方程-开口向下)

**标准方程**:
```
x² = -2py  (p > 0)
```

**前置条件**:
- 存在 Parabola 实体
- 有标准方程 (开口向下)

**输出**:
- `parameters`: p, p/2
- `coordinates`: Focus, Directrix

**适用场景**:
- 开口向下的抛物线

---

## 三、参数关系与离心率 (ID: 11-15)

### Model 11: Ellipse_Parameter_Relation (椭圆参数关系)

**公式**:
```
a² = b² + c²
```
其中 a > b > 0，c 是半焦距

**前置条件**:
- 存在 Ellipse 实体
- 至少有一个参数 (a, b, c)

**输出**:
- `parameters`: 计算缺失的参数

**适用场景**:
- 已知部分参数，求其他参数
- 椭圆参数转换

---

### Model 12: Hyperbola_Parameter_Relation (双曲线参数关系)

**公式**:
```
c² = a² + b²
```
其中 a, b > 0，c 是半焦距

**前置条件**:
- 存在 Hyperbola 实体
- 至少有一个参数 (a, b, c)

**输出**:
- `parameters`: 计算缺失的参数
- `geometric_relations`: 虚轴长、实轴长

**适用场景**:
- 已知部分参数，求其他参数
- 双曲线参数转换

---

### Model 13: Eccentricity_Formula (离心率公式)

**公式**:
```
e = c/a
```
通用离心率定义

**前置条件**:
- 有 c 和 a 参数
- 或有 a, b 参数（可计算 c）

**输出**:
- `parameters`: e (离心率)
- `geometric_relations`: e = c/a

**适用场景**:
- 计算椭圆或双曲线离心率
- 已知焦距和长轴

---

### Model 14: Ellipse_Eccentricity_Range (椭圆离心率范围)

**范围**:
```
0 < e < 1
```

**前置条件**:
- 存在 Ellipse 实体
- 讨论离心率或有 e 参数

**输出**:
- `geometric_relations`: 离心率范围约束

**适用场景**:
- 椭圆离心率取值范围
- 参数约束条件

---

## 四、焦半径与通径 (ID: 16-20)

### Model 16: Ellipse_Focal_Radius (椭圆焦半径)

**公式**:
```
焦点在x轴:
  |PF₁| = a + ex₀
  |PF₂| = a - ex₀

焦点在y轴:
  |PF₁| = a + ey₀
  |PF₂| = a - ey₀
```

**前置条件**:
- 存在 Ellipse 实体
- 已知 a 和 e（或 c）
- 有点在椭圆上

**输出**:
- `geometric_relations`: 焦半径公式

**适用场景**:
- 计算椭圆上点到焦点的距离

---

### Model 17: Parabola_Focal_Radius (抛物线焦半径)

**公式**:
```
|PF| = x₀ + p/2  (开口向右)
|PF| = y₀ + p/2  (开口向上)
```

**前置条件**:
- 存在 Parabola 实体
- 已知 p 参数

**输出**:
- `geometric_relations`: 焦半径公式

**适用场景**:
- 计算抛物线上点到焦点的距离

---

### Model 19: Hyperbola_Latus_Rectum (双曲线通径)

**公式**:
```
通径长度 = 2b²/a
```

**前置条件**:
- 存在 Hyperbola 实体
- 已知 a, b 参数

**输出**:
- `parameters`: latus_rectum
- `geometric_relations`: 通径长度

**适用场景**:
- 计算双曲线的通径长度

---

## 五、渐近线相关 (ID: 21-24)

### Model 21: Hyperbola_Asymptote (双曲线渐近线)

**方程**:
```
焦点在x轴: y = ±(b/a)x
焦点在y轴: x = ±(b/a)y
```

**前置条件**:
- 存在 Hyperbola 实体
- 已知 a, b 参数

**输出**:
- `equations`: 渐近线方程
- `geometric_relations`: 渐近线关系

**适用场景**:
- 求双曲线渐近线方程

---

### Model 22: Hyperbola_Focus_To_Asymptote_Distance (焦点到渐近线距离)

**公式**:
```
d = b
```
焦点到渐近线的距离等于 b

**前置条件**:
- 存在 Hyperbola 实体
- 有渐近线信息
- 已知 b 参数

**输出**:
- `geometric_relations`: 距离公式

**适用场景**:
- 计算焦点到渐近线的距离

---

### Model 24: Hyperbola_Equal_Axis (等轴双曲线)

**性质**:
```
a = b  ⇒  e = √2
渐近线: y = ±x
```

**前置条件**:
- 存在 Hyperbola 实体
- 有渐近线为 y = ±x 或提及等轴双曲线

**输出**:
- `parameters`: a = b, e = √2
- `geometric_relations`: 等轴双曲线性质

**适用场景**:
- 识别等轴双曲线
- 简化计算

---

## 六、第二定义与准线 (ID: 25-29)

### Model 29: Parabola_Directrix (抛物线准线)

**方程**:
```
开口向右: x = -p/2
开口向左: x = p/2
开口向上: y = -p/2
开口向下: y = p/2
```

**前置条件**:
- 存在 Parabola 实体
- 已知 p 参数

**输出**:
- `geometric_relations`: 准线方程

**适用场景**:
- 求抛物线准线方程

---

## 七、焦点三角形 (ID: 30-32)

### Model 32: Ellipse_Focal_Triangle_Perimeter (椭圆焦点三角形周长)

**公式**:
```
周长 = 2(a + c)
```
其中 △PF₁F₂ 是椭圆焦点三角形

**前置条件**:
- 存在 Ellipse 实体
- 已知 a, c 参数
- 有焦点三角形

**输出**:
- `parameters`: perimeter
- `geometric_relations`: 周长公式

**适用场景**:
- 计算焦点三角形周长

---

## 八、韦达定理系列 (ID: 41-43)

### Model 41: Vieta_Theorem (韦达定理)

**公式**:
```
对于 Ax² + Bx + C = 0:
  x₁ + x₂ = -B/A
  x₁ · x₂ = C/A
```

**前置条件**:
- 存在二次方程

**输出**:
- `parameters`: x1_plus_x2, x1_times_x2
- `geometric_relations`: 韦达定理关系式

**适用场景**:
- 曲线与直线交点
- 根与系数关系

---

### Model 42: Vieta_Theorem_Sum (韦达定理-和)

**公式**:
```
x₁ + x₂ = -B/A
```

**前置条件**:
- 存在二次方程

**输出**:
- `parameters`: x1_plus_x2

**适用场景**:
- 只需要根的和

---

### Model 43: Vieta_Theorem_Product (韦达定理-积)

**公式**:
```
x₁ · x₂ = C/A
```

**前置条件**:
- 存在二次方程

**输出**:
- `parameters`: x1_times_x2

**适用场景**:
- 只需要根的积

---

## 九、点差法 (ID: 44-46)

### Model 46: Point_Difference_Method_Hyperbola (点差法-双曲线)

**原理**:
```
设两点 P₁(x₁, y₁), P₂(x₂, y₂) 在双曲线上
两式相减得:
  (x₁² - x₂²)/a² - (y₁² - y₂²)/b² = 0
⇒ k_AB = (b²/a²) · (x₁ + x₂)/(y₁ + y₂)
```

**前置条件**:
- 存在 Hyperbola 实体
- 有中点或弦相关信息

**输出**:
- `geometric_relations`: 点差法关系式

**适用场景**:
- 弦的中点问题
- 斜率与中点关系

---

## 十、三角形定理 (ID: 47-49)

### Model 47: Cosine_Law (余弦定理)

**公式**:
```
c² = a² + b² - 2ab·cos(C)
```

**前置条件**:
- 存在 Triangle 实体
- 有边长或角度信息

**输出**:
- `geometric_relations`: 余弦定理关系式

**适用场景**:
- 计算三角形边长
- 已知两边一角

---

### Model 57: Triangle_Area_With_Sin (三角形面积-正弦公式)

**公式**:
```
S = (1/2)ab·sin(C)
```

**前置条件**:
- 有三角形或面积相关信息
- 有边长或角度

**输出**:
- `geometric_relations`: 面积公式

**适用场景**:
- 计算三角形面积
- 已知两边夹角

---

## 十一、距离与坐标 (ID: 52-55)

### Model 53: Two_Points_Distance (两点距离公式)

**公式**:
```
d = √[(x₂ - x₁)² + (y₂ - y₁)²]
```

**前置条件**:
- 有两个点的坐标

**输出**:
- `parameters`: distance
- `geometric_relations`: 距离公式

**适用场景**:
- 计算两点距离

---

### Model 54: Midpoint_Formula (中点公式)

**公式**:
```
M = ((x₁ + x₂)/2, (y₁ + y₂)/2)
```

**前置条件**:
- 有两个点的坐标
- 或有中点相关信息

**输出**:
- `coordinates`: 中点坐标
- `geometric_relations`: 中点关系

**适用场景**:
- 计算线段中点
- 中点弦问题

---

## 十二、三角形面积 (ID: 56-58)

### Model 56: Triangle_Area_Formula (三角形面积公式)

**公式**:
```
S = (1/2)|x₁(y₂ - y₃) + x₂(y₃ - y₁) + x₃(y₁ - y₂)|
```

**前置条件**:
- 有三个点的坐标

**输出**:
- `parameters`: area
- `geometric_relations`: 面积公式

**适用场景**:
- 已知三点坐标求面积

---

## 十三、向量运算 (ID: 59-62)

### Model 61: Vector_Perpendicular_Condition (向量垂直条件)

**公式**:
```
a⃗ ⊥ b⃗  ⇔  a⃗·b⃗ = 0
⇔  x₁x₂ + y₁y₂ = 0
```

**前置条件**:
- 有向量信息
- 或有垂直关系

**输出**:
- `geometric_relations`: 垂直条件

**适用场景**:
- 判断向量垂直
- 垂直约束条件

---

### Model 62: Vector_Collinear_Condition (向量共线条件)

**公式**:
```
a⃗ ∥ b⃗  ⇔  x₁y₂ - x₂y₁ = 0
⇔  x₁/x₂ = y₁/y₂
```

**前置条件**:
- 有向量信息
- 或有共线/平行判断需求

**输出**:
- `geometric_relations`: 共线条件

**适用场景**:
- 判断三点共线
- 向量平行条件

---

## 十四、不等式 (ID: 63-64)

### Model 63: Basic_Inequality (基本不等式)

**公式**:
```
a + b ≥ 2√(ab)  (a, b > 0)
等号成立条件: a = b
```

**前置条件**:
- 需要求最值
- 或有不等式相关信息

**输出**:
- `geometric_relations`: 基本不等式

**适用场景**:
- 求最值问题
- 已知和求积/已知积求和

---

## 十五、判别式 (ID: 65-67)

### Model 65: Discriminant_Delta (判别式)

**公式**:
```
Δ = B² - 4AC

Δ > 0: 两个不相等实根
Δ = 0: 两个相等实根
Δ < 0: 无实根
```

**前置条件**:
- 存在二次方程
- 讨论根的情况

**输出**:
- `parameters`: Delta
- `geometric_relations`: 判别式关系

**适用场景**:
- 判断直线与曲线位置关系
- 交点个数判断

---

## 十六、三角形特殊定理 (ID: 68-71)

### Model 70: Incircle_Radius_Formula (内切圆半径公式)

**公式**:
```
r = S/s
其中 S 是面积，s = (a + b + c)/2 是半周长
```

**前置条件**:
- 有三角形
- 已知面积或边长

**输出**:
- `parameters`: incircle_radius
- `geometric_relations`: 内切圆半径

**适用场景**:
- 计算内切圆半径

---

## 十七、圆相关 (ID: 75-76)

### Model 75: Circle_Standard_Equation (圆的标准方程)

**方程**:
```
(x - h)² + (y - k)² = r²
```
圆心 (h, k)，半径 r

**前置条件**:
- 存在 Circle 实体
- 有方程或圆心半径信息

**输出**:
- `parameters`: h, k, r
- `coordinates`: 圆心

**适用场景**:
- 识别圆的标准方程
- 提取圆心和半径

---

## 十八、高级技巧 (ID: 77-79)

### Model 78: Substitution_X_Equals_MY_Plus_N (代换 x = my + n)

**技巧**:
```
设直线: x = my + n
代入曲线方程消元
```

**前置条件**:
- 有直线与曲线
- 直线可能垂直于 x 轴或斜率不存在

**输出**:
- `equations`: 代换后的方程
- `geometric_relations`: 代换关系

**适用场景**:
- 处理垂直或近垂直直线
- 避免斜率不存在的情况

---

### Model 79: Quadratic_Function_Maximum (二次函数最值)

**公式**:
```
f(x) = ax² + bx + c  (a ≠ 0)

对称轴: x = -b/(2a)
最值: f(-b/(2a)) = c - b²/(4a)

a > 0: 最小值
a < 0: 最大值
```

**前置条件**:
- 有二次函数
- 讨论最值

**输出**:
- `parameters`: 对称轴, 最值
- `geometric_relations`: 最值公式

**适用场景**:
- 求二次函数最值
- 参数范围问题

---

## 附录：模型状态说明

### 状态标识

- ✅ **已实现**: 模型代码完成并通过测试
- ⏳ **未实现**: 模型尚未实现

### 应用成功率

**整体**: 72.0%  
**分类统计**:
- 曲线定义: ~85%
- 标准方程: ~90%
- 参数关系: ~75%
- 几何工具: ~70%
- 代数工具: ~80%

### 高频模型 (Top 10)

1. Model 5: Hyperbola_Equation_Standard_X (双曲线标准方程)
2. Model 12: Hyperbola_Parameter_Relation (双曲线参数关系)
3. Model 13: Eccentricity_Formula (离心率公式)
4. Model 3: Ellipse_Equation_Standard_X (椭圆标准方程)
5. Model 41: Vieta_Theorem (韦达定理)
6. Model 9: Parabola_Equation_Standard_Up (抛物线标准方程)
7. Model 21: Hyperbola_Asymptote (双曲线渐近线)
8. Model 53: Two_Points_Distance (两点距离)
9. Model 11: Ellipse_Parameter_Relation (椭圆参数关系)
10. Model 16: Ellipse_Focal_Radius (椭圆焦半径)

---

**文档版本**: v1.0  
**维护**: EGR Team  
**最后更新**: 2026-01-18  
**参见**: [API Reference](../doc/api_reference.md)
