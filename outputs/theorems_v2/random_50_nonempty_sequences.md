# 随机抽取的非空定理序列题目

- 数据文件：`C:\GitHub\EGR\data\train_with_models_v3_candidate.json`
- 序列字段：`models_v3_executable`
- 非空候选数：5359
- 抽样数：50
- 随机种子：20260708
- Applicator 完整执行：4/50
- 最终答案正确：2/50

## 1. 题目 ID 300

- 数据索引：299
- V3 质量：C

### 题目

过椭圆$\frac{x^{2}}{4}+\frac{y^{2}}{3}=1$的左焦点$F_{1}$作直线$l$交椭圆于$A$、$B$两点，则$\triangle A B F_{2}$(其中$F_{2}$为椭圆的右焦点) 的周长为?

### 形式化信息

- 已知：`l: Line;G: Ellipse;A: Point;B: Point;F2: Point;F1: Point;Expression(G) = (x^2/4 + y^2/3 = 1);LeftFocus(G) = F1;RightFocus(G)=F2;PointOnCurve(F1, l);Intersection(l, G) = {A, B}`
- 查询：`Perimeter(TriangleOf(A,B,F2))`
- 答案：`8`

### 解题过程

$由椭圆\frac{x^{2}}{4}+\frac{y^{2}}{3}=1可得a=2;椭圆的定义可得:|AF_{1}|+|AF_{2}|=|BF_{1}|+|BF_{2}|=2a=4\therefore\triangleABF_{2}的周长=|AB|+|AF_{2}|+|BF_{2}|=|AF_{1}|+|BF_{1}|+|AF_{2}|+|BF_{2}|=8.$

### 定理内容序列

#### 步骤 1：Ellipse_Equation_Standard_X

- 具体公式/规则：$x^2/a^2+y^2/b^2=1$
- 类别：`standard_equation`
- 所需对象类型：`无`
- 所需信息：`ExpressionPolynomial`
- 产出信息：`ConicStandardForm, ParameterOf`
- 目录依赖：`无`
- Applicator 支持：`CONCRETE`
- 本题执行状态：`APPLIED`

#### 步骤 2：Ellipse_Definition

- 具体公式/规则：$|PF1|+|PF2|=2a$
- 类别：`definition`
- 所需对象类型：`无`
- 所需信息：`无`
- 产出信息：`DefinitionRelation`
- 目录依赖：`无`
- Applicator 支持：`CONCRETE`
- 本题执行状态：`NO_MATCH`

### 当前 Applicator 回放结果

- 能否完整执行：**否（存在失败步骤）**
- 最终答案：**未得到正确答案**
- 初始目标状态：`GOAL_NOT_REACHED`
- 最终目标状态：`GOAL_NOT_REACHED`
- Applicator 实际值：`None`
- 标注期望值：`None`
- 结果说明：无
- 首个失败步骤：第 2 步
- 失败状态：`NO_MATCH`
- 缺失谓词：`无`
- 缺失对象类型：`无`

---

## 2. 题目 ID 405

- 数据索引：404
- V3 质量：C

### 题目

已知双曲线$\frac{x^{2}}{m}-y^{2}=1$的离心率是$2$，则$m$的值是?

### 形式化信息

- 已知：`G: Hyperbola;m: Number;Expression(G) = (-y^2 + x^2/m = 1);Eccentricity(G) = 2`
- 查询：`m`
- 答案：`1/3`

### 解题过程

$由题意知,双曲线的离心率e=\frac{\sqrt{m+1}}{\sqrt{m}}=2,解得m=\frac{1}{3}.$

### 定理内容序列

#### 步骤 1：Hyperbola_Equation_Standard_X

- 具体公式/规则：$x^2/a^2-y^2/b^2=1$
- 类别：`standard_equation`
- 所需对象类型：`无`
- 所需信息：`ExpressionPolynomial`
- 产出信息：`ConicStandardForm, ParameterOf`
- 目录依赖：`无`
- Applicator 支持：`CONCRETE`
- 本题执行状态：`NO_MATCH`

#### 步骤 2：Eccentricity_Formula

- 具体公式/规则：$e=c/a$
- 类别：`parameter`
- 所需对象类型：`无`
- 所需信息：`ParameterOf`
- 产出信息：`ParameterOf, EquationConstraint`
- 目录依赖：`Ellipse_Parameter_Relation → Hyperbola_Parameter_Relation`
- Applicator 支持：`CONCRETE`
- 本题执行状态：`NO_MATCH`

### 当前 Applicator 回放结果

- 能否完整执行：**否（存在失败步骤）**
- 最终答案：**未得到正确答案**
- 初始目标状态：`GOAL_UNSUPPORTED`
- 最终目标状态：`GOAL_UNSUPPORTED`
- Applicator 实际值：`None`
- 标注期望值：`None`
- 结果说明：query grammar is not supported
- 首个失败步骤：第 1 步
- 失败状态：`NO_MATCH`
- 缺失谓词：`无`
- 缺失对象类型：`无`

---

## 3. 题目 ID 411

- 数据索引：410
- V3 质量：C

### 题目

已知双曲线经过点$(1,2 \sqrt{2})$，其一条渐近线方程为$y=2 x$，则该双曲线的标准方程为?

### 形式化信息

- 已知：`G: Hyperbola;H: Point;Coordinate(H) = (1, 2*sqrt(2));PointOnCurve(H, G);Expression(OneOf(Asymptote(G))) = (y = 2*x)`
- 查询：`Expression(G)`
- 答案：`y^2/4-x^2=1`

### 解题过程

$由双曲线的渐近线方程设双曲线方程为x^{2}-\frac{y^{2}}{4}=\lambda(\lambda\neq0),由点(1,2\sqrt{2})在双曲线上,有1-\frac{(2\sqrt{2})}{4}=\lambda,所以\lambda=-1,故双曲线方程为\frac{y^{2}}{4}-x^{2}=1$

### 定理内容序列

#### 步骤 1：Hyperbola_Equation_Standard_X

- 具体公式/规则：$x^2/a^2-y^2/b^2=1$
- 类别：`standard_equation`
- 所需对象类型：`无`
- 所需信息：`ExpressionPolynomial`
- 产出信息：`ConicStandardForm, ParameterOf`
- 目录依赖：`无`
- Applicator 支持：`CONCRETE`
- 本题执行状态：`NO_MATCH`

#### 步骤 2：Hyperbola_Asymptote

- 具体公式/规则：$y=+/-(b/a)x$
- 类别：`asymptote`
- 所需对象类型：`Hyperbola`
- 所需信息：`ConicStandardForm`
- 产出信息：`AsymptoteFamilyOf, EquationConstraint`
- 目录依赖：`Hyperbola_Equation_Standard_X → Hyperbola_Equation_Standard_Y`
- Applicator 支持：`CONCRETE`
- 本题执行状态：`NO_MATCH`

### 当前 Applicator 回放结果

- 能否完整执行：**否（存在失败步骤）**
- 最终答案：**未得到正确答案**
- 初始目标状态：`GOAL_NOT_REACHED`
- 最终目标状态：`GOAL_NOT_REACHED`
- Applicator 实际值：`None`
- 标注期望值：`None`
- 结果说明：无
- 首个失败步骤：第 1 步
- 失败状态：`NO_MATCH`
- 缺失谓词：`ExpressionPolynomial`
- 缺失对象类型：`无`

---

## 4. 题目 ID 453

- 数据索引：452
- V3 质量：C

### 题目

已知双曲线$C$: $\frac{x^{2}}{a^{2}}-\frac{y^{2}}{b^{2}}=1(a>0, b>0)$的渐近线方程为$y=\pm \frac{1}{2} x$ , $F_{1}(-\sqrt{5}, 0)$ , $F_{2}(\sqrt{5}, 0)$分别为$C$的左，右焦点，若动点$P$在$C$的右支上，则$\frac{|P F_{1}|^{2}}{|P F_{2}|}$的最小值是?

### 形式化信息

- 已知：`C: Hyperbola;b: Number;a: Number;F1: Point;F2: Point;P: Point;a>0;b>0;Expression(C) = (-y^2/b^2 + x^2/a^2 = 1);Coordinate(F1) = (-sqrt(5), 0);Coordinate(F2) = (sqrt(5), 0);Expression(Asymptote(C)) = (y = pm*(x/2));LeftFocus(C) = F1;RightFocus(C) = F2;PointOnCurve(P, RightPart(C))`
- 查询：`Min(Abs(LineSegmentOf(P, F1))^2/Abs(LineSegmentOf(P, F2)))`
- 答案：`16`

### 解题过程

$因为双曲线的渐近线方程为y=\pm\frac{1}{2}x,焦点坐标为F_{1}(-\sqrt{5},0),F_{2}(\sqrt{5},0)所以\frac{b}{a}=\frac{1}{2},c=\sqrt{5},即a=2,b=1,所以双曲线方程为\frac{x^{2}}{4}-y^{2}=1设|PF_{2}|=m,则|PF_{1}|=4+m,且m\geqslant\sqrt{5}-2\frac{F_{1}^{2}}{F_{1}}=\frac{(4+m)^{2}}{m}=\frac{16}{m}+m+8\geqslant2\sqrt{\frac{16}{m}\cdotm}+8=16,当且仅当\frac{16}{m}=m,即m=4时等号成立所以\frac{|PF_{1}|^{2}}{|PF_{2}|}的最小值是16$

### 定理内容序列

#### 步骤 1：Hyperbola_Equation_Standard_X

- 具体公式/规则：$x^2/a^2-y^2/b^2=1$
- 类别：`standard_equation`
- 所需对象类型：`无`
- 所需信息：`ExpressionPolynomial`
- 产出信息：`ConicStandardForm, ParameterOf`
- 目录依赖：`无`
- Applicator 支持：`CONCRETE`
- 本题执行状态：`APPLIED`

#### 步骤 2：Hyperbola_Asymptote

- 具体公式/规则：$y=+/-(b/a)x$
- 类别：`asymptote`
- 所需对象类型：`Hyperbola`
- 所需信息：`ConicStandardForm`
- 产出信息：`AsymptoteFamilyOf, EquationConstraint`
- 目录依赖：`Hyperbola_Equation_Standard_X → Hyperbola_Equation_Standard_Y`
- Applicator 支持：`CONCRETE`
- 本题执行状态：`APPLIED`

#### 步骤 3：Hyperbola_Parameter_Relation

- 具体公式/规则：$c^2=a^2+b^2$
- 类别：`parameter`
- 所需对象类型：`无`
- 所需信息：`ParameterOf`
- 产出信息：`ParameterOf, EquationConstraint`
- 目录依赖：`Hyperbola_Equation_Standard_X → Hyperbola_Equation_Standard_Y`
- Applicator 支持：`CONCRETE`
- 本题执行状态：`APPLIED`

### 当前 Applicator 回放结果

- 能否完整执行：**是（完整执行）**
- 最终答案：**未得到正确答案**
- 初始目标状态：`GOAL_UNSUPPORTED`
- 最终目标状态：`GOAL_UNSUPPORTED`
- Applicator 实际值：`None`
- 标注期望值：`None`
- 结果说明：query grammar is not supported

---

## 5. 题目 ID 701

- 数据索引：700
- V3 质量：C

### 题目

已知定点$A(3,4)$，点$P$是抛物线$y^{2}=4 x$上一动点，点$P$到直线$x=-1$的距离为$d$，则$|P A|+d$的最小值是?

### 形式化信息

- 已知：`G: Parabola;H: Line;A: Point;P: Point;Expression(G) = (y^2 = 4*x);Expression(H) = (x = -1);Coordinate(A) = (3, 4);PointOnCurve(P, G);Distance(P, H) = d;d:Number`
- 查询：`Min(d + Abs(LineSegmentOf(P, A)))`
- 答案：`2*sqrt(5)`

### 解题过程

$点A是抛物线y^{2}=4x外一点,所以|PA|+d=|PF|+|PA|\geqslant|AF|=\sqrt{(3-1)^{2}+4^{2}}=2\sqrt{5},当且仅当点P为线段AF与抛物线交点时取等号,即|PA|+d的最小值是2\sqrt{5}$

### 定理内容序列

#### 步骤 1：Parabola_Equation_Standard_Right

- 具体公式/规则：$y^2=2px$
- 类别：`standard_equation`
- 所需对象类型：`无`
- 所需信息：`ExpressionPolynomial`
- 产出信息：`ConicStandardForm, ParameterOf`
- 目录依赖：`无`
- Applicator 支持：`CONCRETE`
- 本题执行状态：`APPLIED`

#### 步骤 2：Parabola_Definition

- 具体公式/规则：$|PF|=distance(P,directrix)$
- 类别：`definition`
- 所需对象类型：`无`
- 所需信息：`无`
- 产出信息：`DefinitionRelation`
- 目录依赖：`无`
- Applicator 支持：`CONCRETE`
- 本题执行状态：`NO_MATCH`

#### 步骤 3：Two_Points_Distance

- 具体公式/规则：$d=sqrt((x2-x1)^2+(y2-y1)^2)$
- 类别：`coordinate`
- 所需对象类型：`Point`
- 所需信息：`CoordinateOf`
- 产出信息：`CoordinateOf, DistanceOf, SlopeOf`
- 目录依赖：`无`
- Applicator 支持：`CONCRETE`
- 本题执行状态：`NO_MATCH`

### 当前 Applicator 回放结果

- 能否完整执行：**否（存在失败步骤）**
- 最终答案：**未得到正确答案**
- 初始目标状态：`GOAL_UNSUPPORTED`
- 最终目标状态：`GOAL_UNSUPPORTED`
- Applicator 实际值：`None`
- 标注期望值：`None`
- 结果说明：query grammar is not supported
- 首个失败步骤：第 2 步
- 失败状态：`NO_MATCH`
- 缺失谓词：`无`
- 缺失对象类型：`无`

---

## 6. 题目 ID 834

- 数据索引：833
- V3 质量：C

### 题目

过点$(2 \sqrt{3}, \sqrt{3})$且渐近线与双曲线$C$: $y^{2}-\frac{x^{2}}{2}=1$的渐近线相同的双曲线方程为?

### 形式化信息

- 已知：`C: Hyperbola;Expression(C) = (-x^2/2 + y^2 = 1);Z: Hyperbola;H: Point;Coordinate(H) = (2*sqrt(3), sqrt(3));PointOnCurve(H, Z);Asymptote(C) = Asymptote(Z)`
- 查询：`Expression(Z)`
- 答案：`x^2/6-y^2/3=1`

### 解题过程

$由题意可知,设与双曲线C:y^{2}-\frac{x^{2}}{2}=1的渐近线相同的双曲线方程为y^{2}-\frac{x^{2}}{2}=\lambda(\lambda\neq0),将点(2\sqrt{3},\sqrt{3})代入,即可求出\lambda,进而求出结果详解】根据题意,双曲线C:y^{2}-\frac{x^{2}}{2}=1渐近线方程为_{y}=\pm\frac{\sqrt{2}}{2}x'所以要求的双曲线方程为y^{2}-\frac{x^{2}}{2}=\lambda(\lambda\neq0),又过点(2\sqrt{3},\sqrt{3}),代入方程可得\lambda=-3,因此双曲线方程为\frac{x^{2}}{6}-\frac{y^{2}}{3}=1$

### 定理内容序列

#### 步骤 1：Hyperbola_Common_Asymptote_System

- 具体公式/规则：$x^2/a^2-y^2/b^2=lambda$
- 类别：`asymptote`
- 所需对象类型：`Hyperbola`
- 所需信息：`ConicStandardForm`
- 产出信息：`AsymptoteFamilyOf, EquationConstraint`
- 目录依赖：`Hyperbola_Asymptote`
- Applicator 支持：`CONCRETE`
- 本题执行状态：`NO_MATCH`

#### 步骤 2：Hyperbola_Equation_Standard_Y

- 具体公式/规则：$y^2/a^2-x^2/b^2=1$
- 类别：`standard_equation`
- 所需对象类型：`无`
- 所需信息：`ExpressionPolynomial`
- 产出信息：`ConicStandardForm, ParameterOf`
- 目录依赖：`无`
- Applicator 支持：`CONCRETE`
- 本题执行状态：`APPLIED`

### 当前 Applicator 回放结果

- 能否完整执行：**否（存在失败步骤）**
- 最终答案：**未得到正确答案**
- 初始目标状态：`GOAL_NOT_REACHED`
- 最终目标状态：`GOAL_NOT_REACHED`
- Applicator 实际值：`None`
- 标注期望值：`None`
- 结果说明：无
- 首个失败步骤：第 1 步
- 失败状态：`NO_MATCH`
- 缺失谓词：`ConicStandardForm`
- 缺失对象类型：`无`

---

## 7. 题目 ID 841

- 数据索引：840
- V3 质量：C

### 题目

点$P$是椭圆$\frac{x^{2}}{25}+\frac{y^{2}}{16}=1$上的动点，$F_{1}$为椭圆的左焦点，定点$M(6,4)$，则$P M+P F_{1}$的最大值为?

### 形式化信息

- 已知：`G: Ellipse;M: Point;P: Point;F1: Point;Expression(G) = (x^2/25 + y^2/16 = 1);Coordinate(M) = (6, 4);PointOnCurve(P, G);LeftFocus(G) = F1`
- 查询：`Max(LineSegmentOf(P, F1) + LineSegmentOf(P, M))`
- 答案：`15`

### 解题过程

$由椭圆方程可知a^{2}=25,b^{2}=16,\thereforec^{2}=25-16=9,\thereforec=3左焦点F_{1}(-3,0),右焦点F_{2}(3,0).由椭圆的定义可知PF_{1}+PF_{2}=2a=10,\thereforePF_{1}=10-PF_{2}.\thereforePM+PF_{1}=PM-PF_{2}+10.分析可知点M在椭圆外,所以PM-PF_{2}\leqslantMF_{2}=\sqrt{(6-3)^{2}+4^{2}}=5,\thereforePM+PF_{1}=PM-PF_{2}+10\leqslant5+10=15.即PM+PF的最大值为15.$

### 定理内容序列

#### 步骤 1：Ellipse_Equation_Standard_X

- 具体公式/规则：$x^2/a^2+y^2/b^2=1$
- 类别：`standard_equation`
- 所需对象类型：`无`
- 所需信息：`ExpressionPolynomial`
- 产出信息：`ConicStandardForm, ParameterOf`
- 目录依赖：`无`
- Applicator 支持：`CONCRETE`
- 本题执行状态：`APPLIED`

#### 步骤 2：Ellipse_Parameter_Relation

- 具体公式/规则：$a^2=b^2+c^2$
- 类别：`parameter`
- 所需对象类型：`无`
- 所需信息：`ParameterOf`
- 产出信息：`ParameterOf, EquationConstraint`
- 目录依赖：`Ellipse_Equation_Standard_X → Ellipse_Equation_Standard_Y`
- Applicator 支持：`CONCRETE`
- 本题执行状态：`APPLIED`

#### 步骤 3：Ellipse_Definition

- 具体公式/规则：$|PF1|+|PF2|=2a$
- 类别：`definition`
- 所需对象类型：`无`
- 所需信息：`无`
- 产出信息：`DefinitionRelation`
- 目录依赖：`无`
- Applicator 支持：`CONCRETE`
- 本题执行状态：`NO_MATCH`

#### 步骤 4：Eccentricity_Formula

- 具体公式/规则：$e=c/a$
- 类别：`parameter`
- 所需对象类型：`无`
- 所需信息：`ParameterOf`
- 产出信息：`ParameterOf, EquationConstraint`
- 目录依赖：`Ellipse_Parameter_Relation → Hyperbola_Parameter_Relation`
- Applicator 支持：`CONCRETE`
- 本题执行状态：`APPLIED`

#### 步骤 5：Ellipse_Second_Definition

- 具体公式/规则：$|PF|/d=e$
- 类别：`directrix`
- 所需对象类型：`无`
- 所需信息：`ParameterOf`
- 产出信息：`DirectrixExpressionOf`
- 目录依赖：`Eccentricity_Formula → Ellipse_Directrix`
- Applicator 支持：`CONCRETE`
- 本题执行状态：`APPLIED`

#### 步骤 6：Two_Points_Distance

- 具体公式/规则：$d=sqrt((x2-x1)^2+(y2-y1)^2)$
- 类别：`coordinate`
- 所需对象类型：`Point`
- 所需信息：`CoordinateOf`
- 产出信息：`CoordinateOf, DistanceOf, SlopeOf`
- 目录依赖：`无`
- Applicator 支持：`CONCRETE`
- 本题执行状态：`NO_MATCH`

### 当前 Applicator 回放结果

- 能否完整执行：**否（存在失败步骤）**
- 最终答案：**未得到正确答案**
- 初始目标状态：`GOAL_UNSUPPORTED`
- 最终目标状态：`GOAL_UNSUPPORTED`
- Applicator 实际值：`None`
- 标注期望值：`None`
- 结果说明：query grammar is not supported
- 首个失败步骤：第 3 步
- 失败状态：`NO_MATCH`
- 缺失谓词：`无`
- 缺失对象类型：`无`

---

## 8. 题目 ID 1166

- 数据索引：1165
- V3 质量：C

### 题目

点$(0,1)$到双曲线$x^{2}-\frac{y^{2}}{3}=1$的渐近线的距离是?

### 形式化信息

- 已知：`G: Hyperbola;H: Point;Expression(G) = (x^2 - y^2/3 = 1);Coordinate(H) = (0, 1)`
- 查询：`Distance(H, Asymptote(G))`
- 答案：`1/2`

### 解题过程

$\because渐近线方程为\sqrt{3}x\pmy=0,\therefore点(0,1)到直线的距离为d=\frac{|1|}{\sqrt{3+1}}=\frac{1}{2},$

### 定理内容序列

#### 步骤 1：Hyperbola_Equation_Standard_X

- 具体公式/规则：$x^2/a^2-y^2/b^2=1$
- 类别：`standard_equation`
- 所需对象类型：`无`
- 所需信息：`ExpressionPolynomial`
- 产出信息：`ConicStandardForm, ParameterOf`
- 目录依赖：`无`
- Applicator 支持：`CONCRETE`
- 本题执行状态：`APPLIED`

#### 步骤 2：Hyperbola_Asymptote

- 具体公式/规则：$y=+/-(b/a)x$
- 类别：`asymptote`
- 所需对象类型：`Hyperbola`
- 所需信息：`ConicStandardForm`
- 产出信息：`AsymptoteFamilyOf, EquationConstraint`
- 目录依赖：`Hyperbola_Equation_Standard_X → Hyperbola_Equation_Standard_Y`
- Applicator 支持：`CONCRETE`
- 本题执行状态：`APPLIED`

#### 步骤 3：Point_To_Line_Distance

