
## 📊 **Conic10K 数据集整体结构**

每个问题包含 **7个字段**，形成一个完整的数学问题标注体系：

```json
{
    "text": "自然语言问题",
    "fact_expressions": "形式化的条件/事实",
    "query_expressions": "形式化的查询目标",
    "answer_expressions": "形式化的答案",
    "fact_spans": "事实对应的文本位置",
    "query_spans": "查询对应的文本位置",
    "process": "自然语言解题过程"
}
```

---

## 🔍 **逐字段详细解析**

### 1️⃣ **text（问题文本）**

**格式**: 自然语言 + LaTeX数学公式

**示例**：
```json
"text": "椭圆$\\frac{x^{2}}{2}+\\frac{y^{2}}{3}=1$的离心率为?"
```

**特点**：
- 使用LaTeX格式表示数学公式（`$...$`包裹）
- 平均每个问题包含 **5.76个LaTeX表达式**
- 平均 **83.43个token**

---

### 2️⃣ **fact_expressions（形式化条件）**

**作用**: 将问题中的条件翻译成**无歧义的形式化语言**

**语法**: 基于断言逻辑（Assertional Logic）

#### **基本组成部分**：

| 组件 | 格式 | 示例 |
|------|------|------|
| **声明** | `变量: 类型` | `G: Ellipse` |
| **断言** | `操作符(参数) = 值` | `Eccentricity(G) = 1/2` |
| **不等式** | `表达式 > 值` | `a>0`, `m>0` |

---

### 📝 **案例1：简单椭圆问题**

```json
{
    "text": "椭圆$\\frac{x^{2}}{2}+\\frac{y^{2}}{3}=1$的离心率为?",
    
    "fact_expressions": "G: Ellipse;Expression(G) = (x^2/2 + y^2/3 = 1)",
    
    "query_expressions": "Eccentricity(G)",
    
    "answer_expressions": "sqrt(3)/3"
}
```

**解读**：

```python
# fact_expressions 翻译：
G: Ellipse                              # 声明：G是一个椭圆
Expression(G) = (x^2/2 + y^2/3 = 1)    # 条件：G的方程是...

# query_expressions 翻译：
Eccentricity(G)                         # 求：G的离心率

# answer_expressions 翻译：
sqrt(3)/3                               # 答案：√3/3
```

---

### 📝 **案例2：复杂双曲线问题**

```json
{
    "text": "已知双曲线$\\frac{x^{2}}{4}-\\frac{y^{2}}{m^{2}}=1(m>0)$的一条渐近线方程是$5x-2y=0$，则$m$=?",
    
    "fact_expressions": "G: Hyperbola;m: Number;m>0;Expression(G) = (x^2/4 - y^2/m^2 = 1);Expression(OneOf(Asymptote(G))) = (5*x - 2*y = 0)",
    
    "query_expressions": "m",
    
    "answer_expressions": "5",
    
    "process": "双曲线的渐近线方程为y=±(m/2)x，直线5x-2y=0的方程可化为y=(5/2)x，所以m=5."
}
```

**形式化分解**：

```python
# 声明部分
G: Hyperbola        # G是双曲线
m: Number          # m是数字

# 约束条件
m > 0              # m大于0

# 方程信息
Expression(G) = (x^2/4 - y^2/m^2 = 1)  # 双曲线方程

# 渐近线信息
Expression(OneOf(Asymptote(G))) = (5*x - 2*y = 0)  
# OneOf表示"其中一条"渐近线

# 查询目标
m  # 求m的值

# 答案
5
```

---

### 📝 **案例3：几何关系复杂问题**

这是一个非常复杂的例子，展示了形式化表示的强大表达能力：

```json
{
    "text": "已知$F$点为双曲线$C$: $\\frac{x^{2}}{a^{2}}-\\frac{y^{2}}{b^{2}}=1(a>0, b>0)$的一个焦点，以点$F$为圆心的圆与$C$的渐近线相切，且与$C$交于$A$、$B$两点，若$AF \\perp x$轴，则$C$的离心率为?"
}
```

**形式化表示**：

