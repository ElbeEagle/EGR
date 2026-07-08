# Theorems V2 第三阶段信息空间与执行器报告

## 1. 实现范围

本阶段保持旧定理库和前两阶段 V2 代码不变，新增独立的 structured stack：

- Point2D：规范化二维点坐标；
- LineEquation：规范化直线一般式 a*x+b*y+c=0；
- QuadraticPolynomial：记录代入得到的一元二次式、变量和几何根标签；
- Vector2D：记录由端点坐标得到的向量分量；
- IntersectionOf、IntersectionCountOf、PointPositionOf、LineNormalFormOf、VectorScaleRelation 等显式关系谓词。

新增 16 个 concrete executor：

- Vieta 与判别式：41、42、43、65、66、67；
- 坐标公式：52、53、54、55；
- 向量：59、61、62；
- 直线：72、73；
- 直线代入圆锥曲线：78。

V2 concrete 数量由 35 增至 51，80 条定理规范仍全部保留。

## 2. 关键推理链

代数链：

IntersectionOf + LineNormalFormOf + ExpressionPolynomial
→ model 78
→ QuadraticPolynomialOf + RootSetOf + SubstitutionOf
→ models 41/42/43/65
→ RootSumOf / RootProductOf / DiscriminantOf
→ models 66/67
→ DiscriminantConditionOf

坐标与向量链：

CoordinateOf
→ PointPositionOf
→ models 52-55
→ 距离、中点、斜率公式及约束

PointPositionOf
→ VectorOf(Vector2D)
→ models 59/61/62
→ 点积、垂直与共线关系

匹配必须具有明确的目标关系或交点证据，不允许仅因 state 中存在若干点或直线就任意绑定。

## 3. 定理规范调整

第三阶段为 16 个模型覆盖了旧 catalog 的类别级要求，改为 executor 实际使用的 predicate-level contract。例如：

- model 78 要求 IntersectionOf、LineNormalFormOf、ExpressionPolynomial；
- models 42/43 要求 QuadraticPolynomialOf，并可依赖 78；
- models 66/67 要求 DiscriminantOf 与 IntersectionCountOf；
- model 62 直接要求 VectorScaleRelation，不再错误依赖 model 59。

这些覆盖规范同时供 library capability 和 sequence corrector 使用，因此定理库、信息空间和纠错器使用同一依赖定义。

## 4. 数据集裸测

数据仍为 5,355 道含文字过程和定理序列的样本，共 20,212 步。

| 指标 | 第二阶段 35 concrete | 第三阶段 51 concrete |
| --- | ---: | ---: |
| APPLIED + ALREADY_KNOWN | 3,559 | 3,834 |
| SPECIFICATION_ONLY | 6,771 | 3,105 |
| 全步骤裸 apply 率 | 17.61% | 18.97% |
| concrete 步骤裸 apply 率 | 26.48% | 22.41% |
| 裸序列完整跑通 | 276 (5.15%) | 284 (5.30%) |
| 纠错后完整跑通 | 461 (8.61%) | 471 (8.80%) |
| 未解析事实 atom | 9,883 | 6,882 |

concrete 步骤 apply 率下降是分母扩张的结果：3,666 个原 specification-only 步骤进入真实执行，其中 275 个成功或已知，其余明确暴露为 NO_MATCH。它反映数据就绪度，而不是 executor 单元正确率。

新增模型的主要裸测命中：

- model 62：87 APPLIED；
- model 78：53 APPLIED；
- model 42：36 APPLIED、10 ALREADY_KNOWN；
- model 61：28 APPLIED；
- model 43：24 APPLIED、5 ALREADY_KNOWN；
- model 41：13 APPLIED；
- models 52-55：合计仅 5 APPLIED，主要受构造点缺少坐标传播限制。

## 5. 结论

本阶段已经补齐“直线与圆锥曲线相交后进入 Vieta/判别式”的核心信息通道，也建立了坐标和向量的 typed representation。当前主要瓶颈不再是这些公式没有 executor，而是训练事实中的构造对象尚不能转化为坐标：

- Focus、Vertex、MidPoint、FootPoint 等构造点需要坐标生成规则；
- LineOf、LineSegmentOf、Asymptote 等嵌套对象需要稳定实体化；
- 符号坐标和代数等价需要更强但仍可审计的化简器；
- model 52-55 的目标量常隐含在文字过程而非初始 fact expressions 中。

下一阶段应优先做构造点坐标传播和嵌套几何对象实体化，再扩展弦长、点差法和面积定理。原训练数据没有被覆盖；新的序列修复候选单独输出。