- 具体公式/规则：$d=|Ax0+By0+C|/sqrt(A^2+B^2)$
- 类别：`coordinate`
- 所需对象类型：`Point`
- 所需信息：`CoordinateOf`
- 产出信息：`CoordinateOf, DistanceOf, SlopeOf`
- 目录依赖：`无`
- Applicator 支持：`CONCRETE`
- 本题执行状态：`NO_MATCH`

### 当前 Applicator 回放结果

- 能否完整执行：**否（存在失败步骤）**
- 最终答案：**未得到正确答案**
- 初始目标状态：`GOAL_UNSUPPORTED`
- 最终目标状态：`GOAL_UNSUPPORTED`
- Applicator 实际值：`None`
- 标注期望值：`None`
- 结果说明：query grammar is not supported
- 首个失败步骤：第 3 步
- 失败状态：`NO_MATCH`
- 缺失谓词：`LineNormalFormOf, RequestedPointLineDistanceOf`
- 缺失对象类型：`无`

---

## 9. 题目 ID 1326

- 数据索引：1325
- V3 质量：C

### 题目

若抛物线经过点$(-1, \frac{1}{2})$ ,$(2,2)$，则该抛物线的标准方程为?

### 形式化信息

- 已知：`G: Parabola;H: Point;I: Point;Coordinate(H) = (-1, 1/2);Coordinate(I) = (2, 2);PointOnCurve(H, G);PointOnCurve(I,G)`
- 查询：`Expression(G)`
- 答案：`x^2=2*y`

### 解题过程

$由所过两点坐标即可设出抛物线方程,待定系数即可求得结果因为抛物线经过点(-1,\frac{1}{2}),(2,2),即抛物线经过第一、二象限故设抛物线方程为x^{2}=2py,(p>0),代入点(2,2),可得4p=4,即p=1则抛物线方程为:x^{2}=2y.$

### 定理内容序列

#### 步骤 1：Parabola_Equation_Standard_Up

- 具体公式/规则：$x^2=2py$
- 类别：`standard_equation`
- 所需对象类型：`无`
- 所需信息：`ExpressionPolynomial`
- 产出信息：`ConicStandardForm, ParameterOf`
- 目录依赖：`无`
- Applicator 支持：`CONCRETE`
- 本题执行状态：`NO_MATCH`

### 当前 Applicator 回放结果

- 能否完整执行：**否（存在失败步骤）**
- 最终答案：**未得到正确答案**
- 初始目标状态：`GOAL_NOT_REACHED`
- 最终目标状态：`GOAL_NOT_REACHED`
- Applicator 实际值：`None`
- 标注期望值：`None`
- 结果说明：无
- 首个失败步骤：第 1 步
- 失败状态：`NO_MATCH`
- 缺失谓词：`ExpressionPolynomial`
- 缺失对象类型：`无`

---

## 10. 题目 ID 1405

- 数据索引：1404
- V3 质量：C

### 题目

已知点$P(2,2 \sqrt{2})$为抛物线$y^{2}=2 p x$上一点，那么点$P$到抛物线准线的距离是?

### 形式化信息

- 已知：`G: Parabola;Expression(G) = (y^2 = 2*(p*x));p: Number;P: Point;Coordinate(P) = (2, 2*sqrt(2));PointOnCurve(P, G)`
- 查询：`Distance(P, Directrix(G))`
- 答案：`3`

### 解题过程

$\because点P(2,2\sqrt{2})为抛物线y^{2}=2px上一点,\therefore(2\sqrt{2})^{2}=2p\times2,解得p=2,\therefore抛物线焦点坐标为(1,0),准线方程为x=-1\therefore点P到抛物线的准线的距离为2-(-1)=3$

### 定理内容序列

#### 步骤 1：Parabola_Equation_Standard_Right

- 具体公式/规则：$y^2=2px$
- 类别：`standard_equation`
- 所需对象类型：`无`
- 所需信息：`ExpressionPolynomial`
- 产出信息：`ConicStandardForm, ParameterOf`
- 目录依赖：`无`
- Applicator 支持：`CONCRETE`
- 本题执行状态：`NO_MATCH`

#### 步骤 2：Parabola_Definition

- 具体公式/规则：$|PF|=distance(P,directrix)$
- 类别：`definition`
- 所需对象类型：`无`
- 所需信息：`无`
- 产出信息：`DefinitionRelation`
- 目录依赖：`无`
- Applicator 支持：`CONCRETE`
- 本题执行状态：`NO_MATCH`

#### 步骤 3：Parabola_Directrix

- 具体公式/规则：$x or y=+/-p/2$
- 类别：`directrix`
- 所需对象类型：`无`
- 所需信息：`ParameterOf`
- 产出信息：`DirectrixExpressionOf`
- 目录依赖：`Parabola_Equation_Standard_Right → Parabola_Equation_Standard_Left → Parabola_Equation_Standard_Up → Parabola_Equation_Standard_Down`
- Applicator 支持：`CONCRETE`
- 本题执行状态：`NO_MATCH`

#### 步骤 4：Parabola_Focal_Radius

- 具体公式/规则：$|PF|=x+p/2$
- 类别：`focal_radius`
- 所需对象类型：`Point`
- 所需信息：`PointOnCurve`
- 产出信息：`DistanceOf, EquationConstraint`
- 目录依赖：`Parabola_Definition → Parabola_Equation_Standard_Right → Parabola_Equation_Standard_Left → Parabola_Equation_Standard_Up → Parabola_Equation_Standard_Down`
- Applicator 支持：`CONCRETE`
- 本题执行状态：`NO_MATCH`

### 当前 Applicator 回放结果

- 能否完整执行：**否（存在失败步骤）**
- 最终答案：**未得到正确答案**
- 初始目标状态：`GOAL_UNSUPPORTED`
- 最终目标状态：`GOAL_UNSUPPORTED`
- Applicator 实际值：`None`
- 标注期望值：`None`
- 结果说明：query grammar is not supported
- 首个失败步骤：第 1 步
- 失败状态：`NO_MATCH`
- 缺失谓词：`无`
- 缺失对象类型：`无`

---

## 11. 题目 ID 1442

- 数据索引：1441
- V3 质量：C

### 题目

若焦点在$x$轴上的椭圆$\Gamma$: $\frac{x^{2}}{16}+\frac{y^{2}}{m}=1$的焦距为$2 \sqrt{7}$，则$m$的值为?

### 形式化信息

- 已知：`PointOnCurve(Focus(Gamma), xAxis);Gamma: Ellipse;Expression(Gamma) = (x^2/16 + y^2/m = 1);m: Number;FocalLength(Gamma) = 2*sqrt(7)`
- 查询：`m`
- 答案：`9`

### 解题过程

$由已知可得:2c=2\sqrt{7},所以c=\sqrt{7}又c^{2}=a2-b^{2}=16-m=7,所以m=9,$

### 定理内容序列

#### 步骤 1：Ellipse_Equation_Standard_X

- 具体公式/规则：$x^2/a^2+y^2/b^2=1$
- 类别：`standard_equation`
- 所需对象类型：`无`
- 所需信息：`ExpressionPolynomial`
- 产出信息：`ConicStandardForm, ParameterOf`
- 目录依赖：`无`
- Applicator 支持：`CONCRETE`
- 本题执行状态：`NO_MATCH`

#### 步骤 2：Ellipse_Parameter_Relation

- 具体公式/规则：$a^2=b^2+c^2$
- 类别：`parameter`
- 所需对象类型：`无`
- 所需信息：`ParameterOf`
- 产出信息：`ParameterOf, EquationConstraint`
- 目录依赖：`Ellipse_Equation_Standard_X → Ellipse_Equation_Standard_Y`
- Applicator 支持：`CONCRETE`
- 本题执行状态：`NO_MATCH`

### 当前 Applicator 回放结果

- 能否完整执行：**否（存在失败步骤）**
- 最终答案：**未得到正确答案**
- 初始目标状态：`GOAL_UNSUPPORTED`
- 最终目标状态：`GOAL_UNSUPPORTED`
- Applicator 实际值：`None`
- 标注期望值：`None`
- 结果说明：query grammar is not supported
- 首个失败步骤：第 1 步
- 失败状态：`NO_MATCH`
- 缺失谓词：`无`
- 缺失对象类型：`无`

---

## 12. 题目 ID 1747

- 数据索引：1746
- V3 质量：C

### 题目

若直线$y=2 x$与双曲线$\frac{x^{2}}{a^{2}}-\frac{y^{2}}{b^{2}}=1(a>0, b>0)$没有公共点，则该双曲线离心率的取值范围为?

### 形式化信息

- 已知：`H: Line;Expression(H) = (y = 2*x);G: Hyperbola;Expression(G) = (-y^2/b^2 + x^2/a^2 = 1);b: Number;a: Number;a>0;b>0;NumIntersection(H, G) = 0`
- 查询：`Range(Eccentricity(G))`
- 答案：`(1, sqrt(5)]`

### 解题过程

$由直线y=2x与双曲线\frac{x^{2}}{a^{2}}-\frac{y^{2}}{b^{2}}=1(a>0,b>0)没有公共点,分析出\frac{b}{a}\leqslant2,再求e的范围.[详解]\because双曲线\frac{x^{2}}{a^{2}}-\frac{y^{2}}{b^{2}}=1(a>0,b>0)的渐近线方程:y=\pm\frac{b}{a}x^{,}且直线y=2x与双曲线没有公共点,\therefore\frac{b}{a}\leqslant2即e=\sqrt{1+\frac{b^{2}}{a^{2}}}\leqslant\sqrt{5}又e>1,$

### 定理内容序列

#### 步骤 1：Hyperbola_Equation_Standard_X

- 具体公式/规则：$x^2/a^2-y^2/b^2=1$
- 类别：`standard_equation`
- 所需对象类型：`无`
- 所需信息：`ExpressionPolynomial`
- 产出信息：`ConicStandardForm, ParameterOf`
- 目录依赖：`无`
- Applicator 支持：`CONCRETE`
- 本题执行状态：`APPLIED`

#### 步骤 2：Hyperbola_Asymptote

- 具体公式/规则：$y=+/-(b/a)x$
- 类别：`asymptote`
- 所需对象类型：`Hyperbola`
- 所需信息：`ConicStandardForm`
- 产出信息：`AsymptoteFamilyOf, EquationConstraint`
- 目录依赖：`Hyperbola_Equation_Standard_X → Hyperbola_Equation_Standard_Y`
- Applicator 支持：`CONCRETE`
- 本题执行状态：`APPLIED`

#### 步骤 3：Hyperbola_Eccentricity_Range

- 具体公式/规则：$e>1$
- 类别：`parameter`
- 所需对象类型：`无`
- 所需信息：`ParameterOf`
- 产出信息：`ParameterOf, EquationConstraint`
- 目录依赖：`Eccentricity_Formula`
- Applicator 支持：`CONCRETE`
- 本题执行状态：`APPLIED`

### 当前 Applicator 回放结果

- 能否完整执行：**是（完整执行）**
- 最终答案：**未得到正确答案**
- 初始目标状态：`GOAL_UNSUPPORTED`
- 最终目标状态：`GOAL_UNSUPPORTED`
- Applicator 实际值：`None`
- 标注期望值：`None`
- 结果说明：query grammar is not supported

---

## 13. 题目 ID 2015

- 数据索引：2014
- V3 质量：C

### 题目

已知$F$是椭圆$\frac{x^{2}}{a^{2}}+\frac{y^{2}}{b^{2}}=1(a>b>0)$的左焦点，$A$为右顶点，$P$是椭圆上的一点，$P F \perp x$轴，若$|P F|=\frac{3}{4}|A F|$，则该椭圆的离心率是?

### 形式化信息

- 已知：`G: Ellipse;b: Number;a: Number;P: Point;F: Point;A:Point;a > b;b > 0;Expression(G) = (y^2/b^2 + x^2/a^2 = 1);LeftFocus(G) = F;RightVertex(G) = A;PointOnCurve(P, G);IsPerpendicular(LineSegmentOf(P,F),xAxis);Abs(LineSegmentOf(P,F))=(3/4)*Abs(LineSegmentOf(A,F))`
- 查询：`Eccentricity(G)`
- 答案：`1/4`

### 解题过程

$根据椭圆几何性质可知|PF|=\frac{b^{2}}{a},|AF|=a-c,所以\frac{b^{2}}{a}=\frac{3}{4}(a+c),即4b^{2}=3a^{2}-3ac,由因为b^{2}=a^{2}-c^{2},所以有4(a^{2}-c^{2})=3a^{2}+3ac,整理可得4c^{2}+3ac-a^{2}=0,两边同除以a2得:4e^{2}+3e-1=0,所以(4e-1)(e+1)=0,由于0<e<1,所以e=\frac{1}{4}$

### 定理内容序列

#### 步骤 1：Ellipse_Equation_Standard_X

- 具体公式/规则：$x^2/a^2+y^2/b^2=1$
- 类别：`standard_equation`
- 所需对象类型：`无`
- 所需信息：`ExpressionPolynomial`
- 产出信息：`ConicStandardForm, ParameterOf`
- 目录依赖：`无`
- Applicator 支持：`CONCRETE`
- 本题执行状态：`APPLIED`

#### 步骤 2：Vector_Perpendicular_Condition

- 具体公式/规则：$u dot v=0$
- 类别：`vector`
- 所需对象类型：`Vector`
- 所需信息：`VectorOf`
- 产出信息：`EquationConstraint`
- 目录依赖：`Vector_Dot_Product_Algebraic`
- Applicator 支持：`CONCRETE`
- 本题执行状态：`NO_MATCH`

#### 步骤 3：Pythagorean_Theorem

- 具体公式/规则：$a^2+b^2=c^2$
- 类别：`triangle`
- 所需对象类型：`Triangle`
- 所需信息：`TriangleOf`
- 产出信息：`EquationConstraint`
- 目录依赖：`无`
- Applicator 支持：`CONCRETE`
- 本题执行状态：`NO_MATCH`

#### 步骤 4：Homogenization_Eccentricity

- 具体公式/规则：$divide by a^2$
- 类别：`advanced`
- 所需对象类型：`无`
- 所需信息：`EquationConstraint`
- 产出信息：`EquationConstraint`
- 目录依赖：`Ellipse_Parameter_Relation → Hyperbola_Parameter_Relation → Eccentricity_Formula`
- Applicator 支持：`SPECIFICATION_ONLY`
- 本题执行状态：`SPECIFICATION_ONLY`

### 当前 Applicator 回放结果

- 能否完整执行：**否（存在失败步骤）**
- 最终答案：**未得到正确答案**
- 初始目标状态：`GOAL_NOT_REACHED`
- 最终目标状态：`GOAL_NOT_REACHED`
- Applicator 实际值：`None`
- 标注期望值：`None`
- 结果说明：无
- 首个失败步骤：第 2 步
- 失败状态：`NO_MATCH`
- 缺失谓词：`RequestedDotProductOf`
- 缺失对象类型：`Vector`

---

## 14. 题目 ID 2202

- 数据索引：2201
- V3 质量：C

### 题目

已知双曲线$\frac{x^{2}}{a^{2}}-\frac{y^{2}}{b^{2}}=1(a>0, b>0)$的离心率为$\frac{2 \sqrt{3}}{3}$，则该双曲线的渐近线方程为?

### 形式化信息

- 已知：`G: Hyperbola;Expression(G) = (-y^2/b^2 + x^2/a^2 = 1);b: Number;a: Number;a>0;b>0;Eccentricity(G) = (2*sqrt(3))/3`
- 查询：`Expression(Asymptote(G))`
- 答案：`y=pm*(sqrt(3)/3)*x`

### 解题过程

$\because双曲线\frac{x^{2}}{a^{2}}-\frac{y^{2}}{b^{2}}=1(a>0,b>0)的离心率为\frac{2\sqrt{3}}{3},即\frac{c}{a}=\frac{2\sqrt{3}}{3},所以\frac{c^{2}}{a^{2}}=\frac{4}{3},所以\frac{a2+b^{2}}{a^{2}}=\frac{4}{3},故\frac{b^{2}}{a^{2}}=\frac{1}{3},所以双曲线\frac{x^{2}}{a^{2}}-\frac{y^{2}}{b^{2}}=1(a>0,b>0)的渐近线的方程为y=\pm\frac{b}{a}x=\pm\frac{\sqrt{3}}{3}x$

### 定理内容序列

#### 步骤 1：Hyperbola_Equation_Standard_X

- 具体公式/规则：$x^2/a^2-y^2/b^2=1$
- 类别：`standard_equation`
- 所需对象类型：`无`
- 所需信息：`ExpressionPolynomial`
- 产出信息：`ConicStandardForm, ParameterOf`
- 目录依赖：`无`
- Applicator 支持：`CONCRETE`
- 本题执行状态：`APPLIED`

#### 步骤 2：Eccentricity_Formula

- 具体公式/规则：$e=c/a$
- 类别：`parameter`
- 所需对象类型：`无`
- 所需信息：`ParameterOf`
- 产出信息：`ParameterOf, EquationConstraint`
- 目录依赖：`Ellipse_Parameter_Relation → Hyperbola_Parameter_Relation`
- Applicator 支持：`CONCRETE`
- 本题执行状态：`NO_MATCH`

#### 步骤 3：Hyperbola_Asymptote

- 具体公式/规则：$y=+/-(b/a)x$
- 类别：`asymptote`
- 所需对象类型：`Hyperbola`
- 所需信息：`ConicStandardForm`
- 产出信息：`AsymptoteFamilyOf, EquationConstraint`
- 目录依赖：`Hyperbola_Equation_Standard_X → Hyperbola_Equation_Standard_Y`
- Applicator 支持：`CONCRETE`
- 本题执行状态：`APPLIED`

### 当前 Applicator 回放结果

- 能否完整执行：**否（存在失败步骤）**
- 最终答案：**未得到正确答案**
- 初始目标状态：`GOAL_NOT_REACHED`
- 最终目标状态：`VALUE_UNRESOLVED`
- Applicator 实际值：`{'__type__': 'LineEquationTarget', 'kind': 'asymptote', 'axis': 'y', 'value': {'__type__': 'Term', 'operator': 'abs', 'arguments': [{'__type__': 'Term', 'operator': 'sqrt_positive', 'arguments': [{'__type__': 'Term', 'operator': 'div', 'arguments': [{'__type__': 'Term', 'operator': 'mul', 'arguments': [{'__type__': 'Term', 'operator': 'symbol', 'arguments': ['b']}, {'__type__': 'Term', 'operator': 'symbol', 'arguments': ['b']}]}, {'__type__': 'Term', 'operator': 'mul', 'arguments': [{'__type__': 'Term', 'operator': 'symbol', 'arguments': ['a']}, {'__type__': 'Term', 'operator': 'symbol', 'arguments': ['a']}]}]}]}]}}`
- 标注期望值：`{'__type__': 'LineEquationTarget', 'kind': 'asymptote', 'axis': 'y', 'value': {'__type__': 'Term', 'operator': 'abs', 'arguments': [{'__type__': 'Term', 'operator': 'mul', 'arguments': [{'__type__': 'Fraction', 'numerator': 1, 'denominator': 3}, {'__type__': 'Term', 'operator': 'sqrt', 'arguments': [{'__type__': 'Fraction', 'numerator': 3, 'denominator': 1}]}]}]}}`
- 结果说明：无
- 首个失败步骤：第 2 步
- 失败状态：`NO_MATCH`
- 缺失谓词：`无`
- 缺失对象类型：`无`

---

## 15. 题目 ID 2383

- 数据索引：2382
- V3 质量：C

### 题目

已知双曲线$\frac{x^{2}}{4}-\frac{y^{2}}{12}=1$的左准线与$x$轴的交点为点$P$，则点$P$到其中一条渐近线的距离为?

### 形式化信息

- 已知：`G: Hyperbola;P: Point;Expression(G) = (x^2/4 - y^2/12 = 1);Intersection(LeftDirectrix(G), xAxis) = P`
- 查询：`Distance(P, OneOf(Asymptote(G)))`
- 答案：`sqrt(3)/2`

### 解题过程

$a=2,c=4,左准线方程为x=-\frac{a^{2}}{c}=-1所以P(-1,0),又渐近线方程为:\sqrt{3}x\pmy=0,所以P到渐近线的距离为d=\frac{|\sqrt{3}\pm0|}{\sqrt{3+1}}=\frac{\sqrt{3}}{2},填\frac{\sqrt{3}}{2}$

### 定理内容序列

#### 步骤 1：Hyperbola_Equation_Standard_X

- 具体公式/规则：$x^2/a^2-y^2/b^2=1$
- 类别：`standard_equation`
- 所需对象类型：`无`
- 所需信息：`ExpressionPolynomial`
- 产出信息：`ConicStandardForm, ParameterOf`
- 目录依赖：`无`
- Applicator 支持：`CONCRETE`
- 本题执行状态：`APPLIED`

#### 步骤 2：Hyperbola_Parameter_Relation

- 具体公式/规则：$c^2=a^2+b^2$
- 类别：`parameter`
- 所需对象类型：`无`
- 所需信息：`ParameterOf`
- 产出信息：`ParameterOf, EquationConstraint`
- 目录依赖：`Hyperbola_Equation_Standard_X → Hyperbola_Equation_Standard_Y`
- Applicator 支持：`CONCRETE`
- 本题执行状态：`APPLIED`

#### 步骤 3：Hyperbola_Directrix

- 具体公式/规则：$x=+/-a^2/c$
- 类别：`directrix`
- 所需对象类型：`无`
- 所需信息：`ParameterOf`
- 产出信息：`DirectrixExpressionOf`
- 目录依赖：`Hyperbola_Parameter_Relation → Eccentricity_Formula`
- Applicator 支持：`CONCRETE`
- 本题执行状态：`APPLIED`

#### 步骤 4：Hyperbola_Asymptote

- 具体公式/规则：$y=+/-(b/a)x$
- 类别：`asymptote`
- 所需对象类型：`Hyperbola`
- 所需信息：`ConicStandardForm`
- 产出信息：`AsymptoteFamilyOf, EquationConstraint`
- 目录依赖：`Hyperbola_Equation_Standard_X → Hyperbola_Equation_Standard_Y`
- Applicator 支持：`CONCRETE`
- 本题执行状态：`APPLIED`

#### 步骤 5：Point_To_Line_Distance

- 具体公式/规则：$d=|Ax0+By0+C|/sqrt(A^2+B^2)$
- 类别：`coordinate`
- 所需对象类型：`Point`
- 所需信息：`CoordinateOf`
- 产出信息：`CoordinateOf, DistanceOf, SlopeOf`
- 目录依赖：`无`
- Applicator 支持：`CONCRETE`
- 本题执行状态：`NO_MATCH`

### 当前 Applicator 回放结果

