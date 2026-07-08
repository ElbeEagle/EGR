# Theorems V2 第五阶段 Quantity 与语义漂移报告

## 1. 本阶段实现

本阶段新增 canonical Quantity 层，将原先分散的长度、距离、点线距离、面积、斜率、点积、半径和倾角统一表示为：

QuantityValueOf(QuantityRef(kind, subjects...)) = value

旧 predicate 保留，因此前四阶段仍可复现。Quantity closure 还会把定理产生的 DistanceFormulaOf、SlopeFormulaOf、CoordinateAreaFormulaOf、DotProductFormulaOf 和圆半径回写到 canonical quantity 索引。

新增坐标传播：

- 已知准线表达式与命名 DirectrixOf 联合生成 LineNormalFormOf；
- Directrix(G) 作为虚拟直线实体化；
- 圆心到切线的投影生成 TangentPoint 坐标；
- CircleStandardForm 和命名 CenterPointOf 均可提供圆心；
- Radius、Length、Inclination、TangentRelation 等原始事实进入 typed state。

## 2. 新增 executor

新增 10 个 concrete executor，V2 concrete 数量由 62 增至 72：

- 焦点三角形面积：30、31；
- 抛物线焦点弦：33、34、35、36；
- 椭圆中点弦斜率：40；
- 向量点积几何式：60；
- 直线截距式：74；
- 圆切线条件：76。

仍保持 specification-only 的模型：

63、64、68、69、70、71、77、79。

这些模型不是因为代码量大而暂缓，而是训练序列中的实际语义与 catalog 名称尚未对齐。

## 3. 全量评估

数据仍为 5,355 题、20,212 个步骤。

| 指标 | 第四阶段 62 concrete | 第五阶段 72 concrete |
| --- | ---: | ---: |
| APPLIED + ALREADY_KNOWN | 4,154 | 4,172 |
| SPECIFICATION_ONLY | 1,401 | 1,142 |
| 全步骤裸 apply 率 | 20.55% | 20.64% |
| concrete 步骤裸 apply 率 | 22.08% | 21.88% |
| 裸序列完整跑通 | 298 (5.56%) | 298 (5.56%) |
| 纠错后完整跑通 | 489 (9.13%) | 490 (9.15%) |
| 未解析事实 atom | 4,908 | 4,288 |

新增 executor 的裸测状态：

- model 33：8 APPLIED；
- model 34：1 APPLIED；
- model 36：2 APPLIED；
- model 74：1 APPLIED；
- model 76：1 APPLIED；
- models 30、31、35、40、60：0 APPLIED。

纵向单元测试均通过，因此低命中反映的是训练事实和序列前置条件不足，不应通过放松 matcher 解决。

## 4. 主要 concern

### 4.1 标签不是同一抽象层

剩余模型混合了三类动作：

- 数学定理：中位线、内切圆半径；
- 代数策略：基本不等式、均值不等式取等；
- 求解操作：齐次化、二次函数极值。

把三类动作都作为同一种 theorem executor，会使 applicator 的输入输出契约失真。建议后续拆为 TheoremAction、AlgebraTactic 和 GeometryConstruction。

### 4.2 训练标签存在语义漂移

典型例子：

- model 68 名为 Triangle_Midline_Theorem，但大量样本实际使用抛物线准线投影和比例关系；
- model 79 名为 Quadratic_Function_Maximum，但样本主要使用判别式判断直线与双曲线交点；
- model 77 名为 Homogenization_Eccentricity，在样本中承担多种无统一前置条件的代数化简；
- model 63 Basic_Inequality 常对应整段最值推理，而不是单个 a+b>=2sqrt(ab) 状态转换；
- 个别焦点三角形样本在 Ellipse 上先标注 hyperbola 标准式 model 5，导致后续正确 executor 无法获得参数。

### 4.3 剩余 specification-only 构成覆盖上限

在评估样本中，剩余 1,142 个 specification-only 步骤分布为：

| Model | Steps |
| --- | ---: |
| 63 | 335 |
| 64 | 26 |
| 68 | 320 |
| 69 | 30 |
| 70 | 35 |
| 71 | 43 |
| 77 | 221 |
| 79 | 132 |

如果不先修订标签本体，直接实现这 8 条只会把 SPECIFICATION_ONLY 转成 NO_MATCH，无法有效提升完整序列跑通率。

## 5. 建议下一步

1. 从每个剩余模型分层抽样 30-50 题，建立“catalog 含义 / 文字过程实际动作 / 应有输入输出”三列审计表；
2. 将一个过宽标签拆成多个可执行 action，例如 BasicInequalityApply、CompleteSquare、DiscriminantFeasibility；
3. 为训练序列增加 action_version，并保留原始 models 作为 legacy 标签；
4. 用已实现的 72 个 executor 自动验证新序列，只回灌能够得到 APPLIED 或 ALREADY_KNOWN 的改动；
5. 完成标签迁移后再实现剩余模型，而不是继续追求表面 concrete coverage。

原训练数据未修改，Quantity 评估和序列修复候选均输出为独立文件。
