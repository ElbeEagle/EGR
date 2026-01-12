# Sampled 500 Problems with Non-Empty Process
Total valid problems available: 5357
Sampled: 500

## Problem Index: 55
**ID**: 56
**Text**:  
已知过点$M(1 , 0)$的直线$A B$与抛物线$y^{2}=2 x$交于$A$、$B$两点，$O$为坐标原点，若$O A$ , $O B$的斜率之和为$1$，则直线$A B$方程为?

**Process**:  
设直线AB的方程并代入抛物线方程,根据韦达定理以及斜率公式,可得t的值,进而得到直线的方程羊解】依题意可设直线AB的方程为:x=ty+1,代入y^{2}=2x得y^{2}-2ty-2=0.设A(x_{1},y_{1}),B(x_{2},y_{2}),则y_{1}y_{2}=-2,y_{1}+y_{2}=2t所以_{k_{OA}}+k_{OB}=\frac{y_{1}}{x_{1}}+\frac{y_{2}}{x_{2}}=\frac{2}{y_{1}}+\frac{2}{y_{2}}=\frac{2(y_{1}+y_{2})}{y_{1}y_{2}}=\frac{4t}{-2}=-2t'\therefore-2t=1,解得t=-\frac{1}{2},\therefore直线AB的方程为:x=-\frac{1}{2}y+1,即2x+y-2=0

**Theorem Sequence**:  
Parabola_Equation_Standard_Right, Substitution_x_equals_my_plus_n, Vieta_Theorem_Sum, Vieta_Theorem_Product, Midpoint_Formula

---

## Problem Index: 61
**ID**: 62
**Text**:  
已知双曲线$C$的焦点在$y$轴上，虚轴长为$4$，且与双曲线$\frac{x^{2}}{4}-\frac{y^{2}}{3}=1$有相同渐近线，则双曲线$C$的方程为?

**Process**:  
由题意,设所求双曲线为\frac{x^{2}}{4}-\frac{y^{2}}{3}=1且\lambda\neq0,即\frac{x^{2}}{4\lambda}-\frac{y^{2}}{3\lambda}=1\because焦点在y轴上,虚轴长为4,\therefore\begin{cases}\lambda<0\\2\sqrt{-42}=4\end{cases},解得\lambda=-1,即双曲线C的方程为\frac{y^{2}}{3}-\frac{x^{2}}{4}=1

**Theorem Sequence**:  
Hyperbola_Equation_Standard_Y, Hyperbola_Asymptote

---

## Problem Index: 74
**ID**: 75
**Text**:  
已知椭圆$C$:$\frac{x^{2}}{a^{2}}+\frac{y^{2}}{b^{2}}=1  (a>b>0)$的右准线与$x$轴交于点$A$，点$B$的坐标为$(0, a)$，若椭圆上的点$M$满足$\overrightarrow {A B}=3 \overrightarrow {A M}$，则椭圆$C$的离心率值为?

**Process**:  
由\overline{A}\overline{B}=3\overline{A}\overline{M},得M(\frac{2a^{2}}{3c},\frac{1}{3}a),将M坐标代入\frac{x^{2}}{a^{2}}+\frac{y^{2}}{b^{2}}=1,结合b^{2}=a^{2}-c^{2}化简为\frac{4a^{2}}{9c^{2}}+\frac{a^{2}}{9a^{2}-9c^{2}}=1得\frac{4}{9e^{2}}+\frac{1}{9-9e^{2}}=1解得e^{2}=\frac{2}{3},e=\frac{\sqrt{6}}{3}.【思路点晴】本题主要考查的是椭圆的简单几何性质和向量共线的性质,属于难题.本题先由\overline{AB}=3\overline{AM}利用向量共线的性质和已知的A(\frac{a^{2}}{c},0),B(0,a)点坐标,求出M点的坐标M(\frac{2a^{2}}{3c},\frac{1}{3}a),通过该点在椭圆上,代入方程\frac{x^{2}}{a^{2}}+\frac{y^{2}}{3^{2}}=1,转化得到关于a,c的方程,由此计算出椭圆的离心率.老点:1.进线向量:2椭圆的离心率

**Theorem Sequence**:  
Ellipse_Equation_Standard_X, Ellipse_Definition, Ellipse_Focal_Radius, Eccentricity_Formula

---

## Problem Index: 138
**ID**: 139
**Text**:  
已知抛物线$C_{1}$的顶点在坐标原点，准线为$x=-3$，圆$C_{2}$:$(x-3)^{2}+y^{2}=1$，过圆心$C_{2}$的直线$l$与抛物线$C_{1}$交于点$A$ , $B$ , $l$与圆$C_{2}$交于点$M$，$N$，且$|A M|<|A N|$，则$|A M|+\frac{1}{4}| B M |$的最小值为?

**Process**:  
设抛物线的方程:y^{2}=2px(p>0),由准线方程x=-3可得\frac{p}{2}=3,即p=6,抛物线的标准方程为y^{2}=12x,焦点坐标F(3,0)圆C_{2}:(x\cdot3)^{2}+y^{2}=1的圆心为(3,0),半径为1由直线AB过抛物线的焦点,利用极坐标,可设A(\rho_{1},\theta),B(\rho_{2},\pi+0)由\rho=\frac{p}{1-\cos\theta},可得\frac{1}{|AF|}+\frac{1}{BF}=\frac{1-\cos\theta}{p}+\frac{1+\cos\theta}{p}=\frac{2}{p}=\frac{1}{3}|AM|+\frac{1}{4}|BM|=|AF|\cdot1+\frac{1}{4}(|BF|+1)=|AF|+\frac{1}{4}|BF|-\frac{3}{4}=3(\frac{1}{1AF}|+\frac{1}{|BF|})(|AF|+\frac{1}{4}|BF|)-\frac{3}{4}+\frac{|AF|}{|BF|}+\frac{|BF|}{4|AF|})-\frac{3}{4}\geqslant3(\frac{5}{4}+2\sqrt{\frac{1}{4}})-\frac{3}{4}=6,当且仅当|BF|=2|AF|=9时取得等号,则|AM|+\frac{1}{4}|BM|的最小值为6.

**Theorem Sequence**:  
Parabola_Equation_Standard_Right, Parabola_Definition, Parabola_Directrix, Trapezoid_Midline_Theorem, Basic_Inequality

---

## Problem Index: 147
**ID**: 148
**Text**:  
已知双曲线经过点$(2 \sqrt{2}, 1)$，其一条渐近线方程为$y=\frac{1}{2} x$，则该双曲线的标准方程为?

**Process**:  
设双曲线方程为:mx^{2}+ny^{2}=1(mn<0),由题意可知:\begin{cases}8m+n=1\\\sqrt{-\frac{m}{n}}=\frac{1}{2}\end{cases}解得:\begin{cases}m=\frac{1}{4}\\n=1\end{cases}双曲线的方程为:x^{2}-y2=1.

**Theorem Sequence**:  
Hyperbola_Equation_Standard_X, Hyperbola_Parameter_Relation

---

## Problem Index: 152
**ID**: 153
**Text**:  
已知点$P$为抛物线$y^{2}=4 x$上一个动点，$Q$为圆$x^{2}+(y-4)^{2}=1$上一个动点，当点$P$到点$Q$的距离与点$P$到抛物线的准线的距离之和最小时，点$P$的横坐标为?

**Process**:  
根据抛物线的定义可知,点P到抛物线y^{2}=4x的准线的距离等于其到焦点F(1,0)的距离,所以点P到点Q的距离与点P到抛物线的准线的距离之和等于|PF|与P到圆x^{2}+(y-4)^{2}=1的圆心C(0,4)的距离之和减去半径1的值,直线FC的方程为y=-4x+4,由方程组\begin{cases}y=-4\\y=2=4x\end{cases}4x+4\_可得x=\frac{9-\sqrt{17}}{8}.

**Theorem Sequence**:  
Parabola_Equation_Standard_Right, Circle_Standard_Equation, Two_Points_Distance

---

## Problem Index: 183
**ID**: 184
**Text**:  
若抛物线$y^{2}=8 x$的焦点$F$与双曲线$\frac{x^{2}}{3}-\frac{y^{2}}{n}=1$的一个焦点重合，则$n$的值为?

**Process**:  
已知抛物线y^{2}=8x,则其焦点F坐标为(2,0)双曲线\frac{x^{2}}{3}-\frac{y^{2}}{n}=1的右焦点为(\sqrt{3+n},0)所以\sqrt{3+n}=2,解得n=1,

**Theorem Sequence**:  
Parabola_Equation_Standard_Right, Hyperbola_Equation_Standard_X

---

## Problem Index: 185
**ID**: 186
**Text**:  
椭圆的长轴为$A_{1} A_{2}$, $B$为短轴一端点，若$\angle A_{1} B A_{2}=120^{\circ}$，则椭圆的离心率为?

**Process**:  
由题意椭圆的长轴为A_{1}A_{2},B为短轴的一端点,若\angleA_{1}BA_{2}=120^{\circ},得出\angleA_{1}A_{2}B=30^{\circ}故\angleA_{2}BO=60^{\circ},由此知\frac{b}{a}=\frac{\sqrt{3}}{3},即\frac{b^{2}}{a^{2}}=\frac{1}{3},即\frac{a2-c^{2}}{a^{2}}=\frac{1}{3}整理得1-e^{2}=\frac{1}{3}解得e=\frac{\sqrt{6}}{3}

**Theorem Sequence**:  
Ellipse_Equation_Standard_X, Ellipse_Focal_Triangle_Perimeter, Eccentricity_Formula

---

## Problem Index: 220
**ID**: 221
**Text**:  
若双曲线$x^{2}+m y^{2}=1$的焦距等于虚轴长的$3$倍，则$m$的值为?

**Process**:  
先将双曲线化为标准形式,进而得到a^{2}=1,b^{2}=-\frac{1}{m},c^{2}=1-\frac{1}{m},根据题意列出方程,求出m的值.详解】x^{2}+my^{2}=1化为标准方程:x^{2}-\frac{y^{2}}{-\frac{1}{m}}=1则a^{2}=1,b^{2}=-\frac{1}{m},故c^{2}=1-\frac{1}{m},则可得:2\sqrt{1-\frac{1}{m}}=6\sqrt{-\frac{1}{m}}解得:m=-8,

**Theorem Sequence**:  
Hyperbola_Equation_Standard_X, Hyperbola_Parameter_Relation

---

## Problem Index: 236
**ID**: 237
**Text**:  
若双曲线的一条渐近线经过点$(8,-6)$，则其离心率等于?

**Process**:  
设一条渐近线方程为y=kx,由题意知-6=8k,得k=-\frac{3}{4}\therefore渐近线方程为y=-\frac{3}{4}x若焦点在x轴上,则\frac{b}{a}=\frac{3}{4},于是离心率e=\frac{c}{a}=\sqrt{1+}\frac{2}{12}若焦点在y轴上,则\frac{a}{b}=\frac{3}{4},于是离心率e=\frac{c}{a}=\sqrt{1+(\frac{b}{a})^{2}}=\frac{5}{3}

**Theorem Sequence**:  
Hyperbola_Equation_Standard_X, Hyperbola_Asymptote, Eccentricity_Formula

---

## Problem Index: 266
**ID**: 267
**Text**:  
设$F_{1}$ , $F_{2}$分别为双曲线$\frac{x^{2}}{a^{2}}-\frac{y^{2}}{b^{2}}=1  (a>0 , b>0)$的左、右焦点，若双曲线上存在一点$P$，使得$|P F_{1}|+|P F_{2}|=3 b$ ,$|P F_{1}| \cdot|P F_{2}|=\frac{9}{4} a b$，则该双曲线的离心率为?

**Process**:  
因为点P在双曲线\frac{x^{2}}{a^{2}}-\frac{y^{2}}{b^{2}}=1(a>0,b>0)上,所以||PF_{1}|-|PF_{2}||=2a,即(|PF_{1}|-|PF_{2}|)^{2}=4a^{2},因为(|PF_{1}|-|PF_{2})^{2}=(|PF_{1}|+|PF_{2}|)^{2}-4|PF_{1}|\cdot|PF_{2}|,所以9b^{2}-9ab=4a^{2},解得:b=\frac{4}{3}a或b=-\frac{1}{3}a(舍去),所以该双曲线的离心率为e=\frac{c}{a}=\sqrt{\frac{c^{2}}{a^{2}}}=\sqrt{\frac{a2+b^{2}}{a^{2}}}=\sqrt{1+\frac{b^{2}}{a2}}=\sqrt{1+\frac{16}{9}}=\frac{5}{3},所以答案应填:\frac{5}{3}

**Theorem Sequence**:  
Hyperbola_Equation_Standard_X, Hyperbola_Definition, Ellipse_Definition, Pythagorean_Theorem, Eccentricity_Formula

---

## Problem Index: 291
**ID**: 292
**Text**:  
已知抛物线$x^{2}=4 y$，焦点是$F(0,1)$ , $A$为抛物线上一动点，以$A F$为直径的圆与定直线相切，则直线的方程为?

**Process**:  
易知F(0,1)为抛物线x^{2}=4y的焦点,设点A(x_{0},y_{0}),由抛物线的定义可得|AF|=y_{0}+1,所以,圆心M到x轴的距离恒等于半径\frac{|AF|}{2},所以定直线的方程为y=0.

**Theorem Sequence**:  
Parabola_Equation_Standard_Right, Parabola_Definition, Parabola_Focal_Radius, Circle_Standard_Equation

---

## Problem Index: 301
**ID**: 302
**Text**:  
已知双曲线$C$: $\frac{x^{2}}{a^{2}}-\frac{y^{2}}{b^{2}}=1(a>0, b>0)$的焦点为$F_{1}$、$F_{2}$，离心率为$\frac{\sqrt{6}}{2}$，若$C$上一点$P$满足$|P F_{1}|-|PF_{2}|=2 \sqrt{6}$，则$C$的方程为?

**Process**:  
\because|PF_{1}|-|PF_{2}|=2\sqrt{6},由双曲线的定义可知a=\sqrt{6}由e=\frac{c}{a}=\frac{\sqrt{6}}{2},得c=3,则b^{2}=c^{2}-a^{2}=3,所以双曲线C的方程为\frac{x^{2}}{6}-\frac{y^{2}}{3}=1

**Theorem Sequence**:  
Hyperbola_Equation_Standard_X, Hyperbola_Definition, Eccentricity_Formula

---

## Problem Index: 322
**ID**: 323
**Text**:  
$F_{1}$、$F_{2}$分别为双曲线$\frac{x^{2}}{a^{2}}-\frac{y^{2}}{b^{2}}=1(a>0, b>0)$的左、右焦点，过点$F_{2}$作此双曲线一条渐近线的垂线，垂足为$M$，满足$|\overrightarrow{M F_{1}}|=3|\overrightarrow{M F_{2}}|$，则此双曲线的渐近线方程为?

**Process**:  
设点F_{2}(c,0)到渐近线y=\frac{b}{a}x的距离为d=\frac{|bc|}{\sqrt{1+(\frac{b}{a})^{2}}}=b,即|\overrightarrow{MF_{2}}|=b又|\overrightarrow{MF_{1}}|=3|\overrightarrow{MF_{2}}|.所以|\overrightarrow{MF_{1}}|=3b,在\triangleMF_{1}O中,|\overrightarrow{OM}|=a,|\overrightarrow{OF}|=c,\cos\angleF_{1}OM=-\frac{a}{c},由余弦定理得:\frac{a^{2}+c^{2}-9b^{2}}{2ac}=-\frac{a}{c}又c^{2}=a^{2}+b^{2},得a^{2}=2b^{2},即\frac{b}{a}=\frac{\sqrt{2}}{2}所以渐近线方程为y=\pm\frac{\sqrt{2}}{2}x

**Theorem Sequence**:  
Hyperbola_Equation_Standard_X, Hyperbola_Asymptote, Hyperbola_Focus_To_Asymptote_Distance, Eccentricity_Formula

---

## Problem Index: 326
**ID**: 327
**Text**:  
已知$F_{1}$、$F_{2}$是双曲线$\frac{x^{2}}{a^{2}}-\frac{y^{2}}{b^{2}}=1(a>0, b>0)$的左右焦点，过点$F_{2}$作双曲线的一条渐近线的垂线，垂足为点$A$，交另一条渐近线于点$B$，且$\overrightarrow{A F_{2}}=-\frac{1}{2} \overrightarrow{F_{2} B}$，则该双曲线的离心率为?

**Process**:  
注意到在\triangleF_{2}BF_{1}中,OA为中位线,可得\triangleOBF_{1}为等边三角形,从而得到2a=c,e=2.[详解]由题意知在\triangleBF_{1}F_{2},A为边BF_{2}的中点,BF_{1}\botBF_{2},|OA|=a,|BF|=2a,|OB|=c\because\triangleOBF为等腰三角形,又\because\angleAOF_{2}=\angleBOF_{1}=\angleBF_{1}O,\therefore\triangleOBF为等边三角形\therefore2a=c,e=2b然安为.2

**Theorem Sequence**:  
Ellipse_Equation_Standard_X, Ellipse_Definition, Ellipse_Focal_Triangle_Perimeter, Eccentricity_Formula

---

## Problem Index: 354
**ID**: 355
**Text**:  
双曲线$9 x^{2}-16 y^{2}=-144$的实轴长等于?其渐近线与圆$x^{2}+y^{2}-2 x+m=0$相切，则$m$=?

**Process**:  
将双曲线的方程化为标准方程:\frac{y2}{9}-\frac{x^{2}}{16}=1,\therefore实轴长2\cdot3=6,渐近线方程为3x\pm4y=0,将圆的方程化为标准方程:(x-1)^{2}+y^{2}=1-m,\therefore\frac{3}{\sqrt{3^{2}+4^{2}}}=\sqrt{1-m}\Rightarrowm=\frac{16}{25},故填:6,\frac{16}{25}

**Theorem Sequence**:  
Hyperbola_Equation_Standard_X, Hyperbola_Asymptote, Circle_Standard_Equation

---

## Problem Index: 385
**ID**: 386
**Text**:  
椭圆$C_{1}$方程为$\frac{x^{2}}{a^{2}}+\frac{y^{2}}{b^{2}}=1$，双曲线$C_{2}$的方程为$\frac{x^{2}}{a^{2}}-\frac{y^{2}}{b^{2}}=1$ , $C_{1}$ , $C_{2}$的离心率之积为$\frac{\sqrt{3}}{2}$，则$C_{2}$的渐近线方程为?

**Process**:  
两个曲线的离心率分别是e_{1}=\frac{\sqrt{a^{2}-b^{2}}}{a},e_{2}=\frac{\sqrt{a^{2}+b^{2}}}{a},乘积为\frac{\sqrt{a^{4}-b^{4}}}{a^{2}}=\frac{\sqrt{3}}{2}解得\frac{b^{4}}{a^{4}}=\frac{1}{4},\frac{b}{a}=\frac{\sqrt{2}}{2},所以双曲线的渐近线方程是y=\pm\frac{b}{a}x=\pm\frac{\sqrt{2}}{2}x

**Theorem Sequence**:  
Ellipse_Equation_Standard_X, Hyperbola_Definition, Eccentricity_Formula

---

## Problem Index: 400
**ID**: 401
**Text**:  
已知直线$l$: $x-y+m=0$与双曲线$x^{2}-\frac{y^{2}}{2}=1$交于不同的两点$A$、$B$，若线段$A B$的中点在圆$x^{2}+y^{2}=5$上，则$m$的值是?

**Process**:  
设点A(x_{1},y_{1}),B(x_{2},y_{2}),线段AB的中点M(x_{0},y_{0}),由\begin{cases}x-y+m=0\\x^{2}-\frac{y^{2}}{2}=1\end{cases},得x^{2}-2mx-m^{2}-2=0(判别式\triangle>0)\becausex_{1}+x_{2}=2m,\thereforex_{0}=\frac{x_{1}+x_{2}}{2}=m,y_{0}=x_{0}+m=2m,\because点M(x_{0},y_{0})在圆x^{2}+y^{2}=5上,则m^{2}+(2m)^{2}=5,故m=\pm1

**Theorem Sequence**:  
Hyperbola_Equation_Standard_X, Point_Difference_Method_Hyperbola, Circle_Standard_Equation

---

## Problem Index: 420
**ID**: 421
**Text**:  
若抛物线$y^{2}=4 x$上的点$M$到焦点的距离为$11$，则$M$到$y$轴的距离是?

**Process**:  
抛物线的准线为x=-1,\because点M到焦点的距离为11,\therefore点M到准线x=-1的距离为11,\therefore点M到y轴的距离为10,

**Theorem Sequence**:  
Parabola_Equation_Standard_Right, Parabola_Definition, Parabola_Directrix

---

## Problem Index: 423
**ID**: 424
**Text**:  
已知抛物线$C$: $y^{2}=8 x$，其焦点为点$F$，点$P$是抛物线$C$上的动点，过点$F$作直线$(m+1) x+y-4 m-6=0$的垂线，垂足为$Q$，则$|P Q|+|P F|$的最小值为?

**Process**:  
将已知直线(m+1)x-4m+y-6=0化为m(x-4)+x+y-6=0,当x=4时y=2,可确定直线过定点(4,2),记为M点.\because过点F做直线(m+1)x-4m+y-6=0的垂线,垂足为Q\thereforeFQ\bot直线(m+1)x-4m+y-6=0,即FQ\botMQ,\angleFQM=90^{\circ}故Q点的轨迹是以FM为直径的圆,半径r=\sqrt{2},其圆心为FM的中点,记为点H,\thereforeH(3,1)\becauseP在抛物线C:y^{2}=8x上,其准线为x=-2\therefore|PF|等于P到准线的距离.过P作准线的垂线,垂足为R.要使|PF|+|PQ|取到最小,即|PR|+|PQ|最小此时R、P、Q三点共线,且三点连线后直线RQ过圆心H.如图所示,此时(|PR|+|PQ|)=HR-r=5-\sqrt{2}

**Theorem Sequence**:  
Parabola_Equation_Standard_Right, Substitution_x_equals_my_plus_n, Parabola_Definition, Parabola_Directrix, Point_To_Line_Distance

---

## Problem Index: 429
**ID**: 430
**Text**:  
已知$B_{1}$、$B_{2}$是椭圆$C$:$\frac{x^{2}}{a^{2}}+\frac{y^{2}}{b^{2}}=1(a>b>0)$的两个短轴端点，$P$是椭圆上任意一点，$|P B_{1}| \leq|B_{1} B_{2}|$，则该椭圆离心率的取值范围是?

**Process**:  
P是椭圆上任意一点,设P(a\cos\theta,b\sin\theta),\theta\in[0,2\pi),由|PB_{1}|\leqslant|B_{1}B_{2}|,根据两点的距离公式,有\sqrt{(a\cos\theta)^{2}+(b\sin\theta-b)^{2}}\leqslant2b,整理得(a^{2}-b^{2})\sin^{2}\theta-2b^{2}\sin\theta+3b^{2}-a^{2}\geqslant0,即关于\sin\theta的二次函数在区间[-1,1]非负,讨论函数的对称轴,函数最小值大于等于0时满足题意,此时再由离心率公式即得.解】由题,设P(a\cos\theta,b\sin\theta),\theta\in[0,2\pi),由|PB_{1}|\leqslant|B_{1}B_{2}|,可得\sqrt{(a\cos\theta)^{2}+(b\sin\theta-b)^{2}}\leqslant2b,即(a\cos\theta)^{2}+(b\sin\theta-b)^{2}\leqslant4b^{2}整理得:(a^{2}-b^{2})\sin^{2}\theta-2b^{2}\sin\theta+3b^{2}-a^{2}\geqslant0,即为关于\sin\theta的二次函数在区间[-1,19又关于\sin\theta的二次函数开口朝上,则讨论对称轴是否在区间(-1,1)当0<\frac{b^{2}}{a2-b^{2}}<1时,对称轴在区间(-1,1)内,又\sin\theta=1时,有(a^{2}-b^{2})\sin^{2}\theta-2b^{2}\sin\theta+3b^{2}-a^{2}=0,故此二次函数最低点小于0当\frac{b^{2}}{a2-b^{2}}\geqslant1时,对称轴在区间(-1,1)外,此时二次函数最小值在端点取到由\sin\theta=1时,有(a^{2}-b^{2})\sin^{2}\theta-2b^{2}\sin\theta+3b^{2}-a^{2}=0\sin\theta=-1时,有(a^{2}-b^{2})\sin^{2}\theta-2b^{2}\sin\theta+3b^{2}-a^{2}=4b^{2}>0.此时(a^{2}-b^{2})\sin^{2}\theta-2b^{2}\sin\theta+3b^{2}-a^{2}\geqslant0恒成立,故\frac{b^{2}}{a^{2}-b^{2}}\geqslant1即\frac{a^{2}-c^{2}}{c^{2}}\geqslant1,故a^{2}\geqslant2c^{2},(\frac{c}{a})^{2}=\frac{c^{2}}{a^{2}}\leqslant\frac{1}{2},则e=\frac{c}{a}\leqslant\frac{\sqrt{2}}{2},即e\in(0,\frac{\sqrt{2}}{2}

**Theorem Sequence**:  
Ellipse_Equation_Standard_X, Ellipse_Tangent_Line, Vector_Collinear_Condition, Ellipse_Eccentricity_Range

---

## Problem Index: 440
**ID**: 441
**Text**:  
已知$F_{1}$和$F_{2}$是椭圆$\frac{x^{2}}{3}+y^{2}=1$的两个焦点，则$|F_{1} F_{2}|$=?

**Process**:  
椭圆\frac{x2}{3}+y^{2}=1的a=\sqrt{3},b=1,\thereforec=\sqrt{a^{2}-b^{2}}=\sqrt{2}.即有|F_{1}F_{2}|=2\sqrt{2}

**Theorem Sequence**:  
Hyperbola_Equation_Standard_X, Hyperbola_Asymptote

---

## Problem Index: 464
**ID**: 465
**Text**:  
已知双曲线$C$: $\frac{x^{2}}{a^{2}}-\frac{y^{2}}{b^{2}}=1(a>0, b>0)$的离心率为$\frac{5}{3}$，则双曲线$C$的渐近线方程为?

**Process**:  
因为双曲线C:\frac{x^{2}}{a^{2}}-\frac{y^{2}}{b^{2}}=1(a>0,b>0)的离心率为\frac{5}{3}所以e=\frac{c}{a}=\sqrt{1+(\frac{b}{a})^{2}}=\frac{5}{3}.解得\frac{b}{a}=\frac{4}{3},所以双曲线C的渐近线方程为y=\pm\frac{4}{3}x,

**Theorem Sequence**:  
Hyperbola_Equation_Standard_X, Hyperbola_Asymptote, Eccentricity_Formula

---

## Problem Index: 488
**ID**: 489
**Text**:  
若双曲线$C$: $\frac{x^{2}}{a^{2}}-\frac{y^{2}}{b^{2}}=1(a>0, b>0)$的渐近线与圆$(x-2)^{2}+y^{2}=2$相切，则双曲线$C$的离心率为?

**Process**:  
双曲线C:\frac{x^{2}}{a^{2}}-\frac{y^{2}}{b^{2}}=1(a>0,b>0)的渐近线y=\pm\frac{b}{a}x^{,}即:bx\pmay=0,渐近线与圆(x-2)^{2}+y^{2}=2相切,可得\frac{2b}{\sqrt{a^{2}+b^{2}}}=\sqrt{2},解得a=b,所以双曲线的离心率为\_e=\frac{c}{a}=\frac{\sqrt{2}a}{a}=\sqrt{2}

**Theorem Sequence**:  
Hyperbola_Equation_Standard_X, Hyperbola_Asymptote, Circle_Standard_Equation, Point_To_Line_Distance, Eccentricity_Formula

---

## Problem Index: 528
**ID**: 529
**Text**:  
已知抛物线$C$: $y^{2}=4 x$的焦点为$F$，其准线$l$与$x$轴的交点为$K$，点$P(x, y)(y>0)$为$C$上一点，当$\frac{|P K|}{|P F|}$最大时，直线$K P$的斜率为?

**Process**:  
由题意求出焦点坐标以及准线方程,由抛物线的性质得到到焦点的距离转化为到准线的距离,当\frac{|PK|}{|PF|}最大时,即求\tan\anglePKF的最大值,由均值不等式求出最大值时点P的坐标由题意可得,焦点F(1,0),准线方程为x=过点P作PM垂直准线,垂足为M则|PF|=|PM|,且PM//KF所以\frac{|PK|}{|PF|}=\frac{|PK|}{|PM|}=\frac{}{\cos}因为PM//KF,所以\angleMPK=\anglePKF即\frac{|PK|}{|PF|}=\frac{1}{\cos\anglePKF}(0\leqslant\anglePKF<\frac{\pi}{2})求\frac{|PK|}{|PF|}的最大值,即求\cos\anglePKF的最小值,等价\tan\anglePKF的最大值,设P(\frac{a^{2}}{4},a),a>0,\tan\anglePKF=\frac{a}{\frac{a^{2}}{4}+1}=\frac{1}{\frac{a}{4}+\frac{1}{a}}\leqslant\frac{1}{2\sqrt{\frac{a}{4}\cdot\frac{1}{a}}}=当且仅当\frac{a}{4}=\frac{1}{a},即a=2时取等号,即直线KP的斜率为1

**Theorem Sequence**:  
Parabola_Equation_Standard_Right, Parabola_Definition, Parabola_Directrix, Basic_Inequality

---

## Problem Index: 529
**ID**: 530
**Text**:  
已知点$B$为椭圆$C$: $\frac{x^{2}}{4}+y^{2}=1$的上顶点，过$B$作圆$O$: $x^{2}+y^{2}=r^{2}(0<r<\frac{6}{7})$的切线$l$, $l$与椭圆$C$的另一交点为$Q$，若$O Q=\frac{\sqrt{13}}{2}$，则$r$=?

**Process**:  
B(0,1),设Q(x_{0},y_{0}),则有\frac{x_{0}^{2}}{4}+y_{0}2=1,OQ=\sqrt{x_{0}^{2}+y_{0}^{2}}=\sqrt{x_{0}^{2}+1-\frac{x_{0}^{2}}{4}}=\sqrt{\frac{3}{4}x_{0}^{2}+1}=\frac{\sqrt{13}}{2}\thereforex_{0}=\pm\sqrt{3},不妨设x_{0}=\sqrt{3},则y_{0}=\pm\frac{1}{2},当y_{0}=-\frac{1}{2}时,Q(\sqrt{3},-\frac{1}{2}),k_{BQ}=\frac{1+\frac{1}{2}}{0-\sqrt{3}}=-\frac{\sqrt{3}}{2}BQ:y=-\frac{\sqrt{3}}{2}x+1'即\frac{\sqrt{3}}{2}x+y-1=0O到BQ距离d=\frac{1}{\sqrt{\frac{7}{4}}}=\frac{2}{\sqrt{7}}=\frac{2\sqrt{7}}{7}<\frac{6}{7},此时,\frac{2\sqrt{7}}{7},当y_{0}=\frac{1}{2}时,Q(\sqrt{3},\frac{1}{2}),k_{BQ}=\frac{1-\frac{1}{2}}{0-\sqrt{3}}=-\frac{\sqrt{3}}{6},BQ:\frac{\sqrt{3}}{6}x+y-1=0'O到BQ距离d=\frac{1}{\sqrt{\frac{13}{2}}}=\frac{\sqrt{156}}{13}>\frac{6}{7},舍去,\therefore_{r=\frac{2\sqrt{7}}{7}}数答客为:2\sqrt{7}

**Theorem Sequence**:  
Ellipse_Equation_Standard_X, Ellipse_Tangent_Line, Two_Points_Distance, Basic_Inequality

---

## Problem Index: 562
**ID**: 563
**Text**:  
已知斜率为$k$的直线$L$与椭圆$C$: $\frac{x^{2}}{6}+\frac{y^{2}}{3}=1$相交于$A$、$B$两点，若线段$A B$的中点为$M(-1,1)$，则$k$的值是?

**Process**:  
设A(x_{1},y_{1}),B(x_{2},y_{2}),代入椭圆方程得:\begin{cases}\frac{x^{2}}{6}+\frac{y^{2}}{3}=1\\\frac{x^{2}}{6}+\frac{y^{2}}{3}=1\end{cases}上下两式作差可得:\frac{x_{1}^{2}-x_{2}^{2}}{6}+y_{1}^{2}-y_{2}^{2}即:\frac{(x_{1}+x_{2})(x_{1}-x_{2})}{\thereforek_{AB}=\frac{y_{1}-y_{2}}{x_{1}}-x_{2}}=-\frac{1}{2}、又线段AB的中点为M(-1,1)\thereforex_{1}+x_{2}=-2,y_{1}+y_{2}=2\Rightarrowk_{AB}=\frac{1}{2}本题正确结果:\frac{1}{2}

**Theorem Sequence**:  
Ellipse_Equation_Standard_X, Vector_Collinear_Condition

---

## Problem Index: 563
**ID**: 564
**Text**:  
已知抛物线$C$的焦点为$F$，点$A$、$B$在$C$上，满足$\overrightarrow{A F}+\overrightarrow{B F}=\overrightarrow{0}$，且$\overrightarrow{A F} \cdot \overrightarrow{B F}=-16$，点$P$是抛物线的准线上任意一点，则$\Delta P A B$的面积为?

**Process**:  
设抛物线C:y2=2px(p>0),因为\overrightarrow{AF}+\overrightarrow{BF}=\overrightarrow{0},所以F是线段AB的中点,易得AB与x轴垂直,继而可得\overrightarrow{AF}\cdot\overrightarrow{BF}=-p^{2}=-16,求出p的值,再由|AB|=2p,点P到AB的距离为p计算\trianglePAB的面积即可.详解】不妨设抛物线C:y2=2px(p>0)因为\overrightarrow{AF}+\overrightarrow{BF}=\overrightarrow{0},所以\overrightarrow{AF}=\overrightarrow{FB},所以F是线段AB的中点,则AB与x轴垂直所以\overrightarrow{AF}\cdot\overrightarrow{BF}=-p^{2}=-16,所以p=4,|AB|=2p=8,点P到AB的距离为p=4,所以S_{\trianglePAB}=\frac{1}{2}\times8\times4=16.

**Theorem Sequence**:  
Parabola_Equation_Standard_Right, Substitution_x_equals_my_plus_n, Vieta_Theorem_Sum, Vieta_Theorem_Product, Vector_Collinear_Condition, Triangle_Area_Formula

---

## Problem Index: 582
**ID**: 583
**Text**:  
已知椭圆$C$的左、右焦点分别为$F_{1}(-3,0)$和$F_{2}(3,0)$，且其图像过定点$M(0,4)$，则$C$的离心率$e$=?

**Process**:  
由题意得c=3,b=4\thereforea=5,e=\frac{3}{5}

**Theorem Sequence**:  
Ellipse_Equation_Standard_X, Eccentricity_Formula

---

## Problem Index: 595
**ID**: 596
**Text**:  
椭圆$x^{2}+m y^{2}=1$的长轴长是短轴长的两倍，则$m$的值为?

**Process**:  
将椭圆方程化为标准形式,分成焦点在x轴、y轴两种情况进行分类讨论,由此求和导m的值[详解]将x^{2}+my^{2}=1转换成x^{2+\frac{y^{2}}{1}}=1,当焦点在x轴时,长轴长是2,短轴长是2\sqrt{\frac{1}{m}}=1,则m=4,当焦点在y轴时,短轴长是2,长轴长是2\sqrt{\frac{1}{m}}=4,则m=\frac{1}{4}.综上填4或\frac{1}{4}

**Theorem Sequence**:  
Ellipse_Equation_Standard_X, Eccentricity_Formula

---

## Problem Index: 632
**ID**: 633
**Text**:  
抛物线$y^{2}=-8 x$上到焦点距离等于$6$的点的坐标是?

**Process**:  
\because抛物线方程为y^{2}=8x,可得2p=8,\frac{p}{2}=2.\therefore抛物线的焦点为F(-2,0),准线为x=2设抛物线上点P(m,n)到焦点F的距离等于6根据抛物线的定义,得点P到F的距离等于P到准线的距离,即|PF|=-m+2=6,解得m=-4,\thereforen^{2}=8m=32,可得n=\pm4\sqrt{2},因此,点P的坐标为(-4,\pm4\sqrt{2})

**Theorem Sequence**:  
Parabola_Equation_Standard_Right, Parabola_Definition, Parabola_Directrix

---

## Problem Index: 639
**ID**: 640
**Text**:  
抛物线顶点是坐标原点，焦点是椭圆$x^{2}+4 y^{2}=1$的一个焦点，则此抛物线方程?

**Process**:  
椭圆x^{2}+4y^{2}=1\thereforex^{2}+\frac{y^{2}}{4}=1\thereforea^{2}=1,b^{2}=\frac{1}{4}\thereforec^{2}=\frac{3}{4},焦点为\pm\frac{\sqrt{3}}{2},0,所以抛物线方程为y^{2}=\pm2\sqrt{3}x

**Theorem Sequence**:  
Ellipse_Equation_Standard_X, Parabola_Equation_Standard_Right

---

## Problem Index: 656
**ID**: 657
**Text**:  
双曲线$C$与双曲线$x^{2}-\frac{y^{2}}{4}=1$有公共的渐近线，且$C$过点$(2,0)$，则$C$的标准方程为?

**Process**:  
设C的标准方程为x2-\frac{y^{2}}{4}=\lambda(\lambda\neq0),因为点(2,0)在双曲线上,所以\lambda=2^{2}=4,故C的标准方程为x^{2}-\frac{y^{2}}{4}=4,即\frac{x^{2}}{4}-\frac{y^{2}}{16}=1答案:\frac{x^{2}}{4}-\frac{y^{2}}{16}=1

**Theorem Sequence**:  
Hyperbola_Equation_Standard_X, Hyperbola_Asymptote

---

## Problem Index: 665
**ID**: 666
**Text**:  
已知双曲线$C$的渐近线方程为$2 x \pm 3 y=0$，写出双曲线$C$的一个标准方程?

**Process**:  
双曲线C的渐近线方程为2x\pm3y=0可得双曲线方程为:\frac{x^{2}}{9}-\frac{y^{2}}{4}=\lambda,\lambda\inR,且\lambda\neq0所求双曲线方程为:\frac{x^{2}}{9}-\frac{y^{2}}{4}=1,答案不唯一.

**Theorem Sequence**:  
Hyperbola_Equation_Standard_X, Hyperbola_Asymptote

---

## Problem Index: 670
**ID**: 671
**Text**:  
已知倾斜角是$60^{\circ}$的直线$l$过抛物线$y^{2}=4 x$的焦点$F$，且与抛物线交于$A$、$B$两点，则弦长$|A B|$=?

**Process**:  
设A(x_{1},y_{1}),B(x_{2},y_{2}),A,B到准线的距离分别为d_{A},d_{B}由抛物线的定义可知|AF|=d_{A}=x_{1}+1,|BF|=d_{B}=x_{2}+1,于是|AB|=|AF|+|BF|=x_{1}+x_{2}+2,由已知得抛物线的焦点为F(1,0),斜率k=\tan60^{\circ}=\sqrt{3},所以直线AB方程为y=\sqrt{3}(x-1)将y=\sqrt{3}(x-1)代入方程y^{2}=4x,化简得3x^{2}-10x+3=0.由求根公式得x_{1}+x_{2}=\frac{10}{3},于是|AB|=|AF|+|BF|=x_{1}+x_{2}+2=\frac{10}{3}+2=\frac{16}{3}

**Theorem Sequence**:  
Parabola_Equation_Standard_Right, Parabola_Definition, Parabola_Focal_Radius, Triangle_Midline_Theorem

---

## Problem Index: 673
**ID**: 674
**Text**:  
直线$A B$过抛物线$y^{2}=4 x$的焦点$F$，且与抛物线交于$A$、$B$两点，且线段$A B$的中点的横坐标是$3$，则直线$A B$的斜率是?

**Process**:  
根据抛物线方程,得到F(1,0),设直线方程为x=my+1,与抛物线方程联\underline{1}y^{2}-4my-4=0,再根据线段AB的中点的横坐标为3,x_{1}+x_{2}=6,求得m,即可得到直线斜率[详解]因为直线AB过抛物线y^{2}=4x的焦点F(1,0)且与抛物线交于A、B两点所以斜率不为0,设直线AB方程为x=my+1,与抛物线方程联立得:y^{2}-4my-4=0,由韦达定理得:y_{1}+y_{2}=4m,y_{1}\cdoty_{2}=-4,所以x_{1}+x_{2}=4m(y_{1}+y_{2})+2=4m^{2}+2=2\times3解得m=\pm1所以直线的方程为x=\pmy+1,所以k_{AB}=\pm1.b女安为.1.或-1

**Theorem Sequence**:  
Parabola_Equation_Standard_Right, Substitution_x_equals_my_plus_n, Vieta_Theorem_Sum, Triangle_Midline_Theorem

---

## Problem Index: 699
**ID**: 700
**Text**:  
已知$F(1,0)$为椭圆$E$: $\frac{x^{2}}{a^{2}}+\frac{y^{2}}{b^{2}}=1  (a>b>0)$的右焦点，过$E$的下顶点$B$和$F$的直线与$E$的另一交点为$A$，若$4 \overrightarrow{B F}=5 \overrightarrow{F A}$，则$a$=?

**Process**:  
由椭圆方程可得B(0,-b),F(1,0)所以k_{BF}=\frac{0-(-b)}{1-0}=b'所以直线BF:y=b(x-1),联立\begin{cases}y=b(x-1)\\\frac{x^{2}}{a^{2}}+\frac{y^{2}}{12}=1\end{cases},整理可得(1+a^{2})x^{2}-2a^{2}x=0,解得x=0或x=\frac{2a^{2}}{1+a^{2}}所以x_{A}=\frac{2a^{2}}{1+a^{2}},所以y_{A}=\frac{b(a^{2}-1)}{1+a^{2}}因为4\overrightarrow{BF}=5\overrightarrow{FA},即4(1,b)=5(\frac{1}{1}所以4l,b)=5(\frac{2a2}{1+a^{2}}-1,\frac{b(a^{2}-1)}{1+a^{2}}),

**Theorem Sequence**:  
Ellipse_Equation_Standard_X, Point_Difference_Method_Hyperbola, Vector_Collinear_Condition, Eccentricity_Formula

---

## Problem Index: 715
**ID**: 716
**Text**:  
已知椭圆$C$: $\frac{x^{2}}{a^{2}}+\frac{y^{2}}{b^{2}}=1(a>b>0)$的离心率为$\frac{\sqrt{3}}{2}$，直线$l$与椭圆$C$交于$A$、$B$两点，且线段$A B$的中点为$M(-2,1)$，则直线$l$的斜率为?

**Process**:  
由椭圆离心率和a,b,c关系可得a,b关系,再由点差法和中点坐标公式、两点的斜率公式可得所求值解】由题意可得e=\frac{c}{a}=\sqrt{1-\frac{b^{2}}{a^{2}}}=\frac{\sqrt{3}}{2},整理可得a=2b,设A(x_{1},y_{1}),B(x_{2},y_{2}),则\frac{x_{1}^{2}}{a^{2}}+\frac{y_{1}^{2}}{b^{2}}=1,\frac{x_{2}2}{a^{2}}+\frac{y_{2}2}{b^{2}}=1两式相减可得\frac{(x_{1}-x_{2})(x}{a^{2}}(y_{1}\becauseAB的中点为M(-2,1),x_{1}+x_{2}=-4,y_{1}+y=2,则直线斜率k=\frac{y_{1}-y_{2}}{x_{1}-x_{2}}=-\frac{b^{2}}{a^{2}}\cdot\frac{x_{1}+x_{2}}{y_{1}+y_{2}}=-\frac{1}{4}\times(-2)=\frac{1}{2}

**Theorem Sequence**:  
Ellipse_Equation_Standard_X, Point_Difference_Method, Eccentricity_Formula

---

## Problem Index: 728
**ID**: 729
**Text**:  
已知直线$l$: $2 x-y+1=0$与抛物线$y^{2}=16 x$交于$A$、$B$两点，过$A$、$B$分别作$l$的垂线与$x$轴交于$C$、$D$两点，则$|C D|$=?

**Process**:  
设A(x_{1},y_{1}),B(x_{2},y_{2})联立方程得:\begin{cases}2x-y+1=0\\y2=16x\end{cases}可得:4x^{2}-12x+1=0,所以x_{1}+x_{2}=3,x_{1}x_{2}=\frac{1}{4}又因为\tan\theta=2,所以\cos\theta=\frac{\sqrt{5}}{5}所以|CD|=\frac{|AB|}{\cos\theta}=10\sqrt{2}.

**Theorem Sequence**:  
Parabola_Equation_Standard_Right, Substitution_x_equals_my_plus_n, Triangle_Midline_Theorem

---

## Problem Index: 738
**ID**: 739
**Text**:  
已知点$A(4,4)$和抛物线$y^{2}=4 x$上两点$B$、$C$，使得$A B \perp B C$，则点$C$的纵坐标的取值范围为?

**Process**:  
设B(\frac{y_{1}^{2}}{4},y_{1}),C(\frac{2}{4},y_{2}),则k_{AB}=\frac{y_{1}-4}{\frac{y_{1}^{2}}{1}-4}=\frac{4}{y_{1}+4},同理k_{BC}=\frac{4}{y_{1}+y_{2}}由k_{AB}\cdotk_{BC}=-1得(y_{1}+4)(y_{1}+y_{2})=-16y_{2}+16=0且y\neq4,根据题意,该方程有实数根,所以A=(y_{2}+4)^{2}-4(4y_{2}+16)=y_{2}^{2}-8y_{2}-48\geqslant0,解得y_{2}\geqslant12或y_{2}\leqslant-4检验当y_{2}=-4时,y_{1}=0;当y_{2}=12时,y_{1}=-8,均满足题意,故点C的纵坐标的取值范围为(-\infty,-4]\cup[12,+\infty).

**Theorem Sequence**:  
Parabola_Equation_Standard_Right, Ellipse_Tangent_Line, Vector_Collinear_Condition, Quadratic_Function_Maximum

---

## Problem Index: 745
**ID**: 746
**Text**:  
$P$为抛物线$C$: $y^{2}=4 x$上一动点，$F$为$C$的焦点，平面上一点$A(3, m)$，若$|P F|+|P A|$的最小值为$4$，则实数$m$的取值范围为?

**Process**:  
抛物线C:y^{2}=4x的准线方程为:l:x=-1,设PB\botl,垂足为B.设P点坐标为(\frac{y^{2}}{4},y).根据抛物线的定义有|PF|+|PA|=|PB|+|PA|,当P线段AB上时,|PF|+|PA|有最小值,最小值为4,符合题意,此时有0\leqslant\frac{y^{2}}{4}\leqslant3,y=m\Rightarrowm\in[-2\sqrt{3},2\sqrt{3}].

**Theorem Sequence**:  
Parabola_Equation_Standard_Right, Parabola_Definition, Parabola_Directrix, Triangle_Midline_Theorem

---

## Problem Index: 758
**ID**: 759
**Text**:  
已知双曲线$C$: $\frac{x^{2}}{a^{2}}-\frac{y^{2}}{b^{2}}=1(a>0, b>0)$的左顶点为$M$，任意一条平行于$x$轴的直线交双曲线$C$于$A$、$B$两点，若总有$\overrightarrow{M A} \cdot \overrightarrow{M B}=0$，则双曲线$C$的离心率为?

**Process**:  
设A(x,y),则B(-x,y),且y^{2}=b^{2}(\frac{x^{2}}{a^{2}}-1),又M(-a,0),所以\overrightarrow{MA}=(x+a,y)\overrightarrow{MB}=(-x+a,y),得\overrightarrow{MA}\cdot\overrightarrow{MB}=-x^{2}+a^{2}+y^{2}=0,即(a^{2}-b^{2})(\frac{x^{2}}{a^{2}}-1)=0对于x<-a或x>a恒成立,故a^{2}=b^{2},即a=b,所以双曲线C的离心率为e=\sqrt{1+\frac{b^{2}}{a^{2}}}=\sqrt{2}

**Theorem Sequence**:  
Hyperbola_Equation_Standard_X, Point_Difference_Method, Vector_Collinear_Condition, Ellipse_Parameter_Relation

---

## Problem Index: 774
**ID**: 775
**Text**:  
已知$F$为双曲线$E$: $\frac{x^{2}}{a^{2}}-\frac{y^{2}}{b^{2}}=1(a>0, b>0)$的右焦点，过点$F$向双曲线$E$的一条渐近线引垂线，垂足为$A$，且交另一条渐近线于点$B$，若$|O F|=|F B|$，则双曲线$E$的离心率是?

**Process**:  
求得双曲线的渐近线方程,结合直角三角形的性质和渐近线的对称性,可得a,b关系,进而可得离心率.双曲线E:\frac{x^{2}}{a^{2}}-\frac{y^{2}}{b^{2}}=1的渐近线方程为y=\pm\frac{b}{a}x'若|OF|=|FB|,可得在直角三角形OAB中.由\angleAOF=\angleBOF=\angleABO=30^{\circ},得\frac{b}{a}=\tan30^{\circ}=\frac{\sqrt{3}}{3},

**Theorem Sequence**:  
Hyperbola_Equation_Standard_X, Hyperbola_Asymptote, Eccentricity_Formula

---

## Problem Index: 775
**ID**: 776
**Text**:  
已知椭圆的方程为$\frac{x^{2}}{16}+\frac{y^{2}}{m^{2}}=1(m>0)$. 如果直线$y=\frac{\sqrt{2}}{2} x$与椭圆的一个交点$M$在$x$轴上的射影恰为椭圆的右焦点$F$，则椭圆的离心率为?

**Process**:  
由椭圆方程得到右焦点的坐标为(\sqrt{16-m^{2}}\because直线与椭圆的一个交点M在x轴的射影恰为椭圆的右焦点F得到MF\botx轴.\thereforeM的横坐标为\sqrt{16-m^{2}}代入到直线方程得到M的纵坐标为\sqrt{\frac{16-m^{2}}{2}}则M(\sqrt{16-m^{2}},\sqrt{\frac{16-m^{2}}{2})}把M的坐标代入椭圆方程得:\frac{16-m^{2}}{16}+\frac{16-m^{2}}{2m^{2}}=1化简得:(m^{2})^{2}+8m^{2}-128=0,即(m^{2}-8)(m^{2}+16)=0解得m^{2}=8,m^{2}=-16(舍去),\becausem>0,\thereforem=2\sqrt{2}.所以椭圆方程为\frac{x^{2}}{16}+\frac{y^{2}}{8}=1,所以a^{2}=16,b^{2}=8,则c^{2}=a^{2}-b^{2}=8所以_{e}=\frac{c}{a}=\frac{2\sqrt{2}}{4}=\frac{\sqrt{2}}{2}故各案为\sqrt{2}

**Theorem Sequence**:  
Ellipse_Equation_Standard_X, Ellipse_Focal_Radius, Eccentricity_Formula

---

## Problem Index: 792
**ID**: 793
**Text**:  
双曲线的方程为$\frac{x^{2}}{16}-\frac{y^{2}}{9}=1$，则其离心率$e$=?

**Process**:  
由题意可得a=4,b=3,c=\sqrt{a^{2}+b^{2}}=5故其离心率为e=\frac{c}{a}=\frac{5}{4}

**Theorem Sequence**:  
Hyperbola_Equation_Standard_X, Hyperbola_Parameter_Relation, Eccentricity_Formula

---

## Problem Index: 800
**ID**: 801
**Text**:  
已知$F_{1}$、$F_{2}$分别为双曲线$\frac{x^{2}}{a^{2}}-\frac{y^{2}}{b^{2}}=1$的左、右焦点，$P$为双曲线右支上一点，满足$|P F_{2}|=|F_{1} F_{2}|$，直线$P F_{1}$与圆$x^{2}+y^{2}=a^{2}$有公共点，则双曲线的离心率的最大值是?

**Process**:  
结合平面几何性质得到|F_{1}M|=\frac{a+c}{2},进而结合勾股定理求得|OM|^{2}=c^{2}-(\frac{a+c}{2})^{2},然后根据直线PF_{1}与圆x^{2}+y^{2}=a^{2}有公共点得到|OM|^{2}\leqslanta^{2},从而得到a,c的齐次式,进而解不等式即可求出结果.|\_PF_{1}于N,因为|PF_{2}|=|F_{1}F_{2}|,所以|PN|=|F_{1}N|又因为|OF_{2}|=|F_{1}O|,所以|MN|=|F_{1}M|,故|F_{1}M|=\frac{1}{4}|F_{1}P|,又因为|PF_{1}|-|PF_{2}|=2a,且|PF_{2}|=|F_{1}F_{2}|=2c,所以|PF_{1}|=2a+2c,因此|F_{1}M|=\frac{a+c}{2},所以|OM|^{2}=c^{2}-(\frac{a+c}{2})^{2},又因为直线PF_{1}与圆x^{2}+y^{2}=a^{2}有公共点,所以|OM|^{2}\leqslanta^{2},故c^{2}-(\frac{a+c}{2})^{2}\leqslanta^{2},即3c^{2}-2ac-5a^{2}\leqslant0,则3e^{2}-2e-5\leqslant0,所以-1\leqslante\leqslant\frac{5}{3},又因为双曲线的离心率e>1,所以1<e\leqslant\frac{5}{3},故离心率的最大值为\frac{5}{3}

**Theorem Sequence**:  
Hyperbola_Definition, Midpoint_Formula, Triangle_Midline_Theorem, Point_To_Line_Distance, Homogenization_Eccentricity, Eccentricity_Formula

---

## Problem Index: 814
**ID**: 815
**Text**:  
过抛物线$y^{2}=4 x$的焦点$F$的直线交抛物线于$A$、$B$两点, 若$\overrightarrow{A F}=2 \overrightarrow{F B}$, 则$|A F|$=?

**Process**:  
过抛物线y^{2}=4x的焦点F的直线交抛物线于A,B两点,且\overrightarrow{AF}=2\overrightarrow{FB}则直线的斜率存在,设直线AB为y=k(x-1),所以\begin{cases}y=k(x-1)\\y2=4x\end{cases},整理可得k^{2}x^{2}-(2k^{2}+4)x+k^{2}=0,设A(x_{1},y_{1}),B(x_{2},y_{2}),则x_{1}x_{2}=1(1)由\overrightarrow{AF}=2\overrightarrow{FB},则x_{1}+1=2(x_{2}+1)(2)将(1)(2)联立可求出x_{1}=2或x_{1}=-1(舍去)所以|AF|=x_{1}+\frac{p}{2}=x_{1}+1=3.

**Theorem Sequence**:  
Parabola_Definition, Substitution_x_equals_my_plus_n, Vieta_Theorem, Vieta_Theorem_Sum, Vieta_Theorem_Product, Ellipse_Definition, Parabola_Focal_Radius

---

## Problem Index: 828
**ID**: 829
**Text**:  
过抛物线$y^{2}=8 x$的焦点的一条直线$l$交抛物线于$A$、$B$两点，若以$A B$为直径的圆的半径为$8$，则直线$l$的倾斜角为?

**Process**:  
分类讨论直线斜率不存在3.存当圆的半径为8时的直线斜率,从而得到直线倾斜角.详解】抛物线y^{2}=8x的焦点坐标为(2,0)所以当直线/斜率不存在时,以AB为直径的圆的半径为4,不符合题意当直线l斜率存在时,设直线l方程为y=k(x-2),代入y^{2}=8x得k^{2}x^{2}-(4k^{2}+8)x+4k^{2}=0,设A(x_{1},y_{1}),B(x_{2},y_{2}),则|AB|=x_{1}+x_{2}+p=\frac{4k^{2}+8}{k^{2}}+4=16解得:k=\pm1,所以直线l的倾斜角为45^{\circ}或135

**Theorem Sequence**:  
Parabola_Equation_Standard_Right, Parabola_Directrix, Parabola_Focal_Chord_Formula_Angle, Chord_Length_Formula_With_K, Discriminant_Delta, Discriminant_Tangent_Condition

---

## Problem Index: 852
**ID**: 853
**Text**:  
点$p(1, m)$是顶点为原点、焦点在$x$轴上的抛物线上一点，它到抛物线的焦点的距离为$2$，则$m$的值为?

**Process**:  
根据顶点为原点、焦点在x轴上的抛物线,点P(1,m)横坐标大于0,知道抛物线开口向右,可以设y^{2}=2px(p>0),准线方程x=-\frac{p}{2},则1+\frac{p}{2}=2,\thereforep=2,抛物线方程为y^{2}=4x,点P(1,m)代得入m=\pm2.

**Theorem Sequence**:  
Parabola_Equation_Standard_Right, Parabola_Directrix

---

## Problem Index: 854
**ID**: 855
**Text**:  
已知$F_{1}$、$F_{2}$是双曲线$C$: $\frac{x^{2}}{a^{2}}-\frac{y^{2}}{b^{2}}=1(a>0, b>0)$的左右焦点，以$F_{1}$为圆心，双曲线的半焦距$c$为半径的圆与双曲线交于$P$、$Q$两点，若$P F_{2}$与圆$F_{1}$相切，则双曲线$C$的离心率为?

**Process**:  
如图所示,根据题意可得PF_{1}=c,F_{1}F_{2}=2c连接PF_{1},可得PF_{1}\botPF_{2},所以PF_{1}^{2}+PF_{2}^{2}=F_{1}F_{2}2,解得PF_{2}=\sqrt{3}c因为PF_{2}-PF_{1}=2a,所以\sqrt{3}c-c=2a,可得e=\frac{c}{a}=\sqrt{3}+1.

**Theorem Sequence**:  
Hyperbola_Definition, Pythagorean_Theorem, Ellipse_Definition, Eccentricity_Formula

---

## Problem Index: 861
**ID**: 862
**Text**:  
已知椭圆$C$: $\frac{x^{2}}{a^{2}}+\frac{y^{2}}{b^{2}}=1(a>b>0)$的左、右焦点分别为$F_{1}$、$F_{2}$，抛物线$y^{2}=2 p x$的焦点与$F_{2}$重合，若点$P$为椭圆和抛物线的一个公共点且$\cos \angle P F_{1} F_{2}=\frac{5}{7}$，则椭圆的离心率为?

**Process**:  
由P在抛物线上可得:\cos\anglePF_{1}F_{2}=\frac{|PF_{2}|}{|PF_{1}|}=\frac{5}{7}又|PF_{1}|+|PF_{2}|=2a,解得|PF_{1}|=\frac{7}{6}a,|PF_{2}|=\frac{5}{6}a.APF_{1}F_{2}中,利用余弦定理可得:\cos\anglePF_{1}F_{2}=\frac{\frac{49}{36}a^{2}+4c^{2}-\frac{25}{36}a^{2}}{2\times\frac{7}{6}a\times2c}=\frac{5}{7}化简得:a^{2}+6c^{2}=5ac所以6e^{2}-5e+1=0,解得e=\frac{1}{2}或e=\frac{1}{3},故填\frac{1}{2}或\frac{1}{3}

**Theorem Sequence**:  
Ellipse_Definition, Cosine_Law, Eccentricity_Formula

---

## Problem Index: 866
**ID**: 867
**Text**:  
已知双曲线$\frac{x^{2}}{a^{2}}-\frac{y^{2}}{b^{2}}=1(a>0 , b>0)$的渐近线方程为$y=\pm \sqrt{3} x$，则它的离心率为?

**Process**:  
由题意,得e=\frac{c}{a}=\sqrt{1+(\frac{b}{a})^{2}}=\sqrt{1+3}=2.

**Theorem Sequence**:  
Hyperbola_Equation_Standard_X, Hyperbola_Parameter_Relation, Eccentricity_Formula

---

## Problem Index: 873
**ID**: 874
**Text**:  
直线$l$: $y=k x+1$与双曲线$C$: $x^{2}-y^{2}=1$仅有一个公共点，则$k$=?

**Process**:  
由\begin{cases}y=kx+1\\x^{2}-y2=1\end{cases}得:(1-k^{2})x^{2}-2kx-2=0,则当:1-k^{2}=0时,即k=\pm1方程(1-k^{2})x^{2}-2kx-2=0有一个根,两曲线有一个公共点.则当:1-k^{2}\neq0时,有一个解,则\triangle=4k^{2}+8(1-k^{2})=0,k=\pm\sqrt{2},综上k=\pm1或k=\pm\sqrt{2},当时直线与双曲线只有一个交点

**Theorem Sequence**:  
Hyperbola_Equation_Standard_X, Hyperbola_Asymptote, Substitution_x_equals_my_plus_n, Vieta_Theorem, Discriminant_Delta, Discriminant_Intersect_Condition

---

## Problem Index: 876
**ID**: 877
**Text**:  
已知焦点在$x$轴上的椭圆的离心率为$\frac{\sqrt{2}}{2}$，且它的长轴长等于圆$O$: $x^{2}+y^{2}-4 x-12=0$的半径，则椭圆的短轴长是?

**Process**:  
圆C的方程可化为(x-2)^{2}+y^{2}=16,半径为4,\therefore椭圆的长轴长2a=4,\thereforea=2.又离心率e=\frac{c}{a}=\frac{\sqrt{2}}{2}\thereforec=\sqrt{2},b=\sqrt{a^{2}-c^{2}}=\sqrt{2}\therefore椭圆的短轴长是2\sqrt{2}

**Theorem Sequence**:  
Circle_Standard_Equation, Ellipse_Equation_Standard_X, Eccentricity_Formula, Ellipse_Parameter_Relation

---

## Problem Index: 882
**ID**: 883
**Text**:  
设双曲线$C$: $\frac{x^{2}}{a^{2}}-\frac{y^{2}}{b^{2}}=1(a>0, b>0)$的右焦点为$F(c, 0)$，直线$l$: $y=\sqrt{2}(x-c)$与双曲线$C$交于$A$、$B$两点若$\overrightarrow{A F}=t \overrightarrow{F B}(t>0)$，则实数$t$的取值范围为?

**Process**:  
设A(x_{1},y_{1}),B(x_{2},y_{2}),联立直线l与双曲线的方程,消去x可以得到一个之次方程利用韦达定理可以得到y_{1}+y_{2}=-\frac{2\sqrt{2}b^{2}c}{b^{2}-2a^{2}}\textcircled{1},y_{1}y_{2}=\frac{2b^{4}}{b^{2}-2a^{2}}\textcircled{2}又由\overrightarrow{AF}=t\overrightarrow{FB}(t>0)可得-y_{1}=ty_{2}\textcircled{3},将\textcircled{3}代入\textcircled{1}\textcircled{2}两式化简可得e^{2}=\frac{3(1-t)^{2}}{(1+t)^{2}},由e^{2}>1即可解得t的取值范围(详解)设A(x_{1},y_{1}),联立\begin{cases}y=\sqrt{2}(x-c)\\\frac{x^{2}}{a^{2}}-\frac{y^{2}}{b^{2}}=1\end{cases}消去x整理得(b^{2}-2a^{2})y^{2}+2\sqrt{2}b^{2}cy+2b^{4}=0\triangle>0,所以y_{1}+y_{2}=-\frac{2\sqrt{2}b^{2}c}{b^{2}-2a2}\textcircled{1},y_{1}y_{2}=\frac{2b^{4}}{b^{2}-2a^{2}}\textcircled{2}因为\overrightarrow{AF}=t\overrightarrow{FB}(t>0),所以-y=ty_{2}\textcircled{3},将\textcircled{3}代入\textcircled{1}\textcircled{2}两式整理得-[\frac{2\sqrt{2}b^{2}c}{(b^{2}-2a^{2})(1-t)}=\frac{2b^{4}}{b^{2}-2a^{2}}则e^{2}=\frac{3(1-t)^{2}}{2}.又双曲线的离心率e\in(1,+\infty)所以e^{2}=\frac{3(1-t)^{2}}{(1+t)^{2}}\in(1,+\infty),解得t\in(0,2-\sqrt{3})\cup(2+\sqrt{3},+\infty)

**Theorem Sequence**:  
Hyperbola_Equation_Standard_X, Substitution_x_equals_my_plus_n, Vieta_Theorem, Vieta_Theorem_Sum, Vieta_Theorem_Product, Vector_Collinear_Condition, Homogenization_Eccentricity, Eccentricity_Formula

---

## Problem Index: 896
**ID**: 897
**Text**:  
已知椭圆$\frac{x^{2}}{4}+\frac{y^{2}}{m}=1$的离心率为$\frac{\sqrt{2}}{2}$，则实数$m$=?

**Process**:  
\textcircled{1}若焦点在x轴上,则m<4,即a^{2}=4,b^{2}=m\thereforec^{2}=a^{2}-b^{2}=4-m\therefore\frac{c^{2}}{a^{2}}=\frac{4-m}{4}=\frac{1}{2},即m=2.\textcircled{2}若焦点在y轴上,则m>4,即a^{2}=m,b^{2}=4\thereforec^{2}=a^{2}-b^{2}=m-4\therefore得到\frac{c^{2}}{a^{2}}=\frac{m-4}{m}=\frac{1}{2},即m=8.

**Theorem Sequence**:  
Ellipse_Equation_Standard_X, Ellipse_Parameter_Relation, Eccentricity_Formula

---

## Problem Index: 973
**ID**: 974
**Text**:  
已知点$M$在抛物线$y^{2}=4 x$上，若以点$M$为圆心的圆与$x$轴和其准线$l$都相切，则点$M$到其顶点$O$的距离为?

**Process**:  
利用已知条件求出M的坐标,然后求解点M到其顶点O的距离.点M在抛物线y^{2}=4x上,若以点M为圆心的圆与x轴和其准线|都相切,设M(x,x+1)可得(x+1)^{2}=4x,解得x=1,所以M(1,2)点M到其顶点O的距离为:\sqrt{2^{2}+1^{2}}=\sqrt{5}数答安为:\sqrt{5}P.tress.to.ter-----物线的简单几何性质,考查了运算能力,属于中档题

**Theorem Sequence**:  
Parabola_Equation_Standard_Right, Parabola_Definition, Point_To_Line_Distance, Quadratic_Function_Maximum

---

## Problem Index: 999
**ID**: 1000
**Text**:  
设$A B$是双曲线$\Gamma$的实轴，点$C$在$\Gamma$上，且$\angle C A B=\frac{\pi}{4}$，若$A B=4$, $B C=\sqrt{26}$，则双曲线的焦距是?

**Process**:  
如图所示,在4ABC中,由余弦定理得CB^{2}=CA^{2}+BA^{2}-2CA\cdotBA\cdot\cos\frac{\pi}{4},解得CA=5\sqrt{2}过C作CM\botx轴于M,CM=5\sqrt{2}\times\cos\frac{\pi}{4}=5,AM=5,\thereforeC(3,5),点C坐标代入双曲线方程得\frac{9}{2^{2}}-\frac{25}{b^{2}}=1,解得b^{2}=20c=\sqrt{a^{2}+b^{2}}=2\sqrt{6},双曲线的焦距是2c=4\sqrt{6}青】本题考查了直线与双曲线的位置关系,利用平面几何知识和圆锥曲线的定义是解此类题的有效方法,属于中档题

**Theorem Sequence**:  
Hyperbola_Equation_Standard_X, Hyperbola_Asymptote, Triangle_Area_Formula, Cosine_Law, Vector_Dot_Product_Algebraic, Eccentricity_Formula

---

## Problem Index: 1005
**ID**: 1006
**Text**:  
已知抛物线$y^{2}=4 x$的焦点$F$和$A(1,1)$，点$P$为抛物线上的动点，则$|P A|+|P F|$取到最小值时,点$P$的坐标为?

**Process**:  
过点P作PB垂直于准线,过A作AH垂直于准线,PA+PF=PA+PB\leqslantAH此时最小,点P与点A的纵坐标相同,所以点P为(\frac{1}{4},1)5.主要考查抛物线的简单几何性质,考查抛物线的最值,意在式些知识的掌握水平和数形结合分析推理能力.(2)解答圆锥曲线问题时,看到焦点和焦半径要联想到曲线的定义提高解题效率.

**Theorem Sequence**:  
Parabola_Equation_Standard_Right, Parabola_Definition, Parabola_Directrix

---

## Problem Index: 1010
**ID**: 1011
**Text**:  
已知椭圆$\frac{x^{2}}{16}+\frac{y^{2}}{12}=1$的焦点为$F_{1}$、$F_{2}$，点$M$在椭圆上，且$M F_{1} \perp x$轴，则点$F_{1}$到直线$F_{2} M$的距离为?

**Process**:  
由椭圆方程知:a=4,b=2\sqrt{3},c=2\becauseMF_{1}\botx轴,即MF_{1}为椭圆的半通径|MF_{1}|=\frac{b^{2}}{a}=3\therefore|MF_{2}|=2a-|MF_{1}|=5设F_{1}到直线F_{2}M的距离为d,则S_{AF_{1}F_{2}M}=\frac{1}{2}|F_{2}M|\cdotd=\frac{1}{2}|F_{1}F_{2}|\cdot|MF_{1}|即\frac{5}{2}d=6,解得:d=\frac{12}{5}

**Theorem Sequence**:  
Ellipse_Equation_Standard_X, Ellipse_Parameter_Relation, Triangle_Area_Formula

---

## Problem Index: 1021
**ID**: 1022
**Text**:  
直线$l$: $y=2(x-\sqrt{5})$过双曲线$C$: $\frac{x^{2}}{a^{2}}-\frac{y^{2}}{b^{2}}=1(a>0, b>0)$的右焦点$F$且与双曲线$C$只有一个公共点, 则$C$的离心率为?

**Process**:  
结合双曲线的性质\frac{b}{a}=2,0=2(c-\sqrt{5}),求出a,c即可.[详解]过双曲线C:\frac{x^{2}}{a^{2}}-\frac{y^{2}}{b^{2}}=1(a>0,b>0)的渐近线方程为y=\frac{b}{a}x因为过双曲线C:\frac{x^{2}}{a^{2}}-\frac{y^{2}}{b^{2}}=1(a>0,b>0)的右焦点F的直线:y=2(x-\sqrt{5})与C只有一个个公共点所以\frac{b}{a}=2,0=2(c-\sqrt{5}),又因为a^{2}+b^{2}=c^{2},解得c=\sqrt{5},a=1,所以e=\frac{c}{a}=\sqrt{5},

**Theorem Sequence**:  
Hyperbola_Equation_Standard_X, Hyperbola_Asymptote, Line_Point_Slope_Form, Hyperbola_Parameter_Relation, Eccentricity_Formula

---

## Problem Index: 1035
**ID**: 1036
**Text**:  
已知圆$M$:$(x-3)^{2}+(y-4)^{2}=4 $,$ O$为坐标原点，过点$P$作圆$M$的切线，切点为$T$，若$P O=P T$，则点$P$的轨迹方程是?

**Process**:  
由(x-3)^{2}+(y-4)^{2}=4可知:M(3,4),半径为2,因为TP是圆M的切线,所以TP\botMT\RightarrowTP^{2}=PM^{2}-TM^{2},设P(x,y),因为PO=PT,所以PO^{2}=PT^{2},即OP^{2}=PM^{2}-TM^{2},所以x^{2}+y^{2}=(x-3)^{2}+(y-4)^{2}-4\Rightarrow6x+8y-21=0,

**Theorem Sequence**:  
Circle_Standard_Equation, Circle_Tangent_Condition, Line_Point_Slope_Form, Hyperbola_Asymptote, Midpoint_Formula, Two_Points_Distance

---

## Problem Index: 1036
**ID**: 1037
**Text**:  
已知双曲线$\frac{x^{2}}{a^{2}}-\frac{y^{2}}{b^{2}}=1(a>0, b>0)$的两条渐近线均与圆$C$: $x^{2}+y^{2}-6 x+5=0$相切，则该双曲线的离心率等于?

**Process**:  
先将圆的方程化为标准方程,再根据双曲线的两条渐近线均和圆C:x^{2}+y^{2}-6x+5=0相切,利用圆心到直线的距离等于半径,可建立几何量之间的关系,从而可求双曲线离心率.[详解]双曲线\frac{x^{2}}{a^{2}}-\frac{y^{2}}{b^{2}}=1(a>0,b>0)的两条渐近线方程为y=\pm\frac{b}{a}x即bx\pmay=0,圆C:x^{2}+y^{2}-6x+5=0化为标准方程(x-3)^{2}+y^{2}=4\thereforeC(3,0),半径为2,\because双曲线\frac{x^{2}}{a^{2}}-\frac{y^{2}}{b^{2}}=1(a>0,b>0)的两条渐近线均与圆C:x^{2}+y^{2}-6x+5=0相切,\frac{3b}{\sqrt{a^{2}+b^{2}}}=2,\therefore9b^{2}=4b^{2}+4a^{2},\therefore5b^{2}=4a^{2},\becauseb^{2}=c^{2}-a^{2},\therefore5(c^{2}-a^{2})=4a^{2},\therefore9a^{2}=5c^{2},\thereforee=\frac{c}{a}=\frac{3\sqrt{5}}{5}\therefore双曲线的离心率等于\frac{3\sqrt{5}}{5}.

**Theorem Sequence**:  
Circle_Standard_Equation, Hyperbola_Asymptote, Point_To_Line_Distance, Circle_Tangent_Condition, Hyperbola_Parameter_Relation, Eccentricity_Formula

---

## Problem Index: 1038
**ID**: 1039
**Text**:  
已知双曲线的渐近线方程为$y=\pm \frac{4}{3} x$, 并且焦距为$20$, 则双曲线的标准方程为?

**Process**:  
因为双曲线的渐近线方程为y=\pm\frac{4}{3}x,所以设双曲线的标准方程为\frac{x^{2}}{9}-\frac{y^{2}}{16}=k;k>0时,有\frac{x^{2}}{9k}-\frac{y^{2}}{16k}=1,又焦距为20,所以9k+16k=(\frac{20}{2})^{2}=100\Rightarrowk=4,;则双曲线的标准方程为\frac{x^{2}}{36}-\frac{y^{2}}{64}=1;k<0时,有\frac{\sqrt[64}{16k}-\frac{x^{2}}{9k}=1,又焦距为20,所以9k+16k=(\frac{20}{2})^{2}=100\Rightarrowk=4,;则双曲线的标准方程为\frac{y^{2}}{64}-\frac{x^{2}}{36}=1

**Theorem Sequence**:  
Hyperbola_Equation_Standard_X, Hyperbola_Asymptote, Hyperbola_Common_Asymptote_System

---

## Problem Index: 1050
**ID**: 1051
**Text**:  
已知点$M$在抛物线$C$: $y^{2}=4 x$上运动，圆$C$过点$(5,0)$ ,$(2, \sqrt{3})$ ,$(3,-2)$，过点$M$引直线$l_{1}$ , $l_{2}$与圆$C$相切，切点分别为$P$、$Q$，则$|P Q|$的取值范围为?

**Process**:  
设圆C'的方程为x^{2}+y^{2}+Dx+Ey+F=0,将(5,0),(2,\sqrt{3}),(3,-2)分别代入,可很13+3D-2E+F=0\begin{cases}25+5D+F=0\\7+2D+\sqrt{3}E+F=0,\\13+3D-2F+F=0\end{cases}解得\begin{cases}D=-6\\E=0\\F=5\end{cases},即圆C':(x-3)^{2}+y^{2}=4;如图,连接MC',C'P,C'Q,PQ,易得C'P\botMP,C'Q\botMQ,MC'\botPQ所以四边形MPC'Q的面积为\frac{1}{2}|MC'|\cdot|PQ|;另外四边形MPC'Q的面积为\triangleMPC'面积的两倍,所以\frac{1}{2}|MC'|\cdot|PQ|=|MP|\cdot|C'P|故|PQ|=\frac{2|MP|\cdot|C'P|}{|MC'|}=\frac{4\sqrt{|C'M|^{2}-4}}{|C'M|}=4\sqrt{1-\frac{4}{|C'M|^{2}}}故当|C'M|最小时,|PQ|最小,设M(x,y),则|MC'|=\sqrt{(x-3)^{2}+y^{2}}=\sqrt{x^{2}-2x+9},所以当x=1时,|MC'|_{\min}=2\sqrt{2},当x=无穷大时,|PQ|趋近圆的直径4,故|PQ|的取值范围为[2\sqrt{2},4)

**Theorem Sequence**:  
Circle_Standard_Equation, Triangle_Area_Formula, Two_Points_Distance

---

## Problem Index: 1053
**ID**: 1054
**Text**:  
双曲线$C$: $\frac{x^{2}}{16}-\frac{y^{2}}{9}=1$的顶点到其渐近线的距离为?

**Process**:  
因为双曲线C:\frac{x2}{16}-\frac{y^{2}}{9}=1的顶点为(\pm4,0),渐近线方程为:y=\pm\frac{b}{a}x=\pm\frac{3}{4}x.即3x\pm4y=0,因此顶点到渐近线的距离为:\frac{|3\times4|}{\sqrt{3^{2}+4^{2}}}=\frac{12}{5}.

**Theorem Sequence**:  
Hyperbola_Equation_Standard_X, Hyperbola_Asymptote, Point_To_Line_Distance

---

## Problem Index: 1071
**ID**: 1072
**Text**:  
已知抛物线$C$: $y^{2}=4 x$的焦点为$F$，准线为$l$，点$P$在抛物线$C$上，$P Q$垂直$l$于点$Q$ , $Q F$与$y$轴交于点$T$、$O$为坐标原点，且$|O T|=2$，则$|P F|$?

**Process**:  
依题意可得F(1,0),l:x=-1,根据抛物线的定义可知|PQ|=|PF|,设PQ与y轴相交于点M,因为|OT|=2,又|OF|=|QM|,所以\triangleTMQ\cong\triangleTOF,所以T为OM的中点,所以|OM|=4即P的纵坐标为4,在y^{2}=4x中令y=4,得x=4,所以|PQ|=x+\frac{p}{2}=4+1=5,所以|PF|=5

**Theorem Sequence**:  
Parabola_Equation_Standard_Right, Parabola_Definition, Parabola_Directrix, Parabola_Focal_Radius

---

## Problem Index: 1073
**ID**: 1074
**Text**:  
设椭圆$\frac{x^{2}}{m^{2}}+\frac{y^{2}}{4}=1$过点$(-2, \sqrt{3})$，则焦距等于?

**Process**:  
因为椭圆\frac{x^{2}}{m^{2}}+\frac{y^{2}}{4}=1过点(-2,\sqrt{3})所以将其代入,得m^{2}=16,所以c^{2}=16-4=12,c=2\sqrt{3}故焦距2c=4\sqrt{3}

**Theorem Sequence**:  
Ellipse_Equation_Standard_X, Ellipse_Parameter_Relation

---

## Problem Index: 1087
**ID**: 1088
**Text**:  
已知椭圆$\frac{x^{2}}{4}+y^{2}=1$与双曲线$\frac{x^{2}}{a^{2}}-y^{2}=1$有公共焦点$F_{1}$、$F_{2}$、$P$是它们的一个公共点，则$S_{\Delta F_{1} P F_{2}}$=?

**Process**:  
由题a^{2}=2,则点P满足\begin{cases}\frac{x2}{2}-y^{2}=1,\\\frac{x^{2}}{4}+y2=1,\end{cases}解得y=\pm\frac{\sqrt{3}}{3},则S_{\triangleF_{1}PF_{2}}=c|y|=1

**Theorem Sequence**:  
Ellipse_Equation_Standard_X, Hyperbola_Equation_Standard_X, Triangle_Area_Formula

---

## Problem Index: 1100
**ID**: 1101
**Text**:  
若顶点在原点的抛物线的焦点与圆$x^{2}+y^{2}-4 x=0$的圆心重合，则该抛物线的准线方程为?

**Process**:  
\because顶点在原点的抛物线的焦点与圆x^{2}+y^{2}-4x=0的圆心重合\therefore抛物线的焦点F(2,0)\therefore该抛物线的准线方程为x=-:

**Theorem Sequence**:  
Parabola_Equation_Standard_Right, Parabola_Directrix

---

## Problem Index: 1105
**ID**: 1106
**Text**:  
已知点$P(1, \sqrt{3})$在双曲线$C$: $\frac{x^{2}}{a^{2}}-\frac{y^{2}}{b^{2}}=1(a>0, b>0)$的渐近线上，$F$为$C$的右焦点，$O$为原点，若$\angle F P O=90^{\circ}$，则$C$的方程为?

**Process**:  
因为双曲线C:\frac{x^{2}}{a^{2}}-\frac{y^{2}}{b^{2}}=1(a>0,b>0)的渐近线方程为y=\pm\frac{b}{a}x,P(1,\sqrt{3})在渐近线上,所以\frac{b}{a}=\angleFOP=60^{\circ},所以OF=c=4,b=2\sqrt{3},a=2,所以C的方程为\frac{x^{2}}{4}-\frac{y^{2}}{12}=1

**Theorem Sequence**:  
Hyperbola_Equation_Standard_X, Hyperbola_Asymptote, Hyperbola_Parameter_Relation

---

## Problem Index: 1106
**ID**: 1107
**Text**:  
点$P(x, y)$是曲线$C$: $\frac{x^{2}}{4}+\frac{y^{2}}{3}=1$上一个动点，则$2 x+\sqrt{3} y$的取值范围为?

**Process**:  
由点P(x,y)是曲线C:\frac{x^{2}}{4}+\frac{y^{2}}{3}=1上一个动点,可设x=2\cos\theta,y=\sqrt{3}\sin\theta,\theta\in[0,2\pi),则2x+\sqrt{3}y=4\cos\theta+3\sin\theta=5\sin(\theta+\alpha),其中\tan\alpha=\frac{4}{3}又5\sin(\theta+\alpha)\in[-5,5],则2x+\sqrt{3}y\in[-5,5].

**Theorem Sequence**:  
Ellipse_Equation_Standard_X, Ellipse_Parametric_Equation, Quadratic_Function_Maximum

---

## Problem Index: 1107
**ID**: 1108
**Text**:  
若抛物线$y^{2}=2 p x(p>0)$上的点$(x_{0} , 2)(x_{0}>\frac{p}{2})$到其焦点的距离为$\frac{5}{2}$，则$p$=?

**Process**:  
由题意2px_{0}=4且x_{0}+\frac{p}{2}=\frac{5}{2},消去x_{0}得p^{2}-5p+4=0,解得p=1或p=4(舍去)

**Theorem Sequence**:  
Parabola_Equation_Standard_Right, Parabola_Directrix

---

## Problem Index: 1115
**ID**: 1116
**Text**:  
若点$P$是曲线$C_{1}$: $y^{2}=16 x$上的动点，点$Q$是曲线$C_{2}$:$(x-4)^{2}+y^{2}=9$上的动点，点$O$为坐标原点，则$|\frac{P Q}{O P}|$的最小值是?

**Process**:  
曲线C_{2}:(x-4)^{2}+y^{2}=9圆心C_{2}(4,0)是抛物线焦点F,半径为3,所以|\frac{PQ}{OP}|\geqslant\frac{|PF|-3}{|OP|},转化为求\frac{|PF|-3}{|OP|}的最小值,设P(x,y),利用焦半径公式和抛物线方程将\frac{|PF|-3}{|OP|}表示为x的函数,化简运用二次函数的最值,即可求解.羊解】抛物线C_{1}:y^{2}=16x的焦点为F(4,0)曲线C_{2}:(x-4)^{2}+y^{2}=9圆心F(4,0),半径为3,\therefore|\frac{PQ}{OP}|\geqslant\frac{|PF|-3}{|OP|},P,Q,F三点共线时等号成立,设P(x,y),x>0则\frac{|PF|-3}{|OP|}=当t=\frac{7}{15},即x=\frac{8}{7}时,\frac{|PF|-3}{|OP|}取得最小值为\frac{\sqrt{15}}{8},所以x=\frac{8}{7}时,|\frac{PQ}{OP}|取得最小值为\frac{\sqrt{15}}{8}

**Theorem Sequence**:  
Parabola_Equation_Standard_Right, Parabola_Definition, Parabola_Directrix, Circle_Standard_Equation, Point_To_Line_Distance, Quadratic_Function_Maximum

---

## Problem Index: 1120
**ID**: 1121
**Text**:  
设$\frac{x^{2}}{25}+\frac{y^{2}}{16}=1$的左焦点为$F_{1}$ , $P(x_{0}, y_{0})$为椭圆上一点，则$|P F_{1}|$的最大值为?

**Process**:  
已知椭圆方程为\frac{x^{2}}{25}+\frac{y^{2}}{16}=1^{1},则a=5,b=4,c=3,左焦点为F_{1}坐标为(-3,0),则\lambda\because-5\leqslantx_{0}\leqslant5,故当x_{0}=5时,即当P(x_{0},y_{0})为椭圆右顶点(5,0)时|PF_{1}|的最大值为8,故|PF_{1}|的最大值为8

**Theorem Sequence**:  
Ellipse_Equation_Standard_X, Ellipse_Parameter_Relation, Ellipse_Definition

---

## Problem Index: 1174
**ID**: 1175
**Text**:  
已知直线$x-m y-2=0$与抛物线$C$: $y^{2}=\frac{1}{2} x$交于$A$、$B$两点.$P$是线段$A B$的中点，过$P$作$x$轴的平行线交$C$于点$Q$，若以$A B$为直径的圆经过$Q$，则$m$=?

**Process**:  
设AB的坐标,直线与抛物线的方程联立求出两根之和,进而求出AB的中点P的坐标,由题意求出Q的坐标,进而求出弦长|AB|,|PQ|,再由题意可得m的值.设A(x_{1},y_{1}),B(x_{2},y_{2}),由\begin{cases}x-my\\y2=\frac{1}{2}x\end{cases}-2=0整理可得2y^{2}-my-2=0,\triangle=m^{2}+8>0,y_{1}+y_{2}=\frac{m}{2},y_{1}y_{2}=-1所以AB的中点P(\frac{m^{2}}{4}+2,\frac{m}{4}),则Q(\frac{m^{2}}{8},\frac{m}{4}),即|PQ|=\frac{m^{2}}{8}+2又|AB|=\sqrt{1+m^{2}}|_{y_{1}}-y_{2}|=\sqrt{1+m^{2}}\sqrt{\frac{m^{2}}{4}+4}所以\sqrt{1+m^{2}}\sqrt{\frac{m^{2}}{4}+4}=2(\frac{m^{2}}{8}+2)即\sqrt{1+m^{2}}=\sqrt{\frac{m^{2}}{4}+4},解得m=\pm2若】本题考杳抛物线的性质及以线段为直径的圆的性质,属于中档题

**Theorem Sequence**:  
Parabola_Equation_Standard_Right, Substitution_x_equals_my_plus_n, Vieta_Theorem, Vieta_Theorem_Sum, Vieta_Theorem_Product, Equal_Area_Method, Point_To_Line_Distance, Triangle_Area_Formula

---

## Problem Index: 1186
**ID**: 1187
**Text**:  
双曲线$E$: $\frac{y^{2}}{a^{2}}-\frac{x^{2}}{b^{2}}=1(a>0, b>0)$的渐近线与圆$C$:$(x-2)^{2}+y^{2}=1$相切，则双曲线$E$的离心率为?

**Process**:  
圆C:(x-2)^{2}+y^{2}=1的圆心(2,0),半径为1双曲线E:\frac{y^{2}}{a^{2}}-\frac{x^{2}}{b^{2}}=1(a>0,b>0)的渐近线y=\pm\frac{a}{b}x因为双曲线E的渐近线与圆C相切,所以\frac{2a}{\sqrt{a2+b^{2}}}=\frac{2a}{c}=1,则e=\frac{c}{a}=2

**Theorem Sequence**:  
Circle_Standard_Equation, Hyperbola_Asymptote, Circle_Tangent_Condition, Eccentricity_Formula

---

## Problem Index: 1206
**ID**: 1207
**Text**:  
已知点$F$为抛物线$E$: $y^{2}=4 x$的焦点，点$A(2, m)$在抛物线$E$上，则$|A F|$=?

**Process**:  
A(2,m)代入抛物线方程,解得m=\pm2\sqrt{2},焦点为(1,0),故|AF|=\sqrt{1+8}=3

**Theorem Sequence**:  
Parabola_Equation_Standard_Right, Parabola_Definition, Parabola_Directrix, Parabola_Focal_Radius, Two_Points_Distance

---

## Problem Index: 1207
**ID**: 1208
**Text**:  
已知直线$l$过抛物线$C$的焦点，且与$C$的对称轴垂直，$l$与$C$交于$A$、$B$两点，$|A B|=12$ , $P$为$C$的准线上的一点，则$\triangle A B P$的面积为?

**Process**:  
分析:可由|AB|=12得出p,从而可得抛物线方程,抛物线的准线方程,因此4ABP的AB边上的高易得.详不妨设抛物线方程为y^{2}=2px,|AB|=2p=12,p=6,\therefore准线方程为x=-3,P到直线AB的距离为6,\thereforeS_{\triangleABP}=\frac{1}{2}\times12\times6=36.

**Theorem Sequence**:  
Parabola_Equation_Standard_Right, Parabola_Definition, Parabola_Directrix, Parabola_Focal_Chord_Formula_Angle, Triangle_Area_Formula

---

## Problem Index: 1212
**ID**: 1213
**Text**:  
已知椭圆的焦点在$x$轴，长轴长$2 a$为$10$，离心率为$\frac{3}{5}$，则该椭圆的标准方程为?

**Process**:  
椭圆的长轴长为10,离心率为\frac{3}{5},可得a=5,c=3,则b=4,焦点在x轴上的椭圆的标准方程为\frac{x2}{16}+\frac{y^{2}}{25}=1

**Theorem Sequence**:  
Ellipse_Equation_Standard_X, Ellipse_Parameter_Relation, Eccentricity_Formula

---

## Problem Index: 1274
**ID**: 1275
**Text**:  
已知椭圆$C$: $\frac{x^{2}}{4}+\frac{y^{2}}{3}=1$ , $A_{1}$, $A_{2}$为长轴的两个端点，点$P$是椭圆上的一点，且满足直线$P A_{1}$的斜率的取值范围是$[1,2]$，则直线$P A_{2}$的斜率的取值范围是?

**Process**:  
首先得到A_{1}(-2,0),A_{2}(2,0),设P(m,n),根据题意计算得到k_{PA_{1}}\cdotk_{PA_{2}}=-\frac{3}{4},再根据1\leqslantk_{PA_{1}}\leqslant2,即可得到答案.详解】由题知:a=2,则A_{1}(-2,0),A_{2}(2,0),设P(m,n),因为k_{PA_{1}}=\frac{n}{m+2},k_{PA_{2}}=\frac{n}{m-2},k_{PA_{1}}\cdotk_{PA_{2}}=\frac{n}{m+2}_{\frac{12-3m^{2}}{4}}=\frac{n^{2}}{m^{2}-4}因为1\leqslantk_{PA_{1}}\leqslant2,所以-\frac{3}{4}\leqslantk_{PA_{2}}\leqslant-\frac{3}{8}

**Theorem Sequence**:  
Ellipse_Equation_Standard_X, Line_Point_Slope_Form, Substitution_x_equals_my_plus_n, Vieta_Theorem, Vieta_Theorem_Sum, Midpoint_Formula, Vector_Perpendicular_Condition, Cosine_Law

---

## Problem Index: 1285
**ID**: 1286
**Text**:  
抛物线$C$: $x=2 p y^{2}(p>0)$的焦点$F$到准线的距离为$2$，过点$F$的直线与$C$交于$A$、$B$两点，$C$的准线与$x$轴的交点为$M$，若$\triangle M A B$的面积为$3 \sqrt{2}$，则$\frac{|A F|}{|B F|}$=?

**Process**:  
抛物线C:x=2py2(p>0)化为标准形式为:y^{2}=\frac{1}{2p}x(p>0)\because抛物线的焦点F到准线的距离为2\therefore\frac{1}{4p}=2,即p=\frac{1}{8}\therefore抛物线方程为y2=4x(p>0),焦点F(1,0)\because过点F的直线与C交于A,B两点\therefore设直线AB方程为:x=my+1与抛物线方程联立得:y^{2}-4my-4=0设A(x_{1},y_{1}),B(x_{2},y_{2}),不妨假设A点在x轴上方,B点在x轴下方则y_{1}+y_{2}=4m,y_{1}y_{2}=-4设点M到直线AB的距离为d则d=\frac{|1+1|}{\sqrt{m^{2}+1}}=\frac{2}{\sqrt{m^{2}+1}}\thereforeS_{\DeltaMAB}=\frac{1}{2}AB\cdotd=\frac{1}{2}\times4(1+m^{2})\times\frac{2}{\sqrt{m^{2}+1}}=4\sqrt{m^{2}+1}=3\sqrt{2}解得:m^{2}=\frac{1}{8}\thereforem=\pm\frac{\sqrt{2}}{4}当m=\frac{\sqrt{2}}{4}时,y_{1}+y_{2}=\sqrt{2},y_{1}y解得:|y_{1}=2\sqrt{2}\begin{cases}y_{2}=-\sqrt{2}\\\end{cases}此时:\begin{cases}x_{1}=2\\x_{2}=\frac{1}{2}\end{cases}\therefore|AF|=x_{1}+1=3,|BF|=x_{2}+1=\frac{3}{2}\frac{|AF|}{BF}\begin{matrix}\\-=2当_{m}=-\frac{\sqrt{2}}{4}时,y_{1}+y_{2}=-\sqrt{2},y_{1}y_{2}=-4解得:\begin{cases}y_{1}=\sqrt{2}\\y_{2}=-2\sqrt{2}\end{cases}\therefore|AF|=x_{1}+1=\frac{3}{2},|BF|=x_{2}+1=3\frac{|AF|}{BF}=\frac{1}{2}

**Theorem Sequence**:  
Parabola_Equation_Standard_Right, Parabola_Definition, Substitution_x_equals_my_plus_n, Vieta_Theorem, Vieta_Theorem_Sum, Vieta_Theorem_Product, Triangle_Area_Formula, Equal_Area_Method

---

## Problem Index: 1312
**ID**: 1313
**Text**:  
已知椭圆$C$: $\frac{x^{2}}{a^{2}}+\frac{y^{2}}{b^{2}}=1(a>b>0)$的左，右焦点分别为$F_{1}$、$F_{2}$，点$A$、$B$在椭圆上，且满足$\overrightarrow{A F_{1}}=2 \overrightarrow{F_{1} B} $, $\overrightarrow{A F_{2}} \cdot \overrightarrow{A F_{1}}=0$，则椭圆$C$的离心率为?

**Process**:  
设|AF_{1}|=2m(m>0),因为\overrightarrow{AF}_{1}=2\overrightarrow{F_{1}B},所以|BF_{1}|=m又因为\overrightarrow{AF}_{2}\cdot\overrightarrow{AF_{1}}=0,|F_{1}F_{2}|=2c,所以|AF_{2}|=\sqrt{|F_{1}F_{2}|^{2}-|AF_{1}|^{2}}=2\sqrt{c2-m^{2}}又因为|BF_{2}|=\sqrt{|AB|^{2}+|AF_{2}|^{2}}=\sqrt{4c^{2}+5m^{2}},且|AF_{1}|+|AF_{2}|=|BF_{1}|+|BF_{2}|=2a,所以2m+2\sqrt{c^{2}-m^{2}}=m+\sqrt{4c^{2}+5m^{2}},所以m+2\sqrt{c^{2}-m^{2}}=\sqrt{4c^{2}+5m^{2}}所以m^{2}+4c^{2}-4m^{2}+4m\sqrt{c^{2}-m^{2}}=4c^{2}+5m^{2},所以c^{2}=5m^{2},所以c=\sqrt{5}m又因为2a=2m+2\sqrt{c^{2}-m^{2}}=6m,所以a=3m,所以e=\frac{c}{a}=\frac{\sqrt{5}m}{3m}=\frac{\sqrt{5}}{3},

**Theorem Sequence**:  
Hyperbola_Equation_Standard_X, Hyperbola_Definition, Cosine_Law, Vector_Dot_Product_Algebraic, Ellipse_Parameter_Relation, Hyperbola_Parameter_Relation, Eccentricity_Formula

---

## Problem Index: 1317
**ID**: 1318
**Text**:  
已知圆$C$:$(x-1)^{2}+(y-1)^{2}=2$经过椭圆$\Gamma$: $\frac{x^{2}}{a^{2}}+\frac{y^{2}}{b^{2}}=1  (a>b>0)$的右焦点$F$和上顶点$B$，则椭圆$\Gamma$的离心率为?

**Process**:  
在方程(x-1)^{2}+(y-1)^{2}=2中,令y=0得x=1,0.令x=0,得y=1,0.据题意得c=1,b=1所以a=\sqrt{2},e=\frac{c}{a}=\frac{\sqrt{2}}{2}

**Theorem Sequence**:  
Circle_Standard_Equation, Eccentricity_Formula

---

## Problem Index: 1318
**ID**: 1319
**Text**:  
渐近线是$2 x-\sqrt{3} y=0$和$2 x+\sqrt{3} y=0$，且过点$(6,6)$的双曲线的标准方程是?

**Process**:  
\because渐近线是2x\pm\sqrt{3}y=0设双曲线方程为(2x+\sqrt{3}y)(2x-\sqrt{3}y)=\lambda(\lambda\neq0)即4x^{2}-3y^{2}=\lambda将(6,6)代入得4\times36-3\times36=\lambda\therefore\lambda=36\therefore双曲线的标准方程是\frac{x^{2}}{9}-\frac{y^{2}}{12}=

**Theorem Sequence**:  
Hyperbola_Equation_Standard_X, Hyperbola_Asymptote, Hyperbola_Common_Asymptote_System

---

## Problem Index: 1329
**ID**: 1330
**Text**:  
已知抛物线$x^{2}=2 p y(p>0)$的焦点$F$，准线为$l$，点$P(4, y_{0})$在抛物线上，$K$为$l$与$y$轴的交点，且$|P K|=\sqrt{2}|P F|$，则$y_{0}$=?

**Process**:  
过P作准线l的垂线,垂足为M,则|PM|=|PF|,在Rt\trianglePKM中,\because|PK|=\sqrt{2}|PF|=\sqrt{2}|PM|\thereforePM=KM=4,\thereforey_{0}=4-\frac{p}{x},把P(4,44-\frac{p}{2})代入抛物线方程x^{2}=2py,解得p=4.\thereforey_{0}=4-2=2.效答家为2可能,本题主要考查了抛物线的定义及方程思想,考查计算能力及转化能力,属于中档题

**Theorem Sequence**:  
Parabola_Equation_Standard_Right, Parabola_Definition, Parabola_Directrix, Pythagorean_Theorem

---

## Problem Index: 1337
**ID**: 1338
**Text**:  
已知$F_{1}$、$F_{2}$分别为椭圆$\frac{x^{2}}{4}+y^{2}=1$左右焦点,点$P$在椭圆上,$|\overrightarrow{P F_{1}}+\overrightarrow{P F_{2}}|=2 \sqrt{3}$, 则$\angle F_{1} P F_{2}$=?

**Process**:  
椭圆\frac{x^{2}}{4}+y^{2}=1焦点在x轴上,|PF_{1}|+|PF_{2}|=2a=4,|F_{1}F_{2}|^{2}=2\sqrt{3}由余弦定理可知:|F_{1}F_{2}|^{2}=|PF_{1}|^{2}+|PF_{2}|^{2}-2|PF_{1}|\cdot|PF_{2}|\cos\angleF_{1}PF_{2}=12则|\overrightarrow{PF_{1}}+\overrightarrow{PF_{2}}^{2}=|\overrightarrow{PF_{1}}^{2}+2\overrightarrow{PF_{1}}\cdot\overrightarrow{PF_{2}}+|\overrightarrow{PF_{2}}^{2}|=12,\therefore2|PF_{1}||PF_{2}|\cos\angleF_{1}PF_{2}=0,则\cos\angleF_{1}PF_{2}=0\therefore\angleF_{1}PF_{2}=\frac{\pi}{2}

**Theorem Sequence**:  
Ellipse_Equation_Standard_X, Ellipse_Parameter_Relation, Ellipse_Definition, Cosine_Law, Vector_Dot_Product_Algebraic

---

## Problem Index: 1350
**ID**: 1351
**Text**:  
双曲线$\frac{x^{2}}{4}-\frac{y^{2}}{m}=1$的虚轴长是实轴长的$2$倍，则$m$的值=?

**Process**:  
由双曲线方程可知a^{2}=4,b^{2}=m\thereforea=2,b=\sqrt{m},由虚轴长是实轴长的2倍可知\sqrt{m}=4\thereforem=16

**Theorem Sequence**:  
Hyperbola_Equation_Standard_X, Hyperbola_Parameter_Relation

---

## Problem Index: 1355
**ID**: 1356
**Text**:  
若抛物线$y^{2}=m x$的焦点与椭圆$\frac{x^{2}}{6}+\frac{y^{2}}{2}=1$的右焦点重合，则实数$m$的值为?

**Process**:  
由椭圆方程\frac{x^{2}}{6}+\frac{y^{2}}{2}=1可知,a^{2}=6,b^{2}=2,则c^{2}=a^{2}-b^{2}=4即椭圆的右焦点的坐标为(2,0),抛物线y^{2}=mx的焦点坐标为(\frac{m}{4},0)\because抛物线的焦点与椭圆的右焦点重合,\therefore\frac{m}{4}=2,即m=8,

**Theorem Sequence**:  
Ellipse_Equation_Standard_X, Ellipse_Parameter_Relation, Parabola_Equation_Standard_Right, Parabola_Directrix

---

## Problem Index: 1359
**ID**: 1360
**Text**:  
已知$P$是双曲线$\frac{x^{2}}{4}-y^{2}=1$上的一点，$F_{1}$、$F_{2}$是双曲线的两个焦点，且$\angle F_{1} P F_{2}=60^{\circ}$，则$\Delta F_{1} P F_{2}$的面积是?

**Process**:  
设点P为双曲线\frac{x^{2}}{4}-y^{2}=1右支上的点,且|F_{1}F_{2}|=2\sqrt{5}由双曲线定义,可知|PF_{1}|-|PF_{2}|=2a=4则在\trianglePF_{1}F_{2}中,由余弦定理可知:|F_{1}F_{2}|^{2}=|PF_{1}|^{2}+|PF_{2}|^{2}-2|PF_{1}||PF_{2}|\cos\angleF_{1}PF_{2}即|F_{1}F_{2}|^{2}=(|PF_{1}|-|PF_{2}|)^{2}+2|PF_{1}||PF_{2}|-2|PF_{1}||PF_{2}|\cos\angleF_{1}PF_{2}即(2\sqrt{5})^{2}=4^{2}+2|PF_{1}||PF_{2}|-2|PF_{1}||PF_{2}|60^{\circ},解得|PF_{1}||PF_{2}|=4则_{S_{\DeltaF_{1}PF_{2}}=\frac{1}{2}|PF_{1}||PF_{2}|\cdot\sin\angleF_{1}PF_{2}=\frac{1}{2}\times4\times\frac{\sqrt{3}}{2}=\sqrt{3}

**Theorem Sequence**:  
Hyperbola_Equation_Standard_X, Hyperbola_Definition, Cosine_Law, Triangle_Area_Formula

---

## Problem Index: 1377
**ID**: 1378
**Text**:  
已知抛物线$C$: $y^{2}=2 x$的焦点为$F$，过$F$且垂直于$x$轴的直线$l$与$C$交于$A$、$B$两点，则以线段$A B$为直径的圆被$y$轴所截得的弦长为?

**Process**:  
对抛物线C:y^{2}=2x,其焦点为F(\frac{1}{2},0),令x=\frac{1}{2},可得y=\pm1,故|AB|=2则所求圆的半径r=1,又圆心F到y轴的距离为\frac{1}{2},故以线段AB为直径的圆被y轴所截得的弦长为2\sqrt{r2-d^{2}}=2\sqrt{1-\frac{1}{4}}=\sqrt{3}

**Theorem Sequence**:  
Parabola_Equation_Standard_Right, Parabola_Directrix, Parabola_Latus_Rectum, Trapezoid_Midline_Theorem, Circle_Tangent_Condition, Chord_Length_Formula_With_K

---

## Problem Index: 1392
**ID**: 1393
**Text**:  
已知$M$是抛物线$x^{2}=4 y$上一点，$F$为其焦点，点$A$在圆$C$:$(x+1)^{2}+(y-5)^{2}=1$上，则$|M A|+|M F|$的最小值是?

**Process**:  
抛物线准线为l:y=-1,|MA|+|MF|=MA+d_{A-l}\geqslantd_{C-l}-r=5+1-1=5

**Theorem Sequence**:  
Parabola_Equation_Standard_Right, Parabola_Definition, Parabola_Directrix, Point_To_Line_Distance

---

## Problem Index: 1397
**ID**: 1398
**Text**:  
已知直线$l$过抛物线$C$: $y^{2}=4 x$的焦点，$l$与$C$交于$A$ , $B$两点，过点$A$、$B$分别作$C$的切线，且交于点$P$，则点$P$的轨迹方程为?

**Process**:  
不妨将抛物线翻转为x^{2}=4y,设翻转后的直线l的方程为y=kx+1,翻转后的A,B两点的坐标分别为(x_{1},y_{1}),(x_{2},y_{2}),则联立\begin{cases}x^{2}=4y,\\y=kx+1\end{cases}得x^{2}-4kx-4=0\textcircled{1},易得抛物线x^{2}=4y在点A处的切.联立\begin{cases}y-\frac{1}{4}x^{2}=\frac{1}{2}x_{1}(x-x_{1}),\\y-\frac{1}{2}x(x-x),\end{cases}同理可得抛物线x^{2}=4y在点B处的切线方程为y-\frac{1}{4}x_{2}^{2}=\frac{1}{2}x_{1}(x-x_{1}x_{1}x_{2},再由\textcircled{1}可得x_{1}x_{2}=-4,所以y=-1.故原抛物线C相应的点P的轨迹方程为x=

**Theorem Sequence**:  
Parabola_Equation_Standard_Right, Parabola_Tangent_Line, Line_Point_Slope_Form, Substitution_x_equals_my_plus_n, Vieta_Theorem

---

## Problem Index: 1411
**ID**: 1412
**Text**:  
双曲线$x^{2}-y^{2}=2$的离心率是?

**Process**:  
双曲线x^{2}-y^{2}=2的标准方程为\frac{x^{2}}{2}-\frac{y^{2}}{2}=1则a^{2}=2,b^{2}=2,则c^{2}=2+2=4,即a=\sqrt{2},c=2,则离心率e=\frac{c}{a}=\frac{2}{\sqrt{2}}=\sqrt{2},

**Theorem Sequence**:  
Hyperbola_Equation_Standard_X, Hyperbola_Parameter_Relation, Eccentricity_Formula

---

## Problem Index: 1421
**ID**: 1422
**Text**:  
曲线$\sqrt{(x-1)^{2}+y^{2}}=\frac{\sqrt{2}}{2}(2-x)$的焦点是双曲线$C$的焦点，点$(3, \frac{2 \sqrt{39}}{3})$在$C$上，则$C$的方程是?

**Process**:  
:整理\sqrt{(x-1)^{2}+y^{2}}=\frac{\sqrt{2}}{2}(2-x)可得:\frac{x^{2}}{2}+y^{2}=1该方程表示椭圆,其焦点坐标为(-1,0),(1,0).由题可设双曲线C的方程为:\frac{x^{2}}{a^{2}}-\frac{y^{2}}{b^{2}}=1(a>0,b>0),且c=1因为点(3,\frac{2\sqrt{39}}{3})在C上,将它代入上式可得:\frac{9}{a^{2}}-\frac{52}{b^{2}}=1又a^{2}+b^{2}=c^{2}=1,解得:a^{2}=\frac{1}{3},b^{2}=\frac{2}{3},所以双曲线C的方程为:3x^{2}-\frac{3}{7}y2=1.

**Theorem Sequence**:  
Two_Points_Distance, Eccentricity_Formula, Hyperbola_Parameter_Relation, Hyperbola_Equation_Standard_X

---

## Problem Index: 1429
**ID**: 1430
**Text**:  
若双曲线$C$: $\frac{x^{2}}{a^{2}}-\frac{y^{2}}{b^{2}}=1(a>0, b>0)$的离心率为$3$，则抛物线$y=\frac{1}{4} x^{2}$的焦点到双曲线$C$的渐近线距离为?

**Process**:  
y=\frac{1}{4}x2的焦点(0,1)双曲线的离心率等于3,即\frac{c}{a}=3,c^{2}=a^{2+b^{2}}\frac{c^{2}}{a^{2}}=1+(\frac{b}{a})^{2},\frac{b}{a}=2\sqrt{2}则双曲线的渐近线方程为y=\pm2\sqrt{2}x,焦点(0,1)到双曲线的渐近线距离等于d=\frac{}{1}\frac{1}{\sqrt{1+8}}=\frac{1}{3}.

**Theorem Sequence**:  
Parabola_Equation_Standard_Up, Parabola_Directrix, Hyperbola_Equation_Standard_X, Hyperbola_Asymptote, Point_To_Line_Distance, Eccentricity_Formula

---

## Problem Index: 1442
**ID**: 1443
**Text**:  
已知点$M$在以$A$、$B$为焦点的椭圆上，点$C$为该椭圆所在平面内的一点，且满足以下两个条件：($1$)$\overrightarrow{M A}+\overrightarrow{M B}=2 \overrightarrow{M C}$；($2$)$|\overrightarrow{M A}|=2|\overrightarrow{M B}|=2|\overrightarrow{M C}|$，则该椭圆的离心率为?

**Process**:  
利用椭圆的对称性及\overrightarrow{MA}+\overrightarrow{MB}=2\overrightarrow{MC}可得:点C与原点O重合,设MA=m,利用椭圆定义及|\overrightarrow{MA}|=2|\overrightarrow{MB}|=2|\overrightarrow{MC}|可得:m=\frac{4a}{3},\frac{m}{2}=\frac{2a}{3},再对角B分别在两个三角形中利用余弦定理列方程,整理可得:9c^{2}=6a^{2},问题得解详解]依据题意作出图形如下:因为O为AB的中点,所以\overrightarrow{MA}+\overrightarrow{MB}=2\overrightarrow{MO}又\overrightarrow{MA}+\overrightarrow{MB}=2\overrightarrow{MC},所以C与原点O重合设MA=m,则MB=\frac{m}{2},MO=\frac{m}{2}由椭圆定义可得:MA+MB=m+\frac{m}{2}=2a所以m=\frac{4a}{3},\frac{m}{2}=\frac{2a}{3}在AOBM及AABM中,由余弦定理可得:\cosB=\frac{(\frac{2a}{3})^{2}+(2c)^{2}-(\frac{4a}{3})^{2}}{2\times2c\times\frac{2a}{3}}=\frac{(\frac{2a}{3})^{2}+c^{2}-(\frac{2a}{3})^{2}}{2\timesc\times\frac{2a}{3}}整理得:9c^{2}=6a^{2}所以e=\sqrt{\frac{c^{2}}{a^{2}}}=\sqrt{\frac{6}{9}}=\frac{\sqrt{6}}{3}

**Theorem Sequence**:  
Ellipse_Equation_Standard_X, Ellipse_Definition, Vector_Collinear_Condition, Midpoint_Formula, Cosine_Law, Eccentricity_Formula

---

## Problem Index: 1493
**ID**: 1494
**Text**:  
已知抛物线$E$: $y^{2}=2 p x(p>0)$的焦点为$F$，直线$l$过点$F$与抛物线交于$A$、$B$两点，与其准线交于点$C$(点$B$在点$A$，$C$间)，若$|B C|=3|B F|$，且$|A B|=9$，则$p$=?

**Process**:  
如下图所示:过点B作BD\botl,垂足为点D,设直线AB的倾斜角为锐角\alpha,则\angleCBD=\alpha.与抛物线的定义得|BF|=|BD|.所以,\cos\alpha=\frac{|BD|}{|BC|}=\frac{|BF|}{|BD|}=\frac{1}{3},\therefore\sin\alpha=\sqrt{1-\cos^{2}\alpha}=\frac{2\sqrt{2}}{3},\tan\alpha=\frac{\sin\alpha}{\cos\alpha}=2\sqrt{2}又知抛物线E的焦点为F(\frac{p}{2},0),所以,直线AB的方程为y=2\sqrt{2}(x-\frac{p}{2}),设点A(x_{1},y_{1})、B(x_{2},y_{2}),将直线AB的方程与抛物线E的方程联立\begin{cases}2\\y=2\sqrt{2}\end{cases}(x-\frac{p}{2})消去y并整理得4x^{2}-5px+p^{2}=0,由韦达定理得x+x=\frac{5p}{x}由抛物线的定义可得|AB|=x_{1}+x_{2}+p=\frac{9p}{4}=9,解得p=4,

**Theorem Sequence**:  
Parabola_Equation_Standard_Right, Parabola_Definition, Parabola_Directrix, Trapezoid_Midline_Theorem, Equal_Area_Method

---

## Problem Index: 1504
**ID**: 1505
**Text**:  
与双曲线$x^{2}-\frac{y^{2}}{4}=1$有相同渐近线，且过点$(1,2 \sqrt{3})$的双曲线方程为?

**Process**:  
由题意设所求双曲线方程为x^{2}-\frac{y^{2}}{4}=\lambda,由于双曲线过点(1,2\sqrt{3})所以1-\frac{12}{4}=\lambda,\lambda=-2,双曲线方程为x^{2}-\frac{y^{2}}{4}=-2^{,}即\frac{y^{2}}{8}-\frac{x^{2}}{2}=1.

**Theorem Sequence**:  
Hyperbola_Common_Asymptote_System, Hyperbola_Equation_Standard_X

---

## Problem Index: 1513
**ID**: 1514
**Text**:  
已知双曲线$\frac{x^{2}}{a^{2}}-\frac{y^{2}}{b^{2}}=1(a>0, b>0)$的离心率$e$是$2$，则此时$\frac{b^{2}+1}{3 a}$的最小值是?

**Process**:  
由双曲线\frac{x^{2}}{a^{2}}-\frac{y^{2}}{b^{2}}=1(a>0,b>0)的离心率是2,可得\frac{c}{a}=2,所以\frac{a2+b^{2}}{a^{2}}=1+\frac{b^{2}}{a^{2}}=4所以b^{2}=3a^{2},则\frac{3a2+1}{3a}=a+\frac{1}{3a}\geqslant2\sqrt{a\cdot\frac{1}{3a}}=\frac{2\sqrt{3}}{3},当且仅当a=\frac{1}{3a},即a=\frac{\sqrt{3}}{3}时等号成立.

**Theorem Sequence**:  
Hyperbola_Equation_Standard_X, Eccentricity_Formula, Homogenization_Eccentricity

---

## Problem Index: 1516
**ID**: 1517
**Text**:  
已知点$M(-3,0)$, $N(3,0)$, $B(1,0)$，圆$C$与直线$M N$切于点$B$，过$M$、$N$与圆$C$相切的两直线相交于点$P$，则$P$点的轨迹方程为?

**Process**:  
如图,设直线MP,NP与圆C分别切于点A,D,由切线长定理得|MA|=|MB|=4,|ND|=|NB|=2,|PA|=|PD|.所以|PM|-|PN|=(|PA|+|MA|)-(|PD|+|ND|)=|MA|-|ND|=4-2=2<|MN|所以点P的轨迹为以M(-3,0),N(3,0)为焦点,实轴长为2的双曲线的右支(且去掉右顶点).设双曲线的方程为\frac{x^{2}}{a^{2}}-\frac{y^{2}}{b^{2}}=1.则2a=2,c=3,故a=1,b^{2}=9-1=8,所以点P的轨迹方程为x^{2}-\frac{y^{2}}{8}=1(x>1)

**Theorem Sequence**:  
Ellipse_Equation_Standard_X, Ellipse_Parameter_Relation

---

## Problem Index: 1517
**ID**: 1518
**Text**:  
设$A$、$B$是抛物线$x^{2}=4 y$上相异的两点，则$|\overrightarrow{O A}+\overrightarrow{O B}|^{2}-|\overrightarrow{A B}|^{2}$的最小值是?

**Process**:  
由题意直线AB的斜率存在,设AB:y=kx+t.由\begin{cases}y=kx+t\\x^{2}=4y\end{cases}消去y整理得x^{2}-4kx-4t=0,且_{A}=16k^{2}+16t>0设A(x_{1},y_{1}),B(x_{2},y_{2}),AB中点为M(x_{0},y_{0})则\begin{cases}x_{1}+x_{2}=4k\\x_{1}x_{2}=-4t\end{cases}=\frac{x_{1}+x_{2}}{2}=2ky_{0}=kx_{0}+t=2k^{2}+\thereforeM(2k,2k^{2}+t),\therefore|\overrightarrow{OM}|=\sqrt{4k^{4}+4k^{2}t+4k^{2}+t^{2}}又|\overrightarrow{AB}|=\sqrt{1+k^{2}}|x_{1}x_{2}|=\sqrt{(1+k^{2})(16k^{2}+16t)}=\sqrt{16k^{4}+16k^{2}t+16k^{2}+16t}|\overrightarrow{OA}+\overrightarrow{OB}|^{2}-|\overrightarrow{AB}|^{2}=4|\overrightarrow{OM}|^{2}-|\overrightarrow{AB}|^{2}=4t^{2}-16t=4(t-2)^{2}-16\geqslant-16,当t=2时等号成立\therefore|\overrightarrow{OA}+\overrightarrow{OB}|^{2}-|\overrightarrow{AB}|^{2}的最小值是-16.

**Theorem Sequence**:  
Parabola_Equation_Standard_Right, Substitution_x_equals_my_plus_n, Vieta_Theorem, Vieta_Theorem_Sum, Midpoint_Formula, Point_To_Line_Distance, Chord_Length_Formula_With_K, Quadratic_Function_Maximum

---

## Problem Index: 1529
**ID**: 1530
**Text**:  
已知动点$P(x, y)$在椭圆$\frac{x^{2}}{100}+\frac{y^{2}}{64}=1$上，若$A$点的坐标为$(6,0)$ ,$|\overrightarrow{A M}|=1$，且$\overrightarrow{P M} \cdot \overrightarrow{A M}=0$，则$|\overrightarrow{P M}|$的最小值为?

**Process**:  
\because\overrightarrow{PM}\cdot\overrightarrow{AM}=0,\thereforePM\botAM,\therefore|PM|=|AP|^{2}-|AM|^{2},又\because|\overrightarrow{AM}|=1,\therefore|AP|越小,|PM|就越小.设P(10\cosx,8\sinx),则|AP|^{2}=(10\cosx-6)^{2}+(8\sinx-()=100\cos^{2}x-120\cosx+36+64\sin^{2}x=36\cos^{2}x-120\cosx+100=(6\cosx-10)^{2},\therefore|AP|的最小值为\sqrt{(6-10)^{2}}=4,\therefore|PM|的最小值为:\sqrt{4^{2}-1^{2}}=\sqrt{15}

**Theorem Sequence**:  
Ellipse_Equation_Standard_X, Vector_Perpendicular_Condition, Ellipse_Parametric_Equation, Two_Points_Distance, Quadratic_Function_Maximum

---

## Problem Index: 1544
**ID**: 1545
**Text**:  
已知抛物线$C$: $x^{2}=2 p y(p>0)$的焦点为$F$，若$C$上一点$M(x_{0}, 3)$到焦点$F$的距离为$6$，则$x_{0}$的值为?

**Process**:  
依题意,|MF|=3+\frac{p}{2}=6,解得p=6,故抛物线C:x^{2}=12y;将M(x_{0},3)代入可得x_{0}^{2}=36,则x_{0}=\pm6.

**Theorem Sequence**:  
None

---

## Problem Index: 1556
**ID**: 1557
**Text**:  
已知椭圆$\frac{x^{2}}{a^{2}}+\frac{y^{2}}{b^{2}}=1(a>b>0)$的左、右焦点分别为$F_{1}$, $F_{2}$, 过$F_{1}$且与$x$轴垂直的直线交椭圆于$A$、$B$两点，直线$A F_{2}$与椭圆的另一个交点为$C$，若$S_{\triangle A B C}=3 S_{\triangle B C F_{2}}$，则椭圆的离心率为?

**Process**:  
设椭圆的左、右焦点分别为F_{1}(-c,0),F_{2}(c,0),将x=-c代入椭圆方程可得y=\pm\frac{b^{2}}{a},可设A(-c,\frac{b^{2}}{a}),C(x,y),由S_{\triangleABC}=3S_{\triangleBCF_{2}},得\overrightarrow{AF_{2}}=2\overrightarrow{F_{2}C},即有(2c,-\frac{b^{2}}{a})=2(x-c,y),即得x=2c,y=-\frac{b^{2}}{2a}=2y',代入椭圆方程可得\frac{4c^{2}}{a^{2}}+\frac{b^{2}}{4a^{2}}=1,由e=\frac{c}{a},b^{2}=a^{2}-c2,即有4e^{2}+\frac{1}{4}-\frac{1}{4}e^{2}=1,解得e=\frac{\sqrt{5}}{5}故答案)为:\frac{\sqrt{5}}{6}

**Theorem Sequence**:  
Ellipse_Equation_Standard_X, Vector_Collinear_Condition, Ellipse_Parameter_Relation, Homogenization_Eccentricity, Eccentricity_Formula

---

## Problem Index: 1568
**ID**: 1569
**Text**:  
已知$O$为坐标原点，抛物线$C$: $y^{2}=8 x$的焦点为$F$、$P$为$C$上一点，$P F$与$x$轴垂直，$Q$为$x$轴上一点，若$P$在以线段$O Q$为直径的圆上，则该圆的方程为?

**Process**:  
由题意得:\because抛物线C:y^{2}=8x的焦点为F(2,0),PF与x轴垂直\thereforeP点的横坐标为2\thereforey^{2}=16,即y=\pm4故P点的坐标为(2,4)或(2,-4)又\becauseQ为x轴上一点,且OQ为直径,P点在圆上故设圆心为(m,0),于是有(2-m)^{2}+16=m^{2},即20-4m=0\Rightarrowm=5所以圆的方程为(x-5)^{2}+y^{2}=25x^{2}

**Theorem Sequence**:  
Parabola_Equation_Standard_Right, Circle_Standard_Equation, Vector_Perpendicular_Condition, Midpoint_Formula

---

## Problem Index: 1598
**ID**: 1599
**Text**:  
过抛物线$C$: $y^{2}=2 p x(p>0)$焦点$F$的直线$l$与抛物线$C$交于$A$、$B$两点，若抛物线$C$的准线上一点$M(-2,2)$满足$\overrightarrow{M A} \cdot \overrightarrow{M B}=0$，则$|A B|$的值为?

**Process**:  
由已知抛物线的准线为x=-2,所以\frac{p}{2}=2,p=4,抛物线方程为y^{2}=8x焦点为F(2,0),因为直线l过焦点,,可设其方程为l:x=ky+2(k\neq0)因为\overrightarrow{MA}\cdot\overrightarrow{MB}=0,所以M在以AB为直径的圆上,设点A(x_{1},y_{1}),B(x_{2},y_{2}).所以\begin{cases}y_{1}^{2}=8x_{1}\\y_{2}^{2}=8x_{2}\end{cases}\frac{1}{2}=8x_{1},两式相减得\frac{y_{1}-y_{2}}{x_{1}-x_{2}}=\frac{8}{y_{1}+y_{2}}=\frac{1}{k},设AB的中点为Q(x_{0},y_{0}),则y_{0}=\frac{y_{1}+y_{2}}{2}=4k'x_{0}=4k^{2}+2,所以Q(4k^{2}+2,4k)是以AB为直径的圆的圆心,由抛物线定义知,圆的半径为r=\frac{|AB|}{2}=\frac{x_{1}+x_{2}+4}{2}=\frac{2x_{0}+4}{2}=4k^{2}+4因为|QM|^{2}=(x_{0}+2)^{2}+(y_{0}-2)^{2}=(4k^{2}+4)^{2}+(4k-2)^{2}=r^{2}所以(4k^{2}+4)^{2}+(4k-2)^{2}=(4k^{2}+4)^{2},解得k=\frac{1}{2}所以|AB|=2r=2[4\times(\frac{1}{7})^{2}+4数答家为:10

**Theorem Sequence**:  
Parabola_Equation_Standard_Right, Parabola_Directrix, Substitution_x_equals_my_plus_n, Vieta_Theorem_Sum, Point_Difference_Method, Midpoint_Formula, Parabola_Definition, Vector_Perpendicular_Condition, Circle_Standard_Equation

---

## Problem Index: 1599
**ID**: 1600
**Text**:  
椭圆$\frac{x^{2}}{a^{2}}+\frac{y^{2}}{20}=1$的焦点在$x$轴上，焦距为$8$，则该椭圆的离心率为?

**Process**:  
由于椭圆焦距2c=8,c=4,椭圆焦点在x上,故a^{2}=20+4^{2}=36,a=6,所以椭圆离心率为\frac{c}{a}=\frac{4}{6}=\frac{2}{3}.

**Theorem Sequence**:  
Ellipse_Equation_Standard_X, Ellipse_Parameter_Relation, Eccentricity_Formula

---

## Problem Index: 1600
**ID**: 1601
**Text**:  
以$(1,-1)$为中点的抛物线$y^{2}=8 x$的弦所在直线方程为?

**Process**:  
此弦不垂直于X轴,故设点(1,-1)为中点的抛物线y^{2}=8x的弦的两端点为A(x_{1},y_{i})B(x_{2},y_{2})得到y_{1}^{2}=8x_{1},y_{2}^{2}=8x_{2}两式相减得到(y_{1}+y_{2})(y_{i}-y_{2})=8(x_{1}-x_{2})\thereforek=y_{1}-y_{2}/x_{1}-x_{2}=-4\therefore直线方程为y+1=4(x-1),即4x+y-3=0

**Theorem Sequence**:  
Parabola_Equation_Standard_Right, Point_Difference_Method, Midpoint_Formula, Slope_Formula, Line_Point_Slope_Form

---

## Problem Index: 1631
**ID**: 1632
**Text**:  
已知直线$y=k x+1$与曲线$y^{2}=2 x$只有一个交点，则实数$k$的值为?

**Process**:  
联立直线方程与抛物线方程可得:k^{2}x^{2}+(2k-2)x+1=0,\textcircled{1}若k=0,则y=1,x=\frac{1}{2},满足题意;\textcircled{2}若k\neq0,则a=(2k-2)^{2}-4k^{2}=0,解得k=\frac{1}{2}综上所述,k=0或\frac{1}{2}.

**Theorem Sequence**:  
Parabola_Equation_Standard_Right, Discriminant_Delta, Discriminant_Tangent_Condition

---

## Problem Index: 1648
**ID**: 1649
**Text**:  
设双曲线$C$: $\frac{x^{2}}{a^{2}}-\frac{y^{2}}{b^{2}}=1(a>0 , b>0)$的一条渐近线为$y=\sqrt{2} x$，则$C$的离心率为?

**Process**:  
由双曲线方程\frac{x^{2}}{a^{2}}-\frac{y^{2}}{b^{2}}=1可得其焦点在x轴上,因为其一条渐近线为y=\sqrt{2}x,所以\frac{b}{a}=\sqrt{2},e=\frac{c}{a}=\sqrt{1+\frac{b^{2}}{a^{2}}}=\sqrt{3}

**Theorem Sequence**:  
Hyperbola_Equation_Standard_X, Hyperbola_Asymptote, Eccentricity_Formula

---

## Problem Index: 1673
**ID**: 1674
**Text**:  
若椭圆$\frac{x^{2}}{25}+\frac{y^{2}}{16}=1$上一点$P$到焦点$F_{1}$的距离为$6$，则点$P$到另一个焦点$F_{2}$的距离是?

**Process**:  
由椭圆的定义即可求解由椭圆定义知PF_{1}+PF_{2}=10,又PF_{1}=6,\thereforePF_{2}=4

**Theorem Sequence**:  
Ellipse_Equation_Standard_X, Ellipse_Definition

---

## Problem Index: 1676
**ID**: 1677
**Text**:  
已知双曲线$\frac{x^{2}}{a^{2}}-\frac{y^{2}}{b^{2}}=1(a>0 , b>0)$的左焦点为$F$，离心率为$\sqrt{2}$. 若经过$F$和$P(0 , 4)$两点的直线平行于双曲线的一条渐近线，则双曲线的方程为?

**Process**:  
设点F(-c,0)(c>0),因为该双曲线的离心率为\sqrt{2},所以\frac{c}{a}=\sqrt{2},\textcircled{1}又经过F和P(0,4)两点的直线平行于双曲线的一条渐近线,所以k_{FP}=\frac{4-0}{0-(-c)}=\frac{b}{a},\textcircled{2}联立\textcircled{1}\textcircled{2},解得b=2\sqrt{2}又a^{2}+b^{2}=c^{2},即a^{2}+8=c^{2}\textcircled{3},联立\textcircled{1}\textcircled{3},解得a^{2}=8,c^{2}=16,故双曲线的方程为\frac{x^{2}}{8}-\frac{y^{2}}{8}=1

**Theorem Sequence**:  
Hyperbola_Equation_Standard_X, Eccentricity_Formula, Hyperbola_Asymptote, Slope_Formula, Line_Point_Slope_Form, Hyperbola_Parameter_Relation

---

## Problem Index: 1683
**ID**: 1684
**Text**:  
已知抛物线的顶点在原点，焦点在$y$轴上，且抛物线上一点$M(m,-2)$到焦点的距离为$4$，则抛物线的方程是?

**Process**:  
由题意可设抛物线方程为x^{2}=-2px(p>0),所以抛物线上的点P到F的距离等于\frac{p}{2}-(-2)=4,\thereforep=4,所以抛物线方程为x^{2}=-8y.

**Theorem Sequence**:  
Parabola_Equation_Standard_Down, Parabola_Definition, Parabola_Directrix

---

## Problem Index: 1693
**ID**: 1694
**Text**:  
若椭圆$\frac{x^{2}}{m}+\frac{y^{2}}{3}=1$的一个焦点在抛物线$y^{2}=8 x$的准线上，则$m$=?

**Process**:  
先求出抛物线y^{2}=8x的准线,从而可得c的值,进而可求出m的值抛物线y^{2}=8x的准线为直线x=-2,因为椭圆\frac{x^{2}}{m}+\frac{y^{2}}{3}=1的一个焦点在抛物线y^{2}=8x的准线上.所以可得c=2,所以m=a^{2}=b^{2}+c^{2}=3+2^{2}=7,

**Theorem Sequence**:  
Parabola_Equation_Standard_Right, Parabola_Directrix, Ellipse_Equation_Standard_X, Ellipse_Parameter_Relation

---

## Problem Index: 1699
**ID**: 1700
**Text**:  
已知抛物线方程为$y^{2}=4 x$，直线$l$过定点$M(-2,1)$，斜率为$k$，当直线$l$与抛物线$y^{2}=4 x$只有一个公共点时，斜率$k$取值的集合为?

**Process**:  
由题意设直线方程为:y=k(x+2)+1,代入抛物线方程整理可得k^{2}x^{2}+(4k^{2}+2k-4)x+4k^{2}+4k+1=0(*)直线与抛物线只有一个公共点等价于(*)只有一个根,\textcircled{1}k=0时,y=1符合题意;\textcircled{2}k\neq0时,\triangle=(4k^{2}+2k\cdot4)^{2}\cdot4k^{2}(4k^{2}+4k+1)=整理得2k^{2}+k\cdot1=0,解得k=\frac{1}{4}或k=-1.综上k\in[-1,0,\frac{1}{2})

**Theorem Sequence**:  
Hyperbola_Equation_Standard_X, Hyperbola_Asymptote, Discriminant_Delta, Hyperbola_Eccentricity_Range

---

## Problem Index: 1715
**ID**: 1716
**Text**:  
已知顶点在坐标原点的抛物线的焦点坐标为$(0,-2)$，则此抛物线的标准方程为?

**Process**:  
分析:根据抛物线的焦点坐标,判断出抛物线的形式,设抛物线方程为x^{2}=-2py(p>0),的值,得出标准方程.详由抛物线的焦点坐标,设抛物线方程为x^{2}=-2py(p>0),由\frac{p}{2}=2,p=4,所以抛物线方程为x^{2}=-8y

**Theorem Sequence**:  
Parabola_Equation_Standard_Down, Parabola_Directrix

---

## Problem Index: 1725
**ID**: 1726
**Text**:  
已知点$P$是双曲线$\frac{x^{2}}{a^{2}}-\frac{y^{2}}{b^{2}}=1(a>0, b>0)$右支上一点,$F_{1}$、$F_{2}$分别是双曲线的左右焦点,$I$为$\Delta P F_{1} F_{2}$的内心, 若$S_{\Delta I P F_{1}}=\frac{\sqrt{6}}{3} S_{\Delta I F_{1} F_{2}}+S_{\Delta I P F_{2}}$则双曲线的离心率为?

**Process**:  
设\trianglePF_{1}F_{2}的内切圆的半径为r,r_{2}\frac{\sqrt[4m+n]{-y+yF_{2}-4P_{2}r}}{|.2-b}.|-|-x-\frac{1}{x}

**Theorem Sequence**:  
Incircle_Radius_Formula

---

## Problem Index: 1783
**ID**: 1784
**Text**:  
已知双曲线$\frac{x^{2}}{a^{2}}-\frac{y^{2}}{b^{2}}=1(a>0, b>0)$的左焦点为$F$，右顶点为$A$，直线$x=a$与双曲线的一条渐近线的交点为$B$. 若$\angle B F A=30^{\circ}$，则双曲线的渐近线方程为?

**Process**:  
根据\tan\angleBFA的值得到关于a,b的方程,从而求得渐近线的斜率,即可得答案由题意,可得A(a,0),双曲线的渐近线方程为ay\pmbx=0,不妨设B点为直线x=a与y=\frac{b}{a}x的交点,则B点的坐标为(a,b)因为AB\botFA,\angleBFA=30^{\circ}所以\tan\angleBFA=\frac{|AB|}{|FA|}=\frac{b}{a+c}=\frac{}{a+}解得\frac{b}{a}=\sqrt{3},所以渐近线的方程为y\pm\sqrt{3}x=0

**Theorem Sequence**:  
Hyperbola_Equation_Standard_X, Hyperbola_Asymptote, Vector_Perpendicular_Condition, Slope_Formula, Homogenization_Eccentricity

---

## Problem Index: 1796
**ID**: 1797
**Text**:  
以直线$3 x-4 y-2=0$及$3 x+4 y-10=0$为渐近线，一个顶点为$(2,4)$的双曲线方程是?

**Process**:  
根据双曲线渐近线的交点是双曲线的对称中心这一性质,通过解方程组求出双曲线的对称中心,忽后根据顶点的位置,结合平移的性质进行求解即可.因为双曲线渐近线的交点是双曲线的对称中心,所以双曲线的对称中心坐标就是方程解组\begin{cases}3x-4y-2=0\\3x-4y-10=0\end{cases}的解,解得\begin{cases}x=2\\y=1\end{cases}因此双曲线的对称中心坐标为(2,1)该双曲线向左平移2个单位长度,再向下平移1个单位长度,变成对称中心为坐标原点的双曲线.所以该双曲线的顶点(2,4)经过向左平移2个单位长度,再向下平移1个单位长度,变成(0,3)因此对称中心为原点的双曲线的焦点在纵轴上,a=3.该双曲线经过这样的平移后,就为3x-4y=0和3x+4y=0,即有\frac{b}{a}=\frac{4}{3}\Rightarrowb=4,所以平移后对称中心为坐标原点的双曲线方程为\frac{y^{2}}{9}-\frac{x^{2}}{16}=1,因此原双曲线的方程为:.

**Theorem Sequence**:  
Hyperbola_Equation_Standard_Y, Hyperbola_Asymptote, Line_Point_Slope_Form

---

## Problem Index: 1814
**ID**: 1815
**Text**:  
已知双曲线$C$: $\frac{x^{2}}{a^{2}}-\frac{y^{2}}{b^{2}}=1(a>0 , b>0)$的右顶点，右焦点分别为$A$、$F$，它的左准线与$x$轴的交点为$B$，若$A$是线段$B F$的中点，则双曲线$C$的离心率为?

**Process**:  
由题意知:B(-\frac{a^{2}}{c},0),A(a,0),F(c,0),则2a=c-\frac{a}{c}即e^{2}-2e-1=0,解得e=\sqrt{2}+1.

**Theorem Sequence**:  
Ellipse_Directrix, Eccentricity_Formula, Homogenization_Eccentricity

---

## Problem Index: 1815
**ID**: 1816
**Text**:  
已知椭圆$\frac{x^{2}}{4}+\frac{y^{2}}{3}=1$的右焦点为$F$、$A$为椭圆在第一象限内的点，连接$A F$并延长交椭圆于点$B$，连接$A O$($O$为坐标原点) 并延长交椭圆于点$C$，若$S_{\triangle A B C}=3$，则点$A$的坐标为?

**Process**:  
求得F(1,0),设AB的方程为x=my+1,联立椭圆方程,运用韦达定理,以及完全平方公式,结合题意可得S_{\triangleABO}=S_{\triangleAOF}+S_{\triangleBOF}=\frac{1}{2}\cdot|OF|\cdot|y_{1}-y_{2}|=\frac{3}{2},即有|y_{1}-y_{2}|=3,平方后由韦达定理,解方程可得m=0,可得A的坐标.由题意可得F(1,0),设AB的方程为x=my+1,联立椭圆方程可得(4+3m^{2})y^{2}+6my-9=0,设A(x_{1},y_{1})B(x_{2},y_{2})\frac{m}{3m^{2}}'^{'}y_{1}y_{2}=y_{2}^{2}-4y_{1}y_{2}=\frac{36m2}{(4+3m)^{2}}由O为AC的中点,且\triangleABC的面积为3,可得\triangleABO的面积为\frac{3}{2}S_{\triangleABO}=S_{\triangleAOF}+S_{\triangleBOF}=\frac{1}{2}\cdot|OF|\cdot|y_{1}-y_{2}|=\frac{3}{2},即有|y_{1}-y_{2}|=3,可得\frac{36m^{2}}{(4+3m^{2})^{2}}+\frac{36}{4+3m^{2}}=9,化为9m^{4}+m^{2}=0,即m=0,则AB\botx轴,可得A(1,\frac{3}{2})

**Theorem Sequence**:  
Ellipse_Equation_Standard_X, Substitution_x_equals_my_plus_n, Vieta_Theorem_Sum, Vieta_Theorem_Product, Midpoint_Formula, Triangle_Area_Coordinate

---

## Problem Index: 1826
**ID**: 1827
**Text**:  
若直线$y=x+1$与抛物线$x^{2}=2 y$相交于$A$ , $B$两点，则线段$AB$的中点坐标是?

**Process**:  
解析过程略

**Theorem Sequence**:  
None

---

## Problem Index: 1830
**ID**: 1831
**Text**:  
已知双曲线$\frac{x^{2}}{a^{2}}-\frac{y^{2}}{b^{2}}=1(a>0, b>0)$的一条渐近线为$2 x+y=0$,一个焦点为$(\sqrt{5}, 0)$，则双曲线的标准方程为?

**Process**:  
因为渐近线为2x+y=0,所以\begin{cases}\frac{b}{a}=2\\c=\sqrt{5}\\c^{2}=b^{2}+a2\end{cases}解得a=1,b=2即双曲线的标)准方程为x2-\frac{y^{2}}{4}=1

**Theorem Sequence**:  
Hyperbola_Equation_Standard_X, Hyperbola_Asymptote, Hyperbola_Parameter_Relation

---

## Problem Index: 1844
**ID**: 1845
**Text**:  
若曲线$x^{2}-y^{2}=4$与直线$y=k(x-2)+3$有两个不同的公共点，则实数$k$的取值范围是?

**Process**:  
联立直线与双曲线方程消元得关于x的方程,注意字母系数的讨论.双曲线与直线有两个不同的公共点,二次项系数不为零且判别式大于零,解不等式取交集即可.解】联立\begin{cases}x^{2}-y^{2}=4\\y=k(x-2)+3\end{cases},消y得(1-k^{2})x^{2}+2k(2k-3)x-(2k-3)^{2}-4=0当_{1}-k^{2}=0,即k=\pm1时,不满足题意.当1-k^{2}\neq0,即k\neq\pm1时,\because曲线x^{2}-y^{2}=4与直线y=k(x-2)+3有两个不同的公共点,\therefore\Delta=4k^{2}(2k-3)^{2}+4(1-k^{2})[(2k-3)^{2}+4]=-4(12k-13)>0,解得,k<\frac{13}{12}

**Theorem Sequence**:  
Hyperbola_Equation_Standard_X, Discriminant_Delta, Discriminant_Intersect_Condition

---

## Problem Index: 1896
**ID**: 1897
**Text**:  
设点$P$是椭圆$C$: $\frac{x^{2}}{8}+\frac{y^{2}}{4}=1$上的动点，$F$为$C$的右焦点，定点$A(2,1)$，则$|P A|+|P F|$的取值范围是?

**Process**:  
\frac{x^{2}}{8}+\frac{y^{2}}{4}=1,F为C的右焦点,F(2,0),左焦点F_{1}(-2,0)|PA|+|PF|=|PA|+2a-|PF_{1}|=4\sqrt{2}+|PA|-|PF_{1}||PA|+|PF|=|PA|+2a-|PF_{1}|=4\sqrt{2}+|PA|-|PF_{1}||PA|+|PF|\in[4\sqrt{2}-\sqrt{17},4\sqrt{2}+\sqrt{17}]

**Theorem Sequence**:  
Ellipse_Equation_Standard_X, Ellipse_Definition, Two_Points_Distance

---

## Problem Index: 1897
**ID**: 1898
**Text**:  
椭圆$C$: $\frac{x^{2}}{a^{2}}+\frac{y^{2}}{b^{2}}=1(a>b>0)$的左、右焦点分别为$F_{1}$、$F_{2}$，点$A$在椭圆上，$\overrightarrow{A F_{1}} \cdot \overrightarrow{A F_{2}}=0$，直线$A F_{2}$交椭圆于点$B$，$|\overrightarrow{A B}|=|\overrightarrow{A F}|$，则椭圆的离心率为?

**Process**:  
可以利用条件三角形ABF_{1}为等腰直角三角形,设出边长,找到边长与a、b之间等量关系,然后把等量关系带入到勾股定理表达的等式中,即可求解离心率.由题意知三角形ABF_{1}为等腰直角三角形,设AF_{1}=AB=x,则x+x+\sqrt{2}x=4a,解得x=(4-2\sqrt{2})a,AF_{2}=(2\sqrt{2}-2)a,在三角形AF_{1}F_{2}中,由勾股定理得(AF_{1})^{2}+(AF_{2})^{2}=(2c)^{2},所以e^{2}=9-6\sqrt{2},e=\sqrt{6}-\sqrt{3}

**Theorem Sequence**:  
Ellipse_Equation_Standard_X, Ellipse_Definition, Pythagorean_Theorem, Cosine_Law, Eccentricity_Formula

---

## Problem Index: 1939
**ID**: 1940
**Text**:  
双曲线$\frac{x^{2}}{4}-\frac{y^{2}}{9}=1$的虚轴长是?

**Process**:  
根据双曲线的几何性质可以得出虚轴长.双曲线\frac{x^{2}}{a^{2}}-\frac{y^{2}}{b^{2}}=1(a>0,b>0)的虚轴长是2b.所以双曲线\frac{x^{2}}{4}-\frac{y^{2}}{9}=1的虚轴长是6.

**Theorem Sequence**:  
Hyperbola_Equation_Standard_Y

---

## Problem Index: 2010
**ID**: 2011
**Text**:  
已知$F_{1}$、$F_{2}$是椭圆$C$:$\frac{x^{2}}{36}+\frac{y^{2}}{27}=1$的两个焦点，点$P$为椭圆$C$上的点，$|P F_{1}|=8$，若$M$为线段$P F_{1}$的中点，则线段$O M$的长为?

**Process**:  
F_{1},F_{2}是椭圆C:\frac{x^{2}}{36}+\frac{y^{2}}{27}=1的两个焦点,可得F_{1}(-3,0),F_{2}(3,0).a=点P为椭圆C上的点,|PF_{1}|=8,则|PF_{2}|=4,M为线段PF_{1}的中点,则线段OM的长为:\frac{1}{2}|PF_{2}|=2.

**Theorem Sequence**:  
Ellipse_Equation_Standard_X, Ellipse_Definition, Triangle_Midline_Theorem

---

## Problem Index: 2032
**ID**: 2033
**Text**:  
已知双曲线$\frac{x^{2}}{a^{2}}-\frac{y^{2}}{b^{2}}=1(a>0, b>0)$的右焦点为$F$，若过点$F$且倾斜角为$60^{\circ}$的直线与双曲线的右支有且只有一个交点，则此双曲线离心率的取值范围是?

**Process**:  
根据直线与渐进线的关系得到\frac{b}{a}\geqslant\sqrt{3},再计算离心率范围得到答案过F的直线l与双曲线的右支有且只有一个交点,则其斜率为正的渐近线的倾斜角应不小于1的倾斜角已知l的倾斜角是60^{\circ},从而\frac{b}{a}>\sqrt{3},故e=\frac{c}{a}\geqslant2.

**Theorem Sequence**:  
Hyperbola_Equation_Standard_X, Hyperbola_Asymptote, Hyperbola_Eccentricity_Range

---

## Problem Index: 2053
**ID**: 2054
**Text**:  
已知过抛物线$y^{2}=2 p x(p>0)$焦点$F$的直线$l$与抛物线交于$A$、$B$两点，且$|A F|=\frac{3}{2}|B F|$，则直线$l$的斜率$k$=?

**Process**:  
当A(x_{0},y_{0})在第一象限,直线的倾斜角为\theta,\theta\in(0,\frac{\pi}{2}),得到y_{0}=|AF|\sin\theta,x_{0}=\frac{p}{2}+|AF|\cos\theta,代入y^{2}=2px(p>0),得到|AF|^{2}\sin^{2}\thetax^{2}-2p\cos\theta|AF|x-p^{2}=0,利用求根公式求得|AF|,|BF|,再根据|AF|=\frac{3}{2}|BF|求解,同理当点A(x_{0},y_{0})在第四象限时,由抛物线的对称性求解.羊解】设直线的倾斜角为\theta,当点A(x_{0},y_{0})在第一象限时,由题意得:\theta\in(0,\frac{\pi}{2})则y_{0}=|AF|\sin\theta,x_{0}=\frac{p}{2}+|AF|\cos\theta,代入y^{2}=2px(p>0)得:|AF|^{2}\sin^{2}\thetax^{2}-2p\cos\theta|AF|x-p^{2}=0,所以=\frac{p}{1-\cos\theta},同理|BF|=\frac{p}{1+\cos\theta}因为所以\frac{|AF|}{BF}=\frac{1+\cos\theta}{1-\cos\theta}=\frac{3}{2},解得\cos\theta=\frac{1}{5},则\sin\theta=\frac{2\sqrt{6}}{5}所以k=\tan\theta=2\sqrt{6},当点A(x_{0},y_{0})在第四象限时,由题意得:\theta\in(\frac{\pi}{2},\pi)由抛物线的对称性得:k=\tan\theta=-2\sqrt{6},

**Theorem Sequence**:  
Parabola_Equation_Standard_Right, Parabola_Focal_Radius, Line_Point_Slope_Form, Vieta_Theorem_Sum, Parabola_Focal_Chord_Formula_Angle, Basic_Inequality

---

## Problem Index: 2073
**ID**: 2074
**Text**:  
已知双曲线$C$: $\frac{x^{2}}{a^{2}}-\frac{y^{2}}{b^{2}}=1(a>0, b>0)$的一条渐近线与圆$x^{2}+(y-2 \sqrt{3})^{2}=4$相交于$A$、$B$两点，且$|A B|=2$，则双曲线$C$的离心率为?

**Process**:  
由双曲线、圆的方程确定渐近线方程为y=\pm\frac{b}{a}x,圆心为(0,2\sqrt{3}),半径为r=2,根据圆的相交弦与半径、弦心距之间的几何关系有_{r2-d^{2}}=\frac{|AB|^{2}}{4},结合双曲线参数间的关系即可求其离心率由题意知:双曲线的渐近线为y=\pm\frac{b}{a}x^{,}而圆心为(0,2\sqrt{3}),半径为r=2,\therefore圆心到渐近线的距离d=\frac{|2\sqrt{3}|}{\sqrt{1+\frac{b^{2}}{2}}}=\frac{2\sqrt{3}a}{\sqrt{a^{2}+b^{2}}},而|AB|=2,\thereforer2-d^{2}=1,故\frac{12a^{2}}{a^{2}+b^{2}}=3,又a^{2}+b^{2}=c^{2},e=\frac{c}{a}>1,\thereforee=2.

**Theorem Sequence**:  
Hyperbola_Equation_Standard_Y, Hyperbola_Asymptote, Circle_Standard_Equation, Point_To_Line_Distance, Pythagorean_Theorem, Eccentricity_Formula

---

## Problem Index: 2081
**ID**: 2082
**Text**:  
点$P$是圆$(x-2)^{2}+(y-5)^{2}=1$上的点，点$Q$是抛物线$y^{2}=4 x$上的点，则点$Q$到直线$x=-1$的距离与到点$P$的距离之和的最小值是?

**Process**:  
如下图,d=PQ+QM\geqslant(AQ-1)+QF\geqslantAF=\sqrt{26}-1,所以填\sqrt{26}-1

**Theorem Sequence**:  
Circle_Standard_Equation, Parabola_Definition, Two_Points_Distance

---

## Problem Index: 2087
**ID**: 2088
**Text**:  
抛物线$y^{2}=-8 x$的焦点到准线的距离为?

**Process**:  
试题解析:依题可得p=2,所以抛物线y^{2}=-8x的焦点到准线的距离为4

**Theorem Sequence**:  
Parabola_Equation_Standard_Down, Parabola_Directrix

---

## Problem Index: 2111
**ID**: 2112
**Text**:  
双曲线$x^{2}-\frac{y^{2}}{3}=1$上一点$P$到$M(3,0)$的距离最小值为?

**Process**:  
设P(x_{0},y_{0}),则x_{0}^{2}-\frac{y_{0}^{2}}{3}=1^{2}于是得|PM|=\sqrt{(x_{0}-3)^{2}+y_{0}^{2}}=\sqrt{4x_{0}^{2}-6x_{0}+6}=\sqrt{4(x_{0}-\frac{3}{4})^{2}+\frac{15}{4}},而|x_{0}|\geqslant1,则当x_{0}=1时,|PM|_{\min}=2,所以双曲线x^{2}-\frac{y^{2}}{3}=1上一点P到M(3,0)的距离最小值为2.

**Theorem Sequence**:  
Hyperbola_Equation_Standard_X, Two_Points_Distance, Quadratic_Function_Maximum

---

## Problem Index: 2117
**ID**: 2118
**Text**:  
双曲线$\frac{x^{2}}{9}-\frac{y^{2}}{16}=1$的左、右焦点分别为$F_{1}$、$F_{2}$，点$P$在双曲线上，且$|P F_{1}| \cdot|P F_{2}|=64$，则$\Delta P F_{1} F_{2}$的面积$S$=?

**Process**:  
由双曲线的定义可得||PF_{1}|-|PF_{2}||=2\sqrt{9}=6,由余弦定理有\cos\angleF_{1}PF_{2}=\frac{|PF_{1}^{2}+|PF_{2}|^{2}-|F_{1}F_{2}|^{2}}{2|PF_{1}|\cdot|PF_{2}|}=\frac{(||PF_{1}|-|PF_{2}||)^{2}+2|PF_{1}|\cdot|PF_{2}|-|F_{1}F_{2}|}{2|PF_{1}|\cdot|PF_{2}|}又||PF_{1}|-|PF_{2}||=6,|PF_{1}|\cdot|PF_{2}|=64,|F_{1}F_{2}|=2\sqrt{9+16}=10,代入得\cos\angleF_{1}PF_{2}=\frac{36+128-100}{128}=\frac{1}{2},又\angleF_{1}PF_{2}\in(0,\pi),故\angleF_{1}PF_{2}=\frac{\pi}{3}故_{S}=\frac{1}{2}|PF_{1}|\cdot|PF_{2}|\sin\angleF_{1}PF_{2}=\frac{1}{2}\times64\times\frac{\sqrt{3}}{2}=16\sqrt{3}

**Theorem Sequence**:  
Hyperbola_Equation_Standard_X, Hyperbola_Definition, Cosine_Law, Triangle_Area_With_Sin

---

## Problem Index: 2120
**ID**: 2121
**Text**:  
设抛物线$C$: $y^{2}=4 x$焦点为$F$，斜率为正数的直线$l$过焦点$F$，交抛物线$C$于$A$、$B$两点，交准线于点$Q$，若$\overrightarrow{A B}=\overrightarrow{B Q}$，则直线$l$的斜率为?

**Process**:  
分别过A,B作准线l的垂线,垂足分别为A',B'.\therefore|AF|=|AA'|,|BF|=|BB'|\because|AB|=|BQ|,则B为AQ中点,在\triangleAQA中,|BB'|=\frac{1}{2}|AA'|,\therefore|BF|=\frac{1}{2}|AF|,设|BF|=a,则|BB'|=a,|AB|=|BQ|=3a,\therefore|QB'|=2\sqrt{2}a,\thereforek=\tan\angleQBB'=\frac{|QB|}{|BB|}=\frac{2\sqrt{2}a}{a}=2\sqrt{2}

**Theorem Sequence**:  
Parabola_Equation_Standard_Right, Parabola_Definition, Parabola_Directrix, Vector_Collinear_Condition, Slope_Formula

---

## Problem Index: 2194
**ID**: 2195
**Text**:  
已知抛物线$y^{2}=4 x$上有一点$A$到焦点$F$的距离为$5$，则$A$到原点$O$的距离$|O A|$=?

**Process**:  
因为|AF|=5,所以A到抛物线准线的距离也等于5因为焦点坐标为(1,0),所以准线方程为x=-1点A的横坐标为5-1=4,代入抛物线方程得纵坐标为4所以点A到原点距离为\sqrt{4^{2}+4^{2}}=4\sqrt{2}

**Theorem Sequence**:  
Parabola_Equation_Standard_Right, Parabola_Definition, Parabola_Focal_Radius, Two_Points_Distance

---

## Problem Index: 2196
**ID**: 2197
**Text**:  
已知直线$y=k(x+3)(k>0)$与抛物线$C$: $y^{2}=12 x$相交于$A$、$B$两点,$F$为$C$的焦点, 若$|F A|=3|F B|$, 则$k$的值等于?

**Process**:  
设A(x_{1},y_{1}),B(x_{2},y_{2}).易知F(3,0)联立直线y=k(x+3)(k>0)与抛物线C:y^{2}=12x.化为k^{2}x^{2}+(6k^{2}-12)x+9k^{2}=0,(k>0)\thereforex_{1}+x_{2}=\frac{12}{k^{2}}-6\textcircled{1},x_{1}x_{2}=9\textcircled{2}.\because|FA|=3|FB|,根据抛物线的定义,可得|FA|=x_{1}+3,|FB|=x_{2}+3,\thereforex_{1}+3=3(x_{2}+3)\textcircled{3},化为x_{1}=3x_{2}+6.联立\textcircled{1}\textcircled{2}\textcircled{3},解得k=\frac{\sqrt{3}}{2}

**Theorem Sequence**:  
Parabola_Equation_Standard_Right, Line_Point_Slope_Form, Vieta_Theorem_Sum, Vieta_Theorem_Product, Vector_Collinear_Condition, Parabola_Definition, Parabola_Focal_Radius

---

## Problem Index: 2225
**ID**: 2226
**Text**:  
已知双曲线$C$: $\frac{x^{2}}{a^{2}}-\frac{y^{2}}{b^{2}}=1$的离心率$e=\frac{5}{4}$，且其右焦点为$F_{2}(5,0)$，则双曲线$C$的方程为?

**Process**:  
由离心率求出a,再由b^{2}=c^{2}-a^{2}求出b,得双曲线方程因为所求双曲线的右焦点为F_{2}(5,0)且离心率为e=\frac{c}{a}=\frac{5}{4},所以c=5,a=4,b^{2}=c^{2}-a^{2}=9,所以所求双曲线方程为\frac{x^{2}}{16}-\frac{y^{2}}{9}=1

**Theorem Sequence**:  
Hyperbola_Equation_Standard_X, Eccentricity_Formula, Hyperbola_Parameter_Relation

---

## Problem Index: 2269
**ID**: 2270
**Text**:  
直线$l$: $x=m y+2$经过抛物线$C$: $y^{2}=2 p x(p>0)$的焦点$F$，与抛物线相交于$A$、$B$两点，过原点的直线经过弦$A B$的中点$D$，并且与抛物线交于点$E$(异于原点)，则$\frac{|O D|}{|O E|}$的取值范围是?

**Process**:  
直线l:x=my+2经过(2,0)是抛物线C:y^{2}=2px(p>0)的焦点F(2,0),所以p=4,抛物线方程为:y^{2}=8x,联立\begin{cases}y2=8x\\x=my+2\end{cases},可得y^{2}-8my-16=0,\triangle=64m^{2}+64>0恒成立,设A(x_{1},y_{1})、B(x_{2},y_{2}所以y_{1}+y_{2}=8m,x_{1}+x_{2}=m(y_{1}+y_{2})+4=8m^{2}+4所以弦AB的中点D(4m^{2}+2,4m)所以OD的方程为:y=\frac{4m}{4m^{2}+2}x^{2}由题意可知m\neq0,与抛物线y^{2}=8x联立\begin{cases}y^{2}=8x\\y=\frac{4m}{4m^{2}+2}x\end{cases},解得y_{E}=\frac{4(2m^{2}+1)}{m}而\frac{|OD|}{|OE|}=\frac{|y_{D}|}{|y_{E}|}=\frac{m^{2}}{2m^{2}+1}=\frac{1}{2+\frac{1}{m2}},因为m^{2}>0,所以\frac{1}{m^{2}}>0,所以2+\frac{1}{m^{2}}>2,所以0<\frac{1}{2+\frac{1}{m2}}<\frac{1}{2},即0<\frac{|OD|}{|OE|}<\frac{1}{2},

**Theorem Sequence**:  
Parabola_Equation_Standard_Right, Substitution_x_equals_my_plus_n, Vieta_Theorem_Sum, Vieta_Theorem_Product, Midpoint_Formula, Line_Point_Slope_Form

---

## Problem Index: 2296
**ID**: 2297
**Text**:  
抛物线$y^{2}=2 x$的焦点坐标为?

**Process**:  
焦点在x轴的正半轴上,且p=1,利用焦点为(\frac{p}{2},0),写出焦点坐标.抛物线y^{2}=2x的焦点在x轴的正半轴上,且p=1,\therefore\frac{p}{2}=\frac{1}{2},故焦点坐标为(\frac{1}{2},0)

**Theorem Sequence**:  
Parabola_Equation_Standard_Right, Parabola_Directrix

---

## Problem Index: 2305
**ID**: 2306
**Text**:  
过抛物线$y^{2}=8 x$的焦点的弦$AB$中点的横坐标为$3$，则$|A B|$=?

**Process**:  
解析过程略

**Theorem Sequence**:  
None

---

## Problem Index: 2308
**ID**: 2309
**Text**:  
过椭圆$\frac{x^{2}}{16}+\frac{y^{2}}{9}=1$的右焦点$F$作与$x$轴垂直的直线与椭圆交于$A$、$B$两点，则以$A B$为直径的圆的面积是?

**Process**:  
解析由题意,在\frac{x2}{16}+\frac{y^{2}}{9}=1中,c=\sqrt{16-9}=\sqrt{7}故F(\sqrt{7},0).当x=\sqrt{7}时,y=\pm3\sqrt{1-\frac{7}{16}}=\pm\frac{9}{4},所以|AB|=\frac{9}{2}故以AB为直径的圆的面积是\pi\times(\frac{9}{4})^{2}=\frac{81\pi}{16}

**Theorem Sequence**:  
Ellipse_Equation_Standard_X, Ellipse_Latus_Rectum, Circle_Standard_Equation

---

## Problem Index: 2344
**ID**: 2345
**Text**:  
已知点$P(a, b)$是曲线$(x-2 y+2) \cdot \sqrt{12-3 x^{2}-4 y^{2}}=0$上的动点则$a^{2}+(b+\frac{1}{4})^{2}$的取值范围是?

**Process**:  
方程(x-2y+2)\cdot\sqrt{12-3x^{2}-4y^{2}}=0即\begin{cases}x-2y+2=0\\12-3x^{2}-4y2\geqslant0\end{cases}或2-3x^{2}-4y^{2}=0,即\begin{cases}x-2y+2=0\\\frac{x^{2}}{4}+\frac{y^{2}}{3}\leqslant0\end{cases}或\frac{x^{2}}{4}+\frac{y^{2}}{3}=1所以P对应的图形如图所示(椭圆及其内部的线段)设Q(0,-\frac{1}{4}),则|PQ|^{2}=a2+(b+\frac{1}{4})^{2},当P在椭圆上时,|PQ|^{2}=4(1-\frac{b^{2}}{3})+(b+\frac{1}{4})^{2}=-\frac{1}{3}(b-\frac{3}{4})^{2}+\frac{17}{4}而-\sqrt{3}\leqslantb\leqslant\sqrt{3},故(\sqrt{3}-\frac{1}{4})^{2}\leqslant|PQ|^{2}\leqslant\frac{17}{4},当P在椭圆内部的线段上时,有|PQ|^{2}\geqslant|\frac{|0+\frac{1}{2}+2|}{\sqrt{1+4}}}{^{2}}=\frac{5}{4},又此时|PQ|^{2}<\frac{17}{4},而\frac{5}{4}=1.25<(\sqrt{3}-\frac{1}{4})^{2}故|PQ|^{2}\in[\frac{5}{4},均答家头

**Theorem Sequence**:  
Ellipse_Equation_Standard_X, Line_Point_Slope_Form, Two_Points_Distance, Quadratic_Function_Maximum

---

## Problem Index: 2363
**ID**: 2364
**Text**:  
设点$Q$是椭圆$\frac{x^{2}}{36}+\frac{y^{2}}{9}=1$上异于长轴端点的任意一点，$F_{1}$、$F_{2}$为两焦点，动点$P$满足$\overrightarrow{P F}_{1}+\overrightarrow{P F_{2}}+\overrightarrow{P Q}=\overrightarrow{0}$，则动点$P$的轨迹方程为?

**Process**:  
设P(x,y),Q(x_{0},y_{0})(x_{0}\neq\pm6)由题可知:F_{1}(-3\sqrt{3},0),F_{2}(3\sqrt{3},0)由\overrightarrow{PF_{1}}+\overrightarrow{PF_{2}}+\overrightarrow{PQ}=\overrightarrow{0},所以(-3\sqrt{3}-x+3\sqrt{3}-x+x_{0}-x,-y-y+y_{0}-y)=(0,0)所以\begin{cases}x_{0}=3x\\y_{y}=3y\end{cases},(x\neq\pm2)又\frac{x_{0}^{2}}{36}+:\frac{y_{0}^{2}}{9}=1,所以\frac{x^{2}}{4}+y^{2}=1(x\neq\pm2)

**Theorem Sequence**:  
Ellipse_Equation_Standard_X, Vector_Collinear_Condition

---

## Problem Index: 2383
**ID**: 2384
**Text**:  
已知双曲线的顶点在坐标轴，中心在原点，渐近线经过点$P(m, 2 m)(m \neq 0)$，则双曲线的离心率为?

**Process**:  
分为焦点在x轴和y轴两种情况进行讨论,设出双曲线方程,求出渐近线方程,由渐近线经过点P(m,2m),求出a和b的关系,再利用c^{2}=a^{2}+b^{2}及e=\frac{c}{a}即可得解当焦点在x轴上时,设双曲线的方程为\frac{x^{2}}{a^{2}}-\frac{y^{2}}{b^{2}}=1(a>0,b>0),渐近线方程为y=\pm\frac{b}{a}x由渐近线经过点P(m,2m)(m\neq0),得2m=\frac{b}{a}m'解得b=2a.所以b^{2}=4a^{2},c^{2}=a^{2}+b^{2}=a^{2}+4a^{2}=5a^{2}双曲线的离心率e=\frac{c}{a}=\sqrt{5}当焦点在y轴上时,设双曲线的方程为\frac{y^{2}}{a^{2}}-\frac{x^{2}}{b^{2}}=1(a>0,b>0)渐近线方程为y=\pm\frac{a}{b}x,由渐近线经过点P(m,2m)(m\neq0),得2m=\frac{a}{b}m,解得b=\frac{1}{2}a.所以b^{2}=\frac{1}{4}a^{2},c^{2}=a^{2}+b^{2}=a^{2}+\frac{1}{4}a^{2}=\frac{5}{4}a^{2},双曲线的离心率e=\frac{c}{a}=\frac{\sqrt{5}}{2}综上,双曲线的离心率为\sqrt{5}或\frac{\sqrt{5}}{2}

**Theorem Sequence**:  
Hyperbola_Equation_Standard_X, Hyperbola_Equation_Standard_Y, Hyperbola_Asymptote, Eccentricity_Formula

---

## Problem Index: 2399
**ID**: 2400
**Text**:  
设椭圆$\frac{x^{2}}{25}+\frac{y^{2}}{16}=1$上一点$P$到左焦点$F$的距离为$4$，若点$M$满足$\overrightarrow{O M}=\frac{1}{2}(\overrightarrow{O P}+\overrightarrow{O F})$，则$|\overrightarrow{O M}|$=?

**Process**:  
由椭圆\frac{x^{2}}{25}+\frac{y^{2}}{16}=1得a=5,b=4,设椭圆的右焦点为F,则|PF|+|PF|=10,又点P到左焦点F的距离为4.所以|PF|=6,因为\overrightarrow{OM}=\frac{1}{2}(\overrightarrow{OP}+\overrightarrow{OF}),则M为PF的中点,又O为FF的中点,\therefore|OM|=\frac{1}{2}|PF|=3,即|\overrightarrow{OM}|=3.

**Theorem Sequence**:  
Ellipse_Equation_Standard_X, Ellipse_Definition, Triangle_Midline_Theorem

---

## Problem Index: 2435
**ID**: 2436
**Text**:  
已知椭圆$\frac{x^{2}}{9}+\frac{y^{2}}{4}=1$的两个焦点为$F_{1}$、$F_{2}$、$P$为椭圆上一动点，若$A B$是以点$P$为圆心，$1$为半径的圆的一条直径，则$\overrightarrow{F_{1} A} \cdot \overrightarrow{F_{1} B}+\overrightarrow{F_{2} A} \cdot \overrightarrow{F_{2} B}$的取值范围是?

**Process**:  
由向量的线性运算可得\overrightarrow{F_{1}A}\cdot\overrightarrow{F_{1}B}+\overrightarrow{F_{2}A}\cdot\overrightarrow{F_{2}B}=PF_{1}^{2}+PF_{2}^{2}-2=|PF_{1}|^{2}+|PF_{2}|^{2}-2'结合椭圆的定义可得|PF_{1}|^{2}+|PF_{2}|^{2}-2=2(|PF_{1}|-3)^{2}+16,然后由椭圆的几何性质可得|PF_{1}|\in[3-\sqrt{5},3+\sqrt{5}],再结合二次函数值域的求法即可得解.(详解]由已知条件可得|\overrightarrow{PA}|=|\overrightarrow{PB}|=1且\overrightarrow{PA}=-\overrightarrow{PB},则\overrightarrow{F_{1}A}\cdot\overrightarrow{F_{1}B}=(\overrightarrow{F_{1}P}+\overrightarrow{PA})\cdot(\overrightarrow{F_{1}P}+\overrightarrow{PB})=\overrightarrow{F_{1}P}^{2}+\overrightarrow{FP_{1}}\cdot(\overrightarrow{PA}+\overrightarrow{PB})+\overrightarrow{PA}\cdot\overrightarrow{PB}=\overrightarrow{FP_{1}}^{2}-1同理\overrightarrow{F_{2}A}\cdot\overrightarrow{F_{2}B}=\overrightarrow{FP_{2}}-1,则\overrightarrow{F_{1}A}\cdot\overrightarrow{F_{1}B}+\overrightarrow{F_{2}A}\cdot\overrightarrow{F_{2}B}=P\overrightarrow{F_{1}}^{2}+PF_{2}^{2}-2=|PF_{1}|^{2}+|PF_{2}|^{2}-2由椭圆的定义可得|PF_{1}|+|PF_{2}|=6,则|PF_{1}|^{2}+|PF_{2}|^{2}-2=|PF_{1}|^{2}+(6-|PF_{1}|)^{2}-2=2(|PF_{1}|-3)^{2}+16,由椭圆的几何性质可得|PF|\in[3-\sqrt{5},3+\sqrt{5}]即2(|PF_{1}|-3)^{2}+16\in[16,26]即\overrightarrow{F_{1}A}\cdot\overrightarrow{F_{1}B}+\overrightarrow{F_{2}A}\cdot\overrightarrow{F_{2}B}的取值范围是[16,26]

**Theorem Sequence**:  
Ellipse_Equation_Standard_X, Ellipse_Definition, Vector_Collinear_Condition, Ellipse_Parameter_Relation, Quadratic_Function_Maximum, Basic_Inequality

---

## Problem Index: 2437
**ID**: 2438
**Text**:  
已知点$F$是抛物线$x^{2}=4 y$的焦点，点$M(1,2)$，点$P$为抛物线上的任意一点，则$|P M|+|P F|$的最小值为?

**Process**:  
如图,过P作抛物线准线y=-1的垂线,垂足为Q,连接MQ,则|PM|+|PF|=|PM|+|PQ|\geqslant|MQ|\geqslant2+1=3,当且仅当M,P,Q共线时等号成立,故|PM|+|PF|的最小值为3,

**Theorem Sequence**:  
Parabola_Equation_Standard_Up, Parabola_Definition, Parabola_Directrix, Two_Points_Distance

---

## Problem Index: 2469
**ID**: 2470
**Text**:  
双曲线$9 x^{2}-16 y^{2}=144$的离心率$e$=?

**Process**:  
双曲线9x^{2}-16y^{2}=144即为\frac{x^{2}}{16}-\frac{y^{2}}{9}=1,其中a=4,b=3,c=\sqrt{4^{2}+3^{2}}=5,e=\frac{c}{a}=\frac{5}{4}

**Theorem Sequence**:  
Hyperbola_Equation_Standard_X, Hyperbola_Parameter_Relation, Eccentricity_Formula

---

## Problem Index: 2503
**ID**: 2504
**Text**:  
已知双曲线$C$的标准方程为$\frac{x^{2}}{a^{2}}-\frac{y^{2}}{b^{2}}=1(a>0, b>0)$，且其焦点$F(3,0)$到渐近线的距离等于$\sqrt{5}$，则双曲线的标准方程为?

**Process**:  
分析:根据双曲线C的标准方程求得双曲线的渐近线的方程,再根据焦点F(3,0)到渐近线的距离等于\sqrt{5},利用点到直线距离公式,即可得出\frac{3b}{c}=\sqrt{5},即可求出b,然后结合a^{2}=c^{2}-b^{2},从而求得双曲线的标准方程.详\because双曲线C的标准方程为\frac{x^{2}}{a^{2}}-\frac{y^{2}}{b^{2}}=1(a>0,b>0)\therefore双曲线的渐近线的方程为y=\pm\frac{b}{a}x'即bx\pmay=0.\because其焦点F(3,0)到新近线的距离等于\sqrt{5}\therefored=\frac{3b}{\sqrt{b^{2}+a^{2}}}=\sqrt{5},即\frac{3b}{c}=\sqrt{5}\becausec=3\becauseb=\sqrt{5}\thereforea^{2}=c^{2}-b^{2}=4\therefore双曲线的标准方程为\frac{x^{2}}{4}-\frac{y^{2}}{5}=1

**Theorem Sequence**:  
Hyperbola_Equation_Standard_X, Hyperbola_Asymptote, Hyperbola_Focus_To_Asymptote_Distance, Point_To_Line_Distance

---

## Problem Index: 2507
**ID**: 2508
**Text**:  
已知抛物线$C$: $y^{2}=6 x$，过抛物线的焦点$F$的直线$l$交抛物线于点$A$，交抛物线的准线于点$B$，若$\overrightarrow{F B}=3  \overrightarrow {FA}$，则点$A$到原点的距离为?

**Process**:  
抛物线C,准线垂直地x轴,垂足为D,|DF|=3,过A作准线的垂线,垂足为C,由抛物线的定义可知:|AF|=|AC|,\therefore3|AF|=|FB|,\therefore|AB|=2|AC|,由三角形相似得|AC|=2,则点A横坐标为|AC|-\frac{3}{2}=\frac{1}{2},故点A的坐标为(\frac{3}{2},-\sqrt{3}),则点A到原点的距离为\frac{\sqrt{13}}{2}

**Theorem Sequence**:  
Parabola_Equation_Standard_Right, Parabola_Definition, Parabola_Directrix, Pythagorean_Theorem, Two_Points_Distance

---

## Problem Index: 2526
**ID**: 2527
**Text**:  
直线$y=x$与抛物线$y^{2}=2 x$交于$A$、$B$两点，则$|A B|$=?

**Process**:  
联立\begin{cases}y=x\\y2=2x\end{cases}两个交点为A(0,0),B(2,2),故|AB|=\sqrt{(2-0)^{2}+(2-0)^{2}}=2\sqrt{2}

**Theorem Sequence**:  
Parabola_Equation_Standard_Right, Two_Points_Distance

---

## Problem Index: 2540
**ID**: 2541
**Text**:  
已知直线$l$: $y=k x+1  (k \in R)$，若直线$l$上总存在点$M$与两点$A(-1,0)$, $B(1,0)$连线的斜率之积为$-3 m(m>0)$，则实数$m$的取值范围是?

**Process**:  
先求出与两点A(-1,0),B(1,0)连线的斜率之积为-3m(m>0)的点M的轨迹方程,由方程确定曲线,然后利用直线l所过定点是否在曲线内部或曲线上来确定结论设M(x,y),则k_{PA}k_{PB}=\frac{y}{x+1}\times\frac{y}{x-1}=\frac{y^{2}}{x^{2}-1}=-3m,整理得x^{2}+\frac{y^{2}}{3m}=1由题意直线l:y=kx+1与曲线x^{2}+\frac{y^{2}}{3m}=1总有公共点.直线y=kx+l过定点P(0,1)当3m=1时,曲线x^{2}+\frac{y^{2}}{3m}=1表示圆x^{2}+y^{2}=1,也过定点P(0,1),满足题意;当3m>1时,曲线x^{2}+\frac{y^{2}}{3m}=1表示椭圆,定点P(0,1)在椭圆x^{2}+\frac{y^{2}}{3m}=1内部,满足题意,m>\frac{1}{3}当0<3m<1时,曲线x^{2}+\frac{y^{2}}{3m}=1表示椭圆,定点P(0,1)在椭圆x^{2}+\frac{y^{2}}{3m}=1外部,此时直线y=1与椭圆无公共点,不合题意,综上,m\geqslant\frac{1}{3}

**Theorem Sequence**:  
Ellipse_Equation_Standard_X, Slope_Formula, Vector_Perpendicular_Condition, Discriminant_Delta, Basic_Inequality

---

## Problem Index: 2561
**ID**: 2562
**Text**:  
已知点$A(4,0)$，抛物线$C$: $y^{2}=2 p x  (0<p<4)$的准线为$l$，点$P$在$C$上，作$P H \perp l$于$H$，且$|P H|=|P A|$ , $\angle A P H=120^{\circ}$，则$p$=?

**Process**:  
设焦点为F,则\anglePAF=\frac{\pi}{3},x_{P}=\frac{x_{P}+\frac{p}{2}}{2}+\frac{p}{2}\Rightarrowx_{P}=\frac{3p}{2},所以

**Theorem Sequence**:  
Parabola_Focal_Radius

---

## Problem Index: 2571
**ID**: 2572
**Text**:  
已知抛物线$C$的顶点在坐标原点，焦点与双曲线$\frac{x^{2}}{7}-\frac{y^{2}}{2}=1$的右焦点重合，则抛物线$C$的方程是?

**Process**:  
由于双曲线:\frac{x^{2}}{7}-\frac{y^{2}}{2}=1中a^{2}=7,b^{2}=2,所以c=3,从而它右焦点为(3,0),所以抛物线C的方程是y^{2}=12x

**Theorem Sequence**:  
Hyperbola_Equation_Standard_Y, Hyperbola_Parameter_Relation, Parabola_Equation_Standard_Right

---

## Problem Index: 2584
**ID**: 2585
**Text**:  
已知抛物线$C$: $y^{2}=2 p x(p>0)$的焦点为$F$，准线为$l$ , $A$ ,$B$是抛物线$C$上的两个动点，且$A F \perp A B$, $\angle A B F=30^{\circ}$，设线段$A B$的中点$M$在准线$l$上的射影为点$N$，则$\frac{|M N|}{|A B|}$的值是?

**Process**:  
如图示,作BE\botl,AD\botl,由抛物线定义,得|AF|=|AD|,|BF|=|BE|在梯形ABED中,2|MN|=|AD|+|BE|=a+b,因为且AF\botAB,\angleABF=30^{\circ},所以b=2a,则|MN|=\frac{3a}{2},又|AB|=\sqrt{b^{2}-a^{2}}=\sqrt{3}a故\frac{|MN|}{|AB|}=\frac{\frac{3a}{2}}{\sqrt{3}a}=\frac{\sqrt{3}}{2},

**Theorem Sequence**:  
Parabola_Equation_Standard_Right, Parabola_Definition, Parabola_Directrix, Pythagorean_Theorem, Vector_Collinear_Condition, Basic_Inequality

---

## Problem Index: 2587
**ID**: 2588
**Text**:  
已知$P$是椭圆$\frac{x^{2}}{12}+\frac{y^{2}}{4}=1$上不同于左顶点$A$，右顶点$B$的任意一点，记直线$PA$，$PB$的斜率分别为$k_{1}$, $k_{2}$, 则$k_{1} \cdot k_{2}$的值为?

**Process**:  
设P(x,y),A(-2\sqrt{3},0),B(-2\sqrt{3},0)则k_{1}=\frac{y}{x+2\sqrt{3}},k_{2}=k_{1}k_{2}=\frac{y}{x+2\sqrt{3}}\cdot\frac{y}{x-2\sqrt{3}}=\frac{y^{2}}{x^{2}-12},\cdots\cdots\textcircled{1}因为P在椭圆上,所以\frac{x^{2}}{12}+\frac{y^{2}}{4}=1,即y^{2}=\frac{12-x^{2}}{3}\cdots\cdots\textcircled{2}把\textcircled{2}代入\textcircled{1},得k_{1}k_{2}=\frac{y^{2}}{x^{2}-12}=-\frac{1}{3}

**Theorem Sequence**:  
Ellipse_Equation_Standard_X, Slope_Formula, Vector_Perpendicular_Condition, Ellipse_Parameter_Relation

---

## Problem Index: 2589
**ID**: 2590
**Text**:  
过双曲线$x^{2}-y^{2}=4$的右焦点$F$作倾斜角为$105^{\circ}$的直线，交双曲线于$P$、$Q$两点，则$|F P| \cdot|F Q|$的值为?

**Process**:  
由题意,F(2\sqrt{2},0),直线斜率k=\tan105^{\circ}=-(2+\sqrt{3}),所以直线方程为y=-(2+\sqrt{3})(x-2\sqrt{2}),代入x^{2}-y^{2}=4得(6+4\sqrt{3})x^{2}-4\sqrt{2}(7+4\sqrt{3})x+60+32\sqrt{3}=0,设P(x_{1},y_{1}),Q(x_{2},y_{2}),则x_{1}+x_{2}=\frac{4\sqrt{2}(7+4\sqrt{3})}{6+4\sqrt{3}},\cdotx_{2}=\frac{60+32\sqrt{3}}{6+4\sqrt{3}}又|FP|=\sqrt{1+k^{2}}|x_{1}-2\sqrt{2}|,|FQ|=\sqrt{1+k^{2}}|x_{2}-2\sqrt{2}|\therefore|FP|\cdot|FQ|=(1+k^{2})|x_{1}x_{2}-2\sqrt{2}(x_{1}+x_{2})+8|=(8+4\sqrt{3})\cdot|\frac{60+32\sqrt{3}}{6+4\sqrt{3}}-\frac{16(7+4\sqrt{3})}{6+4\sqrt{3}}+8|=\frac{(8+4\sqrt{3})(+4)}{6+4\sqrt{3}}=\frac{8\sqrt{3}}{3}

**Theorem Sequence**:  
Hyperbola_Equation_Standard_X, Line_Point_Slope_Form, Vieta_Theorem_Sum, Two_Points_Distance

---

## Problem Index: 2601
**ID**: 2602
**Text**:  
设$F_{1}$、$F_{2}$为椭圆$C$: $\frac{x^{2}}{a^{2}}+\frac{y^{2}}{b^{2}}=1(a>b>0)$的左、右焦点，过$F_{2}$的直线与椭圆交于$A$、$B$两点，若$\overrightarrow{A F_{1}} \cdot \overrightarrow{A F_{2}}=0$ , $\overrightarrow{A F_{2}}=3 \overrightarrow{F_{2} B}$，则椭圆$C$的离心率为?

**Process**:  
根据题意及椭圆的定义,设F_{2}B=x_{\prime}则可表示出其他各边长度,根据勾股定理,可求得x,在Rt\triangleAF_{1}F_{2}中,利用勾股定理,求得a与c的关系,代入公式即可得答案.由题意得,AF_{1}\botAF_{2},且|\overrightarrow{AF_{2}}|=3|\overrightarrow{F_{2}B}|,如图所示:设F_{2}B=x,则AF_{2}=3x.所以根据椭圆的定义可得AF_{1}=2a-3x,BF_{1}=2a-x因为AF_{1}\botAF_{2},所以(2a-x)^{2}=(2a-3x)^{2}+(3x+x)^{2}.解得x=\frac{a}{3}所以AF_{1}=2a-3x=a,AF_{2}=3x=a在Rt\triangleAF_{1}F_{2}中,AF_{1}2+AF_{2}2=F_{1}F_{2}2,即a^{2}+a^{2}=(2c)^{2}所以e=\frac{c}{a}=\sqrt{\frac{c^{2}}{a^{2}}}=\sqrt{\frac{1}{2}}=\frac{\sqrt{2}}{2}

**Theorem Sequence**:  
Ellipse_Equation_Standard_X, Ellipse_Definition, Vector_Collinear_Condition, Pythagorean_Theorem, Cosine_Law, Eccentricity_Formula

---

## Problem Index: 2609
**ID**: 2610
**Text**:  
双曲线$\frac{x^{2}}{9}-\frac{y^{2}}{16}=1$的离心率为?

**Process**:  
\because由题可知a=3,b=4\thereforec=\sqrt{3^{2}+4^{4}}=5\therefore离心率e=\frac{c}{a}=\frac{5}{3}

**Theorem Sequence**:  
Hyperbola_Parameter_Relation, Eccentricity_Formula

---

## Problem Index: 2622
**ID**: 2623
**Text**:  
已知椭圆$G$的中心在坐标原点，长轴在$y$轴上，离心率为$\frac{\sqrt{3}}{2}$，且$G$上一点到$G$的两个焦点的距离之和是$12$，则椭圆的方程是?

**Process**:  
由题意离心率为\frac{\sqrt{3}}{2},可得:\frac{c}{a}=\frac{\sqrt{3}}{2},且C上一点到C的两个焦点的距离之和是12可得2a=12,解得a=6,c=3,则b=3所以椭圆C的标准方程\frac{y^{2}}{36}+\frac{x^{2}}{9}=1.

**Theorem Sequence**:  
Ellipse_Equation_Standard_Y, Ellipse_Parameter_Relation, Eccentricity_Formula

---

## Problem Index: 2702
**ID**: 2703
**Text**:  
已知点$(3, \sqrt{15})$在双曲线$C$: $\frac{x^{2}}{a^{2}}-\frac{y^{2}}{12}=1(a>0)$上，则双曲线$C$的离心率是?

**Process**:  
由题意可得\frac{9}{a^{2}}-\frac{15}{12}=1,解得a=2,所以c=\sqrt{4+12}=4,故双曲线C的离心率是\frac{4}{3}=2.

**Theorem Sequence**:  
Hyperbola_Equation_Standard_X, Eccentricity_Formula

---

## Problem Index: 2723
**ID**: 2724
**Text**:  
圆$x^{2}+y^{2}=9$的切线$M T$过双曲线$\frac{x^{2}}{9}-\frac{y^{2}}{12}=1$的左焦点$F$，其中$T$为切点，$M$为切线与双曲线右支的交点，$P$为$M F$的中点，$O$为坐标原点，则$|P O|-|P T|$=?

**Process**:  
记右焦点F,|FF|=\sqrt{OF^{2}-|OT|}=b=|P|=|PF|-|FF|=\frac{1}{2}|MF|-b,|PO|=\frac{1}{2}|PF|\Rightarrow|PO|-|PF|=b-\frac{1}{2}|MF|-|MF|=b-a=2\sqrt{3}-3

**Theorem Sequence**:  
Hyperbola_Equation_Standard_X, Hyperbola_Focus_To_Asymptote_Distance, Triangle_Midline_Theorem

---

## Problem Index: 2725
**ID**: 2726
**Text**:  
若抛物线$y^{2}=8 a x$的焦点与双曲线$\frac{x^{2}}{a^{2}}-y^{2}=1$的右焦点重合，则双曲线的离心率为?

**Process**:  
抛物线y^{2}=8ax的焦点坐标为(2a,0),双曲线\frac{x^{2}}{a^{2}}-y^{2}=1的右焦点为(\sqrt{a^{2}+1},0),则2a=\sqrt{a^{2}+1},得a^{2}=\frac{1}{3},e=\sqrt{1+\frac{1}{a^{2}}}=2;

**Theorem Sequence**:  
Parabola_Equation_Standard_Right, Hyperbola_Equation_Standard_X, Eccentricity_Formula

---

## Problem Index: 2730
**ID**: 2731
**Text**:  
已知$F_{1}$、$F_{2}$是椭圆$\frac{x^{2}}{a^{2}}+\frac{y^{2}}{b^{2}}=1(a>b>0)$的左、右焦点，过左焦点$F_{1}$的直线交椭圆于$A$、$B$两点，且满足$|A B|=|B F_{2}|=4|B F_{1}|$则该椭圆的离心率是?

**Process**:  
先根据椭圆定义求得|AB|,|BF_{2}|,|AF_{2}|,再利用余弦定理列方程解得离心率.因为|BF_{2}|=4|BF_{1}||BF_{2}|+|BF_{1}|=2a,所以|BF_{2}|=4|BF_{1}|=\frac{8a}{5}\therefore|AB|=\frac{8a}{5},|AF_{1}|=\frac{6}{x}\frac{a}{5},|AF_{2}|=2a-\frac{6a}{5}=\frac{4a}{5}因此_{\cos}\angleABF_{2}=\frac{(\frac{8}{5}a)^{2}+(\frac{2}{5}a)^{2}}{2\times\frac{8}{5}a\times\frac{2}{5}a}=\frac{(\frac{8}{5}a)^{2}+(\frac{8}{5}a)^{2}-(\frac{4}{5}a)}{2\times\frac{8}{5}a\times\frac{8}{5}a}\therefore2a^{2}=5c^{2}\thereforee=\frac{\sqrt{10}}{5}

**Theorem Sequence**:  
Ellipse_Equation_Standard_X, Ellipse_Definition, Vector_Collinear_Condition, Pythagorean_Theorem, Cosine_Law, Eccentricity_Formula

---

## Problem Index: 2734
**ID**: 2735
**Text**:  
已知直线$x=t$与椭圆$\frac{x^{2}}{25}+\frac{y^{2}}{9}=1$交于$P$、$Q$两点，若点$F$为该椭圆的左焦点，则使$\overrightarrow{F P} \cdot \overrightarrow{F Q}$取最小值时$t$的值为?

**Process**:  
易知椭圆的左焦点为F(-4,0)根据对称性可设P(t,y_{0}),Q(t,-y_{0}),且-5<t<5,则\overrightarrow{FP}=(t+4,y_{0}),\overrightarrow{FQ}=(t+4,-所以\overrightarrow{FP}\cdot\overrightarrow{FQ}=(t+4,y_{0}).(t+-y_{0})=(t+4)^{2}-y_{0}^{2}.又因为y_{0}^{2}=9(1-\frac{t^{2}}{25})=9-\frac{9}{25}t^{2},所以\overrightarrow{FP}\cdot\overrightarrow{FQ}=(t+4)^{2}-y_{0}^{2}=\frac{34}{25}t^{2}+8t+7所以当t=-\frac{50}{17}时,\overrightarrow{FP}\cdot\overrightarrow{FQ}取得最小值.故填-\frac{50}{17}睛)本题主要考查了椭圆的标准方程,向量的数量积,二次函数的最值,属于中档题

**Theorem Sequence**:  
Ellipse_Equation_Standard_Y, Vector_Dot_Product_Algebraic, Quadratic_Function_Maximum

---

## Problem Index: 2755
**ID**: 2756
**Text**:  
当直线$k x-y+3=0$与椭圆$\frac{x^{2}}{16}+\frac{y^{2}}{4}=1$相切时，$k$=?

**Process**:  
将直线方程与椭圆方程联立整理得(1+4k^{2})x^{2}+24kx+20=0\thereforeA=0\therefore(24k)^{2}-4(1+4k^{2})\times20=0\thereforek=\pm\frac{\sqrt{5}}{4}

**Theorem Sequence**:  
Ellipse_Equation_Standard_X, Discriminant_Tangent_Condition

---

## Problem Index: 2761
**ID**: 2762
**Text**:  
已知抛物线$T$: $y^{2}=2 p x(p>0)$的准线被圆$C$: $x^{2}+y^{2}-4 y-4=0$截得的弦长为$4$，则抛物线$T$的方程为?

**Process**:  
将圆C的方程化为标准方程为x^{2}+(y-2)^{2}=8,则圆心C(0,2),半径r=2\sqrt{2}因为抛物线T的准线方程为x=-\frac{p}{2},所以圆心到准线的距离d=\frac{p}{2}由圆C的半径r=2\sqrt{2},弦长为4,得(\frac{p}{2})^{2}+2^{2}=(2\sqrt{2})^{2},解得p=4.于是抛物线T的方程y^{2}=8x.

**Theorem Sequence**:  
Parabola_Equation_Standard_Up, Circle_Standard_Equation, Parabola_Directrix, Point_To_Line_Distance

---

## Problem Index: 2764
**ID**: 2765
**Text**:  
已知斜率为$-\frac{1}{3}$的直线与椭圆$\frac{x^{2}}{9}+\frac{y^{2}}{7}=1$相交于不同的两点$A$、$B$、$M$为$y$轴上一点且满足$|M A|=|M B|$，则点$M$的纵坐标的取值范围是?

**Process**:  
设直线AB的方程为y=-\frac{1}{3}x由\begin{cases}y=-\frac{1}{3}x+t\\\frac{x^{2}}{9}+\frac{y^{2}}{7}=1\end{cases}消去y并化简得8x^{2}-6tx+9t^{2}-63=0设A(x_{1},y_{1}),B(x_{2},y_{2}),x_{1}+x_{2}=\frac{3}{4}t,x_{1}\cdotx_{2}=\frac{9t^{2}-63}{8}\triangle=36t^{2}-32(9t^{2}-63)>0,解得-2\sqrt{2}<t<2\sqrt{2}\frac{x_{1}+x_{2}}{由于}=\frac{3}{8}t,\frac{y_{1}+y_{2}}{2}=\frac{-\frac{1}{3}(x_{1}+x_{2})+2t}{2}=-\frac{1}{6}(x_{1}+x_{2})+t=-\frac{1}{6}\times\frac{3}{4}t+t=\frac{7}{8}tAB垂直平分线的方程为y-\frac{7}{8}t=3(x-\frac{3}{8}t)令x=0得y=-\frac{1}{4}t,也即M的纵坐标的取值范围是(\frac{2}{-\frac{\sqrt{2}}{2}},\frac{\sqrt{2}}{2})

**Theorem Sequence**:  
Ellipse_Equation_Standard_X, Vieta_Theorem_Sum, Vieta_Theorem_Product, Chord_Length_Formula_With_K, Midpoint_Formula, Line_Point_Slope_Form, Basic_Inequality

---

## Problem Index: 2782
**ID**: 2783
**Text**:  
与双曲线$\frac{x^{2}}{4}-\frac{y^{2}}{2}=1$有相同焦点且过点$P(2,1)$的双曲线的方程为?

**Process**:  
依题意,设所求双曲线为\frac{x^{2}}{a^{2}}-\frac{y^{2}}{b^{2}}=1(a>0,b>0)又两曲线有相同的焦点,所以a^{2}+b^{2}=c^{2}=4+2=6\textcircled{1}.又点P(2,1)在双曲线\frac{x^{2}}{a^{2}}-\frac{y^{2}}{b^{2}}=1上,所以\frac{4}{a^{2}}-\frac{1}{b^{2}}=1\textcircled{2}由\textcircled{1}\textcircled{2}联立得a2=b^{2}=3.故所求双曲线方程为\frac{x^{2}}{3}-\frac{y^{2}}{3}=1

**Theorem Sequence**:  
Ellipse_Equation_Standard_X, Hyperbola_Equation_Standard_X, Ellipse_Parameter_Relation

---

## Problem Index: 2794
**ID**: 2795
**Text**:  
直线$x-y-2=0$与抛物线$y^{2}=2 p x(p>0)$交于$A$、$B$两点，若线段$A B$被点$M(4,2)$平分，则抛物线的准线方程为?

**Process**:  
设A(x_{1},y_{1}),B(x_{2},y_{2}),由线段AB被点M(4,2)平分,可知y_{1}+y_{2}=4又y_{1}^{2}=2px_{1},y_{2}^{2}=2px_{2},所以(y_{1}+y_{2})(y_{1}-y_{2})=2p(x_{1}-x_{2})由题意可知,直线l的斜率存在,且为1,所以x_{1}\neqx_{2},所以4\times\frac{y_{1}-y_{2}}{x_{1}-x_{2}}=2p'即4\times1=2p,所以p=2.故抛物线的准线方程为x=-1

**Theorem Sequence**:  
Parabola_Equation_Standard_Right, Point_Difference_Method, Midpoint_Formula, Slope_Formula, Parabola_Directrix

---

## Problem Index: 2802
**ID**: 2803
**Text**:  
抛物线$C$: $y^{2}=2 p x(p>0)$的焦点为$F$、$M$是抛物线$C$上的点，$O$为坐标原点，若$\Delta O F M$的外接圆与抛物线$C$的准线相切，且该圆的面积为$9 \pi$，则$p$=?

**Process**:  
根据圆的性质与抛物线的定义列式求解即可.\because4OFM的外接圆与抛物线C的准线相切,\thereforeAOFM的外接圆的圆心到准线的距离等于圆的半径.\because圆的面积为9\pi,\therefore圆的半径为3,又\because圆心在OF的垂直平分线上,OF=\frac{p}{2},\therefore\frac{p}{2}+\frac{p}{4}=3,p=4.

**Theorem Sequence**:  
Parabola_Equation_Standard_Up, Circle_Standard_Equation, Parabola_Definition, Parabola_Directrix

---

## Problem Index: 2809
**ID**: 2810
**Text**:  
若抛物线$y^{2}=2 p x(p>0)$的焦点恰好是双曲线$\frac{x^{2}}{5}-\frac{y^{2}}{4}=1$的右焦点，则$p$=?

**Process**:  
抛物线y^{2}=2px(p>0)的焦点坐标为(\frac{p}{2},0),双曲线\frac{x^{2}}{5}-\frac{y^{2}}{4}=1中,a^{2}=5,b^{2}=4,\thereforec=\sqrt{a^{2}+b^{2}}=3,\therefore双曲线\frac{x^{2}}{5}-\frac{y^{2}}{4}=1的右焦点为(3,0),则\frac{p}{2}=3,得p=6.

**Theorem Sequence**:  
Parabola_Equation_Standard_Right, Hyperbola_Equation_Standard_X, Hyperbola_Parameter_Relation

---

## Problem Index: 2816
**ID**: 2817
**Text**:  
已知椭圆$C$: $\frac{x^{2}}{4}+\frac{y^{2}}{3}=1$的左右焦点为$F_{1}$、$F_{2}$, 点$A$、$B$在椭圆上 ($A$、$B$可以重合) 且$\overrightarrow{F_{1} A}=\lambda \overrightarrow{F_{2} B}(\lambda \in[\frac{1}{3}, 3])$，则$|F_{1} A|+|F_{2} B|$的取值范围是?

**Process**:  
画出图形,利用椭圆对称性将所求问题转化为求过焦点的弦长的范围问题,结合a,b,c和几何性质即可求解.如图,由\overrightarrow{F_{1}A}=\lambda\overrightarrow{F_{2}B}(\lambda\in[\frac{1}{3},3])可知,AB'与BF_{2}所在直线斜率应相等,由椭圆对称性可知,|BF_{2}|=|B'F_{1}|,当A,B点都集中在左端点时,|F_{1}A|=a-c=1,|F_{2}B|=a+c=3,此时\lambda=\frac{1}{3},同理当A,B点都集中在右端点时,\lambda=3,故所求问题转化为求过椭圆焦点的弦长范围,由几何性质可知,最短弦长为通径\frac{2b^{2}}{a}=3^{n}最长弦长为长轴2a=4,故|F_{1}A|+|F_{2}B|的取值范围是[3,4]

**Theorem Sequence**:  
Ellipse_Equation_Standard_X, Ellipse_Definition, Ellipse_Focal_Radius, Ellipse_Latus_Rectum, Basic_Inequality

---

## Problem Index: 2828
**ID**: 2829
**Text**:  
椭圆$\frac{x^{2}}{4}+\frac{y^{2}}{3}=1$的右焦点到直线$y = \sqrt{3} x$的距离为?

**Process**:  
因为椭圆方程为\frac{x^{2}}{4}+\frac{y^{2}}{3}=1所以c^{2}=a^{2}-b^{2}=1所以右焦点的坐标为(1,0)直线方程化为-般式为\sqrt{3}x-y=0由点到直线距离公式可得d=\frac{|\sqrt{3}\times1|}{\sqrt{1\sqrt{3}}^{2}+(-1}==\frac{\sqrt{3}}{2}

**Theorem Sequence**:  
Ellipse_Equation_Standard_X, Point_To_Line_Distance

---

## Problem Index: 2842
**ID**: 2843
**Text**:  
若椭圆$\frac{x^{2}}{12}+\frac{y^{2}}{m}=1$与双曲线$x^{2}-8 y^{2}=8$的焦点相同，则$m$的值为?

**Process**:  
将双曲线方程化为标准方程得:\frac{x^{2}}{8}-y^{2}=1,所以双曲线的焦点坐标为(\pm3,0),由于椭圆与双曲线有相同的焦点,所以由椭圆的方程得:m=12-9=3

**Theorem Sequence**:  
Hyperbola_Equation_Standard_X, Ellipse_Equation_Standard_X, Ellipse_Parameter_Relation

---

## Problem Index: 2861
**ID**: 2862
**Text**:  
已知椭圆$C$: $\frac{x^{2}}{a^{2}}+\frac{y^{2}}{b^{2}}=1(a>b>0)$的左、右焦点分别是$F_{1}$、$F_{2}$、$A$是椭圆上顶点，过点$F_{1}$作$F_{1} D \perp A F_{2}$，垂足为$D$，若$|F_{2} D|=\frac{1}{2}|F_{1} F_{2}|$，则椭圆$C$的离心率为?

**Process**:  
在RtAF_{1}DF_{2}中,若|F_{2}D|=\frac{1}{2}|F_{1}F_{2}|,则\angleDF_{1}F_{2}=30^{\circ}故\angleF_{1}F_{2}D=90^{\circ}-\angleDF_{1}F_{2}=90^{\circ}-30^{\circ}=60^{\circ}.又显然|AF_{1}|=|AF_{2}|,所以AAF_{1}F_{2}是等边三角形故|AF_{1}|=|F_{1}F_{2}|,即a=2c故\frac{c}{a}=\frac{1}{2},即椭圆C的离心率为\frac{1}{3}

**Theorem Sequence**:  
Ellipse_Equation_Standard_X, Ellipse_Latus_Rectum, Pythagorean_Theorem, Eccentricity_Formula

---

## Problem Index: 2862
**ID**: 2863
**Text**:  
已知椭圆$C$: $\frac{x^{2}}{9}+\frac{y^{2}}{b^{2}}=1(3>b>0)$的左，右焦点分别为$F_{1}$、$F_{2}$、$O$为坐标原点，$P$是椭圆上一点，延长$P F_{2}$与椭圆交于点$A$，若$|O F_{1}|=|O A|$ ,$\triangle O F_{1} A$的面积为$2$，则$|P F_{2}|$=?

**Process**:  
因为|OF_{1}|=|OA|,所以\angleF_{2}AF_{1}=90^{\circ},所以\triangleOF_{1}A的面积S=\frac{1}{2}\times\frac{1}{2}|AF_{1}|\cdot|AF_{2}|=2,所以|AF_{1}|\cdot|AF_{2}|=8,由椭圆的定义可得|AF_{1}|+|AF_{2}|=6,所以|\frac{|AF|}{|AF_{2}|=4}或||AF|_{1}|=4设|PF_{2}|=n,则|PF_{1}|=6-n,当\begin{cases}AF_{1}=2\\AF_{2}=4\end{cases}时,由勾股定理得|AF_{1}|^{2}+|AP|^{2}=|PF_{1}|^{2},即2^{2}+(4+n)^{2}=(6-n)^{2},解得n=\frac{4}{5};当|AF_{1}|AF_{1}|=4_{时},由勾股定理得4^{2}+(2+n)^{2}=(6-n)^{2},解得n=1;AF||=22综上,|PF_{2}|=1或\frac{4}{6}

**Theorem Sequence**:  
Ellipse_Equation_Standard_X, Ellipse_Definition, Pythagorean_Theorem, Cosine_Law

---

## Problem Index: 2866
**ID**: 2867
**Text**:  
已知双曲线$C$: $\frac{x^{2}}{a^{2}}-\frac{y^{2}}{b^{2}}=1(a>0 , b>0)$的左、右焦点分别为$F_{1}$、$F_{2}$，过$F_{1}$的直线$l$与圆$x^{2}+y^{2}=a^{2}$相切于点$T$，且直线$l$与双曲线$C$的右支交于点$P$，若$\overrightarrow {F_{1} P}=3 \overrightarrow{F_{1} T}$, 则双曲线$C$的离心率为?

**Process**:  
如图,由题可知,|OF_{1}|=|OF_{2}|=c,|OT|=a,则|F_{1}T|=b,\because\overrightarrow{F_{1}P}=3\overrightarrow{F_{1}T}\therefore|TP|=2b,|F_{1}P|=3b,又\because|PF_{1}|-|PF_{2}|=2a,\therefore|PF_{2}|=3b-2a.作F_{2}MOT,得F_{2}M=2a,|TM|=b,则|PM|=b.在Rt\triangleMPF_{2}中,|PM|^{2}+|MF_{2}|^{2}=|PF_{2}|^{2}即b^{2}+(2a)^{2}=(3b-2a)^{2}得2b=3a.又\becausec^{2}=a^{2}+b^{2},\thereforec^{2}=a^{2}+\frac{9}{4}a^{2},即4c^{2}=13a^{2}\thereforee=\frac{\sqrt{13}}{2},

**Theorem Sequence**:  
Hyperbola_Equation_Standard_X, Hyperbola_Asymptote, Vector_Collinear_Condition, Cosine_Law, Eccentricity_Formula

---

## Problem Index: 2884
**ID**: 2885
**Text**:  
斜率为$2$的直线$l$过双曲线$\frac{x^{2}}{a^{2}}-\frac{y^{2}}{b^{2}}=1(a>0, b>0)$的右焦点且与双曲线的左右两支分别相交，则双曲线的离心率$e$的取值范围?

**Process**:  
依据题意,结合图形可知,双曲线的一条渐近线的斜率\frac{b}{a}大于2.即\frac{b}{a}>2,因此该双曲线的离心率e=\frac{c}{a}=\sqrt{1+(\frac{b}{a})^{2}}>\sqrt{5}

**Theorem Sequence**:  
Hyperbola_Equation_Standard_X, Hyperbola_Asymptote, Hyperbola_Eccentricity_Range

---

## Problem Index: 2889
**ID**: 2890
**Text**:  
$\frac{x^{2}}{16}-\frac{y^{2}}{9}=1$，则此双曲线的离心率为?

**Process**:  
由双曲线的方程\frac{x^{2}}{16}-\frac{y^{2}}{9}=1,则a=4,b=3,所以c=\sqrt{a^{2}+b^{2}}=5所以双曲线的离心率为e=\frac{c}{a}=\frac{5}{4}

**Theorem Sequence**:  
Hyperbola_Equation_Standard_X, Hyperbola_Parameter_Relation, Eccentricity_Formula

---

## Problem Index: 2891
**ID**: 2892
**Text**:  
双曲线$\frac{x^{2}}{4}-\frac{y^{2}}{3}=1$的实轴端点为$M$、$N$，不同于$M$、$N$的点$P$在此双曲线上，那么$P M$,$P N$的斜率之积为?

**Process**:  
由双曲线\frac{x^{2}}{4}-\frac{y^{2}}{3}=1的实轴端点为M、N,可得M(-2,0),N(2,0)设P点的坐标为(x,y),可得\frac{x^{2}}{4}-\frac{y^{2}}{3}=1,y=\frac{3}{4}(x^{2}-4),可得k_{PM}\cdotk_{PN}=\frac{y}{x+2}\cdot\frac{y}{x-2}=\frac{y^{2}}{x2-4},将y=\frac{3}{4}(x-4)代入可得k_{PM}\cdotk_{PN}=\frac{3}{4},故答案:\frac{3}{4}睛】本题主要考查双曲线的性质及直线的斜率,掌握双曲线的性质并灵活运用是解题的关键

**Theorem Sequence**:  
Hyperbola_Equation_Standard_X, Slope_Formula, Vector_Perpendicular_Condition

---

## Problem Index: 2896
**ID**: 2897
**Text**:  
中心在坐标原心,焦点在$x$轴且长轴长为$18$,焦距为$6$的椭圆的标准方程为?

**Process**:  
根据题意,要求椭圆的焦点在x轴上,若长轴长为18,且焦距为6,即a=9,c=3,则b^{2}=a^{2}-c^{2}=81-9=72'故椭圆的标准方程为:\frac{x^{2}}{81}+\frac{y^{2}}{72}=1,

**Theorem Sequence**:  
Ellipse_Equation_Standard_X, Ellipse_Parameter_Relation

---

## Problem Index: 2921
**ID**: 2922
**Text**:  
点$P$的方程$\sqrt{(x-5)^{2}+y^{2}}-\sqrt{(x+5)^{2}+y^{2}}=8$所表示的曲线上的点，点$P$的纵坐标是$3$，则其横坐标为?

**Process**:  
取点F_{1}(-5,0),F_{2}(5,0),则|F_{1}F_{2}|=10,由题意得|PF_{2}|-|PF_{1}|=8<10,\therefore点P的轨迹为以F_{1}(-5,0),F_{2}(5,0)为焦点,a=4的双曲线的左支\therefore点P的轨迹方程为\frac{x^{2}}{16}-\frac{y^{2}}{9}=1(x<0),设点P(x_{0},3)(x_{0}<0),此时\frac{x_{0}^{2}}{16}-\frac{3^{2}}{3}=1,解得x_{0}=-4\sqrt{2}

**Theorem Sequence**:  
Hyperbola_Definition, Hyperbola_Equation_Standard_Y, Hyperbola_Parameter_Relation

---

## Problem Index: 2924
**ID**: 2925
**Text**:  
过抛物线$C$: $y=x^{2}$上的一点$M$(非顶点)作$C$的切线与$x$轴,$y$轴分别交于$A$、$B$两点，则$\frac{|M A|}{|M B|}$=?

**Process**:  
利用导数求出切线方程,分别得到两点的坐标,即可得到结果由y=x^{2},则y=2x.设点M(x_{0},x_{0}^{2})(x_{0}\neq0),则曲线C在M处的切线的斜率为k=2x_{0}.所以曲线C在M处的切线方程为:y-x_{0}=2x_{0}(x-x_{0})即y=2x_{0}x-x_{0}.所以A(\frac{x_{0}}{2},0),B(0,-x_{0})由M,A,B三点的坐标可得,A点为BM的中点所以\frac{|MA|}{|MB|}=\frac{1}{2}.

**Theorem Sequence**:  
Parabola_Equation_Standard_Up, Parabola_Tangent_Line, Vector_Collinear_Condition

---

## Problem Index: 2928
**ID**: 2929
**Text**:  
设抛物线为$y^{2}=4 x$，过点$(1,0)$的直线$l$与抛物线交于$P(x_{1}, y_{1})$ , $Q(x_{2}, y_{2})$两点，则$x_{1} x_{2}+y_{1} y_{2}$=?

**Process**:  
设直线l方程为x=ty+1,则\begin{cases}x=ty+1\\y=4x\end{cases},可得y^{2}-4ty-4=0\cdoty_{1}y_{2}=-4,又\becausey_{1}^{2}=4x_{1},y_{2}2=4x_{2}\thereforex_{1}x_{2}=\frac{y_{1}2y_{2}2}{16}=1所以x_{1}x_{2}+y_{1}y_{2}=1-4=-3

**Theorem Sequence**:  
Parabola_Equation_Standard_Right, Substitution_x_equals_my_plus_n, Vieta_Theorem_Sum, Vieta_Theorem_Product, Vector_Dot_Product_Algebraic

---

## Problem Index: 2957
**ID**: 2958
**Text**:  
若抛物线$x^{2}=2 p y(p>0)$的焦点在圆$x^{2}+y^{2}+2 x-1=0$上，则这条抛物线的准线方程为?

**Process**:  
求出圆x^{2}+y^{2}+2x-1=0与y轴正半轴的交点坐标,可得抛物线的焦点坐标,则答案可求.由x^{2}+y^{2}+2x\cdot1=0,取x=0,得y^{2}=1,即y=\pm1,\because抛物线x^{2}=2py(p>0)的焦点在圆x^{2}+y^{2}+2x\cdot1=0上\therefore可得抛物线x^{2}=2py(p>0)的焦点坐标为(0,1),则\frac{p}{2}=1\therefore抛物线x^{2}=2py(p>0)的准线方程为y=-\frac{p}{2}=-1.

**Theorem Sequence**:  
Circle_Standard_Equation, Parabola_Equation_Standard_Up, Parabola_Directrix

---

## Problem Index: 2997
**ID**: 2998
**Text**:  
设$P$是抛物线$y^{2}=2 x$上的一点，$A(a, 0)  (0<a<1)$，则$|P A|$的最小值是?

**Process**:  
由题意,点P(x,y)到点A(a,0)(a\inR)的距离d=\sqrt{(x-a)^{2}+y^{2}}\becausey^{2}=2x,\therefored=\sqrt{(x-a)^{2}+y^{2}}=\sqrt{(x-a)^{2}+2x}=\sqrt{[x-(a-1)]^{2}+2a-1}\because0<a<1,\therefore当x=0时,最小值为a,

**Theorem Sequence**:  
Parabola_Equation_Standard_Right, Two_Points_Distance, Quadratic_Function_Maximum

---

## Problem Index: 2999
**ID**: 3000
**Text**:  
椭圆$\frac{x^{2}}{a^{2}}+\frac{y^{2}}{b^{2}}=1  (a>b>0)$的两个焦点分别为$F_{1}$、$F_{2}$、$P$为椭圆上一点，且$|P F_{2}|=\frac{\sqrt{3}}{2}|P F_{1}|$  , 则 $\angle P F_{1} F_{2}$的最大值为?

**Process**:  
由椭圆的定义可得|PF_{1}|+|PF_{2}|=2a,又|PF_{2}|=\frac{\sqrt{3}}{2}|PF_{1}|可得|PF_{1}|=4(2-\sqrt{3})a_{1}|PF_{2}|=2\sqrt{3}(2-\sqrt{3})a在\trianglePF_{1}F_{2}中,|F_{1}F_{2}|=2c.2=\frac{|PF_{1}^{2}+|F_{1}F_{2}|^{2}-|PF_{2}|^{2}}{2|PF_{1}||F_{1}F_{2}|}=\frac{4c^{2}+[4(2-\sqrt{3})a]}{4c\cdot4(2-\sqrt{3})a}(2-\sqrt{3})a]\frac{\sqrt{3})a}{c}\geqslant2\times\frac{1}{4}=\frac{1}{2}当且仅当c=(2-\sqrt{3})a时取得等号,所以\anglePF_{1}F_{2}的最大值为\frac{\pi}{3}.

**Theorem Sequence**:  
Ellipse_Equation_Standard_X, Ellipse_Definition, Cosine_Law, Basic_Inequality

---

## Problem Index: 3007
**ID**: 3008
**Text**:  
已知中心在原点，焦点坐标为$(0, \pm 5 \sqrt{2})$的椭圆截直线$3 x-y-2=0$所得的弦的中点的横坐标为$\frac{1}{2}$，则该椭圆的方程为?

**Process**:  
设椭圆方程为\frac{y^{2}}{a^{2}}+\frac{x^{2}}{b^{2}}=1(a>b>0),则a^{2}=b^{2}+c^{2}=b^{2}+50\textcircled{1}设直线3x-y-2=0与椭圆相交的弦的端点为A(x_{1},y_{1}),B(x_{2},y_{2})则\begin{cases}b^{2}y_{1}^{2}+a^{2}x_{1}^{2}=a^{2}b^{2}\\b^{2}y_{2}+a^{2}x_{2}^{2}=a^{2}b^{2}\end{cases}\thereforeb^{2}(y_{1}-y_{2})(y_{1}+y_{2})+a(x_{1}-x_{2})(x_{1}+x_{2})=0而弦的中点的横坐标为\frac{1}{2},则纵坐标为-\frac{1}{2},即x_{1}+x_{2}=2\times\frac{1}{2}=1,y_{1}+y_{2}=2\times(-\frac{1}{2})=-11,\frac{y_{1}-y_{2}}{x_{1}-x_{2}}=3\thereforeb^{2}\times3\times(-1)+a^{2}\times1=0,即a^{2}=3b^{2}\textcircled{2}联立\textcircled{1}\textcircled{2}得:a^{2}=75,b^{2}=25故该椭圆的方程为\frac{y^{2}}{75}+\frac{x^{2}}{25}=

**Theorem Sequence**:  
Ellipse_Equation_Standard_Y, Point_Difference_Method_Ellipse, Midpoint_Formula, Line_Point_Slope_Form, Ellipse_Parameter_Relation

---

## Problem Index: 3017
**ID**: 3018
**Text**:  
设$F$是抛物线$C$: $y^{2}=4 x$的焦点，过$F$的直线$l$交抛物线$C$于$A$、$B$两点，当$|A B|=6$时，以$A B$为直径的圆与$y$轴相交所得弦长是?

**Process**:  
设A(x_{1},y_{1}),B(x_{2},y_{2}),\therefore|AB|=x_{1}+1+x_{2}+1=6\Rightarrowx_{1}+x_{2}=4,\therefore以AB为直径的圆的圆心到与y轴相交所得弦的弦心距为2,\therefore所求弦长为2\sqrt{3^{2}-2^{2}}=2\sqrt{5}

**Theorem Sequence**:  
Parabola_Equation_Standard_Right, Parabola_Definition, Parabola_Focal_Radius, Parabola_Focal_Chord_Length, Midpoint_Formula, Pythagorean_Theorem

---

## Problem Index: 3021
**ID**: 3022
**Text**:  
斜率为$-\frac{1}{3}$的直线$l$与椭圆$C$: $\frac{x^{2}}{a^{2}}+\frac{y^{2}}{b^{2}}=1 ( a>b>0)$相交于$A$、$B$两点，线段$A B$的中点坐标为$(1,1)$，则椭圆$C$的离心率等于?

**Process**:  
设A(x_{1},y_{1}),B(x_{2},y_{2}),则\frac{x_{1}^{2}}{a^{2}}+\frac{y_{1}^{2}}{b^{2}}=1\textcircled{1},\frac{x_{2}^{2}}{a^{2}}+\frac{y_{2}^{2}}{b^{2}}=1\textcircled{2}\because(1,1)是线段AB的中点,\frac{1}{2}(x_{1}+x_{2})=1,\frac{1}{2}(y_{1}+y_{2})=1,\because直线AB的方程是y=-\frac{1}{3}(x-1)+1,\thereforey_{1}-y_{2}=-\frac{1}{3}(x_{1}-x_{2}),\textcircled{1}\textcircled{2}两式相减可得:\frac{1}{a^{2}}(x_{1}^{2}-x_{2}^{2})+\frac{1}{b^{2}}(y_{1}^{2}-y_{2}^{2})=0,\therefore\frac{1}{a^{2}}(x_{1}-x_{2})(x_{1}+x_{2})+\frac{1}{b^{2}}(y_{1}-y_{2})(y_{1}+y_{2})=0,\therefore2\times\frac{1}{a^{2}}(x_{1}-x_{2})+2\times\frac{1}{b^{2}}(y_{1}-y_{2})=0,\therefore\frac{b^{2}}{a^{2}}=\frac{1}{3},\thereforee^{2}=1-\frac{b^{2}}{a^{2}}=\frac{2}{3}e=\frac{\sqrt{6}}{3}

**Theorem Sequence**:  
Ellipse_Equation_Standard_X, Point_Difference_Method_Ellipse, Midpoint_Formula, Slope_Formula, Line_Point_Slope_Form, Homogenization_Eccentricity, Eccentricity_Formula

---

## Problem Index: 3041
**ID**: 3042
**Text**:  
已知点$M$是抛物线$C$: $y^{2}=8 x$上一点，$F$为抛物线$C$的焦点，则以$M$为圆心，$|M F|=4$为半径的圆被直线$x=-1$截得的弦长为?

**Process**:  
如图所示眼据抛物线性质可得MF=MQ=4=2+x_{M}得M(2,4),所以M到x=1的距离为3,根据直线与圆的弦长公式可得:该弦长为2.\sqrt{16-9}=2\sqrt{7}

**Theorem Sequence**:  
Parabola_Equation_Standard_Right, Parabola_Definition, Parabola_Focal_Radius, Circle_Standard_Equation, Pythagorean_Theorem

---

## Problem Index: 3063
**ID**: 3064
**Text**:  
已知$F_{1}$、$F_{2}$分别是椭圆$C$: $\frac{x^{2}}{20}+\frac{y^{2}}{16}=1$的左右焦点，点$P$是椭圆$C$上任意一点，令$m= |\overrightarrow{P F_{1}}| \cdot |\overrightarrow {P F_{2}}|$，则$m$的最大值为?

**Process**:  
由椭圆定义可知|PF_{1}|+|PF_{2}|=2a=4\sqrt{5},所以_{m}=|PF_{1}|\cdot|PF_{2}|\leqslant(\frac{|PF_{1}|+|PF_{2}|}{2})^{2}=20当且仅当|PF_{1}|=|PF_{2}|=2\sqrt{5}时等号成立,所以m的最大值为20.

**Theorem Sequence**:  
Ellipse_Equation_Standard_X, Ellipse_Definition, Basic_Inequality

---

## Problem Index: 3065
**ID**: 3066
**Text**:  
已知$F$为抛物线$C$: $x^{2}=8 y$的焦点，$P$为$C$上一点，$M(-4 , 3)$，则$\triangle P M F$周长的最小值是?

**Process**:  
如图,F为抛物线C:x^{2}=8y的焦点,P为C上一点,M(-4,3)抛物线C:x^{2}=8y的焦点为F(0,2),准线方程为y=-2.过P作准线的垂线,垂足为Q,则有|PF|=|PQ||PM|+|PF|=|PM|+|PQ|\geqslant|MQ|=5当且仅当M,P,Q三点共线时,等号成立所以\trianglePMF的周长最小值为5+\sqrt{(-4)^{2}+(3-2)^{2}}=5+\sqrt{17}

**Theorem Sequence**:  
Parabola_Equation_Standard_Up, Parabola_Definition, Parabola_Directrix, Two_Points_Distance

---

## Problem Index: 3109
**ID**: 3110
**Text**:  
直线$l$过抛物线$C$: $y^{2}=2 p x(p>0)$的焦点$F(1,0)$且与$C$交于$A$、$B$两点，则$\frac{1}{|A F|}+\frac{1}{|B F|}$=?

**Process**:  
由题得,抛物线C:y^{2}=2px(p>0)的焦点F(1,0),所以\frac{p}{2}=1,故p=2.所以抛物线C的方程为:y^{2}=4x.可设A(x_{1},y_{1}),B(x_{2},y_{2}),由抛物线的定义可知:|AF|=x_{1}+1,|BF|=x_{2}+1当斜率不存在时,x_{1}=x_{2}=1,所以:\frac{1}{|AF|}+\frac{1}{|BF|}=\frac{1}{x_{1}+1}+\frac{1}{x_{2}+1}=\frac{1}{2}+\frac{1}{2}=1当斜率存在时,设直线l的斜率为k(k\neq0),则直线方程为:y=k(x-1)联立\begin{cases}y=k(x\\y^{2}=4x\end{cases}-1),整理得:k^{2}x^{2}-2(k^{2}+2)x+k^{2}=0,\frac{1}{+1}=\frac{x_{1}+x_{2}+2}{x_{1}x_{2}+x_{1}+x_{2}+1}=\frac{x_{1}+x_{2}+2}{x_{1}+x_{2}+2}=1.

**Theorem Sequence**:  
Parabola_Equation_Standard_Right, Substitution_x_equals_my_plus_n, Vieta_Theorem_Sum, Vieta_Theorem_Product, Parabola_Definition, Parabola_Focal_Radius, Basic_Inequality

---

## Problem Index: 3117
**ID**: 3118
**Text**:  
已知圆$C$:$(x-a)^{2}+(y-b)^{2}=r^{2}(b>0)$，圆心在抛物线$y^{2}=4 x$上，经过点$A(3,0)$，且与抛物线的准线相切，则圆$C$的方程为?

**Process**:  
抛物线y^{2}=4x的准线为x=-1,所以r=|a-(1)|=|a+1|又该圆经过点A(3,0),所以(3-a)^{2}+(0-b)^{2}=(a+1)^{2};圆心在抛物线y^{2}=4x上,所以b^{2}=4a,联立解方程组得a=2,b=2\sqrt{2}.所以所求圆的方程为(x-2)^{2}+(y-2\sqrt{2})^{2}=9

**Theorem Sequence**:  
Parabola_Equation_Standard_Right, Circle_Standard_Equation, Parabola_Definition, Parabola_Directrix

---

## Problem Index: 3153
**ID**: 3154
**Text**:  
双曲线$C$: $\frac{x^{2}}{3}-y^{2}=1$的焦距是?

**Process**:  
直接利用焦距公式得到答案.[详解]双曲线C:\frac{x^{2}}{3}-y^{2}=1,c^{2}=a^{2}+b^{2}=4,c=2焦距为2c=4

**Theorem Sequence**:  
Hyperbola_Equation_Standard_X, Hyperbola_Parameter_Relation

---

## Problem Index: 3176
**ID**: 3177
**Text**:  
双曲线$\frac{x^{2}}{9}-y^{2}=1$的渐近线方程为?

**Process**:  
通过双曲线方程可知:双曲线的焦点在横轴上,a=3,b=1,所以双曲线\frac{x^{2}}{9}-y2=1的渐近线方程为:y=\pm\frac{b}{a}x\Rightarrowy=\pm\frac{1}{3}x\Rightarrow\pmx-3y=0

**Theorem Sequence**:  
Hyperbola_Equation_Standard_X, Hyperbola_Asymptote

---

## Problem Index: 3181
**ID**: 3182
**Text**:  
已知双曲线$C$: $\frac{x^{2}}{a^{2}}-\frac{y^{2}}{b^{2}}=1(a>0, b>0)$的左，右焦点分别为$F_{1}$、$F_{2}$、$P$是该双曲线右支上一点，且$(\overrightarrow{O P}+\overrightarrow{O F_{2}}) \cdot \overrightarrow{P F_{2}}=0$ ($O$为坐标原点) , $2|\overrightarrow{P F_{1}}|=3|\overrightarrow{P F_{2}}|$，则双曲线$C$的离心率为?

**Process**:  
\because(\overrightarrow{OP}+\overrightarrow{OF})\cdot\overrightarrow{PF_{2}}=0,\therefore\triangleOPF_{2}为等腰三角形且|OP|=|OF_{2}|,又|OF_{1}|=|OF_{2}|\therefore|OP|=|OF_{1}|=|OF_{2}|,\thereforePF_{1}\botPF_{2}.又|PF_{1}|-|PF_{2}|=2a,2|PF_{1}|=3|PF_{2}|\therefore|PF_{1}|=6a,|PF_{2}|=4a,则(6a)^{2}+(4a)^{2}=(2c)^{2},可得\frac{c^{2}}{a^{2}}=13.\therefore双曲线C的离心率为\sqrt{13}

**Theorem Sequence**:  
Hyperbola_Equation_Standard_X, Hyperbola_Definition, Pythagorean_Theorem, Vector_Perpendicular_Condition, Eccentricity_Formula

---

## Problem Index: 3224
**ID**: 3225
**Text**:  
已知双曲线$\frac{x^{2}}{m}-\frac{y^{2}}{m+6}=1(m>0)$的虚轴长是实轴长的$2$倍，则双曲线的标准方程为?

**Process**:  
根据题中条件,得出2\sqrt{m}\times2=2\sqrt{m+6},求出m,即可得出双曲线方程.由题意可得:a^{2}=m,b^{2}=m+6,则实轴长为:2\sqrt{m},虚轴长为2\sqrt{m+6}因为虚轴长是实轴长的2倍,所以2\sqrt{m}\times2=2\sqrt{m+6},解得:m=2.代入\frac{x^{2}}{m}-\frac{y^{2}}{m+6}=1可得双曲线方程为\frac{x^{2}}{2}-\frac{y^{2}}{8}=1

**Theorem Sequence**:  
Hyperbola_Parameter_Relation

---

## Problem Index: 3235
**ID**: 3236
**Text**:  
设点$M$是椭圆$\frac{x^{2}}{a^{2}}+\frac{y^{2}}{b^{2}}=1(a>b>0)$上的点，以点$M$为圆心的圆与$x$轴相切于椭圆的焦点$F$，圆$Z$与$y$轴相交于不同的两点$P$、$Q$:且满足$|\overrightarrow{M P}+\overrightarrow{M Q}|=|\overrightarrow{P Q}|$则椭圆的离心率为?

**Process**:  
由向量加法的平行四边形法则知由于|\overrightarrow{MP}+\overrightarrow{MQ}|=|\overrightarrow{PQ}|,则以MP,MQ为邻边的平行四边形是矩形,再由对称性知其为正方形,从而易得a,b,c的关系式,变形后可求得离心率e详解]\because|\overrightarrow{MP}+\overrightarrow{MQ}|=|\overrightarrow{PQ}|,由向量加法的平行四边形法则知以MP,MQ为邻边的平行四边形是矩形,又|MP|=|MQ|,因此此四边形是正方形.以点M为圆心的圆与x轴相切于椭圆的焦点F则MF\botx轴,\therefore|MF|=\frac{b^{2}}{a},x_{M}=c,\therefore\frac{b^{2}}{a}=\sqrt{2}c^{2}\thereforeb^{2}=a^{2}-c^{2}=\sqrt{2}ac即e^{2}+\sqrt{2}e-1=0,\thereforee=\frac{-\sqrt{2}+\sqrt{6}}{2}-\sqrt{2}-\sqrt{6}舍去),\therefore_{e}=\frac{\sqrt{6}-\sqrt{2}}{}

**Theorem Sequence**:  
Ellipse_Equation_Standard_X, Circle_Standard_Equation, Vector_Perpendicular_Condition, Homogenization_Eccentricity

---

## Problem Index: 3238
**ID**: 3239
**Text**:  
已知椭圆两个焦点的坐标分别是$(-2,0)$ ,$(2,0)$，并且经过点$(\frac{5}{2},-\frac{3}{2})$，则它的标准方程为?

**Process**:  
因为椭圆的焦点在x轴上,所以设它的标准方程为\frac{x^{2}}{a^{2}}+\frac{y^{2}}{b^{2}}=1(a>b>0)所以a=\sqrt{10}又因为c=2,所以b^{2}=a^{2}-c^{2}=6,所以椭圆的标准方程为\frac{x^{2}}{10}+\frac{y^{2}}{6}=1客头+\frac{y^{2}}{c}=1

**Theorem Sequence**:  
Ellipse_Equation_Standard_X, Ellipse_Parameter_Relation

---

## Problem Index: 3259
**ID**: 3260
**Text**:  
如果方程$\frac{x^{2}}{2-m}-\frac{y^{2}}{m+1}=1$表示双曲线，则$m$的取值范围是?

**Process**:  
当焦点在x轴上时,2-m>0且m+1>0,解得-1<m<2;当焦点在y轴上时,2-m<0且m+1<0,此时无解.综上可知,当该方程表示双曲线时,m的取值范围是-1<m<2睛】本题主要考查了双曲线的标准方程,属于中档题

**Theorem Sequence**:  
Hyperbola_Equation_Standard_X, Hyperbola_Equation_Standard_Y

---

## Problem Index: 3261
**ID**: 3262
**Text**:  
已知双曲线$\frac{x^{2}}{a^{2}}-\frac{y^{2}}{b^{2}}=1(a>0, b>0)$的一条渐近线方程为$y=\sqrt{3} x$，若其右顶点到这条渐近线的距离为$\sqrt{3}$，则双曲线方程为?

**Process**:  
右顶点(a,0)到渐近线y=\sqrt{3}x的距离d=\frac{\sqrt{3}a}{2}=\sqrt{3},解得:a=2.由双曲线方程知其渐近线方程为y=\pm\frac{b}{a}x,\therefore\frac{b}{a}=\sqrt{3},解得:b=2\sqrt{3},\therefore双曲线方程为\frac{x^{2}}{4}-\frac{y^{2}}{12}=1

**Theorem Sequence**:  
Hyperbola_Equation_Standard_X, Hyperbola_Asymptote, Point_To_Line_Distance

---

## Problem Index: 3310
**ID**: 3311
**Text**:  
椭圆$\frac{x^{2}}{36}+\frac{y^{2}}{9}=1$和点$P(4,2)$，直线$l$经过点$P$且与椭圆交于$A$、$B$两点. 当$P$点恰好为线段$A B$的中点时，线段$A B$所在直线$l$的斜率为?

**Process**:  
设A(x_{1},y_{1}),B(x_{2},y_{2})则\begin{cases}\frac{x_{1}2}{36}+\frac{y_{1}}{9}=1\\\frac{x_{2}}{36}+\frac{y_{2}}{9}=1\end{cases},两式相减可得\frac{(x_{1}+x_{2})(x_{1}-x_{2})}{36}+\frac{(y_{1}+y_{2})(y_{1}-y_{2})}{9}=因为P(4,2)为线段AB的中点,所以\frac{x_{1}+x_{2}}{2}=4,\frac{y_{1}+y_{2}}{2}=2^{,}代入上式,则\frac{8(x_{1}-x_{2})}{36}+\frac{4(y_{1}-y_{2})}{9}=0^{,}整理可得k_{AB}=\frac{y_{1}^{2}-y_{2}}{2}=-\frac{1}{2}.

**Theorem Sequence**:  
Ellipse_Equation_Standard_X, Point_Difference_Method_Ellipse, Midpoint_Formula, Slope_Formula, Line_Point_Slope_Form

---

## Problem Index: 3328
**ID**: 3329
**Text**:  
已知双曲线$\frac{x^{2}}{a^{2}}-\frac{y^{2}}{b^{2}}=1$的焦点为$F_{1}$ , $F_{2}$ ,过左焦点$F_{1}$的直线交双曲线左支于$A$、$B$两点，若$|A F_{2}|+|B F_{2}|=2|A B|$，则$|A B|$等于?

**Process**:  
根据题意画图如下:由双曲线定义可得:|AF_{2}|-|AF|=2a,|BF_{2}|-|BF_{1}|=2a.\therefore|AF_{2}|+|BF_{2}|=4a+(|AF|+|BF_{1}|)=4a+|AB|.又已知|AF_{2}|+|BF_{2}|=2|AB|\therefore2|AB|=4a+|AB|,得|AB=4a

**Theorem Sequence**:  
Hyperbola_Definition, Ellipse_Focal_Triangle_Perimeter

---

## Problem Index: 3362
**ID**: 3363
**Text**:  
已知斜率为$1$的直线过椭圆$\frac{x^{2}}{4}+y^{2}=1$的右焦点交椭圆于$A$、$B$两点，则弦$A B$的长为?

**Process**:  
椭圆\frac{x2}{4}+y^{2}=1的右焦点为F(\sqrt{3},0),直线AB的方程为y=x-\sqrt{3}联立\begin{cases}y=x-\sqrt{3}\\\frac{x^{2}}{4}+y^{2}=1\end{cases}得5x^{2}-8\sqrt{3}x+8=0,a=8^{2}\times3-4\times5\times8=32>0设点A(x_{1},y_{1})、B(x_{2},y_{2}),由韦达定理可得x_{1}+x_{2}=\frac{8\sqrt{3}}{5},x_{1}x_{2}=\frac{8}{5}|AB|=\sqrt{2}\cdot\sqrt{(x_{1}+x_{2})^{2}-4x_{1}x_{2}}=\sqrt{2}\times\sqrt{(\frac{8\sqrt{3}}{5})^{2}-4\times\frac{8}{5}}=\frac{8}{5}

**Theorem Sequence**:  
Ellipse_Equation_Standard_X, Line_Point_Slope_Form, Vieta_Theorem_Sum, Vieta_Theorem_Product, Chord_Length_Formula_With_K

---

## Problem Index: 3381
**ID**: 3382
**Text**:  
已知直线$l$是过抛物线$x^{2}=4 y$焦点的一条直线，$l$与抛物线交于$A(x_{1}, y_{1})$, $B(x_{2}, y_{2})$两点.则$x_{1} x_{2}$=?

**Process**:  
因为抛物线x^{2}=4y焦点坐标为(0,1)显然直线的斜率存在,设直线方程为y=kx+1将直线y=kx+1代入抛物线x^{2}=4y,整理得x^{2}-4kx-4=0.\thereforex_{1}x_{2}=-4

**Theorem Sequence**:  
Parabola_Equation_Standard_Up, Vieta_Theorem_Sum, Vieta_Theorem_Product

---

## Problem Index: 3384
**ID**: 3385
**Text**:  
已知双曲线$C$: $x^{2}-y^{2}=1$，点$F_{1}$、$F_{2}$为其两个焦点，点$P$为双曲线$C$上一点，且满足$P F_{1} \perp P F_{2}$，则$|P F_{1}|+|P F_{2}|$=的值为?

**Process**:  
由题意,双曲线x^{2}-y^{2}=1,可得a=b=1,c=\sqrt{a^{2}+b^{2}}=1根据双曲线的定义,可得|PF_{1}|-|PF_{2}|=2a=2.因为满足PF_{1}\botPF_{2},可得|PF_{1}|^{2}+|PF_{2}|^{2}=|F_{1}F_{2}|^{2}=(2c)^{2}=8又由(|PF_{1}|-|PF_{2}|)^{2}=|PF_{1}|^{2}+|PF_{2}|^{2}-2|PF_{1}||PF_{2}|=4,可得|PF_{1}||PF_{2}|=2所以(|PF_{1}|+|PF_{2}|)^{2}=|PF_{1}|^{2}+|PF_{2}|^{2}+2|PF_{1}||PF_{2}|=8+4=12,所以|PF_{1}|+|PF_{2}|=2\sqrt{3}

**Theorem Sequence**:  
Hyperbola_Equation_Standard_X, Hyperbola_Definition, Pythagorean_Theorem, Vector_Perpendicular_Condition, Hyperbola_Parameter_Relation

---

## Problem Index: 3387
**ID**: 3388
**Text**:  
已知$F_{1}$、$F_{2}$分别为椭圆$C$:$ \frac{x^{2}}{a^{2}}+\frac{y^{2}}{b^{2}}=1(a>b>0)$的左，右焦点，点$P$为$C$的上顶点，且$\angle F_{1} P F_{2}=\frac{\pi}{3} $, $S_{\Delta F_{1} P F_{2}}=\sqrt{3}$. 则$C$的方程是?

**Process**:  
\angleF_{1}PF_{2}=\frac{\pi}{3}\Rightarrowa=2c,S_{\triangleF_{1}PF_{2}}=\frac{1}{2}\times2c\timesb=\sqrt{3},故_{b}=\frac{\sqrt{3}}{c}又a^{2}=b^{2}+c^{2},即4c^{2}=\frac{3}{c^{2}}+c^{2},解得:c^{2}=1,故a^{2}=4,b^{2}=3,所以C的方程是\frac{x^{2}}{4}+\frac{y^{2}}{3}=1

**Theorem Sequence**:  
Ellipse_Equation_Standard_X, Ellipse_Focal_Triangle_Area, Triangle_Area_Formula, Ellipse_Parameter_Relation

---

## Problem Index: 3392
**ID**: 3393
**Text**:  
双曲线$\frac{y^{2}}{9}-\frac{x^{2}}{4}=1$，焦点坐标为?

**Process**:  
由双曲线方程\frac{y^{2}}{9}-\frac{x^{2}}{4}=1可得a=3,b=2c=\sqrt{a^{2}+b^{2}}=\sqrt{13},由于此双曲线的焦点在y轴上,所以双曲线焦点坐标为(0,\pm\sqrt{13})

**Theorem Sequence**:  
Hyperbola_Equation_Standard_Y, Hyperbola_Parameter_Relation

---

## Problem Index: 3405
**ID**: 3406
**Text**:  
若直线$l$:$x-y+m=0$与椭圆$x^{2}+\frac{y^{2}}{2}=1$交于$A$、$B$两点，且线段$A B$的中点在圆$x^{2}+y^{2}=1$上，则$m$=?

**Process**:  
设点A(x_{1},y_{1})、B(x_{2},y_{2}),联立\begin{cases}y=x+m\\2x^{2}+y2=2\end{cases},可得3x^{2}+2mx+m^{2}-2=0A=4m^{2}-12(m^{2}-2)=24-8m^{2}>0,解得-\sqrt{3}<m<\sqrt{3},由韦达定理可得x_{1}+x_{2}=-\frac{2m}{3},则y_{1}+y_{2}=x_{1}+x_{2}+2m=\frac{4m}{3}所以,线段AB的中点为M(-\frac{m}{3},\frac{2m}{3})由题意可得(-\frac{m}{3})^{2}+(\frac{2m}{3})^{2}=1,解得m=\pm\frac{3\sqrt{5}}{5}.

**Theorem Sequence**:  
Ellipse_Equation_Standard_X, Vieta_Theorem_Sum, Vieta_Theorem_Product, Discriminant_Delta, Vector_Dot_Product_Algebraic, Vector_Perpendicular_Condition, Basic_Inequality

---

## Problem Index: 3422
**ID**: 3423
**Text**:  
已知抛物线$y^{2}=8 x$上有一条长为$9$的动弦$A B$，则$A B$中点到$y$轴的最短距离为?

**Process**:  
易知抛物线y^{2}=8x的准线方程为l:x=-2,设A(x_{1},y_{1}),B(x_{2},y_{2}),且AB的中点为C(x_{0},y_{0})分别过点A,B,C作直线l:x=-2的垂线,垂足分别为M,N,H,则|CH|=\frac{|AM|+|BN|}{2},由抛物线定义,得|MH|=\frac{|AM|+|BN|}{2}=\frac{|AF|+|BF|}{2}\geqslant\frac{|AB|}{2}=\frac{9}{2}(当且仅当A,B,F三点共线时取

**Theorem Sequence**:  
Parabola_Equation_Standard_Right, Parabola_Definition, Parabola_Directrix, Parabola_Focal_Radius, Midpoint_Formula, Basic_Inequality

---

## Problem Index: 3423
**ID**: 3424
**Text**:  
若椭圆$\frac{x^{2}}{a^{2}}+\frac{y^{2}}{b^{2}}=1$的焦点在$x$轴上，过点$(2,1)$作圆$x^{2}+y^{2}=4$的切线，切点分别为$A$ , $B$，直线$AB$恰好经过椭圆的右焦点和上顶点，则椭圆方程为?

**Process**:  
设M(2,1),圆x^{2}+y2=4的圆心为0,则AB是圆x^{2}+y^{2}=4与以oM为直径的圆的公共弦所在直线,以OM为直径的圆的方程为(x-1)^{2}+(y-\frac{1}{2})^{2}=\frac{5}{4},即x^{2}+y^{2}-2x-y=0,两圆方程相减,即得AB的方程为2x+y=4,则直线与坐标轴的交点为(2,0).(0,4),又因为焦点在x轴上,则c=2,b=4,a^{2}=20,所以椭圆方程为\frac{x^{2}}{20}+\frac{y^{2}}{16}=1

**Theorem Sequence**:  
Circle_Standard_Equation, Ellipse_Equation_Standard_X, Ellipse_Parameter_Relation

---

## Problem Index: 3429
**ID**: 3430
**Text**:  
若实数$x$ , $y$满足方程$\sqrt{x^{2}+(y+3)^{2}}+\sqrt{x^{2}+(y-3)^{2}}=10$，则$\sqrt{(x-1)^{2}+y^{2}}+\sqrt{x^{2}+(y-3)^{2}}$的取值范围为?

**Process**:  
由已知条件得出点P在以F_{1}(0,3),F_{2}(0,-3)为焦点,以10为长轴长的椭圆上,再由两点的距离公椭圆的定义将问题转化为求d=10+|PA|-|PF_{2}|的范围,根据两点的距离公式可求得范围设点P(x,y),则由椭圆的定义得点P在以F_{1}(0,3)F_{2}(0,-3)为焦点,以10为长轴长的椭圆上,所在椭圆的方程为:\frac{x^{2}}{16}+\frac{y^{2}}{25}=1,而\sqrt{(x-1)^{2}+y^{2}}+\sqrt{x^{2}+(y-3)^{2}}表示点P(x,y)到点A(1,0)F_{1}(0,3)的距离之和,即d=|PA|+|PF_{1}|,由椭圆的定义得|PF_{1}|+|PF_{2}|=2a=10,所以|PF_{1}|=10-|PF_{2}|,所以d=|PA|+|PF_{1}|=|PA|+(10-|PF_{2}|)=10+|PA|-|PF_{2}|,而-|AF_{2}|\leqslant|PA|-|PF_{2}|\leqslant|AF_{2}|,又|AF_{2}|=\sqrt{1^{2}+3^{2}}=\sqrt{10},所以D.所以\sqrt{10}\leqslantd=10+|PA|-|PF_{2}|\leqslant10+\sqrt{10},

**Theorem Sequence**:  
Ellipse_Definition, Ellipse_Equation_Standard_Y, Ellipse_Focal_Radius, Two_Points_Distance, Basic_Inequality

---

## Problem Index: 3449
**ID**: 3450
**Text**:  
与双曲线$\frac{x^{2}}{16}-\frac{y^{2}}{9}=1$共渐近线且过点$(2 \sqrt{3},-3)$的双曲线方程是?

**Process**:  
据题意可设所求方程》3\frac{x^{2}}{16}-\frac{y^{2}}{9}=,\lambda,把(2\sqrt{3},-3))代入易得\lambda=-\frac{1}{4},故所求双曲线方程为\frac{\frac{y^{2}}{9}}{4}-\frac{x^{2}}{4}=1答案:\frac{y^{2}}{\frac{9}{4}}-\frac{x^{2}}{4}=1

**Theorem Sequence**:  
Hyperbola_Equation_Standard_Y, Hyperbola_Asymptote, Hyperbola_Common_Asymptote_System

---

## Problem Index: 3452
**ID**: 3453
**Text**:  
已知椭圆$C$: $\frac{x^{2}}{a^{2}}+\frac{y^{2}}{b^{2}}=1(a>b>0)$的左焦点为$F$，右顶点为$A$，若椭圆$C$上存在点$P$使得$P F \perp P A$，则椭圆$C$的离心率$e$的取值范围是?

**Process**:  
设点P(x,y).由\angleAPF=90^{\circ}知,点P在以FA为直径的圆上.圆的方程是(x-\frac{a-c}{2})^{2}+y^{2}=(\frac{a+c}{2})^{2},即y^{2}=(a-c)x-x^{2}+ac^{\circ}\textcircled{1}又点P在椭圆上,故\frac{x^{2}}{a^{2}}+\frac{y^{2}}{b^{2}}=1\textcircled{2}把\textcircled{1}代入\textcircled{2},得(a^{2}-b^{2})x^{2}-a^{2}(a-c)x+a^{2}b^{2}-a^{3}c=0.故(x-a)[(a^{2}-b^{2})x-ab^{2}+a^{2}c]=0因为x\neqa,所以x=\frac{ab^{2}-a^{2}c}{a^{2}-b^{2}}又-c<x<a,\therefore-c<\frac{ab^{2}-a2c}{a2-b^{2}}<a\therefore2ab^{2}<a^{2}c+a^{3},即2a(a^{2}-c^{2})<a^{2}c+a^{3}两边同处c^{3},整理得:2(\frac{c}{a})^{2}+(\frac{c}{a})-1>0,即2e^{2}+e-1>0,解得:e>\frac{1}{2}或e<-又0<e<1,\therefore所求椭圆的离心率的取值范围是e\in(\frac{1}{2},1)

**Theorem Sequence**:  
Ellipse_Equation_Standard_X, Vector_Perpendicular_Condition, Circle_Standard_Equation, Ellipse_Parameter_Relation, Homogenization_Eccentricity, Ellipse_Eccentricity_Range

---

## Problem Index: 3478
**ID**: 3479
**Text**:  
若双曲线$\frac{x^{2}}{a^{2}}-\frac{y^{2}}{b^{2}}=1(a>0, b>0)$的渐近线方程是$y=\pm \frac{1}{2} x$，则双曲线的离心率为?

**Process**:  
由题意得:\frac{b}{a}=\frac{1}{2}e=\sqrt{1+\frac{b^{2}}{a^{2}}}=\sqrt{\frac{5}{4}}=\frac{\sqrt{5}}{2}

**Theorem Sequence**:  
Hyperbola_Asymptote, Eccentricity_Formula

---

## Problem Index: 3494
**ID**: 3495
**Text**:  
直线$y=k x+2$与焦点在$x$轴上的椭圆$\frac{x^{2}}{16}+\frac{y^{2}}{b^{2}}=1(b>0)$恒有两个公共点，则实数$b$的取值范围是?

**Process**:  
求出直线定点,数形结合将题意转化为定点需在椭圆内求出b>2,又因为椭圆的焦点在x轴上,所以b<a=4,取交集即可得解.直线恒过定点(0,2),要保证直线与椭圆有两个公共点则定点需在椭圆内,所以\frac{0}{16}+\frac{4}{b^{2}}<1,解得b>2,又因为椭圆的焦点在x轴上,所以b<a=4,即b\in(2,4)

**Theorem Sequence**:  
Ellipse_Equation_Standard_X, Line_Point_Slope_Form, Discriminant_Delta

---

## Problem Index: 3536
**ID**: 3537
**Text**:  
平面上到两定点$(4,0)$与$(-4,0)$的距离之和为$8$的动点的轨迹方程为?

**Process**:  
记点A(4,0)、B(-4,0),设所求点为P,由|PA|+|PB|=|AB|可得知点P的轨迹,进而可得出点P的轨迹方程.记点A(4,0)、B(-4,0),设所求点为P,则|PA|+|PB|=|AB|.则点P的轨迹为线段AB,即所求动点的轨迹方程为y=0(-4\leqslantx\leqslant4)

**Theorem Sequence**:  
Two_Points_Distance

---

## Problem Index: 3566
**ID**: 3567
**Text**:  
已知抛物线$C$的方程为$y=-4 x^{2}$，则$C$的焦点坐标是?

**Process**:  
由抛物线C的方程为y=-4x^{2},得出其标准方程为x^{2}=-\frac{1}{4}y.则焦点坐标为(0,-\frac{1}{16})

**Theorem Sequence**:  
Parabola_Equation_Standard_Down

---

## Problem Index: 3570
**ID**: 3571
**Text**:  
已知椭圆$C$: $\frac{x^{2}}{a^{2}}+\frac{y^{2}}{b^{2}}=1(a>b>0)$的左、右焦点分别为$F_{1}$、$F_{2}$、$P$为椭圆上一点，且满足$\overrightarrow{P F_{1}} \cdot(\overrightarrow{O F_{1}}+\overrightarrow{O P})=0$($O$为坐标原点)若$|P F_{1}|=\sqrt{2}|P F_{2}|$，则椭圆的离心率为?

**Process**:  
如图,取PF_{1}的中点A,连接OA,\overrightarrow{A}=\overrightarrow{OF_{1}}+\overrightarrow{OP},\overrightarrow{OA}=\frac{1}{2}\overrightarrow{F_{2}P}\therefore\overrightarrow{OF_{1}}+\overrightarrow{OP}=\overrightarrow{F_{2}P},\because\overrightarrow{PF}\cdot(\overrightarrow{OF}+\overrightarrow{OP})=0,\therefore\overrightarrow{PF_{1}}\cdot\overrightarrow{F_{2}P}=0,\therefore\overrightarrow{PF_{1}}\bot\overrightarrow{F_{2}P},\because|\overrightarrow{PF_{1}}|=\sqrt{2}|\overrightarrow{PF_{2}}|,不妨设|PF_{2}|=m,则|PF_{1}|=\sqrt{2}m,\because|PF_{2}|+|PF_{1}|=2a=m+\sqrt{2}m,\thereforem=\frac{2}{1+\sqrt{2}}a=2(\sqrt{2}-1)a,\because|F_{1}F_{2}|=2c,\therefore4c^{2}=m^{2}+2m^{2}=3m^{2}=3\times4a^{2}(3-2\sqrt{2})\therefore\frac{c^{2}}{a^{2}}=9-6\sqrt{2}=(\sqrt{6}-\sqrt{3})^{2}\thereforee=\sqrt{6}-\sqrt{3},

**Theorem Sequence**:  
Ellipse_Equation_Standard_X, Ellipse_Definition, Vector_Dot_Product_Algebraic, Vector_Perpendicular_Condition, Eccentricity_Formula

---

## Problem Index: 3588
**ID**: 3589
**Text**:  
双曲线$\frac{x^{2}}{2}-y^{2}=1$的实轴长为?

**Process**:  
由\frac{x^{2}}{2}-y^{2}=1得,a^{2}=2,故实轴长为2a=2\sqrt{2}

**Theorem Sequence**:  
Hyperbola_Equation_Standard_X, Hyperbola_Equal_Axis

---

## Problem Index: 3593
**ID**: 3594
**Text**:  
设抛物线$y^{2}=2 x$的焦点为$F$，过点$F$的直线$l$与抛物线交于$A$、$B$两点，且$|A F|=4|B F|$，则弦长$A B$=?

**Process**:  
求出抛物线的焦点坐标,由直线方程的点斜式写出直线l的方程,和抛物线方程联立后利用弦长公式得答案.抛物线焦点坐标为F(\frac{1}{2},0)设点A(x_{1},y_{1}),A(x_{2},y_{2})设直线l方程为x=my+\frac{1}{2},由抛物线的定义有|AF|=x_{1}+\frac{p}{2}=x_{1}+\frac{1}{2},|BF|=x_{2}+\frac{p}{2}=x_{2}+\frac{1}{2}由|AF|=4|BF|,得x_{1}+\frac{1}{2}=4(x_{2}+\frac{1}{2}),即my_{1}+1=4(my_{2}+所以有m(y_{1}-4y_{2})=3\cdots\cdots(1)又由\begin{cases}x=my+\frac{1}{2}\\y2=2x\end{cases}得:y^{2}-2my-1=0,所以y_{1}+y_{2}=2m,y-1\cdots\cdots(2)由(1),(2)联立解得:m^{2}=\frac{9}{16}又|AB|=|AF|+|BF|=x_{1}+x_{2}+1=my+my_{2}+2=m(y_{1}+y_{2})+2=2m^{2}+2=2\times\frac{9}{16}+2=\frac{25}{8}

**Theorem Sequence**:  
Parabola_Equation_Standard_Right, Substitution_x_equals_my_plus_n, Vieta_Theorem_Sum, Parabola_Focal_Radius, Basic_Inequality

---

## Problem Index: 3620
**ID**: 3621
**Text**:  
若点$H(2,4)$在抛物线$y^{2}=2 p x$上，则实数$p$的值为?

**Process**:  
将点H的坐标代入抛物线的方程,得4^{2}=2p\times2,解得p=4.

**Theorem Sequence**:  
Parabola_Equation_Standard_Right

---

## Problem Index: 3676
**ID**: 3677
**Text**:  
已知椭圆$\frac{x^{2}}{25}+\frac{y^{2}}{16}=1$，则椭圆的焦点坐标是?

**Process**:  
由题意得:a^{2}=25,b^{2}=16由a^{2}=b^{2}+c^{2}得:c=\sqrt{25-16}=3\therefore焦点坐标为(\pm3,0)本题正确结果:(-3,0),(3,0)

**Theorem Sequence**:  
Ellipse_Equation_Standard_X, Ellipse_Parameter_Relation

---

## Problem Index: 3681
**ID**: 3682
**Text**:  
直线$l$交椭圆$\frac{x^{2}}{4}+y^{2}=1$于$A$、$B$两点，线段$A B$中点坐标为$(-\frac{4}{5}, \frac{1}{5})$，则直线$l$的方程为?

**Process**:  
设A(x_{1},y_{1}),B(x_{2},y_{2}),代入椭圆方程得\begin{cases}\frac{x^{2}}{4}+y^{2}=1\\-\frac{1}{4}+\frac{x+x}{4}+y^{2}=\frac{y-y_{2}}{y_{1}}\end{cases}.两式作差并化简得故填:y=x+1.

**Theorem Sequence**:  
Ellipse_Equation_Standard_X, Point_Difference_Method_Ellipse, Midpoint_Formula, Slope_Formula, Line_Point_Slope_Form

---

## Problem Index: 3686
**ID**: 3687
**Text**:  
已知抛物线$y^{2}=4 x$上一点$P$到准线的距离为$d_{1}$，到直线$l$:$ 4 x-3 y+11=0$的距离为$d_{2}$，则$d_{1}+d_{2}$的最小值为?

**Process**:  
(分析】根据抛物线的定义可知,点P到抛物线准线的距离等于点P到焦点F的距离,过焦点F作直线l:4x-3y+11=0的垂线,此时d_{1}+d_{2}取得最小值,利用点到直线的距离公式,即可求解由题意,抛物线y^{2}=4x的焦点坐标为F(1,0),准线方程为x=-1.如图所示,根据抛物线的定义可知,点P到抛物线准线的距离等于点P到焦点F的距离过焦点F作直线l:4x-3y+11=0的垂线,此时d_{1}+d_{2}取得最小值,由点到直线的距离公式可得\frac{|4\times1+11|}{\sqrt{4^{2}+(-3)^{2}}}=3即d_{1}+d_{2}的最小值为3.的标准方程及其简单的几何性质的应用,以及抛物线的最值问题,其中解答中根据抛物线的定义可知,点P到抛物线准线的距离等于点P到焦点F的距离,利用点到直线的距离公式求解是解答的关键,若重考查了转化思想,以及运算与求解能力,属于中档试题

**Theorem Sequence**:  
Parabola_Equation_Standard_Right, Parabola_Definition, Parabola_Directrix, Point_To_Line_Distance

---

## Problem Index: 3689
**ID**: 3690
**Text**:  
求以椭圆$\frac{x^{2}}{16}+\frac{y^{2}}{9}=1$的短轴的两个端点为焦点，且过点$A(4 ,-5)$的双曲线的标准方程?

**Process**:  
\frac{x2}{16}+\frac{y^{2}}{9}=1中短轴的端点为(0,\pm3),所以双曲线中焦点为(0,\pm3),点A(4,-5)到两焦点的距离之和为2\sqrt{5}\therefore2a=2\sqrt{5}\thereforea=\sqrt{5}\thereforeb^{2}=c^{2}-a^{2}=4,所以双曲线方程为\frac{y^{2}}{5}-\frac{x^{2}}{4}=1

**Theorem Sequence**:  
Ellipse_Equation_Standard_Y, Hyperbola_Equation_Standard_Y, Hyperbola_Parameter_Relation

---

## Problem Index: 3733
**ID**: 3734
**Text**:  
$F_{1}$、$F_{2}$是椭圆$C_{1}$和双曲线$C_{2}$的公共焦点，$e_{1}$ , $e_{2}$分别为曲线$C_{1}$、$C_{2}$的离心率，$P$为曲线$C_{1}$、$C_{2}$的一个公共点，若$\angle F_{1} P F_{2}=\frac{\pi}{3}$，且$e_{2} \in[\sqrt{3}, 2]$，则$e_{1} \in$?

**Process**:  
如图所示,设双曲线C_{2}的标准方程为:\frac{x^{2}}{a_{1}}-\frac{y^{2}}{b_{1}2}=1(a_{1},b_{1}>0),半焦距为c椭圆C_{1}:\frac{x^{2}}{a^{2}}+\frac{y^{2}}{b^{2}}=1(a>b>0),半焦距为c.不妨设点P在第一象限,设|PF_{1}|=m,|PF_{2}|=n.\thereforem+n=2a,m\cdotn=2a_{1}.\Rightarrowm=a+a_{1}.n=a-a_{1}在\trianglePF_{1}F_{2}中,由余弦定理可得:4c^{2}=m^{2}+n^{2}\cdot2mn\cos\frac{\pi}{3}.4c^{2}=a^{2}+3a_{1}^{2}两边同除以c^{2},得\frac{1}{e_{1}^{2}}+\frac{3}{e_{2}^{2}}=4,\because\frac{1}{e_{2}}\in[\frac{1}{4},\frac{1}{3}],\therefore\frac{1}{e_{1}}\in[3,\frac{13}{4}]

**Theorem Sequence**:  
Ellipse_Definition, Hyperbola_Definition, Cosine_Law, Basic_Inequality, Homogenization_Eccentricity, Ellipse_Eccentricity_Range

---

## Problem Index: 3738
**ID**: 3739
**Text**:  
设双曲线$C$: $\frac{x^{2}}{a^{2}}-\frac{y^{2}}{b^{2}}=1(a>0, b>0)$的左、右焦点分别是$F_{1}$、$F_{2}$，过$F_{1}$的直线交双曲线$C$的左支于$M$、$N$两点，若$|M F_{2}|=|F_{1} F_{2}|$，且$2|M F_{1}|=|N F_{1}|$，则双曲线$C$的离心率是?

**Process**:  
取F_{1}M的中点P,连接PF_{2},NF_{2},利用双曲线的定义,以及题中条件,得到|NP|^{2}-|MP|^{2}=|NF_{2}|^{2}-|MF_{2}|^{2},化简整理,即可求出结果取F_{1}M的中点P,连接PF_{2},NF_{2}.因为|MF_{2}|=|F_{1}F_{2}|=2c,所以PF_{2}\botMN根据双曲线的定义可得:|MF_{1}|=|MF_{2}|-2a=2c-2a则|MP|=|F_{1}P|=c-a,又|NF_{1}|=2|MF_{1}|,则|NF_{1}|=4(c-a),因此|NF_{2}|=4c-2a在Rt\triangleNPF_{2}中,|NP|^{2}+|PF_{2}|^{2}=|NF_{2}|^{2}在Rt\triangleMPF_{2}中,|MP|^{2}+|PF_{2}|^{2}=|MF_{2}|^{2}所以|NP|^{2}-|MP|^{2}=|NF|^{2}-|MF_{1}^{2}即(|NF_{1}|+|F_{1}P|)^{2}-|MP|^{2}=|NF_{2}|^{2}-|MF_{2}|^{2}即[5(c-a)]^{2}-(c-a)^{2}=(4c-2a)^{2}-(2c)^{2}整理得(c-a)(3c-5a)=0,解得e=\frac{c}{a}=1或\frac{5}{2}又e>1,所以e=\frac{5}{3}

**Theorem Sequence**:  
Hyperbola_Equation_Standard_X, Hyperbola_Definition, Triangle_Midline_Theorem, Cosine_Law, Eccentricity_Formula

---

## Problem Index: 3780
**ID**: 3781
**Text**:  
椭圆$E$: $\frac{x^{2}}{4}+\frac{y^{2}}{3}=1$的右顶点为$B$，过$E$的右焦点作斜率为$1$的直线$L$与$E$交于$M$、$N$两点，则$\triangle M B N$的面积为?

**Process**:  
由椭圆E的右焦点及直线L的斜率为1,可设直线L的方程为y=x-1,代入椭圆方程,由韦达定理及弦长公式求得|MN|.根据右顶点(2,0),利用点到直线距离公式求得B到直线L的距离d,结合AMBN的面积S=\frac{1}{2}\cdot|MN|\cdotd即可得解.羊解】由题意可知椭圆E:\frac{x^{2}}{4}+\frac{y^{2}}{3}=1右焦点(1,0),右顶点(2,0)直线L的斜率为1,且过右焦点(1,0)设直线L的方程为y=x-1,M(x_{1},y_{1}),N(x_{2},y_{2})由\begin{cases}y=x-1\\\frac{x^{2}}{4}+\frac{y^{2}}{3}=1\end{cases},整理得:7x^{2}-8x-8=0由韦达定理可知x_{1}+x_{2}=\frac{8}{7},x_{1}x_{2}=-\frac{8}{7}\_由弦长公式可得|MN|=\sqrt{1+k^{2}}\cdot\sqrt{(x_{1}+x_{2})^{2}-4x_{1}x_{2}}=\sqrt{2}\cdot\sqrt{(\frac{8}{7})^{2}-4\times(-\frac{8}{7})}=\frac{24}{7}由点到直线的距离公式可知,B到直线L的距离d=\frac{|0-2+1|}{\sqrt{1+(-1)^{2}}}=\frac{\sqrt{2}}{2}AMBN的面积_{S}=\frac{1}{2}\cdot|MN|\cdotd=\frac{1}{2}\times\frac{24}{7}\times\frac{\sqrt{2}}{2}=\frac{\sqrt{1}}{7}\thereforeAMBN的面积为\frac{6\sqrt{2}}{7}

**Theorem Sequence**:  
Ellipse_Equation_Standard_X, Line_Point_Slope_Form, Vieta_Theorem_Sum, Vieta_Theorem_Product, Chord_Length_Formula_With_K, Triangle_Area_Coordinate

---

## Problem Index: 3786
**ID**: 3787
**Text**:  
设抛物线$y^{2}=x$的焦点为$F$，点$M$在抛物线上，线段$M F$的延长线与直线$x=-\frac{1}{4}$交于点$N$，则$\frac{1}{|M F|}+\frac{1}{|N F|}$的值为?

**Process**:  
由题意可得F为(\frac{1}{4},0)准线方程为x=-\frac{1}{4},过点M作MH垂直于准线,垂足为H,准线与x轴的交点为K,可得ANFK\sim\triangleNMH,进而得到\frac{|FK|}{|MH|}=\frac{|NF|}{|NF|+|MF|},化简即为所求由题可得,F为(\frac{1}{4},0)准线方程为x=-\frac{1}{4},过点M作MH垂直于准线,垂足为H,准线与x轴的交点为K,则由抛物线的定义得,|MF|=|MH|.|FK|=\frac{1}{2},且易得ANFK-ANMH\frac{|NF|}{|NF|+|MF|},即\therefore\frac{1}{2|MH|}=\frac{|NF|}{|NF|+|MF|}\therefore2|MF|\cdot|NF|=|NF|+|MF|,两边同时除以|MF|\cdot|NF|\therefore\frac{1}{|MF|}+\frac{1}{|NF|}=2

**Theorem Sequence**:  
Parabola_Equation_Standard_Right, Parabola_Definition, Parabola_Directrix, Pythagorean_Theorem, Basic_Inequality

---

## Problem Index: 3797
**ID**: 3798
**Text**:  
已知过点$(2, \sqrt{3})$的双曲线$E$与双曲线$C$: $\frac{x^{2}}{4}-y^{2}=1$的渐近线相同，则双曲线$E$的方程是?

**Process**:  
因为双曲线E与双曲线C:\frac{x^{2}}{4}-y^{2}=1的渐近线相同,所以可设双曲线E的方程是\frac{x^{2}}{4}-y^{2}=\lambda,将点(2,\sqrt{3})的坐标代入\frac{x^{2}}{4}-y2=2得:1-3=\lambda,\therefore\lambda=-2,\therefore所求的双曲线的标准方程\frac{x^{2}}{4}-y^{2}=-2,即\frac{y^{2}}{2}-\frac{x^{2}}{8}=1,

**Theorem Sequence**:  
Hyperbola_Equation_Standard_X, Hyperbola_Asymptote, Hyperbola_Common_Asymptote_System

---

## Problem Index: 3815
**ID**: 3816
**Text**:  
已知双曲线$\frac{y^{2}}{a^{2}}-\frac{x^{2}}{b^{2}}=1$的一条渐近线方程为$y=\frac{4}{3} x$，则双曲线的离心率为?

**Process**:  
由题\frac{y^{2}}{a^{2}}-\frac{x^{2}}{b^{2}}=1,渐近线方程为;y=\frac{4}{3}x,\frac{a}{b}=\frac{4}{3}.又c^{2}=a^{2}+b^{2},b=\frac{3}{4}a,(\frac{c}{a})^{2}=\frac{25}{16},e=\frac{5}{4}.

**Theorem Sequence**:  
Hyperbola_Equation_Standard_Y, Hyperbola_Asymptote, Eccentricity_Formula

---

## Problem Index: 3824
**ID**: 3825
**Text**:  
抛物线$x^{2}=y$的准线方程为?

**Process**:  
因为抛物线方程为x^{2}=y,所以p=\frac{1}{2}\Rightarrow\frac{p}{2}=\frac{1}{4},又因为抛物线焦点在y轴上所以抛物线x^{2}=y的准线方程为y=-\frac{1}{4}

**Theorem Sequence**:  
Parabola_Equation_Standard_Up, Parabola_Directrix

---

## Problem Index: 3833
**ID**: 3834
**Text**:  
过抛物线$y^{2}=4 x$的焦点作斜率为$1$的直线$l$交抛物线于$A$、$B$两点，则以线段$A B$为直径的圆的方程为?

**Process**:  
抛物线y^{2}=4x的焦点为F(1,0)由题意可知直线l的方程为y=x-1,设点A(x_{1},y_{1})、B(x_{2},y_{2})联立\begin{cases}y2=4x\\y=x-1\end{cases},消去y可得x^{2}-6x+1=0,4=32>0,由韦达定理得x_{1}+x_{2}=6,则\frac{x_{1}+x_{2}}{2}=3,\frac{y_{1}+y_{2}}{2}=\frac{x_{1}+x_{2}}{2}-1=2线段AB的中点为M(3,2),由抛物线的焦点弦长公式可得|AB|=x_{1}+x_{2}+2=8,因此,以线段AB为直径的圆的方程为(x-3)^{2}+(y-2)^{2}=16

**Theorem Sequence**:  
Parabola_Equation_Standard_Right, Line_Point_Slope_Form, Vieta_Theorem_Sum, Circle_Standard_Equation, Parabola_Focal_Chord_Length

---

## Problem Index: 3856
**ID**: 3857
**Text**:  
已知双曲线$\frac{x^{2}}{a^{2}}-\frac{y^{2}}{b^{2}}=1(a>0, b>0)$的离心率等于$2$，其两条渐近线与抛物线$y^{2}=2 p x(p>0)$的准线分别交于$A$、$B$两点，$O$为坐标原点，$S_{\triangle A O B} =\frac{\sqrt{3}}{4}$，则$p$=?

**Process**:  
由题意可得:e=\frac{c}{a}=2,则:\frac{b}{a}=\sqrt{\frac{c^{2}-a^{2}}{a^{2}}}=\sqrt{3},双曲线的渐近线为:y=\pm\sqrt{3}x.令x=-\frac{p}{2}可得:y=\pm\frac{\sqrt{3}}{2}p'据此可得_{S_{\triangleOAB}}=\frac{1}{2}\times\sqrt{3}p\times\frac{p}{2}=\frac{\sqrt{3}}{4}p^{2}=\frac{\sqrt{3}}{4},解得:p=1.

**Theorem Sequence**:  
Eccentricity_Formula, Hyperbola_Asymptote, Hyperbola_Equation_Standard_X, Parabola_Equation_Standard_Right, Parabola_Directrix, Triangle_Area_Coordinate

---

## Problem Index: 3869
**ID**: 3870
**Text**:  
直线$l$与抛物线$y^{2}=4 x$相交于不同两点$A$、$B$，若$M(x_{0}, 4)$是$A B$中点，则直线$l$的斜率$k$=?

**Process**:  
设A(x_{1},y_{1}),B(x_{2},y_{2})\because直线l与抛物线y^{2}=4x相交于不同两点A,B\thereforey_{1}2=4x_{1},y_{2}^{2}=4x_{2},则两式相减得(y_{1}+y_{2})(y_{1}-y_{2})=4(x_{1}-x_{2})\becauseM(x_{0},4)是AB中点\therefore8(y_{1}-y_{2})=4(x_{1}-x_{2})

**Theorem Sequence**:  
Parabola_Equation_Standard_Right, Point_Difference_Method, Slope_Formula, Line_Point_Slope_Form

---

## Problem Index: 3888
**ID**: 3889
**Text**:  
若抛物线$C$: $y^{2}=2 p x$的焦点在直线$x+y-3=0$上，则实数$p$=?抛物线$C$的准线方程为?

**Process**:  
抛物线C:y^{2}=2px的焦点是(\frac{p}{2},0),由题意的\frac{p}{2}+0-3=0,p=6,准线方程为x=-3.

**Theorem Sequence**:  
Ellipse_Equation_Standard_X, Parabola_Equation_Standard_Right, Eccentricity_Formula, Ellipse_Parameter_Relation

---

## Problem Index: 3890
**ID**: 3891
**Text**:  
已知点$Q(\sqrt{2}, 0)$及抛物线$x^{2}=2 y$上一动点$P(x, y)$，则$y+|P Q|$的最小值是?

**Process**:  
抛物线x^{2}=2y的焦点为F(0,\frac{1}{2}),根据抛物线的定义可知y+\frac{1}{2}=|PF|,所以y+|PQ|=|PF|+|PQ|-\frac{1}{2}.故当F,P,Q三点共线时,|PF|+|PQ|-\frac{1}{2}有最小值|FQ|-\frac{1}{2}=\sqrt{(\sqrt{2})^{2}+(\frac{1}{2})^{2}}-\frac{1}{2}=\frac{3}{2}-\frac{1}{2}=1

**Theorem Sequence**:  
Parabola_Equation_Standard_Up, Parabola_Definition, Parabola_Directrix, Two_Points_Distance

---

## Problem Index: 3907
**ID**: 3908
**Text**:  
椭圆$\frac{x^{2}}{16}+\frac{y^{2}}{9}=1$的两焦点分别为$F_{1}$、$F_{2}$，过$F_{1}$作直线交椭圆于$A$、$B$两点，则$\triangle A B F_{2}$周长为?

**Process**:  
因为椭圆\frac{x2}{16}+\frac{y2}{9}=1,\thereforea=4,由椭圆的定义可得AABF_{2}的周长是(|AF_{1}|+|AF_{2}|)+(|BF_{1}|+|BF_{2}|)=2a+2a=4a=16,故选A.

**Theorem Sequence**:  
Ellipse_Equation_Standard_X, Ellipse_Definition

---

## Problem Index: 3913
**ID**: 3914
**Text**:  
已知$F$为抛物线$C$: $y^{2}=4 x$的焦点，过$F$作两条互相垂直的直线$l_{1}$, $l_{2}$，直线$l_{1}$与$C$交于$A$、$B$两点，直线$l_{2}$与$C$交于$D$、$E$两点，则$|A B|+|D E|$的最小值为?

**Process**:  
由题意可知抛物线C:y2=4x的焦点F:(1,0),准线为x=-1设直线l_{1}的解析式为y=k(x-1)\because直线l_{1},l_{2}互相垂直\thereforel_{2}的斜率为-\frac{1}{k}与抛物线的方程联立\begin{cases}y=k(x-1)\\,\end{cases},消去y得k^{2}x^{2}-(2k^{2}+4)x+k^{2}=0设点A(x_{1},y_{1},B(x_{2},y_{2}),C(x_{3},y_{3},D(x_{4},y_{4})由跟与系数的关系得x_{1}+x_{2}=\frac{2k^{2}+4}{k^{2}},同理x_{3}+x_{4}=\frac{2\frac{1}{k^{2}}+4}{\frac{1}{k^{2}}\because根据抛物线的性质,抛物线上的点到焦点的距离等于到准线的距离\therefore|AB|=x_{1}+1+x_{2}+1,同理|DE|=x_{3}+1+x_{4}+1\therefore|AB|+|DE|=\frac{2k^{2}+4}{k^{2}}+\frac{2\frac{1}{k^{2}}+4}{\frac{1}{l^{2}}}+4=8+\frac{4}{k^{2}}+4k^{2}\geqslant8+2\sqrt{4\times4}=16,当且仅当k^{2}=1时取等号.

**Theorem Sequence**:  
Parabola_Equation_Standard_Right, Substitution_x_equals_my_plus_n, Vieta_Theorem_Sum, Discriminant_Delta

---

## Problem Index: 3917
**ID**: 3918
**Text**:  
已知点$F$为抛物线$x^{2}=8 y$的焦点，$M(0,-2)$，点$N$为抛物线上一动点，当$\frac{|N F|}{|N M|}$最小时，点$N$恰好在以$M$、$F$为焦点的双曲线上，则该双曲线的离心率为?

**Process**:  
由题意可得,F(0,2),M(0,-2),抛物线的准线为y=-2.设点_{N}(x_{0},\frac{x_{0}^{2}}{8}),根据对称性,不妨设x_{0}>0,由抛物线的定义可知|NF|=\frac{x_{0}^{2}}{8}+2^{,}又|NM|=\sqrt{x_{0}^{2}+(\frac{x^{2}}{8}+2}设以M,F为焦点的双曲线方程为\frac{y^{2}}{a^{2}}-\frac{x^{2}}{b^{2}}=1.则2a=||NF|-|NM||=|4-4\sqrt{2}|=4(\sqrt{2}-1)即a=2(\sqrt{2}-1).又2c=|MF|=4,c=2,所以离心率e=\frac{c}{a}=\frac{2}{2(\sqrt{2}-1)}=\sqrt{2}+1又2c=|MF|=4,c=

**Theorem Sequence**:  
Parabola_Equation_Standard_Up, Parabola_Directrix, Parabola_Definition, Circle_Standard_Equation, Hyperbola_Definition, Eccentricity_Formula

---

## Problem Index: 3920
**ID**: 3921
**Text**:  
已知椭圆$C$: $\frac{x^{2}}{m}+y^{2}=1(m>1)$，若存在过点$A(1,2)$且相互垂直的直线$l_{1}$ ,$l_{2}$使得$l_{1}$ , $l_{2}$与椭圆$C$均无公共点，则该椭圆离心率的取值范围是?

**Process**:  
椭圆C:\frac{x^{2}}{m}+y^{2}=1(m>1)'\textcircled{1}当直线l_{1},l_{2}中-条斜率不存在和另一条斜率为0,两直线与椭圆相交\textcircled{2}当直线l_{1},l_{2}的斜率都存在时,可设l_{1}:y-2=k(x-1),即y=kx+2-k联立椭圆方程可得(mk^{2}+1)x^{2}+2km(2-k)x+m(2-k)^{2}-m=0,由直线l_{1}和椭圆C无交点,可得A=4k^{2}m^{2}(2-k)^{2}-4(mk^{2}+1)[m(2-k)^{2}-m]<0化为(m-1)k^{2}+4k-3<0,解得\frac{-2-\sqrt{3m+1}}{m-1}<k<\frac{-2+\sqrt{3m+1}}{m-1},由两直线垂直的条件,可将k换为-\frac{1}{k}即有\frac{m-1}{k^{2}}-\frac{4}{k}-3<0,化为3k^{2}+4k-m+1>0,-2+\sqrt{3m+1},m>1,化为8-2m<(4-m)\sqrt{3m+1},1时,\sqrt{3m+1}>2,则4-m>0,得m<4,此时1<m<4.3m+1,解得1<m<4,则\frac{1}{4}<\frac{1}{m}<1.所以,该椭圆的离心率为e=\frac{c}{a}=\sqrt{1-\frac{b^{2}}{a^{2}}}=\sqrt{1-\frac{1}{m}}\in(0,\frac{\sqrt{3}}{2})因此,该椭圆离心率的取值范围是(0,\frac{\sqrt{3}}{2})

**Theorem Sequence**:  
Ellipse_Equation_Standard_X, Point_Difference_Method_Hyperbola, Discriminant_Delta, Line_Point_Slope_Form, Ellipse_Eccentricity_Range

---

## Problem Index: 3925
**ID**: 3926
**Text**:  
已知两定点$P_{1}(-1 , 0)$和$P_{2}(3 , 0)$，则到点$P_{1}$和$P_{2}$的距离的平方和等于$16$的点的轨迹方程为?

**Process**:  
设点P(x,y)到点口_{1}和口_{2}的距离的平方等于16,则PP_{1}^{2}+PP_{2}^{2}=(x+1)^{2}+y^{2}+(x-3)^{2}+y^{2}=16'整理得:x^{2}+y^{2}-2x-3=0.

**Theorem Sequence**:  
Circle_Standard_Equation, Two_Points_Distance

---

## Problem Index: 3927
**ID**: 3928
**Text**:  
设抛物线$y^{2}=2 p x  (p>0)$的焦点为$F$，点$A(0 , 2)$，线段$F A$与抛物线交于点$B$，且$\overrightarrow{F B}=2 \overrightarrow{B A}$，则$ |B F |$=?

**Process**:  
设B(x,y),根据\overrightarrow{FB}=2\overrightarrow{BA}可得出用p表示的B点坐标,再代入抛物线方程可得出p值,然后求得B、F两点坐标,利用两点之间的距离公式可得答案.由题得F(\frac{p}{2},0)(p>0),设B(x,y),则\overrightarrow{FB}=(x-\frac{p}{2},y)2\overrightarrow{BA}=2(-x,2-y)=(-2x,4-2y),由\overrightarrow{FB}=2\overrightarrow{BA}得\begin{cases}x-\frac{p}{2}=-2x\\y=4-2y\end{cases}解得\begin{cases}x=\frac{p}{6}\\y=\frac{4}{3}\end{cases}代入椭圆方程得(\frac{4}{3})^{2}=2p\times\frac{p}{6},解得p=\frac{4\sqrt{3}}{3}所以_{B(}^{2}\frac{3}{9},\frac{4}{3})'F(\frac{2\sqrt{3}}{3},0)'

**Theorem Sequence**:  
Parabola_Equation_Standard_Right, Parabola_Definition, Parabola_Directrix, Vector_Collinear_Condition, Two_Points_Distance

---

## Problem Index: 3931
**ID**: 3932
**Text**:  
已知双曲线$C$:$x^{2}-y^{2}=\lambda(\lambda>0)$的一个焦点为$F$、$O$为坐标原点，在双曲线$C$的渐近线上取一点$P$，使得$|P F|=|P O|$，且$\Delta P O F$的面积为$1$，则$\lambda$=?

**Process**:  
不妨设F为双曲线的右焦点,c为双曲线的半焦距,由题意知P的横坐标为\frac{c}{2},双曲线的渐近线方程为y=\pmx,设点P在渐近线y=x上,则P的纵坐标为\frac{c}{2}所以\trianglePOF的面积为\frac{c^{2}}{4}=1,得c^{2}=4,由题意知c^{2}=2\lambda,所以2\lambda=4,解得\lambda=2.

**Theorem Sequence**:  
Hyperbola_Equation_Standard_X, Hyperbola_Asymptote, Triangle_Area_Formula

---

## Problem Index: 3960
**ID**: 3961
**Text**:  
已知$F_{1}$、$F_{2}$分别是椭圆的左、右焦点，现以$F_{2}$为圆心作一个圆恰好经过椭圆中心并且交椭圆于点$M$、$N$，若过$F_{1}$的直线$M  F_{1}$是圆$F_{2}$的切线，则椭圆的离心率为?

**Process**:  
\becauseF_{1}F_{2}分别是椭圆的左,右焦点现以F_{2}为圆心作一个圆恰好经过椭圆中心并且交椭圆于点M,N过F_{1}的直线MF_{1}是圆F_{2}的切线,\therefore|MF_{2}|=c_{1}|F_{1}F_{2}|=2c,\angleF_{1}MF_{2}=90^{\circ}\therefore|MF_{1}|=\sqrt{4c^{2-c^{2}}=\sqrt{3}c,\therefore2a=\sqrt{3}c+c=(\sqrt{3}+1)c_{2}=\sqrt{3}-.即答案为\sqrt{3}-1

**Theorem Sequence**:  
Ellipse_Definition, Circle_Standard_Equation, Ellipse_Focal_Triangle_Perimeter, Eccentricity_Formula

---

## Problem Index: 3983
**ID**: 3984
**Text**:  
已知抛物线$C$: $y=\frac{1}{8} x^2$的焦点是$F$，点$M$是其准线$l$上一点，线段$M F$交抛物线$C$于点$N$.当$\overrightarrow{M N}=\frac{2}{3} \overrightarrow{M F}$时，$\triangle N O F$的面积是?

**Process**:  
由抛物线的方程可得焦点F坐标及准线方程,因为\overrightarrow{MN}=\frac{2}{3}\overrightarrow{MF},可得N在M,F之间,设NN垂直于准线交于N',由抛物线的性质可得NN'=NF,可得_{\tan}\angleFMN^{'}=\frac{\sqrt{3}}{3},求出直线MF的方程,代入抛物线的方程求出N的横坐标,进而求出ANOF的面积.羊解】由题意抛物线的标准方程为:x^{2}=8y,所以焦点F(0,2),准线方程为y=-2,设NN垂直于准线交于N',如图,由抛物线的性质可得NN'=NF,因为\overrightarrow{MN}=\frac{2}{3}\overrightarrow{MF},可得N在M,F之间,所以MN=2NF=2NN',所以\sin\angleFMN'=\frac{NN'}{MN}=\frac{1}{2},所以_{\tan\angleFMN}=\frac{\sqrt{3}}{3},即直线MF的斜率为\frac{\sqrt{3}}{3},所以直线MF的方程为y=\frac{\sqrt{3}}{3}x+2'将直线MF的方程代入抛物线的方程可得:x^{2}-\frac{8\sqrt{3}}{3}x-16=0'解得x=-\frac{4}{\sqrt{3}}或x=4\sqrt{3}(舍),所以S_{ANOF}=\frac{1}{2}|OF|\cdot|x|=\frac{1}{2}\times2\times\frac{4\sqrt{3}}{3}=\frac{4\sqrt{3}}{3}

**Theorem Sequence**:  
Parabola_Equation_Standard_Up, Parabola_Definition, Parabola_Directrix, Vector_Collinear_Condition, Triangle_Area_Formula

---

## Problem Index: 3987
**ID**: 3988
**Text**:  
已知双曲线$C$: $\frac{x^{2}}{a^{2}}-\frac{y^{2}}{b^{2}}=1(a>0, b>0)$的左、右焦点分别为$F_{1}$ ,$ F_{2}$ , $P(3, \frac{\sqrt{10}}{2})$为$C$的右支上一点，且$|P F_{1}|-|P F_{2}|=4$，则$C$的离心率为?

**Process**:  
由题知2a=4,故a=2,又点_{P}(3,\frac{\sqrt{10}}{2})在双曲线上,所以\frac{9}{4}-\frac{10}{b^{2}}=1'解得b^{2}=2,所以e=\sqrt{1+\frac{b^{2}}{a^{2}}}=\sqrt{1+\frac{2}{4}}=\frac{\sqrt{6}}{2}.

**Theorem Sequence**:  
Ellipse_Equation_Standard_X, Ellipse_Parameter_Relation, Eccentricity_Formula

---

## Problem Index: 3995
**ID**: 3996
**Text**:  
若抛物线$C$: $y^{2}=2 p x(p>0)$上的一点$A(\frac{p}{4}, y_{1})$到它的焦点的距离为$6$，则$p$=?

**Process**:  
根据抛物线的定义知\frac{p}{4}+\frac{p}{2}=6,所以p=8.

**Theorem Sequence**:  
Parabola_Equation_Standard_Up, Parabola_Directrix

---

## Problem Index: 4058
**ID**: 4059
**Text**:  
若椭圆$a x^{2}+b y^{2}=1$与直线$x+y=1$交于$A$、$B$两点，点$M$为$A B$的中点，直线$O M$($O$为坐标原点)的斜率为$\frac{\sqrt{2}}{2}$ , $\frac{b}{a}$的值为?

**Process**:  
设A(x_{1},y_{1}),B(x_{2},y_{2}),则x_{M}=\frac{x_{1}+x_{2}}{2},y_{M}=\frac{y_{1}+y_{2}}{2},\frac{y_{M}}{x_{M}}=\frac{\sqrt{2}}{2},\frac{y_{2}-y_{1}}{x_{2}-x_{1}}=-1.由\begin{cases}ax_{1}^{2}+by_{1}^{2}=1\\ax_{2}^{2}+by_{2}=1\end{cases}作差可得,a(x_{2}^{2}-x_{1}^{2})+b(y_{2}^{2}-y_{1}^{2})=0,即a+b\frac{y_{2}+y_{1}}{x_{2}+x_{1}}\cdot\frac{y_{2}-y_{1}}{x_{2}-x_{1}}=0所以,a+b\times\frac{\sqrt{2}}{2}\times(-1)=0^{,}解得\frac{b}{a}=\sqrt{2}.

**Theorem Sequence**:  
Ellipse_Equation_Standard_X, Point_Difference_Method, Vieta_Theorem_Sum, Vieta_Theorem_Product, Midpoint_Formula

---

## Problem Index: 4119
**ID**: 4120
**Text**:  
如果曲线$2|x|-y-4=0$与曲线$x^{2}+\lambda y^{2}=4(\lambda<0)$恰好有两个不同的公共点，则实数$\lambda$的取值范围是?

**Process**:  
因为曲线2|x|-y-4=0与曲线x^{2}+\lambday^{2}=4(\lambda<0)都过点(\pm2,0),所以双曲线渐近线y=\sqrt{-\frac{1}{2}}x斜率不小于直线y=2x-4斜率,即\sqrt{-\frac{1}{2}}\geqslant2\Rightarrow-\frac{1}{4}\leqslant\lambda<0

**Theorem Sequence**:  
Parabola_Equation_Standard_Right, Hyperbola_Equation_Standard_X, Hyperbola_Asymptote, Discriminant_Delta

---

## Problem Index: 4129
**ID**: 4130
**Text**:  
已知$F_{1}$、$F_{2}$是椭圆$\frac{x^{2}}{100}+\frac{y^{2}}{64}=1$的两个焦点，$P$为椭圆上一点，则$|P F_{1}| \cdot|P F_{2}|$的最大值为?

**Process**:  
根据椭圆的定义,结合基本不等式,求出|PF_{1}|\cdot|PF_{2}|的最大值.\becauseF_{1},F_{2}是椭圆\frac{x2}{100}+\frac{y^{2}}{64}=1的两个焦点,设|PF_{1}|=m,|PF_{2}|=n,根据椭圆的定义得m+n=20,\becausem+n=20\geqslant2\sqrt{mn},\thereforemn\leqslant(\frac{m+n}{2})^{2}=100,当且仅当m=n=10时,等号成立;\therefore|PF|.|PF_{2}|的最大值为100.

**Theorem Sequence**:  
Ellipse_Equation_Standard_X, Ellipse_Definition, Basic_Inequality

---

## Problem Index: 4138
**ID**: 4139
**Text**:  
已知点$A$、$B$是椭圆$G$: $\frac{x^{2}}{a^{2}}+\frac{y^{2}}{b^{2}}=1(a>b>0)$上的两点，且线段$A B$恰好为圆$x^{2}+y^{2}=R^{2}(R>0)$的一条直径，$M$为椭圆$G$上与$A$、$B$不重合的一点，且直线$M A$, $M B$的斜率之积为$-\frac{1}{4}$，则椭圆$G$的离心率为?

**Process**:  
设A(x_{1},y_{1}),M(x_{0},y_{0}),依题意,\begin{cases}\frac{x^{2}}{a^{2}}+\frac{y^{2}}{b^{2}}=1\\\frac{x_{0}^{2}}{a^{2}}+\frac{y_{0}}{\frac{0}{2}}=1\end{cases}两式相减得\frac{x^{2}-x_{0}^{2}}{a^{2}}=\frac{y_{\frac{1}{b^{2}}-y_{0}^{2}}因线段AB恰好为圆x^{2}+y^{2}=R^{2}(R>0于是得直线MA,MB的斜率之积为\frac{y_{1}-y_{0}}{x_{1}}-x_{0}\cdot\frac{x}{x_{1}}-x_{0}=\frac{y_{2}-y_{0}^{2}}{x_{1}^{2}-x_{0}^{2}}=-\frac{b^{2}}{a^{2}}=-\frac{1}{4},解得\frac{b^{2}}{a^{2}}=\frac{1}{4})的-条直径,则B(-x_{1},所以椭圆G的离心率为e=\frac{\sqrt{a2-b^{2}}}{a^{2}}=\sqrt{1-\frac{b^{2}}{a^{2}}}=\frac{\sqrt{3}}{2}.

**Theorem Sequence**:  
Ellipse_Equation_Standard_X, Point_Difference_Method, Vieta_Theorem_Sum, Circle_Standard_Equation, Ellipse_Parameter_Relation, Eccentricity_Formula

---

## Problem Index: 4142
**ID**: 4143
**Text**:  
直线$l$与抛物线$y^{2}=4 x$交于两点$A(x_{1}, y_{1})$, $B(x_{2}, y_{2})$ , $O$为坐标原点，若$\overrightarrow{O A} \cdot \overrightarrow{O B}=-4$，则$x_{1} x_{2}$=?

**Process**:  
因为直线l与抛物线y^{2}=4x交于两点A(x_{1},y_{1}),B(x_{2},y_{2})所以由\overrightarrow{OA}\cdot\overrightarrow{OB}=-4\Rightarrowx_{1}x_{2}+y_{1}y_{2}=-4,因为A(x_{1},y_{1}),B(x_{2},y_{2})在抛物线y^{2}=4x上所以y_{1}^{2}y_{2}^{2}=16x_{1}x_{2},即x_{1}x_{2}=\frac{y_{1}^{2}y_{2}}{16}因此有\frac{y_{1}y_{2}2}{16}+y_{1}y_{2}=-4,解得:y_{1}y_{2}=-8,所以x_{1}x_{2}

**Theorem Sequence**:  
Parabola_Equation_Standard_Right, Vieta_Theorem_Sum, Vieta_Theorem_Product

---

## Problem Index: 4144
**ID**: 4145
**Text**:  
中心在原点，焦点在$y$轴上，若长轴长$10$，焦距为$8$，则椭圆的标准方程为?

**Process**:  
中心在原点,焦点在y轴上,设椭圆的标准方程为\frac{y^{2}}{a^{2}}+\frac{x^{2}}{b^{2}}=1\because长轴长10,焦距为8,\therefore2a=10,2c=8,a=5,c=4,\becausea^{2}=b^{2}+c^{2},\thereforeb^{2}=25-16=9\therefore椭圆的标准方程为\frac{y^{2}}{25}+\frac{x^{2}}{9}=1

**Theorem Sequence**:  
Ellipse_Equation_Standard_X, Ellipse_Parameter_Relation

---

## Problem Index: 4149
**ID**: 4150
**Text**:  
已知椭圆$C$: $\frac{x^{2}}{a^{2}}+\frac{y^{2}}{b^{2}}=1(a>b>0)$的右焦点为$F$，左、右顶点为$A$ , $B$ ,$|F A|=3$ ,$|F B|=1$. 则直线$y=x+\frac{1}{2}$被椭圆$C$截得的弦长为?

**Process**:  
设椭圆的半焦距为c,由|FA|=3,|FB|=1,可得a+c=3,a-c=1,解得a=2,c=1,则b=\sqrt{a^{2}-c^{2}}=\sqrt{4-1}=\sqrt{3}即有椭圆的方程为\frac{x^{2}}{4}+\frac{y^{2}}{3}=1联立直线y=x+\frac{1}{2}和椭圆3x^{2}+4y^{2}=12,可得7x^{2}+4x-11=0,设被椭圆C截得的弦的端点的横坐标分别为x_{1},x_{2},则x_{1}+x_{2}=-\frac{4}{7},x_{1}x_{2}=-\frac{11}{7},可得弦长为\sqrt{1+k^{2}}\cdot\sqrt{(x_{1}+x_{2})^{2}-4x_{1}x_{2}}=\sqrt{1+1}\cdot\sqrt{(-\frac{4}{7})^{2}-4\times(-\frac{11}{7})}=\frac{18\sqrt{2}}{7}

**Theorem Sequence**:  
Ellipse_Equation_Standard_X, Ellipse_Definition, Point_Difference_Method_Hyperbola, Line_Point_Slope_Form, Chord_Length_Formula_With_K

---

## Problem Index: 4169
**ID**: 4170
**Text**:  
如果过两点$A(a, 0)$和$B(0, a)$的直线与抛物线$y=x^{2}-2 x-3$没有交点, 那么实数$a$的取值范围是?

**Process**:  
联立直线AB方程与抛物线方程,消去y,得关于x的二次方程x^{2}-x-a-3=0没有实根,得到\triangle=1+4(a+3)<0\Rightarrowa<-\frac{13}{4}

**Theorem Sequence**:  
Parabola_Equation_Standard_Right, Point_Difference_Method_Hyperbola, Discriminant_Delta, Quadratic_Function_Maximum

---

## Problem Index: 4187
**ID**: 4188
**Text**:  
若$F_{1}$ ,   $F_{2}$是双曲线$\frac{x^{2}}{9}-\frac{y^{2}}{16}=1$的两个焦点，$P$是双曲线上的一点，且$|P F_{1}| \cdot|P F_{2}|=64$，则$\angle F_{1} P F_{2}$=?

**Process**:  
由双曲线定义知|PF_{1}|-|PF_{2}|=\pm6,在\trianglePF_{1}F_{2}中,由余弦定理得:\cos\angleF_{1}PF_{2}=\frac{|PF_{1}^{2}+|PF_{2}|^{2}-100}{2|PF_{1}||PF_{2}|}=\frac{|PF_{1}|-|PF_{2}p^{2}+2|PF_{1}+|PF_{2}|-100}{2|PF_{1}|}=\frac{36+128-100}{128}=\frac{1}{2}\angleF_{1}PF_{2}=\frac{\pi}{3},所以答案应填:\frac{\pi}{3}

**Theorem Sequence**:  
Ellipse_Definition, Ellipse_Focal_Triangle_Perimeter, Triangle_Area_With_Sin

---

## Problem Index: 4203
**ID**: 4204
**Text**:  
已知双曲线$C$: $\frac{x^{2}}{a^{2}}-\frac{y^{2}}{b^{2}}=1(a>0, b>0)$的左顶点为$A $,以$A$为圆心，$b$为半径作圆$G$，圆$G$与双曲线$C$的一条渐近线交于$M$、$N$ 两点.若$\angle M A N=120^{\circ}$，则$C$的离心率为?

**Process**:  
不妨取渐近线为bx-ay=0,依题意作出简图.由图可知,点A到渐近线bx-ay=0的距离为b\sin30^{\circ}=\frac{1}{2}b,所以\frac{1}{2}b=\frac{ab}{c},因此离心率e=\frac{c}{a}=2.

**Theorem Sequence**:  
Hyperbola_Equation_Standard_X, Hyperbola_Asymptote, Point_To_Line_Distance, Eccentricity_Formula

---

## Problem Index: 4204
**ID**: 4205
**Text**:  
若双曲线$C$的方程为$\frac{x^{2}}{k^{2}-1}-\frac{y^{2}}{4-k^{2}}=1$，则$k$的取值范围是?

**Process**:  
由题意得:(k^{2}-1)(4-k^{2})>0,则有\begin{cases}k^{2}-1>0\\4-k^{2}>0\end{cases}或\begin{cases}k^{2}-1<0\\4-k^{2}<0\end{cases},解得k\in(-2,-1)\cup(1,2)

**Theorem Sequence**:  
Ellipse_Equation_Standard_X, Ellipse_Equation_Standard_Y

---

## Problem Index: 4210
**ID**: 4211
**Text**:  
抛物线$y=\frac{1}{12} x^{2}$的焦点坐标为?

**Process**:  
变换得到x^{2}=12y,计算焦点得到答案抛物线y=\frac{1}{12}x^{2}的标准方程为x^{2}=12y,p=6,所以焦点坐标为(0,3)

**Theorem Sequence**:  
Parabola_Equation_Standard_Right, Parabola_Directrix

---

## Problem Index: 4226
**ID**: 4227
**Text**:  
已知双曲线$\frac{x^{2}}{a^{2}}-\frac{y^{2}}{2}=1$的离心率为$\sqrt{3}$，则该双曲线的渐近线方程为?

**Process**:  
利用双曲线的离心率求出a,然后求解双曲线的渐近线方程.双曲线\frac{x^{2}}{a^{2}}-\frac{y^{2}}{2}=1(a>0)的离心率为\sqrt{3},可得:\frac{\sqrt{a^{2}+2}}{a}=\sqrt{3},解得a=1,所以双曲线方程为:\frac{x^{2}}{1}-\frac{y^{2}}{2}=1,所以该双曲线的渐近线为y=\pm\sqrt{2}x

**Theorem Sequence**:  
Hyperbola_Equation_Standard_Y, Hyperbola_Asymptote

---

## Problem Index: 4238
**ID**: 4239
**Text**:  
若抛物线$y^{2}=2 p x(p>0)$的准线经过双曲线$x^{2}-y^{2}=1$的一个焦点，则$p$=?

**Process**:  
由题设可得双曲线的一个焦点是F(\sqrt{2},0),故\frac{p}{2}=\sqrt{2}\Rightarrowp=2\sqrt{2},故应填2\sqrt{2}

**Theorem Sequence**:  
Parabola_Equation_Standard_Up, Parabola_Definition, Parabola_Directrix, Hyperbola_Definition, Eccentricity_Formula

---

## Problem Index: 4257
**ID**: 4258
**Text**:  
已知双曲线$C$: $\frac{x^{2}}{a^{2}}-\frac{y^{2}}{b^{2}}=1$与椭圆$\frac{x^{2}}{9}+\frac{y^{2}}{4}=1$有相同的焦点,且双曲线$C$的渐近线方程为$y=\pm 2 x$，则双曲线$C$的方程为?

**Process**:  
椭圆\frac{x^{2}}{9}+\frac{y^{2}}{4}=1中\thereforea^{2}+b^{2}=5\thereforea=1,b=2,双曲线C的渐近线方程为y=\pm2x\therefore\frac{b}{a}=2\thereforea=1,b=2,双曲线方程为x^{2}-\frac{y^{2}}{4}=1

**Theorem Sequence**:  
Ellipse_Equation_Standard_X, Hyperbola_Equation_Standard_Y

---

## Problem Index: 4264
**ID**: 4265
**Text**:  
若点$M$是直线$l$:$ y=-2$上的动点，过点$M$作抛物线$C$: $y=\frac{1}{4} x^{2}$的两条切线，切点分别为$A$、$B$，则$\overrightarrow{O A} \cdot \overrightarrow{O B}$=?

**Process**:  
设A(x_{1},y_{1}),B(x_{2},y_{2}),则\overrightarrow{OA}\cdot\overrightarrow{OB}=x_{1}x_{2}+y_{1}y_{2}\becauseA,B在y=\frac{1}{4}x^{2}上,\therefore\overrightarrow{OA}\cdot\overrightarrow{OB}=x_{1}x_{2}+y_{1}y_{2}=x_{1}x_{2}+\frac{1}{16}(x_{1}x_{2})^{2},\becausey=\frac{1}{4}x^{2}的导数为y=\frac{1}{2}x,所以切线MA的斜率为\frac{1}{2}x_{1},切线MA的方程为y-y_{1}=\frac{1}{2}x_{1}(x-x_{1})即2y=x_{1}x-2y_{1},同理得切线MB的方程为2y=x_{2}x-2y_{2}\textcircled{2},设M(m,-2),代入\textcircled{1}\textcircled{2}得-4=x_{1}m-2y_{1}且-4=x_{2}m-2y_{2}\therefore直线AB的方程为mx-2y+4=0联立得\begin{cases}mx-2y\\y=\frac{1}{4}x^{2}\end{cases},+4=0x2-2mx-8=0\thereforex_{1}x_{2};=-8.\therefore\overrightarrow{OA}\cdot\overrightarrow{OB}=x_{1}x_{2}+\frac{1}{16}(x_{1}x_{2})^{2}=-4

**Theorem Sequence**:  
Parabola_Equation_Standard_Right, Vieta_Theorem_Sum, Vieta_Theorem_Product, Ellipse_Tangent_Line, Point_Difference_Method_Hyperbola, Vector_Collinear_Condition

---

## Problem Index: 4269
**ID**: 4270
**Text**:  
双曲线$\frac{x^{2}}{4}-y^{2}=1$的右焦点到其一条渐近线的距离是?

**Process**:  
求出右焦点坐标,渐近线方程,利用点到直线的距离公式即可求解.由\frac{x^{2}}{4}-y^{2}=1知:a^{2}=4,b^{2}=1,所以c^{2}=a^{2}+b^{2}=5,即c=\sqrt{5}右焦点(\sqrt{5},0),其中一条渐近线x-2y=0,所以右焦点(\sqrt{5},0)到渐近线x-2y=0距离为d=\frac{\sqrt{5}-0}{\sqrt{1+2^{2}}}=1

**Theorem Sequence**:  
Hyperbola_Equation_Standard_X, Hyperbola_Asymptote, Point_To_Line_Distance

---

## Problem Index: 4283
**ID**: 4284
**Text**:  
已知$F_{1}(-2,0)$ , $F_{2}(2,0)$，设$P$是椭圆$x^{2}+2 y^{2}=8$与双曲线$x^{2}-y^{2}=2$的交点之一，则$|P F_{1}| \cdot|P F_{2}|$=?

**Process**:  
椭圆和双曲线分别化为标准方程为\frac{x^{2}}{8}+\frac{y^{2}}{4}=1,\frac{x^{2}}{2}-\frac{y^{2}}{2}=1^{,}可知两曲线共焦点\begin{cases}设|PF_{1}|=r_{1}||PF_{2}|=r_{2},\\r_{1}+r_{2}=4\sqrt{2}\\|r_{1}-r_{2}|=2\sqrt{2}\end{cases}\begin{cases}r_{1}=3\sqrt{2}\\r_{2}=\sqrt{2}\end{cases}或\begin{cases}x=\sqrt{2}\\r_{2}=3\sqrt{2}\end{cases}\Rightarrowr_{1}xr_{2}=6

**Theorem Sequence**:  
Ellipse_Equation_Standard_X, Hyperbola_Definition, Ellipse_Definition

---

## Problem Index: 4288
**ID**: 4289
**Text**:  
已知$F_{1}$、$F_{2}$为椭圆$C$的两个焦点，$P$为$C$上一点，若$|P F_{1}|+|P F_{2}|=2|F_{1} F_{2}|$，则$C$的离心率为?

**Process**:  
P为椭圆C上一点,由椭圆的定义知,|PF_{1}|+|PF_{2}|=2a因为|PF_{1}|+|PF_{2}|=2|F_{1}F_{2}|=4c,所以2a=4c,所以e=\frac{c}{a}=\frac{1}{2}

**Theorem Sequence**:  
Ellipse_Equation_Standard_X, Ellipse_Definition, Eccentricity_Formula

---

## Problem Index: 4342
**ID**: 4343
**Text**:  
已知实数$x$ ,$y$满足:$x|x|+y|y|=1$，则$|x+y+\sqrt{2}|$的取值范围是?

**Process**:  
当x\geqslant0,y\geqslant0时,x^{2}+y^{2}=1,其图象是单位圆取第一象限的部分当x<0,y\geqslant0时,-x^{2}+y^{2}=1,其图象是双曲线-x^{2}+y^{2}=1取第二象限的部分当x\geqslant0,y<0时,x^{2}-y^{2}=1,其图象是双曲线x^{2}-y^{2}=1取第四象限的部分;当x<0,y<0时,-x^{2}-y^{2}=1,图象不存在所以方程x|x|+y|y|=1对应的图象如下:|x+y+\sqrt{2}|=\frac{|x+y+\sqrt{2}|}{\sqrt{2}}.\sqrt{2},表示的是点(x,y)到直线x+y+\sqrt{2}=0的距离的\sqrt{2}倍所以|x+y+\sqrt{2}|的最大值为单位圆上的点到直线x+y+\sqrt{2}=0的距离的最大值的\sqrt{2}倍,为(\frac{\sqrt{2}}{\sqrt{2}}+1)\sqrt{2}=2\sqrt{2}双曲线的一条渐近线方程为y=-x,直线y=-x与直线x+y+\sqrt{2}=0的距离为1所以|x+y+\sqrt{2}|>\sqrt{2}综上:|x+y+\sqrt{2}|的取值范围是(\sqrt{2},2\sqrt{2}]

**Theorem Sequence**:  
Hyperbola_Equation_Standard_X, Circle_Standard_Equation, Hyperbola_Asymptote, Two_Points_Distance, Quadratic_Function_Maximum

---

## Problem Index: 4347
**ID**: 4348
**Text**:  
顶点在原点，以$x$轴为对称轴且经过点$M(-2,3)$的抛物线的标准方程为?

**Process**:  
由题意可设抛物线的标准方程为y^{2}=-2px\therefore3^{2}=-2p\cdot(-2),解得p=\frac{9}{4}因此抛物线的标准方程为y^{2}=-\frac{9}{2}x与睛)本题主要考查了求抛物线的标准方程,属于基础题

**Theorem Sequence**:  
Parabola_Equation_Standard_Right, Parabola_Directrix

---

## Problem Index: 4364
**ID**: 4365
**Text**:  
若双曲线$\frac{x^{2}}{a^{2}}-y^{2}=1(a>0)$的离心率为$\frac{\sqrt{10}}{3}$，则该双曲线的渐近线方程为?

**Process**:  
双曲线\frac{x^{2}}{a^{2}}-y^{2}=1(a>0)的离心率为\frac{\sqrt{10}}{3},则\begin{cases}\frac{c}{a}=\frac{\sqrt{10}}{3}\\c^{2}-a^{2}=1\end{cases}所以a=3,b=1,则渐近线方程为v=\pm\frac{1}{3}x.故答客为:x+3v=0.

**Theorem Sequence**:  
Hyperbola_Equation_Standard_Y, Hyperbola_Asymptote

---

## Problem Index: 4369
**ID**: 4370
**Text**:  
已知$P$是抛物线$y^{2}=4 x$上一动点，定点$A(0,2 \sqrt{2})$，过点$P$作$P Q \perp y$轴于点$Q$, 则$|P A|+|P Q|$的最小值是?

**Process**:  
由抛物线y^{2}=4x可知,其焦点坐标为F(1,0),准线x=-1.设点P到其准线的距离为d,根据抛物线的定义可的d=|PF|则点P到y轴的距离为|PQ|=|PF|-1,且|FA|=\sqrt{1^{2}+(2\sqrt{2})^{2}}=3则|PA|+|PQ|=|PA|+|PF|-1\geqslant|FA|-1=2(当且仅当A,P,F三点共线时取等号)所以|PA|+|PQ|的最小值为2.有睛)本题主要考查抛物线的定义的应用,其中解答中由抛物线的定义转化为|PQ|=|PF|-1,再借助图形得到|PA|+|PQ|=|PA|+|PF|-1\geqslant|FA|-1是解答的关键,若重考查了转化思想,以及数形结合的应用,以及运算与求解能力,属于基础提

**Theorem Sequence**:  
Parabola_Equation_Standard_Right, Parabola_Definition, Parabola_Directrix, Two_Points_Distance

---

## Problem Index: 4370
**ID**: 4371
**Text**:  
已知点$P$为椭圆$\frac{x^{2}}{3}+y^{2}=1$上任一点，点$Q$是抛物线$x^{2}=2 \sqrt{6} y$的准线上的任意一点，以$P Q$为直径的圆过原点$O$，试判断$\frac{1}{|O P|^{2}}+\frac{1}{|O Q|^{2}}$=?

**Process**:  
抛物线C的标准方程为x^{2}=2\sqrt{6}y,其准线方程为:y=-\frac{\sqrt{6}}{2}设P(x_{P},y_{P}),Q(x_{Q},-\frac{\sqrt{6}}{2})因为以PQ为直径的圆过原点,所以OP\botOQ,所以x_{P}\neq0.所以_{P}x_{Q}-\frac{\sqrt{6}}{2}=0'即x_{Q}=\frac{\sqrt{6}y_{P}}{2x_{P}},所以|\frac{1}{|OP}

**Theorem Sequence**:  
Parabola_Equation_Standard_Right, Parabola_Definition, Parabola_Focal_Radius, Two_Points_Distance, Basic_Inequality

---

## Problem Index: 4384
**ID**: 4385
**Text**:  
已知$P(x, y)$是双曲线$\frac{x^{2}}{4}-y^{2}=1$上任意一点，$F_{1}$是双曲线的左焦点，$O$是坐标原点，则$\overrightarrow{P O} \cdot \overrightarrow{P F_{1}}$的最小值是?

**Process**:  
先算出\overrightarrow{PO}\cdot\overrightarrow{PF_{1}}的表达式,根据x的取值范围,求出\overrightarrow{PO}\cdot\overrightarrow{PF_{1}}的最值.由已知可得:F_{1}的坐标为(\sqrt{5},0),设P(x,y),则\overrightarrow{PO}\cdot\overrightarrow{PF_{1}}=(\cdotx,\cdoty)\cdot(\sqrt{5}\cdotx,-y)=x^{2}+\sqrt{5}x+y^{2}=x^{2}+\sqrt{5}x+\frac{x^{2}}{4}-1=\frac{5}{4}x^{2}+\sqrt{5}x\cdot1=(\frac{\sqrt{5}}{2}x+1)2-2,x\in(-\infty,2]\cup[2,+\infty)\therefore当x=-2时,\overrightarrow{P0}\cdot\overrightarrow{PF},的最小值为:4-2\sqrt{5}

**Theorem Sequence**:  
Ellipse_Equation_Standard_X, Ellipse_Tangent_Line, Vector_Collinear_Condition, Basic_Inequality

---

## Problem Index: 4388
**ID**: 4389
**Text**:  
已知双曲线$x^{2}-\frac{y^{2}}{b}=1$的一个焦点为$(2,0)$. 若已知点$M(4,0)$，点$N(x, y)$是双曲线上的任意一点，则$ |M N|$的最小值为?

**Process**:  
由题意得到1+b=4,所以b=3,因此得y^{2}=3x^{2}-3,由两点间的距离公式得|MN|=\sqrt{(x-4)^{2}+y^{2}}=\sqrt{4x^{2}-8x+13}=\sqrt{4(x^{2}-2x+1)+9}=\sqrt{4(x-1)^{2}+9}又x\leqslant-1或x\geqslant1\therefore当x=1时,|MN|取得最小值3

**Theorem Sequence**:  
Ellipse_Equation_Standard_X, Ellipse_Equation_Standard_Y, Two_Points_Distance, Basic_Inequality

---

## Problem Index: 4389
**ID**: 4390
**Text**:  
已知抛物线$y=a x^{2}$的准线与圆$x^{2}+y^{2}-6 y-7=0$相切，则$a$的值为?

**Process**:  
先表示出准线方程,然后抛物线y=ax2的准线与圆x^{2}+y^{2}-6y-7=0相切,可以得到圆心到准线的距离等于半径从而得到p的值.[详解]抛物线y=ax^{2},即x^{2}=\frac{1}{a}y''准线方程为y=-\frac{1}{4a}.因为抛物线x^{2}=\frac{1}{a}y的准线与圆x^{2}+(y-3)^{2}=16相切,当a>0时,3+\frac{1}{4a}=4,解得a=\frac{1}{4},当a<0时,-21.3=4,解得a=-\frac{1}{28}

**Theorem Sequence**:  
Parabola_Equation_Standard_Right, Parabola_Directrix, Circle_Standard_Equation, Point_To_Line_Distance

---

## Problem Index: 4444
**ID**: 4445
**Text**:  
若双曲线$\frac{x^{2}}{a^{2}}-\frac{y^{2}}{b^{2}}=1$的一个焦点到一条渐近线的距离为$2 a$，则双曲线的离心率为?

**Process**:  
双曲线焦点到渐近线的距离为b,\thereforeb=2a,\thereforeb^{2}=4a^{2},\thereforec^{2}-a^{2}=4a^{2},\therefore5a^{2}=c^{2},\thereforee=\sqrt{5}

**Theorem Sequence**:  
Hyperbola_Equation_Standard_X, Hyperbola_Focus_To_Asymptote_Distance, Eccentricity_Formula

---

## Problem Index: 4449
**ID**: 4450
**Text**:  
若双曲线$\frac{x^{2}}{a^{2}}-\frac{y^{2}}{b^{2}}=1(a>0, b>0)$的渐近线互相垂直，则该双曲线的离心率为?

**Process**:  
由题意可得双曲线为等轴双曲线,从而可得a=b,进而可求出离心率双曲线渐近线互相垂直可知为等轴双曲线,即:a=b,所以c=\sqrt{2}a.所以离心率e=\frac{c}{a}=\sqrt{2}

**Theorem Sequence**:  
Ellipse_Equation_Standard_X, Ellipse_Tangent_Line, Vector_Collinear_Condition, Basic_Inequality

---

## Problem Index: 4459
**ID**: 4460
**Text**:  
椭圆$\frac{x^{2}}{25}+\frac{y^{2}}{9}=1$的左焦点为$F_{1}$、$P$为椭圆上的动点，$M$是圆$x^{2}+(y-2 \sqrt{5})^{2}=1$上的动点，则$|P M|+|P F_{1}|$的最大值是?

**Process**:  
圆x^{2}+(y-2\sqrt{5})^{2}=1的圆心为C(0,2\sqrt{5}),半径为1由椭圆方程\frac{x^{2}}{25}+\frac{y^{2}}{9}-1可知a^{2}=25,b^{2}=9,所以a=5,左焦点F(-4,0)|PC|+|PF_{1}|=|PC|+2a-|PF_{2}|=10+|PC|-|PF_{2}|\leqslant10+|CF_{2}|=10+\sqrt{4^{2}+(2\sqrt{5})^{2}}=16(|PM|+|PF_{1})_{\max}=(|PC|+|PF_{1}|)_{\max}+1=17

**Theorem Sequence**:  
Ellipse_Equation_Standard_X, Circle_Standard_Equation, Ellipse_Definition, Pythagorean_Theorem, Two_Points_Distance

---

## Problem Index: 4477
**ID**: 4478
**Text**:  
已知双曲线$C$: $\frac{x^{2}}{a^{2}}-\frac{y^{2}}{b^{2}}=1(a>0, b>0)$的离心率为$\sqrt{3}$，若曲线$y(y-k x)=0$与双曲线$C$有且仅有$2$个交点，则实数$k$的取值范围?

**Process**:  
由已知,\sqrt{1+\frac{b^{2}}{a^{2}}}=\sqrt{3},\frac{b}{a}=\sqrt{2}\cdoty(y-kx)=0即y=0或y=kx,其中y=0与双曲线有两个交点,所以y=kx与双曲线无交点,所以y=kx处于y=\pm\sqrt{2}x所夹含纵轴的区域内,故k\leqslant-\sqrt{2}或k\geqslant\sqrt{2}

**Theorem Sequence**:  
Hyperbola_Equation_Standard_X, Hyperbola_Asymptote, Eccentricity_Formula

---

## Problem Index: 4489
**ID**: 4490
**Text**:  
已知抛物线$C$: $y^{2}=8 x$的焦点为$F$，准线与$x$轴的交点为$K$，点$A$在抛物线上，且$|A K|=\sqrt{2}|A F|$ , $O$是坐标原点，则$|O A|$=?

**Process**:  
设A到准线的距离等于AM,由抛物线的定义可得|AF|=|AM|,由|AK|=\sqrt{2}|AF|可得\triangleAMK为等腰直角三角形.设点A(\frac{s^{2}}{8},s),\because准线方程为x=-2,|AM|=|MK|.\therefore\frac{s^{2}}{8}+2=|s|,\therefores=\pm4,\thereforeA(2,\pm4),\therefore|AO|=\sqrt{4+16}=2\sqrt{5}

**Theorem Sequence**:  
Parabola_Equation_Standard_Right, Parabola_Definition, Parabola_Directrix, Two_Points_Distance

---

## Problem Index: 4493
**ID**: 4494
**Text**:  
若方程$\frac{x^{2}}{2+m}+\frac{y^{2}}{m+1}=1$表示双曲线，则实数$m$的取值范围是?

**Process**:  
分析:利用双曲线方程的特点,可得(2+m)(m+1)<0,解不等式,即可求出实数m的取值范围详因为方程\frac{x^{2}}{2+m}+\frac{y^{2}}{m+1}=1表示双曲线,所以(2+m)(m+1)<0,解得-2<m<-1,所以实数m的取值范围是(-2,-1).

**Theorem Sequence**:  
Ellipse_Equation_Standard_X, Ellipse_Equation_Standard_Y

---

## Problem Index: 4521
**ID**: 4522
**Text**:  
已知双曲线$\frac{x^{2}}{a^{2}}-\frac{y^{2}}{b^{2}}=1(a>0, b>0)$的右焦点为$F$，过$F$的直线$l$与双曲线的渐近线交于$A$、$B$两点，且与其中一条渐近线垂直，若$\overrightarrow{A F}=3 \overrightarrow{F B}$，则此双曲线的离心率为?

**Process**:  
由题意得右焦点F(c,0),设一条渐近线OA(O为坐标原点)的方程为y=\frac{b}{a}x,则另一条渐近线OB的方程为y=-\frac{b}{a}x'设A(m,\frac{bm}{a}),B(n,-\frac{bn}{a}),\because\overrightarrow{AF}=3\overrightarrow{FB},\therefore(c-m,-\frac{bm}{a})=3(n-c,-\frac{bn}{a})\therefore\_^{\circ}-m=3(n-c),-\frac{bm}{a}=-\frac{3bn}{a},解得m=2c,n=\frac{2}{3}c\thereforeB(\frac{2}{3}c,-\frac{2bc}{3a}).由题意知FB\botOB,则\frac{2b}{a}.(-\frac{b}{a})=-1,化简可得2b^{2}=a^{2},即2(c^{2}-a^{2})=a^{2}解得2c^{2}=3a^{2},即e=\frac{c}{a}=\frac{\sqrt{6}}{2}

**Theorem Sequence**:  
Ellipse_Equation_Standard_X, Ellipse_Definition, Eccentricity_Formula

---

## Problem Index: 4522
**ID**: 4523
**Text**:  
已知$F$为双曲线$C$: $\frac{x^{2}}{9}-\frac{y^{2}}{16}=1$的一个焦点，则点$F$到双曲线$C$的一条渐近线的距离为?

**Process**:  
双曲线C:\frac{x^{2}}{9}-\frac{y^{2}}{16}=1的焦点为(-5,0)、(5,0)由双曲线C的对称性,不妨取焦点F(5,0),渐近线为y=\frac{4}{3}x则则点F到渐近线的距离为d=\frac{|\frac{4}{3}\times5-0|}{\sqrt{1+(\frac{4}{2})^{2}}}=4

**Theorem Sequence**:  
Hyperbola_Equation_Standard_X, Hyperbola_Asymptote, Circle_Standard_Equation, Point_To_Line_Distance

---

## Problem Index: 4524
**ID**: 4525
**Text**:  
设$F_{1}$、$F_{2}$分别是椭圆$\frac{x^{2}}{16}+\frac{y^{2}}{7}=1$的左、右焦点，$E$为椭圆上任一点，$N$点的坐标为 $(5,1)$ ，则$|E N|+|E F_{1}|$的最大值为?

**Process**:  
首先利用椭圆的定义,转化|EN|+|EF_{1}|=8+(|EN|-|EF_{2}|),利用|EN|-|EF_{2}|\leqslant|NF_{2}|结合数形结合分析距离和的最大值.\because|EF_{1}|+|EF_{2}|=8\therefore|EN|+|EF_{1}|=8+(|EN|-|EF_{2}|)\because|EN|-|EF_{2}|\leqslant|NF_{2}|,如图,当E,F_{2},N三点共线时,等号成立所以\because|EN|-|EF_{2}|的最大值是|F_{2}N|=\sqrt{(5-3)^{2}+(1-0)^{2}}=\sqrt{5},即|EN|+|EF_{1}|的最大值是8+\sqrt{5}

**Theorem Sequence**:  
Ellipse_Equation_Standard_X, Eccentricity_Formula

---

## Problem Index: 4550
**ID**: 4551
**Text**:  
抛物线$y^{2}=x$上一点$P$到焦点的距离是$2$，则$P$点坐标为?

**Process**:  
由题意得抛物线的准线方程为x=-\frac{1}{4}设点P的坐标为(x_{0},y_{0}),则由抛物线的定义得x_{0}+\frac{1}{4}=2,解得x_{0}=\frac{7}{4}此时y_{0}^{2}=\frac{7}{4},解得y_{0}=\pm\frac{\sqrt{7}}{2}所以P点坐标为\frac{7}{4},\pm\frac{\sqrt{7}}{2}.答案:\frac{7}{4},\pm\frac{\sqrt{7}}{2}

**Theorem Sequence**:  
Parabola_Equation_Standard_Right, Parabola_Definition, Parabola_Directrix

---

## Problem Index: 4562
**ID**: 4563
**Text**:  
若抛物线的顶点在原点，对称轴为坐标轴，焦点在直线$3 x-4 y-12=0$上，则抛物线方程为?

**Process**:  
直线3x-4y-12=0与两坐标轴的交点坐标为(4,0),(0,-3),即抛物线的焦点为(4,0)或(0,-3);当焦点为(4,0)时,抛物线方程为y^{2}=16x;当焦点为(0,-3)时,抛物线方程为x^{2}=-12y;所以抛物线方程为y^{2}=16x或x^{2}=-12y

**Theorem Sequence**:  
Parabola_Equation_Standard_Right, Parabola_Directrix

---

## Problem Index: 4581
**ID**: 4582
**Text**:  
抛物线$y^{2}=4 x$上一点$M$到焦点的距离为$3$，则点$M$的横坐标$x$=?

**Process**:  
由题意得抛物线y^{2}=4x的焦点F(1,0),准线方程为x=-1,由抛物线的定义可知MF=x+1=3,解得x=2

**Theorem Sequence**:  
Parabola_Equation_Standard_Right, Parabola_Definition, Parabola_Directrix

---

## Problem Index: 4588
**ID**: 4589
**Text**:  
已知椭圆$\frac{x^{2}}{9}+\frac{y^{2}}{5}=1$的左右焦点分别为$F_{1}$、$F_{2}$，点$P$在椭圆上，设线段$P F_{1}$的中点为$M$ ,且$|O F_{2}|=|O M| $,则$\triangle P F_{1} F_{2}$的面积为?

**Process**:  
由余弦定理,结合椭圆的定义,可求得|PF_{2}||PF_{1}||F_{1}F_{2}|,再用余弦定理和面积公式求解即可由题意可得a=3,b=\sqrt{5},c=\sqrt{9-5}=2.因为O,M分别是F_{1}F_{2}和F_{1}P的中点,所以,|PF_{2}|=2|OM|=2|OF|_{2}=2c=4,根据椭圆定义,可得|PF_{1}|=2a-2c=2,又因》3F_{1}F_{2}=2c=4,所以,\cos\anglePF_{2}F_{1}=\frac{|PF|_{2}^{2}+|F_{1}F_{2}|^{2}-|PF_{1}|^{2}}{\sqrt[2]{PF|_{2}\cdot|F_{1}F|_{2}^{2}}}=\frac{16+16-4}{2\times4\times4}=\frac{7}{8},所以.\sin\anglePF_{F}_{1}=\sqrt{1-\cos^{2}\anglePF_{2}F_{1}=\frac{\sqrt{15}}{8},故\trianglePF_{1}F_{2}的面积是\frac{1}{2}|PF_{2}|\cdot|F_{1}F_{2}|\cdot\sin\anglePF_{2}F_{1}=\sqrt{15}

**Theorem Sequence**:  
Ellipse_Equation_Standard_X, Ellipse_Definition, Ellipse_Focal_Triangle_Perimeter, Triangle_Midline_Theorem, Triangle_Area_With_Sin, Triangle_Area_Formula

---

## Problem Index: 4602
**ID**: 4603
**Text**:  
椭圆$\frac{x^{2}}{25}+\frac{y^{2}}{9}=1$的左右焦点分别为$F_{1}$、$F_{2}$、$P$为椭圆上一点，且$\angle F_{1} P F_{2}=60^{\circ}$，则$\Delta F_{1} P F_{2}$的面积为?

**Process**:  
因为椭圆\frac{x^{2}}{25}+\frac{y^{2}}{9}=1的左右焦点分别为F_{1},F_{2},P为椭圆上一点所以|PF_{1}|+|PF_{2}|=10,|F_{1}F_{2}|=8,又\angleF_{1}PF_{2}=60^{\circ}在\triangleF_{1}PF_{2}由余弦定理可知,|F_{1}F_{2}|=|PF_{1}|^{2}+|PF_{2}|^{2}-2|PF_{1}|\cdot|PF_{2}|\cos60^{\circ}=(|PF_{1}|+|PF_{2}|)^{2}-2|PF_{1}||PF_{2}|-2|PF_{1}|\cdot|PF_{2}|\cos60^{\circ}=(|PF_{1}|+|PF_{2}|)^{2}-3|PF_{1}|\cdot|PF_{2}|=100-3|PF_{1}|\cdot|PF_{2}|=64,所以|PF_{1}|.|PF_{2}|=12,所以S\trianglePF_{1}F_{2}=\frac{1}{2}|PF_{1}|\cdot|PF_{2}|\sin60^{\circ}=3\sqrt{3}

**Theorem Sequence**:  
Ellipse_Equation_Standard_X, Ellipse_Definition, Ellipse_Focal_Triangle_Perimeter, Triangle_Area_Formula

---

## Problem Index: 4605
**ID**: 4606
**Text**:  
已知点$P$为抛物线$y^{2}=8 x$上一点，设$P$到此抛物线的准线的距离为$d_{1}$，到直线$4 x+3 y+8=0$的距离为$d_{2}$，则$d_{1}+d_{2}$的最小值为?

**Process**:  
y^{2}=8x的焦点F(2,0),由抛物线定义可知P到此抛物线的准线的距离为d_{1}=PF,所以d_{1}+d_{2}的最小值为F到直线4x+3y+8=0的距离\therefored=\frac{|8+8|}{\sqrt{4^{2}+3^{2}}}=\frac{16}{5}

**Theorem Sequence**:  
Parabola_Equation_Standard_Right, Parabola_Definition, Parabola_Directrix, Two_Points_Distance

---

## Problem Index: 4632
**ID**: 4633
**Text**:  
设抛物线$y^{2}=4 x$的焦点为$F$，过点$(\frac{1}{2}, 0)$的动直线交抛物线于不同的两点$P$、$Q$，线段$P Q$的中点为$M$，则点$M$的轨迹方程为?

**Process**:  
设直线PQ的方程为x=ty+\frac{1}{2},设P(x_{1},y_{1}),Q(x_{2},y_{2}),然后联立直线方程与抛物线方程,运用韦达定理得到y_{1}+y_{2},继而得出x_{1}+x_{2},再根据中点坐标公示得出点M的坐标,消去参数t得到轨迹方程.设直线PQ的方程为x=ty+\frac{1}{2},设P(x_{1},y_{1}),Q(x_{2},y_{2}),M(x,y)联立\begin{cases}y2=4x\\x=ty+\frac{1}{2}\end{cases},得y^{2}-4ty-2=0,则a=16t^{2}+8>0,所以y_{1}+y_{2}=4t,x_{1}+x_{2}=4t^{2}+1,由中点坐标公式得:M(2t^{2}+\frac{1}{2},2t)则由\begin{cases}x=2t^{2}+\frac{1}{2}\\y=2t\end{cases}消去t得,得点M的轨迹方程为y^{2}=2x-1.

**Theorem Sequence**:  
Ellipse_Equation_Standard_X, Vector_Collinear_Condition, Two_Points_Distance

---

## Problem Index: 4680
**ID**: 4681
**Text**:  
已知$F$是双曲线$\frac{x^{2}}{a^{2}}-\frac{y^{2}}{b^{2}}=1(a>0 , b>0)$的右焦点，$A$是双曲线上位于第一象限内的一点，$\overrightarrow{O A} \cdot \overrightarrow{O F}=|\overrightarrow{O F}|^{2}$，直线$O A$的方程为$y=\frac{2 \sqrt{3}}{3} x$，则双曲线的离心率为?

**Process**:  
分析:由\overrightarrow{OA}\cdot\overrightarrow{OF}=|\overrightarrow{OF}|^{2},可得AF\botx轴,从而求得A(c,\frac{b^{2}}{a}),代入直线OA的方程为y=\frac{2\sqrt{3}}{3}x'可得结果.详\because\overrightarrow{OA}\cdot\overrightarrow{OF}=|\overrightarrow{OA}|\cdot|\overrightarrow{OF}|\cos<AOF=|\overrightarrow{OF}|^{2}\therefore\overrightarrow{OA}\cos<A\overrightarrow{OF}=|\overrightarrow{OF}|.,\thereforeAF\botx轴,令x=c,得y_{A}=\frac{b^{2}}{a},\thereforeA(c,\frac{b^{2}}{a})又\becauseOA的方程为y=\frac{2\sqrt{3}}{3}x'\therefore\frac{b^{2}}{c}=\frac{2\sqrt{3}}{3}'\therefore\frac{b^{2}}{ac}=\frac{a^{2}-c^{2}}{ac}=\frac{2\sqrt{3}}{3}即e-\frac{1}{e}=\frac{2\sqrt{3}}{3},e^{2}-\frac{2\sqrt{3}}{3}e-1=0'e=\sqrt{3},

**Theorem Sequence**:  
Ellipse_Equation_Standard_X, Ellipse_Definition, Eccentricity_Formula, Vector_Collinear_Condition

---

## Problem Index: 4685
**ID**: 4686
**Text**:  
抛物线$y^{2}=2 x$的一条弦被$A(4,2)$平分，那么这条弦所在的直线方程是?

**Process**:  
设弦的两个端点的坐标,用点差法,即:代入抛物线方程后作差,代入A点坐标得到弦所在的直线的斜率,由点斜式求出直线的方程设弦的两个端点为M(x_{1},y_{1}),N(x_{2},y_{2})分别代入抛物线方程,得:y_{1}2=2x\textcircled{1}\textcircled{1}\textcircled{1}-\textcircled{2}得:y_{1}2-y_{2}^{2}=2(x_{1}-x_{2}),即\frac{y_{1}^{2}}{x_{1}-x_{2}}=又因为MN被点A(4,2)平分,所以y_{1}+y_{2}即弦MN所在的直线的斜率k=\frac{1}{2}所以这条线所在的直线方程为:y-2=\frac{1}{2}(x-4),即x-2y=0.

**Theorem Sequence**:  
Parabola_Equation_Standard_Right, Point_Difference_Method, Midpoint_Formula

---

## Problem Index: 4698
**ID**: 4699
**Text**:  
已知点$A(0,4)$，抛物线$C$: $x^{2}=2 p y(0<p<4)$的准线为$l$，点$P$在$C$上，作$P H \perp l$于$H$，且$|P H|=|P A|$，$\angle A P H=120^{\circ}$，则抛物线方程为?

**Process**:  
设抛物线的焦点为F(0,\frac{p}{2}),|AF|=4-\frac{p}{2},由抛物线的定义可知,|PH|=|PF|\because|PH|=|PA|,\therefore|PA|=|PF|,不妨设点P在第一象限,过点P作PQ\boty轴于点Q,则Q为AF的中点,|AQ|=|FQ|=\frac{1}{2}|AF|=\frac{1}{2}(4-\frac{p}{2}),\because\frac{1}{2}(4-\frac{\frac{x}{2}}{2}),\because\angleAPH=120^{\circ},\therefore\angleAPQ=120^{\circ}-90^{\circ}=30^{\circ},\therefore|PQ|=\sqrt{3}|AQ|=\frac{\sqrt{3}}{2}(4-\frac{p}{2})^{,}|OQ|=|FQ|+|OF|=\frac{1}{2}(4-\frac{p}{2})+\frac{p}{2}=2+\frac{p}{4},\therefore点P的坐标为(\frac{\sqrt{3}}{2}(4-\frac{p}{2}),2+\frac{p}{4},\because点P在抛物线C上,\therefore\sqrt{3}(4-\frac{p}{2})]=2p\times(2+\frac{p}{4})^{,}化简得5p^{2}+112p-192=0,解之得p=\frac{8}{5}或-24(舍负)\therefore抛物线方程为x^{2}=\frac{16}{5}y

**Theorem Sequence**:  
Parabola_Equation_Standard_Up, Parabola_Directrix, Parabola_Definition, Triangle_Midline_Theorem

---

## Problem Index: 4732
**ID**: 4733
**Text**:  
设直线过双曲线$C$的一个焦点，且与$C$的一条对称轴垂直，与$C$交于$A$、$B$两点，$|A B|$为$C$的实轴长的$2$倍，则$C$的离心率为?

**Process**:  
设双曲线的标准方程为\frac{x^{2}}{a^{2}}-\frac{y^{2}}{b^{2}}=1(a>0,b>0),由题意,得\frac{2b^{2}}{a}=4a'即b^{2}=2a^{2}.c^{2}=3a2,所以双曲线的离心率为e=\sqrt{3}

**Theorem Sequence**:  
Hyperbola_Equation_Standard_X, Hyperbola_Latus_Rectum, Eccentricity_Formula

---

## Problem Index: 4762
**ID**: 4763
**Text**:  
已知$F_{1}$、$F_{2}$为椭圆$\frac{x^{2}}{9}+\frac{y^{2}}{5}=1$的两个焦点，过点$F_{1}$的直线交椭圆于$A$、$B$两点，若$|A B|=5$，则$\triangle A B F_{2}$的面积为?

**Process**:  
设直线AB的方程为y=k(x+2),A(x_{1},y_{1}),B(x_{2},y_{2}),联立方程组,利用弦长公式和椭圆的定义,求得_{k}=\pm\frac{\sqrt{3}}{3},得出直线AB的方程,再结合点到直线的距离公式和三角形的面积公式,即可求解.由椭圆\frac{x2}{9}+\frac{y^{2}}{5}=1,可得a^{2}=9,b^{2}=5,则c=\sqrt{a^{2}-b^{2}}=2即椭圆的焦点坐标分别为F_{1}(-2,0),F_{2}(2,0),设直线AB的方程为y=k(x+2),A(x_{1},y_{1}),B(x_{2},y_{2})组\begin{cases}y=k(x+2)\\\frac{x^{2}}{9}+\frac{y^{2}}{5}=1\end{cases},可得(5+9k^{2})x^{2}+36k^{2}x+36k^{2}-45=0则x_{1}+x_{2}=-\frac{36k^{2}}{5+9k^{2}},x_{1}x_{2}=\frac{36k^{2}-45}{5+9k^{2}}根据椭圆的定义,可得推得|AB|=e(x_{1}+x_{2})+2a=\frac{2}{3}\times(-\frac{36k^{2}}{5+9k^{2}})+6=5解得k^{2}=\frac{1}{3},即k=\pm\frac{\sqrt{3}}{3},此时直线方程为y=\pm\frac{\sqrt{3}}{3}(x+2)即直线方程为\sqrt{3}x-3y+2\sqrt{3}=0或-\sqrt{3}x+3}-2\sqrt{3}=0,又由点F_{2}到直线AB的距离都为d_{1}=\frac{|2\sqrt{3}+2\sqrt{3}|}{\sqrt{3+9}}=2或d_{2}=\frac{|-2\sqrt{3}-2\sqrt{3}|}{\sqrt{3+9}}=2,所以\triangleABF_{2}的面积为S=\frac{1}{2}|AB|\cdotd=\frac{1}{2}\times5\times2=5.

**Theorem Sequence**:  
Ellipse_Equation_Standard_X, Point_Difference_Method_Hyperbola, Line_Point_Slope_Form, Eccentricity_Formula, Point_To_Line_Distance, Triangle_Area_Formula

---

## Problem Index: 4773
**ID**: 4774
**Text**:  
已知抛物线$y^{2}=4 x$的焦点为$F$，点$A$、$B$是抛物线上两点，且点$A$在第一象限内. 若$\overrightarrow{A F}=4 \overrightarrow{F B}$，则直线$A B$的方程的一般形式为?

**Process**:  
由已知,F(1,0),直线AB的斜率不为0,设A(x_{1},y_{1}),B(x_{2},y_{2})(y_{1}>0,y_{2}<0)直线AB的方程为x=my+1,联立抛物线方程得y^{2}-4my-4=0,y_{1}+y_{2}=4m,y_{1}y_{2}=-4,又\overrightarrow{AF}=4\overrightarrow{FB},所以(1-x_{1},-y)=4(x_{2}-1,y_{2})所以y_{1}=-4y_{2},y_{1}y_{2}=-4y_{2}^{2}=-^{\frac{1}{4}}所以y_{2}=-1,y_{1}=4,从而y_{1}+y_{2}=3=4m,解得m=\frac{3}{4}所以AB方程为x=\frac{3}{4}y+1,即4x-3y-4=0.

**Theorem Sequence**:  
Parabola_Equation_Standard_Right, Substitution_x_equals_my_plus_n, Vieta_Theorem_Sum, Vieta_Theorem_Product, Triangle_Area_Formula

---

## Problem Index: 4861
**ID**: 4862
**Text**:  
设$b \in R$，若曲线$y^{2}=-|x|+1$与直线$y=-x+b$有公共点，则$b$的取值范围是?

**Process**:  
y^{2}=-|x|+1=\begin{cases}-x+1,x\geqslant0\\x+1,x\leqslant0\end{cases}如图所示:当直线y=-x+b与曲线y^{2}=-x+1相\Square时\begin{cases}y2=-x+1\\v=-x+b\end{cases}\Rightarrowx^{2}+(1-2b)x+b^{2}-1=0,\Delta=(1-2b)^{2}-4(b^{2}-1)=0,解得b=\frac{5}{4}当直线yy=-x+b与曲线y^{2}=x+1相切时,\begin{cases}y^{2}=x+1\\v=-x+b\end{cases}\Rightarrowx^{2}-(2b+1)x+b^{2}-1=0,\triangle=(2b+1)^{2}-4(b^{2}-1)=0,解得b=-\frac{5}{4}因为曲线y^{2}=-|x|+1与直线y=-x+b有公共点,所以b的取值范围为[-\frac{5}{4},\frac{5}{4}].

**Theorem Sequence**:  
Parabola_Equation_Standard_Right, Parabola_Directrix, Point_Difference_Method_Hyperbola, Discriminant_Delta, Quadratic_Function_Maximum

---

## Problem Index: 4871
**ID**: 4872
**Text**:  
双曲线$4 x^{2}-3 y^{2}=-12$的渐近线方程为?

**Process**:  
该双曲线的标准方程为\frac{y^{2}}{4}-\frac{x^{2}}{3}=1,它的焦点在y轴上,其中a=2,b=\sqrt{3},所以渐近线方程为y=\pm\frac{a}{b}x=\pm\frac{2}{\frac{2}{5}}x=\pm\frac{2\sqrt{3}}{3}x

**Theorem Sequence**:  
Hyperbola_Equation_Standard_Y, Hyperbola_Asymptote

---

## Problem Index: 4922
**ID**: 4923
**Text**:  
已知双曲线$\frac{y^{2}}{6}-\frac{x^{2}}{3}=1$，则以双曲线中心为顶点，以双曲线准线为准线的抛物线方程为?

**Process**:  
双曲线\frac{y^{2}}{6}-\frac{x^{2}}{3}=1的准线方程为:y=\pm\frac{a^{2}}{c}\Rightarrowy=\pm2,由题意可知,抛物线的准线方程为y=\pm2,所以标准方程为x^{2}=\pm8y

**Theorem Sequence**:  
Hyperbola_Equation_Standard_Y, Ellipse_Directrix, Parabola_Directrix

---

## Problem Index: 4926
**ID**: 4927
**Text**:  
已知椭圆$C$: $\frac{x^{2}}{25}+\frac{y^{2}}{9}=1$, $F_{1}$, $F_{2}$是该椭圆的左、右焦点，点$A(4,1)$ , $P$是椭圆上的一个动点，当$\triangle A P F_{1}$的周长取最大值时，$\triangle A P F_{1}$的面积为?

**Process**:  
分析:先利用椭圆的定义将椭圆上的点到左焦点的距离转化为到右焦点的距离,再利用平面几何知识进行求解.详连接AF_{2},PF_{2},由椭圆方程\frac{x^{2}}{25}+\frac{y^{2}}{9}=1,得a=5,F_{1}(-4,0),F_{2}(4,0),则AAPF_{1}的周长为|PF_{1}|+|PA|+|AF_{1}|=10+|PA|-|PF_{2}|+|AF_{1}|\leqslant10+|AF_{2}|+|AF_{1}|(当且仅当P在射线AF_{2}上时取等号),在椭圆方程\frac{x^{2}}{25}+\frac{y^{2}}{9}=1中令x=4,得y=-\frac{9}{5},则|AP|=\frac{14}{5},S_{AAPF_{1}}=\frac{1}{2}\times8\times\frac{14}{5}=\frac{56}{5}

**Theorem Sequence**:  
Ellipse_Equation_Standard_X, Ellipse_Definition, Pythagorean_Theorem, Two_Points_Distance, Triangle_Area_Formula

---

## Problem Index: 4933
**ID**: 4934
**Text**:  
一条渐近线方程是$x+\sqrt{3} y=0$的双曲线，它的一个焦点与方程是$y^{2}=16 x$的抛物线的焦点相同，此双曲线的标准方程是?

**Process**:  
因为抛物线y^{2}=16x,所以其焦点为(4,0)因为双曲线的一条渐近线是x+\sqrt{3}y=0.所以,设双曲线方程为\frac{x^{2}}{3\lambda}-\frac{y^{2}}{\lambda}=1所以3\lambda+\lambda=16,\lambda=4故所求的双曲线方程为\frac{x^{2}}{12}-\frac{y^{2}}{4}=1】本题考查通过双曲线的渐近线和焦点求标准方程,属于简单题

**Theorem Sequence**:  
Parabola_Equation_Standard_Right, Hyperbola_Equation_Standard_X, Hyperbola_Asymptote

---

## Problem Index: 4937
**ID**: 4938
**Text**:  
双曲线$\frac{x^{2}}{a^{2}}-y^{2}=1(a>0)$的左右焦点分别为$F_{1}$、$F_{2}$、$P$为双曲线右支上一点，若$|P F_{1}|=6$，且$\cos \angle F_{1} P F_{2}=\frac{5}{6}$，则双曲线的离心率为?

**Process**:  
因为|PF_{1}|=6,则|PF_{2}|=6-2a,且|F_{1}F_{2}|=2c=2\sqrt{a^{2}+1}.又\cos\angleF_{1}PF_{2}=\frac{5}{6},由余弦定理\cos\angleF_{1}PF_{2}=\frac{|PF_{1}|^{2}+|PF_{2}|^{2}-|F_{1}F_{2}|^{2}}{2|PF_{1}||PF_{2}|}=\frac{s}{(}即\frac{5}{6}=\frac{36+36-24a+4a2-4a2-4}{2\times6\times(6-2a)},解得a=2.所以c=\sqrt{5},所以双曲线的离心率e=\frac{c}{a}=\frac{\sqrt{5}}{2}

**Theorem Sequence**:  
Hyperbola_Equation_Standard_X, Hyperbola_Definition, Pythagorean_Theorem, Triangle_Area_With_Sin, Eccentricity_Formula

---

## Problem Index: 4941
**ID**: 4942
**Text**:  
设双曲线$C$: $\frac{x^{2}}{2}+\frac{y^{2}}{m}=1$的离心率为$e$，其渐近线与圆$M$:$(x-2)^{2}+y^{2}=e^{2}$相切，则$m$=?

**Process**:  
由题意可知m<0,双曲线的渐近线方程为\frac{x}{\sqrt{2}}\pm\pm\frac{y}{\sqrt{-m}}=0,即\sqrt{-m}\pm\sqrt{2}y=0且e^{2}=1+\frac{-m}{2},圆心到渐近线的距离为\frac{|2\sqrt{-m}}{\sqrt{2-m}}|=e=\sqrt{1-\frac{m}{2}}化简得(m+2)^{2}=0,解得m=-2,

**Theorem Sequence**:  
Hyperbola_Equation_Standard_X, Hyperbola_Asymptote, Circle_Standard_Equation, Point_To_Line_Distance, Eccentricity_Formula

---

## Problem Index: 4966
**ID**: 4967
**Text**:  
已知抛物线$C$: $y^{2}=4 x$ , $F$为$C$的焦点，过点$(-2,0)$且斜率为$\frac{2}{3}$的直线$l$交抛物线于$A$、$B$两点，则$|A F|+|B F|$=?

**Process**:  
设A(x_{1},y_{1}),B(x_{2},y_{2}),由题意可得直线方程为y=\frac{2}{3}(x+2),与抛物线方程联立\begin{cases}y=\frac{2}{3}(x+2)\\y^{2}=4x\end{cases}得x^{2}-5x+4=0,所以x_{1}+x_{2}=5,由抛物线焦半径公式得|AF|+|BF|=x_{1}+\frac{p}{3}+x_{2}+\frac{p}{2}=x_{1}+x_{2}+p=5+2=7.故答客为:7.

**Theorem Sequence**:  
Parabola_Equation_Standard_Right, Substitution_x_equals_my_plus_n, Parabola_Focal_Radius

---

## Problem Index: 4992
**ID**: 4993
**Text**:  
$F_{1}$、$F_{2}$是椭圆$\frac{x^{2}}{5}+\frac{y^{2}}{4}=1$的左、右焦点，点$P$在椭圆上运动，则$|P F_{1}| \cdot|P F_{2}|$的最大值是?

**Process**:  
因为点P在椭圆\frac{x^{2}}{5}+\frac{y^{2}}{4}=1上,|由椭圆的定义可知|PF_{1}|+|PF_{2}|=2a=2\sqrt{5}又由|PF_{1}||PF_{2}|\leqslant(\frac{|PF_{1}+|PF_{2}|}{2})^{2}=(\sqrt{5})^{2}=5'当且仅当|PF_{1}|=|PF_{2}|时取等号所以|PF_{1}||PF_{2}|的最大值为5.

**Theorem Sequence**:  
Ellipse_Equation_Standard_X, Ellipse_Definition, Basic_Inequality

---

## Problem Index: 5009
**ID**: 5010
**Text**:  
曲线$C$:$|x^{2}-y^{2}-1|=1$与直线$l$: $y=k x-1$有$4$个交点，则$k$的取值范围是?

**Process**:  
曲线C:|x^{2}-y^{2}-1|=1化简为x^{2}-y^{2}=0即y=\pmx,或x^{2}-y^{2}=2,所以曲线C表示两题相交直线与双曲线,曲线C与直线l由4个交点,所以与两直线y=\pmx有两个交点.只需k\neq\pm1,直线l与双曲线x^{2}-y^{2}=2有两个交点,联立\begin{cases}y=kx-1\\x^{2}-y^{2}=2\end{cases}消去y得,(1-k^{2})x^{2}+2kx-3=0,方程有两个解须\begin{cases}k^{2}-1\neq0\\4=4k^{2}-12(1-k^{2})>0\end{cases}解得-\frac{\sqrt{6}}{2}<k<\frac{\sqrt{6}}{2}且k\neq\pm1,所以所求的k的取值范围是(-\frac{\sqrt{6}}{2},-1)\cup(

**Theorem Sequence**:  
Hyperbola_Equation_Standard_X, Point_Difference_Method_Hyperbola, Discriminant_Delta, Quadratic_Function_Maximum

---

## Problem Index: 5022
**ID**: 5023
**Text**:  
双曲线$\frac{x^{2}}{16}-\frac{y^{2}}{9}=1$的离心率为?

**Process**:  
由题可知:a=4,b=3,由c=\sqrt{a^{2}+b^{2}}=5所以离心率e=\frac{c}{a}=\frac{5}{4}

**Theorem Sequence**:  
Hyperbola_Equation_Standard_X, Hyperbola_Parameter_Relation, Eccentricity_Formula

---

## Problem Index: 5023
**ID**: 5024
**Text**:  
动圆$x^{2}+y^{2}-(4 m+2) x-2 m y+4 m^{2}+4 m+1=0$的圆心的轨迹方程是?

**Process**:  
把圆的方程化为标准方程得:[x-(2m+1)]^{2}+(y-m)^{2}=m2(m\neq0),则圆心坐标为\begin{cases}x=2m+1\\y=m\end{cases},因为m\neq2m+1,因为m\neq0,得到x\neq1,消去m可得x-2y-1=0,

**Theorem Sequence**:  
Circle_Standard_Equation, Vector_Collinear_Condition

---

## Problem Index: 5082
**ID**: 5083
**Text**:  
已知椭圆$M$: $\frac{x^{2}}{4}+y^{2}=1$，直线$l$与椭圆$M$相交于$A$、$B$两点，点$D(1, \frac{1}{2})$是弦$A B$的中点，则直线$l$的方程为?

**Process**:  
设A(x_{1},y_{1},B(x_{2},y_{2}),因为直线l与椭圆M相交于A,B两点所以有\begin{cases}\frac{x_{1}^{2}}{4}+y_{1}^{2}=1\\\frac{x_{2}}{4}+y_{2}=1\end{cases},两式作差得:y_{1}-y_{2}^{2}=\frac{x_{2}}{4}-\frac{x_{1}}{4}整理得k_{AB}=\frac{y_{1}-y_{2}}{x_{1}-x_{2}}=-\frac{1}{4}\times\frac{x_{1}+x_{2}}{y_{1}+y_{2}}因为点D(1,\frac{1}{2})是弦AB的中点,所以x_{1}+x_{2}=2,y_{1}+y_{2}=1,所以k_{AB}=-\frac{1}{2}所以直线l的方程为y-\frac{1}{2}=-\frac{1}{2}(x-1),整理得x+2y-2=0

**Theorem Sequence**:  
Ellipse_Equation_Standard_X, Point_Difference_Method, Midpoint_Formula

---

## Problem Index: 5087
**ID**: 5088
**Text**:  
已知圆$C$过双曲线$\frac{x^{2}}{9}-\frac{y^{2}}{16}=1$的一个顶点和一个焦点，且圆心在此双曲线上，则圆心到双曲线中心的距离是?

**Process**:  
由双曲线的几何性质易知圆C过双曲线同一支上的顶点和焦点,所以圆C的圆心的横坐标为4.故圆心坐标为(4,\pm\frac{4\sqrt{7}}{3})\therefore它到中心(0,0)的距离为d=\sqrt{16+\frac{112}{9}}=\frac{16}{3}

**Theorem Sequence**:  
Hyperbola_Equation_Standard_X, Hyperbola_Asymptote, Circle_Standard_Equation

---

## Problem Index: 5096
**ID**: 5097
**Text**:  
抛物线$M$:$y^{2}=8 x$的焦点为$F$，双曲线$x^{2}-y^{2}=1$的一条渐近线与抛物线$M$交于$A$、$B$两点，则$\triangle A B F$的面积为?

**Process**:  
由已知F(2,0),双曲线的一条渐近线为y=x,由\begin{cases}y=x\\y2=8x\end{cases}得\begin{cases}x=0\\y=0\end{cases}或\begin{cases}x=8\\y=8\end{cases},即A(0,0),B(8,8),所以S_{\triangleABF}=\frac{1}{2}\times2\times8=8.

**Theorem Sequence**:  
Parabola_Equation_Standard_Right, Hyperbola_Equation_Standard_X, Hyperbola_Asymptote, Triangle_Area_Formula

---

## Problem Index: 5110
**ID**: 5111
**Text**:  
若抛物线$x^{2}=2 p y(p>0)$上的点$(m, 3)$到焦点的距离是$5$, 则$m^{2}$=?

**Process**:  
因为(m,3)是抛物线x^{2}=2py(p>0)上的点,所以点(m,3)到焦点的距离3-(-\frac{p}{2})=5,解得p=4,所以抛物线方程为x^{2}=8y.点(m,3)代入x^{2}=8y得m^{2}=24

**Theorem Sequence**:  
Parabola_Equation_Standard_Up, Parabola_Definition, Parabola_Directrix

---

## Problem Index: 5130
**ID**: 5131
**Text**:  
已知椭圆$C$: $\frac{x^{2}}{a^{2}}+\frac{y^{2}}{b^{2}}=1(a>b>0)$的离心率为$\frac{\sqrt{3}}{2}$，过右焦点$F$且斜率为$k(k>0)$的直线与椭圆$C$相交于$A$、$B$两点. 若$\overrightarrow{A F}=3 \overrightarrow{F B}$，则$k$=?

**Process**:  
由已知e=\frac{c}{a}=\sqrt{1-\frac{b^{2}}{a^{2}}}=\frac{\sqrt{3}}{2},所以a=2b,所以a=\frac{2}{\sqrt{3}}c,b=\frac{c}{\sqrt{3}},则椭圆方程\frac{x^{2}}{a^{2}}+\frac{y^{2}}{b^{2}}=1变为\frac{3}{4}x^{2}+3y^{2}=c^{2}.设AA(x_{1},y_{1}),B(x_{2},y_{2}),又\overrightarrow{AF}=3\overrightarrow{FB},所以(c-x_{1},-y_{1})=3(x_{2}-c,y_{2}),所以\begin{cases}c-x_{1}=3(x_{2}\\-y_{1}=3y_{2}\end{cases}所以\begin{cases}x_{1}+3x_{2}=4c\\y_{1}+3y_{2}=0\end{cases}\frac{3}{4}x_{1}^{2}+3y_{1}^{2}=c^{2}\textcircled{1}\frac{3}{4}x_{2}^{2}+3y_{2}^{2}=c^{2}\textcircled{2}.\textcircled{1}-9\times\textcircled{2},得\frac{3}{4}(x_{1}+3x_{2})(x_{1}-3x_{2})+3(y_{1}+3y_{2})(y_{1}-3y_{2})=-8c^{2},所以\frac{3}{4}\times4c(x_{1}-3x_{2})=-8c^{2},所以x_{1}-3x_{2}=-\frac{8}{3}c,所以x_{1}=\frac{2}{3}c,x_{2}=\frac{10}{9}c,从而y_{1}=-\frac{\sqrt{2}}{3}c^{2}y_{2}=\frac{\sqrt{2}}{9},所以A(\frac{2}{3}c,-\frac{\sqrt{2}}{3}c),B(\frac{10}{9}c,\frac{\sqrt{2}}{9}c),故k=\sqrt{2}

**Theorem Sequence**:  
Ellipse_Equation_Standard_X, Ellipse_Definition, Vector_Collinear_Condition, Eccentricity_Formula

---

## Problem Index: 5137
**ID**: 5138
**Text**:  
过双曲线$C$: $\frac{x^{2}}{a^{2}}-\frac{y^{2}}{b^{2}}=1(a>0 , b>0)$右支上一点$P$作两条渐近线的平行线分别与另一渐近线交于点$M$、$N$、$O$为坐标原点，设$\Delta O M N$的面积为$S$，若$S \geq \frac{b^{2}}{2}$，则双曲线$C$的离心率取值范围为 (用区间作答)?

**Process**:  
设P(m,n),y=-\frac{b}{a}x+d是过P与渐近线y=-\frac{b}{a}x平行的直线,交y轴于D(0,d)点,与渐近线y=\frac{b}{a}x交于M(x_{1},y_{1}),联立\begin{cases}y=-\frac{b}{a}x+d\\y=\frac{b}{a}x\end{cases}解得x_{1}=\frac{bm+an}{2b}则S_{\triangleDOM}=\frac{1}{2}|x_{1}\cdotd|,由题知四边形OMPN是平行四边形又P(m,n)在双曲线上,应满足\frac{m^{2}}{a^{2}}-\frac{n^{2}}{b^{2}}=1,即b^{2}m^{2}-a^{2}n^{2}=a^{2}b^{2}则S_{OMPN}=2S_{\DeltaOMP}=2(S_{\DeltaOPD}-S_{\DeltaDMO})=|md|-|x_{1}\cdotd|=|(m-x_{1})d|=|\frac{(bm-an)(bm+an)}{2ab}|=\frac{a2b^{2}}{2ab}=\frac{ab}{2}则S=\frac{1}{2}S_{OMPN}=\frac{ab}{4}\geqslant\frac{b^{2}}{2},解得\frac{b}{a}\leqslant\frac{1}{2}可得离心率e=\frac{c}{a}=\sqrt{1+\frac{b^{2}}{a2}}\leqslant\frac{\sqrt{5}}{2}所以离心率的范围为(1,\frac{\sqrt{5}}{2}]'

**Theorem Sequence**:  
Hyperbola_Equation_Standard_X, Hyperbola_Asymptote, Point_Difference_Method_Hyperbola, Triangle_Midline_Theorem, Triangle_Area_Formula, Basic_Inequality

---

## Problem Index: 5168
**ID**: 5169
**Text**:  
圆$x^{2}+y^{2}=9$的切线$M T$过双曲线$\frac{x^{2}}{9}-\frac{y^{2}}{12}=1$的左焦点$F$，其中$T$为切点，$M$为切线与双曲线右支的交点，$P$为$M F$的中点，则$|P O|-|P T|$=?

**Process**:  
记右焦点F,|FF|=\sqrt{OF^{2}-|or|}=b\Rightarrow|P|=|PF|-|TF|=\frac{1}{2}|MF|-b,|PO|=\frac{1}{2}|PF|\Rightarrow|PO|-|PF|=b-\frac{1}{2}|MF|-|MF|=b-a=2\sqrt{3}-3

**Theorem Sequence**:  
Hyperbola_Equation_Standard_X, Ellipse_Latus_Rectum, Eccentricity_Formula

---

## Problem Index: 5231
**ID**: 5232
**Text**:  
已知两定点$A(-1,0)$, $B(1,0)$，如果平面内动点$C$满足条件$|C A|=\sqrt{3}|C B|$，则$S_\triangle{A B C}$的最大值是?

**Process**:  
设动点C坐标,再由几何条件|CA|=\sqrt{3}|CB|,可得C轨迹方程,进一步可得所求解设C(x,y),由|CA|=\sqrt{3}|CB|,\_可得\sqrt{(x+1)^{2}+(y-0)^{2}}=\sqrt{3}\sqrt{(x-1)^{2}+(y-0)^{2}}整理得:x^{2}+y^{2}-4x+1=0,即(x-2)^{2}+y^{2}=3所以S_{AABC}=\frac{1}{2}\times|AB|\timesh_{AB}(h_{AB}表示\triangleABC中AB边上的高)显然(h_{AB})_{\max}=\sqrt{3},所以S_{AABC}最大值为\sqrt{3}

**Theorem Sequence**:  
Circle_Standard_Equation, Two_Points_Distance

---

## Problem Index: 5241
**ID**: 5242
**Text**:  
已知$A(-\frac{1}{2}, 0)$, $B$是圆$F$:$(x-\frac{1}{2})^{2}+y^{2}=4$($F$为圆心) 上一动点，线段$A B$的垂直平分线交$B F$于$P$，则动点$P$的轨迹方程为?

**Process**:  
先根据题意可知|BP|+|PF|正x而PB|=|PA|,进而可知|AP|+|PF|=2.根据椭圆的定义可知,点P的轨迹为以A,F为焦点的椭圆,根据A,F求得a,c,进而求得b,答案可得依题意可知|BP|+|PF|=2,|PB|=|PA|\therefore|AP|+|PF|=2根据椭圆的定义可知,点P的轨迹为以A,F为焦点的椭圆,a=1,c=\frac{1}{2},则有b=\frac{\sqrt{3}}{2}故点P的轨迹方程为x^{2}+\frac{4}{3}y^{2}=1

**Theorem Sequence**:  
Ellipse_Equation_Standard_X, Ellipse_Definition, Circle_Standard_Equation, Pythagorean_Theorem

---

## Problem Index: 5246
**ID**: 5247
**Text**:  
若$a>2$，则双曲线$\frac{x^{2}}{a^{2}}-\frac{y^{2}}{(a+1)^{2}}=1$的离心率$e$的取值范围是?

**Process**:  
运用双曲线的离心率公式和二次函数的单调性,计算可得e的取值范围.[详解]双曲线\frac{x^{2}}{a^{2}}-\frac{y^{2}}{(a+1)^{2}}=1,可得e^{2}=\frac{a^{2}+(a+1)^{2}}{a^{2}}=2+\frac{2}{a}+\frac{1}{a^{2}}=(\frac{1}{a}+1)^{2}+1由a>2,可得0<\frac{1}{a}<\frac{1}{2},则e^{2}\in(2,\frac{13}{4}),可得e\in(\sqrt{2},\frac{\sqrt{13}}{2})

**Theorem Sequence**:  
Hyperbola_Equation_Standard_X, Eccentricity_Formula, Ellipse_Eccentricity_Range

---

## Problem Index: 5267
**ID**: 5268
**Text**:  
已知抛物线$C$:$4 x+a y^{2}=0$恰好经过圆$M$:$(x-1)^{2}+(y-2)^{2}=1$的圆心，则抛物线$C$的焦点坐标为?

**Process**:  
圆M的圆心为(1,2),代入4x+ay2=0得a=-1,将抛物线C的方程化为标准方程得y^{2}=4x,故焦点坐标为(1,0).

**Theorem Sequence**:  
Ellipse_Equation_Standard_X, Hyperbola_Asymptote, Eccentricity_Formula

---

## Problem Index: 5281
**ID**: 5282
**Text**:  
已知双曲线的焦距为$10$，双曲线上的点到两个焦点之间的距离之差的绝对值为$8$，则该双曲线标准方程的焦点坐标是?

**Process**:  
由题意知:焦点在x轴上时,坐标为(5,0),(-5,0);焦点在y轴上时,焦点坐标为(0,5),(0,-5).故焦点为:(5,0),(-5,0)或(0,5),(0,-5)

**Theorem Sequence**:  
Hyperbola_Equation_Standard_X

---

## Problem Index: 5285
**ID**: 5286
**Text**:  
设点$P(x_{1}, y_{1})$在椭圆$\frac{x^{2}}{8}+\frac{y^{2}}{2}=1$上，点$Q(x_{2}, y_{2})$在直线$x+2 y-8=0$上，则$3|x_{2}-x_{1}|+6|y_{2}-y_{1}|$的最小值为?

**Process**:  
由题意,设\begin{cases}x_{1}=2\sqrt{2}\cos\alpha\\y=\sqrt{2}\sin\alpha\end{cases},\alpha\in[0,2\pi),则3|x_{2}-x_{1}|+6|y_{2}-y_{1}|=3|x_{2}-2\sqrt{2}\cos\alpha|+6|y_{2}-\sqrt{2}\sin\alpha|=3(|x_{2}-2\sqrt{2}\cos\alpha|+2|y_{2}-\sqrt{2}\sin\alpha|)3(|x|2\sqrt{2}\cos\alpha|+2|,-\sqrt{2}\sin\alpha)\geqslant3|x_{2}+2y.-2\sqrt{2}(\cos\alpha+\sin\alpha)=3|8-4\sin(\alpha+\frac{\pi}{4})|\geqslant3|8-4|=12,当且仅当\alpha=\frac{\pi}{4}时取“=”.

**Theorem Sequence**:  
Ellipse_Equation_Standard_X, Ellipse_Tangent_Line, Basic_Inequality

---

## Problem Index: 5304
**ID**: 5305
**Text**:  
不论$a$为何值时，直线$(a-1) x-y+2 a+1=0$恒过定点$P$，则过$P$点的抛物线的标准方程为?

**Process**:  
因为不论a为何值时,直线(a-1)x-y+2a+1=0恒过定点P,则过点(x+2)a+(-x-y+1)=0故x=-2,y=3,因此过点p的抛物线的方程为x^{2}=\frac{4}{3}y或y^{2}=-\frac{9}{2}x

**Theorem Sequence**:  
Parabola_Equation_Standard_Right, Parabola_Directrix

---

## Problem Index: 5315
**ID**: 5316
**Text**:  
双曲线$\frac{x^{2}}{16}-\frac{y^{2}}{64}=1$上一点$P$到它的一个焦点的距离为$7$，则点$P$到另一个焦点的距离等于?

**Process**:  
双曲线\frac{x^{2}}{16}-\frac{y^{2}}{64}=1的a=4,b=8,c=\sqrt{16+64}=4\sqrt{5}设左右焦点为F_{1},F_{2},则由双曲线的定义,得|PF|-|PF_{2}|=2a=8,可设|PF|=7,则有|PF_{2}|=15或|PF_{2}|=-1(舍去)

**Theorem Sequence**:  
Hyperbola_Equation_Standard_X, Hyperbola_Definition

---

## Problem Index: 5342
**ID**: 5343
**Text**:  
已知双曲线$x^{2}-y^{2}=m$与椭圆$2 x^{2}+3 y^{2}=m+1$有相同的焦点，则实数$m$=?

**Process**:  
根据焦点相同,则焦距相等,建立方程求解[详解]由2x^{2}+3y^{2}=m+1可得\frac{x2}{2}+\frac{y^{2}}{\frac{m+1}{3}}=1,由x^{2}-y^{2}=m可得\frac{x^{2}}{m}-\frac{y^{2}}{m}=1所以焦点在x轴上,且\frac{m+1}{2}-\frac{m+1}{3}=m+m解得m=\frac{1}{11}

**Theorem Sequence**:  
Circle_Standard_Equation, Vector_Collinear_Condition

---

## Problem Index: 5367
**ID**: 5368
**Text**:  
双曲线$C$: $\frac{x^{2}}{a^{2}}-\frac{y^{2}}{b^{2}}=1(a>0, b>0)$的左、右焦点分别为$F_{1}$、$F_{2}$，过$F_{2}$的直线交曲线$C$右支于$P$、$Q$两点，且$P Q \perp P F_{1}$，若$3|P Q|=4|P F_{1}|$，则$C$的离心率等于?

**Process**:  
如图,设|PQ|=4t(t>0),由3|PQ|=4|PF_{1}|可得|PF_{1}|=3t由双曲线定义,有|PF_{1}|-|PF_{2}|=2a,所以|PF_{2}|=3t-2a,|QF_{2}|=|PQ|-|PF_{1}|=t+2a,又|QF_{1}|-|QF_{2}|=2a,所以|QF_{1}|=t+4a,因为PQ\botPF_{1},所以|PF_{1}|+|PF_{2}|^{2}=4c^{2},|PF_{1}|^{2}+|PQ|^{2}=|QF_{1}^{2}|即(3t)^{2}+(3t-2a)^{2}=4c^{2\textcircled{1}},(3t)^{2}+(4t)^{2}=(t+4a)^{2}\textcircled{2},由\textcircled{2}解得t=a,代入\textcircled{1},得(3a)^{2}+(3a-2a)^{2}=4c^{2},即10a^{2}=4c^{2}所以e=\frac{c}{a}=\sqrt{\frac{10}{4}}=\frac{\sqrt{10}}{2}

**Theorem Sequence**:  
Hyperbola_Equation_Standard_X, Hyperbola_Definition, Pythagorean_Theorem, Ellipse_Focal_Triangle_Perimeter, Triangle_Area_With_Sin, Eccentricity_Formula

---

## Problem Index: 5370
**ID**: 5371
**Text**:  
已知$F$是椭圆$\frac{x^{2}}{a^{2}}+\frac{y^{2}}{b^{2}}=1(a>b>0)$的右焦点，点$P$在椭圆上，且$P$到原点$O$的距离等于半焦距，$\triangle P O F$的面积为$6$，则$b$=?

**Process**:  
设P(x_{0},y_{0}),\because点P在椭圆上,\therefore\frac{x_{0}^{2}}{a^{2}}+\frac{y_{0}^{2}}{b^{2}}=1\textcircled{1}又\because点P到原点O的距离等于半焦距\therefore\sqrt{x_{0}^{2}+y_{0}^{2}}=c,即x_{0}^{2}+y_{0}^{2}=c^{2}\textcircled{2}\because\trianglePOF的面积为6.\therefore\frac{1}{2}\timesc\times|y_{0}|=6,可得|y_{0}|=\frac{12}{c}\textcircled{3}把\textcircled{3}代入\textcircled{2}得,x_{0}^{2}=c^{2}-\frac{144}{c^{2}}144a^{2}把\textcircled{3}代入\textcircled{1}得,x_{0}^{2}=a^{2}-\frac{144a^{2}}{b^{2}c^{2}}c^{2}-\frac{144}{c^{2}}=a^{2}-\frac{144a^{2}}{b^{2}c^{2}}故得b=2\sqrt{:}

**Theorem Sequence**:  
Ellipse_Equation_Standard_X, Ellipse_Definition, Triangle_Area_Formula, Eccentricity_Formula

---

## Problem Index: 5373
**ID**: 5374
**Text**:  
若双曲线$C$的标准方程为$\frac{x^{2}}{a^{2}}-\frac{y^{2}}{b^{2}}=1$, $P(\sqrt{2}, 1)$为$C$上一点，一个焦点到一条渐近线的距离为$2$，则双曲线的标准方程为?

**Process**:  
设双曲线的右焦点为(c,0),一条渐近线为bx-ay=0根据点到直线的距离公式\frac{|bc|}{\sqrt{a^{2}+b^{2}}}=b=2\frac{2}{2})^{2}-\frac{1^{2}}{b^{2}}=1\thereforea^{2}=\frac{8}{5},b=2,所以双曲线的标准方程为\frac{x^{2}}{8}-\frac{y^{2}}{4}=1

**Theorem Sequence**:  
Hyperbola_Equation_Standard_X, Hyperbola_Asymptote, Point_To_Line_Distance, Hyperbola_Parameter_Relation

---

## Problem Index: 5422
**ID**: 5423
**Text**:  
若双曲线$x^{2}-y^{2}=1$上的右支上一点$P(a, b)$到直线$y=x$的距离为$\sqrt{2}$，则$a+b$的值为?

**Process**:  
由点P(a,b)在双曲线上,则a^{2}-b^{2}=1,即(a+b)(a-b)=1,又点P到直线y=x的距离d=\frac{|a-b|}{\sqrt{2}}=\sqrt{2},所以|a-b|=2,又点P在右支上,则a>b,所以a-b=2,所以(a+b)\times2=1,所以a+b=\frac{1}{2}

**Theorem Sequence**:  
Hyperbola_Equation_Standard_X, Point_To_Line_Distance, Two_Points_Distance

---

## Problem Index: 5451
**ID**: 5452
**Text**:  
椭圆$\frac{x^{2}}{4}+\frac{y^{2}}{k}=1$的离心率为$\frac{2}{3}$，则实数$k$=?

**Process**:  
由题意可得\frac{b^{2}}{a^{2}}=\frac{5}{9},对椭圆的焦点位置进行分类讨论,可得出关于实数k的等式,由此可求得实数k的取值范围.作解】因为e^{2}=\frac{c^{2}}{a^{2}}=\frac{a^{2}-b^{2}}{a^{2}}=1-\frac{b^{2}}{a^{2}}=\frac{4}{9},可得\frac{b^{2}}{a^{2}}=\frac{5}{9}.若椭圆的焦点在x轴上,则\frac{b^{2}}{a^{2}}=\frac{k}{4}=\frac{5}{9},解得k=\frac{20}{9}若椭圆的焦点在y轴上,则\frac{b^{2}}{a^{2}}=\frac{4}{k}=\frac{5}{9},解得k=\frac{36}{5}综上所述,k=\frac{20}{9}或\frac{36}{5}

**Theorem Sequence**:  
Ellipse_Equation_Standard_X, Eccentricity_Formula

---

## Problem Index: 5458
**ID**: 5459
**Text**:  
抛物线$x^{2}=4 y$的弦$A B$过焦点$F$，且$A B$的长为$6$，则$A B$的中点$M$的纵坐标?

**Process**:  
由已知p=2,设A(x_{1},y_{1}),B(x_{2},y_{2}),则AB|=y_{1}+y_{2}+p=6,y_{1}+y_{2}=4,所以\frac{y_{1}+y_{2}}{2}=2

**Theorem Sequence**:  
Parabola_Equation_Standard_Right, Parabola_Definition, Parabola_Directrix, Vieta_Theorem_Sum

---

## Problem Index: 5463
**ID**: 5464
**Text**:  
已知点$P$为中心在坐标原点的椭圆$C$上的一点，且椭圆的右焦点为$F_{2}(\sqrt{5}, 0)$，线段$P F_{2}$的垂直平分线为$y=2 x$，则椭圆$C$的方程为?

**Process**:  
点P为中心在坐标原点的椭圆C上的一点,且椭圆的右焦点为F_{2}(\sqrt{5},0),可得c=\sqrt{5}与直线PF_{2}的垂直经过F_{2}的直线方程:y=-\frac{1}{2}(x-\sqrt{5}),x+2y-\sqrt{5}=0,F_{2}到垂直平分线为y=2x的距离为:\frac{2\sqrt{5}}{\sqrt{5}}=2,原点到直线x+2y-\sqrt{5}=0的距离为:可得a=2+1=3,所以b=2,则椭圆C的方程为\frac{x^{2}}{0}+\frac{y^{2}}{4}=1

**Theorem Sequence**:  
Ellipse_Equation_Standard_X, Vector_Collinear_Condition, Point_To_Line_Distance

---

## Problem Index: 5470
**ID**: 5471
**Text**:  
过$(3,-6)$且与双曲线$x^{2}-\frac{y^{2}}{2}=1$有相同渐近线的双曲线的标准方程为?

**Process**:  
\because与双曲线x^{2}-\frac{y^{2}}{2}=1有相同的渐近线,\therefore设双曲线方程为x^{2}-\frac{y^{2}}{2}=2(\lambda\neq0)将(3,-6)代入,可得3^{2}-\frac{(-6)^{2}}{2}=\lambda.\therefore\lambda=-9,\therefore所求双曲线的标准方程是\frac{y^{2}}{18}-\frac{x^{2}}{9}=1.

**Theorem Sequence**:  
Hyperbola_Equation_Standard_X, Hyperbola_Asymptote

---

## Problem Index: 5473
**ID**: 5474
**Text**:  
已知$A(-1,0)$, $B(2,0)$, 直线$l$: $x+2 y+a=0$上存在点$M$, 使得$M A^{2}+2 M B^{2}=10$, 则实数$a$的取值范围为?

**Process**:  
设M(x,y),由MA^{2}+2MB^{2}=10得(x+1)^{2}+y^{2}+2[(x-2)^{2}+y^{2}]=10整理得3x^{2}-6x+3y^{2}=1,由题意可得直线l:x+2y+a=0与3x^{2}-6x+3y^{2}=1有交点,联立得15x2-(24-6a)x+3a^{2}-4=0\therefore\Delta=(24-6a)^{2}-60(3a^{2}-4)\geqslant0整理得3a^{2}+6a-17\leqslant0解得-1-\frac{\sqrt[2]{15}}{3}\leqslant\frac{a}{5}\leqslant-1+\frac{2\sqrt{15}}{3}

**Theorem Sequence**:  
Circle_Standard_Equation, Vector_Collinear_Condition, Discriminant_Delta, Quadratic_Function_Maximum

---

## Problem Index: 5481
**ID**: 5482
**Text**:  
已知$F_{1}(-1,0)$, $F_{2}(1,0)$是椭圆$C$的两个焦点，过$F_{2}$且垂直于$x$轴的直线交$C$于$A$、$B$两点且$|A B|=3$, 则$C$的方程为?

**Process**:  
依题意设椭圆C的方程为\frac{x^{2}}{a^{2}}+\frac{y^{2}}{b^{2}}=1(a>b>0),由条件可得A(1,\frac{b^{2}}{a}),B(1,-\frac{b^{2}}{a}),因|AB|=\frac{b^{2}}{a}-(-\frac{b^{2}}{a})=\frac{2b^{2}}{a}=3,即2b^{2}=3a,所以\begin{cases}2b^{2}=3a,\\a^{2}-b^{2}=c^{2}=1,\end{cases}解得\begin{cases}a=2,\\b=\sqrt{3},\end{cases}所以椭圆C的方程为\frac{x^{2}}{4}+\frac{y^{2}}{3}=1.故选C.

**Theorem Sequence**:  
Ellipse_Equation_Standard_X, Ellipse_Latus_Rectum, Eccentricity_Formula

---

## Problem Index: 5506
**ID**: 5507
**Text**:  
过双曲线$M$: $x^{2}-\frac{y^{2}}{b^{2}}=1$的左顶点$A$作斜率为$1$的直线$l$，若$l$与双曲线$M$的两条渐近线分别相交于$B$、$C$，且$|A B|=|B C|$，则双曲线$M$的离心率是?

**Process**:  
过双曲线M:x^{2}-\frac{y^{2}}{b^{2}}=1的左顶点A(-1,0)作斜率为1的直线l:y=x+1,若l与双曲线M的两条渐近线x^{2}-\frac{y^{2}}{b^{2}}=0分别相交于点B(x_{1},y_{1}),c(x_{2},y_{2})联立方程组\begin{cases}x^{2}-\frac{y^{2}}{b^{2}}=0\\y=x+1\end{cases}代入消元得(b^{2}-1)x^{2}-2x-1=0,\begin{cases}x_{1}+x_{2}=\frac{2}{b^{2}-1}\\\end{cases}_{2}=-2x_{1}x.|x_{1}x_{2}=\frac{1}{1-b^{2}}|=|BC|,则B为AC中点,2x_{1}=-1+代入解得\begin{cases}x_{1}=-\frac{1}{4}\\x_{2}=\frac{1}{3}\end{cases}\thereforeb^{2}=9,双曲线M的离心率e=\frac{c}{a}=\sqrt{10}

**Theorem Sequence**:  
Hyperbola_Equation_Standard_X, Hyperbola_Asymptote, Point_Difference_Method_Hyperbola, Vieta_Theorem_Sum, Vieta_Theorem_Product, Eccentricity_Formula

---

## Problem Index: 5524
**ID**: 5525
**Text**:  
若双曲线$\frac{x^{2}}{a^{2}}-\frac{y^{2}}{b^{2}}=1  (a>0 , b>0)$的一个焦点到一条渐近线的距离等于焦距的$\frac{1}{4}$，则该双曲线的离心率是?

**Process**:  
点(c,0)到直线y=\frac{b}{a}x的距离为:d=\frac{|bc|}{\sqrt{a^{2}+b^{2}}}=\frac{bc}{c}=b=\frac{1}{4}\times2c=\frac{c}{2},所以4b^{2}=c^{2},4(c^{2}-a^{2})=c^{2},\frac{c^{2}}{a^{2}}=\frac{4}{3},所以\frac{c}{a}=\frac{2\sqrt{3}}{3}.

**Theorem Sequence**:  
Hyperbola_Equation_Standard_X, Hyperbola_Asymptote, Hyperbola_Focus_To_Asymptote_Distance

---

## Problem Index: 5528
**ID**: 5529
**Text**:  
倾斜角为$\frac{\pi}{4}$的直线过抛物线$y^{2}=2 x$的焦点$F$，交抛物线于$A$、$B$两点，则$|A B|$=?

**Process**:  
由抛物线y^{2}=2x得焦点F(\frac{1}{2},0),再求得直线的方程,将直线的方程与抛物线的方程联立得出交点的坐标的关系x_{1}+x_{2}=3,再由抛物线的定义可求得线段的长由抛物线y^{2}=2x得焦点F(\frac{1}{2},0),\therefore倾斜角为\frac{\pi}{4}的直线过焦点F的方程为:y=x-\frac{1}{2},与抛物线y^{2}=2x联立得x^{2}-3x+\frac{1}{4}=0,令A(x_{1},y_{1}),B(x_{2},y_{2}),则x_{1}+x_{2}=3,由抛物线的定义得|AF|=x_{1}+\frac{1}{2},|BF|=x_{2}+\frac{1}{2},\therefore|_{AB}|=x_{1}+\frac{1}{2}+x_{2}+\frac{1}{2}=x_{1}+x_{2}+1=4,

**Theorem Sequence**:  
Parabola_Equation_Standard_Right, Parabola_Focal_Radius, Substitution_x_equals_my_plus_n, Vieta_Theorem_Sum, Chord_Length_Formula_With_K

---

## Problem Index: 5535
**ID**: 5536
**Text**:  
已知点$P(2,4)$在抛物线$C$: $y^{2}=2 p x$上，过其焦点$F$且倾斜角为$45^{\circ}$的直线$l$与$C$交于$M$、$N$两点，则$\triangle P M N$的面积为?

**Process**:  
依题意求出抛物线方程,即可求出焦点坐标,从而求出直线l的方程,联立直线与抛物线方程,利用抛物线焦点弦公式求出弦MN,再利用点到直线的距离求出点P(2,4)到直线l的距离,从而求出三角形的面积;因为P(2,4)在抛物线C:y^{2}=2px,所以4^{2}=2p\times2,所以p=4,即抛物线方程为y^{2}=8x焦点F(2,0),直线l的倾斜角为45^{\circ},所以直线l的方程为y=x-2联立直线与抛物线方程得\begin{cases}y^{2}=8x\\y=x-2\end{cases}消去y得x^{2}-12x+4=0,设M(x_{1},y_{1}),N(x_{2},y_{2})所以x_{1}+x_{2}=12,所以MN=x_{1}+x_{2}+p=16,点P(2,4)到直线l的距离d=\frac{4}{\sqrt{1^{2}+(}}\frac{4}{+(-1)^{2}}=2\sqrt{2}所以S_{\DeltaPMN}=\frac{1}{2}MN\cdotd=\frac{1}{2}\times16\times2\sqrt{2}=16\sqrt{2}

**Theorem Sequence**:  
Parabola_Equation_Standard_Right, Parabola_Definition, Parabola_Focal_Radius, Parabola_Directrix, Point_Difference_Method_Hyperbola, Triangle_Midline_Theorem, Point_To_Line_Distance, Triangle_Area_Formula

---

## Problem Index: 5538
**ID**: 5539
**Text**:  
已知$F$是双曲线$C$: $\frac{x^{2}}{a^{2}}-\frac{y^{2}}{b^{2}}=1(a>0, b>0)$的右焦点，点$M$在$C$的右支上，坐标原点为$O$，若$|F M|=2|O F|$，且$\angle O F M=120^{\circ}$，则双曲线$C$的离心率为?

**Process**:  
设双曲线C的左焦点为F_{1},由题意可得|MF|=|F_{1}F|=2c,\angleMFF_{1}=120^{\circ},由余弦定理有|MF_{1}^{2}|=|MF|^{2}+|F_{1}F|^{2}-2|MF|\cdot|F_{1}F|\cos\angleMFF_{1}=4c^{2}+4c^{2}-2\cdot4c^{2}\cdot(-\frac{1}{2})=12c^{2}即有|MF_{1}|=2\sqrt{3}c,由双曲线的定义可得|MF_{1}|-|MF|=2a,即为2\sqrt{3}c-2c=2a,即有_{c}=\frac{\sqrt{3}+1}{2}a'所以双曲线C的离心率为_{e}=\frac{c}{a}=\frac{\sqrt{3}+1}{2}

**Theorem Sequence**:  
Hyperbola_Equation_Standard_X, Hyperbola_Definition, Pythagorean_Theorem, Triangle_Area_With_Sin, Eccentricity_Formula

---

## Problem Index: 5547
**ID**: 5548
**Text**:  
已知椭圆$C$: $\frac{x^{2}}{a^{2}}+\frac{y^{2}}{b^{2}}=1(a>b>0)$的右焦点为$F$，直线$y=\frac{b}{3}$与$C$交于$A$、$B$两点，若以$A B$为直径的圆经过点$F$，则$C$的离心率为?

**Process**:  
设F(c,0)(c>0),将y=\frac{b}{3}代入椭圆方程得x=\pm\frac{2\sqrt{2}}{3}a'不妨设A(-\frac{2\sqrt{2}a}{3},\frac{b}{3})B(\frac{2\sqrt{2}a}{3},\frac{b}{3})\overrightarrow{AF}=(c+\frac{2\sqrt{2}a}{3},-\frac{b}{3}),\overrightarrow{BF}=(c-\frac{2\sqrt{2}a}{3},-\frac{b}{3})因为以AB为直径的圆经过点F,所\overrightarrow{AF}\cdot\overrightarrow{BF}=0即(c+\frac{2\sqrt{2}a}{3})(c-\frac{2\sqrt{2}a}{3})+\frac{b^{2}}{9}=0'整理得c^{2}-\frac{8}{9}a^{2}+\frac{b^{2}}{9}=0,

**Theorem Sequence**:  
Ellipse_Equation_Standard_X, Vector_Collinear_Condition, Ellipse_Parameter_Relation

---

## Problem Index: 5552
**ID**: 5553
**Text**:  
设$F_{1}$、$F_{2}$是双曲线$C$: $\frac{x^{2}}{a^{2}}-\frac{y^{2}}{b^{2}}=1(a>0, b>0)$的左、右焦点，$P$是双曲线$C$右支上一点，若$|P F_{1}|+|P F_{2}|=4 a $, $\angle F_{1} P F_{2}=60^{\circ}$，则双曲线$C$的渐近线方程是?

**Process**:  
由双曲线定义可知|PF_{1}|-|PF_{2}|=2a,且|PF_{1}|+|PF_{2}|=4a那么可以求出|PF_{1}|=3a,|PF_{2}|=a\trianglePF_{1}F_{2}中,由余弦定理可得\cos60^{\circ}=\frac{|PF_{1}^{2}+|PF_{2}^{2}-|F_{1}F_{2}|}{2|PF_{1}|\cdot|PF_{2}|}即\frac{1}{2}=\frac{(3a)^{2}+a^{2}-4c^{2}}{2\times3a\timesa}即3a^{2}=10a^{2}-4c^{2},4c^{2}=7a^{2},且a^{2}+b^{2}=c^{2}那么\frac{b^{2}}{a^{2}}=\frac{3}{4},故渐近线方程为y=\pm\frac{\sqrt{3}}{2}x,即\sqrt{3}x\pm2y=0.

**Theorem Sequence**:  
Hyperbola_Equation_Standard_X, Hyperbola_Definition, Pythagorean_Theorem, Triangle_Area_With_Sin, Hyperbola_Asymptote

---

## Problem Index: 5574
**ID**: 5575
**Text**:  
$P$是抛物线$x^{2}=4 y$上一点，抛物线的焦点为$F$，且$|P F|=5$，则$P$点的纵坐标为?

**Process**:  
抛物线x^{2}=4y的准线方程为y=-1,焦点的坐标为(0,1),设P点的纵坐标为(x,y)则\begin{cases}x^{2}=4y\\y+1=5\end{cases}\"\begin{cases}x=\pm4\\y=4\end{cases}\"所以答案应填4.

**Theorem Sequence**:  
Parabola_Equation_Standard_Right, Parabola_Definition, Parabola_Directrix

---

## Problem Index: 5579
**ID**: 5580
**Text**:  
已知$F_{1}$、$F_{2}$是椭圆$C_{1}$: $\frac{x^{2}}{4}+y^{2}=1$与双曲线$C_{2}$的公共焦点，$A$是$C_{1}$、$C_{2}$，在第二象限的公共点，若$\angle F_{1} A F_{2}=\frac{\pi}{3}$，则$C_{2}$的离心率为?

**Process**:  
由题意首先求得双曲线中c的值,然后结合椭圆的定义和余弦定理可求得a的值,最后利用离心率的定义即可求得双曲线的离心率.羊解】设C_{2}\frac{x^{2}}{a_{1}^{2}}-\frac{y^{2}}{b_{1}^{2}}=1(a_{1}b_{1}>0),由题意知c=c_{1}=\sqrt{3}由椭圆的定义得AF_{1}+AF_{2}=2a=4,在\triangleF_{1}AF_{2}中,由余弦定理:(2c)^{2}=12=AF_{1}^{2}+AF_{2}^{2}-2AF_{1}\cdotAF_{2}\cos\frac{\pi}{3}=(AF_{1}+AF_{2})^{2}-3AF_{1}\cdotAF_{2}=16-3AF_{1}\cdotAF_{2}解得AF_{1}\cdotAF_{2}=\frac{4}{3},\therefore(AF_{1}-AF_{2})^{2}=(AF_{1}+AF_{2})^{2}-4AF_{1}\cdotAF_{2}=\frac{32}{3},假设F_{1}F_{2}分别为左、右焦点,AF_{2}>AF_{1},则AF_{2}-AF_{1}=\frac{4}{3}\sqrt{6}=2a_{1},解得a_{1}=\frac{2}{3}\sqrt{6}所以C_{2}的离心率e=\frac{c_{1}}{a_{1}}=\frac{3\sqrt{2}}{4}睛】双曲线的离心率是双曲线最重要的几何性质,求双曲线的离心率(或离心率的取值范围),常见有两种方法:\textcircled{1}求出a,c,代入公式e=\frac{c}{a}\textcircled{2}只需要根据一个条件得到关于a,b,c的齐次式,结合b^{2}=c^{2}-a^{2}转化为a,c的齐次式,然后等式(不等式)两边分别除以a或a^{2}转化为关于e的方程(不等式),解方程(不等式)即可得e(e的取值范围).

**Theorem Sequence**:  
Ellipse_Equation_Standard_X, Hyperbola_Definition, Ellipse_Definition, Eccentricity_Formula, Ellipse_Focal_Triangle_Perimeter, Triangle_Area_With_Sin, Triangle_Area_Formula, Basic_Inequality

---

## Problem Index: 5588
**ID**: 5589
**Text**:  
顶点在原点，对称轴为坐标轴，且过点$P(-4,-2)$的抛物线的标准方程是?

**Process**:  
根据P(-4,-2)的位置,分别考虑抛物线的焦点在x轴负半轴、y轴负半轴,由此计算出抛物线方程.羊解】当抛物线的焦点在x轴负半轴时,设y^{2}=-2px(p>0),代入点P(-4,-2)所以4=8p,所以p=\frac{1}{2},所以y^{2}=-x;当抛物线的焦点在y轴负半轴时,设x^{2}=-2py(p>0),代入点P(所以16=4p,所以p=4,所以x^{2}=-8y

**Theorem Sequence**:  
Parabola_Equation_Standard_Right, Parabola_Equation_Standard_Up

---

## Problem Index: 5589
**ID**: 5590
**Text**:  
中心在原点的双曲线，其渐近线方程是$y=\pm \sqrt{3} x$，且过点$(\sqrt{2}, \sqrt{3})$，则双曲线的标准方程为?

**Process**:  
因为该双曲线的渐近线方程为y=\pm\sqrt{3}x,所以设该双曲线方程为3x^{2}-y^{2}=\lambda(\lambda\neq0),将点(\sqrt{2},\sqrt{3})代入得:6-3=\lambda\Rightarrow\lambda=3,即该双曲线方程为x^{2}-\frac{y^{2}}{3}=1

**Theorem Sequence**:  
Hyperbola_Equation_Standard_X, Hyperbola_Asymptote

---

## Problem Index: 5605
**ID**: 5606
**Text**:  
抛物线$x^{2}=4 y$上的点到其焦点的最短距离为?

**Process**:  
抛物线x^{2}=4y的焦点F(0,1),设点P(t,\frac{t^{2}}{4})为抛物线x^{2}=4y上任意一点,所以当t=0,即点P为抛物线顶点时,|PF|取最小值1.

**Theorem Sequence**:  
Parabola_Equation_Standard_Right, Parabola_Definition, Parabola_Directrix

---

## Problem Index: 5610
**ID**: 5611
**Text**:  
已知抛物线$C$: $4 x^{2}+m y=0$恰好经过圆$M$:$(x-1)^{2}+(y-2)^{2}=1$的圆心，则抛物线$C$的焦点坐标为?

**Process**:  
由题可得圆M的圆心为(1,2)代入4x^{2}+my=0得m=-2,将抛物线C的方程化为标准方程得x^{2}=\frac{1}{2}y故焦点坐标为(0,\frac{1}{8})

**Theorem Sequence**:  
Parabola_Equation_Standard_Right, Ellipse_Tangent_Line, Circle_Standard_Equation

---

## Problem Index: 5613
**ID**: 5614
**Text**:  
已知椭圆$C$: $\frac{x^{2}}{a^{2}}+\frac{y^{2}}{b^{2}}=1(a>b>0)$的右焦点为$F$，过点$F$作圆$x^{2}+y^{2}=b^{2}$的切线，若两条切线互相垂直，则$C$的离心率为?

**Process**:  
由题意,椭圆\frac{x^{2}}{a^{2}}+\frac{y^{2}}{b^{2}}=1(a>b>0),可得右焦点为F(c,0)因为过点F(c,0)作圆x^{2}+y^{2}=b^{2}的切线,可得\sqrt{2}b=c,则2b^{2}=c^{2}即2(a^{2}-c^{2})=c^{2},即2a^{2}=3c^{2},可得\frac{c^{2}}{a^{2}}=\frac{2}{3},所以e=\frac{c}{a}=\frac{\sqrt{6}}{3}

**Theorem Sequence**:  
Ellipse_Equation_Standard_X, Circle_Standard_Equation, Point_Difference_Method_Hyperbola, Point_To_Line_Distance, Eccentricity_Formula

---

## Problem Index: 5625
**ID**: 5626
**Text**:  
抛物线$y^{2}=4 x$的焦点为$F$，点$P(x, y)$为该抛物线上的动点，又点$A(-1,0)$，则$\frac{|P F|}{|P A|}$的最小值是?

**Process**:  
根据抛物线的定义,可求得|PF|=x+1,又|PA所以\frac{|PF|}{|PA|}=\frac{x+1}{\sqrt{y^{2}+(x+1)^{2}}}\textcircled{1}.因为y^{2}=4x,令\frac{2}{x+1}=t,则\textcircled{1}式可化简为\overline{\sqrt{1}}\underline{1}t^{2}+2t+1=其中t\in(0,2],即可求得-\sqrt{3}最小值为\frac{\sqrt{2}}{2},所以\frac{|PF|}{|PA|}的最小值为\frac{\sqrt{2}}{2}

**Theorem Sequence**:  
Parabola_Equation_Standard_Right, Parabola_Definition, Parabola_Focal_Radius, Basic_Inequality

---

## Problem Index: 5627
**ID**: 5628
**Text**:  
已知双曲线$C$: $\frac{x^{2}}{a^{2}}-\frac{y^{2}}{b^{2}}=1$的左, 右焦点分别为$F_{1}$、$F_{2}$，点$P$在双曲线上，$\Delta P F_{1} F_{2}$的内切圆圆心为$I$，且满足$\overrightarrow{P F_{1}} \cdot \overrightarrow{P F_{2}}=\overrightarrow{P I} \cdot \overrightarrow{P F_{1}}$,$P F_{2} \perp F_{1} F_{2}$ ,则双曲线$C$的离心率为?

**Process**:  
由\overrightarrow{PF}\cdot\overrightarrow{PF_{2}}=\overrightarrow{PI}\cdot\overrightarrow{PF}_{1},即\overrightarrow{PF_{1}}\cdot\overrightarrow{PF_{2}}-\overrightarrow{PI}\cdot\overrightarrow{PF_{1}}=0,即\overrightarrow{PF_{1}}\cdot(\overrightarrow{PF_{2}}-\overrightarrow{PI})=\overrightarrow{PF}\cdot\overrightarrow{IF_{2}}=0所以PF_{1}\botIF_{2},又IF_{2}是\anglePF_{2}F_{1}的角平分线,所以F_{1}F_{2}=PF_{2},即2c=\frac{b^{2}}{a},即2ac=b^{2},所以c^{2}-a^{2}=2ac,从而e^{2}-2e-1=0,解得e=\sqrt{2}+1或e=-\sqrt{2}+1(舍去)

**Theorem Sequence**:  
Ellipse_Definition, Ellipse_Focal_Triangle_Perimeter, Eccentricity_Formula

---

## Problem Index: 5640
**ID**: 5641
**Text**:  
过抛物线$x^{2}=8 y$的焦点$F$作直线交抛物线于$A(x_{1}, y_{1})$ , $B(x_{2}, y_{2})$两点，若$y_{1}+y_{2}=8$，则线段$A B$的长为?

**Process**:  
由抛物线定义得|AF|=y_{1}+\frac{p}{2},|BF|=y_{2}+\frac{p}{2}所以|AB|=|AF|+|BF|=y+y+p=12.

**Theorem Sequence**:  
Parabola_Equation_Standard_Right, Parabola_Definition, Parabola_Focal_Radius, Vieta_Theorem_Sum

---

## Problem Index: 5655
**ID**: 5656
**Text**:  
抛物线$x^{2}=\frac{1}{4} y$的准线方程是?

**Process**:  
本题考查根据抛物线的方程求准线方程,判定开口方向,求得p的值,然后根据公式得出准线方程抛物线x^{2}=\frac{1}{4}y中,y\geqslant0,是一原点为顶点,开口方向向上的抛物线,2p=\frac{1}{4}\therefore抛物线的准线方程为y=-\frac{1}{16},

**Theorem Sequence**:  
Parabola_Equation_Standard_Right, Parabola_Directrix

---

## Problem Index: 5697
**ID**: 5698
**Text**:  
已知$P$为椭圆$4 x^{2}+y^{2}=4$上的点，$O$为原点，则$|O P|$的取值范围是?

**Process**:  
\because椭圆方程为4x^{2}+y^{2}=4\therefore椭圆的标准方程为x^{2}+\frac{y^{2}}{4}=1\thereforea^{2}=4,b^{2}=1\becauseP为椭圆上的点,O为原点\therefore|OP|的取值范围是1,2

**Theorem Sequence**:  
Ellipse_Equation_Standard_X

---

## Problem Index: 5699
**ID**: 5700
**Text**:  
已知点$M$是椭圆$\frac{x^{2}}{4}+\frac{y^{2}}{9}=1$上的动点，作$M D \perp x$轴. 垂足为$D$. 点$P$在线段$M D$上，且$\frac{|D M|}{|D P|}=\frac{3}{2}$，当点$M$运动时，点$P$的轨迹方程?

**Process**:  
设P(x,y),M(x_{0},y_{0}),\therefore\frac{x_{0}^{2}}{4}+\frac{y_{0}^{2}}{9}=1^{;}\becauseMD\botx轴,P在MD上且\frac{|DM|}{|DP|}=\frac{3}{2},\therefore\begin{cases}x=x_{0}\\\frac{y_{0}}{v}=\frac{3}{2}\end{cases}\begin{cases}x_{0}=x\\y_{0}=\frac{3}{2}y\end{cases}\therefore\frac{x^{2}}{4}+\frac{y^{2}}{4}=1,即点P的轨迹方程为x^{2}+y^{2}=4.

**Theorem Sequence**:  
Ellipse_Equation_Standard_Y, Vector_Collinear_Condition

---

## Problem Index: 5701
**ID**: 5702
**Text**:  
已知圆$M$: $x^{2}+(y-1)^{2}=1$，圆$N$: $x^{2}+(y+1)^{2}=1$，直线$l_{1}$ , $l_{2}$分别过圆心$M$、$N$且$l_{1}$与圆$M$相交于$A$ , $B$ , $l_{2}$与圆$N$相交于$C$、$D$、$P$是椭圆$\frac{x^{2}}{3}+\frac{y^{2}}{4}=1$上的任意一动点，则$\overrightarrow{P A} \cdot \overrightarrow{P B}+\overrightarrow{P C} \cdot \overrightarrow{P D}$的最小值为?

**Process**:  
易知点M、N为椭圆的两个焦点,所以|M|+|PN|=4.同时,结合图像已知,MA+MB=0,MA\cdotMB=-1'NC+N=0,NC\cdotN=-1'所以\overset\rightarrowPA_{=}(PM+\frac{\overset\rightarrowPC\cdot}{P_{D}}+MA)\cdot(PM+MB)+(\overrightarrow{PN}+\overrightarrow{NC})\cdot(\overrightarrow{PN}+\overrightarrow{ND})=\frac{\sqrt{m}}{PM^{2}}+\frac{\sqrt[m]{A}}{PM}.(MA+MB)+MA\cdotMB+PN^{2}+PN.(N'C+MD+N^{x}\cdotM\frac{\pi}{D}=|PM|^{2}+0-1+|PN|^{2}+0-1=|PM|^{2}+|PN^{2}|-2又因(\frac{x+y}{2})^{2}\leqslant\frac{x^{2}+y^{2}}{2},所以|\overrightarrow{PM}|^{2}+|\overrightarrow{PN}|^{2}\geqslant\frac{|PM|+|PN|^{2}}{2}=8'M^{2}+|NN^{2}-2\geqslant\frac{(|M|+||N|)^{2}}{2}-2=6'故\overrightarrow{PA}\cdot\overrightarrow{PB}+\overrightarrow{PC}\cdot\overrightarrow{PD}\geqslant6因此\frac{\sqrt{1}}{PA}\cdot\overrightarrow{PB}+\overrightarrow{PC}\cdot\overrightarrow{PD}的最小值为6.

**Theorem Sequence**:  
Ellipse_Equation_Standard_X, Circle_Standard_Equation, Vector_Collinear_Condition, Basic_Inequality

---

## Problem Index: 5763
**ID**: 5764
**Text**:  
过双曲线$\frac{x^{2}}{a^{2}}-\frac{y^{2}}{b^{2}}=1$的一个焦点$F$作一条渐近线的垂线，若垂足恰在线段$O F$($O$为原点) 的垂直平分线上，则双曲线的离心率为?

**Process**:  
设垂足为D,根据双曲线方程可知其中一个渐近线为y=”b″ax,焦点为F(\sqrt{a^{2}+b^{2}},0)所以D点坐标(\underline{\sqrt{a^{2+b^{2}}},\frac{b\sqrt{a^{2}+b^{2}}}{2}\thereforekDF=\"=-b/\"a\becauseOD\botDF\thereforekDF\cdotkOD=-1\thereforeb/a=\"a\"/b,即a=b\thereforee=\"c\"/a=\frac{\sqrt{a^{2}+b^{2}}}{}=

**Theorem Sequence**:  
Hyperbola_Equation_Standard_X, Hyperbola_Asymptote, Vector_Collinear_Condition, Eccentricity_Formula

---

## Problem Index: 5776
**ID**: 5777
**Text**:  
已知点$P$是椭圆$C$: $\frac{x^{2}}{9}+y^{2}=1$上的一个动点，点$Q$是圆$E$: $x^{2}+(y-4)^{2}=3$上的一个动点，则$|PQ|$的最大值是?

**Process**:  
由圆E:x^{2}+(y-4)^{2}=3可得圆心为E(0,4),又点Q在圆E上\therefore|PQ||EP|+|EQ|=|EP|+\sqrt{3}(当且仅当直线PQ过点E时取等号)设P(x_{1},y_{1})是椭圆C上的任意一点,则\frac{x^{2}}{9}+y_{1}^{2}=1'即x_{1}^{2}=9-9y_{1}^{2}.\becauseEP|^{2}=x_{1}^{2}+(y_{1}-4)^{2}=9-9y_{1}^{2}+(y_{1}-4)^{2}=-8(y_{1}+\frac{1}{2})^{2}+27\becausey_{1}\in[-1,1],\therefore当y_{1}=-\frac{1}{2}时,|EP|^{2}取得最大值27,即PQ|\leqslant3\sqrt{3}+\sqrt{3}=4\sqrt{3}\because|PQ|的最大值为4\sqrt{3}

**Theorem Sequence**:  
Ellipse_Equation_Standard_X, Circle_Standard_Equation, Two_Points_Distance

---

## Problem Index: 5842
**ID**: 5843
**Text**:  
椭圆$\frac{x^{2}}{6}+\frac{y^{2}}{2}=1$与双曲线$\frac{x^{2}}{3}-\frac{y^{2}}{b^{2}}=1$有公共的焦点$F_{1}$、$F_{2}$，则双曲线的渐近线方程为?

**Process**:  
由题意可得:焦点坐标为(\pm2,0),所以b^{2}+3=4\Rightarrowb^{2}=1,所以双曲线的渐近线方程为y=\pm\frac{\sqrt{3}}{3}x

**Theorem Sequence**:  
Hyperbola_Equation_Standard_X, Hyperbola_Asymptote

---

## Problem Index: 5843
**ID**: 5844
**Text**:  
设抛物线$y^{2}=2 p x(p>0)$的焦点为$F$，准线为$l$，过抛物线上点$A(3, y_{0})$作$l$的垂线，垂足为$B$. 设$C(\frac{7}{2} p, 0)$,$A F$与$B C$相交于点$E$若$|F E|=2|A E|$，则$p$的值为?

**Process**:  
由题意可得:AB//CF,则\triangleABE\sim\triangleFCE,结合|FE|=2|AE|可知:\frac{|AB|}{|CF|}=\frac{|AE|}{|FE|}=\frac{1}{2}由题意可知:|AB|=3+\frac{p}{2},|CF|=\frac{7}{2}p-\frac{p}{2}=3p据此有:\frac{3+\frac{p}{2}}{3p}=\frac{1}{2},求解关于实数p的方程可得:p=3

**Theorem Sequence**:  
Parabola_Equation_Standard_Right, Parabola_Directrix, Triangle_Midline_Theorem

---

## Problem Index: 5844
**ID**: 5845
**Text**:  
已知$F_{1}$、$F_{2}$分别是双曲线$C$: $\frac{x^{2}}{a^{2}}-\frac{y^{2}}{b^{2}}=1(a>0, b>0)$的左、右焦点，以$F_{1} F_{2}$为直径的圆与双曲线的渐近线的一个公共点为$P$，若$|P F_{1}|=2|P F_{2}|$，则双曲线的离心率为?

**Process**:  
\because以F_{1}F_{2}为直径的圆的圆心是(0,0),半径为:c;故圆的标准方程为:x^{2}+y^{2}=c^{2}又\because双曲线的其中一条渐近线方程为:y=\frac{b}{a}x不妨设P在第一象限联立\begin{cases}y=\frac{b}{a}x\\x^{2}+y^{2}=c^{2}\end{cases}可得:\begin{cases}x=a\\y=b\end{cases}\becauseF_{1}(-c,0),F_{2}(c,0)根据两点间距离公式可得:故:\sqrt{(a+c)^{2}+b^{2}}=2\sqrt{(a-c)^{2}+b^{2}}+c^{2+b^{2}}c_{n}=2\sqrt{2c^{2}-2ac}\cdot3c=5a,即\frac{c}{a}=\frac{5}{2}\thereforee=\frac{5}{3}双曲线的离心率为:\frac{5}{3}

**Theorem Sequence**:  
Hyperbola_Equation_Standard_X, Hyperbola_Asymptote, Vector_Collinear_Condition, Eccentricity_Formula

---

## Problem Index: 5863
**ID**: 5864
**Text**:  
方程$x^{2}+(k-1) y^{2}=k+1$表示焦点在$x$轴上的双曲线，则实数$k$的取值范围是?

**Process**:  
将双曲线方程化为标准方程,再利用方程x^{2}+(k-1)y^{2}=k+1表示焦点在x轴上的双曲线,构建不等式组,从而可求实数k的取值范围双曲线方程可化为:\frac{x^{2}}{k+1}-\frac{y^{2}}{\frac{k+1}{1-k}}=1\because方程x^{2}+(k\cdot1)y^{2}=k+1表示焦点在x轴上的双曲线\because\begin{cases}k+1>0\\\frac{k+1}{1-k}>0\end{cases}1<k<1故实数k的取值范围是

**Theorem Sequence**:  
Hyperbola_Equation_Standard_X

---

## Problem Index: 5883
**ID**: 5884
**Text**:  
已知$A B$是过抛物线$y^{2}=4 x$焦点$F$的弦，$P$为该抛物线准线上的动点，则$\overrightarrow{P A} \cdot \overrightarrow{P B}$的最小值为?

**Process**:  
由抛物线y^{2}=4x的焦点为F(1,0),\therefore直线AB的方程可设为x=ty+1,代入抛物线方程得y2-4ty-4=0,设A(x_{1},y_{1},B(x_{2},y_{2}),则y_{1}+y_{2}=4t,y_{1}y_{2}=-4,又P为该抛物线准线上的动点,可设P(-1,m),则\overrightarrow{PA}=(x_{1}+1,y_{1}-m)=(ty_{1}+2,y_{1}-m)\overrightarrow{PB}=(x_{2}+1,y_{2}-m)=(ty_{2}+2,y_{2}-m)\therefore\overrightarrow{PA}\cdot\overrightarrow{PB}=(ty_{1}+2)(ty_{2}+2)+(y_{1}-m)(y_{2}-=(t^{2}+1)y,y_{2}+(2t-m)(y_{1}+y_{2})+4+m^{2}=(2t-m)^{2}\geqslant0

**Theorem Sequence**:  
Parabola_Equation_Standard_Right, Substitution_x_equals_my_plus_n, Vieta_Theorem_Sum, Vieta_Theorem_Product, Vector_Collinear_Condition

---

## Problem Index: 5901
**ID**: 5902
**Text**:  
顶点在原点，且过点$(-4,4)$的抛物线的标准方程是?

**Process**:  
当抛物线开口向上时,设抛物线方程为x^{2}=2py,(p>0),将点(-4,4)代入得2p=4所以抛物线方程为x^{2}=4y;当抛物线开口向左时,设抛物线方程为y^{2}=2px,(p>0),将点(-4,4)代入得2p=-4,所以抛物线方程为y^{2}=-4x.综上可得所求抛物线方程为y^{2}=-4x或x^{2}=4v.老占.抛物线方程

**Theorem Sequence**:  
Parabola_Equation_Standard_Right, Parabola_Equation_Standard_Up

---

## Problem Index: 5917
**ID**: 5918
**Text**:  
设双曲线$\frac{x^{2}}{a^{2}}-\frac{y^{2}}{a+1}=1$的两个焦点为$F_{1}$、$F_{2}$，点$P$在双曲线上，若$P F_{1} \perp P F_{2}$，则点$P$到坐标原点$O$的距离的最小值为?

**Process**:  
利用已知条件PF_{1}\botPF_{2},点P到坐标原点O的距离为c,转化求解c的最小值即可.[详解]双曲线\frac{x2}{a^{2}}-\frac{y^{2}}{a+1}=1的两个焦点为F_{1},F_{2},点P在双曲线上,若PF_{1}\botPF_{2}则点P到坐标原点O的距离为c,所以c=\sqrt{a^{2}+a+1}=\sqrt{(a+\frac{1}{2})^{2}+\frac{3}{4}}\geqslant\frac{\sqrt{3}}{2},当且仅当a=-\frac{1}{2}时,取得最小值:\frac{\sqrt{3}}{2}

**Theorem Sequence**:  
Hyperbola_Equation_Standard_X, Hyperbola_Parameter_Relation, Basic_Inequality

---

## Problem Index: 5921
**ID**: 5922
**Text**:  
已知直线$y=k x+m(k>0)$与抛物线$C$: $y^{2}=4 x$及其准线分别交于$M$、$N$两点，$F$为抛物线的焦点，若$3 \overrightarrow {F M}=\overrightarrow{M N}$，则$k$等于?

**Process**:  
抛物线C:y^{2}=4x的焦点F(1,0),直线l:y=kx+m过抛物线的焦点,\thereforek+m=0过N做NN'\bot准线x=-1,垂足为N',由抛物线的定义,|NN'|=|NF由\angleNNM与直线l倾斜角相等,由3\overrightarrow{FM}=\overrightarrow{MN}则\cos\angleNNM=\frac{|NN'|}{|MN|}=\frac{1}{3},则\tan\angleNNM=\pm2\sqrt{2},因为k>0\therefore直线l的斜率k=2\sqrt{2},

**Theorem Sequence**:  
Parabola_Equation_Standard_Right, Parabola_Definition, Parabola_Directrix, Vector_Collinear_Condition, Triangle_Midline_Theorem

---

## Problem Index: 5927
**ID**: 5928
**Text**:  
已知直线$l$与抛物线$C$: $y^{2}=x$交于$A$、$B$两点.且线段$A B$的中点在直线$y=1$上，若$\overrightarrow{O A} \cdot \overrightarrow{O B}=0$($O$为坐标原点），则$\triangle A O B$的面积为?

**Process**:  
由题意知:直线l的斜率不为0,所以设直线l的方程为x=my+t(t\neq0)由\begin{cases}x=my+t\\y2=x\end{cases},消x得y^{2}-my-t=0,设A(x_{1},y_{1}),B(x_{2},y_{2}),则y_{1}+y_{2}=m,y_{1}y_{2}=-t,A=m^{2}+4t>0,因为线段AB的中点在直线y=1上,所以y_{1}+y_{2}=2,即m=2.因为\overrightarrow{OA}\cdot\overrightarrow{OB}=0,所以x_{1}x_{2}+y_{1}y_{2}=y_{1}y_{2}+(my_{1}+t)(my_{2}+t)=y_{1}y_{2}+m^{2}y_{1}y_{2}+mt(y_{1}+y_{2})+t^{2}=y_{1}y_{2}+4y_{1}y_{2}+2t\times2+t^{2}=t^{2}-t=0,解得t=1或t=0(舍)所以y_{1}+y_{2}=2,y_{1}y_{2}=-1,直线l的方程为x=2y+1,所以|AB|=\sqrt{1+2^{2}}\sqrt{(y_{1}+y_{2})^{2}-4y_{1}y_{2}}=2\sqrt{10}原点O到直线l的距离为d=\frac{|0-0-1|}{\sqrt{5}}=\frac{\sqrt{5}}{5}所以\triangleAOB的面积为\frac{1}{2}\times|AB|\timesd=\frac{1}{2}\times2\sqrt{10}\times\frac{\sqrt{5}}{5}=\sqrt{2}

**Theorem Sequence**:  
Parabola_Equation_Standard_Right, Substitution_x_equals_my_plus_n, Vieta_Theorem_Sum, Vieta_Theorem_Product, Vector_Collinear_Condition

---

## Problem Index: 5931
**ID**: 5932
**Text**:  
过抛物线$C$: $y^{2}=4 x$的焦点$F$的直线$l$交$C$于$A$、$B$两点，设$A$、$B$在$y$轴上的投影分别为$A^{\prime}$, $B^{\prime}$，若$|A B|=\frac{3}{2}(|A A^{\prime}|+|B B^{\prime}|)$，则直线$l$的斜率为?

**Process**:  
由抛物线的定义可知:|AB|=|AF|+|BF|=|AA|+1+|BB|+1=|AA|+|BB|+2=\frac{3}{2}(|AA|+|BB|)\therefore|AA|+|BB|=4,\therefore|AB|=6.设直线l的倾斜角为\alpha,则|AB|=\frac{4}{\sin^{2}\alpha}=6,\therefore\sin^{2}a=\frac{2}{3}.\tan\alpha=\pm\sqrt{2}即直线/的斜率为\pm\sqrt{2}

**Theorem Sequence**:  
Parabola_Equation_Standard_Right, Parabola_Definition, Parabola_Focal_Radius, Triangle_Area_With_Sin, Triangle_Midline_Theorem

---

## Problem Index: 5952
**ID**: 5953
**Text**:  
若双曲线的两准线间的距离是焦距的$\frac{3}{5}$，则双曲线的离心率为?

**Process**:  
双曲线的两准线的距离为:2\frac{a^{2}}{c},两焦点间的距离为:2c,根据题意可由:\frac{2a^{2}}{c}=\frac{3}{5}\times2c化简为:5a^{2}=3c2解得:e=\frac{\sqrt{15}}{2},所以答案为:\frac{\sqrt{15}}{2}

**Theorem Sequence**:  
Ellipse_Equation_Standard_X, Ellipse_Equation_Standard_Y, Eccentricity_Formula

---

## Problem Index: 5966
**ID**: 5967
**Text**:  
过抛物线$y^{2}=2 x$的焦点$F$作直线交抛物线于$A$、$B$两点，若$|A B|=\frac{25}{12}$, $|A F|<|B F|$, 则$|A F|$=?

**Process**:  
设|AF|=m,|BF|=n,则\frac{1}{m}+\frac{1}{n}=\frac{2}{p},又|AB|=\frac{25}{12},所以m+n=\frac{25}{12},mn=\frac{25}{24}则m=\frac{5}{6},n=\frac{5}{4}【考点定位】本题主要考查了抛物线的简单性质及抛物线与直线的关系,当遇到抛物线焦点弦问题时,常根据焦点设出直线方程与抛物线方程联立,把韦达定理和抛物线定义相结合解决问题,属于难题

**Theorem Sequence**:  
Parabola_Equation_Standard_Right, Parabola_Focal_Radius, Vieta_Theorem_Sum, Basic_Inequality

---

## Problem Index: 5969
**ID**: 5970
**Text**:  
已知椭圆$\frac{x^{2}}{a^{2}}+\frac{y^{2}}{b^{2}}=1$的左、右焦点分别为$F_{1}$、$F_{2}$，上顶点为$D$，且$\angle F_{1} D F_{2}=120^{\circ}$，若第一象限的点$A$、$B$在$C$上，$|A F_{2}|=2$ ,$|B F_{2}|=4$ ,$|A B|=3$，则直线$A B$的斜率为?

**Process**:  
椭圆\frac{x^{2}}{a^{2}}+\frac{y^{2}}{b^{2}}=1的左、右焦点分别为F_{1}F_{2},上顶点为D,且\angleF_{1}DF_{2}=120^{\circ}所以,\angleF_{1}DO=60^{\circ},由椭圆的几何性质可知|DF_{1}|=a,|OF_{1}|=c,椭圆的离心率为e=\frac{c}{a}=\sin60^{\circ}=\frac{\sqrt{3}}{2}设点A(x_{1},y_{1})、B(x_{2},y_{2}),则0<x_{1}<a_{1}0<x_{2}<a_{2}=|ex_{1}-a|=a-ex_{1}=2,同理可得|BF_{2}|=a-ex_{2}=4,所以,|BF_{2}|-|AF_{2}|=e(x_{1}-x_{2})=\frac{\sqrt{3}}{2}(x_{1}-x_{2})=2'解得x_{1}-,x_{2}=.4\sqrt{3},设直线AB的斜率为k,由弦长公式可得|AB|=\sqrt{1+k^{2}}|x_{1}-x_{2}|=\frac{4\sqrt{3}}{3}\sqrt{1+k^{2}}=3解得k=\pm\frac{\sqrt{11}}{4}.因为点A、B都在第一象限,则k<0,故_{k}=-\frac{\sqrt{11}}{4}.

**Theorem Sequence**:  
Ellipse_Equation_Standard_X, Ellipse_Definition, Ellipse_Focal_Radius, Eccentricity_Formula, Triangle_Midline_Theorem

---

## Problem Index: 5975
**ID**: 5976
**Text**:  
$F$是抛物线$y^{2}=4 x$的焦点，过$F$的直线$l$交抛物线于$A$、$B$两点，$O$为坐标原点，若$|A F|=10$，则$\triangle O A B$的面积为?

**Process**:  
设点A为第一象限内的点,设点A(x_{1},y_{1})、B(x_{2},y_{2}),利用抛物线的定义可求得点A的坐标,可得出直线AB的方程,将直线AB的方程与抛物线的方程联立,列出韦达定理,求出|y_{1}-y_{2}|的值由此可求得\triangleOAB的面积.设点A为第一象限内的点,设点A(x_{1},y_{1})、B(x_{2},y_{2})抛物线y^{2}=4x的准线方程为x=-1,由抛物线的定义可得|AF|=x_{1}+1=10,解得x_{1}=9由于点A为第一象限内的点,则y_{1}>0,可得y_{1}=\sqrt{4x_{1}}=6,即点A(9,6),直线AF的斜率为k_{AF}=\frac{6}{9-1}=\frac{3}{4},所以,直线AB的方程为y=\frac{3}{4}(x-1),即x=\frac{4}{3}y+1.联立\begin{cases}x=\frac{4}{3}y+1\\y2=4x\end{cases},消去x并整理可得y^{2}-\frac{16}{3}y-4=0,由韦达定理可得y_{1}+y_{2}=\frac{16}{3},\thereforey_{2}=\frac{16}{3}-y_{1}=\frac{16}{3}-6=-\frac{2}{3}因此,S_{\triangleOAB}=\frac{1}{2}|OF|\cdot|y-y_{2}|=\frac{1}{2}\times1\times6+\frac{2}{3}=\frac{10}{3}.

**Theorem Sequence**:  
Parabola_Equation_Standard_Right, Parabola_Definition, Parabola_Focal_Radius, Triangle_Area_Formula

---

## Problem Index: 5979
**ID**: 5980
**Text**:  
若双曲线的一个焦点坐标为$(5,0)$，实轴长为$6$，则它的标准方程是?

**Process**:  
由于双曲线的一个焦点坐标为(5,0),所以双曲线的焦点在x轴上,c=5,实轴长2a=6,a=3,b=\sqrt{c^{2}-a^{2}}=4,所以双曲线的标准方程是\frac{x^{2}}{9}-\frac{y^{2}}{16}=1

**Theorem Sequence**:  
Hyperbola_Equation_Standard_X, Hyperbola_Definition, Hyperbola_Parameter_Relation

---

## Problem Index: 5985
**ID**: 5986
**Text**:  
已知双曲线$\frac{x^{2}}{a^{2}}-\frac{y^{2}}{b^{2}}=1(a>0, b>0)$的焦点为$F_{1}$、$F_{2}$、$P$是双曲线上一点，且$\angle F_{1} P F_{2}=\frac{\pi}{3}$. 若$\Delta F_{1} P F_{2}$的外接圆和内切圆的半径分别为$R$, $r$，且$R=4 r$，则双曲线的离心率为?

**Process**:  
双曲线的焦点为F_{1}(-c,0),F_{2}(c,0),|F_{1}F_{2}|=2c,在\triangleF_{1}PF_{2}中,由正弦定理得:2R=\frac{|F_{1}F_{2}|}{\sin\angleF_{1}PF_{2}}=\frac{2c}{\sin\frac{\pi}{3}}=\frac{4\sqrt{3}}{3}c解得_{R}=\frac{2\sqrt{3}}{3}c'r=\frac{1}{4}R=\frac{\sqrt{3}}{6}c设|PF_{1}|=m,|PF_{2}|=n,在\triangleF_{1}PF_{2}中,由余弦定理得:4c^{2}=m^{2}+n^{2}-2mn\cos\frac{\pi}{3}=(m-n)^{2}+mn解得mn=4(c^{2}-a^{2})所以S_{\triangleF_{1}PF_{2}}=\frac{1}{2}mn\sin\frac{\pi}{3}=\sqrt{3}(c^{2}-a^{2}),因为(m+n)^{2}=(m-n)^{2}+4mn=4a^{2}+16(c^{2}-a^{2})=16c^{2}-12a^{2}又s_{\DeltaF_{1}PF_{2}}=\frac{1}{2}(m+n+2c)r=\frac{\sqrt{3}c(m+n+2c)}{12}所以\sqrt{3}(c^{2}-a^{2})=\frac{\sqrt{3}c(m+n+2c)}{12},则m+n=\frac{10c^{2}-12a^{2}}{c}所以_{(m+n)^{2}}=(\frac{10c^{2}-12a^{2}}{c})^{2}=16c^{2}-12a^{2}整理得21c^{4}+36a^{4}-57a^{2}c^{2}=0,则(c^{2}-a^{2})(2lc^{2}-36a^{2})=0解得e=\frac{c}{a}=\frac{2\sqrt{21}}{7}或e=1(舍去)

**Theorem Sequence**:  
Hyperbola_Equation_Standard_X, Hyperbola_Definition, Ellipse_Focal_Triangle_Perimeter, Pythagorean_Theorem, Triangle_Area_With_Sin, Triangle_Area_Formula, Eccentricity_Formula

---

## Problem Index: 6003
**ID**: 6004
**Text**:  
已知抛物线$C$: $y^{2}=2 p x(p>0)$的焦点为$F(2,0)$，则抛物线$C$的方程是?

**Process**:  
因为抛物线C:y^{2}=2px(p>0)的焦点为F(2,0)即\frac{p}{2}=2,所以p=4,所以抛物线C的方程是y^{2}=8x

**Theorem Sequence**:  
Parabola_Equation_Standard_Right, Parabola_Directrix

---

## Problem Index: 6005
**ID**: 6006
**Text**:  
焦点在$y$轴上的双曲线$y^{2}-m x^{2}=1$的离心率为$\frac{\sqrt{5}}{2}$，则$m$的值为?

**Process**:  
双曲线的标准方程为y^{2}-\frac{x^{2}}{m}=1,由题意可得m>0,则a=1,b=\frac{1}{\sqrt{m}},c=\sqrt{a^{2}+b^{2}}=\sqrt{1+\frac{1}{m}}所以,e=\frac{c}{a}=\sqrt{1+\frac{1}{m}}=\frac{\sqrt{5}}{2},解得m=4

**Theorem Sequence**:  
Hyperbola_Equation_Standard_X, Eccentricity_Formula

---

## Problem Index: 6009
**ID**: 6010
**Text**:  
抛物线$y=x^{2}$的焦点到准线的距离是?

**Process**:  
由抛物线的解析式求出p,即可求解由y=x^{2}变形得x^{2}=y,故抛物线焦点在y的正半轴,2p=1,p=\frac{1}{2},故抛物线y=x^{2}的焦点到准线的距离是p=\frac{1}{2}

**Theorem Sequence**:  
Parabola_Equation_Standard_Right, Parabola_Directrix

---

## Problem Index: 6019
**ID**: 6020
**Text**:  
经过点$M(2,1)$作直线$l$交双曲线$x^{2}-\frac{y^{2}}{2}=1$于$A$、$B$两点，且$M$为$A B$的中点，则直线$l$的方程为?

**Process**:  
设点A(x_{1},y_{1}),点B(x_{2},y_{2}),代入双曲线方程,两式作差,利用中点坐标公式求出直线的斜率.根据点斜式即可求解.设点A(x_{1},y_{1}),点B(x_{2},y_{2})M(x_{0},y_{0}),则2x_{1}^{2}-y_{1}^{2}=2,\cdots\cdots\textcircled{1}2x_{2}^{2}-y_{2}^{2}=2,\cdots\cdots\textcircled{2}\textcircled{1}-\textcircled{2}得2(x_{1}+x_{2})(x_{1}-x_{2})-(y_{1}+y_{2})(y_{1}-y_{2})=0,2\times2x_{0}-2y_{0}\frac{y_{1}-y_{2}}{x_{1}-x_{2}}=0,所以8-2k=0,所以k=4,所以y-1=4(x-2)所以直线l的方程为4x-y-7=0.

**Theorem Sequence**:  
Hyperbola_Equation_Standard_X, Point_Difference_Method, Midpoint_Formula

---

## Problem Index: 6035
**ID**: 6036
**Text**:  
已知双曲线$C$的中心在原点，$F(-2,0)$是一个焦点，过$F$的直线$l$与双曲线$C$交于$A$、$B$两点，且$A B$的中点为$N(-3,-1)$，则$C$的方程是?

**Process**:  
由F,N的坐标得k_{l}=1设双曲线方程为\frac{x^{2}}{a^{2}}-\frac{y^{2}}{b^{2}}=1(a>0,b>0),则a^{2}+b^{2}=4设A(x_{1},y_{1}),B(x_{2},y_{2})则x_{1}+x_{2}=-6,y_{1}+y_{2}2,\frac{y_{1}-y_{2}}{x_{1}-x_{2}}=k_{l}=1由\frac{x_{1}^{2}}{a^{2}}-\frac{y_{1}^{2}}{b^{2}}=1\frac{x_{2}^{2}}{a^{2}}+y_{2}=-2,\frac{y_{2}^{2}}{x_{1}+x_{2}}=k_{1}=1即\frac{-6}{a^{2}}+\frac{2k_{l}}{b^{2}}=0,a^{2}=3b于是a^{2}=3,b^{2}=1所以C的方程为\frac{x^{2}}{3}-y^{2}=1

**Theorem Sequence**:  
Hyperbola_Equation_Standard_X, Point_Difference_Method_Hyperbola, Line_Point_Slope_Form, Point_Difference_Method, Hyperbola_Parameter_Relation

---

## Problem Index: 6038
**ID**: 6039
**Text**:  
若直线$l$: $y=x+b$与抛物线$C$:$ x^{2}=4 y$相切于点$A$，则以点$A$为圆心且与抛物线$C$的准线相切的圆的标准方程为?

**Process**:  
y=\frac{1}{4}x^{2},y=\frac{1}{2}x=1,x=2,故切点为(2,1),到准线y=-1的距离为2,故半径为2,圆的方(x-2)^{2}+(y-1)^{2}=4.

**Theorem Sequence**:  
Parabola_Equation_Standard_Right, Ellipse_Tangent_Line, Parabola_Directrix, Circle_Standard_Equation

---

## Problem Index: 6091
**ID**: 6092
**Text**:  
设$F_{1}$、$F_{2}$是椭圆$C$: $\frac{x^{2}}{16}+\frac{y^{2}}{7}=1$的左，右焦点，点$P$在$C$上，$O$为坐标原点，且$|O P|=3$，则$\triangle P F_{1} F_{2}$的面积为?

**Process**:  
由题意得,a=4,c=3,|OP|=3=\frac{1}{2}|F_{1}F_{2}|,\thereforeP在以线段F_{1}F_{2}为直径的圆上,\thereforePF_{1}\botPF_{2},\therefore|PF_{1}|^{2}+|PF_{2}|^{2}=|F_{1}F_{2}|^{2}=36\textcircled{1},由椭圆的定义知,|PF_{1}|+|PF_{2}|=8\textcircled{2},由\textcircled{1}\textcircled{2},解得|PF_{1}|\cdot|PF_{2}|=14,\thereforeS_{\DeltaPF_{1}F_{2}}=\frac{1}{2}|PF_{1}|\cdot|PF_{2}|=7.

**Theorem Sequence**:  
Ellipse_Equation_Standard_X, Ellipse_Definition, Ellipse_Focal_Triangle_Perimeter, Triangle_Area_Formula

---

## Problem Index: 6105
**ID**: 6106
**Text**:  
设$P$为椭圆$\frac{x^{2}}{9}+\frac{y^{2}}{5}=1$上在第一象限内的一点，$F_{1}$、$F_{2}$分别为左、右焦点，若$|P F_{1}|-|P F_{2}|=\frac{8}{3}$，则以$P$为圆心，$|P F_{2}|$为半径的圆的标准方程为?

**Process**:  
\becauseP为椭圆\frac{x^{2}}{9}+\frac{y^{2}}{5}=1上在第一象限内的一点,F_{1},F_{2}分别为左、右焦点\therefore|F_{1}F_{2}|=4,|PF_{1}|+|PF_{2}|=6\because|PF_{1}|-|PF_{2}|=\frac{8}{3}\therefore|PF_{1}|=\frac{13}{3},|PF_{2}|=\frac{5}{3}\because|PF_{2}|^{2}+|F_{1}F_{2}|^{2}=\frac{25}{9}+16=\frac{169}{9},|PF_{1}|^{2}=\frac{169}{9}\therefore|PF_{2}|^{2}+|F_{1}F_{2}|^{2}=|PF_{1}|^{2},即\anglePF_{2}F_{1}=90^{\circ}\thereforeP(2,\frac{5}{3})\therefore以P为圆心,|PF_{2}|为半径的圆的标准方程为(x-2)^{2}+(y-\frac{5}{3})^{2}=\frac{25}{9}

**Theorem Sequence**:  
Ellipse_Equation_Standard_X, Ellipse_Definition, Ellipse_Focal_Triangle_Perimeter, Circle_Standard_Equation

---

## Problem Index: 6112
**ID**: 6113
**Text**:  
若椭圆$\frac{x^{2}}{64}+\frac{y^{2}}{36}=1$上一点$P$到它的一个焦点的距离等于$4$,那么点$P$到另一个焦点的距离等于?

**Process**:  
因为利用椭圆的定义可知,椭圆\frac{x^{2}}{64}+\frac{y^{2}}{36}=1上一点P到它的一个焦点的距离等于4,那么点P到另一个焦点的距离等于2a-4=2*8-4=12,故填写12.

**Theorem Sequence**:  
Ellipse_Equation_Standard_X, Ellipse_Definition

---

## Problem Index: 6138
**ID**: 6139
**Text**:  
已知双曲线的两个焦点为$F_{1}(-\sqrt{5}, 0)$,   $F_{2}(\sqrt{5}, 0)$, $P$是此双曲线上的一点，且$P F_{1} \perp P F_{2}$,$|P F_{1}| \cdot|P F_{2}|=2$，则该双曲线的离心率是?

**Process**:  
由PF_{1}\botPF_{2},根据勾股定理可得:|PF_{1}|^{2}+|PF_{2}|^{2}=|F_{1}F_{2}|^{2}=20可得(|PF_{1}|-|PF_{2}|)^{2}=|PF_{1}|^{2}+|PF_{2}|^{2}-2|PF_{1}|\cdot|PF_{2}|=20-2|PF_{1}|\cdot|PF_{2}|又|PF_{1}|\cdot|PF_{2}|=2,所以(|PF_{1}|-|PF_{2}|)^{2}=16'所以|PF_{1}|-|PF_{2}|=4=2a所以a=2,c=\sqrt{5}该双曲线的离心率是\frac{c}{a}=\frac{\sqrt{5}}{2}

**Theorem Sequence**:  
Hyperbola_Equation_Standard_X, Hyperbola_Definition, Ellipse_Focal_Triangle_Perimeter, Eccentricity_Formula

---

## Problem Index: 6145
**ID**: 6146
**Text**:  
双曲线$C$: $\frac{x^{2}}{a^{2}}-\frac{y^{2}}{b^{2}}=1(a>0, b>0)$的右焦点为$F$、$O$为坐标原点，以$F$为圆心，$|O F|$为半径的圆与$C$和$C$的渐近线在第一象限分别交于$M$、$N$两点，线段$M F$的中点为$P$. 若$|O N|=|O P|$，则$C$的离心率为?

**Process**:  
求出F到渐近线的距离,从而利用勾股定理求得|ON|,由圆F的方程与双曲线方程联立解得M点坐标,由中点坐标公式得N点坐标,再由|ON|=|OP|列式后可计算出离心率e双曲线过第一象限的渐近线方程为y=\frac{b}{a}x'即bx-ay=0,F(c,0),F到渐近线的距离为d=\frac{|bc|}{\sqrt{b^{2}+a^{2}}}=b,\therefore|ON|=2\sqrt{c^{2}-d^{2}}=2\sqrt{c^{2}-b^{2}}=2a,圆F方程为(x-c)^{2}+y^{2}=c^{2},由\begin{cases}\frac{x^{2}}{a^{2}}-\frac{y^{2}}{b^{2}}=1\\(x-c)^{2}+y^{2}=c^{2}\end{cases},解得\begin{cases}x=\frac{a2+ac}{c}\\y=\frac{b\sqrt{a^{2}+2ac}}{c}\end{cases}(因为M点在S限),即M(\frac{a^{2}+ac}{c},\frac{b\sqrt{a^{2}+2ac}}{c})^{(x-c)+y^{2}=c-x}\because|ON|=|OP|,即|OP|^{2}=4a^{2},\frac{(a^{2}+ac+c^{2})^{2}}{4c^{2}}+\frac{b^{2}(a^{2}+2ac)}{4c^{2}}=4a^{2},整理得c^{2}+4ac-12a^{2}=0,即e^{2}+4e-12=0,

**Theorem Sequence**:  
Hyperbola_Equation_Standard_X, Hyperbola_Asymptote, Circle_Standard_Equation, Triangle_Midline_Theorem, Eccentricity_Formula

---

## Problem Index: 6162
**ID**: 6163
**Text**:  
已知点$P$是双曲线$\frac{x^{2}}{12}-\frac{y^{2}}{4}=1$右支上的一点，且以点$P$及焦点$F_{1}$、$F_{2}$为定点的三角形的面积为$4$，则点$P$的坐标是?

**Process**:  
设P(x,y),x>0.由题意知c^{2}=a^{2}+b^{2}=12+4=16,所以c=4,则F_{1}(-4,0),F_{2}(4,0).由题意可得S_{\trianglePF_{1}F_{2}}=\frac{1}{2}|F_{1}F_{2}||y|=4|y|=4\Rightarrowy=\pm1把y=\pm1代入\frac{x^{2}}{12}-\frac{y^{2}}{4}=1,得x=\sqrt{15}所以P点坐标为(\sqrt{15},\pm1)

**Theorem Sequence**:  
Hyperbola_Equation_Standard_X, Triangle_Area_Formula

---

## Problem Index: 6174
**ID**: 6175
**Text**:  
已知双曲线$C$: $\frac{x^{2}}{a^{2}}-\frac{y^{2}}{b^{2}}=1(a>0 , b>0)$的左、右焦点分别为$F_{1}$、$F_{2}$、$P$是双曲线右支上一点，$P F_{1} \perp P F_{2}$，直线$P F_{2}$交$y$轴于点$Q$，且$\overrightarrow{F_{2} P}=\frac{2}{3} \overrightarrow{P Q}$，则双曲线$C$的离心率为?

**Process**:  
解法一:由题意知|PF_{1}|-|PF_{2}|=2a,|PF_{1}|^{2}+|PF_{2}|^{2}=|F_{1}F_{2}|^{2}=4c^{2}.所以|PF_{1}|\cdot|PF_{2}|=\frac{4c^{2}-4a^{2}}{2}=2b^{2}.设P(x_{0},y_{0}),则|PF_{1}|\cdot|PF_{2}|=2c\cdot|y_{0}|,所以|y_{0}|=\frac{b^{2}}{c}因为\overrightarrow{F_{2}P}=\frac{2}{3}\overrightarrow{PQ},所以x_{0}=\frac{3}{5}c,将P(\frac{3}{5}c,\frac{b^{2}}{c})代入双曲线方程,整理得9e^{4}-50e^{2}+25=0解得e^{2}=5或e^{2}=\frac{5}{9}因为e>1,所以e=\sqrt{5}解法二:设O为坐标原点,由题易得\triangleQOF_{2}\sim\triangleF_{1}PF_{2},所以\frac{|QF_{2}|}{|F_{1}F_{2}|}=\frac{|OF_{2}|}{|PF_{2}|}设|PF_{2}|=2x,因为\overrightarrow{F_{2}P}=\frac{2}{3}\overrightarrow{PQ},所以|QF_{2}|=5x,则\frac{5x}{2c}=\frac{c}{2x},得c=\sqrt{5}x.\overset-2c=2x'|_{PF_{1}^{2}+|PF_{2}|}^{2}=|F_{1}F_{2}|^{2}=4c^{2},所以|PF_{1}|=\sqrt{|F_{1}F_{2}|^{2}-|PF_{2}|^{2}}=4x所以|PF_{1}|-|PF_{2}|=4x-2x=2a,得a=x.所以e=\frac{c}{a}=\sqrt{5}

**Theorem Sequence**:  
Hyperbola_Equation_Standard_X, Hyperbola_Definition, Ellipse_Focal_Triangle_Perimeter, Triangle_Area_With_Sin, Ellipse_Eccentricity_Range

---

## Problem Index: 6179
**ID**: 6180
**Text**:  
已知直线$x-\sqrt{3} y+\sqrt{3}=0$过椭圆$\frac{x^{2}}{a^{2}}+\frac{y^{2}}{b^{2}}=1  (a>b>0)$的左焦点$F$，交椭圆于$A$、$B$两点，交$y$轴于点$C$，$\overrightarrow{F A}=2 \overrightarrow{F C}$，则该椭圆的离心率是?

**Process**:  
因为直线x-\sqrt{3}y+\sqrt{3}=0过椭圆\frac{x^{2}}{a^{2}}+\frac{y^{2}}{b^{2}}=1(a>b>0)的左焦点F所以F(-\sqrt{3},0).设A(x,y),因为\overrightarrow{FA}=2\overrightarrow{FC},由题意可得x-(-\sqrt{3})=2[0-(-\sqrt{3})]所以x=\sqrt{3},又A(x,y)在直线x-\sqrt{3}y+\sqrt{3}=0上,所以y=2,即A(\sqrt{3},2),由题意可得\begin{cases}a2-b^{2}=c^{2}=3\\\frac{3}{a2}+\frac{4}{2}=1\end{cases},解得\begin{cases}a=3\\b=\sqrt{6}\end{cases}所以离心率为e=\frac{c}{a}=\frac{\sqrt{3}}{3}

**Theorem Sequence**:  
Ellipse_Equation_Standard_X, Point_Difference_Method_Hyperbola, Vector_Perpendicular_Condition, Eccentricity_Formula

---

## Problem Index: 6193
**ID**: 6194
**Text**:  
抛物线$y^{2}=4 x$的准线与圆$x^{2}+y^{2}-4 y=0$，相交所得的弦长为?

**Process**:  
抛物线y^{2}=4x的准线方程为x=-1,圆x^{2}+y^{2}-4y=0的标准方程为x^{2}+(y-2)^{2}=4,圆心坐标为(0,2),半径为2,圆心到准线的距离为1,所以弦长为2\sqrt{2^{2}-1}=2\sqrt{3}

**Theorem Sequence**:  
Parabola_Equation_Standard_Right, Parabola_Directrix, Circle_Standard_Equation

---

## Problem Index: 6202
**ID**: 6203
**Text**:  
已知$M(x_{0}, y_{0})$是双曲线$C$: $\frac{x^{2}}{2}-y^{2}=1$上的一点，$F_{1}$、$F_{2}$是$C$上的两个焦点，若$\overrightarrow{M F}_{1} \cdot \overrightarrow{M F}_{2}<0$，则$y_{0}$的取值范围是?

**Process**:  
由题意,\overrightarrow{MF_{1}}\cdot\overrightarrow{MF_{2}}=(-\sqrt{3}-x_{0},-y_{0})\cdot(\sqrt{3}-x_{0},-y_{0})=x_{0}^{2}-3+y_{0}^{2}=3y_{0}^{2}-1<0,\therefore-\frac{\sqrt{3}}{3}<y_{0}<\frac{\sqrt{3}}{3}

**Theorem Sequence**:  
Ellipse_Equation_Standard_X, Vector_Collinear_Condition

---

## Problem Index: 6207
**ID**: 6208
**Text**:  
已知$F$为双曲线$C$: $\frac{x^{2}}{a^{2}}-\frac{y^{2}}{b^{2}}=1(a>0, b>0)$的右焦点，过$F$作$C$的渐近线的垂线$F D$ , $D$为垂足，且$|F D|=\frac{\sqrt{3}}{2}|O F|$（$O$为坐标原点），则$C$的离心率为?

**Process**:  
求出焦点到渐近线的距离就可得到a,b,c的等式,从而可求得离心率由题意F(c,0),一条渐近线方程为y=\frac{b}{a}x^{,}即bx-ay=0,\therefore|FD|=\frac{|bc|}{\sqrt{b^{2}+a^{2}}}=b,由FD=\frac{\sqrt{3}}{2}\begin{matrix}\sqrt{3}&\\\end{matrix}OF得b=\frac{\sqrt{3}}{2}c'\thereforeb^{2}=\frac{3}{4}c^{2}=c^{2}-a^{2},c^{2}=4a^{2},\thereforee=\frac{c}{a}=2.

**Theorem Sequence**:  
Hyperbola_Equation_Standard_X, Hyperbola_Asymptote, Point_To_Line_Distance, Eccentricity_Formula

---

## Problem Index: 6213
**ID**: 6214
**Text**:  
已知经过椭圆$\frac{x^{2}}{25}+\frac{y^{2}}{9}=1$的右焦点$F_{2}$的直线$A B$交椭圆于$A$、$B$两点，$F_{1}$是椭圆的左焦点，那么$\triangle A F_{1} B$的周长等于?

**Process**:  
\because椭圆\frac{x^{2}}{25}+\frac{y^{2}}{9}=1的右焦点F_{2}的直线AB交椭圆于A,B两点,F_{1}是椭圆的左焦点\thereforeAAF_{1}B的周长=|AB|+|AF|+|BF|=|AF_{2}|+|AF|+|BF|+|BF_{2}|=4a=20效答客为20

**Theorem Sequence**:  
Ellipse_Equation_Standard_X, Ellipse_Definition

---

## Problem Index: 6233
**ID**: 6234
**Text**:  
设$B$是椭圆$C$: $\frac{x^{2}}{a^{2}}+\frac{y^{2}}{b^{2}}=1(a>b>0)$的上顶点，若$C$上的任意一点$P$都满足$|P B| \leq 2 b$，则$C$的离心率的取值范围?

**Process**:  
设P(x,y),则|PB|=\sqrt{x^{2}+(y-b)^{2}}=\sqrt{-\frac{c^{2}}{b^{2}}y^{2}-2by+a^{2}+b^{2}}=\sqrt{-\frac{c^{2}}{b^{2}}(y+\frac{b^{3}}{c^{2}})^{2}+a^{2}+b^{2}+\frac{b^{4}}{c^{2}}}\leqslant2b因为y\in[-b,b],当-\frac{b^{3}}{c^{2}}>-b即a^{2}<2c^{2}时,|PA|_{\max}=\sqrt{a^{2}+b^{2}+\frac{b^{4}}{c^{2}}}\leqslant2b'所以a^{2}+b^{2}+\frac{b^{4}}{c^{2}}\leqslant4b^{2}化简得:a^{4}-4a2c^{2}+4c^{4}\leqslant0\therefore(a^{2}-2c^{2})^{2}\leqslant0,显然该不等式不成立,当-\frac{b^{3}}{c^{2}}\leqslant-b^{,}即a^{2}\geqslant2c^{2}时,|PA|_{\max}=\sqrt{4a^{2}-4c^{2}}\leqslant2b,恒成立由a^{2}\geqslant2c^{2},得\frac{c^{2}}{a^{2}}\leqslant\frac{1}{2},所以0<e\leqslant\frac{\sqrt{2}}{2}综上,离心率的范围为(0,\frac{\sqrt{2}}{2}]

**Theorem Sequence**:  
Ellipse_Equation_Standard_X, Vector_Collinear_Condition, Ellipse_Eccentricity_Range

---

## Problem Index: 6253
**ID**: 6254
**Text**:  
双曲线$\frac{x^{2}}{16}-\frac{y^{2}}{9}=1$的左. 右焦点为$F_{1}$、$F_{2}$，若点$P$在双曲线上，$\overrightarrow{P F_{1}} \cdot \overrightarrow{P F_{2}}=0$，则$|\overrightarrow{P F_{1}}+\overrightarrow{P F_{2}}|$=?

**Process**:  
连接PO,则可得|\overrightarrow{PF_{1}}+\overrightarrow{PF_{2}}|=2|\overrightarrow{PO}|=2c,从而可得正确自己连接PO,因为O为F_{1},F_{2}的中点,故\overrightarrow{PF}_{1}+\overrightarrow{PF_{2}}=2\overrightarrow{PO},所以|\overrightarrow{PF_{1}}+\overrightarrow{PF_{2}}|=2|\overrightarrow{PO}|而\overrightarrow{PF}\cdot\overrightarrow{PF_{2}}=0,故\trianglePF_{2}F_{1}是以P为直角顶点的直角三角形,故|\overrightarrow{PF_{1}}+\overrightarrow{PF_{2}}|=2|\overrightarrow{PO}|=2|\overrightarrow{F_{1}O}|=10

**Theorem Sequence**:  
Ellipse_Equation_Standard_X, Ellipse_Definition, Ellipse_Focal_Triangle_Perimeter, Vector_Collinear_Condition

---

## Problem Index: 6283
**ID**: 6284
**Text**:  
设双曲线$\frac{x^{2}}{a^{2}}-\frac{y^{2}}{b^{2}}=1  (a>0 , b>0)$的一个焦点为$F$，虚轴的一个端点为$B$，线段$B F$与双曲线的一条渐近线交于点$A$，若$\overrightarrow{F A}=2 \overrightarrow{A B}$，则双曲线的离心率为?

**Process**:  
由\overrightarrow{FA}=2\overrightarrow{AB},得\overrightarrow{OA}=\frac{1}{3}(\overrightarrow{OF}+2\overrightarrow{OB}),从而求出A点坐标,再由点A在渐近线y=\frac{b}{a}x上,能求出双曲线的离心率.设点F(c,0),B(0,b)由\overrightarrow{FA}=2\overrightarrow{AB},得\overrightarrow{OA}-\overrightarrow{OF}=2(\overrightarrow{OB}-\overrightarrow{OA})\therefore\overrightarrow{OA}=\frac{1}{3}(\overrightarrow{OF}+2\overrightarrow{OB}),\thereforeA(\frac{c}{3},\frac{2b}{3})\because点A在渐近线y=\frac{b}{a}x上,则\frac{2b}{3}=\frac{b}{a}\times\frac{c}{3}.解得e=\frac{c}{a}=2.

**Theorem Sequence**:  
Hyperbola_Equation_Standard_Y, Vector_Collinear_Condition, Hyperbola_Asymptote, Eccentricity_Formula

---

## Problem Index: 6323
**ID**: 6324
**Text**:  
已知双曲线$C$: $\frac{x^{2}}{a^{2}}-\frac{y^{2}}{b^{2}}=1(a>0, b>0)$的一条渐近线与直线$l$: $2 x+y-3=0$平行，则双曲线$C$的离心率是?

**Process**:  
由题意可得双曲线C的一条渐近线方程为y=-\frac{b}{a}x,则-\frac{b}{a}=-2,即\frac{b}{a}=2则e^{2}=\frac{c^{2}}{a^{2}}=\frac{a^{2}+b^{2}}{a^{2}}=1+\frac{b^{2}}{a^{2}},故双曲线C的离心率e=\sqrt{\frac{b^{2}}{a2}+1}=\sqrt{5}.

**Theorem Sequence**:  
Hyperbola_Equation_Standard_X, Hyperbola_Asymptote, Eccentricity_Formula

---

## Problem Index: 6359
**ID**: 6360
**Text**:  
方程$\frac{x^{2}}{3-k}+\frac{y^{2}}{2+k}=1$表示椭圆，则$k$的取值范围是?

**Process**:  
因为\frac{x2}{3-k}+\frac{y^{2}}{k^{2}+k}=1表示=_{1}表示椭圆,所以(3-\frac{1}{2})解得\begin{cases}-2\\x\neq\frac{1}{7}\end{cases}k的取值范围是(-2,\frac{1}{2})\cup(\frac{1}{2},3),故答案)\underline{1}U(\frac{1}{2},3)与睛)本题主要老杳相标准方程,解答过程注意排除方程表示圆的情况,属于基础题

**Theorem Sequence**:  
Ellipse_Equation_Standard_X, Ellipse_Equation_Standard_Y

---

## Problem Index: 6368
**ID**: 6369
**Text**:  
已知$F$为双曲线$C$: $x^{2}-\frac{y^{2}}{8}=1$的右焦点，$P$是$C$左支上一点，又$A(0, \frac{36}{5})$，当$\triangle A P F$的周长最小时，则点$P$的坐标为?

**Process**:  
设双曲线的左焦点为F,由双曲线Cx^{2}-\frac{y^{2}}{8}=1得a=1,b=2\sqrt{2},c=3,即有F(3,0)F(-3,0),所以|AF|=\sqrt{(3-0)^{2}+(0-\frac{36}{5})^{2}}=\sqrt{\frac{1521}{25}}=\frac{39}{5}是定值,由双曲线的定义可得|PF|-|PF|=2a=2,得|PA|+|PF|=|PA|+|PF|+2,而\trianglePFA周长为|PA|+|PF|+|AF|.所以当P在左支上运动到A,P,F共线时,|PA|+|PF|取得最小值|AF|则有\triangleAPF周长取得最小值,直线AF的方程为\frac{x}{-3}+\frac{y}{\frac{36}{5}}=1,即12x-5y+36=0,与双曲线方程联立,\begin{cases}12x-5y+36=0\\x2-\frac{y^{2}}{8}=1\end{cases},解得点P的坐标为(-\frac{11}{7},\frac{24}{7})

**Theorem Sequence**:  
Hyperbola_Equation_Standard_X, Hyperbola_Definition, Ellipse_Definition, Pythagorean_Theorem, Point_Difference_Method_Hyperbola, Triangle_Area_Formula

---

## Problem Index: 6378
**ID**: 6379
**Text**:  
双曲线$\frac{x^{2}}{16}-\frac{y^{2}}{m}=1$的离心率为$\frac{5}{4}$，则$m$等于?

**Process**:  
利用双曲线的离心率计算公式e=\frac{c}{a}=\sqrt{1+\frac{b^{2}}{a}^{2}}即可得出.\because双曲线\frac{x^{2}}{16}-\frac{y^{2}}{m}=1可得a^{2}=16,b^{2}=m,又离心率为\frac{5}{4},则e=\frac{c}{a}=\sqrt{1+\frac{b^{2}}{2}}=\sqrt{1+\frac{m}{16}}=\frac{5}{4},解得m=9.

**Theorem Sequence**:  
Hyperbola_Equation_Standard_X, Eccentricity_Formula

---

## Problem Index: 6379
**ID**: 6380
**Text**:  
已知双曲线$C$: $\frac{x^{2}}{8}-\frac{y^{2}}{8}=1$的左焦点为$F$，点$M$在双曲线$C$的右支上，$A(0,4)$，当$\triangle M A F$的周长最小时，$\triangle M A F$的面积为?

**Process**:  
\triangleMAF的周长为|MA|+|MF|+|AF|,其中|AF|=4\sqrt{2}为定值,所以即求|MA|+|MF|,利用定义可得|MF|=|MF|+4\sqrt{2},所以周长为|MA|+|MF|+8\sqrt{2},作图当M、A、F三点共线时周长最短,利用面积分割求得面积.如图,设双曲线C的右焦点为F.由题意可得a=2\sqrt{2},F(-4,0),F(4,0).因为点M在右支上,所以|MF|-|MF|=2a=4\sqrt{2},所以|MF|=|MF|+4\sqrt{2},则\triangleMAF的周长为|MA|+|MF|+|AF|=|MA|+|MF|+8\sqrt{2}\geqslant|AF|+8\sqrt{2}=12\sqrt{2}即当M在M处时,\triangleMAF的周长最小,此时直线AF的方程为y=-x+4联立\begin{cases}y=-x+4\\\frac{x^{2}}{8}-\frac{y^{2}}{8}=1\end{cases},整理得y-1=0,则y_{M}=1,故\triangleMAF的面积为\frac{1}{2}|FF'||OA|-\frac{1}{2}|FF||y_{M}|=\frac{1}{2}\times8\times(4-1)=12

**Theorem Sequence**:  
Hyperbola_Equation_Standard_X, Hyperbola_Definition, Ellipse_Definition, Pythagorean_Theorem, Two_Points_Distance, Triangle_Area_Formula

---

## Problem Index: 6382
**ID**: 6383
**Text**:  
直线$l$: $x-y-2=0$与圆相切于点$M(3,1)$，且圆心在抛物线$y^{2}=-4 x$的准线上，则圆的标准方程为?

**Process**:  
由抛物线方程,可知准线方程为x=1,设圆心坐标为(1,b),由题+(1-b)^{2}=\frac{|1-b-2|}{\sqrt{2}},解得b=3,r=2\sqrt{2}所以圆的标准方程为(x-1)^{2}+(y-3)^{2}=8

**Theorem Sequence**:  
Parabola_Equation_Standard_Right, Parabola_Directrix, Circle_Standard_Equation

---

## Problem Index: 6391
**ID**: 6392
**Text**:  
已知抛物线$y^{2}=2 p x(p>0)$的准线与曲线$4 x^{2}-\frac{3 y^{2}}{4}=1(y>0)$交于点$P$、$F$为抛物线焦点，直线$P F$的倾斜角为$135^{\circ}$，则$p$=?

**Process**:  
设P(\frac{p}{2}-t,t)代入抛物线得t^{2}+2pt-p^{2}=0\Rightarrowt=-p-\sqrt{2}p\RightarrowP(\frac{3}{2}p+\sqrt{2}p,-p-\sqrt{2}p)代入双曲线得p=2

**Theorem Sequence**:  
Parabola_Equation_Standard_Right, Hyperbola_Equation_Standard_X, Vector_Collinear_Condition

---

## Problem Index: 6392
**ID**: 6393
**Text**:  
若抛物线$x^{2}=4 y$上的点$P(m, n)$到其焦点$F$的距离为$3$，则$n$的值为?

**Process**:  
抛物线x^{2}=4y的焦点为(0,1),准线方程为y=-1,由题意抛物线x^{2}=4y上有点P(m,n)到其焦点的距离为3,结合抛物线的定义可得,n+1=3,解得n=2.

**Theorem Sequence**:  
Parabola_Equation_Standard_Right, Parabola_Definition, Parabola_Directrix

---

## Problem Index: 6394
**ID**: 6395
**Text**:  
已知双曲线$C$: $\frac{x^{2}}{a^{2}}-\frac{y^{2}}{b^{2}}=1(a>0, b>0)$的一条渐近线方程为$y=\frac{\sqrt{5}}{2} x$，且经过点$(2,2 \sqrt{5})$，则$C$的方程为?

**Process**:  
根据题意可设双曲线的标准方程为\frac{x^{2}}{4}-\frac{y^{2}}{5}=\lambda(\lambda\neq0),然后将点(2,2\sqrt{5})的坐标代入双曲线C的方程,求出\lambda的值,即可求得双曲线C的方程.解】由题意可知,双曲线C的一条渐近线方程为\frac{x}{2}-\frac{y}{\sqrt{5}}=0设双曲线C的方程为\frac{x^{2}}{4}-\frac{y^{2}}{5}=\lambda(\lambda\neq0),将点(2,2\sqrt{5})的坐标代入双曲线C的方程得_{\lambda}=\frac{2^{2}}{4}-\frac{(2\sqrt{5})^{2}}{5}=-3所以,双曲线C的方程为\frac{x^{2}}{4}-\frac{y^{2}}{5}=-3,即为\frac{y^{2}}{15}-\frac{x^{2}}{12}=1.

**Theorem Sequence**:  
Hyperbola_Equation_Standard_X, Hyperbola_Asymptote

---

## Problem Index: 6398
**ID**: 6399
**Text**:  
已知双曲线$C$: $\frac{x^{2}}{a^{2}}-\frac{y^{2}}{b^{2}}=1(a>0, b>0)$的左、右焦点分别为$F_{1}$、$F_{2}$，点$A$在$C$的右支上，$A F_{1}$与$C$交于点$B$，若$\overrightarrow{F_{2} A} \cdot \overrightarrow{F_{2} B}=0$,$|\overrightarrow{F_{2} A}|=|\overrightarrow{F_{2} B}|$，则$C$的离心率为?

**Process**:  
因为\overrightarrow{F_{2}A}\cdot\overrightarrow{F_{2}B}=0,|\overrightarrow{F_{2}A}|=|\overrightarrow{F_{2}B|}所以\triangleABF_{2}为等腰直角三角形,设|AF_{2}|=|BF_{2}|=m,则|AB|=\sqrt{2}m,由双曲线的定义可得|AF_{1}|-|AF_{2}|=2a,|BF_{2}|-|BF_{1}|=2a.所以|AF_{1}|=2a+m,|BF_{1}|=m-2a,因为|AB|=|AF_{1}|-|BF_{1}|=(m+2a)-(m-2a)=\sqrt{2}m所以m=2\sqrt{2}a,所以|AF|=2a+2\sqrt{2}a=(2+2\sqrt{2})a,|AF_{2}|=2\sqrt{2}a.在\triangleAF_{1}F_{2}中,由余弦定理得|F_{1}F_{2}|^{2}=|AF_{1}|^{2}+|AF_{2}|^{2}-2|AF_{1}||AF_{2}|\cos\angleF_{1}AF_{2},所以_{4c^{2}}=[(2\sqrt{2}+2)a]+(2\sqrt{2}a)^{2}-2(2\sqrt{2}+2)a\cdot2\sqrt{2}a\cdot\frac{\sqrt{2}}{2}=12a^{2}所以c^{2}=3a^{2},得c=\sqrt{3}a,所以离心率为e=\frac{c}{a}=\sqrt{3}.

**Theorem Sequence**:  
Hyperbola_Equation_Standard_X, Hyperbola_Definition, Ellipse_Definition, Ellipse_Focal_Triangle_Perimeter, Triangle_Area_With_Sin, Eccentricity_Formula

---

## Problem Index: 6404
**ID**: 6405
**Text**:  
双曲线$\frac{x^{2}}{4}-\frac{y^{2}}{16}=1$的实轴长为?

**Process**:  
由已知可得实轴长为2a=4.

**Theorem Sequence**:  
Hyperbola_Equation_Standard_X

---

## Problem Index: 6411
**ID**: 6412
**Text**:  
已知椭圆$\frac{x^{2}}{a^{2}}+\frac{y^{2}}{b^{2}}=1(a>b>0)$的左顶点为$A$，左焦点为$F$，若该椭圆的上顶点到焦点的距离为$2$，离心率$e=\frac{1}{2}$，则椭圆的标准方程是?

**Process**:  
因为椭圆的上顶点到焦点的距离为2,所以a=2因为离心率e=\frac{1}{2},所以c=1,b=\sqrt{a^{2}-c^{2}}=\sqrt{3},则椭圆的方程为\frac{x^{2}}{4}+\frac{y^{2}}{3}=1

**Theorem Sequence**:  
Ellipse_Equation_Standard_X, Ellipse_Definition, Eccentricity_Formula

---

## Problem Index: 6428
**ID**: 6429
**Text**:  
若双曲线$\frac{x^{2}}{a^{2}}-y^{2}=1(a>0)$的一条渐近线为$y=\sqrt{2} x$，则$a$=?

**Process**:  
双曲线标准方程知其渐近线方程为y=\pm\frac{1}{a}x'\because双曲线\frac{x^{2}}{a^{2}}-y^{2}=1(a>0)的一条渐近线为y=\sqrt{2}x\therefore\frac{1}{a}=\sqrt{2},故a=\frac{\sqrt{2}}{2}

**Theorem Sequence**:  
Hyperbola_Equation_Standard_X, Hyperbola_Asymptote

---

## Problem Index: 6455
**ID**: 6456
**Text**:  
已知椭圆$4 x^{2}+n y^{2}=1$的焦点在$x$轴上，长轴长是短轴长的$2$倍，则$n$的值是?

**Process**:  
椭圆4x^{2}+ny^{2}=1的焦点在x轴上,\therefore\frac{x^{2}}{4}+\frac{y^{2}}{n}=1,a=\frac{1}{2},b=\frac{\sqrt{n}}{1}\because长轴长是短轴长的2倍.1=\frac{4\sqrt{n}}{n}解得n=16.故答】本题考查了椭圆的标准方程及其性质,属于基础题

**Theorem Sequence**:  
Ellipse_Equation_Standard_X

---

## Problem Index: 6487
**ID**: 6488
**Text**:  
以$y=\pm x$为渐近线且经过点$(2,0)$的双曲线方程为?

**Process**:  
以y=\pmx为渐近线的双曲线为等轴双曲线,方程可设为x^{2}-y^{2}=\lambda(\lambda\neq0),代入点(2,0)得\lambda=4\thereforex^{2}-y^{2}=4\therefore\frac{x^{2}}{4}-\frac{y^{2}}{4}=1

**Theorem Sequence**:  
Hyperbola_Equation_Standard_X, Hyperbola_Asymptote

---

## Problem Index: 6506
**ID**: 6507
**Text**:  
已知$F_{1}$、$F_{2}$是双曲线$\frac{x^{2}}{a^{2}}-\frac{y^{2}}{b^{2}}=1(a>0, b>0)$的左、右焦点，$P$是其渐近线在第一象限内的点，点$Q$在双曲线上，且满足$\overrightarrow{P F_{1}} \cdot \overrightarrow{P F_{2}}=0$ , $\overrightarrow{P F_{2}}=4 \overrightarrow{P Q}$,则双曲线的离心率为?

**Process**:  
由题意可知,\trianglePF_{1}F_{2}为直角三角形,则OP=OF_{1}=OF_{2}.设点P的坐标为P(x,y)(x>0,y>0),结合点P在渐近线y=\frac{b}{a}x上可得:\begin{cases}y=\frac{b}{a}x\\x^{2}+y^{2}=c^{2}\end{cases},解得:\begin{cases}x=a\\y=b\end{cases},则P(a,b)且F_{2}(c,0),设Q(m,n),由题意有:\overrightarrow{PF_{2}}=(c-a,-b),\overrightarrow{PQ}=(m-a,n-b),则:(c-a,-b)=4(m-a,n-b),\begin{matrix}m=\frac{c}{4}+\frac{3a}{4}&则(\frac{c}{4}+\frac{3a}{4},-\frac{3b}{4})在双曲线上:\\n=-\frac{3b}{4}&即:\frac{1}{16}(e+3)^{2}-\frac{9}{16}=1,则:(e+3)^{2}=25即双曲线的离心率为2.

**Theorem Sequence**:  
Hyperbola_Equation_Standard_X, Hyperbola_Asymptote, Ellipse_Focal_Triangle_Perimeter, Triangle_Midline_Theorem, Eccentricity_Formula

---

## Problem Index: 6525
**ID**: 6526
**Text**:  
方程$\frac{x^{2}}{2-k}+\frac{y^{2}}{k-1}=1$表示双曲线，则实数$k$的取值范围是?

**Process**:  
\because方程\frac{x^{2}}{2-k}+\frac{y^{2}}{k-1}=1表示双曲线,\therefore(2\cdotk)(k\cdot1)<0\thereforek<1或k>2\therefore实数k的取值范围是k<1或k>2数答客为k<1或k>2与要】木题老杏的看占与又曲线的标准方程,解题的关锥是确定双曲线标准方程中平方面的系数是号

**Theorem Sequence**:  
Hyperbola_Equation_Standard_X

---

## Problem Index: 6533
**ID**: 6534
**Text**:  
过点$(\sqrt{2},-2)$且与双曲线$\frac{x^{2}}{2}-y^{2}=1$有公共渐近线的双曲线方程是?

**Process**:  
分析:设所求双曲线的方程为\frac{x^{2}}{2}-y^{2}=m(m\neq0),代入(\sqrt{2},2)求出m即可.详设双曲线方程为\frac{x^{2}}{2}-y^{2}=m(m\neq0),将(\sqrt{2},2)代入可得m=-3,故所求双曲线方程为\frac{y^{2}}{3}-\frac{x^{2}}{6}=1.

**Theorem Sequence**:  
Hyperbola_Equation_Standard_X, Hyperbola_Asymptote

---

## Problem Index: 6544
**ID**: 6545
**Text**:  
椭圆$\frac{x^{2}}{a^{2}}+\frac{y^{2}}{b^{2}}=1(a>b>0)$上任意两点$P$、$Q$，若$O P \perp O Q$，则乘积$|O P| \cdot|O Q|$的最小值为?

**Process**:  
设P(|OP|\cos\theta,|OP|\sin\theta),Q||OQ|\cos(\theta\pm\frac{\pi}{2}),|OQ|si(\theta\pm\frac{\pi}{2}))由P,Q在椭圆上,有\frac{os^{2}\theta}{a^{2}}+\frac{\sin^{2}\theta}{b^{2}}\textcircled{1}\frac{1}{1^{2}}=\frac{\sin^{2}\theta}{a^{2}}+\frac{\cos2\theta}{b^{2}}\textcircled{2}\frac{1}{20}|^{2}=\frac{1}{a^{2}}+\frac{1}{b^{2}}于是当|OP|=|OQ|=\sqrt{\frac{2a2b^{2}}{a2+b^{2}}}时,|OP||OQ|达到最小值\frac{2a2b^{2}}{a^{2}+b^{2}}

**Theorem Sequence**:  
Ellipse_Equation_Standard_X, Ellipse_Tangent_Line, Vector_Collinear_Condition, Basic_Inequality

---

## Problem Index: 6562
**ID**: 6563
**Text**:  
$P$是椭圆$\frac{x^{2}}{16}+\frac{y^{2}}{9}=1$上的动点，作$P D \perp y$轴，$D$为垂足，则$P D$中点的轨迹方程为?

**Process**:  
设点P的坐标为(x_{0},y_{0}),则\frac{x_{0}^{2}}{16}+\frac{y_{0}^{2}}{9}=1'由于PD\boty轴,D为垂足,则D(0,y_{0})设PD的中点为M(x,y),则\begin{cases}x=\frac{x_{0}}{2}\\y=y_{0}\end{cases},可得\begin{cases}x_{0}=2x\\y_{0}=y\end{cases}将\begin{cases}x_{0}=2x\\y_{0}=y\end{cases}代入等式\frac{x^{2}}{16}+\frac{y^{2}}{9}=1可得\frac{(2x)^{2}}{16}+\frac{y^{2}}{9}=1'即\frac{x^{2}}{4}+\frac{y^{2}}{9}=1

**Theorem Sequence**:  
Ellipse_Equation_Standard_X, Vector_Collinear_Condition

---

## Problem Index: 6568
**ID**: 6569
**Text**:  
若方程$\frac{x^{2}}{2 m}+\frac{y^{2}}{m-2}=1$表示焦点在$x$轴上的双曲线，则$m$的取值范围是?

**Process**:  
方程\frac{x^{2}}{2m}+\frac{y^{2}}{m-2}=1表示焦点在x轴上的双曲线,可得:\begin{cases}\\\end{cases},解得m\in(0,2).m-2<0

**Theorem Sequence**:  
Hyperbola_Equation_Standard_X

---

## Problem Index: 6583
**ID**: 6584
**Text**:  
已知$F_{1}$、$F_{2}$是双曲线$\frac{x^{2}}{4}-y^{2}=1$的两个焦点，点$P$在双曲线上，且$\angle F_{1} P F_{2}=60^{\circ}$，则$|P F_{1} |$=?

**Process**:  
双曲线\frac{x2}{4}-y^{2}=1的a=2,b=1,c=\sqrt{5}设|PF_{1}|=m,|PF_{2}|=n,由双曲线的定义可得|m\cdotn|=2a=4,\textcircled{1}在\trianglePF_{1}F_{2}中,\angleF_{1}PF_{2}=60^{\circ}可得4c^{2}=m^{2}+n^{2}-2mn\cos60^{\circ}=m^{2}+n^{2}-mn=(m-n)^{2}+mn即为mn+16=20,即mn=4,\textcircled{2}由\textcircled{1}\textcircled{2}解得m=2\sqrt{2}-2或2\sqrt{2}+2

**Theorem Sequence**:  
Hyperbola_Equation_Standard_X, Hyperbola_Definition, Ellipse_Focal_Triangle_Perimeter, Triangle_Area_Formula

---

## Problem Index: 6595
**ID**: 6596
**Text**:  
已知双曲线$C$: $\frac{x^{2}}{a^{2}}-\frac{y^{2}}{b^{2}}=1(a>0, b>0)$的左右焦点分别为$F_{1}$ , $F_{2}$ ,过$F_{1}$的直线$l$与圆$x^{2}+y^{2}=a^{2}$相切于点$T$，且直线$l$与双曲线$C$的右支交于点$P$，若$F_{1} P=4 F_{1} T$，则双曲线$C$的离心率为?

**Process**:  
根据题意,作出图形,结合双曲线第一定义,再将所有边长关系转化到直角三角形MPF_{2}中,化简求值即可如图,由题可知|OF_{1}|=|OF_{2}|=c,|OT|=a,则|F_{1}T|=b,又\because\overrightarrow{F_{1}P}=4\overrightarrow{F_{1}T},\therefore|TP|=3b,\therefore|F_{1}P|=4b又\because|PF_{1}|-|PF_{2}|=2a,\therefore|PF_{2}|=4b-2a作F_{2}M//OT,可得|F_{2}M|=2a,|TM|=b,则|PM|=2b在AMPF_{2},|PM|^{2}+|MF_{2}|^{2}=|PF_{2}|^{2},即c^{2}=(2b-a)^{2},2b=a+c又\becausec^{2}=a^{2}+b^{2},化简可得3c^{2}-2ac-5a^{2}=0,同除以a^{2},得3e^{2}-2e-5=0解得e=\frac{5}{3}双曲线的离心率为\frac{5}{3}

**Theorem Sequence**:  
Hyperbola_Equation_Standard_X, Hyperbola_Definition, Pythagorean_Theorem, Triangle_Area_With_Sin, Eccentricity_Formula

---

## Problem Index: 6608
**ID**: 6609
**Text**:  
以抛物线$C$: $y^{2}=2 p x(p>0)$的顶点为圆心的圆交$C$于$A$、$B$两点，交$C$的准线于$D$、$E$两点.已知$|A B|=2 \sqrt{6}$ ,$|D E|=2 \sqrt{10}$，则$p$等于?

**Process**:  
如图:|AB|=2\sqrt{6},|AM|=\sqrt{6},|DE|=2\sqrt{10},|DN|=\sqrt{10},|ON|=\frac{p}{2},\thereforex_{A}=\frac{(\sqrt{6})^{2}}{2p}=\frac{3}{p},\because|OD|=|OA|,\frac{1}{20}x^{2}\sqrt{|ON}\therefore\frac{p^{2}}{4}+10=\frac{9}{p^{2}}+6,解得:

**Theorem Sequence**:  
Parabola_Equation_Standard_Right, Parabola_Definition, Parabola_Directrix, Triangle_Midline_Theorem

---

## Problem Index: 6614
**ID**: 6615
**Text**:  
已知椭圆$C$的中心在坐标原点，右焦点$F$为直线$x-2 y-2=0$与$x$轴的交点，且在经过点$F$的所有弦中，最短弦的长度为$\frac{10}{3}$，则$C$的方程为?

**Process**:  
由题得F(2,0),设C:\frac{x^{2}}{a^{2}}+\frac{y^{2}}{b^{2}}=1(a>b>0)则\begin{cases}c=2,\\\frac{2b^{2}}{a}=\frac{10}{3},\\a2=b^{2}+c2\end{cases}解得a=3,b=\sqrt{5},c=2,所以C的方程为\frac{x^{2}}{9}+\frac{y^{2}}{5}=1

**Theorem Sequence**:  
Ellipse_Equation_Standard_X, Ellipse_Latus_Rectum

---

## Problem Index: 6630
**ID**: 6631
**Text**:  
已知直线$l$: $4 x-3 y+6=0$，抛物线$C$: $y^{2}=4 x$图像上的一动点到直线$l$与到$y$轴距离之和的最小值为?

**Process**:  
设抛物线上的点到直线4x-3y+6=0的距离为d_{1},到准线的距离为d_{2},到y轴的距离为d_{3}焦点的距离相等,d_{2}=|PF|d_{1}+d_{3}=d_{1}+d_{2}-1=d_{1}+|PF|-1,如图所示:d_{1}+|PF|的最小值就是焦点F到直线4x-3y+6=0的距离焦点F到直线4x-3y+6=0的距离d=\frac{|4\times1-0+6|}{\sqrt{4^{2}+3^{2}}}=2所以有:d_{1}+|PF|-1的最小值是1,

**Theorem Sequence**:  
Parabola_Equation_Standard_Right, Parabola_Definition, Parabola_Directrix, Point_To_Line_Distance

---

## Problem Index: 6636
**ID**: 6637
**Text**:  
已知点$A(3,1)$，抛物线$y^{2}=4 x$的焦点为$F$，点$P$在抛物线上，则$|P F|+|P A|$的最小值是?

**Process**:  
由题意得抛物线的准线方程为x=-1.过点P作抛物线的准线的垂线,垂足为点D,则|PD|=|PF|.则易得当A,P,D三点共线时,|PD|+|PA|取得最小值3-(-1)=4,所以|PF|+|PA|的最小值为4.

**Theorem Sequence**:  
Parabola_Equation_Standard_Right, Parabola_Definition, Parabola_Directrix, Two_Points_Distance

---

## Problem Index: 6657
**ID**: 6658
**Text**:  
已知点$M$是抛物线$y^{2}=4 x$上的一点，$F$为抛物线的焦点，$A$在圆$C$:$(x-4)^{2}+(y-1)^{2}=1$上，则$|M A|+|M F|$的最小值为?

**Process**:  
抛物线y^{2}=4x的准线方程为:x=-1过点M作MN\bot准线,垂足为N\because点M是抛物线y^{2}=4x的一点,F)为抛物线的焦点\therefore|MN|=|MF|\therefore|MA|+|MF|=|MA|+|MN|\becauseA在圆C:(x-4)^{2}+(y-1)^{2}=1,圆心C(4,1)平\therefore当N,M,C三点共线时,|MA|+|MF|最小\therefore(|MA|+|MF|)_{\min}=(|MA|+|MN|)_{\min}=|CN|-r=5-1=4\therefore(|MA|+|MF|)_{\min}=4.

**Theorem Sequence**:  
Parabola_Equation_Standard_Right, Parabola_Definition, Parabola_Directrix, Circle_Standard_Equation, Two_Points_Distance

---

## Problem Index: 6675
**ID**: 6676
**Text**:  
直线$l$:$ x-t y+1=0(t>0)$和抛物线$C$: $y^{2}=4 x$相交于不同两点$A$、$B$，设$A B$的中点为$M$，抛物线$C$的焦点为$F$，以$M F$为直径的圆与直线$l$相交另一点为$N$，且满足$|M N|=3 \sqrt{3}| N F |$, 则直线$l$的方程为?

**Process**:  
y^{2}=4x的焦点为F(1,0),联立x\cdotty+1=0与y^{2}=4x,可得y^{2}\cdot4ty+4=0,设A(x_{1},y_{1}),B(x_{2},y_{2})可得y_{1}+y_{2}=4t,则中点M(2t^{2}-1,2t)设N(ty_{0}\cdot1,y_{0}),由NF\botl,可得\frac{y_{0}}{ty_{0}-2}=-t,即有y_{0}=\frac{2t}{1+t^{2}}由|MN|=3\sqrt{3}|NF|可得|MN|^{2}=27|NF|^{2}即为(2t^{2}-ty_{0})^{2}+(2t-y_{0})^{2}=27[(ty_{0}-2)^{2}+y_{0}^{2}]结合y_{0}=\frac{2t}{1+t^{2}},整理可得t^{6}=27,解得t=\sqrt{3},可得直线的方程为x-\sqrt{3}y+1=0.

**Theorem Sequence**:  
Parabola_Equation_Standard_Right, Substitution_x_equals_my_plus_n, Ellipse_Tangent_Line, Vieta_Theorem_Sum, Triangle_Midline_Theorem

---

## Problem Index: 6695
**ID**: 6696
**Text**:  
已知双曲线$\frac{x^{2}}{a^{2}}-\frac{y^{2}}{b^{2}}=1(b>a>0)$，焦距为$2 c$，直线$l$经过点$(a, 0)$和$(0, b)$，若$(-a, 0)$到直线$l$的距离为$\frac{2 \sqrt{2}}{3} c$，则离心率为?

**Process**:  
直线l的方程为\frac{x}{a}+\frac{y}{b}=1,即为bx+ay-ab=0,c^{2}=a^{2}+b^{2},(-a,0)到直线l的距离为\frac{2\sqrt{2}}{3}c'可得:\frac{2ab}{\sqrt{a^{2}+b^{2}}}=\frac{2\sqrt{2}}{3}c.即有3ab=\sqrt{2}c^{2},即9a^{2}b^{2}=2c^{4},即9a^{2}(c^{2}-a^{2})=2c^{4},9a^{2c2-9a^{4}-2c^{4}}=0,由于e=\frac{c}{a},则2e^{4}-9e^{2}+9=0解得,e^{2}=3或e^{2}=\frac{3}{2}由于0<a<b,即a^{2}<b^{2},即有c^{2}>2a^{2},即有e^{2}>2,则e=\sqrt{3}

**Theorem Sequence**:  
Ellipse_Equation_Standard_X, Point_To_Line_Distance, Eccentricity_Formula

---

## Problem Index: 6710
**ID**: 6711
**Text**:  
已知焦点在$x$轴上的椭圆$C$经过点$A(2,1)$，且离心率为$\frac{\sqrt{2}}{2}$，则椭圆$C$的方程为?

**Process**:  
由题意,设椭圆C的方程为\frac{x^{2}}{a^{2}}+\frac{y^{2}}{b^{2}}=1(a>b>0)|知|\frac{a^{2}}{a}=\frac{b^{2}+c^{2}}{\frac{\sqrt{2}}{2}},解得b^{2}=3,a^{2}=6,\frac{4}{2}+\frac{1}{2}=1\because椭圆C的方程为\frac{x^{2}}{6}+\frac{y^{2}}{3}=1

**Theorem Sequence**:  
Ellipse_Equation_Standard_X, Ellipse_Directrix, Eccentricity_Formula

---

## Problem Index: 6719
**ID**: 6720
**Text**:  
椭圆$\frac{x^{2}}{a^{2}}+\frac{y^{2}}{b^{2}}=1(a>b>0)$的左、右焦点分别为$F_{1}$、$F_{2}$，椭圆上的点$M$满足:$\angle F_{1} M F_{2}=\frac{2 \pi}{3}$且$\overrightarrow{M F_{1}} \cdot \overrightarrow{M F_{2}}=-2$，则$b$=?

**Process**:  
先根据数量积运算得|MF_{1}||MF_{2}|=4,再结合椭圆的定义与余弦定理即可得b=]因为\angleF_{1}MF_{2}=\frac{2\pi}{3}且\overrightarrow{MF}\cdot\overrightarrow{MF_{2}}=-2,所以|MF_{1}||MF_{2}|=4,由椭圆的定义得|MF_{1}|+|MF_{2}|=2a,故|MF_{1}|^{2}+|MF_{2}|^{2}+2|MF_{1}||MF_{2}|=4a^{2}所以在\triangleF_{1}MF_{2}中,由余弦定理得\cos\angleF_{1}MF_{2}=\frac{|MF_{1}|^{2}+|MF_{2}|^{2}-4}{2|MF_{1}||MF_{2}|}\frac{-4c^{2}}{3}代入数据得-\frac{1}{2}=\frac{4a^{2}-4c^{2}-8}{8}=\frac{4b^{2}-8}{8},解得:b=1

**Theorem Sequence**:  
Ellipse_Equation_Standard_X, Ellipse_Definition, Ellipse_Focal_Triangle_Perimeter, Triangle_Area_With_Sin, Triangle_Area_Formula

---

## Problem Index: 6720
**ID**: 6721
**Text**:  
已知$F_{1}$、$F_{2}$，是双曲线$x^{2}-4 y^{2}=4$的两个焦点，$P$是双曲线上的一点，且满足$\overrightarrow{P F_{1}} \cdot \overrightarrow{P F_{2}}=0$，则$\Delta P F_{1} F_{2}$的面积为?

**Process**:  
\because双曲线x^{2}-4y^{2}=4,\therefore双曲线的标准方程:\frac{x2}{4}-y^{2}=1,\thereforea=2,b=1,c=\sqrt{5}设PF_{1}=m,PF_{2}=n,由双曲线的定义可知:|m-n|=4\textcircled{1}\because\overrightarrow{PF}_{1}\cdot\overrightarrow{PF_{2}}=0,\thereforePF_{1}\botPF_{2},由勾股定理可知:m^{2}+n^{2}=(2\sqrt{5})^{2}\textcircled{2}把\textcircled{1}平方,然后代入\textcircled{2},求得mn=2,\thereforeAPF_{1}F_{2}的面积为S=\frac{1}{2}mn=1,

**Theorem Sequence**:  
Hyperbola_Equation_Standard_X, Hyperbola_Definition, Ellipse_Focal_Triangle_Perimeter, Triangle_Area_Formula

---

## Problem Index: 6752
**ID**: 6753
**Text**:  
点$F_{1}$、$F_{2}$分别为椭圆$E$: $\frac{x^{2}}{a^{2}}+\frac{y^{2}}{b^{2}}=1  (a>b>0)$的左、右焦点，点$A$、$B$、$C$在椭圆$E$上，满足$\overrightarrow{A F_{1}}=\overrightarrow{F_{1} B}$，$\overrightarrow{A F_{2}}=2 \overrightarrow{F_{2} C}$，则椭圆$E$的离心率为?

**Process**:  
如图,因为\overrightarrow{AF}=\overrightarrow{F_{1}B},由椭圆的对称性可得AB\botF_{1}F_{2},不妨设A在x轴上方则x_{A}=-c,故y_{A}=\frac{b^{2}}{a}而\overrightarrow{AF_{2}}=2\overrightarrow{F_{2}C},故x_{C}-c=\frac{1}{2}\times2c,即x_{C}=2c,且y_{C}=-\frac{b^{2}}{2a}将C的坐标代入椭圆方程得到:\frac{4c^{2}}{a^{2}}+\frac{b^{2}}{4a^{2}}=1整理得到:4e^{2}+\frac{1-e^{2}}{4}=1,解得e=\frac{\sqrt{5}}{5}

**Theorem Sequence**:  
Ellipse_Equation_Standard_X, Ellipse_Definition, Vector_Collinear_Condition, Eccentricity_Formula

---

## Problem Index: 6767
**ID**: 6768
**Text**:  
双曲线$\frac{x^{2}}{3}-y^{2}=1$的离心率是?

**Process**:  
双曲线\frac{x2}{3}\cdoty^{2}=1的a=\sqrt{3},b=1,

**Theorem Sequence**:  
Hyperbola_Equation_Standard_X, Hyperbola_Parameter_Relation

---

## Problem Index: 6776
**ID**: 6777
**Text**:  
如果抛物线$y^{2}=ax$的准线是直线$x=-1$，那么它的焦点坐标为?

**Process**:  
由抛物线性质可知抛物线的准线方程坐标与焦点的横坐标互为相反数,所以焦点为(1,0)

**Theorem Sequence**:  
Parabola_Equation_Standard_Right, Parabola_Directrix

---

## Problem Index: 6785
**ID**: 6786
**Text**:  
焦点在$x$轴上，焦距等于$4$，且经过点$P(6,0)$的椭圆标准方程是?

**Process**:  
由题易知c=2,a=6,然后根据b^{2}=a^{2}-c^{2}可求得b^{2}的值,最后写出椭圆的方程即可因为椭圆的焦距等于4,故2c=4,所以c=2.又因为椭圆过点P(6,0),所以a=6,所以b^{2}=a^{2}-c^{2}=36-4=32所以椭圆方程为\frac{x^{2}}{36}+\frac{y^{2}}{32}=1

**Theorem Sequence**:  
Ellipse_Equation_Standard_X, Eccentricity_Formula

---

## Problem Index: 6807
**ID**: 6808
**Text**:  
在直线$l$: $x+y-4=0$任取一点$M$,过$M$且以$\frac{x^{2}}{16}+\frac{y^{2}}{12}=1$的焦点为焦点作椭圆,则所作椭圆的长轴长的最小值为?

**Process**:  
椭圆\frac{x^{2}}{16}+\frac{y^{2}}{12}=1的焦点坐标分别为F_{1}(-2,0),F_{2}(2,0),设点F_{2}(2,0)关于直线l:x+y-4=0的对称点为P(x,y),则\frac{\frac{x+2}{2}+\frac{y}{2}}{(\frac{y}{x-2}}=1+\frac{y}{2}-4=0,解得P(4,2),连接PF_{1}交直线l于点M,直线PF_{1}的方程为x-3y+2=0,联立方程组\begin{cases}x+y-4=0\\x-3y+2=0\end{cases}得M(\frac{5}{2}\frac{3}{2})即为满足所作椭圆的长轴长最小,否则在直线l上任取不同于M(\frac{5}{2},\frac{3}{2})的一点Q,|QF_{1}|+|QF_{2}|>|PF_{1}|=|MF_{1}|+|MF_{2}|,设所求的椭圆长轴长为2a,则2a=|PF_{1}|=2\sqrt{10}

**Theorem Sequence**:  
Ellipse_Equation_Standard_X, Eccentricity_Formula

---

## Problem Index: 6822
**ID**: 6823
**Text**:  
方程$\frac{x^{2}}{4}+\frac{y^{2}}{m}=1$表示焦点在$y$轴上的椭圆，其焦点坐标是?

**Process**:  
根据方程\frac{x^{2}}{4}+\frac{y^{2}}{m}=1表示焦点在y轴上的椭圆,确定a^{2}=m,b^{2}=4,再由a,b,c的关系求出c,写出坐标即可.因为方程\frac{x^{2}}{4}+\frac{y^{2}}{m}=1表示焦点在y轴上的椭圆,所以a^{2}=m,b^{2}=4,所以c=\sqrt{a^{2}-b^{2}}=\sqrt{m-4},所以焦点坐标为:(0,\pm\sqrt{m-4})

**Theorem Sequence**:  
Ellipse_Equation_Standard_X, Eccentricity_Formula

---

## Problem Index: 6849
**ID**: 6850
**Text**:  
设抛物线$x^{2}=p y$的焦点与双曲线$\frac{y^{2}}{3}-x^{2}=1$的上焦点重合, 则$p$的值为?

**Process**:  
由题,抛物线的焦点为(0,\frac{p}{4}),双曲线的焦点为(0,2),即\frac{p}{4}=2,所以p=8,

**Theorem Sequence**:  
Parabola_Equation_Standard_Up, Hyperbola_Equation_Standard_Y, Parabola_Directrix

---

## Problem Index: 6852
**ID**: 6853
**Text**:  
已知抛物线$y=a x^{2}$的准线方程为$y=-\frac{1}{2}$，则实数$a$=?

**Process**:  
由题意可知,抛物线y=ax^{2}的标准方程是x^{2}=\frac{1}{a}y',则其准线方程为y=-\frac{1}{4a}=-\frac{1}{2},所以a=\frac{1}{2}

**Theorem Sequence**:  
Parabola_Equation_Standard_Right, Parabola_Directrix

---

## Problem Index: 6864
**ID**: 6865
**Text**:  
已知双曲线方程为$\frac{x^{2}}{9}-\frac{y^{2}}{16}=1$，则该双曲线的渐近线方程为?

**Process**:  
易知双曲线的焦点在x轴上,且a=3,b=4,所以双曲线的渐近线方程为y=\pm\frac{4}{2}x,即4x\pm3y=0

**Theorem Sequence**:  
Hyperbola_Equation_Standard_X, Hyperbola_Asymptote, Point_To_Line_Distance

---

## Problem Index: 6875
**ID**: 6876
**Text**:  
若点$P$是抛物线$y^{2}=2 x$上的一个动点，则点$P$到直线$3 x-4 y+\frac{7}{2}=0$的距离与$P$到该抛物线的准线的距离之和的最小值为?

**Process**:  
如图,过点P分别作抛物线准线和直线3x-4y+\frac{7}{2}=0的垂线PQ、PA,垂足分别为点Q、A,由抛物线的定义可得|PQ|=|PF|,所以,|PA|+|PQ|=|PA|+|PF|\geqslant|AF|_{\min}当A、P、F三点共线时,|AF|取得最小值,|AF|的最小值为点F到直线3x-4y+\frac{7}{2}=0的距离,即|AF|_{\min}=\frac{|3\times\frac{1}{2}+\frac{7}{2}|}{\sqrt{3^{2}+(-4)^{2}}}=1

**Theorem Sequence**:  
Parabola_Equation_Standard_Right, Parabola_Definition, Parabola_Directrix, Point_To_Line_Distance, Two_Points_Distance

---

## Problem Index: 6880
**ID**: 6881
**Text**:  
椭圆$\frac{x^{2}}{m^{2}+1}+\frac{y^{2}}{m^{2}}=1(m>0)$的焦点为$F_{1}$、$F_{2}$，上顶点为$A$，若$\angle F_{1} A F_{2}=\frac{\pi}{3}$，则$m$=?

**Process**:  
由题意,椭圆\frac{x2}{m^{2}+1}+\frac{y^{2}}{m^{2}}=1(m>0),可得a^{2}=m^{2}+1,b^{2}=m^{2}.则c^{2}=a^{2}-b^{2}=1,所以F_{1}(-1,0),F_{2}(1,0),且上顶点A(0,m),如图所示,因为\angleF_{1}AF_{2}=\frac{\pi}{3},可得\angleF_{1}AO=\frac{\pi}{6},则_{\tan\angleF_{1}AO}=\frac{1}{m}=\frac{\sqrt{3}}{3},解得m=\sqrt{3}

**Theorem Sequence**:  
Ellipse_Equation_Standard_X, Ellipse_Focal_Triangle_Perimeter, Triangle_Midline_Theorem

---

## Problem Index: 6930
**ID**: 6931
**Text**:  
双曲线的一个焦点为$(0,5)$，其渐近线方程为$y=\pm \frac{4}{3} x$，则双曲线的标准方程为?

**Process**:  
由题:双曲线的一个焦点为(0,5),其渐近线方程为y=\pm\frac{4}{3}x所以焦点在y轴上,设标准方程为\frac{y^{2}}{a^{2}}-\frac{x^{2}}{b^{2}}=1,(a>0,b>0),且\frac{a}{b}=\frac{4}{3},a^{2}+b^{2}=25,解得:a=4,b=3.所以双曲线的标准方程为\frac{y^{2}}{16}-\frac{x^{2}}{9}=1

**Theorem Sequence**:  
Hyperbola_Equation_Standard_Y, Hyperbola_Asymptote, Eccentricity_Formula

---

## Problem Index: 6983
**ID**: 6984
**Text**:  
已知中心在原点，对称轴为坐标轴的椭圆，其中一个焦点坐标为$F(2,0)$，椭圆被直线$l$: $y=x+3$所截得的弦的中点横坐标为$-2$，则此椭圆的标准方程为?

**Process**:  
设椭圆方程为\frac{x^{2}}{a^{2}}+\frac{y^{2}}{b^{2}}=1(a>b>0),由\begin{cases}\frac{x^{2}}{a^{2}}+\frac{y^{2}}{b^{2}}=1\\y=x+3\end{cases},得(a^{2}+b^{2})x^{2}+6a^{2x+9a}-a^{2}b^{2}=0所以x_{1}+x_{2}=-\frac{6a2}{a^{2}+b^{2}},由题意-\frac{6a2}{a^{2}+b^{2}}=-2\times2,a^{2}=2b^{2}又c=2,所以a^{2}-b^{2}=b^{2}=c^{2}=4,a^{2}=8,椭圆方程为\frac{x^{2}}{8}+\frac{y^{2}}{4}=1.

**Theorem Sequence**:  
Ellipse_Equation_Standard_X, Point_Difference_Method_Hyperbola, Line_Point_Slope_Form, Eccentricity_Formula

---

## Problem Index: 6985
**ID**: 6986
**Text**:  
若椭圆$C$:$ \frac{x^{2}}{8}+\frac{y^{2}}{4}=1$的右焦点为$F$，且与直线$l$: $x-\sqrt{3} y+2=0$交于$P$、$Q$两点，则$\triangle P Q F$的周长为?

**Process**:  
求出左焦点坐标,利用直线经过椭圆的左焦点,结合椭圆的定义求三角形的周长即可.由题得椭圆C的左焦点F(-2,0)所以直线l:x-\sqrt{3}y+2=0经过左焦点F.\therefore\DeltaPQF的周长|PQ|+|PF|+|QF|=|PF|+|PF|+|QF|+|QF|=4a=8\sqrt{2}

**Theorem Sequence**:  
Ellipse_Equation_Standard_X, Ellipse_Definition, Triangle_Midline_Theorem

---

## Problem Index: 7018
**ID**: 7019
**Text**:  
已知$O$为坐标原点，抛物线$C$: $y^{2}=2 p x(p>0)$的焦点为$F$、$P$为$C$上一点，$P F$与$x$轴垂直，$Q$为$y$轴上一点，且$P Q \perp O P$，若$|P Q|=\sqrt{5}$，则抛物线$C$的准线方程为?

**Process**:  
抛物线C:y^{2}=2px(p>0)的焦点F(\frac{p}{2},0)由抛物线C的对称性,不妨取P(\frac{p}{2},p),则k_{OP}=\frac{p-0}{\frac{P}{2}-0}=2由PQ\botOP,可知k_{PQ}=-\frac{1}{2},直线PQ方程可设为y=-\frac{1}{2}(x-\frac{p}{2})+p=-\frac{1}{2}x+\frac{5}{4}p,则Q(0,\frac{5}{4}p),故有PQ=\sqrt{(\frac{p}{2}-0)^{2}+(\frac{5p}{4}-p)^{2}}=\frac{\sqrt{5}}{4}p=\sqrt{5}故p=4,则抛物线C的准线方程为x=-2

**Theorem Sequence**:  
Parabola_Equation_Standard_Right, Parabola_Directrix, Vector_Collinear_Condition

---

## Problem Index: 7039
**ID**: 7040
**Text**:  
抛物线$y=a x^{2}$的准线方程为$y=1$，则焦点坐标是?

**Process**:  
y=ax^{2}\Rightarrowx^{2}=\frac{1}{a}y\Rightarrowy=-\frac{1}{4a},所以-\frac{1}{4a}=1,F(0,\frac{1}{4a})即F(0,-1)

**Theorem Sequence**:  
Parabola_Equation_Standard_Right, Parabola_Directrix

---

## Problem Index: 7042
**ID**: 7043
**Text**:  
直线$x+2 y-2=0$经过椭圆$\frac{x^{2}}{a^{2}}+\frac{y^{2}}{b^{2}}=1(a>b>0)$的一个焦点和一个顶点，则该椭圆的方程等于?

**Process**:  
对直线x+2y-2=0,令x=0,解得y=1;令y=0,解得x=2,故椭圆的右焦点坐标为(2,0),上顶点坐标为(0,1)则c=2,b=1,则a=\sqrt{b^{2}+c^{2}}=\sqrt{5}故椭圆的方程等于\frac{x^{2}}{5}+y^{2}=1.

**Theorem Sequence**:  
Ellipse_Equation_Standard_X, Eccentricity_Formula

---

## Problem Index: 7064
**ID**: 7065
**Text**:  
已知$O$为坐标原点，抛物线$C$: $y^{2}=8 x$的焦点为$F$、$P$为$C$上一点，$P F$与$x$轴垂直，$Q$为$x$轴上一点，若$P$在以线段$O Q$为直径的圆上，则点$Q$的坐标为?

**Process**:  
点F(2,0),可令P(2,4),设Q(t,0)由OP\botPQ得:\frac{4}{2}\cdot\frac{0-4}{t-2}=-1,解得t=10

**Theorem Sequence**:  
Parabola_Equation_Standard_Right, Vector_Collinear_Condition, Circle_Standard_Equation

---

## Problem Index: 7121
**ID**: 7122
**Text**:  
直线$l$经过点$A(t, 0)$，且与曲线$y=x^{2}$相切，若直线$l$的倾斜角为$45^{\circ}$，则$t$=?

**Process**:  
若直线l的倾斜角为45^{\circ},则直线的斜率为1,所以1:y=x-t,联立\begin{cases}y=x-t\\y=x^{2}\end{cases},消y得:x^{2}-x+t=0.因为直线与曲线相切,所以\triangle=(-1)^{2}-4t=0,\thereforet=\frac{1}{4}

**Theorem Sequence**:  
Parabola_Equation_Standard_Right, Ellipse_Tangent_Line, Point_Difference_Method_Hyperbola, Discriminant_Delta

---

## Problem Index: 7123
**ID**: 7124
**Text**:  
抛物线$y=2 x^{2}$的焦点坐标?

**Process**:  
由题意知x^{2}=\frac{1}{2}y,所以抛物线的焦点在y轴正半轴上,且坐标为(0,\frac{1}{8})

**Theorem Sequence**:  
Parabola_Equation_Standard_Right, Parabola_Directrix

---

## Problem Index: 7149
**ID**: 7150
**Text**:  
已知$F_{1}$、$F_{2}$分别是双曲线$E$: $\frac{x^{2}}{a^{2}}-\frac{y^{2}}{b^{2}}=1(a>0, b>0)$的左、右焦点，过点$F_{1}$的直线$l$与$E$仅有一个公共点，且$l$与$\odot O$: $x^{2}+y^{2}=2 a^{2}$相切，则该双曲线的离心率为?

**Process**:  
双曲线E:\frac{x^{2}}{a^{2}}-\frac{y^{2}}{b^{2}}=1(a>0,b>0)的渐近线方程为y=\pm\frac{b}{a}x,过点F_{1}的直线l与E仅有一个公共点,可得直线l平行于渐近线,可得直线l的方程为y=\pm\frac{b}{a}(x+c),且l与\odotO:x^{2}+y^{2}=2a^{2}相切,可得\frac{bc}{\sqrt{a^{2}+b^{2}}}=b=\sqrt{2}a则双曲线的e=\frac{c}{a}=\sqrt{1+\frac{b^{2}}{a^{2}}}=\sqrt{3}

**Theorem Sequence**:  
Hyperbola_Equation_Standard_X, Hyperbola_Asymptote, Circle_Standard_Equation, Eccentricity_Formula

---

## Problem Index: 7160
**ID**: 7161
**Text**:  
设$P$是抛物线$y^{2}=4 x$上的一个动点，$F$为抛物线的焦点，点$A(6,3)$，则$|P A|+|P F|$的最小值为?

**Process**:  
设点P在准线上的射影为D,则根据抛物线的定义可知|PF|=|PD|,进而把问题转化为求|PA|+|PD|的最小值,进而可推断出当D、P、A三点共线时|PA|+|PD|最小,则答案可得设点P在准线上的射影为D,则根据抛物线的定义可知|PF|=|PD|.所以,要求|PA|+|PF|取得最小值,即求|PA|+|PD|取得最小当D、P、A三点共线时PA+|PD|最小为6-(-1)=7.

**Theorem Sequence**:  
Parabola_Equation_Standard_Right, Parabola_Definition, Parabola_Directrix, Two_Points_Distance

---

## Problem Index: 7178
**ID**: 7179
**Text**:  
已知双曲线$\frac{x^{2}}{a^{2}}-\frac{y^{2}}{b^{2}}=1(a>0, b>0)$的一条渐近线方程为$y=k x(k>0)$，离心率为$2$，则$k$的值为?

**Process**:  
由于y=kx(k>0))双曲线的一条渐近线,则k=\frac{b}{a}又e=\frac{c}{a}=\sqrt{1+(\frac{b}{a})^{2}}=2所以\frac{b}{a}=\sqrt{3},则k=\sqrt{3}.数答安为:,,--

**Theorem Sequence**:  
Hyperbola_Equation_Standard_X, Hyperbola_Asymptote, Eccentricity_Formula

---

## Problem Index: 7185
**ID**: 7186
**Text**:  
过点$P(2,1)$的直线与双曲线$\frac{y^{2}}{2}-x^{2}=1$交于$A$、$B$两点，则以点$P$为中点的弦$A B$所在直线斜率为?

**Process**:  
设A(x_{1},y_{1}),B(x_{2},y_{2})则\begin{cases}\frac{y_{2}}{2}-x_{1}=1\\\frac{y_{2}^{2}-x_{2}}{2}=1\\两式相减得:x_{2}-y_{1}=2\frac{x_{1}+x_{2}}{y_{1}+y}=\frac{4}{1}=4,\end{cases},即k=4经检验,当k=4时,直线与又又曲线相交所以填4的时)本题主要考查了直线与双曲线的位置关系,点差法,属于中档题

**Theorem Sequence**:  
Hyperbola_Equation_Standard_X, Point_Difference_Method, Midpoint_Formula

---

## Problem Index: 7187
**ID**: 7188
**Text**:  
已知椭圆$\frac{x^{2}}{4}+\frac{y^{2}}{3}=1$的左、右两个焦点分别为$F_{1}$、$F_{2}$，若经过$F_{1}$的直线$l$与椭圆相交于$A$、$B$两点，则$\triangle A B F_{2}$的周长等于?

**Process**:  
由\frac{x^{2}}{4}+\frac{y^{2}}{3}=1得a=2,则\triangleABF_{2}的周长等于AB+AF_{2}+BF_{2}=AF_{1}+BF_{1}+AF_{2}+BF_{2}=4a=8

**Theorem Sequence**:  
Ellipse_Equation_Standard_X, Ellipse_Definition

---

## Problem Index: 7188
**ID**: 7189
**Text**:  
设$A$是抛物线$C$: $y^{2}=12 x$上一点，若$A$到$C$的焦点的距离为$10$，则$A$到$y$轴的距离为?

**Process**:  
设抛物线的焦点为F,因为点A到C的焦点的距离为10,所以由抛物线的定义知|AF|=x_{A}+\frac{p}{2}=x_{A}+3=10,解得x_{A}=7,所以点A到v轴的距离为7为答安为

**Theorem Sequence**:  
Parabola_Equation_Standard_Right, Parabola_Focal_Radius

---

## Problem Index: 7192
**ID**: 7193
**Text**:  
双曲线$\frac{y^{2}}{3}-\frac{x^{2}}{2}=1$的焦点坐标为?

**Process**:  
根据双曲线的标准方程直接求解即可.由\frac{y^{2}}{3}-\frac{x^{2}}{2}=1,可知焦点在y轴上a^{2}=3,b^{2}=2,所以c^{2}=a^{2}+b^{2}=5,即c=\sqrt{5}所以双曲线的焦点坐标为(0,\pm\sqrt{5})

**Theorem Sequence**:  
Hyperbola_Equation_Standard_Y, Hyperbola_Parameter_Relation

---

## Problem Index: 7216
**ID**: 7217
**Text**:  
已知双曲线$C$: $\frac{x^{2}}{a^{2}}-\frac{y^{2}}{b^{2}}=1(a>0, b>0)$的离心率为$2$，焦点到渐近线的距离为$\sqrt{3}$，则双曲线$C$的焦距为?

**Process**:  
因为双曲线的离心率为2,焦点(c,0)到渐近线bx-ay=0的距离为\sqrt{3},所以\frac{|\frac{c}{a}}{\sqrt{a^{2}+b^{2}}}=\sqrt{3},解得b=\sqrt{3},a=1,c=2,所以双曲线的焦距为4.

**Theorem Sequence**:  
Hyperbola_Equation_Standard_X, Hyperbola_Asymptote, Point_To_Line_Distance, Eccentricity_Formula

---

## Problem Index: 7235
**ID**: 7236
**Text**:  
已知椭圆方程为$\frac{x^{2}}{2}+y^{2}=1$, 则过点$P(\frac{1}{2}, \frac{1}{2})$且被$P$平分的弦所在直线的方程为?

**Process**:  
设这条弦与椭圆\frac{x^{2}}{2}+y^{2}=1交于点A(x_{1}y_{1})B(x_{2}y_{2})由中点坐标公式知x_{1}+x_{2}=1,y_{1}+y_{2}=1,把A(x_{1}y_{1})B(x_{2}y_{2})代入\frac{x^{2}}{2}+y^{2}=1,作差整理得(x_{1}-x_{2})+2(y_{1}-y_{2})=0,\thereforek_{AB}=\frac{y_{1}-y_{2}}{x_{1}-x_{2}}=-\frac{1}{2}\therefore这条弦所在的直线方程为y-\frac{1}{2}=-\frac{1}{2}(x-\frac{1}{2})即2x+4y-3=0,

**Theorem Sequence**:  
Ellipse_Equation_Standard_X, Point_Difference_Method, Midpoint_Formula

---

## Problem Index: 7237
**ID**: 7238
**Text**:  
设焦点为$F_{1}$、$F_{2}$的椭圆$\frac{x^{2}}{a^{2}}+\frac{y^{2}}{3}=1(a>0)$上的一点$P$也在拋物线$y^{2}=\frac{9}{4} x$上，抛物线焦点为$F_{3}$，若$|P F_{3}|=\frac{25}{16}$，则$\triangle P F_{1} F_{2}$的周长为?

**Process**:  
设P(x_{0},y_{0}),则x_{0}+\frac{9}{16}=\frac{25}{16},所以x_{0}=1,代入抛物线方程,得y_{0}=\pm\frac{3}{2},不妨设点P的坐标为(1,\frac{3}{2}),代入椭圆方程,得a^{2}=4,所以\trianglePF_{1}F_{2}的周长为2a+2c=4+2=6

**Theorem Sequence**:  
Ellipse_Equation_Standard_X, Point_Difference_Method_Hyperbola, Discriminant_Delta, Quadratic_Function_Maximum

---

## Problem Index: 7238
**ID**: 7239
**Text**:  
椭圆$9 x^{2}+4 y^{2}=1$的短轴长为?

**Process**:  
椭圆的标准方程为\frac{x^{2}}{9}+\frac{y^{2}}{1}=1,则a=\frac{1}{2},b=\frac{1}{3},因此,椭圆9x^{2}+4y^{2}=1的短轴长为2b=\frac{2}{3}.

**Theorem Sequence**:  
Parabola_Equation_Standard_Right, Parabola_Definition, Parabola_Focal_Radius, Parabola_Directrix, Chord_Length_Formula_With_K

---

## Problem Index: 7311
**ID**: 7312
**Text**:  
已知点$P(1,2)$在抛物线$E$:$ y^{2}=2 p x(p>0)$上，过点$M(1,0)$的直线$l$交抛物线$E$于$A$、$B$两点，若$\overrightarrow{A M}=3 \overrightarrow{M B}$，则直线$l$的倾斜角的正弦值为?

**Process**:  
因为点在抛物线E:y^{2}=2px(p>0)上,所以4=2p\times1,得p=2,所以y^{2}=4x,设过点M(1,0)的直线方程为:x=my+1.所以\begin{cases}x=my+1\\y^{2}=4x\end{cases}所以y^{2}-4my-4=0设A(x_{1},y_{1}),B(x_{2},y_{2}所以y_{1}+y_{2}=4m,y_{1}y_{2}=又因为\overrightarrow{AM}=3\overrightarrow{MB},所以-y_{1}=3y_{2}所以_{m}=\pm\frac{\sqrt{3}}{3},因为直线的斜率k=\tan\theta=\pm\sqrt{3}由\theta\in(0,\pi),所以\theta=\frac{\pi}{3}或\frac{2\pi}{3},所以\sin\theta=\frac{\sqrt{3}}{2}

**Theorem Sequence**:  
Parabola_Equation_Standard_Right, Substitution_x_equals_my_plus_n, Vieta_Theorem_Sum, Vieta_Theorem_Product, Vector_Collinear_Condition, Triangle_Midline_Theorem

---

## Problem Index: 7317
**ID**: 7318
**Text**:  
已知双曲线$C$: $\frac{x^{2}}{a^{2}}-\frac{y^{2}}{b^{2}}=1(a>0 , b>0)$的一条渐近线与直线$l$: $x+\sqrt{3} y=0$垂直，$C$的一个焦点到$l$的距离为$1$, 则$C$的方程为?

**Process**:  
由已知,一条渐近线方程为\sqrt{3}x-y=0,即b=\sqrt{3}a又\frac{c}{\sqrt{3+1}}=1,故c=2,即a^{2}+b^{2}=4,解得a=1,b=\sqrt{3}双曲线方程为x^{2}-\frac{y^{2}}{3}=1

**Theorem Sequence**:  
Hyperbola_Equation_Standard_X, Hyperbola_Asymptote, Hyperbola_Parameter_Relation

---

## Problem Index: 7349
**ID**: 7350
**Text**:  
已知$F_{1}$、$F_{2}$是椭圆$C$的两个焦点，$P$是$C$上的一点. 若$\overrightarrow{P F_{1}} \cdot \overrightarrow{P F_{2}}=0$且$|P F_{1}|=2|P F_{2}|$，则$C$的离心率为?

**Process**:  
由椭圆的定义有|PF_{1}|+|PF_{2}|=2a,|F_{1}F_{2}|=2c,又|PF_{1}|=2|PF_{2}|,则|PF_{1}|=\frac{4a}{3},|PF_{2}|=\frac{2a}{3},又\overrightarrow{PF}_{1}\cdot\overrightarrow{PF_{2}}=0,则|PF_{1}|^{2}+|PF_{2}|^{2}=|F_{1}F_{2}^{2}|\frac{a^{2}}{a}=4c^{2},\cdot离心率e=\frac{c}{a}=\frac{\sqrt{5}}{3}

**Theorem Sequence**:  
Ellipse_Equation_Standard_X, Ellipse_Definition, Ellipse_Focal_Triangle_Perimeter, Eccentricity_Formula

---

## Problem Index: 7380
**ID**: 7381
**Text**:  
抛物线$C$的顶点在坐标原点，焦点在坐标轴上，且$C$过点$(-2,3)$，则$C$的方程是?

**Process**:  
(1)当抛物线的顶点在坐标原点,对称轴是x轴时设它的标准方程为y^{2}=-2px(p>0),代入点(-2,3)\therefore9=4p可得2p=\frac{9}{2}\thereforey^{2}=-\frac{9}{2}x(2)当对称轴是y轴,设抛物线的方程为x^{2}=2py(p>0)代入点(-2,3)\therefore4=6p可得2p=\frac{4}{3}\therefore抛物线的方程为x^{2}=\frac{4}{3}y综上可知求抛物线的标准方程为y^{2}=-\frac{9}{2}x或x^{2}=\frac{4}{3}y

**Theorem Sequence**:  
Parabola_Equation_Standard_Right, Parabola_Equation_Standard_Up

---

## Problem Index: 7387
**ID**: 7388
**Text**:  
已知$A(1, \frac{1}{2})$, $B(-1, \frac{1}{2})$，直线$A M$的斜率与直线$B M$的斜率之差是$1$，点$F(0, \frac{1}{2})$, $P$是直线$l$: $y=-\frac{1}{2}$上的一点，$Q$是直线$P F$与点$M$的轨迹$C$的交点，且$\overrightarrow{F P}=4 \overrightarrow{F Q}$，则$|Q F|$=?

**Process**:  
设M(x,y),则_{k_{AM}}-k_{BM}=\frac{y-\frac{1}{2}}{x-1}-\frac{y-\frac{1}{2}}{x+1}=1导点M的轨迹C的方程是x^{2}=2y(x\neq\pm1),如下图所示:设点P(t,-\frac{1}{2}),Q(x_{0},y_{0}),\overrightarrow{FP}=(t,-1),\overrightarrow{FQ}=(x_{0},y_{0}-\frac{1}{2}),\because\overrightarrow{FP}=4\overrightarrow{FQ},\therefore4(y_{0}-\frac{1}{2})=-1,解得y_{0}=\frac{1}{4}.由抛物线的定义可得|QF|=\frac{1}{4}+\frac{1}{2}=\frac{3}{4}

**Theorem Sequence**:  
Parabola_Equation_Standard_Right, Point_Difference_Method, Midpoint_Formula, Vector_Collinear_Condition, Triangle_Midline_Theorem

---

## Problem Index: 7401
**ID**: 7402
**Text**:  
已知直线$y=1-x$与双曲线$a x^{2}+b y^{2}=1(a>0, b<0)$的渐近线交于$A$、$B$两点，且过原点和线段$A B$中点的直线的斜率为$-\frac{\sqrt{3}}{2}$，则$\frac{a}{b}$=?

**Process**:  
根据双曲线方程表示出双曲线的渐近线方程,与直线方程联立可得A,B两点坐标,利用中点坐标公式求得中点M的坐标.即可由直线斜率公式求得\frac{a}{b}.[详解]双曲线ax^{2}+by^{2}=1(a>0,b<0)所以其渐近线方程为y=\pm\sqrt{\frac{a}{-b}}\cdotx因为直线y=1-x与渐近线交于A,B两点则\begin{cases}y=1-x\\y=\pm\sqrt{\frac{a}{-b}}\end{cases}.即两个交点坐标为A.\frac{-}{1}设A,B中点坐标为M则由中点坐标公式可得M(\frac{1}{1+\frac{a}{k}},\frac{1}{1}由题意k_{OM}=-\frac{\sqrt{3}}{2}则_{k_{OM}}=\frac{y_{M}}{x_{M}}=\frac{a}{b}=-\frac{\sqrt{3}}{2}

**Theorem Sequence**:  
Hyperbola_Equation_Standard_X, Hyperbola_Asymptote, Point_Difference_Method_Hyperbola, Triangle_Midline_Theorem

---

## Problem Index: 7407
**ID**: 7408
**Text**:  
已知$F$是抛物线$C$: $y=2 x^{2}$的焦点，点$P(x , y)$在抛物线$C$上，且$x=1$，则$| P F |$=?

**Process**:  
由y=2x^{2},得x^{2}=\frac{1}{2}y,则p=\frac{1}{4};由x=1得y=2,由抛物线的性质可得|PF|=2+\frac{p}{2}=2+\frac{1}{8}=\frac{17}{8}

**Theorem Sequence**:  
Parabola_Equation_Standard_Right, Parabola_Focal_Radius

---

## Problem Index: 7411
**ID**: 7412
**Text**:  
双曲线$y^{2}-\frac{x^{2}}{3}=1$的渐近线方程是?

**Process**:  
由题意得y^{2}-\frac{x^{2}}{3}=0,得y=\pm\frac{\sqrt{3}}{3}x所以双曲线y^{2}-\frac{x^{2}}{3}=1的渐近线方程是y=\pm\frac{\sqrt{3}}{3}x

**Theorem Sequence**:  
Hyperbola_Equation_Standard_Y, Hyperbola_Asymptote

---

## Problem Index: 7412
**ID**: 7413
**Text**:  
抛物线$x^{2}=4 \sqrt{3} y$的焦点坐标为?

**Process**:  
抛物线x^{2}=4\sqrt{3}y的焦点坐标(0,\sqrt{3}).

**Theorem Sequence**:  
Parabola_Equation_Standard_Up, Parabola_Directrix

---

## Problem Index: 7413
**ID**: 7414
**Text**:  
曲线$x^{2}-\frac{y^{2}}{3}=1$与直线$y=k x+1$有两个交点，则$k$的取值范围?

**Process**:  
把y=kx+1代入双曲线的方程得(3-k^{2})x^{2}-2kx-4=0,当k=\pm\sqrt{3}时,直线和曲线相交于一个交点,不满足题意,所以舍去当k\neq\pm\sqrt{3}时,A=4k^{2}+16(3-k^{2})=-12k^{2}+48>0,所以-2<k<2.所以k的取值范围为-2<k<2且k\neq\pm\sqrt{3}

**Theorem Sequence**:  
Hyperbola_Equation_Standard_X, Point_Difference_Method_Hyperbola, Discriminant_Delta, Quadratic_Function_Maximum

---

## Problem Index: 7448
**ID**: 7449
**Text**:  
已知椭圆$C$: $\frac{x^{2}}{a^{2}}+\frac{y^{2}}{b^{2}}=1(a>b>0)$的左焦点是点$F$，过原点倾斜角为$\frac{\pi}{3}$的直线$l$与椭圆$C$相交于$M$、$N$两点，若$\angle MFN=\frac{2 \pi}{3}$，则椭圆$C$的离心率是?

**Process**:  
设右焦点为F,设直线l的方程为:y=\sqrt{3}x,设M(x_{0},y_{0}),N(-x_{0},-y_{0}),利用几何性质可得\angleFMF'=\frac{\pi}{3},结合焦点三角形的性质和余弦定理可得s_{\triangleMFF}=\frac{\sqrt{3}}{3}b^{2}=c|y_{0}|'求出M的坐标后代入椭圆方程可求离心率.设右焦点为F,由题意可得直线l的方程为:y=\sqrt{3}x,设M(x_{0},y_{0}),N(-x_{0},-y_{0})连接MF',NF,因为\angleMFN=\frac{2\pi}{3}所以四边形FMFN为平行四边形,则\angleFMF=\frac{\pi}{3}所以4c^{2}=|MF|^{2}+|MF|^{2}-2|MF||MF|\cos\frac{\pi}{3},整理得到4c^{2}=(|MF|+|MF|)^{2}-3|MF||MF|即|MF||MF|=\frac{4b^{2}}{3}故s_{\DeltaMFF}=\frac{1}{2}\times\frac{\sqrt{3}}{2}\times\frac{4b^{2}}{3}=\frac{\sqrt{3}}{3}b^{2}=\frac{1}{2}\times2c\times|y_{0}|所以可得y_{0}=\frac{\sqrt{3}b^{2}}{3c},代入直线l的方程可得x_{0}=\frac{b^{2}}{3c}将M的坐标代入椭圆的方程可得:\frac{b^{4}}{\frac{9c^{2}}{a^{2}}}+\frac{b^{2}}{3c^{2}}=1'整理可得:4a^{4}-14a^{2}c^{2}+c^{4}=0,即e^{4}-14e^{2}+4=0,解得:e^{2}=7\pm3\sqrt{5},由椭圆的离心率e\in(0,1),所以_{e}=\sqrt{7-3\sqrt{5}}=\frac{3\sqrt{2}-\sqrt{10}}{2}

**Theorem Sequence**:  
Ellipse_Equation_Standard_X, Ellipse_Definition, Ellipse_Focal_Triangle_Area, Ellipse_Focal_Triangle_Perimeter, Triangle_Area_With_Sin, Eccentricity_Formula

---

## Problem Index: 7450
**ID**: 7451
**Text**:  
抛物线$y=2 a x^{2}(a>0)$上一点$A(m, \frac{3}{4})$到其焦点$F$的距离为$1$，则$a$的值为?

**Process**:  
】将抛物线方程化为标准方程,利用抛物线的定义将抛物线上的点到焦点的距离转化为到准线的距离,再利用点到直线的距离公式进行求解.将抛物线y=2ax^{2}(a>0)化为x^{2}=\frac{1}{2a}y(a>0)由抛物线定义得点A(m,\frac{3}{4})到准线l:y=-\frac{1}{8a}的距离为1即\frac{3}{4}+\frac{1}{8a}=1,解得a=\frac{1}{2}

**Theorem Sequence**:  
Parabola_Equation_Standard_Right, Ellipse_Tangent_Line, Parabola_Directrix, Basic_Inequality

---

## Problem Index: 7482
**ID**: 7483
**Text**:  
已知椭圆$C$: $\frac{x^{2}}{a^{2}}+\frac{y^{2}}{b^{2}}=1(a>b>0)$的左右焦点为$F_{1}$, $F_{2}$, $|F_{1} F_{2}|=4 \sqrt{5}$，点$P$为椭圆上一点，若$\Delta P F_{1} F_{2}$周长为$4 \sqrt{5}+12$，则椭圆$C$的离心率为?

**Process**:  
设椭圆的半焦距为c,由题意得,\begin{cases}2a+2c=4\sqrt{5}+12\\2c=4\sqrt{5}\end{cases}\Rightarrow\begin{cases}c=2\sqrt{5}\\a=6\end{cases},所以e=\frac{c}{a}=\frac{\sqrt{5}}{3},

**Theorem Sequence**:  
Ellipse_Equation_Standard_X, Ellipse_Definition, Eccentricity_Formula

---

## Problem Index: 7503
**ID**: 7504
**Text**:  
已知双曲线$C$: $\frac{x^{2}}{a^{2}}-\frac{y^{2}}{b^{2}}=1  (a>0 , b>0)$的左、右焦点分别是$F_{1}$、$F_{2}$、$M$是$C$右支上一点，设$\angle F_{1} M F_{2}=\theta$. 若$\overrightarrow{M F_{1}} \cdot \overrightarrow{M F_{2}}=4 b^{2}$，则$\cos \theta$=?

**Process**:  
|MF_{1}|-|MF_{2}|=2a,4c^{2}=|MF_{1}|^{2}+|MF_{2}|^{2}-2|MF_{1}|\cdot|MF_{2}|\cos\theta=(|MF_{1}|-|MF_{2}|)^{2}+2|MF_{1}|\cdot|MF_{2}|-8b^{2}即4c^{2}=4a^{2}+2|MF_{1}|\cdot|MF_{2}|-8b^{2},得到|MF_{1}|\cdot|MF_{2}|=6b^{2}\cos\theta=\frac{\overrightarrow{MF_{1}}\cdot\overrightarrow{MF_{2}}}{|MF\bot|MF_{2}|^{2}}=\frac{4b^{2}}{6b^{2}}=\frac{2}{3}

**Theorem Sequence**:  
Hyperbola_Equation_Standard_X, Hyperbola_Definition, Ellipse_Focal_Triangle_Perimeter, Triangle_Area_With_Sin

---

## Problem Index: 7524
**ID**: 7525
**Text**:  
若双曲线$C$: $\frac{x^{2}}{a^{2}}-\frac{y^{2}}{b^{2}}=1(a>0, b>0)$的离心率为$\sqrt{10}$，则$\frac{b}{a}$的值为?

**Process**:  
离心率e=\frac{c}{a}=\sqrt{10},即c=\sqrt{10}a又c^{2}=a^{2}+b^{2},所以b=\sqrt{c^{2}-a^{2}}=3a\therefore\frac{b}{a}=3本题正确结果:3

**Theorem Sequence**:  
Hyperbola_Equation_Standard_X, Hyperbola_Asymptote

---

## Problem Index: 7559
**ID**: 7560
**Text**:  
已知椭圆$C$: $\frac{x^{2}}{8}+\frac{y^{2}}{2}=1$与圆$M$: $x^{2}+y^{2}+2 \sqrt{2} x+2-r^{2}=0(0<r<\sqrt{2})$，过椭圆$C$的上顶点$P$作圆$M$的两条切线分别与椭圆$C$相交于$A$、$B$两点 (不同于$P$点)，则直线$P A$与直线$P B$的斜率之积等于?

**Process**:  
圆心为M(-\sqrt{2},0),P(0,\sqrt{2})设切线为y=kx+\sqrt{2},由到直线距离d=\frac{|-\sqrt{2}k+\sqrt{2}|}{\sqrt{1+k^{2}}}=r,(2-r)^{2}k^{2}-4k+(2-r)=0,k_{1}k_{2}=1,

**Theorem Sequence**:  
Ellipse_Equation_Standard_X, Circle_Standard_Equation, Vector_Collinear_Condition

---

## Problem Index: 7566
**ID**: 7567
**Text**:  
若抛物线$N$: $y^{2}=2 p x(p>0)$的焦点$(3,0)$，且直线$x=m(m>0)$与抛物线交于$A$、$B$两点，若$O A \perp O B$($O$为坐标原点)，则$m$的值为?

**Process**:  
因为抛物线N:y^{2}=2px(p>0)的焦点(3,0),所以p=6所以抛物线方程为:y^{2}=12x,由直线x=m(m>0)与抛物线N交于A、B两点,且OA\botOB(O为坐标原点)可得A(m,m),B(m,-m)所以m^{2}=12m,解得m=12.

**Theorem Sequence**:  
Parabola_Equation_Standard_Right, Hyperbola_Latus_Rectum, Vector_Collinear_Condition

---

## Problem Index: 7576
**ID**: 7577
**Text**:  
设$F_{1}$是椭圆$\frac{x^{2}}{4}+y^{2}=1$的左焦点，$O$为坐标原点，点$P$在椭圆上，则$\overrightarrow{P F_{1}} \cdot \overrightarrow{P O}$的最大值为?

**Process**:  
依题意作图,可分析得到当点P为椭圆的右端点时\overrightarrow{PF_{2}}\cdot\overrightarrow{PO}的值最大,从而可求得其最大值.\becauseF_{1}是椭圆\frac{x^{2}}{4}+y^{2}=1的左焦点,显然,当点P为椭圆的右端点时,|\overline{PO}|与|\overline{PF_{1}}|均达到最大值且|\overline{PO}|与|\frac{|PF_{1}|}{|}|同向,\cos<\overrightarrow{PF},\overrightarrow{PO}>=1,也是最大值,\therefore\overrightarrow{PF}_{1}\cdot\overrightarrow{PO}的值最大\therefore|\overrightarrow{PF_{1}}|=a+c=2+\sqrt{3},|\overrightarrow{PO}|=2,\therefore(\overrightarrow{PF}_{1}\cdot\overrightarrow{PO})_{\max}=(2+\sqrt{3})\times2\cos0=4+2\sqrt{3}.

**Theorem Sequence**:  
Ellipse_Equation_Standard_X, Ellipse_Definition, Vector_Collinear_Condition

---

## Problem Index: 7594
**ID**: 7595
**Text**:  
过抛物线$y^{2}=-4 x$的焦点$F$作直线$l$，与抛物线交于$A$、$B$两点，与准线交于$C$点，若$\overrightarrow{F C}=4 \overrightarrow{F B}$，则$|\overrightarrow{A B}|$=?

**Process**:  
焦点坐标为F(-1,0).画出图像如下图所示,作BD垂直准线x=1交准线于D,根据抛物线的定义可知BF=BD,由于\overrightarrow{FC}=4\overrightarrow{FB},所以\frac{BD}{BC}=\frac{BF}{BC}=\frac{1}{3},设直线l的倾斜角为\alpha,则\cos\alpha=\frac{1}{3},所以\tan\alpha=\frac{\sqrt{1-\cos2\alpha}}{\cos\alpha}=2\sqrt{2},即直线l的斜率为2\sqrt{2},所以直线l的方程为y=2\sqrt{2}(x+1),代入抛物线方程并化简得2x^{2}+5x+2=0,所以x_{A}+x_{B}=-\frac{5}{2},所以|\overrightarrow{AB}|=|x_{1}+x_{2}|+p=\frac{5}{2}+2=\frac{9}{2}

**Theorem Sequence**:  
Parabola_Equation_Standard_Right, Parabola_Definition, Parabola_Directrix, Triangle_Midline_Theorem, Chord_Length_Formula_With_K

---

## Problem Index: 7595
**ID**: 7596
**Text**:  
椭圆$k x^{2}+2 y^{2}=2$的一个焦点是$(1,0)$，那么$k$=?

**Process**:  
椭圆kx^{2}+2y^{2}=2的标准方程为:\frac{x^{2}}{k}+y^{2}=1因为一个焦点是(1,0),所以焦点在x轴上,且0<k<2,则a^{2}=\frac{2}{k},b^{2}=1.所以\frac{2}{k}-1=1,解得k=1,

**Theorem Sequence**:  
Ellipse_Equation_Standard_X, Eccentricity_Formula

---

## Problem Index: 7596
**ID**: 7597
**Text**:  
抛物线$y=-4 x^{2}$的焦点坐标为?

**Process**:  
由题意知,x^{2}=-\frac{1}{4}y,则焦点坐标为F(0,-\frac{1}{16})

**Theorem Sequence**:  
Parabola_Equation_Standard_Right, Parabola_Directrix

---

## Problem Index: 7611
**ID**: 7612
**Text**:  
已知椭圆$\frac{x^{2}}{a^{2}}+\frac{y^{2}}{b^{2}}=1(a>b>0)$的左、右焦点分别是$F_{1}$、$F_{2}$、$P$是椭圆上一点，若$|P F_{1}|=2|P F_{2}|$，则椭圆的离心率的取值范围是?

**Process**:  
由椭圆的定义知|PF_{1}|+|PF_{2}|=2a,因为|PF_{1}|=2|PF_{2}|,所以|PF_{2}|=\frac{2}{3}a由于|PF_{2}|\geqslanta-c,所以a-c\leqslant\frac{2a}{3},所以\frac{a}{3}\leqslantc,所以\frac{c}{a}\geqslant\frac{1}{3}故椭圆的离心率的取值范围是[\frac{1}{3},

**Theorem Sequence**:  
Ellipse_Equation_Standard_X, Ellipse_Definition, Ellipse_Eccentricity_Range

---

## Problem Index: 7620
**ID**: 7621
**Text**:  
若直线$2 x-c y+1=0$是抛物线$x^{2}=y$的一条切线，则$c$=?

**Process**:  
根据题意,联立方程即可得到联立直线和抛物线得到\begin{cases}2x-c\\x^{2}=y\end{cases}y+1=0

**Theorem Sequence**:  
Parabola_Equation_Standard_Right, Substitution_x_equals_my_plus_n, Discriminant_Delta

---

## Problem Index: 7634
**ID**: 7635
**Text**:  
已知$A B$是过抛物线$2 x^{2}=y$的焦点的弦，若$|A B|=4$，则$A B$的中点的纵坐标是?

**Process**:  
[解析]设A(x_{1},y_{1}),B(x_{2},y_{2}),根据抛物线的定义得出|AB|=y_{1}+y_{2}+p,得出y_{1}+y_{2},最后由\frac{y_{1}+y_{2}}{2}得出AB的中点的纵坐标.设A(x_{1},y_{1}),B(x_{2},y_{2}),由抛物线2x^{2}=y,可得p=\frac{1}{4}\because|AB|=y_{1}+y_{2}+p=4,\thereforey_{1}+y_{2}=4-\frac{1}{4}=\frac{15}{4},故AB的中点的纵坐标是\frac{y_{1}+y_{2}}{2}=\frac{15}{8}

**Theorem Sequence**:  
Parabola_Equation_Standard_Right, Parabola_Definition, Parabola_Focal_Radius, Vieta_Theorem_Sum

---

## Problem Index: 7645
**ID**: 7646
**Text**:  
已知双曲线$x^{2}-k y^{2}=1$的一个焦点是$(\sqrt{5}, 0)$，则其渐进线方程为?

**Process**:  
由题可知c=\sqrt{5},a^{2}=1,b^{2}=\frac{1}{k}(k>0)\therefore1+\frac{1}{k}=5,解得k=\frac{1}{4},令x^{2}-\frac{1}{1}v2=0,可得渐近线方程为y=\pm2x均答:为\_.

**Theorem Sequence**:  
Hyperbola_Equation_Standard_X, Hyperbola_Asymptote

---

## Problem Index: 7648
**ID**: 7649
**Text**:  
在抛物线$y^{2}=2 x$上的点$P$满足到直线$x-y+3=0$的距离最短，则点$P$的坐标为?

**Process**:  
设P(x_{0},y_{0})是y^{2}=2x上任一点,则点P到直线/的距离d=\frac{|x_{0}-y_{0}+3|}{\sqrt{2}}=\frac{|\frac{y_{2}^{2}}{2}-y_{0}+3|}{\sqrt{2}}=\frac{|(y_{0}-1)^{2}+5|}{2\sqrt{2}}当y_{0}=1时,d_{\min}=\frac{5\sqrt{2}}{4},\thereforeP(\frac{1}{2},1)

**Theorem Sequence**:  
Parabola_Equation_Standard_Right, Ellipse_Tangent_Line, Point_To_Line_Distance, Basic_Inequality

---

## Problem Index: 7654
**ID**: 7655
**Text**:  
双曲线$\frac{x^{2}}{a^{2}}-\frac{y^{2}}{b^{2}}=1(a>0, b>0)$的离心率为$\frac{\sqrt{10}}{2}$，则其渐近线的斜率是?

**Process**:  
\because_{e}=\frac{\sqrt{10}}{2},又e=\frac{c}{a}\therefore4c^{2}=10a^{2},4a^{2}+4b^{2}=10a^{2},即4b^{2}=6a^{2}\thereforek=\pm\frac{b}{a}=\pm\frac{\sqrt{6}}{2}

**Theorem Sequence**:  
Hyperbola_Equation_Standard_X, Hyperbola_Asymptote, Eccentricity_Formula

---

## Problem Index: 7673
**ID**: 7674
**Text**:  
已知抛物线$y=a x^{2}$的准线方程为$y=-2$，则实数$a$的值为?

**Process**:  
将y=ax2化为x^{2}=\frac{1}{a}y'由题意,得\frac{1}{4a}=2,即a=\frac{1}{8}.

**Theorem Sequence**:  
Parabola_Equation_Standard_Right, Parabola_Directrix

---

## Problem Index: 7677
**ID**: 7678
**Text**:  
已知抛物线$y^{2}=12 x$的焦点为$F$，过点$P(2 , 1)$的直线$l$与该抛物线交于$A$、$B$两点，且点$P$恰好为线段$A B$的中点，则$|A F|+| B F |$=?

**Process**:  
设A(x_{1},y_{1}),B(x_{2},y_{2})\becauseP(2,1)是AB中点,\therefore\frac{x_{1}+x_{2}}{2}=2,即x_{1}+x_{2}=4.\becauseF(3,0)是抛物线y^{2}=12x的焦点,\therefore|AF|=x_{1}+3,|BF|=x_{2}+3则|AF|+|BF|=x_{1}+x_{2}+3+3=10,

**Theorem Sequence**:  
Parabola_Equation_Standard_Right, Parabola_Focal_Radius

---

## Problem Index: 7690
**ID**: 7691
**Text**:  
若双曲线的渐近线方程为$y=\pm 2 x$，它的一个焦点是$(\sqrt{5}, 0)$，则双曲线的方程是?

**Process**:  
因为双曲线焦点是(\sqrt{5},0),故该双曲线的焦点在x轴上.设双曲线方程为\frac{x^{2}}{a^{2}}-\frac{y^{2}}{b^{2}}=因为双曲线的渐近线为y=\pm2x,则\begin{cases}\frac{b}{a}=2\\\\a+b^{2}=5\end{cases}则双曲线的方程为x2-\frac{y^{2}}{=1}.

**Theorem Sequence**:  
Hyperbola_Equation_Standard_X, Hyperbola_Asymptote, Hyperbola_Parameter_Relation

---

## Problem Index: 7693
**ID**: 7694
**Text**:  
双曲线的一条渐近线方程是$y=2 x$，且过点$(4,0)$，则双曲线的方程为?

**Process**:  
解析过程略

**Theorem Sequence**:  
None

---

## Problem Index: 7748
**ID**: 7749
**Text**:  
已知双曲线$x^{2}-\frac{y^{2}}{m^{2}}=1(m>0)$的一条渐近线方程为$x+\sqrt{3} y=0$, 则$m$=?

**Process**:  
x^{2}-\frac{y^{2}}{m^{2}}=1渐近线方程为x^{2}-\frac{y^{2}}{m^{2}}=0,所以\frac{1}{m^{2}}=(\sqrt{3})^{2}\becausem>0\thereforem=\frac{\sqrt{3}}{3}.

**Theorem Sequence**:  
Hyperbola_Equation_Standard_X, Hyperbola_Asymptote

---

## Problem Index: 7749
**ID**: 7750
**Text**:  
椭圆$2 x^{2}+y^{2}=1$的焦距为?

**Process**:  
2x^{2}+y^{2}=1可化为\frac{x^{2}}{2}+y^{2}=1,设焦距为2c,则c=\sqrt{1-\frac{1}{2}}=\frac{\sqrt{2}}{2},则焦距2c=\sqrt{2}

**Theorem Sequence**:  
Ellipse_Equation_Standard_X, Eccentricity_Formula

---

## Problem Index: 7755
**ID**: 7756
**Text**:  
若抛物线$x^{2}=8 y$上的点$P$到焦点的距离为$12$，则$P$到$x$轴的距离是?

**Process**:  
因为抛物线x^{2}=8y所以焦点坐标为(0,2),准线方程为y=-2因为点P到焦点的距离为12,根据抛物线定义,则P到准线的距离也为12所以点P到x轴的距离为10

**Theorem Sequence**:  
Parabola_Equation_Standard_Right, Parabola_Definition, Parabola_Directrix

---