- 能否完整执行：**否（存在失败步骤）**
- 最终答案：**未得到正确答案**
- 初始目标状态：`GOAL_NOT_REACHED`
- 最终目标状态：`GOAL_NOT_REACHED`
- Applicator 实际值：`None`
- 标注期望值：`None`
- 结果说明：无
- 首个失败步骤：第 5 步
- 失败状态：`NO_MATCH`
- 缺失谓词：`PointPositionOf, LineNormalFormOf, RequestedPointLineDistanceOf`
- 缺失对象类型：`无`

---

## 16. 题目 ID 2384

- 数据索引：2383
- V3 质量：C

### 题目

已知双曲线的顶点在坐标轴，中心在原点，渐近线经过点$P(m, 2 m)(m \neq 0)$，则双曲线的离心率为?

### 形式化信息

- 已知：`G: Hyperbola;P: Point;O:Origin;PointOnCurve(Vertex(G),axis);Center(G)=O;Coordinate(P) = (m, 2*m);Negation(m=0);PointOnCurve(P,Asymptote(G));m:Number`
- 查询：`Eccentricity(G)`
- 答案：`{sqrt(5),sqrt(5)/2}`

### 解题过程

$分为焦点在x轴和y轴两种情况进行讨论,设出双曲线方程,求出渐近线方程,由渐近线经过点P(m,2m),求出a和b的关系,再利用c^{2}=a^{2}+b^{2}及e=\frac{c}{a}即可得解当焦点在x轴上时,设双曲线的方程为\frac{x^{2}}{a^{2}}-\frac{y^{2}}{b^{2}}=1(a>0,b>0),渐近线方程为y=\pm\frac{b}{a}x由渐近线经过点P(m,2m)(m\neq0),得2m=\frac{b}{a}m'解得b=2a.所以b^{2}=4a^{2},c^{2}=a^{2}+b^{2}=a^{2}+4a^{2}=5a^{2}双曲线的离心率e=\frac{c}{a}=\sqrt{5}当焦点在y轴上时,设双曲线的方程为\frac{y^{2}}{a^{2}}-\frac{x^{2}}{b^{2}}=1(a>0,b>0)渐近线方程为y=\pm\frac{a}{b}x,由渐近线经过点P(m,2m)(m\neq0),得2m=\frac{a}{b}m,解得b=\frac{1}{2}a.所以b^{2}=\frac{1}{4}a^{2},c^{2}=a^{2}+b^{2}=a^{2}+\frac{1}{4}a^{2}=\frac{5}{4}a^{2},双曲线的离心率e=\frac{c}{a}=\frac{\sqrt{5}}{2}综上,双曲线的离心率为\sqrt{5}或\frac{\sqrt{5}}{2}$

### 定理内容序列

#### 步骤 1：Hyperbola_Equation_Standard_X

- 具体公式/规则：$x^2/a^2-y^2/b^2=1$
- 类别：`standard_equation`
- 所需对象类型：`无`
- 所需信息：`ExpressionPolynomial`
- 产出信息：`ConicStandardForm, ParameterOf`
- 目录依赖：`无`
- Applicator 支持：`CONCRETE`
- 本题执行状态：`NO_MATCH`

#### 步骤 2：Hyperbola_Equation_Standard_Y

- 具体公式/规则：$y^2/a^2-x^2/b^2=1$
- 类别：`standard_equation`
- 所需对象类型：`无`
- 所需信息：`ExpressionPolynomial`
- 产出信息：`ConicStandardForm, ParameterOf`
- 目录依赖：`无`
- Applicator 支持：`CONCRETE`
- 本题执行状态：`NO_MATCH`

#### 步骤 3：Hyperbola_Asymptote

- 具体公式/规则：$y=+/-(b/a)x$
- 类别：`asymptote`
- 所需对象类型：`Hyperbola`
- 所需信息：`ConicStandardForm`
- 产出信息：`AsymptoteFamilyOf, EquationConstraint`
- 目录依赖：`Hyperbola_Equation_Standard_X → Hyperbola_Equation_Standard_Y`
- Applicator 支持：`CONCRETE`
- 本题执行状态：`NO_MATCH`

#### 步骤 4：Eccentricity_Formula

- 具体公式/规则：$e=c/a$
- 类别：`parameter`
- 所需对象类型：`无`
- 所需信息：`ParameterOf`
- 产出信息：`ParameterOf, EquationConstraint`
- 目录依赖：`Ellipse_Parameter_Relation → Hyperbola_Parameter_Relation`
- Applicator 支持：`CONCRETE`
- 本题执行状态：`NO_MATCH`

### 当前 Applicator 回放结果

- 能否完整执行：**否（存在失败步骤）**
- 最终答案：**未得到正确答案**
- 初始目标状态：`GOAL_NOT_REACHED`
- 最终目标状态：`GOAL_NOT_REACHED`
- Applicator 实际值：`None`
- 标注期望值：`None`
- 结果说明：无
- 首个失败步骤：第 1 步
- 失败状态：`NO_MATCH`
- 缺失谓词：`ExpressionPolynomial`
- 缺失对象类型：`无`

---

## 17. 题目 ID 2500

- 数据索引：2499
- V3 质量：C

### 题目

已知抛物线$C$: $y^{2}=4 x$的焦点为$F$、$O$是坐标原点,点$A$在抛物线$C$上，且$|A O|=|A F|$，则线段$A F$的长是?

### 形式化信息

- 已知：`C: Parabola;A: Point;F: Point;O: Origin;Expression(C) = (y^2 = 4*x);Focus(C)=F;PointOnCurve(A, C);Abs(LineSegmentOf(A, O)) = Abs(LineSegmentOf(A, F))`
- 查询：`Length(LineSegmentOf(A,F))`
- 答案：`3/2`

### 解题过程

$不妨设点A在x轴上方,则由|OF|=1知,x_{A}=\frac{1}{2}.所以y_{A}=\sqrt{2},即A(\frac{1}{2},\sqrt{2}).于是|AF|=|OA|=\sqrt{\frac{1}{4}+2}=\frac{3}{2}$

### 定理内容序列

#### 步骤 1：Parabola_Equation_Standard_Right

- 具体公式/规则：$y^2=2px$
- 类别：`standard_equation`
- 所需对象类型：`无`
- 所需信息：`ExpressionPolynomial`
- 产出信息：`ConicStandardForm, ParameterOf`
- 目录依赖：`无`
- Applicator 支持：`CONCRETE`
- 本题执行状态：`APPLIED`

#### 步骤 2：Parabola_Focal_Radius

- 具体公式/规则：$|PF|=x+p/2$
- 类别：`focal_radius`
- 所需对象类型：`Point`
- 所需信息：`PointOnCurve`
- 产出信息：`DistanceOf, EquationConstraint`
- 目录依赖：`Parabola_Definition → Parabola_Equation_Standard_Right → Parabola_Equation_Standard_Left → Parabola_Equation_Standard_Up → Parabola_Equation_Standard_Down`
- Applicator 支持：`CONCRETE`
- 本题执行状态：`APPLIED`

#### 步骤 3：Two_Points_Distance

- 具体公式/规则：$d=sqrt((x2-x1)^2+(y2-y1)^2)$
- 类别：`coordinate`
- 所需对象类型：`Point`
- 所需信息：`CoordinateOf`
- 产出信息：`CoordinateOf, DistanceOf, SlopeOf`
- 目录依赖：`无`
- Applicator 支持：`CONCRETE`
- 本题执行状态：`APPLIED`

### 当前 Applicator 回放结果

- 能否完整执行：**是（完整执行）**
- 最终答案：**未得到正确答案**
- 初始目标状态：`GOAL_UNSUPPORTED`
- 最终目标状态：`GOAL_UNSUPPORTED`
- Applicator 实际值：`None`
- 标注期望值：`None`
- 结果说明：query grammar is not supported

---

## 18. 题目 ID 2663

- 数据索引：2662
- V3 质量：C

### 题目

若抛物线$y^{2}=2 p x$的准线经过双曲线$x^{2}-\frac{y^{2}}{3}=1$的左焦点，则实数$p$=?

### 形式化信息

- 已知：`G: Hyperbola;H: Parabola;p: Real;Expression(G) = (x^2 - y^2/3 = 1);Expression(H) = (y^2 = 2*(p*x));PointOnCurve(LeftFocus(G), Directrix(H))`
- 查询：`p`
- 答案：`4`

### 解题过程

$双曲线x^{2}-\frac{y^{2}}{3}=1的右焦点为(-2,0),故抛物线y^{2}=2px的准线为x=-2,\therefore-\frac{p}{2}=-2,\thereforep=4,$

### 定理内容序列

#### 步骤 1：Hyperbola_Equation_Standard_X

- 具体公式/规则：$x^2/a^2-y^2/b^2=1$
- 类别：`standard_equation`
- 所需对象类型：`无`
- 所需信息：`ExpressionPolynomial`
- 产出信息：`ConicStandardForm, ParameterOf`
- 目录依赖：`无`
- Applicator 支持：`CONCRETE`
- 本题执行状态：`APPLIED`

#### 步骤 2：Parabola_Equation_Standard_Right

- 具体公式/规则：$y^2=2px$
- 类别：`standard_equation`
- 所需对象类型：`无`
- 所需信息：`ExpressionPolynomial`
- 产出信息：`ConicStandardForm, ParameterOf`
- 目录依赖：`无`
- Applicator 支持：`CONCRETE`
- 本题执行状态：`NO_MATCH`

#### 步骤 3：Parabola_Directrix

- 具体公式/规则：$x or y=+/-p/2$
- 类别：`directrix`
- 所需对象类型：`无`
- 所需信息：`ParameterOf`
- 产出信息：`DirectrixExpressionOf`
- 目录依赖：`Parabola_Equation_Standard_Right → Parabola_Equation_Standard_Left → Parabola_Equation_Standard_Up → Parabola_Equation_Standard_Down`
- Applicator 支持：`CONCRETE`
- 本题执行状态：`NO_MATCH`

### 当前 Applicator 回放结果

- 能否完整执行：**否（存在失败步骤）**
- 最终答案：**未得到正确答案**
- 初始目标状态：`GOAL_NOT_REACHED`
- 最终目标状态：`GOAL_NOT_REACHED`
- Applicator 实际值：`None`
- 标注期望值：`None`
- 结果说明：无
- 首个失败步骤：第 2 步
- 失败状态：`NO_MATCH`
- 缺失谓词：`无`
- 缺失对象类型：`无`

---

## 19. 题目 ID 2901

- 数据索引：2900
- V3 质量：D

### 题目

已知点$P$是双曲线$C$: $\frac{x^{2}}{a^{2}}-\frac{y^{2}}{b^{2}}=1(a>0, b>0)$左支上一点，$F_{1}$、$F_{2}$是双曲线的左、右焦点，且$\overrightarrow{P F_{1}} \cdot \overrightarrow{P F_{2}}=0$，若$P F_{2}$的中点$N$在第一象限，且$N$在双曲线的一条渐近线上，则双曲线的离心率是?

### 形式化信息

- 已知：`C: Hyperbola;b: Number;a: Number;P: Point;F2: Point;F1: Point;N: Point;a>0;b>0;Expression(C) = (-y^2/b^2 + x^2/a^2 = 1);PointOnCurve(P, LeftPart(C));LeftFocus(C) = F1;RightFocus(C) = F2;DotProduct(VectorOf(P, F1), VectorOf(P, F2)) = 0;MidPoint(LineSegmentOf(P, F2)) = N;Quadrant(N) = 1;PointOnCurve(N, OneOf(Asymptote(C)))`
- 查询：`Eccentricity(C)`
- 答案：`sqrt(5)`

### 解题过程

$由题意可设|PF_{1}|=m_{|}|PF_{2}|=n,由双曲线的定义可得n-m=2a\textcircled{1};设F_{1}(-c,0),F_{2}(c,0),由\overrightarrow{PF_{1}}\cdot\overrightarrow{PF_{2}}=0,可得三角形F_{1}PF_{2}是以P为直角顶点的三角形,即有m^{2}+n^{2}=4c^{2}\textcircled{2};直线ON的方程为y=\frac{b}{a}x,由题意可得在直角三角形ONF_{2}中,|ON|=\frac{1}{2}m|NF_{2}|=\frac{1}{2}n,即有\frac{b}{a}=\frac{n}{m}\textcircled{3};由\textcircled{1}\textcircled{3}可得m=\frac{2a^{2}}{b-a}n=\frac{2ab}{b-a},代入\textcircled{2}可得\frac{4a^{4}}{(b-a)^{2}}+\frac{4a2b^{2}}{(b-a)^{2}}=4c^{2},由c^{2}=a^{2}+b^{2},可化为a^{2}=(b-a)^{2},可得b=2a,c=\sqrt{a^{2}+b^{2}}=\sqrt{5}a,则e=\frac{c}{a}=\sqrt{5}$

### 定理内容序列

#### 步骤 1：Hyperbola_Equation_Standard_X

- 具体公式/规则：$x^2/a^2-y^2/b^2=1$
- 类别：`standard_equation`
- 所需对象类型：`无`
- 所需信息：`ExpressionPolynomial`
- 产出信息：`ConicStandardForm, ParameterOf`
- 目录依赖：`无`
- Applicator 支持：`CONCRETE`
- 本题执行状态：`APPLIED`

#### 步骤 2：Hyperbola_Definition

- 具体公式/规则：$||PF1|-|PF2||=2a$
- 类别：`definition`
- 所需对象类型：`无`
- 所需信息：`无`
- 产出信息：`DefinitionRelation`
- 目录依赖：`无`
- Applicator 支持：`CONCRETE`
- 本题执行状态：`NO_MATCH`

#### 步骤 3：Hyperbola_Asymptote

- 具体公式/规则：$y=+/-(b/a)x$
- 类别：`asymptote`
- 所需对象类型：`Hyperbola`
- 所需信息：`ConicStandardForm`
- 产出信息：`AsymptoteFamilyOf, EquationConstraint`
- 目录依赖：`Hyperbola_Equation_Standard_X → Hyperbola_Equation_Standard_Y`
- Applicator 支持：`CONCRETE`
- 本题执行状态：`APPLIED`

#### 步骤 4：Vector_Perpendicular_Condition

- 具体公式/规则：$u dot v=0$
- 类别：`vector`
- 所需对象类型：`Vector`
- 所需信息：`VectorOf`
- 产出信息：`EquationConstraint`
- 目录依赖：`Vector_Dot_Product_Algebraic`
- Applicator 支持：`CONCRETE`
- 本题执行状态：`APPLIED`

#### 步骤 5：Pythagorean_Theorem

- 具体公式/规则：$a^2+b^2=c^2$
- 类别：`triangle`
- 所需对象类型：`Triangle`
- 所需信息：`TriangleOf`
- 产出信息：`EquationConstraint`
- 目录依赖：`无`
- Applicator 支持：`CONCRETE`
- 本题执行状态：`NO_MATCH`

#### 步骤 6：Cosine_Law

- 具体公式/规则：$c^2=a^2+b^2-2ab*cos(C)$
- 类别：`triangle`
- 所需对象类型：`Triangle`
- 所需信息：`TriangleOf`
- 产出信息：`EquationConstraint`
- 目录依赖：`无`
- Applicator 支持：`CONCRETE`
- 本题执行状态：`NO_MATCH`

#### 步骤 7：Homogenization_Eccentricity

- 具体公式/规则：$divide by a^2$
- 类别：`advanced`
- 所需对象类型：`无`
- 所需信息：`EquationConstraint`
- 产出信息：`EquationConstraint`
- 目录依赖：`Ellipse_Parameter_Relation → Hyperbola_Parameter_Relation → Eccentricity_Formula`
- Applicator 支持：`SPECIFICATION_ONLY`
- 本题执行状态：`SPECIFICATION_ONLY`

#### 步骤 8：Eccentricity_Formula

- 具体公式/规则：$e=c/a$
- 类别：`parameter`
- 所需对象类型：`无`
- 所需信息：`ParameterOf`
- 产出信息：`ParameterOf, EquationConstraint`
- 目录依赖：`Ellipse_Parameter_Relation → Hyperbola_Parameter_Relation`
- Applicator 支持：`CONCRETE`
- 本题执行状态：`APPLIED`

### 当前 Applicator 回放结果

- 能否完整执行：**否（存在失败步骤）**
- 最终答案：**未得到正确答案**
- 初始目标状态：`GOAL_NOT_REACHED`
- 最终目标状态：`VALUE_UNRESOLVED`
- Applicator 实际值：`{'__type__': 'Term', 'operator': 'sqrt_positive', 'arguments': [{'__type__': 'Term', 'operator': 'add', 'arguments': [{'__type__': 'Fraction', 'numerator': 1, 'denominator': 1}, {'__type__': 'Term', 'operator': 'pow', 'arguments': [{'__type__': 'Term', 'operator': 'div', 'arguments': [{'__type__': 'Term', 'operator': 'mul', 'arguments': [{'__type__': 'Fraction', 'numerator': 1, 'denominator': 2}, {'__type__': 'Term', 'operator': 'symbol', 'arguments': ['__coord_P_y']}]}, {'__type__': 'Term', 'operator': 'mul', 'arguments': [{'__type__': 'Fraction', 'numerator': 1, 'denominator': 2}, {'__type__': 'Term', 'operator': 'add', 'arguments': [{'__type__': 'Term', 'operator': 'parameter', 'arguments': ['C', 'focal_half_distance']}, {'__type__': 'Term', 'operator': 'symbol', 'arguments': ['__coord_P_x']}]}]}]}, {'__type__': 'Fraction', 'numerator': 2, 'denominator': 1}]}]}]}`
- 标注期望值：`{'__type__': 'Term', 'operator': 'sqrt', 'arguments': [{'__type__': 'Fraction', 'numerator': 5, 'denominator': 1}]}`
- 结果说明：无
- 首个失败步骤：第 2 步
- 失败状态：`NO_MATCH`
- 缺失谓词：`无`
- 缺失对象类型：`无`

---

## 20. 题目 ID 3022

- 数据索引：3021
- V3 质量：D

### 题目

斜率为$-\frac{1}{3}$的直线$l$与椭圆$C$: $\frac{x^{2}}{a^{2}}+\frac{y^{2}}{b^{2}}=1 ( a>b>0)$相交于$A$、$B$两点，线段$A B$的中点坐标为$(1,1)$，则椭圆$C$的离心率等于?

### 形式化信息

- 已知：`l: Line;C: Ellipse;b: Number;a: Number;A: Point;B: Point;a > b;b > 0;Expression(C) = (y^2/b^2 + x^2/a^2 = 1);Slope(l) = -1/3;Intersection(l, C) = {A, B};Coordinate(MidPoint(LineSegmentOf(A,B))) = (1, 1)`
- 查询：`Eccentricity(C)`
- 答案：`sqrt(6)/3`

### 解题过程

$设A(x_{1},y_{1}),B(x_{2},y_{2}),则\frac{x_{1}^{2}}{a^{2}}+\frac{y_{1}^{2}}{b^{2}}=1\textcircled{1},\frac{x_{2}^{2}}{a^{2}}+\frac{y_{2}^{2}}{b^{2}}=1\textcircled{2}\because(1,1)是线段AB的中点,\frac{1}{2}(x_{1}+x_{2})=1,\frac{1}{2}(y_{1}+y_{2})=1,\because直线AB的方程是y=-\frac{1}{3}(x-1)+1,\thereforey_{1}-y_{2}=-\frac{1}{3}(x_{1}-x_{2}),\textcircled{1}\textcircled{2}两式相减可得:\frac{1}{a^{2}}(x_{1}^{2}-x_{2}^{2})+\frac{1}{b^{2}}(y_{1}^{2}-y_{2}^{2})=0,\therefore\frac{1}{a^{2}}(x_{1}-x_{2})(x_{1}+x_{2})+\frac{1}{b^{2}}(y_{1}-y_{2})(y_{1}+y_{2})=0,\therefore2\times\frac{1}{a^{2}}(x_{1}-x_{2})+2\times\frac{1}{b^{2}}(y_{1}-y_{2})=0,\therefore\frac{b^{2}}{a^{2}}=\frac{1}{3},\thereforee^{2}=1-\frac{b^{2}}{a^{2}}=\frac{2}{3}e=\frac{\sqrt{6}}{3}$

### 定理内容序列

#### 步骤 1：Ellipse_Equation_Standard_X

- 具体公式/规则：$x^2/a^2+y^2/b^2=1$
- 类别：`standard_equation`
- 所需对象类型：`无`
- 所需信息：`ExpressionPolynomial`
- 产出信息：`ConicStandardForm, ParameterOf`
- 目录依赖：`无`
- Applicator 支持：`CONCRETE`
- 本题执行状态：`APPLIED`

#### 步骤 2：Point_Difference_Method_Ellipse

- 具体公式/规则：$ellipse point-difference relation$
- 类别：`chord`
- 所需对象类型：`Point`
- 所需信息：`PointOnCurve`
- 产出信息：`EquationConstraint`
- 目录依赖：`Point_Difference_Method → Ellipse_Equation_Standard_X → Ellipse_Equation_Standard_Y`
- Applicator 支持：`CONCRETE`
- 本题执行状态：`APPLIED`

#### 步骤 3：Midpoint_Formula

- 具体公式/规则：$M=((x1+x2)/2,(y1+y2)/2)$
- 类别：`coordinate`
- 所需对象类型：`Point`
- 所需信息：`CoordinateOf`
- 产出信息：`CoordinateOf, DistanceOf, SlopeOf`
- 目录依赖：`无`
- Applicator 支持：`CONCRETE`
- 本题执行状态：`NO_MATCH`

#### 步骤 4：Slope_Formula

- 具体公式/规则：$k=(y2-y1)/(x2-x1)$
- 类别：`coordinate`
- 所需对象类型：`Point`
- 所需信息：`CoordinateOf`
- 产出信息：`CoordinateOf, DistanceOf, SlopeOf`
- 目录依赖：`无`
- Applicator 支持：`CONCRETE`
- 本题执行状态：`NO_MATCH`

#### 步骤 5：Line_Point_Slope_Form

- 具体公式/规则：$y-y0=k(x-x0)$
- 类别：`line`
- 所需对象类型：`Line`
- 所需信息：`CoordinateOf`
- 产出信息：`ExpressionOf`
- 目录依赖：`无`
- Applicator 支持：`CONCRETE`
- 本题执行状态：`NO_MATCH`

#### 步骤 6：Homogenization_Eccentricity

- 具体公式/规则：$divide by a^2$
- 类别：`advanced`
- 所需对象类型：`无`
- 所需信息：`EquationConstraint`
- 产出信息：`EquationConstraint`
- 目录依赖：`Ellipse_Parameter_Relation → Hyperbola_Parameter_Relation → Eccentricity_Formula`
- Applicator 支持：`SPECIFICATION_ONLY`
- 本题执行状态：`SPECIFICATION_ONLY`

