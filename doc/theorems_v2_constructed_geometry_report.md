# Theorems V2 第四阶段构造几何拓展报告

## 1. 新增信息能力

第四阶段在 structured information space 上增加确定性几何闭包：

- 标准圆锥曲线参数与 FocusOf / VertexSideOf 联合生成焦点、顶点坐标；
- Origin 规范化为 Point2D(0,0)；
- MidPointOf 在端点坐标已知时传播中点坐标；
- LineOf(A,B) 与 LineSegmentOf(A,B) 实体化并记录端点；
- 两端点坐标确定 LineNormalFormOf；
- 两条非平行直线唯一确定交点或垂足坐标；
- Asymptote、Chord、Triangle、Angle、Area 等嵌套对象转为显式 predicate。

闭包只执行唯一、确定且可审计的规范化，不猜测未知构造点，不把文字结论当作坐标。

## 2. 新增定理

新增 11 个 concrete executor，V2 concrete 数量由 51 增至 62：

- 点差法：44、45、46；
- 余弦定理、正弦定理、勾股定理：47、48、49；
- 弦长公式：50、51；
- 三角形面积：56、57、58。

每个 executor 配有 predicate-level requirement。点差法要求交点集合与曲线多项式；弦长公式要求代入得到的 QuadraticPolynomialOf 与 LineNormalFormOf；坐标面积要求三个 PointPositionOf。

## 3. 纵向链

构造点链：

ConicStandardForm + ParameterOf + FocusOf / VertexSideOf
→ GeometryClosure
→ PointPositionOf
→ 距离、斜率、向量、直线与面积 executor

弦长链：

IntersectionOf + LineNormalFormOf + ExpressionPolynomial
→ model 78
→ QuadraticPolynomialOf
→ models 42/43
→ root sum/product
→ models 50/51
→ ChordLengthFormulaOf

点差链：

IntersectionOf(line, conic)
+ ExpressionPolynomial(conic)
→ models 44/45/46
→ auditable point-difference equation

## 4. 全数据集结果

评估数据仍为 5,355 题、20,212 个原始定理步骤。

| 指标 | 第三阶段 51 concrete | 第四阶段 62 concrete |
| --- | ---: | ---: |
| APPLIED + ALREADY_KNOWN | 3,834 | 4,154 |
| SPECIFICATION_ONLY | 3,105 | 1,401 |
| 全步骤裸 apply 率 | 18.97% | 20.55% |
| concrete 步骤裸 apply 率 | 22.41% | 22.08% |
| 裸序列完整跑通 | 284 (5.30%) | 298 (5.56%) |
| 纠错后完整跑通 | 471 (8.80%) | 489 (9.13%) |
| 未解析事实 atom | 6,882 | 4,908 |

新增模型裸测命中：

- model 44：73 APPLIED；
- model 45：22 APPLIED；
- model 46：14 APPLIED；
- model 47：73 APPLIED；
- model 48：2 APPLIED；
- model 49：19 APPLIED；
- model 51：16 APPLIED；
- model 56：85 APPLIED；
- model 57：2 APPLIED；
- model 58：0 APPLIED。

model 58 的 executor 已通过坐标三角形测试，但训练样本中的面积问题通常没有三个可传播坐标，因此保持 NO_MATCH。该结果不应通过放松绑定来人为抬高。

几何闭包也反哺已有定理：model 72 从 6 增至 14 个 APPLIED，model 73 从 3 增至 5，model 52/53 分别从 3/1 增至 4/4。

## 5. 判断

本阶段证明构造对象实体化能同时提升新旧定理，而不需要把 abstract state 提前做复杂。剩余 18 个 specification-only 模型主要集中在焦点弦、基础不等式、中线、内切圆、圆切线和极值。

下一步优先级建议：

1. 补 FootPoint、Directrix、TangentPoint 的专用坐标规则，增强距离与圆切线链；
2. 建立 LengthOf / DistanceOf / AreaOf 的统一标量量对象，减少 RequestedXxx 临时谓词；
3. 实现 63、64、68-71、76、79，并让极值模型消费显式目标函数和定义域；
4. 对 1,306 条纠错候选分层审核，区分真实缺步骤与训练序列抽象粒度差异。

原训练 JSON 未修改，评估和候选修复继续输出为独立文件。