```python
# 1. 声明所有对象
C: Hyperbola        # C是双曲线
b: Number           # 参数b
a: Number           # 参数a
G: Circle          # G是圆
A: Point           # 点A
B: Point           # 点B
F: Point           # 点F

# 2. 参数约束
a > 0
b > 0

# 3. 双曲线信息
Expression(C) = (-y^2/b^2 + x^2/a^2 = 1)
OneOf(Focus(C)) = F    # F是C的一个焦点

# 4. 圆的信息
Center(G) = F          # 圆心是F
IsTangent(Asymptote(C), G)  # 圆与渐近线相切

# 5. 交点信息
Intersection(G, C) = {A, B}  # 圆与双曲线交于A、B

# 6. 垂直关系
IsPerpendicular(LineSegmentOf(A, F), xAxis)  # AF垂直于x轴

# 7. 查询
Eccentricity(C)  # 求离心率

# 8. 答案
sqrt(2)
```

---

### 3️⃣ **操作符类型总览**

数据集使用了 **94个操作符** 和 **20个概念**：

#### **几何对象（概念）**：
```
Ellipse, Hyperbola, Parabola, Circle, Line, Point, 
LineSegment, Triangle, Origin, ...
```

#### **常用操作符分类**：

| 类别 | 操作符示例 | 说明 |
|------|-----------|------|
| **方程/表达式** | `Expression()` | 获取曲线方程 |
| **几何属性** | `Focus()`, `Vertex()`, `Center()` | 焦点、顶点、圆心 |
| **距离/长度** | `Distance()`, `Length()`, `Abs()` | 距离、长度 |
| **坐标系** | `Coordinate()`, `XCoordinate()` | 坐标 |
| **曲线特征** | `Eccentricity()`, `Asymptote()` | 离心率、渐近线 |
| **位置关系** | `PointOnCurve()`, `Intersection()` | 点在曲线上、交点 |
| **几何关系** | `IsTangent()`, `IsPerpendicular()` | 相切、垂直 |
| **集合操作** | `OneOf()`, `Min()`, `Max()` | 其中之一、最小、最大 |
| **向量** | `VectorOf()` | 向量 |

---

### 4️⃣ **fact_spans 和 query_spans（文本对齐）**

**作用**: 标注形式化表示的每个句子在原文中的位置

**格式**: 三维数组 `[[[start, end], ...], ...]`

**示例解析**：

```json
{
    "text": "椭圆$\\frac{x^{2}}{2}+\\frac{y^{2}}{3}=1$的离心率为?",
    //      0123456789...                           01234
    //      位置索引（字符级别）
    
    "fact_expressions": "G: Ellipse;Expression(G) = (x^2/2 + y^2/3 = 1)",
    //                   ^^^^^^^^   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    //                   句子1      句子2
    
    "fact_spans": "[[[0, 37]], [[0, 37]]]",
    //              句子1对应   句子2对应
    //              文本[0:37]  文本[0:37]
}
```

**更复杂的例子**：

```json
{
    "text": "已知双曲线$\\frac{x^{2}}{4}-\\frac{y^{2}}{m^{2}}=1(m>0)$...",
    
    "fact_expressions": "G: Hyperbola;m: Number;m>0;...",
    //                   ^^^^^^^^^^^  ^^^^^^^^  ^^^
    //                   句子1        句子2     句子3
    
    "fact_spans": "[[[2, 49]], [[71, 74]], [[5, 49]], ...]"
    //              句子1从字符2  句子2从字符71  句子3从字符5
    //              到字符49      到字符74       到字符49
}
```

**为什么需要这个字段？**
- ✅ 验证标注正确性
- ✅ 训练语义解析模型
- ✅ 可解释性：追踪形式化表示来源

---

### 5️⃣ **process（解题过程）**

**格式**: 自然语言（中文+LaTeX）

**示例**：