#### 步骤 7：Eccentricity_Formula

- 具体公式/规则：$e=c/a$
- 类别：`parameter`
- 所需对象类型：`无`
- 所需信息：`ParameterOf`
- 产出信息：`ParameterOf, EquationConstraint`
- 目录依赖：`Ellipse_Parameter_Relation → Hyperbola_Parameter_Relation`
- Applicator 支持：`CONCRETE`
- 本题执行状态：`NO_MATCH`

### 当前 Applicator 回放结果

- 能否完整执行：**否（存在失败步骤）**
- 最终答案：**未得到正确答案**
- 初始目标状态：`GOAL_NOT_REACHED`
- 最终目标状态：`GOAL_NOT_REACHED`
- Applicator 实际值：`None`
- 标注期望值：`None`
- 结果说明：无
- 首个失败步骤：第 3 步
- 失败状态：`NO_MATCH`
- 缺失谓词：`PointPositionOf, MidPointOf`
- 缺失对象类型：`无`

---

## 21. 题目 ID 3169

- 数据索引：3168
- V3 质量：C

### 题目

已知抛物线$\Gamma$的方程为$y^{2}=6 x$，直线$l$经过抛物线的焦点且倾斜角为$120^{\circ}$，则抛物线$\Gamma$截直线$l$所得的弦长为?

### 形式化信息

- 已知：`Gamma: Parabola;Expression(Gamma) = (y^2 = 6*x);l: Line;PointOnCurve(Focus(Gamma), l);Inclination(l) = ApplyUnit(120, degree)`
- 查询：`Length(InterceptChord(l, Gamma))`
- 答案：`8`

### 解题过程

$由y^{2}=6x,可知抛物线的准线方程为x=-1.5,焦点F(1.5,0),p=3,\because直线l的倾斜角为120^{\circ},且直线l过点F(1.5,0),\therefore直线l的方程为y-0=-\tan60^{\circ}(x-1.5),即y=-\sqrt{3}x+\frac{3\sqrt{3}}{2}设A(x_{1},y_{1}),B(x_{2},y_{2}),联立直线与抛物线方程\begin{cases}y^{2}=6x\\y=-\sqrt{3}x+\frac{3\sqrt{3}}{2}\end{cases}化简整理可得4x^{2}-20x+9=0,所以x_{1}+x_{2}=5,由抛物线的定义可知,|AB|=p+x_{1}+x_{2}=8.$

### 定理内容序列

#### 步骤 1：Parabola_Equation_Standard_Right

- 具体公式/规则：$y^2=2px$
- 类别：`standard_equation`
- 所需对象类型：`无`
- 所需信息：`ExpressionPolynomial`
- 产出信息：`ConicStandardForm, ParameterOf`
- 目录依赖：`无`
- Applicator 支持：`CONCRETE`
- 本题执行状态：`APPLIED`

#### 步骤 2：Line_Point_Slope_Form

- 具体公式/规则：$y-y0=k(x-x0)$
- 类别：`line`
- 所需对象类型：`Line`
- 所需信息：`CoordinateOf`
- 产出信息：`ExpressionOf`
- 目录依赖：`无`
- Applicator 支持：`CONCRETE`
- 本题执行状态：`NO_MATCH`

#### 步骤 3：Vieta_Theorem_Sum

- 具体公式/规则：$x1+x2=-b/a$
- 类别：`algebra`
- 所需对象类型：`无`
- 所需信息：`QuadraticPolynomial`
- 产出信息：`EquationConstraint`
- 目录依赖：`Vieta_Theorem`
- Applicator 支持：`CONCRETE`
- 本题执行状态：`NO_MATCH`

#### 步骤 4：Parabola_Definition

- 具体公式/规则：$|PF|=distance(P,directrix)$
- 类别：`definition`
- 所需对象类型：`无`
- 所需信息：`无`
- 产出信息：`DefinitionRelation`
- 目录依赖：`无`
- Applicator 支持：`CONCRETE`
- 本题执行状态：`NO_MATCH`

#### 步骤 5：Parabola_Focal_Chord_Length

- 具体公式/规则：$|AB|=x1+x2+p$
- 类别：`focal_chord`
- 所需对象类型：`Parabola, Point`
- 所需信息：`PointOnCurve`
- 产出信息：`LengthOf, EquationConstraint`
- 目录依赖：`Parabola_Equation_Standard_Right → Parabola_Equation_Standard_Left → Parabola_Equation_Standard_Up → Parabola_Equation_Standard_Down`
- Applicator 支持：`CONCRETE`
- 本题执行状态：`NO_MATCH`

### 当前 Applicator 回放结果

- 能否完整执行：**否（存在失败步骤）**
- 最终答案：**未得到正确答案**
- 初始目标状态：`GOAL_UNSUPPORTED`
- 最终目标状态：`GOAL_UNSUPPORTED`
- Applicator 实际值：`None`
- 标注期望值：`None`
- 结果说明：query grammar is not supported
- 首个失败步骤：第 2 步
- 失败状态：`NO_MATCH`
- 缺失谓词：`SlopeOf`
- 缺失对象类型：`无`

---

## 22. 题目 ID 3235

- 数据索引：3234
- V3 质量：C

### 题目

已知双曲线$C$经过点$(3,2 \sqrt{2})$，渐近线方程为$y=\pm \frac{2}{3} x$，则双曲线的标准方程为?

### 形式化信息

- 已知：`C: Hyperbola;G: Point;Coordinate(G) = (3, 2*sqrt(2));PointOnCurve(G, C);Expression(Asymptote(C)) = (y = pm*(2/3)*x)`
- 查询：`Expression(C)`
- 答案：`y^2/4-x^2/9=1`

### 解题过程

$根据曲线的共渐近线双曲线系方程,可以设该双曲线的方程为\frac{x^{2}}{9}-\frac{y^{2}}{4}=\lambda(\lambda\neq0),将点(3,2\sqrt{2})带入可得\lambda=-1,所以所求的双曲线的方程为\frac{y^{2}}{4}-\frac{x^{2}}{9}=1$

### 定理内容序列

#### 步骤 1：Hyperbola_Equation_Standard_Y

- 具体公式/规则：$y^2/a^2-x^2/b^2=1$
- 类别：`standard_equation`
- 所需对象类型：`无`
- 所需信息：`ExpressionPolynomial`
- 产出信息：`ConicStandardForm, ParameterOf`
- 目录依赖：`无`
- Applicator 支持：`CONCRETE`
- 本题执行状态：`NO_MATCH`

#### 步骤 2：Hyperbola_Asymptote

- 具体公式/规则：$y=+/-(b/a)x$
- 类别：`asymptote`
- 所需对象类型：`Hyperbola`
- 所需信息：`ConicStandardForm`
- 产出信息：`AsymptoteFamilyOf, EquationConstraint`
- 目录依赖：`Hyperbola_Equation_Standard_X → Hyperbola_Equation_Standard_Y`
- Applicator 支持：`CONCRETE`
- 本题执行状态：`NO_MATCH`

#### 步骤 3：Hyperbola_Common_Asymptote_System

- 具体公式/规则：$x^2/a^2-y^2/b^2=lambda$
- 类别：`asymptote`
- 所需对象类型：`Hyperbola`
- 所需信息：`ConicStandardForm`
- 产出信息：`AsymptoteFamilyOf, EquationConstraint`
- 目录依赖：`Hyperbola_Asymptote`
- Applicator 支持：`CONCRETE`
- 本题执行状态：`NO_MATCH`

### 当前 Applicator 回放结果

- 能否完整执行：**否（存在失败步骤）**
- 最终答案：**未得到正确答案**
- 初始目标状态：`GOAL_NOT_REACHED`
- 最终目标状态：`GOAL_NOT_REACHED`
- Applicator 实际值：`None`
- 标注期望值：`None`
- 结果说明：无
- 首个失败步骤：第 1 步
- 失败状态：`NO_MATCH`
- 缺失谓词：`ExpressionPolynomial`
- 缺失对象类型：`无`

---

## 23. 题目 ID 3247

- 数据索引：3246
- V3 质量：C

### 题目

在$Rt \triangle A B C$中，$A B=A C=2$. 如果一个椭圆通过$A$、$B$两点，它的一个焦点为点$C$，另一个焦点在边$A B$上，则这个椭圆的焦距为?

### 形式化信息

- 已知：`G: Ellipse;A: Point;B: Point;C: Point;LineSegmentOf(A,B)=LineSegmentOf(A,C);LineSegmentOf(A,C)=2;PointOnCurve(A,G);PointOnCurve(B,G);OneOf(Focus(G))=C;F:Point;OneOf(Focus(G))=F;PointOnCurve(F, LineSegmentOf(A, B));Negation(C=F)`
- 查询：`FocalLength(G)`
- 答案：`sqrt(6)`

### 解题过程

$设另一个焦点为F,在Rt\botABC中,AB=AC=2,所以BC=2\sqrt{2},而AC+AF=BC+BF=2a,所以AC+AF+BC+BF=4+2\sqrt{2}=2a\Rightarrowa=2+\sqrt{2},又AC=2.所以AF=\sqrt{2},所以CF=\sqrt{2^{2}+2}=\sqrt{6},即椭圆的焦距为\sqrt{6}$

### 定理内容序列

#### 步骤 1：Ellipse_Equation_Standard_X

- 具体公式/规则：$x^2/a^2+y^2/b^2=1$
- 类别：`standard_equation`
- 所需对象类型：`无`
- 所需信息：`ExpressionPolynomial`
- 产出信息：`ConicStandardForm, ParameterOf`
- 目录依赖：`无`
- Applicator 支持：`CONCRETE`
- 本题执行状态：`NO_MATCH`

#### 步骤 2：Ellipse_Parameter_Relation

- 具体公式/规则：$a^2=b^2+c^2$
- 类别：`parameter`
- 所需对象类型：`无`
- 所需信息：`ParameterOf`
- 产出信息：`ParameterOf, EquationConstraint`
- 目录依赖：`Ellipse_Equation_Standard_X → Ellipse_Equation_Standard_Y`
- Applicator 支持：`CONCRETE`
- 本题执行状态：`NO_MATCH`

#### 步骤 3：Eccentricity_Formula

- 具体公式/规则：$e=c/a$
- 类别：`parameter`
- 所需对象类型：`无`
- 所需信息：`ParameterOf`
- 产出信息：`ParameterOf, EquationConstraint`
- 目录依赖：`Ellipse_Parameter_Relation → Hyperbola_Parameter_Relation`
- Applicator 支持：`CONCRETE`
- 本题执行状态：`NO_MATCH`

#### 步骤 4：Two_Points_Distance

- 具体公式/规则：$d=sqrt((x2-x1)^2+(y2-y1)^2)$
- 类别：`coordinate`
- 所需对象类型：`Point`
- 所需信息：`CoordinateOf`
- 产出信息：`CoordinateOf, DistanceOf, SlopeOf`
- 目录依赖：`无`
- Applicator 支持：`CONCRETE`
- 本题执行状态：`NO_MATCH`

### 当前 Applicator 回放结果

- 能否完整执行：**否（存在失败步骤）**
- 最终答案：**未得到正确答案**
- 初始目标状态：`GOAL_NOT_REACHED`
- 最终目标状态：`GOAL_NOT_REACHED`
- Applicator 实际值：`None`
- 标注期望值：`None`
- 结果说明：无
- 首个失败步骤：第 1 步
- 失败状态：`NO_MATCH`
- 缺失谓词：`ExpressionPolynomial`
- 缺失对象类型：`无`

---

## 24. 题目 ID 3553

- 数据索引：3552
- V3 质量：D

### 题目

过抛物线$y^{2}=2 p x(p<0)$的焦点$F$作两条互相垂直的弦$A B$ , $C D$，若$\triangle A C F$与$\triangle B D F$面积之和的最小值为$32$，则抛物线的方程为?

### 形式化信息

- 已知：`G: Parabola;Expression(G) = (y^2 = 2*p*x);p: Number;p<0;F: Point;Focus(G) = F;PointOnCurve(F, LineSegmentOf(A, B)) = True;PointOnCurve(F, LineSegmentOf(C, D)) = True;IsChordOf(LineSegmentOf(A, B), G)  = True;IsChordOf(LineSegmentOf(C, D), G) = True;IsPerpendicular(LineSegmentOf(A, B), LineSegmentOf(C, D)) = True;A: Point;B: Point;C: Point;D: Point;Min(Area(TriangleOf(A, C, F)) + Area(TriangleOf(B, D, F))) = 32`
- 查询：`Expression(G)`
- 答案：`y^2 = 8*x`

### 解题过程

$设直线AB和x轴的夹角为\theta,由焦半径公式得到\frac{p}{+\sin\theta}S_{\triangleBDF}=\frac{}{2(1+。}S=\frac{p^{2}}{2}[\frac{1}{(1-\cos\theta)(1+\sin\theta)}+\frac{1}{(1+\cos\theta)(1-\sin\theta)}\thereforeS=p^{2}\times\frac{1-\sin\theta\cos\theta}{\sin^{2}\theta\cos2\theta}=p^{2\times}\frac{1-\frac{1}{2}\sin2\theta}{\frac{1}{4}\sin^{2}2\theta}设t=\sin2\theta,\theta\in(0,\frac{\pi}{2})\cup(\frac{\pi}{2},\pi),t\in[-1,0)\cup(0,1]原式化简为S=p^{2}\times(\frac{4}{t^{2}}-\frac{2}{t}),\frac{1}{t}\in(-\infty,-1]\cup[1,+\infty)根据二次函数的性质当t=1时有最小值,此时S=2p^{2}=32,\thereforep=4抛物线方程为y^{2}=8x.$

### 定理内容序列

#### 步骤 1：Parabola_Equation_Standard_Right

- 具体公式/规则：$y^2=2px$
- 类别：`standard_equation`
- 所需对象类型：`无`
- 所需信息：`ExpressionPolynomial`
- 产出信息：`ConicStandardForm, ParameterOf`
- 目录依赖：`无`
- Applicator 支持：`CONCRETE`
- 本题执行状态：`NO_MATCH`

#### 步骤 2：Parabola_Focal_Radius

- 具体公式/规则：$|PF|=x+p/2$
- 类别：`focal_radius`
- 所需对象类型：`Point`
- 所需信息：`PointOnCurve`
- 产出信息：`DistanceOf, EquationConstraint`
- 目录依赖：`Parabola_Definition → Parabola_Equation_Standard_Right → Parabola_Equation_Standard_Left → Parabola_Equation_Standard_Up → Parabola_Equation_Standard_Down`
- Applicator 支持：`CONCRETE`
- 本题执行状态：`NO_MATCH`

#### 步骤 3：Parabola_Focal_Chord_Formula_Angle

- 具体公式/规则：$|AB|=2p/sin(theta)^2$
- 类别：`focal_chord`
- 所需对象类型：`Parabola, Point`
- 所需信息：`PointOnCurve`
- 产出信息：`LengthOf, EquationConstraint`
- 目录依赖：`Parabola_Focal_Chord_Length`
- Applicator 支持：`CONCRETE`
- 本题执行状态：`NO_MATCH`

#### 步骤 4：Triangle_Area_Formula

- 具体公式/规则：$S=base*height/2$
- 类别：`area`
- 所需对象类型：`无`
- 所需信息：`TriangleOf`
- 产出信息：`AreaOf`
- 目录依赖：`Point_To_Line_Distance`
- Applicator 支持：`CONCRETE`
- 本题执行状态：`NO_MATCH`

#### 步骤 5：Basic_Inequality

- 具体公式/规则：$a+b>=2sqrt(ab)$
- 类别：`inequality`
- 所需对象类型：`无`
- 所需信息：`OrderConstraint`
- 产出信息：`OrderConstraint`
- 目录依赖：`无`
- Applicator 支持：`SPECIFICATION_ONLY`
- 本题执行状态：`SPECIFICATION_ONLY`

### 当前 Applicator 回放结果

- 能否完整执行：**否（存在失败步骤）**
- 最终答案：**未得到正确答案**
- 初始目标状态：`GOAL_NOT_REACHED`
- 最终目标状态：`GOAL_NOT_REACHED`
- Applicator 实际值：`None`
- 标注期望值：`None`
- 结果说明：无
- 首个失败步骤：第 1 步
- 失败状态：`NO_MATCH`
- 缺失谓词：`无`
- 缺失对象类型：`无`

---

## 25. 题目 ID 3784

- 数据索引：3783
- V3 质量：C

### 题目

已知$P$是双曲线$\frac{x^{2}}{a^{2}}-\frac{y^{2}}{9}=1(a>0)$右支上的一点，双曲线的一条渐近线方程为$3 x-y=0$，设$F_{1}$、$F_{2}$分别为双曲线的左、右焦点.若$|P F_{2}|=3$，则$|P F_{1}|$=?

### 形式化信息

- 已知：`G: Hyperbola;Expression(G) = (-y^2/9 + x^2/a^2 = 1);a: Number;a>0;P: Point;PointOnCurve(P, RightPart(G));F1: Point;LeftFocus(G)=F1;F2: Point;RightFocus(G)=F2;Expression(OneOf(Asymptote(G)))= (3*x - y = 0);Abs(LineSegmentOf(P, F2)) = 3`
- 查询：`Abs(LineSegmentOf(P, F1))`
- 答案：`5`

### 解题过程

$因为双曲线的渐近线方程为3x-y=0,即y=3x=\frac{b}{a}所以\frac{3}{a}=3,解得a=1根据双曲线定义,P是双曲线\frac{x^{2}}{a^{2}}-\frac{y^{2}}{9}=1(a>0)右支上的一点满足|PF_{1}|-|PF_{2}|=2a=2所以|PF_{1}|=|PF_{2}|+2=5$

### 定理内容序列

#### 步骤 1：Hyperbola_Equation_Standard_X

- 具体公式/规则：$x^2/a^2-y^2/b^2=1$
- 类别：`standard_equation`
- 所需对象类型：`无`
- 所需信息：`ExpressionPolynomial`
- 产出信息：`ConicStandardForm, ParameterOf`
- 目录依赖：`无`
- Applicator 支持：`CONCRETE`
- 本题执行状态：`APPLIED`

#### 步骤 2：Hyperbola_Asymptote

- 具体公式/规则：$y=+/-(b/a)x$
- 类别：`asymptote`
- 所需对象类型：`Hyperbola`
- 所需信息：`ConicStandardForm`
- 产出信息：`AsymptoteFamilyOf, EquationConstraint`
- 目录依赖：`Hyperbola_Equation_Standard_X → Hyperbola_Equation_Standard_Y`
- Applicator 支持：`CONCRETE`
- 本题执行状态：`APPLIED`

#### 步骤 3：Point_To_Line_Distance

- 具体公式/规则：$d=|Ax0+By0+C|/sqrt(A^2+B^2)$
- 类别：`coordinate`
- 所需对象类型：`Point`
- 所需信息：`CoordinateOf`
- 产出信息：`CoordinateOf, DistanceOf, SlopeOf`
- 目录依赖：`无`
- Applicator 支持：`CONCRETE`
- 本题执行状态：`NO_MATCH`

### 当前 Applicator 回放结果

- 能否完整执行：**否（存在失败步骤）**
- 最终答案：**未得到正确答案**
- 初始目标状态：`GOAL_NOT_REACHED`
- 最终目标状态：`GOAL_NOT_REACHED`
- Applicator 实际值：`None`
- 标注期望值：`None`
- 结果说明：无
- 首个失败步骤：第 3 步
- 失败状态：`NO_MATCH`
- 缺失谓词：`LineNormalFormOf, RequestedPointLineDistanceOf`
- 缺失对象类型：`无`

---

## 26. 题目 ID 3894

- 数据索引：3893
- V3 质量：C

### 题目

已知双曲线$\frac{x^{2}}{a^{2}}-\frac{y^{2}}{b^{2}}=1(a>0, b>0)$与圆$x^{2}+y^{2}=b^{2}$在第二、四象限分别相交于两点$A$、$C$，点$F$是该双曲线的右焦点，且$|A F|=2|C F|$，则该双曲线的离心率为?

### 形式化信息

- 已知：`G: Hyperbola;Expression(G) = (-y^2/b^2 + x^2/a^2 = 1);b: Number;a: Number;a>0;b>0;H: Circle;Expression(H) = (x^2 + y^2 = b^2);Intersection(H,G) = {A,C};A: Point;C: Point;Quadrant(A) = 2;Quadrant(C) = 4;RightFocus(G) = F;F: Point;Abs(LineSegmentOf(A, F)) = 2*Abs(LineSegmentOf(C, F))`
- 查询：`Eccentricity(G)`
- 答案：`sqrt(22)/2`

### 解题过程

$双曲线的右焦点为F,左焦点为E,根据对称性可知AFCE是平行四边形,所以|AF|=2|CF|=2|AE|,又点A在双曲线上,所以|AF|-|AE|=2a,因为|AF|=2|CF|,所以|AF|-|AE|=2|CF|-|CF|=2a.所以|CF|=2a,在三角形OFC中,|FC|=2a,|OC|=b,|OF|=c,|AF|=4a可得16a^{2}=b^{2}+c^{2}-2bc\cos\angleAOF4a^{2}=b^{2}+c^{2}-2bc\cos\angleCOF可得20a^{2}=2b^{2}+2c^{2}=4c^{2}-2a^{2}.即:11a^{2}=2c^{2},所以双曲线的离心率为:e=\frac{\sqrt{22}}{2}$

### 定理内容序列

#### 步骤 1：Hyperbola_Equation_Standard_X

- 具体公式/规则：$x^2/a^2-y^2/b^2=1$
- 类别：`standard_equation`
- 所需对象类型：`无`
- 所需信息：`ExpressionPolynomial`
- 产出信息：`ConicStandardForm, ParameterOf`
- 目录依赖：`无`
- Applicator 支持：`CONCRETE`
- 本题执行状态：`APPLIED`

#### 步骤 2：Vector_Perpendicular_Condition

- 具体公式/规则：$u dot v=0$
- 类别：`vector`
- 所需对象类型：`Vector`
- 所需信息：`VectorOf`
- 产出信息：`EquationConstraint`
- 目录依赖：`Vector_Dot_Product_Algebraic`
- Applicator 支持：`CONCRETE`
- 本题执行状态：`NO_MATCH`

#### 步骤 3：Vector_Collinear_Condition

- 具体公式/规则：$u=lambda*v$
- 类别：`vector`
- 所需对象类型：`Vector`
- 所需信息：`VectorOf`
- 产出信息：`EquationConstraint`
- 目录依赖：`Vector_Dot_Product_Algebraic`
- Applicator 支持：`CONCRETE`
- 本题执行状态：`NO_MATCH`

#### 步骤 4：Eccentricity_Formula

- 具体公式/规则：$e=c/a$
- 类别：`parameter`
- 所需对象类型：`无`
- 所需信息：`ParameterOf`
- 产出信息：`ParameterOf, EquationConstraint`
- 目录依赖：`Ellipse_Parameter_Relation → Hyperbola_Parameter_Relation`
- Applicator 支持：`CONCRETE`
- 本题执行状态：`NO_MATCH`

### 当前 Applicator 回放结果

- 能否完整执行：**否（存在失败步骤）**
- 最终答案：**未得到正确答案**
- 初始目标状态：`GOAL_NOT_REACHED`
- 最终目标状态：`GOAL_NOT_REACHED`
- Applicator 实际值：`None`
- 标注期望值：`None`
- 结果说明：无
- 首个失败步骤：第 2 步
- 失败状态：`NO_MATCH`
- 缺失谓词：`RequestedDotProductOf`
- 缺失对象类型：`Vector`

---

## 27. 题目 ID 3926

- 数据索引：3925
- V3 质量：C

### 题目

已知两定点$P_{1}(-1 , 0)$和$P_{2}(3 , 0)$，则到点$P_{1}$和$P_{2}$的距离的平方和等于$16$的点的轨迹方程为?

### 形式化信息

- 已知：`P1: Point;P2: Point;Coordinate(P1) = (-1, 0);Coordinate(P2) = (3, 0);F: Point;(Distance(F, P1))^2 + (Distance(F, P2))^2 = 16`
- 查询：`LocusEquation(F)`
- 答案：`x^2+y^2-2*x-3=0`

### 解题过程

$设点P(x,y)到点口_{1}和口_{2}的距离的平方等于16,则PP_{1}^{2}+PP_{2}^{2}=(x+1)^{2}+y^{2}+(x-3)^{2}+y^{2}=16'整理得:x^{2}+y^{2}-2x-3=0.$

### 定理内容序列

#### 步骤 1：Circle_Standard_Equation

- 具体公式/规则：$(x-h)^2+(y-k)^2=r^2$
- 类别：`circle`
- 所需对象类型：`Circle`
- 所需信息：`ExpressionPolynomial`
- 产出信息：`CircleStandardForm, ParameterOf`
- 目录依赖：`无`
- Applicator 支持：`CONCRETE`
- 本题执行状态：`NO_MATCH`

#### 步骤 2：Two_Points_Distance

- 具体公式/规则：$d=sqrt((x2-x1)^2+(y2-y1)^2)$
- 类别：`coordinate`
- 所需对象类型：`Point`
- 所需信息：`CoordinateOf`
- 产出信息：`CoordinateOf, DistanceOf, SlopeOf`
- 目录依赖：`无`
- Applicator 支持：`CONCRETE`
- 本题执行状态：`NO_MATCH`

### 当前 Applicator 回放结果

- 能否完整执行：**否（存在失败步骤）**
- 最终答案：**未得到正确答案**
- 初始目标状态：`GOAL_UNSUPPORTED`
- 最终目标状态：`GOAL_UNSUPPORTED`
- Applicator 实际值：`None`
- 标注期望值：`None`
- 结果说明：query grammar is not supported
- 首个失败步骤：第 1 步
- 失败状态：`NO_MATCH`
- 缺失谓词：`ExpressionPolynomial`
- 缺失对象类型：`Circle`

---

## 28. 题目 ID 4372

- 数据索引：4371
- V3 质量：A

### 题目

椭圆$\frac{x^{2}}{9}+\frac{y^{2}}{4}=1$的长轴长为?

### 形式化信息

- 已知：`G: Ellipse;Expression(G) = (x^2/9 + y^2/4 = 1)`
- 查询：`Length(MajorAxis(G))`
- 答案：`6`

### 解题过程

$由题,a^{2}=9,即a=3,所以长轴长为2a=6,$

### 定理内容序列

#### 步骤 1：Ellipse_Equation_Standard_X

- 具体公式/规则：$x^2/a^2+y^2/b^2=1$
- 类别：`standard_equation`
- 所需对象类型：`无`
- 所需信息：`ExpressionPolynomial`
- 产出信息：`ConicStandardForm, ParameterOf`
- 目录依赖：`无`
- Applicator 支持：`CONCRETE`
- 本题执行状态：`APPLIED`

### 当前 Applicator 回放结果

- 能否完整执行：**是（完整执行）**
- 最终答案：**正确**
- 初始目标状态：`GOAL_NOT_REACHED`
- 最终目标状态：`ANSWER_CORRECT`
- Applicator 实际值：`{'__type__': 'Fraction', 'numerator': 6, 'denominator': 1}`
- 标注期望值：`{'__type__': 'Fraction', 'numerator': 6, 'denominator': 1}`
- 结果说明：无

---

## 29. 题目 ID 4606

- 数据索引：4605
- V3 质量：C

### 题目

已知点$P$为抛物线$y^{2}=8 x$上一点，设$P$到此抛物线的准线的距离为$d_{1}$，到直线$4 x+3 y+8=0$的距离为$d_{2}$，则$d_{1}+d_{2}$的最小值为?

### 形式化信息

- 已知：`G: Parabola;Expression(G) = (y^2 = 8*x);P: Point;PointOnCurve(P, G);d1: Number;d2: Number;H: Line;Expression(H) = (4*x + 3*y + 8 = 0);Distance(P, Directrix(G)) = d1;Distance(P, H) = d2`
- 查询：`Min(d1 + d2)`
- 答案：`16/5`

### 解题过程

$y^{2}=8x的焦点F(2,0),由抛物线定义可知P到此抛物线的准线的距离为d_{1}=PF,所以d_{1}+d_{2}的最小值为F到直线4x+3y+8=0的距离\therefored=\frac{|8+8|}{\sqrt{4^{2}+3^{2}}}=\frac{16}{5}$

### 定理内容序列

#### 步骤 1：Parabola_Equation_Standard_Right

- 具体公式/规则：$y^2=2px$
- 类别：`standard_equation`
- 所需对象类型：`无`
- 所需信息：`ExpressionPolynomial`
- 产出信息：`ConicStandardForm, ParameterOf`
- 目录依赖：`无`
- Applicator 支持：`CONCRETE`
- 本题执行状态：`APPLIED`

#### 步骤 2：Parabola_Definition

- 具体公式/规则：$|PF|=distance(P,directrix)$
- 类别：`definition`
- 所需对象类型：`无`
- 所需信息：`无`
- 产出信息：`DefinitionRelation`
- 目录依赖：`无`
- Applicator 支持：`CONCRETE`
- 本题执行状态：`NO_MATCH`

#### 步骤 3：Parabola_Directrix

- 具体公式/规则：$x or y=+/-p/2$
- 类别：`directrix`
- 所需对象类型：`无`
- 所需信息：`ParameterOf`
- 产出信息：`DirectrixExpressionOf`
- 目录依赖：`Parabola_Equation_Standard_Right → Parabola_Equation_Standard_Left → Parabola_Equation_Standard_Up → Parabola_Equation_Standard_Down`
- Applicator 支持：`CONCRETE`
- 本题执行状态：`APPLIED`

#### 步骤 4：Two_Points_Distance

- 具体公式/规则：$d=sqrt((x2-x1)^2+(y2-y1)^2)$
- 类别：`coordinate`
- 所需对象类型：`Point`
- 所需信息：`CoordinateOf`
- 产出信息：`CoordinateOf, DistanceOf, SlopeOf`
- 目录依赖：`无`
- Applicator 支持：`CONCRETE`
- 本题执行状态：`NO_MATCH`

### 当前 Applicator 回放结果

- 能否完整执行：**否（存在失败步骤）**
- 最终答案：**未得到正确答案**
- 初始目标状态：`GOAL_UNSUPPORTED`
- 最终目标状态：`GOAL_UNSUPPORTED`
- Applicator 实际值：`None`
- 标注期望值：`None`
- 结果说明：query grammar is not supported
- 首个失败步骤：第 2 步
- 失败状态：`NO_MATCH`
- 缺失谓词：`无`
- 缺失对象类型：`无`

---

## 30. 题目 ID 4831

- 数据索引：4830
- V3 质量：C

### 题目

已知$M(2,0)$, $P$是圆$N$: $x^{2}+4 x+y^{2}-32=0$上一动点，线段$M P$的垂直平分线交$N P$于点$Q$，则动点$Q$的轨迹方程为?

### 形式化信息

- 已知：`M: Point;Coordinate(M) = (2, 0);N: Circle;Expression(N) = (y^2 + x^2 + 4*x - 32 = 0);P: Point;PointOnCurve(P, N);Q: Point;Intersection(PerpendicularBisector(LineSegmentOf(M, P)), LineSegmentOf(N, P)) = Q`
- 查询：`LocusEquation(Q)`
- 答案：`x^2/9+y^2/5=1`

### 解题过程

$圆N:x^{2}+4x+y2-32=0可化为(x+2)^{2}+y^{2}=6^{2},所以N(-2,0),半径r=6,|MN|=4.依题意|QP|=|QM|,所以|QN|+|QM|=|QN|+|QP|=|NP|=6>|MN|.所以Q的轨迹为椭圆,2a=6,2c=4,a=3,c=2,b=\sqrt{a^{2}-c^{2}}=\sqrt{\frac{}{1}}所以动点Q的轨迹方程为\frac{x^{2}}{9}+\frac{y^{2}}{5}=1$

### 定理内容序列

#### 步骤 1：Ellipse_Equation_Standard_X

- 具体公式/规则：$x^2/a^2+y^2/b^2=1$
- 类别：`standard_equation`
- 所需对象类型：`无`
- 所需信息：`ExpressionPolynomial`
- 产出信息：`ConicStandardForm, ParameterOf`
- 目录依赖：`无`
- Applicator 支持：`CONCRETE`
- 本题执行状态：`NO_MATCH`

#### 步骤 2：Circle_Standard_Equation

- 具体公式/规则：$(x-h)^2+(y-k)^2=r^2$
- 类别：`circle`
- 所需对象类型：`Circle`
- 所需信息：`ExpressionPolynomial`
- 产出信息：`CircleStandardForm, ParameterOf`
- 目录依赖：`无`
- Applicator 支持：`CONCRETE`
- 本题执行状态：`APPLIED`

#### 步骤 3：Ellipse_Definition

- 具体公式/规则：$|PF1|+|PF2|=2a$
- 类别：`definition`
- 所需对象类型：`无`
- 所需信息：`无`
- 产出信息：`DefinitionRelation`
- 目录依赖：`无`
- Applicator 支持：`CONCRETE`
- 本题执行状态：`NO_MATCH`

#### 步骤 4：Pythagorean_Theorem

- 具体公式/规则：$a^2+b^2=c^2$
- 类别：`triangle`
- 所需对象类型：`Triangle`
- 所需信息：`TriangleOf`
- 产出信息：`EquationConstraint`
- 目录依赖：`无`
- Applicator 支持：`CONCRETE`
- 本题执行状态：`NO_MATCH`

### 当前 Applicator 回放结果

- 能否完整执行：**否（存在失败步骤）**
- 最终答案：**未得到正确答案**
- 初始目标状态：`GOAL_UNSUPPORTED`
- 最终目标状态：`GOAL_UNSUPPORTED`
- Applicator 实际值：`None`
- 标注期望值：`None`
- 结果说明：query grammar is not supported
- 首个失败步骤：第 1 步
- 失败状态：`NO_MATCH`
- 缺失谓词：`无`
- 缺失对象类型：`无`

---

## 31. 题目 ID 5039

- 数据索引：5038
- V3 质量：C

### 题目

设抛物线$y^{2}=2 p x(p>0)$上一点$P(2, m)$到$y$轴的距离是到焦点距离的一半，则抛物线的标准方程为?

### 形式化信息

- 已知：`G: Parabola;p: Number;P: Point;m:Number;p>0;Expression(G) = (y^2 = 2*(p*x));Coordinate(P) = (2, m);PointOnCurve(P,G);Distance(P,yAxis)=Distance(P,Focus(G))/2`
- 查询：`Expression(G)`
- 答案：`y^2=8*x`

### 解题过程

$由题意可得2+\frac{p}{2}=2\times2,解得p=4,故该抛物线的标准方程为y^{2}=8x$

### 定理内容序列

#### 步骤 1：Parabola_Equation_Standard_Right

- 具体公式/规则：$y^2=2px$
- 类别：`standard_equation`
- 所需对象类型：`无`
- 所需信息：`ExpressionPolynomial`
- 产出信息：`ConicStandardForm, ParameterOf`
- 目录依赖：`无`
- Applicator 支持：`CONCRETE`
- 本题执行状态：`APPLIED`

#### 步骤 2：Parabola_Definition

- 具体公式/规则：$|PF|=distance(P,directrix)$
- 类别：`definition`
- 所需对象类型：`无`
- 所需信息：`无`
- 产出信息：`DefinitionRelation`
- 目录依赖：`无`
- Applicator 支持：`CONCRETE`
- 本题执行状态：`NO_MATCH`

#### 步骤 3：Parabola_Directrix

- 具体公式/规则：$x or y=+/-p/2$
- 类别：`directrix`
- 所需对象类型：`无`
- 所需信息：`ParameterOf`
- 产出信息：`DirectrixExpressionOf`
- 目录依赖：`Parabola_Equation_Standard_Right → Parabola_Equation_Standard_Left → Parabola_Equation_Standard_Up → Parabola_Equation_Standard_Down`
- Applicator 支持：`CONCRETE`
- 本题执行状态：`APPLIED`

### 当前 Applicator 回放结果

- 能否完整执行：**否（存在失败步骤）**
- 最终答案：**未得到正确答案**
- 初始目标状态：`GOAL_NOT_REACHED`
- 最终目标状态：`VALUE_UNRESOLVED`
- Applicator 实际值：`{'__type__': 'StandardConicForm', 'curve_type': 'parabola', 'orientation': 'right', 'a2': None, 'b2': None, 'two_p': {'__type__': 'Term', 'operator': 'mul', 'arguments': [{'__type__': 'Fraction', 'numerator': 2, 'denominator': 1}, {'__type__': 'Term', 'operator': 'symbol', 'arguments': ['p']}]}, 'focus_offset': {'__type__': 'Term', 'operator': 'mul', 'arguments': [{'__type__': 'Fraction', 'numerator': 1, 'denominator': 2}, {'__type__': 'Term', 'operator': 'symbol', 'arguments': ['p']}]}}`
- 标注期望值：`{'__type__': 'PolynomialEquation', 'x2': 0, 'xy': 0, 'y2': {'__type__': 'Fraction', 'numerator': 1, 'denominator': 1}, 'x': {'__type__': 'Fraction', 'numerator': -8, 'denominator': 1}, 'y': 0, 'constant': 0}`
- 结果说明：无
- 首个失败步骤：第 2 步
- 失败状态：`NO_MATCH`
- 缺失谓词：`无`
- 缺失对象类型：`无`

---

## 32. 题目 ID 5055

- 数据索引：5054
- V3 质量：C

### 题目

已知抛物线$H$:$ 4x^{2}=y $的准线$l$与双曲线$C$: $\frac{x^{2}}{a^{2}}-\frac{y^{2}}{b^{2}}=1(a>0, b>0)$的渐近线交于$A$、$B$两点，若$|A B|=\frac{1}{8}$, 则双曲线$C$的离心率$e$=?

### 形式化信息

- 已知：`C: Hyperbola;b: Number;a: Number;H: Parabola;A: Point;B: Point;e: Number;l:Line;a>0;b>0;Expression(C) = (-y^2/b^2 + x^2/a^2 = 1);Expression(H) = (4*x^2=y);Directrix(H)=l;Intersection(l,Asymptote(C))={A, B};Abs(LineSegmentOf(A, B)) = 1/8;Eccentricity(C)=e`
- 查询：`e`
- 答案：`sqrt(2)`

### 解题过程

$已知抛物线H:4x^{2}=y即x^{2}=\frac{1}{4}y的准线l为y=\frac{1}{16}与双曲线C:\frac{x^{2}}{a^{2}}-\frac{y^{2}}{b^{2}}=1(a>0,b>0)的渐近线方程为y=\pm\frac{b}{a}x'当y=\frac{1}{16}时x=\pm\frac{a}{16b},又因为|AB|=\frac{1}{8},所以\frac{a}{8b}=\frac{1}{8},\thereforea=b,c^{2}=a^{2}+b^{2}=2a^{2},所以c=\sqrt{2}a则双曲线C的离心率e==\frac{c}{a}=\sqrt{2}$

### 定理内容序列

#### 步骤 1：Parabola_Equation_Standard_Up

- 具体公式/规则：$x^2=2py$
- 类别：`standard_equation`
- 所需对象类型：`无`
- 所需信息：`ExpressionPolynomial`
- 产出信息：`ConicStandardForm, ParameterOf`
- 目录依赖：`无`
- Applicator 支持：`CONCRETE`
- 本题执行状态：`APPLIED`

#### 步骤 2：Parabola_Directrix

- 具体公式/规则：$x or y=+/-p/2$
- 类别：`directrix`
- 所需对象类型：`无`
- 所需信息：`ParameterOf`
- 产出信息：`DirectrixExpressionOf`
- 目录依赖：`Parabola_Equation_Standard_Right → Parabola_Equation_Standard_Left → Parabola_Equation_Standard_Up → Parabola_Equation_Standard_Down`
- Applicator 支持：`CONCRETE`
- 本题执行状态：`APPLIED`

#### 步骤 3：Hyperbola_Equation_Standard_X

- 具体公式/规则：$x^2/a^2-y^2/b^2=1$
- 类别：`standard_equation`
- 所需对象类型：`无`
- 所需信息：`ExpressionPolynomial`
- 产出信息：`ConicStandardForm, ParameterOf`
- 目录依赖：`无`
- Applicator 支持：`CONCRETE`
- 本题执行状态：`APPLIED`

#### 步骤 4：Hyperbola_Asymptote

- 具体公式/规则：$y=+/-(b/a)x$
- 类别：`asymptote`
- 所需对象类型：`Hyperbola`
- 所需信息：`ConicStandardForm`
- 产出信息：`AsymptoteFamilyOf, EquationConstraint`
- 目录依赖：`Hyperbola_Equation_Standard_X → Hyperbola_Equation_Standard_Y`
- Applicator 支持：`CONCRETE`
- 本题执行状态：`APPLIED`

#### 步骤 5：Eccentricity_Formula

- 具体公式/规则：$e=c/a$
- 类别：`parameter`
- 所需对象类型：`无`
- 所需信息：`ParameterOf`
- 产出信息：`ParameterOf, EquationConstraint`
- 目录依赖：`Ellipse_Parameter_Relation → Hyperbola_Parameter_Relation`
- Applicator 支持：`CONCRETE`
- 本题执行状态：`NO_MATCH`

### 当前 Applicator 回放结果

- 能否完整执行：**否（存在失败步骤）**
- 最终答案：**未得到正确答案**
- 初始目标状态：`GOAL_NOT_REACHED`
- 最终目标状态：`GOAL_NOT_REACHED`
- Applicator 实际值：`None`
- 标注期望值：`None`
- 结果说明：无
- 首个失败步骤：第 5 步
- 失败状态：`NO_MATCH`
- 缺失谓词：`无`
- 缺失对象类型：`无`

---

## 33. 题目 ID 5069

- 数据索引：5068
- V3 质量：D

### 题目

直线$y=k x+1$被椭圆$\frac{x^{2}}{a^{2}}+y^{2}=1(a>1)$截得的线段长为 （用$a$ , $k$表示）?

### 形式化信息

- 已知：`G: Ellipse;a: Number;H: Line;k: Number;a>1;Expression(G) = (y^2 + x^2/a^2 = 1);Expression(H) = (y = k*x + 1)`
- 查询：`Length(InterceptChord(H, G))`
- 答案：`(2*a^2*Abs(k)/(1 + a^2*k^2))*sqrt(1 + k^2)`

### 解题过程

$联立方程组,按照k\neq0、k=0分类,结合韦达定理、弦长公式即可得解由题意\begin{cases}\frac{x^{2}}{a^{2}}+y^{2}=1\\y=kx+1\end{cases},化简得(1+a2k^{2})x^{2}+2ka^{2}x=0,当k\neq0时,A>0,设交点坐标分别为(x_{1},y_{1}),(x_{2},y_{2})则x_{1}+x_{2}=-\frac{2ka^{2}}{1+a2k^{2}},x_{1}x_{2}=0,此时截得的线段长为\sqrt{1+k^{2}}|x_{1}-x_{2}|=\sqrt{1+k^{2}}\sqrt{(x_{1}+x_{2})^{2}-}\frac{2a^{2}|k|}{4x_{1}x_{2}}=\frac{2a_{1}+a^{2}k^{2}}{\sqrt{1+k^{2}}}当k=0时,截得的线段长为0,满足上式;综上,直线y=kx+1被椭圆\frac{x^{2}}{a^{2}}+y^{2}=1(a>1)截得的线段长为\frac{2a^{2}|k|}{1+a2k^{2}}\sqrt{1+k^{2}}$

### 定理内容序列

#### 步骤 1：Ellipse_Equation_Standard_X

- 具体公式/规则：$x^2/a^2+y^2/b^2=1$
- 类别：`standard_equation`
- 所需对象类型：`无`
- 所需信息：`ExpressionPolynomial`
- 产出信息：`ConicStandardForm, ParameterOf`
- 目录依赖：`无`
- Applicator 支持：`CONCRETE`
- 本题执行状态：`NO_MATCH`

#### 步骤 2：Point_Difference_Method_Hyperbola

- 具体公式/规则：$hyperbola point-difference relation$
- 类别：`chord`
- 所需对象类型：`Point`
- 所需信息：`PointOnCurve`
- 产出信息：`EquationConstraint`
- 目录依赖：`Point_Difference_Method → Hyperbola_Equation_Standard_X → Hyperbola_Equation_Standard_Y`
- Applicator 支持：`CONCRETE`
- 本题执行状态：`NO_MATCH`

#### 步骤 3：Line_Point_Slope_Form

- 具体公式/规则：$y-y0=k(x-x0)$
- 类别：`line`
- 所需对象类型：`Line`
- 所需信息：`CoordinateOf`
- 产出信息：`ExpressionOf`
- 目录依赖：`无`
- Applicator 支持：`CONCRETE`
- 本题执行状态：`NO_MATCH`

#### 步骤 4：Vieta_Theorem_Sum

- 具体公式/规则：$x1+x2=-b/a$
- 类别：`algebra`
- 所需对象类型：`无`
- 所需信息：`QuadraticPolynomial`
- 产出信息：`EquationConstraint`
- 目录依赖：`Vieta_Theorem`
- Applicator 支持：`CONCRETE`
- 本题执行状态：`NO_MATCH`

#### 步骤 5：Vieta_Theorem_Product

- 具体公式/规则：$x1*x2=c/a$
- 类别：`algebra`
- 所需对象类型：`无`
- 所需信息：`QuadraticPolynomial`
- 产出信息：`EquationConstraint`
- 目录依赖：`Vieta_Theorem`
- Applicator 支持：`CONCRETE`
- 本题执行状态：`NO_MATCH`

#### 步骤 6：Chord_Length_Formula_With_K

- 具体公式/规则：$|AB|=|x1-x2|*sqrt(1+k^2)$
- 类别：`chord`
- 所需对象类型：`Point`
- 所需信息：`PointOnCurve`
- 产出信息：`EquationConstraint`
- 目录依赖：`Slope_Formula`
- Applicator 支持：`CONCRETE`
- 本题执行状态：`NO_MATCH`

#### 步骤 7：Triangle_Midline_Theorem

- 具体公式/规则：$midline=base/2$
- 类别：`midline`
- 所需对象类型：`无`
- 所需信息：`MidpointOf`
- 产出信息：`LengthOf`
- 目录依赖：`无`
- Applicator 支持：`SPECIFICATION_ONLY`
- 本题执行状态：`SPECIFICATION_ONLY`

### 当前 Applicator 回放结果

- 能否完整执行：**否（存在失败步骤）**
- 最终答案：**未得到正确答案**
- 初始目标状态：`GOAL_UNSUPPORTED`
- 最终目标状态：`GOAL_UNSUPPORTED`
- Applicator 实际值：`None`
- 标注期望值：`None`
- 结果说明：query grammar is not supported
- 首个失败步骤：第 1 步
- 失败状态：`NO_MATCH`
- 缺失谓词：`无`
- 缺失对象类型：`无`

---

## 34. 题目 ID 5257

- 数据索引：5256
- V3 质量：C

### 题目

已知双曲线的焦点到其渐近线的距离等于双曲线的实轴长，则该双曲线的渐近线方程为?

### 形式化信息

- 已知：`G: Hyperbola;Distance(Focus(G), Asymptote(G)) = Length(RealAxis(G))`
- 查询：`Expression(Asymptote(G))`
- 答案：`{y=pm*2*x, y=pm*(1/2)*x}`

### 解题过程

$讨论双曲线的焦点在x轴或y轴上,求得焦点坐标和渐近线方程,由题意可得a,b的关系,进而得到所求双曲线的渐近线方程.当焦点在x轴上的双曲线方程设为\frac{x^{2}}{a^{2}}-\frac{y^{2}}{b^{2}}=1(a,b>0)渐近线方程为bx\pmay=0,焦点为(\pmc,0)可得焦点到渐近线的距离为\frac{bc}{\sqrt{b^{2}+a^{2}}}=b=2a则所求渐近线方程为y=\pm2x;当焦点在y轴上的双曲线方程设为\frac{y^{2}}{a^{2}}-\frac{x^{2}}{b^{2}}=1(a,b>0)渐近线方程为by\pmax=0,焦点为(0,\pmc)可得焦点到渐近线的距离为\frac{bc}{\sqrt{b^{2}+a^{2}}}=b=2a则所求渐近线方程为y=\pm\frac{1}{2}x;综上可得,渐近线方程为y=\pm2x或y=\pm\frac{1}{2}x$

### 定理内容序列

#### 步骤 1：Hyperbola_Equation_Standard_Y

- 具体公式/规则：$y^2/a^2-x^2/b^2=1$
- 类别：`standard_equation`
- 所需对象类型：`无`
- 所需信息：`ExpressionPolynomial`
- 产出信息：`ConicStandardForm, ParameterOf`
- 目录依赖：`无`
- Applicator 支持：`CONCRETE`
- 本题执行状态：`NO_MATCH`

#### 步骤 2：Hyperbola_Asymptote

- 具体公式/规则：$y=+/-(b/a)x$
- 类别：`asymptote`
- 所需对象类型：`Hyperbola`
- 所需信息：`ConicStandardForm`
- 产出信息：`AsymptoteFamilyOf, EquationConstraint`
- 目录依赖：`Hyperbola_Equation_Standard_X → Hyperbola_Equation_Standard_Y`
- Applicator 支持：`CONCRETE`
- 本题执行状态：`NO_MATCH`

#### 步骤 3：Point_To_Line_Distance

- 具体公式/规则：$d=|Ax0+By0+C|/sqrt(A^2+B^2)$
- 类别：`coordinate`
- 所需对象类型：`Point`
- 所需信息：`CoordinateOf`
- 产出信息：`CoordinateOf, DistanceOf, SlopeOf`
- 目录依赖：`无`
- Applicator 支持：`CONCRETE`
- 本题执行状态：`NO_MATCH`

#### 步骤 4：Hyperbola_Parameter_Relation

- 具体公式/规则：$c^2=a^2+b^2$
- 类别：`parameter`
- 所需对象类型：`无`
- 所需信息：`ParameterOf`
- 产出信息：`ParameterOf, EquationConstraint`
- 目录依赖：`Hyperbola_Equation_Standard_X → Hyperbola_Equation_Standard_Y`
- Applicator 支持：`CONCRETE`
- 本题执行状态：`NO_MATCH`

### 当前 Applicator 回放结果

- 能否完整执行：**否（存在失败步骤）**
- 最终答案：**未得到正确答案**
- 初始目标状态：`GOAL_NOT_REACHED`
- 最终目标状态：`GOAL_NOT_REACHED`
- Applicator 实际值：`None`
- 标注期望值：`None`
- 结果说明：无
- 首个失败步骤：第 1 步
- 失败状态：`NO_MATCH`
- 缺失谓词：`ExpressionPolynomial`
- 缺失对象类型：`无`

---

## 35. 题目 ID 5360

- 数据索引：5359
- V3 质量：C

### 题目

以抛物线$y^{2}=2 p x(p>0)$焦点$F$为端点的一条射线交抛物线于点$A$，交$y$轴于点$B$，若$|A F|=2$, $|B F|=3$，则$p$=?

### 形式化信息

- 已知：`G: Parabola;Expression(G) = (y^2 = 2*(p*x));p: Number;p>0;F: Point;Focus(G) = F;Endpoint(Z) = F;A: Point;Intersection(Z, G) = A;B: Point;Intersection(Z, yAxis) = B;Abs(LineSegmentOf(A, F)) = 2;Abs(LineSegmentOf(B, F)) = 3;Z: Ray`
- 查询：`p`
- 答案：`3`

### 解题过程

$依题意可得F(\frac{p}{2},0),设A(x_{1},y_{1}),则|AF|=x_{1}+\frac{p}{2}=2,因为|AF|=2,|BF|=3,所以|AB|=|BF|-|AF|=3-2=1,所以\frac{|AB|}{|BF|}=\frac{1}{3},又\frac{|AB|}{|BF|}=\frac{x_{1}}{\frac{P}{2}}=\frac{2x_{1}}{P}所以\frac{2x_{1}}{p}=\frac{1}{3},所以p=6x_{1},所以x_{1}+\frac{6x_{1}}{2}=2,解得x_{1}=\frac{1}{2},所以p=6x_{1}=6\times\frac{1}{2}=3.$

### 定理内容序列

#### 步骤 1：Parabola_Equation_Standard_Right

- 具体公式/规则：$y^2=2px$
- 类别：`standard_equation`
- 所需对象类型：`无`
- 所需信息：`ExpressionPolynomial`
- 产出信息：`ConicStandardForm, ParameterOf`
- 目录依赖：`无`
- Applicator 支持：`CONCRETE`
- 本题执行状态：`APPLIED`

#### 步骤 2：Parabola_Definition

- 具体公式/规则：$|PF|=distance(P,directrix)$
- 类别：`definition`
- 所需对象类型：`无`
- 所需信息：`无`
- 产出信息：`DefinitionRelation`
- 目录依赖：`无`
- Applicator 支持：`CONCRETE`
- 本题执行状态：`NO_MATCH`

#### 步骤 3：Parabola_Focal_Radius

- 具体公式/规则：$|PF|=x+p/2$
- 类别：`focal_radius`
- 所需对象类型：`Point`
- 所需信息：`PointOnCurve`
- 产出信息：`DistanceOf, EquationConstraint`
- 目录依赖：`Parabola_Definition → Parabola_Equation_Standard_Right → Parabola_Equation_Standard_Left → Parabola_Equation_Standard_Up → Parabola_Equation_Standard_Down`
- Applicator 支持：`CONCRETE`
- 本题执行状态：`NO_MATCH`

#### 步骤 4：Vector_Collinear_Condition

- 具体公式/规则：$u=lambda*v$
- 类别：`vector`
- 所需对象类型：`Vector`
- 所需信息：`VectorOf`
- 产出信息：`EquationConstraint`
- 目录依赖：`Vector_Dot_Product_Algebraic`
- Applicator 支持：`CONCRETE`
- 本题执行状态：`NO_MATCH`

### 当前 Applicator 回放结果

- 能否完整执行：**否（存在失败步骤）**
- 最终答案：**未得到正确答案**
- 初始目标状态：`GOAL_NOT_REACHED`
- 最终目标状态：`GOAL_NOT_REACHED`
- Applicator 实际值：`None`
- 标注期望值：`None`
- 结果说明：无
- 首个失败步骤：第 2 步
- 失败状态：`NO_MATCH`
- 缺失谓词：`无`
- 缺失对象类型：`无`

---

## 36. 题目 ID 5594

- 数据索引：5593
- V3 质量：C

### 题目

若在抛物线$y^{2}=4 x$上求一点$Q$，使它到点$A(7,8)$与到准线的距离之和最小，则点$Q$的坐标是?

### 形式化信息

- 已知：`G: Parabola;Expression(G) = (y^2 = 4*x);Q: Point;PointOnCurve(Q, G);A: Point;Coordinate(A) = (7, 8);WhenMin(Distance(Q, A) + Distance(Q, Directrix(G)))`
- 查询：`Coordinate(Q)`
- 答案：`(4, 4)`

### 解题过程

$\because抛物线方程为y^{2}=4x,\therefore抛物线的焦点为F(1,0),准线方程为x=-1,由抛物线的定义,点Q到准线的距离等于它到焦点的距离所求的最小值即为|QA|+|QF|的最小值.根据平面几何知识,可得当A、Q、F三点共线时,|QA|+|QF|最小,由此可得|QA|+|QF|的最小值为A到焦点F(1,0)的距离此时直线AF的斜率k=\frac{4}{3},直线AF的方程为y=\frac{4}{3}(x-1)联立\begin{cases}y=\frac{4}{3}(x-1)\\v2=4x\end{cases},解得\begin{cases}x=4\\y=4\end{cases}或\begin{cases}x=\frac{1}{4}\\y=-1\end{cases}(舍去)即点Q的坐标是(4,4),$

### 定理内容序列

#### 步骤 1：Parabola_Equation_Standard_Right

- 具体公式/规则：$y^2=2px$
- 类别：`standard_equation`
- 所需对象类型：`无`
- 所需信息：`ExpressionPolynomial`
- 产出信息：`ConicStandardForm, ParameterOf`
- 目录依赖：`无`
- Applicator 支持：`CONCRETE`
- 本题执行状态：`APPLIED`

#### 步骤 2：Parabola_Definition

- 具体公式/规则：$|PF|=distance(P,directrix)$
- 类别：`definition`
- 所需对象类型：`无`
- 所需信息：`无`
- 产出信息：`DefinitionRelation`
- 目录依赖：`无`
- Applicator 支持：`CONCRETE`
- 本题执行状态：`NO_MATCH`

#### 步骤 3：Parabola_Directrix

- 具体公式/规则：$x or y=+/-p/2$
- 类别：`directrix`
- 所需对象类型：`无`
- 所需信息：`ParameterOf`
- 产出信息：`DirectrixExpressionOf`
- 目录依赖：`Parabola_Equation_Standard_Right → Parabola_Equation_Standard_Left → Parabola_Equation_Standard_Up → Parabola_Equation_Standard_Down`
- Applicator 支持：`CONCRETE`
- 本题执行状态：`APPLIED`

#### 步骤 4：Two_Points_Distance

- 具体公式/规则：$d=sqrt((x2-x1)^2+(y2-y1)^2)$
- 类别：`coordinate`
- 所需对象类型：`Point`
- 所需信息：`CoordinateOf`
- 产出信息：`CoordinateOf, DistanceOf, SlopeOf`
- 目录依赖：`无`
- Applicator 支持：`CONCRETE`
- 本题执行状态：`NO_MATCH`

### 当前 Applicator 回放结果

- 能否完整执行：**否（存在失败步骤）**
- 最终答案：**未得到正确答案**
- 初始目标状态：`VALUE_UNRESOLVED`
- 最终目标状态：`VALUE_UNRESOLVED`
- Applicator 实际值：`{'__type__': 'Point2D', 'x': {'__type__': 'Term', 'operator': 'symbol', 'arguments': ['__coord_Q_x']}, 'y': {'__type__': 'Term', 'operator': 'symbol', 'arguments': ['__coord_Q_y']}}`
- 标注期望值：`{'__type__': 'Point2D', 'x': {'__type__': 'Fraction', 'numerator': 4, 'denominator': 1}, 'y': {'__type__': 'Fraction', 'numerator': 4, 'denominator': 1}}`
- 结果说明：无
- 首个失败步骤：第 2 步
- 失败状态：`NO_MATCH`
- 缺失谓词：`无`
- 缺失对象类型：`无`

---

## 37. 题目 ID 5857

- 数据索引：5856
- V3 质量：C

### 题目

若抛物线$y^{2}=2 p x$的焦点与双曲线$\frac{x^{2}}{3}-y^{2}=1$的左焦点重合，则抛物线方程为?

### 形式化信息

- 已知：`H: Parabola;Expression(H) = (y^2 = 2*(p*x));p: Number;G: Hyperbola;Expression(G) = (x^2/3 - y^2 = 1);Focus(H) = LeftFocus(G)`
- 查询：`Expression(H)`
- 答案：`y^2=-8*x`

### 解题过程

$\frac{x^{2}}{3}-y^{2}=1的左焦点坐标为(-2,0),则\frac{p}{2}=-2,解得:p=-4,所以抛物线的方程为y2=-8x$

### 定理内容序列

#### 步骤 1：Hyperbola_Equation_Standard_X

- 具体公式/规则：$x^2/a^2-y^2/b^2=1$
- 类别：`standard_equation`
- 所需对象类型：`无`
- 所需信息：`ExpressionPolynomial`
- 产出信息：`ConicStandardForm, ParameterOf`
- 目录依赖：`无`
- Applicator 支持：`CONCRETE`
- 本题执行状态：`APPLIED`

#### 步骤 2：Parabola_Equation_Standard_Right

- 具体公式/规则：$y^2=2px$
- 类别：`standard_equation`
- 所需对象类型：`无`
- 所需信息：`ExpressionPolynomial`
- 产出信息：`ConicStandardForm, ParameterOf`
- 目录依赖：`无`
- Applicator 支持：`CONCRETE`
- 本题执行状态：`NO_MATCH`

#### 步骤 3：Parabola_Directrix

- 具体公式/规则：$x or y=+/-p/2$
- 类别：`directrix`
- 所需对象类型：`无`
- 所需信息：`ParameterOf`
- 产出信息：`DirectrixExpressionOf`
- 目录依赖：`Parabola_Equation_Standard_Right → Parabola_Equation_Standard_Left → Parabola_Equation_Standard_Up → Parabola_Equation_Standard_Down`
- Applicator 支持：`CONCRETE`
- 本题执行状态：`NO_MATCH`

### 当前 Applicator 回放结果

- 能否完整执行：**否（存在失败步骤）**
- 最终答案：**未得到正确答案**
- 初始目标状态：`GOAL_NOT_REACHED`
- 最终目标状态：`GOAL_NOT_REACHED`
- Applicator 实际值：`None`
- 标注期望值：`None`
- 结果说明：无
- 首个失败步骤：第 2 步
- 失败状态：`NO_MATCH`
- 缺失谓词：`无`
- 缺失对象类型：`无`

---

## 38. 题目 ID 5859

- 数据索引：5858
- V3 质量：D

### 题目

设点$F$为抛物线$C$: $y^{2}=2 p x  (p>0)$的焦点，点$A(0,2)$, 若线段$A F$的中点$B$在抛物线上，则$|B F|$=?

### 形式化信息

- 已知：`C: Parabola;Expression(C) = (y^2 = 2*p*x);p: Number;A: Point;F: Point;B: Point;p>0;Coordinate(A) = (0, 2);Focus(C) = F;PointOnCurve(B, C);MidPoint(LineSegmentOf(A,F))=B`
- 查询：`Abs(LineSegmentOf(B, F))`
- 答案：`3*sqrt(2)/4`

### 解题过程

$焦点F的坐标为(\frac{p}{2},0),则线段AF的中点B的坐标为(\frac{p}{4},1)又点B在抛物线上,将点B的坐标代入抛物线方程可得1=\frac{p^{2}}{2},解得p=\sqrt{2}或-\sqrt{2}(舍去),则点F的坐标为(\frac{\sqrt{2}}{2},0),点B的坐标为(\frac{\sqrt{2}}{4},1),由两点间的距离公式可得|BF|=(\frac{\sqrt{2}}{2}-\frac{\sqrt{2}}{4})^{2}+(0-1)^{2}=\frac{3\sqrt{2}}{4}$

### 定理内容序列

#### 步骤 1：Parabola_Equation_Standard_Right

- 具体公式/规则：$y^2=2px$
- 类别：`standard_equation`
- 所需对象类型：`无`
- 所需信息：`ExpressionPolynomial`
- 产出信息：`ConicStandardForm, ParameterOf`
- 目录依赖：`无`
- Applicator 支持：`CONCRETE`
- 本题执行状态：`APPLIED`

#### 步骤 2：Parabola_Definition

- 具体公式/规则：$|PF|=distance(P,directrix)$
- 类别：`definition`
- 所需对象类型：`无`
- 所需信息：`无`
- 产出信息：`DefinitionRelation`
- 目录依赖：`无`
- Applicator 支持：`CONCRETE`
- 本题执行状态：`NO_MATCH`

#### 步骤 3：Parabola_Directrix

- 具体公式/规则：$x or y=+/-p/2$
- 类别：`directrix`
- 所需对象类型：`无`
- 所需信息：`ParameterOf`
- 产出信息：`DirectrixExpressionOf`
- 目录依赖：`Parabola_Equation_Standard_Right → Parabola_Equation_Standard_Left → Parabola_Equation_Standard_Up → Parabola_Equation_Standard_Down`
- Applicator 支持：`CONCRETE`
- 本题执行状态：`APPLIED`

#### 步骤 4：Triangle_Midline_Theorem

- 具体公式/规则：$midline=base/2$
- 类别：`midline`
- 所需对象类型：`无`
- 所需信息：`MidpointOf`
- 产出信息：`LengthOf`
- 目录依赖：`无`
- Applicator 支持：`SPECIFICATION_ONLY`
- 本题执行状态：`SPECIFICATION_ONLY`

#### 步骤 5：Two_Points_Distance

- 具体公式/规则：$d=sqrt((x2-x1)^2+(y2-y1)^2)$
- 类别：`coordinate`
- 所需对象类型：`Point`
- 所需信息：`CoordinateOf`
- 产出信息：`CoordinateOf, DistanceOf, SlopeOf`
- 目录依赖：`无`
- Applicator 支持：`CONCRETE`
- 本题执行状态：`NO_MATCH`

### 当前 Applicator 回放结果

- 能否完整执行：**否（存在失败步骤）**
- 最终答案：**未得到正确答案**
- 初始目标状态：`GOAL_NOT_REACHED`
- 最终目标状态：`GOAL_NOT_REACHED`
- Applicator 实际值：`None`
- 标注期望值：`None`
- 结果说明：无
- 首个失败步骤：第 2 步
- 失败状态：`NO_MATCH`
- 缺失谓词：`无`
- 缺失对象类型：`无`

---

## 39. 题目 ID 6087

- 数据索引：6086
- V3 质量：C

### 题目

已知双曲线$\frac{x^{2}}{a^{2}}-\frac{y^{2}}{b^{2}}=1(a>0, b>0)$的左、右焦点分别为$F_{1}$、$F_{2}$, 过$F_{1}$作圆$x^{2}+y^{2}=a^{2}$的切线，交双曲线右支于点$M$，若$\angle F_{1} M F_{2}=45°$，则双曲线的渐近线方程为?

### 形式化信息

- 已知：`G: Hyperbola;a: Number;b: Number;H: Circle;F1: Point;M: Point;F2: Point;l: Line;a>0;b>0;Expression(G) = (-y^2/b^2 + x^2/a^2 = 1);Expression(H) = (x^2 + y^2 = a^2);LeftFocus(G) = F1;RightFocus(G) = F2;PointOnCurve(F1, l);TangentOfPoint(F1,H)=l;Intersection(l,RightPart(G))=M;AngleOf(F1, M, F2) = ApplyUnit(45,degree)`
- 查询：`Expression(Asymptote(G))`
- 答案：`y = pm*sqrt(2)*x`

### 解题过程

$如图所示:切点为A,连接OA,过F_{2}作BF_{2}\botF_{1}M于BO是F_{1}F_{2}中点,OA/\!/BF_{2}\RightarrowBF_{2}=2OA=2a\angleF_{1}MF_{2}=45\RightarrowMF=2\sqrt{2}a,BM=2a\RightarrowBF_{1}=2\sqrt{2}a在RtABF_{1}F_{2}中,根据勾股定理得:(2\sqrt{2}a)^{2}+(2a)^{2}=(2c)^{2}\Rightarrowb^{2}=2a^{2}渐近线方程为:y=\pm\sqrt{2}x$

### 定理内容序列

#### 步骤 1：Hyperbola_Equation_Standard_X

- 具体公式/规则：$x^2/a^2-y^2/b^2=1$
- 类别：`standard_equation`
- 所需对象类型：`无`
- 所需信息：`ExpressionPolynomial`
- 产出信息：`ConicStandardForm, ParameterOf`
- 目录依赖：`无`
- Applicator 支持：`CONCRETE`
- 本题执行状态：`APPLIED`

#### 步骤 2：Circle_Standard_Equation

- 具体公式/规则：$(x-h)^2+(y-k)^2=r^2$
- 类别：`circle`
- 所需对象类型：`Circle`
- 所需信息：`ExpressionPolynomial`
- 产出信息：`CircleStandardForm, ParameterOf`
- 目录依赖：`无`
- Applicator 支持：`CONCRETE`
- 本题执行状态：`APPLIED`

#### 步骤 3：Circle_Tangent_Condition

- 具体公式/规则：$distance(center,line)=radius$
- 类别：`circle`
- 所需对象类型：`Circle`
- 所需信息：`ExpressionPolynomial`
- 产出信息：`CircleStandardForm, ParameterOf`
- 目录依赖：`Point_To_Line_Distance → Circle_Standard_Equation`
- Applicator 支持：`CONCRETE`
- 本题执行状态：`NO_MATCH`

#### 步骤 4：Hyperbola_Asymptote

- 具体公式/规则：$y=+/-(b/a)x$
- 类别：`asymptote`
- 所需对象类型：`Hyperbola`
- 所需信息：`ConicStandardForm`
- 产出信息：`AsymptoteFamilyOf, EquationConstraint`
- 目录依赖：`Hyperbola_Equation_Standard_X → Hyperbola_Equation_Standard_Y`
- Applicator 支持：`CONCRETE`
- 本题执行状态：`APPLIED`

#### 步骤 5：Pythagorean_Theorem

- 具体公式/规则：$a^2+b^2=c^2$
- 类别：`triangle`
- 所需对象类型：`Triangle`
- 所需信息：`TriangleOf`
- 产出信息：`EquationConstraint`
- 目录依赖：`无`
- Applicator 支持：`CONCRETE`
- 本题执行状态：`NO_MATCH`

#### 步骤 6：Cosine_Law

- 具体公式/规则：$c^2=a^2+b^2-2ab*cos(C)$
- 类别：`triangle`
- 所需对象类型：`Triangle`
- 所需信息：`TriangleOf`
- 产出信息：`EquationConstraint`
- 目录依赖：`无`
- Applicator 支持：`CONCRETE`
- 本题执行状态：`APPLIED`

#### 步骤 7：Hyperbola_Parameter_Relation

- 具体公式/规则：$c^2=a^2+b^2$
- 类别：`parameter`
- 所需对象类型：`无`
- 所需信息：`ParameterOf`
- 产出信息：`ParameterOf, EquationConstraint`
- 目录依赖：`Hyperbola_Equation_Standard_X → Hyperbola_Equation_Standard_Y`
- Applicator 支持：`CONCRETE`
- 本题执行状态：`APPLIED`

### 当前 Applicator 回放结果

- 能否完整执行：**否（存在失败步骤）**
- 最终答案：**未得到正确答案**
- 初始目标状态：`GOAL_NOT_REACHED`
- 最终目标状态：`VALUE_UNRESOLVED`
- Applicator 实际值：`{'__type__': 'LineEquationTarget', 'kind': 'asymptote', 'axis': 'y', 'value': {'__type__': 'Term', 'operator': 'abs', 'arguments': [{'__type__': 'Term', 'operator': 'sqrt_positive', 'arguments': [{'__type__': 'Term', 'operator': 'div', 'arguments': [{'__type__': 'Term', 'operator': 'mul', 'arguments': [{'__type__': 'Term', 'operator': 'symbol', 'arguments': ['b']}, {'__type__': 'Term', 'operator': 'symbol', 'arguments': ['b']}]}, {'__type__': 'Term', 'operator': 'mul', 'arguments': [{'__type__': 'Term', 'operator': 'symbol', 'arguments': ['a']}, {'__type__': 'Term', 'operator': 'symbol', 'arguments': ['a']}]}]}]}]}}`
- 标注期望值：`{'__type__': 'LineEquationTarget', 'kind': 'asymptote', 'axis': 'y', 'value': {'__type__': 'Term', 'operator': 'abs', 'arguments': [{'__type__': 'Term', 'operator': 'sqrt', 'arguments': [{'__type__': 'Fraction', 'numerator': 2, 'denominator': 1}]}]}}`
- 结果说明：无
- 首个失败步骤：第 3 步
- 失败状态：`NO_MATCH`
- 缺失谓词：`TangentRelation, LineNormalFormOf`
- 缺失对象类型：`无`

---

## 40. 题目 ID 6222

- 数据索引：6221
- V3 质量：C

### 题目

抛物线$y=\frac{1}{16} x^{2}$的焦点与双曲线$\frac{x^{2}}{3}-\frac{y^{2}}{m}=-1$的上焦点重合，则$m$=?

### 形式化信息

- 已知：`H: Parabola;Expression(H) = (y = x^2/16);G: Hyperbola;Expression(G) = (x^2/3 - y^2/m = -1);m: Number;Focus(H) = UpperFocus(G)`
- 查询：`m`
- 答案：`13`

### 解题过程

$抛物线y=\frac{1}{16}x^{2}的焦点为(0,4),所以m+3=4^{2}\Rightarrowm=13.$

### 定理内容序列

#### 步骤 1：Parabola_Equation_Standard_Up

- 具体公式/规则：$x^2=2py$
- 类别：`standard_equation`
- 所需对象类型：`无`
- 所需信息：`ExpressionPolynomial`
- 产出信息：`ConicStandardForm, ParameterOf`
- 目录依赖：`无`
- Applicator 支持：`CONCRETE`
- 本题执行状态：`APPLIED`

#### 步骤 2：Parabola_Directrix

- 具体公式/规则：$x or y=+/-p/2$
- 类别：`directrix`
- 所需对象类型：`无`
- 所需信息：`ParameterOf`
- 产出信息：`DirectrixExpressionOf`
- 目录依赖：`Parabola_Equation_Standard_Right → Parabola_Equation_Standard_Left → Parabola_Equation_Standard_Up → Parabola_Equation_Standard_Down`
- Applicator 支持：`CONCRETE`
- 本题执行状态：`APPLIED`

#### 步骤 3：Hyperbola_Equation_Standard_Y

- 具体公式/规则：$y^2/a^2-x^2/b^2=1$
- 类别：`standard_equation`
- 所需对象类型：`无`
- 所需信息：`ExpressionPolynomial`
- 产出信息：`ConicStandardForm, ParameterOf`
- 目录依赖：`无`
- Applicator 支持：`CONCRETE`
- 本题执行状态：`NO_MATCH`

#### 步骤 4：Hyperbola_Parameter_Relation

- 具体公式/规则：$c^2=a^2+b^2$
- 类别：`parameter`
- 所需对象类型：`无`
- 所需信息：`ParameterOf`
- 产出信息：`ParameterOf, EquationConstraint`
- 目录依赖：`Hyperbola_Equation_Standard_X → Hyperbola_Equation_Standard_Y`
- Applicator 支持：`CONCRETE`
- 本题执行状态：`NO_MATCH`

### 当前 Applicator 回放结果

- 能否完整执行：**否（存在失败步骤）**
- 最终答案：**未得到正确答案**
- 初始目标状态：`GOAL_UNSUPPORTED`
- 最终目标状态：`GOAL_UNSUPPORTED`
- Applicator 实际值：`None`
- 标注期望值：`None`
- 结果说明：query grammar is not supported
- 首个失败步骤：第 3 步
- 失败状态：`NO_MATCH`
- 缺失谓词：`无`
- 缺失对象类型：`无`

---

## 41. 题目 ID 6355

- 数据索引：6354
- V3 质量：C

### 题目

点$A(1,0)$，点$B$是$x$轴上的动点，线段$P B$的中点$E$在$y$轴上，且$A E$垂直$P B$，则$P$点的轨迹方程为?

### 形式化信息

- 已知：`A: Point;Coordinate(A) = (1, 0);B: Point;PointOnCurve(B, xAxis);P: Point;E: Point;MidPoint(LineSegmentOf(P, B)) = E;PointOnCurve(E, yAxis);IsPerpendicular(LineSegmentOf(A, E), LineSegmentOf(P, B))`
- 查询：`LocusEquation(P)`
- 答案：`(y^2=4*x)&(Negation(x=0))`

### 解题过程

$设P(x,y),B(m,0),则中点E坐标为E(\frac{x+m}{2},\frac{y}{2}),由\frac{x+m}{2}=0得m=-x,即E(0,又AE\botPB,若x\neq0,则_{k_{AE}}\cdotk_{PB}=\frac{\frac{y}{2}}{0-1}\times\frac{y}{2x}即y^{2}=4x若x=0,则m=0,P,B重合,直线PB不存在所以轨迹方程是y^{2}=4x(x\neq0)$

### 定理内容序列

#### 步骤 1：Parabola_Equation_Standard_Right

- 具体公式/规则：$y^2=2px$
- 类别：`standard_equation`
- 所需对象类型：`无`
- 所需信息：`ExpressionPolynomial`
- 产出信息：`ConicStandardForm, ParameterOf`
- 目录依赖：`无`
- Applicator 支持：`CONCRETE`
- 本题执行状态：`NO_MATCH`

#### 步骤 2：Vector_Collinear_Condition

- 具体公式/规则：$u=lambda*v$
- 类别：`vector`
- 所需对象类型：`Vector`
- 所需信息：`VectorOf`
- 产出信息：`EquationConstraint`
- 目录依赖：`Vector_Dot_Product_Algebraic`
- Applicator 支持：`CONCRETE`
- 本题执行状态：`NO_MATCH`

### 当前 Applicator 回放结果

- 能否完整执行：**否（存在失败步骤）**
- 最终答案：**未得到正确答案**
- 初始目标状态：`GOAL_UNSUPPORTED`
- 最终目标状态：`GOAL_UNSUPPORTED`
- Applicator 实际值：`None`
- 标注期望值：`None`
- 结果说明：query grammar is not supported
- 首个失败步骤：第 1 步
- 失败状态：`NO_MATCH`
- 缺失谓词：`ExpressionPolynomial`
- 缺失对象类型：`无`

---

## 42. 题目 ID 6504

- 数据索引：6503
- V3 质量：C

### 题目

设$m$为常数，若点$F(0,5)$是双曲线$\frac{y^{2}}{m}-\frac{x^{2}}{9}=1$的一个焦点，则$m$=?

### 形式化信息

- 已知：`G: Hyperbola;m: Number;F: Point;Expression(G) = (-x^2/9 + y^2/m = 1);Coordinate(F) = (0, 5);OneOf(Focus(G)) = F`
- 查询：`m`
- 答案：`16`

### 解题过程

$双曲线的焦点坐标为F(0,5),故焦点在y轴上,由c^{2}=a^{2}+b^{2}得25=m+9,m=16$

### 定理内容序列

#### 步骤 1：Hyperbola_Equation_Standard_Y

- 具体公式/规则：$y^2/a^2-x^2/b^2=1$
- 类别：`standard_equation`
- 所需对象类型：`无`
- 所需信息：`ExpressionPolynomial`
- 产出信息：`ConicStandardForm, ParameterOf`
- 目录依赖：`无`
- Applicator 支持：`CONCRETE`
- 本题执行状态：`NO_MATCH`

#### 步骤 2：Eccentricity_Formula

- 具体公式/规则：$e=c/a$
- 类别：`parameter`
- 所需对象类型：`无`
- 所需信息：`ParameterOf`
- 产出信息：`ParameterOf, EquationConstraint`
- 目录依赖：`Ellipse_Parameter_Relation → Hyperbola_Parameter_Relation`
- Applicator 支持：`CONCRETE`
- 本题执行状态：`NO_MATCH`

### 当前 Applicator 回放结果

- 能否完整执行：**否（存在失败步骤）**
- 最终答案：**未得到正确答案**
- 初始目标状态：`GOAL_UNSUPPORTED`
- 最终目标状态：`GOAL_UNSUPPORTED`
- Applicator 实际值：`None`
- 标注期望值：`None`
- 结果说明：query grammar is not supported
- 首个失败步骤：第 1 步
- 失败状态：`NO_MATCH`
- 缺失谓词：`无`
- 缺失对象类型：`无`

---

## 43. 题目 ID 6876

- 数据索引：6875
- V3 质量：C

### 题目

若点$P$是抛物线$y^{2}=2 x$上的一个动点，则点$P$到直线$3 x-4 y+\frac{7}{2}=0$的距离与$P$到该抛物线的准线的距离之和的最小值为?

### 形式化信息

- 已知：`G: Parabola;H: Line;P: Point;Expression(G) = (y^2 = 2*x);Expression(H) = (3*x - 4*y + 7/2 = 0);PointOnCurve(P, G)`
- 查询：`Min(Distance(P,H)+Distance(P,Directrix(G)))`
- 答案：`1`

### 解题过程

$如图,过点P分别作抛物线准线和直线3x-4y+\frac{7}{2}=0的垂线PQ、PA,垂足分别为点Q、A,由抛物线的定义可得|PQ|=|PF|,所以,|PA|+|PQ|=|PA|+|PF|\geqslant|AF|_{\min}当A、P、F三点共线时,|AF|取得最小值,|AF|的最小值为点F到直线3x-4y+\frac{7}{2}=0的距离,即|AF|_{\min}=\frac{|3\times\frac{1}{2}+\frac{7}{2}|}{\sqrt{3^{2}+(-4)^{2}}}=1$

### 定理内容序列

#### 步骤 1：Parabola_Equation_Standard_Right

- 具体公式/规则：$y^2=2px$
- 类别：`standard_equation`
- 所需对象类型：`无`
- 所需信息：`ExpressionPolynomial`
- 产出信息：`ConicStandardForm, ParameterOf`
- 目录依赖：`无`
- Applicator 支持：`CONCRETE`
- 本题执行状态：`APPLIED`

#### 步骤 2：Parabola_Definition

- 具体公式/规则：$|PF|=distance(P,directrix)$
- 类别：`definition`
- 所需对象类型：`无`
- 所需信息：`无`
- 产出信息：`DefinitionRelation`
- 目录依赖：`无`
- Applicator 支持：`CONCRETE`
- 本题执行状态：`NO_MATCH`

#### 步骤 3：Parabola_Directrix

- 具体公式/规则：$x or y=+/-p/2$
- 类别：`directrix`
- 所需对象类型：`无`
- 所需信息：`ParameterOf`
- 产出信息：`DirectrixExpressionOf`
- 目录依赖：`Parabola_Equation_Standard_Right → Parabola_Equation_Standard_Left → Parabola_Equation_Standard_Up → Parabola_Equation_Standard_Down`
- Applicator 支持：`CONCRETE`
- 本题执行状态：`APPLIED`

#### 步骤 4：Point_To_Line_Distance

- 具体公式/规则：$d=|Ax0+By0+C|/sqrt(A^2+B^2)$
- 类别：`coordinate`
- 所需对象类型：`Point`
- 所需信息：`CoordinateOf`
- 产出信息：`CoordinateOf, DistanceOf, SlopeOf`
- 目录依赖：`无`
- Applicator 支持：`CONCRETE`
- 本题执行状态：`NO_MATCH`

#### 步骤 5：Two_Points_Distance

- 具体公式/规则：$d=sqrt((x2-x1)^2+(y2-y1)^2)$
- 类别：`coordinate`
- 所需对象类型：`Point`
- 所需信息：`CoordinateOf`
- 产出信息：`CoordinateOf, DistanceOf, SlopeOf`
- 目录依赖：`无`
- Applicator 支持：`CONCRETE`
- 本题执行状态：`NO_MATCH`

### 当前 Applicator 回放结果

- 能否完整执行：**否（存在失败步骤）**
- 最终答案：**未得到正确答案**
- 初始目标状态：`GOAL_UNSUPPORTED`
- 最终目标状态：`GOAL_UNSUPPORTED`
- Applicator 实际值：`None`
- 标注期望值：`None`
- 结果说明：query grammar is not supported
- 首个失败步骤：第 2 步
- 失败状态：`NO_MATCH`
- 缺失谓词：`无`
- 缺失对象类型：`无`

---

## 44. 题目 ID 6877

- 数据索引：6876
- V3 质量：C

### 题目

过抛物线$y^{2}=2 p x(p>0)$的焦点$F$的直线交抛物线于点$A$ , $B$，交其准线$l$于点$C$，若点$F$是$AC$的中点，且$A F=4$，则线段$AB$的长为?

### 形式化信息

- 已知：`A: Point;B: Point;G: Parabola;p: Number;H: Line;C: Point;F: Point;l:Line;p>0;Expression(G) = (y^2 = 2*p*x);Focus(G)=F;PointOnCurve(F,H);Intersection(H,G) = {A,B};Directrix(G)=l;Intersection(H,l)=C;MidPoint(LineSegmentOf(A, C)) = F;LineSegmentOf(A, F) = 4`
- 查询：`Length(LineSegmentOf(A, B))`
- 答案：`16/3`

### 解题过程

$设过抛物线y^{2}=2px(p>0)的焦点F(\frac{p}{2},0)的直线交抛物线于点A(x_{1},y_{1}),B(x_{2},y_{2}),交其准线l:x=-\frac{p}{2}于C(-\frac{p}{2},y_{3}),因为F是AC的中点,且AF=4所以-\frac{p}{2}+x_{1}=\frac{p}{2}\times2,解得\begin{cases}p=2\\x_{1}=3\end{cases},即F(1,0),A(3,2\sqrt{3}),则AF的方程为y=\sqrt{3}(x-1),联立\begin{cases}\frac{\frac{1}{2}}=4\\y^{2}=4x\\y=\sqrt{3}(x-1)\end{cases}3x^{2}-10x+3=0,解得x_{2}=\frac{1}{3},所以|AB|=|AF|+|BF|=4+\frac{1}{3}+1=\frac{16}{3}.$

### 定理内容序列

#### 步骤 1：Parabola_Equation_Standard_Right

- 具体公式/规则：$y^2=2px$
- 类别：`standard_equation`
- 所需对象类型：`无`
- 所需信息：`ExpressionPolynomial`
- 产出信息：`ConicStandardForm, ParameterOf`
- 目录依赖：`无`
- Applicator 支持：`CONCRETE`
- 本题执行状态：`APPLIED`

#### 步骤 2：Substitution_x_equals_my_plus_n

- 具体公式/规则：$x=my+n$
- 类别：`advanced`
- 所需对象类型：`无`
- 所需信息：`EquationConstraint`
- 产出信息：`EquationConstraint`
- 目录依赖：`Line_Point_Slope_Form`
- Applicator 支持：`CONCRETE`
- 本题执行状态：`NO_MATCH`

#### 步骤 3：Vieta_Theorem_Sum

- 具体公式/规则：$x1+x2=-b/a$
- 类别：`algebra`
- 所需对象类型：`无`
- 所需信息：`QuadraticPolynomial`
- 产出信息：`EquationConstraint`
- 目录依赖：`Vieta_Theorem`
- Applicator 支持：`CONCRETE`
- 本题执行状态：`NO_MATCH`

#### 步骤 4：Parabola_Focal_Radius

- 具体公式/规则：$|PF|=x+p/2$
- 类别：`focal_radius`
- 所需对象类型：`Point`
- 所需信息：`PointOnCurve`
- 产出信息：`DistanceOf, EquationConstraint`
- 目录依赖：`Parabola_Definition → Parabola_Equation_Standard_Right → Parabola_Equation_Standard_Left → Parabola_Equation_Standard_Up → Parabola_Equation_Standard_Down`
- Applicator 支持：`CONCRETE`
- 本题执行状态：`NO_MATCH`

#### 步骤 5：Chord_Length_Formula_With_K

- 具体公式/规则：$|AB|=|x1-x2|*sqrt(1+k^2)$
- 类别：`chord`
- 所需对象类型：`Point`
- 所需信息：`PointOnCurve`
- 产出信息：`EquationConstraint`
- 目录依赖：`Slope_Formula`
- Applicator 支持：`CONCRETE`
- 本题执行状态：`NO_MATCH`

### 当前 Applicator 回放结果

- 能否完整执行：**否（存在失败步骤）**
- 最终答案：**未得到正确答案**
- 初始目标状态：`GOAL_UNSUPPORTED`
- 最终目标状态：`GOAL_UNSUPPORTED`
- Applicator 实际值：`None`
- 标注期望值：`None`
- 结果说明：query grammar is not supported
- 首个失败步骤：第 2 步
- 失败状态：`NO_MATCH`
- 缺失谓词：`LineNormalFormOf`
- 缺失对象类型：`无`

---

## 45. 题目 ID 6939

- 数据索引：6938
- V3 质量：C

### 题目

已知椭圆$\frac{x^{2}}{a^{2}}+\frac{y^{2}}{b^{2}}=1(a>b>0)$左焦点为$F_{1}$，右顶点为$A$，以$F_{1} A$为直径的圆与椭圆有三个公共点，则椭圆离心率的取值范围为?

### 形式化信息

- 已知：`G: Ellipse;Expression(G) = (y^2/b^2 + x^2/a^2 = 1);b: Number;a: Number;a > b;b > 0;F1: Point;LeftFocus(G) = F1;A: Point;RightVertex(G) = A;H: Circle;IsDiameter(LineSegmentOf(F1, A), H);NumIntersection(H, G) = 3`
- 查询：`Range(Eccentricity(G))`
- 答案：`(1/2, 1)`

### 解题过程

$设公共点M(x_{0},y_{0}),N(x_{0},-y_{0}),则\cdot\frac{y_{0}}{x_{0}-a}=-1,(x_{0}+c)(x_{0}-a)+y_{0}^{2}=0,\frac{x_{0}+c\cdotx_{0}-a}{\frac{x_{0}^{2}}{a^{2}}+\frac{y_{0}^{2}}{b^{2}}}=1\Rightarrowx_{0}^{2}+(c-a)x_{0}-ac+b^{2}-\frac{b^{2}x_{0}^{2}}{a^{2}}=0即\frac{c^{2}}{a^{2}}x_{0}^{2}+(c-a)x_{0}-ac+b^{2}=0,则方程\frac{c^{2}}{a^{2}}x^{2}+(c-a)x-ac+b^{2}=0的两根为x_{0},a故ax_{0}=\frac{b^{2}-ac}{c^{2}}\Rightarrowx_{0}=\frac{a(b^{2}-ac)}{c^{2}}<a\Rightarrowb^{2}-ac<c^{2}化为2e^{2}+e-1>0\Rightarrow\frac{1}{2}<e<1$

### 定理内容序列

#### 步骤 1：Ellipse_Equation_Standard_X

- 具体公式/规则：$x^2/a^2+y^2/b^2=1$
- 类别：`standard_equation`
- 所需对象类型：`无`
- 所需信息：`ExpressionPolynomial`
- 产出信息：`ConicStandardForm, ParameterOf`
- 目录依赖：`无`
- Applicator 支持：`CONCRETE`
- 本题执行状态：`APPLIED`

#### 步骤 2：Hyperbola_Equation_Standard_X

- 具体公式/规则：$x^2/a^2-y^2/b^2=1$
- 类别：`standard_equation`
- 所需对象类型：`无`
- 所需信息：`ExpressionPolynomial`
- 产出信息：`ConicStandardForm, ParameterOf`
- 目录依赖：`无`
- Applicator 支持：`CONCRETE`
- 本题执行状态：`NO_MATCH`

#### 步骤 3：Point_Difference_Method

- 具体公式/规则：$subtract two point equations$
- 类别：`chord`
- 所需对象类型：`Point`
- 所需信息：`PointOnCurve`
- 产出信息：`EquationConstraint`
- 目录依赖：`无`
- Applicator 支持：`CONCRETE`
- 本题执行状态：`NO_MATCH`

#### 步骤 4：Midpoint_Formula

- 具体公式/规则：$M=((x1+x2)/2,(y1+y2)/2)$
- 类别：`coordinate`
- 所需对象类型：`Point`
- 所需信息：`CoordinateOf`
- 产出信息：`CoordinateOf, DistanceOf, SlopeOf`
- 目录依赖：`无`
- Applicator 支持：`CONCRETE`
- 本题执行状态：`NO_MATCH`

#### 步骤 5：Eccentricity_Formula

- 具体公式/规则：$e=c/a$
- 类别：`parameter`
- 所需对象类型：`无`
- 所需信息：`ParameterOf`
- 产出信息：`ParameterOf, EquationConstraint`
- 目录依赖：`Ellipse_Parameter_Relation → Hyperbola_Parameter_Relation`
- Applicator 支持：`CONCRETE`
- 本题执行状态：`NO_MATCH`

### 当前 Applicator 回放结果

- 能否完整执行：**否（存在失败步骤）**
- 最终答案：**未得到正确答案**
- 初始目标状态：`GOAL_UNSUPPORTED`
- 最终目标状态：`GOAL_UNSUPPORTED`
- Applicator 实际值：`None`
- 标注期望值：`None`
- 结果说明：query grammar is not supported
- 首个失败步骤：第 2 步
- 失败状态：`NO_MATCH`
- 缺失谓词：`无`
- 缺失对象类型：`无`

---

## 46. 题目 ID 6954

- 数据索引：6953
- V3 质量：C

### 题目

抛物线$y^{2}=a x(a>0)$上的点$P(\frac{3}{2}, y_{0})$到焦点$F$的距离为$2$，则$a$=?

### 形式化信息

- 已知：`G: Parabola;a: Number;P: Point;F: Point;a>0;y0:Number;Expression(G) = (y^2 = a*x);Coordinate(P) = (3/2, y0);PointOnCurve(P, G);Focus(G) = F;Distance(P, F) = 2`
- 查询：`a`
- 答案：`2`

### 解题过程

$\because抛物线y^{2}=ax(a>0)上一点P(\frac{3}{2},y)到焦点F的距离为2,\therefore该点到准线的距离为2,抛物线的准线方程为x=-\frac{a}{4},\therefore\frac{3}{2}+\frac{a}{4}=2,求得a=2,$

### 定理内容序列

#### 步骤 1：Parabola_Equation_Standard_Right

- 具体公式/规则：$y^2=2px$
- 类别：`standard_equation`
- 所需对象类型：`无`
- 所需信息：`ExpressionPolynomial`
- 产出信息：`ConicStandardForm, ParameterOf`
- 目录依赖：`无`
- Applicator 支持：`CONCRETE`
- 本题执行状态：`APPLIED`

#### 步骤 2：Parabola_Definition

- 具体公式/规则：$|PF|=distance(P,directrix)$
- 类别：`definition`
- 所需对象类型：`无`
- 所需信息：`无`
- 产出信息：`DefinitionRelation`
- 目录依赖：`无`
- Applicator 支持：`CONCRETE`
- 本题执行状态：`NO_MATCH`

#### 步骤 3：Parabola_Directrix

- 具体公式/规则：$x or y=+/-p/2$
- 类别：`directrix`
- 所需对象类型：`无`
- 所需信息：`ParameterOf`
- 产出信息：`DirectrixExpressionOf`
- 目录依赖：`Parabola_Equation_Standard_Right → Parabola_Equation_Standard_Left → Parabola_Equation_Standard_Up → Parabola_Equation_Standard_Down`
- Applicator 支持：`CONCRETE`
- 本题执行状态：`APPLIED`

### 当前 Applicator 回放结果

- 能否完整执行：**否（存在失败步骤）**
- 最终答案：**正确**
- 初始目标状态：`GOAL_NOT_REACHED`
- 最终目标状态：`ANSWER_CORRECT`
- Applicator 实际值：`{'__type__': 'Fraction', 'numerator': 2, 'denominator': 1}`
- 标注期望值：`{'__type__': 'Fraction', 'numerator': 2, 'denominator': 1}`
- 结果说明：无
- 首个失败步骤：第 2 步
- 失败状态：`NO_MATCH`
- 缺失谓词：`无`
- 缺失对象类型：`无`

---

## 47. 题目 ID 7008

- 数据索引：7007
- V3 质量：C

### 题目

已知点$M$为椭圆$\frac{x^{2}}{27}+\frac{y^{2}}{26}=1$上任意一点，$A B$是圆$(x-1)^{2}+y^{2}=8$的一条直径，则$\overrightarrow{M A} \cdot \overrightarrow{M B}$的最大值与最小值的和为?

### 形式化信息

- 已知：`G: Ellipse;H: Circle;A: Point;B: Point;M: Point;Expression(G) = (x^2/27 + y^2/26 = 1);Expression(H) = (y^2 + (x - 1)^2 = 8);PointOnCurve(M, G);IsDiameter(LineSegmentOf(A, B), H)`
- 查询：`Min(DotProduct(VectorOf(M, A), VectorOf(M, B)))+Max(DotProduct(VectorOf(M, A), VectorOf(M, B)))`
- 答案：`40`

### 解题过程

$因为圆(x-1)^{2}+y^{2}=8,圆心C(1,0)半径为2\sqrt{2},设M(x,y),-3\sqrt{3}\leqslantx\leqslant3\sqrt{3},因为\overrightarrow{MA}=\overrightarrow{MC}+\overrightarrow{CA},\overrightarrow{MB}=\overrightarrow{MC}+\overrightarrow{CB}=\overrightarrow{MC}-\overrightarrow{BC}=\overrightarrow{MC}-\overrightarrow{CA}所以\overrightarrow{MA}\cdot\overrightarrow{MB}=(\overrightarrow{MC}+\overrightarrow{CA})\cdot(\overrightarrow{MC}-\overrightarrow{CA})=(\overrightarrow{MC})^{2}-(\overrightarrow{CA})^{2}=(\overrightarrow{MC})^{2}-8=(x-1)^{2}+y2-8.因为A(x,y)在\frac{x^{2}}{27}+\frac{y^{2}}{26}=1上,所以y^{2}=26-\frac{26}{27}x^{2}所以\overrightarrow{MA}\cdot\overrightarrow{MB}=(x-1)^{2}+26-\frac{26}{27}x^{2}-8=\frac{1}{27}x^{2}-2x+19,-3\sqrt{3}\leqslantx\leqslant3\sqrt{3},函数y=\frac{1}{27}x^{2}-2x+19,为对称轴为x=27,开口向上的抛物线,当x=-3\sqrt{3}时,\overrightarrow{MA}\cdot\overrightarrow{MB}取得最大值为6\sqrt{3}+20,当x=3\sqrt{3}时,\overrightarrow{MA}\cdot\overrightarrow{MB}取得最小值为-6\sqrt{3}+20,所以最大值与最小值的和为40$

### 定理内容序列

#### 步骤 1：Ellipse_Equation_Standard_X

- 具体公式/规则：$x^2/a^2+y^2/b^2=1$
- 类别：`standard_equation`
- 所需对象类型：`无`
- 所需信息：`ExpressionPolynomial`
- 产出信息：`ConicStandardForm, ParameterOf`
- 目录依赖：`无`
- Applicator 支持：`CONCRETE`
- 本题执行状态：`APPLIED`

#### 步骤 2：Circle_Standard_Equation

- 具体公式/规则：$(x-h)^2+(y-k)^2=r^2$
- 类别：`circle`
- 所需对象类型：`Circle`
- 所需信息：`ExpressionPolynomial`
- 产出信息：`CircleStandardForm, ParameterOf`
- 目录依赖：`无`
- Applicator 支持：`CONCRETE`
- 本题执行状态：`APPLIED`

#### 步骤 3：Vector_Dot_Product_Algebraic

- 具体公式/规则：$u dot v=x1*x2+y1*y2$
- 类别：`vector`
- 所需对象类型：`Vector`
- 所需信息：`VectorOf`
- 产出信息：`EquationConstraint`
- 目录依赖：`无`
- Applicator 支持：`CONCRETE`
- 本题执行状态：`NO_MATCH`

#### 步骤 4：Two_Points_Distance

- 具体公式/规则：$d=sqrt((x2-x1)^2+(y2-y1)^2)$
- 类别：`coordinate`
- 所需对象类型：`Point`
- 所需信息：`CoordinateOf`
- 产出信息：`CoordinateOf, DistanceOf, SlopeOf`
- 目录依赖：`无`
- Applicator 支持：`CONCRETE`
- 本题执行状态：`NO_MATCH`

#### 步骤 5：Quadratic_Function_Maximum

- 具体公式/规则：$extremum by completing square$
- 类别：`advanced`
- 所需对象类型：`无`
- 所需信息：`EquationConstraint`
- 产出信息：`EquationConstraint`
- 目录依赖：`Discriminant_Delta`
- Applicator 支持：`SPECIFICATION_ONLY`
- 本题执行状态：`SPECIFICATION_ONLY`

### 当前 Applicator 回放结果

- 能否完整执行：**否（存在失败步骤）**
- 最终答案：**未得到正确答案**
- 初始目标状态：`GOAL_UNSUPPORTED`
- 最终目标状态：`GOAL_UNSUPPORTED`
- Applicator 实际值：`None`
- 标注期望值：`None`
- 结果说明：query grammar is not supported
- 首个失败步骤：第 3 步
- 失败状态：`NO_MATCH`
- 缺失谓词：`VectorOf, RequestedDotProductOf`
- 缺失对象类型：`Vector`

---

## 48. 题目 ID 7141

- 数据索引：7140
- V3 质量：C

### 题目

已知双曲线$C$: $\frac{x^{2}}{a^{2}}-\frac{y^{2}}{3}=1(a>0)$的右焦点为$F$，则点$F$到双曲线$C$的渐近线的距离?

### 形式化信息

- 已知：`C: Hyperbola;a: Number;F: Point;a>0;Expression(C) = (-y^2/3 + x^2/a^2 = 1);RightFocus(C) = F`
- 查询：`Distance(F, Asymptote(C))`
- 答案：`sqrt(3)`

### 解题过程

$设F(c,0),即a^{2}+b^{2}=a^{2}+3=c^{2}.双曲线的一条渐近线方程设为\sqrt{3}x-ay=0,可得F到渐近线的距离为d=\frac{\sqrt{3}c}{\sqrt{3+a^{2}}}=\frac{\sqrt{3}c}{c}=\sqrt{3}$

### 定理内容序列

#### 步骤 1：Hyperbola_Equation_Standard_X

- 具体公式/规则：$x^2/a^2-y^2/b^2=1$
- 类别：`standard_equation`
- 所需对象类型：`无`
- 所需信息：`ExpressionPolynomial`
- 产出信息：`ConicStandardForm, ParameterOf`
- 目录依赖：`无`
- Applicator 支持：`CONCRETE`
- 本题执行状态：`APPLIED`

#### 步骤 2：Hyperbola_Asymptote

- 具体公式/规则：$y=+/-(b/a)x$
- 类别：`asymptote`
- 所需对象类型：`Hyperbola`
- 所需信息：`ConicStandardForm`
- 产出信息：`AsymptoteFamilyOf, EquationConstraint`
- 目录依赖：`Hyperbola_Equation_Standard_X → Hyperbola_Equation_Standard_Y`
- Applicator 支持：`CONCRETE`
- 本题执行状态：`APPLIED`

#### 步骤 3：Point_To_Line_Distance

- 具体公式/规则：$d=|Ax0+By0+C|/sqrt(A^2+B^2)$
- 类别：`coordinate`
- 所需对象类型：`Point`
- 所需信息：`CoordinateOf`
- 产出信息：`CoordinateOf, DistanceOf, SlopeOf`
- 目录依赖：`无`
- Applicator 支持：`CONCRETE`
- 本题执行状态：`NO_MATCH`

### 当前 Applicator 回放结果

- 能否完整执行：**否（存在失败步骤）**
- 最终答案：**未得到正确答案**
- 初始目标状态：`GOAL_UNSUPPORTED`
- 最终目标状态：`GOAL_UNSUPPORTED`
- Applicator 实际值：`None`
- 标注期望值：`None`
- 结果说明：query grammar is not supported
- 首个失败步骤：第 3 步
- 失败状态：`NO_MATCH`
- 缺失谓词：`PointPositionOf, LineNormalFormOf, RequestedPointLineDistanceOf`
- 缺失对象类型：`无`

---

## 49. 题目 ID 7353

- 数据索引：7352
- V3 质量：C

### 题目

已知抛物线$x^{2}=2 p y  (p>0)$焦点为$F$、$O$为坐标原点，直线$l$过点$F$与抛物线交于$A$、$B$两点，与$x$轴交于$C(2p,0)$，若$|A B|=17$，则$\triangle O C F$的面积为?

### 形式化信息

- 已知：`G: Parabola;Expression(G) = (x^2 = 2*(p*y));p: Number;p>0;F: Point;Focus(G) = F;O: Origin;l: Line;PointOnCurve(F, l);A: Point;B: Point;Intersection(l, G) = {A, B};C: Point;Coordinate(C) = (2*p, 0);Intersection(l, xAxis) = C;Abs(LineSegmentOf(A, B)) = 17`
- 查询：`Area(TriangleOf(O, C, F))`
- 答案：`32`

### 解题过程

$\because直线l过点F(0,\frac{p}{2}),C(2p,0),\therefore_{K_{FC}}=\frac{0-\frac{p}{2}}{2p-0}=-\frac{1}{4}联立直线l与抛物线方程\begin{cases}x+\frac{p}{2},\\y=-\frac{1}{4}x+\frac{p}{2}\\x^{2}=2py\end{cases},可得x^{2}+\frac{p}{2}x-p^{2}=0,设A(x_{1},y_{1}),B(x_{2},y_{2}),由韦达定理可得,由弦长公式可得|AB|x_{2}=-\frac{p}{2},x_{2}x_{2}=-p^{2},17,\sqrt{1+(-\frac{1}{4})^{2}|x_{2}-x_{2}|x_{2}^{2}}=\frac{\sqrt{x}}{3}=\frac{\sqrt{17}}{4}\sqrt{(-\frac{p}{2})^{2}-4p^{2}}=\frac{17p}{8}=17'\thereforep=8,\thereforeS_{\triangleOCF}=\frac{1}{2}\cdotOC\cdotOF=\frac{1}{2}\cdot2p\cdot\frac{p}{2}=32.均答安为.\_32$

### 定理内容序列

#### 步骤 1：Parabola_Equation_Standard_Right

- 具体公式/规则：$y^2=2px$
- 类别：`standard_equation`
- 所需对象类型：`无`
- 所需信息：`ExpressionPolynomial`
- 产出信息：`ConicStandardForm, ParameterOf`
- 目录依赖：`无`
- Applicator 支持：`CONCRETE`
- 本题执行状态：`NO_MATCH`

#### 步骤 2：Ellipse_Tangent_Line

- 具体公式/规则：$x0*x/a^2+y0*y/b^2=1$
- 类别：`tangent`
- 所需对象类型：`Point`
- 所需信息：`PointOnCurve`
- 产出信息：`ExpressionOf`
- 目录依赖：`Ellipse_Equation_Standard_X → Ellipse_Equation_Standard_Y`
- Applicator 支持：`CONCRETE`
- 本题执行状态：`NO_MATCH`

#### 步骤 3：Vector_Collinear_Condition

- 具体公式/规则：$u=lambda*v$
- 类别：`vector`
- 所需对象类型：`Vector`
- 所需信息：`VectorOf`
- 产出信息：`EquationConstraint`
- 目录依赖：`Vector_Dot_Product_Algebraic`
- Applicator 支持：`CONCRETE`
- 本题执行状态：`NO_MATCH`

#### 步骤 4：Triangle_Area_Formula

- 具体公式/规则：$S=base*height/2$
- 类别：`area`
- 所需对象类型：`无`
- 所需信息：`TriangleOf`
- 产出信息：`AreaOf`
- 目录依赖：`Point_To_Line_Distance`
- Applicator 支持：`CONCRETE`
- 本题执行状态：`NO_MATCH`

### 当前 Applicator 回放结果

- 能否完整执行：**否（存在失败步骤）**
- 最终答案：**未得到正确答案**
- 初始目标状态：`GOAL_NOT_REACHED`
- 最终目标状态：`GOAL_NOT_REACHED`
- Applicator 实际值：`None`
- 标注期望值：`None`
- 结果说明：无
- 首个失败步骤：第 1 步
- 失败状态：`NO_MATCH`
- 缺失谓词：`无`
- 缺失对象类型：`无`

---

## 50. 题目 ID 7443

- 数据索引：7442
- V3 质量：C

### 题目

若实数$x$,$y$满足$\frac{x|x|}{4}+\frac{y|y|}{9}=1$，且$|3 x+2 y-t|$的最大值为$3 \sqrt{2}$，则实数$t$的值是?

### 形式化信息

- 已知：`x_: Real;y_:Real;t: Real;(x_*Abs(x_))/4 + (y_*Abs(y_))/9 = 1;Max(Abs(-t + 3*x_ + 2*y_)) = 3*sqrt(2)`
- 查询：`t`
- 答案：`3*sqrt(2)`

### 解题过程

$当x>0,y>0时,曲线为椭圆\frac{x^{2}}{4}+\frac{y^{2}}{9}=1在第一象限的图象,当x>0,y<0时,曲线为双曲线\frac{x^{2}}{4}-\frac{y^{2}}{9}=1在第四象限的图象,当x<0,y>0时,曲线为双曲线\frac{y^{2}}{9}-\frac{x^{2}}{4}=1在第二象限的图象,当x<0,y<0时,原方程无实数解.因为直线3x+2y=0是双曲线\frac{x^{2}}{4}-\frac{y^{2}}{9}=1和\frac{y^{2}}{9}-\frac{x^{2}}{4}=1的渐近线,令3x+2y-t=0,则\frac{|3x+2y-t|}{\sqrt{13}}表示曲线上的点到直线3x+2y-t=0的距离.因为|3x+2y-t|的最大值为3\sqrt{2},所以\frac{|3x+2y-t|}{\sqrt{13}}的最大值为\frac{3\sqrt{26}}{3}由图知,曲线上到直线3x+2y=0距离最大的点在椭圆\frac{x^{2}}{4}+\frac{y^{2}}{9}=1上,设椭圆上动点坐标为(2\cos\theta,3\sin\theta),\theta\in(0,\frac{\pi}{2}).由点到直线的距离公式得\frac{|6\cos\theta+6\sin\theta|}{\sqrt{3^{2}+2^{2}}}=\frac{|6\sqrt{2}\sin(\theta+\frac{\pi}{4})|}{\sqrt{13}}\leqslant\frac{6\sqrt{26}}{13}因为\frac{6\sqrt{26}}{BB}>\frac{3\sqrt{26}}{B},所以\frac{13x+2y-t}{\sqrt{13}}要想有最大值\frac{3\sqrt{26}}{16}.直线3x+2y=0需向上平移.所以\frac{|t|}{\sqrt{13}}=\frac{3\sqrt{26}}{13},解得t=3\sqrt{2},$

### 定理内容序列

#### 步骤 1：Ellipse_Equation_Standard_X

- 具体公式/规则：$x^2/a^2+y^2/b^2=1$
- 类别：`standard_equation`
- 所需对象类型：`无`
- 所需信息：`ExpressionPolynomial`
- 产出信息：`ConicStandardForm, ParameterOf`
- 目录依赖：`无`
- Applicator 支持：`CONCRETE`
- 本题执行状态：`NO_MATCH`

#### 步骤 2：Hyperbola_Equation_Standard_X

- 具体公式/规则：$x^2/a^2-y^2/b^2=1$
- 类别：`standard_equation`
- 所需对象类型：`无`
- 所需信息：`ExpressionPolynomial`
- 产出信息：`ConicStandardForm, ParameterOf`
- 目录依赖：`无`
- Applicator 支持：`CONCRETE`
- 本题执行状态：`NO_MATCH`

#### 步骤 3：Hyperbola_Asymptote

- 具体公式/规则：$y=+/-(b/a)x$
- 类别：`asymptote`
- 所需对象类型：`Hyperbola`
- 所需信息：`ConicStandardForm`
- 产出信息：`AsymptoteFamilyOf, EquationConstraint`
- 目录依赖：`Hyperbola_Equation_Standard_X → Hyperbola_Equation_Standard_Y`
- Applicator 支持：`CONCRETE`
- 本题执行状态：`NO_MATCH`

#### 步骤 4：Point_Difference_Method_Hyperbola

- 具体公式/规则：$hyperbola point-difference relation$
- 类别：`chord`
- 所需对象类型：`Point`
- 所需信息：`PointOnCurve`
- 产出信息：`EquationConstraint`
- 目录依赖：`Point_Difference_Method → Hyperbola_Equation_Standard_X → Hyperbola_Equation_Standard_Y`
- Applicator 支持：`CONCRETE`
- 本题执行状态：`NO_MATCH`

#### 步骤 5：Point_To_Line_Distance

- 具体公式/规则：$d=|Ax0+By0+C|/sqrt(A^2+B^2)$
- 类别：`coordinate`
- 所需对象类型：`Point`
- 所需信息：`CoordinateOf`
- 产出信息：`CoordinateOf, DistanceOf, SlopeOf`
- 目录依赖：`无`
- Applicator 支持：`CONCRETE`
- 本题执行状态：`NO_MATCH`

#### 步骤 6：Quadratic_Function_Maximum

- 具体公式/规则：$extremum by completing square$
- 类别：`advanced`
- 所需对象类型：`无`
- 所需信息：`EquationConstraint`
- 产出信息：`EquationConstraint`
- 目录依赖：`Discriminant_Delta`
- Applicator 支持：`SPECIFICATION_ONLY`
- 本题执行状态：`SPECIFICATION_ONLY`

### 当前 Applicator 回放结果

- 能否完整执行：**否（存在失败步骤）**
- 最终答案：**未得到正确答案**
- 初始目标状态：`GOAL_UNSUPPORTED`
- 最终目标状态：`GOAL_UNSUPPORTED`
- Applicator 实际值：`None`
- 标注期望值：`None`
- 结果说明：query grammar is not supported
- 首个失败步骤：第 1 步
- 失败状态：`NO_MATCH`
- 缺失谓词：`ExpressionPolynomial`
- 缺失对象类型：`无`

---