```json
{
    "text": "抛物线$x^{2}=ay$过点$A(1, \\frac{1}{4})$，则点$A$到此抛物线的焦点的距离为?",
    
    "process": "∵抛物线x²=ay过点A(1,1/4)，∴1²=a×1/4，解得a=4。因此抛物线的方程为x²=4y，得到其焦点为F(0,1)，准线方程为y=-1。∵抛物线上的点到焦点的距离等于该点到抛物线准线的距离，∴点A到此抛物线的焦点的距离为1/4-(-1)=1/4+1=5/4"
}
```

**特点**：
- 有些问题有详细的推理过程
- **有些问题 process 为空字符串**（如第一个例子）
- 平均推理步数：**4.23步**

---

## 🎯 **特殊语法：伪操作符**

为了更贴近自然语言，设计了3个**伪操作符**：

### 1. **OneOf（其中之一）**

```python
# 例子：一条渐近线（双曲线有两条）
Expression(OneOf(Asymptote(G))) = (5*x - 2*y = 0)

# 而不是明确指定是哪一条
```

### 2. **WhenMin / WhenMax（在最小/最大值时）**

```python
# 例子：当距离和最小时的情况
WhenMin(Abs(LineSegmentOf(F1,M)) + Abs(LineSegmentOf(F1,N)))
```

---

## 📊 **数据复杂度展示**

让我用一个**完整的复杂案例**展示所有组件：

```json
{
    "text": "设$P$为双曲线$\\frac{x^{2}}{a^{2}}-\\frac{y^{2}}{b^{2}}=1(a>0, b>0)$上除顶点外的任意一点，$F_{1}$、$F_{2}$分别为左右焦点，$\\Delta F_{1}PF_{2}$的内切圆交实轴于点$M$，则$|F_{1}M|\\cdot|MF_{2}|$值为?",
    
    "fact_expressions": "G: Hyperbola;b: Number;a: Number;F1: Point;P: Point;F2: Point;M: Point;a>0;b>0;Expression(G) = (-y^2/b^2 + x^2/a^2 = 1);PointOnCurve(P, G);Negation(P=Vertex(G));LeftFocus(G) = F1;RightFocus(G) = F2;Intersection(InscribedCircle(TriangleOf(F1, P, F2)), RealAxis(G)) = M",
    
    "query_expressions": "Abs(LineSegmentOf(F1, M))*Abs(LineSegmentOf(M, F2))",
    
    "answer_expressions": "b^2"
}
```

**复杂度分析**：
- ✅ 7个对象声明
- ✅ 2个参数约束
- ✅ 9个断言
- ✅ 嵌套函数调用（如 `InscribedCircle(TriangleOf(...))`）
- ✅ 复杂查询表达式（乘积）

---

## 🔥 **数据集的核心创新点**

### 1. **双重标注体系**

```
自然语言 ←→ 形式化表示
     ↓           ↓
  text      fact/query_expressions
     ↓           ↓
  spans    文本位置对齐
```

### 2. **可验证性**

形式化表示使得：
- ✅ 可以自动检查标注一致性
- ✅ 可以符号推理验证答案
- ✅ 消除自然语言歧义

### 3. **分离理解与推理**

通过两个任务评估：

| 任务 | 输入 | 输出 | 评估能力 |
|------|------|------|---------|
| **语义解析** | text | fact/query_expressions | **理解**能力 |
| **数学问答** | text | answer | **理解+推理**能力 |

---

## 📈 **数据统计回顾**

```
总问题数:          10,861
训练集:            7,758 (71.4%)
验证集:            1,035 (9.5%)
测试集:            2,068 (19.1%)

形式化标注:
  - 操作符数:       94
  - 概念数:         20
  - 平均句子数:     10.55/问题
  - 平均操作符:     15.70/问题

复杂度:
  - 平均推理步数:   4.23
  - 平均LaTeX数:   5.76
  - 平均Token数:   83.43
```

---

## 💡 **为什么这个数据集设计得好？**

1. **封闭知识域** → 控制变量，纯粹测试推理能力
2. **形式化表示** → 无歧义，可验证，可自动评估理解能力
3. **文本对齐** → 可解释性，训练对齐模型
4. **高质量标注** → 双人标注+验证员+自动检查+模型交叉验证
5. **推理步数多** → 真正考验复杂推理，而非简单模式匹配

