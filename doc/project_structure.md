# 当前实现地图

更新：2026-10-14。开发前先读本文，再按任务阅读[关键接口](api_reference.md)、[开发记录](../dev_record.md)及[开发规格](../docs/开发规格/README.md)。本文记录当前代码事实，规格中的设计不自动视为已实现。

## 目标与当前阶段

以题目状态和推理模型的状态转换完成圆锥曲线求解：双层状态 → 模型选择与对象绑定 → 模型应用／公共符号操作 → 新状态 → 答案。

- **已有基础**：旧状态构造、定理库、选择器训练、推理／搜索、符号求解与评估模块均有代码；不代表全库数学正确性或端到端质量已验证。
- **独立验证**：新绑定接口已跑通 ID 2 的 RM5→RM21（m=5）及 ID 9 的 RM3→RM11→RM5→RM12（t=9）；另已验证 ID 65/200/353/380/549 的正向渐近线链；ID 1516 仅验证椭圆参数子链；ID 5 的标准模型→RM17 及标准模型→RM29→RM52→RM2 均得到 5/4；ID 3723 原始查询经 RM9→RM29→RM52 得到 65/16；ID 946/1793 经同链及焦点坐标实例化得到 1/8、1/4；ID 7260 原始查询经 RM7→RM72→RM52 得到 2√5/5；均为固定链与模式预检，不是自主选择模型。
- **尚未接入**：新状态与旧状态没有自动双向同步；新应用器尚未接入旧求解器、轨迹构建器和选择器。ID 51 仍为数学／规格案例；ID 56 已完成固定 RM78→RM42→RM43→RM55 求参闭环，未接入自主选择器。
- **当前方向**：分批完善 80 个模型的执行契约、共享操作与可信轨迹，再训练选择器。Entropy／求解进度机制和 LLM 实验后置。

## 代码导航

下列路径均相对仓库根目录；“旧流程”表示迁移前基础，不表示应删除。文件表说明模块用途；核心函数及数据结构的中文含义见 [API 参考](api_reference.md)。

| 文件／目录 | 主要职责与状态 |
| --- | --- |
| `src/state/symbolic_state.py`、`abstract_state.py` | 旧符号状态和 28 维抽象特征，已用于旧流程 |
| `src/state/state_constructor.py`、`equation_normalizer.py` | 旧输入解析、方程归一化和特征构建；配置定理库时会提取参数 |
| `src/state/state_sequence_builder.py` | 按给定模型 ID 序列构造旧训练轨迹；尚未迁移到新应用器 |
| `src/theorems/base_model.py`、`theorem_library.py`、`models/` | 原模型定义、注册与执行；部分模型已有代码，注册数量不等于可靠覆盖率 |
| `src/selector/` | 分类网络、数据加载和训练基础；默认 28 维输入、80 类输出 |
| `src/reasoning/reasoning_engine.py`、`model_selector.py`、`search.py` | 旧求解编排、候选策略与搜索；这里的选择策略与 `src/selector/` 的网络不同 |
| `src/reasoning/query_parser.py`、`answer_extractor.py`、`answer_comparator.py` | 旧查询解析、答案抽取和比较；抽取可能调用符号推导 |
| `src/solver/symbolic_solver.py` | 旧精确符号求解基础，含多种查询相关推导；迁移时按职责拆分复用 |
| `src/evaluation/protocol.py` | 样本报告、轨迹指标与汇总输出；报告必须注明数据和执行路径 |
| `src/entropy/`、`src/reasoning/entropy_estimator.py` | 已有熵相关代码，当前开发后置 |

### 当前绑定执行链的关键文件

计算模块接收数学表达式并返回计算结果；提案模块组织一次模型应用，返回待提交的变化与来源；应用器检查并统一写入状态。数据结构保存信息，查询类型表达求解目标，二者自身不执行推导。

| 文件 | 主要职责 |
| --- | --- |
| [coordinate_product_facts.py](../src/state/coordinate_product_facts.py) | 保存坐标分量别名／给定交点数，校验声明并定位已有坐标积；不推导符号结果，见[规格30](../docs/开发规格/30_ID1833坐标别名与乘积查询.md) |
| [named_line_facts.py](../src/state/named_line_facts.py) | 命名直线输入：规范 LineOf 身份，保存无序交点集合、斜率和及分母要求，供后续参数化与斜率推理使用 |
| [chord_facts.py](../src/state/chord_facts.py) | 保存数值复合中点、(line,curve)弦身份及匿名无序端点对，不求端点坐标 |
| [midpoint_operations.py](../src/solver/midpoint_operations.py) | 计算中点对应的端点和，核验数值椭圆中点资格；支持直接中点／点差方向，不写状态 |
| [midpoint_proposals.py](../src/theorems/midpoint_proposals.py) | 组织RM54端点和、RM40直接中点及RM45点差提案；核验同源绑定与已有线，交应用器提交 |
| [transition_state.py](../src/state/transition_state.py) | 题目状态与事实定义：解析已给信息，保存对象、方程、关系、模型结果及来源；表示查询目标并读取已提交答案 |
| [transition_primitives.py](../src/solver/transition_primitives.py) | 受限解析、椭圆／双曲线标准形式、共焦点实例化、斜率、实根与条件检查 |
| [standard_proposals.py](../src/theorems/standard_proposals.py) | 标准椭圆／双曲线参数提案：从绑定方程提取半轴平方、轴向及类型条件，供 RM3–6 使用 |
| [parabola_operations.py](../src/solver/parabola_operations.py) | 抛物线公共计算：提取标准式系数、将数值点代入方程、由系数和方向计算 p 与焦点 |
| [parabola_proposals.py](../src/theorems/parabola_proposals.py) | 抛物线模型提案：组织参数提取／点恢复、焦点坐标实例化、焦半径、准线及定义路径，供 RM2/7–10/17/29 使用 |
| [distance_operations.py](../src/solver/distance_operations.py) | 一般点到直线精确距离；RM52 调用，数值输入边界与定义路径由 `tests/test_bound_parabola_definition.py` 验证 |
| [distance_proposals.py](../src/theorems/distance_proposals.py) | RM52 共用命名点／焦点属性到直线的距离提案；`test_bound_line_distance.py` 覆盖解析、查询隔离及真实事实子案例 |
| [line_proposals.py](../src/theorems/line_proposals.py) | 直线参数恢复提案：利用已知点与直线方程的一致性求一个参数，并提出斜率／截距结果，供 RM72 使用 |
| [eccentricity_proposals.py](../src/theorems/eccentricity_proposals.py) | 离心率计算提案：核验已有 a²、b²、c² 后计算 e，向 RM13 返回待提交属性与来源 |
| [intersection_operations.py](../src/solver/intersection_operations.py) | 交点相关公共计算：将直线代入标准抛物线，支持过点未知直线族及水平分支检查，计算数值／受限局部参数二次根关系及实根数，并由根关系及坐标映射计算弦长；不生成命名交点 |
| [intersection_proposals.py](../src/theorems/intersection_proposals.py) | RM78/42/43/50 提案：绑定消元事实，组织数值消元、命名直线参数化、根关系及弦长计算，包装结果与来源供应用器提交 |
| [focal_chord_proposals.py](../src/theorems/focal_chord_proposals.py) | RM33/34/35/59 提案：分别组织焦点弦长、轴向／横向积和原点点积，交应用器提交；不互相暗中补做模型 |
| [symbolic_focal_proposals.py](../src/theorems/symbolic_focal_proposals.py) | 组织受限符号焦点弦提案，核对来源，提出非退化条件与一项坐标积，交既有应用器提交 |
| [focal_chord_evidence.py](../src/theorems/focal_chord_evidence.py) | 核验给定／计算两种焦点弦证据及数值一致性，返回来源和验证操作供提案消费，不修改状态 |
| [slope_proposals.py](../src/theorems/slope_proposals.py) | RM55 斜率和提案：读取已有命名根关系，验证原点斜率分母，再提出局部参数赋值；不补做韦达 |
| [tangent_operations.py](../src/solver/tangent_operations.py) | 数值椭圆切点核验及切线计算，返回残差和方程，不改状态 |
| [tangent_proposals.py](../src/theorems/tangent_proposals.py) | RM38/39切线提案：读取已提交标准参数、验证给定切点，组织椭圆／抛物线切线及来源供应用器提交 |
| `model_042.py`、`model_043.py`、[model_050.py](../src/theorems/models/model_050.py) | 根和／根积／弦长模型入口：将绑定动作转交相应提案；RM50 仅新绑定接口可执行 |
| [model_039.py](../src/theorems/models/model_039.py) | RM39 模型入口：将绑定应用转交切线提案函数；旧无绑定执行接口未实现 |
| [parameter_proposals.py](../src/theorems/parameter_proposals.py) | 普通参数关系提案：利用椭圆／双曲线的 a²、b²、c² 关系补全参数或求标量，供 RM11/RM12 使用 |
| [bound_application.py](../src/theorems/bound_application.py) | 绑定执行与状态提交：核验动作对象，调用模型提案，检查冲突并一次性提交全部变化，记录来源与执行结果 |
| `model_003.py`、`model_011.py`、`model_012.py`（`src/theorems/models/`） | 椭圆参数、普通参数关系及共焦点约束；RM11/RM12 共用 `parameter_proposals.py` |
| [model_005.py](../src/theorems/models/model_005.py)、[model_021.py](../src/theorems/models/model_021.py) | 原模型类新增 `propose_bound`；RM5 记录类型条件；RM21 支持渐近线正／反向模式，旧接口保留 |
| [bound_slice.py](../src/reasoning/bound_slice.py) | 固定动作链诊断入口：预检标准方向、依次调用应用器并读取答案，返回结果与轨迹；不负责学习型模型选择 |
| [test_bound_transition_slice.py](../tests/test_bound_transition_slice.py) | 真实题、绑定隔离、重复执行、多解、条件不足、冲突与回滚测试 |

新增测试：[test_bound_parabola.py](../tests/test_bound_parabola.py) 覆盖 ID 5 与四向抛物线；[test_bound_y_axis.py](../tests/test_bound_y_axis.py) 覆盖 y 轴标准模型、关系和渐近线；[test_bound_parameter_modes.py](../tests/test_bound_parameter_modes.py) 覆盖普通参数关系和正向渐近线；[test_bound_shared_focus.py](../tests/test_bound_shared_focus.py)，覆盖 ID 9 及多曲线关系边界。

运行：`python3 -m src.reasoning.bound_slice --problem-id 2`。
详细结果及限制见[实现记录](../docs/开发规格/07_RM5_RM21实现记录.md)；诊断 trace 尚不是最终训练 schema。ID 9 的命令、证据及限制见[共焦点实现记录](../docs/开发规格/08_ID9共焦点实现记录.md)。

审计工具：[model_binding_inventory.py](../scripts/audit/model_binding_inventory.py) 输出全 80 ID 的接口存在性与弱标注统计；不能作为语义覆盖率报告。

## 数据与设计依据

- `model/conic_model_ids.json`、`conic_model_descriptions.md`：80 个高层模型的 ID、名称与数学定义。`object.json`、`operators.json` 是表达语言词汇，不是已实现的运算库。
- `data/train_with_models_v3.json`：当前案例来源，按记录 `id` 定位。Opus 辅助标注的 `models` 仅作弱参考，不直接视为可执行顺序。
- [开发规格](../docs/开发规格/README.md)：已确认职责、真实案例、全库简表与运行证据；开发新模型前阅读相关条目。
- `paper/`、`docs/项目理解/`：研究目标与路线背景；不能用历史规划替代当前实现状态。
- `doc/module*.md` 等旧文档保留为历史参考，涉及现状时核对代码及本文。

## 后续顺序与维护

1. RM4/RM6 与 y 轴框架、渐近线及参数关系已验证，见[本批记录](../docs/开发规格/10_Y轴标准模型实现记录.md)。ID 5 已完成标准参数恢复与焦半径闭环，见[记录](../docs/开发规格/11_ID5抛物线实现记录.md)。定义路径已完成，见[记录](../docs/开发规格/12_ID5定义路径实现记录.md)。RM52 已支持独立直线绑定／距离查询；ID 5882/1253 仅验证显式事实子案例，见[记录](../docs/开发规格/13_一般直线距离实现记录.md)。ID 3723 已完成原始查询闭环，见[记录](../docs/开发规格/14_ID3723准线别名实现记录.md)。ID 946/1793 焦点别名坐标实例化已验证，见[记录](../docs/开发规格/15_焦点别名坐标实现记录.md)。ID 7260 已完成[职责设计](../docs/开发规格/16_ID7260交点与参数恢复设计.md)，D5 已确认，交点事实及 RM7／RM72 参数子链已验证，见[记录](../docs/开发规格/17_ID7260参数子链实现记录.md)；Focus(G) 距离原始查询现已接通，见[记录](../docs/开发规格/18_ID7260焦点距离闭环.md)；全库选型已完成，下一批为 RM13 正向离心率与 ID 5988/7488/1586/4528，见[选型规格](../docs/开发规格/19_模型覆盖审计与下一组选型.md)；四题 RM13 原始查询已验证，见[实现记录](../docs/开发规格/20_RM13正向离心率实现记录.md)。RM39 切点验证、派生切线及 ID 2106 原始查询已验证，见[记录](../docs/开发规格/21_RM39抛物线切线实现记录.md)。ID 6347 的[消元与根关联契约](../docs/开发规格/22_ID6347消元与根关联契约.md)及 RM78 数值消元子步骤已完成；RM42/43 实根资格与 RM50 弦长查询现已完成，ID 6347 原题得到 8，见[闭环记录](../docs/开发规格/23_ID6347根关系与弦长闭环.md)；ID 56 的[参数化契约与结构化输入](../docs/开发规格/24_ID56命名直线与参数化契约.md)已完成；RM78 方向检查、局部参数与根对关联已完成，见[记录](../docs/开发规格/25_ID56参数化与命名根关联实现.md)；符号 RM42/43 与 RM55 已完成 ID56 闭环，见[记录](../docs/开发规格/26_ID56符号韦达与斜率求参闭环.md)；ID6347 的 RM33 焦点弦长路径已完成，见[记录](../docs/开发规格/27_ID6347焦点弦长路径.md)；RM34/35 的[证据审查与首批选型](../docs/开发规格/28_RM34_RM35证据审查与首批选型.md)已完成：优先4373数值积子链、1191轴向验证；现已完成数值RM34/35与RM59：4373原题点积−3、1191事实投影和6347计算证据验证，见[实现记录](../docs/开发规格/29_RM34_RM35与原点点积闭环.md)；后续回到职责表选型，1833符号参数和坐标分量别名另批；暂不扩展离心率范围或反向模式。
2. 分批覆盖全部 80 个模型，抽提公共运算；同时形成可回放轨迹，处理弱标注顺序问题。
3. 统一状态初始化、轨迹构建与求解入口，再开展选择器训练和系统评估；Entropy、LLM 工作另行安排。
4. 历次详细案例与验证见[开发记录](../dev_record.md)及[规格导航](../docs/开发规格/README.md)。

每次只更新受影响的模块行、接入状态和后续步骤；接口细节放 API 文档，变更经过放开发记录，避免重复维护三份功能清单。

候选审查工具：[focal_chord_candidates.py](../scripts/audit/focal_chord_candidates.py) 读取 RM34/35 弱标注候选，记录输入解析缺口并独立核验焦点弦乘积；不是求解器或覆盖率评测。

本批模型入口：新增 model_034.py／model_035.py 仅转交绑定提案；model_059.py 保留旧实现并增加原点点积绑定。named_line_facts.py 新增焦点归属结构与点积目标；transition_state.py 接入并只读答案。bound_slice.py 的 origin-dot 模式保存固定回放；test_bound_focal_products.py 覆盖本批真实案例与拒绝边界。

ID1833 已通过独立的方向无关符号RM35固定回放得到−p²，非退化条件p≠0由曲线类型与原式导出并原子提交，不默认p>0。数值模式未放宽；符号模式只处理已给命名焦点弦，见[规格31](../docs/开发规格/31_ID1833方向无关符号焦点弦.md)。下一步回到职责表选择新的有限案例。

RM38已完成ID2126原题固定RM3→RM38，得x+2y−4=0；复用TangentQuery及切线提交，支持两轴数值非圆椭圆。见[规格32](../docs/开发规格/32_RM38椭圆切线与ID2126.md)。后续中点弦实现见下段。

ID4795已接入复合中点、弦身份与匿名无序端点对；独立Line的Expression(l)复用只读查询。固定RM4→RM40得2x+y−2=0，不生成端点坐标，见[规格34](../docs/开发规格/34_ID4795中点弦与RM40闭环.md)。RM54→RM45独立点差路径现已实现，见[规格35](../docs/开发规格/35_ID4795端点和与点差路径.md)；不是RM40前置，尚未接自主选择器。

## 命名端点中点弦（首批已接入）

5644／3682／6164已接通两条独立固定链。`src/state/chord_facts.py`新增ChordEndpointNames和collect_named_chords，将椭圆Intersection中的无序点名关联现有pair，分别保留交点／中点来源；`src/state/transition_state.py`新增chord_endpoint_names容器和收集入口。支持反序、重排及重复合并，不生成坐标。

`src/solver/midpoint_operations.py`新增verify_chord_endpoints核验已有数值端点的曲线／直线归属及两点不同、中点一致；`src/theorems/midpoint_proposals.py`扩展绑定与chord_line_proposal，记录已读坐标来源后交原应用器提交。符号坐标未定，身份／数值矛盾不静默处理。RM54只提出坐标和，RM40不依赖它。旧抛物线named_intersections未扩展。

详情及证据见[规格37](../docs/开发规格/37_命名端点中点弦实现.md)。7439线段对象现已接入（见下节）；命名中点别名及RM46的后续实现见下节，7300数据差异待审；未接自主选择器。

## ID7439线段弦（有限模式）

`src/state/segment_chord_facts.py`新增SegmentChord及collect_segment_chords，保存已声明线段H、内部所在直线@overlap:H、椭圆及来源，收集IsChordOf(H,G)和数值Coordinate(MidPoint(H))。`src/state/chord_facts.py`抽提store_chord_midpoint复用匿名弦／端点对，不生成端点坐标。

`src/state/transition_state.py`新增segment_chords容器、LineSegment声明及Expression(OverlappingLine(H))入口，复用只读NamedLineQuery；`src/theorems/midpoint_proposals.py`扩展身份和来源核验，公共计算、模型提案提交沿用原路径。

7439两条固定链均得x+2y−3=0。仅支持显式数值复合中点；显式所在直线别名后置；命名中点别名及RM46的后续实现见下节。见[规格38](../docs/开发规格/38_ID7439线段弦对象实现.md)。

## 线段命名中点别名（首批已实现）

2227／2324／3337已接入MidPoint(H)=M，两条独立固定链均完成。`src/state/midpoint_alias_facts.py`新增ChordMidpointAlias、collect_midpoint_aliases、resolve_midpoint_aliases及check_midpoint_alias：先收集别名，原坐标解析后关联数值，并在模型绑定时检查原坐标ID、点名、值及来源是否匹配快照。

`src/state/transition_state.py`新增midpoint_aliases容器和前后解析入口；`src/state/chord_facts.py`扩展ChordMidpoint.alias_point，标记来源点；`src/theorems/midpoint_proposals.py`在绑定阶段执行检查，沿用原计算／提案／提交。缺坐标不可应用、符号坐标未定、过期或矛盾快照拒绝；查询保持只读。

见[规格40](../docs/开发规格/40_线段命名中点别名实现.md)。命名端点中点别名2290／4761已实现（见下节）；RM46已按独立资格契约接入（见下节）。未接自主选择器。

## 命名端点中点别名（2290／4761）

`src/state/midpoint_alias_facts.py`扩展既有ChordMidpointAlias：声明线段用segment，命名端点用segment=None、pair_id和无序endpoints快照；collect_midpoint_aliases接受MidPoint(LineSegmentOf(A,B))=M并关联唯一弦，check_midpoint_alias重新核验点对与弦身份。原坐标快照解析／检查、RM40／54／45提案、应用器及只读查询复用。

两题已完成两条独立固定链；2290用RM4得9x+4y−13=0，4761用RM3得x+2y−2=0。反序／重排支持，缺坐标不可应用、符号未定、错绑／过期快照拒绝。自主选择未接入，RM46见下节，详见[规格41](../docs/开发规格/41_命名端点中点别名实现.md)。

## RM46数值双曲线点差（有限实现）

- `src/state/chord_facts.py`、`src/state/segment_chord_facts.py` → 输入身份关联。扩展既有中点／交点及线段收集函数，允许双曲线，复用弦身份、无序端点对及别名来源，不生成端点坐标。
- `src/solver/midpoint_operations.py` → 公共计算。新增 `hyperbola_point_difference`，读取带符号系数和端点坐标和，返回方向、直线、代入二次式与判别式；独立检查实弦资格，不修改状态。
- `src/theorems/midpoint_proposals.py` → 模型提案。扩展 `check_midpoint_binding` 和 `derive_point_difference_chord`，核验双曲线绑定、同对坐标和及来源；按轴向选择正负系数，提出直线及弦级 `midpoint_q`、`intersection_discriminant`，供提交和轨迹复核。
- `src/theorems/models/model_046.py`、`src/theorems/bound_application.py` → 模型入口与状态提交。新增 RM46 的 `propose_bound` 转交公共提案；扩展候选、类型隔离及派生直线提交许可，应用器沿用事务提交与冲突回滚。RM54兼容双曲线，RM40／45仍限椭圆。
- `src/reasoning/bound_slice.py` → 固定链诊断。新增 `solve_hyperbola_chord_slice` 和 `hyperbola-chord` 模式，回放 RM5/6→RM54→RM46，再读取已提交直线；不是自主选择器。
- `tests/test_bound_hyperbola_chord.py`（新增）、`tests/test_bound_segment_chord.py` → 行为验证。新增25项覆盖真实题、轴向符号、独立交点核验、退化、前提缺失、错绑与回滚；旧线段拒绝测试改用仍不支持的抛物线类型。

RM46动作模式为 `derive_point_difference_chord`，绑定同一curve、equation_id、line、relation_id。只接受RM5/6已提交参数／轴向及RM54同对端点和；缺少前提不自动补算。公共操作按带符号系数和判别式检查两个不同实交点，不复用椭圆内点判断。弦级midpoint_q与intersection_discriminant保存资格结果，查询仅读取已提交方程。

1801／4359固定链得到x−y−3=0，3119无实弦拒绝，不计为原题已解。范围与接口见[规格42](../docs/开发规格/42_RM46双曲线点差与实弦资格.md)；未接自主选择器。

## 下一小批：RM41数值根和积

`scripts/audit/vieta_batch_selection.py`为新增选型审查工具：audit保存6题原始输入及现有链结果；independent_length仅用于独立求交核验。3057得到√15、6347得到8，当前执行仍是RM78→RM42→RM43→RM50。RM41现已接入，最新实现见下节。见[规格43](../docs/开发规格/43_RM41有限案例选型与输出契约.md)。

## RM41联合根关系（有限实现）

- `src/theorems/intersection_proposals.py` → 根关系模型提案。新增derive_root_relations，读取已绑定消元记录，复用韦达和实根分类计算，一次提出root_sum、root_product、discriminant、distinct_real_roots；不直接修改状态。
- `src/theorems/models/model_041.py` → RM41入口。新增propose_bound，转交联合提案；旧apply保留。
- `src/theorems/bound_application.py` → 绑定、候选与提交编排。扩展check_binding和enumerate_actions支持RM41，按同一曲线、直线、方程及消元记录绑定；原应用器继续负责原子提交、幂等及冲突回滚。
- `src/reasoning/bound_slice.py` → 固定链诊断。扩展solve_chord_length_slice的joint_roots选项，选择78→41→50，默认仍为78→42→43→50；CLI新增joint-root-chord。查询继续只读。
- `tests/test_bound_joint_roots.py`（新增）→ 联合提案验证。覆盖两题等价性、来源、重复执行、部分属性补齐、冲突原子性、错绑／多直线隔离及重根、非实根、退化和符号拒绝。

3057／6347固定78→41→50分别得√15／8；仍保留分步链。未接自主选择器，范围见[规格44](../docs/开发规格/44_RM41数值根关系联合提案.md)。

## 下一批：ID1827正向中点

`scripts/audit/root_midpoint_contract.py`新增设计审查：probe_midpoint核验现有78→41子链及仿射平均，audit保存4题输入和入口缺口。1827独立结果(1,2)，原始查询仍未接入；下一批扩展数值命名根关联、RM54正向提交及只读坐标查询。见[规格45](../docs/开发规格/45_ID1827根关系到中点契约.md)。

## ID1827正向中点已接入

- `src/theorems/root_midpoint_proposals.py` → 数值根中点核验与提案。MidpointCoordinateQuery保存无序点对；verify_numeric_association重查命名身份及原式回代；derive_midpoint_from_roots读取有来源的根和／资格，提出midpoint_x/y；read_midpoint只读取完整结果，不推导。
- `src/state/transition_state.py` → 查询入口。扩展复合中点坐标查询解析与只读结果分派，不创建虚构端点或命名中点坐标。
- `src/theorems/intersection_proposals.py` → 消元与韦达提案。数值RM78填写已有命名关联字段并记录所有重复声明来源；多点对歧义拒绝。RM42/43区分数值关联与原符号参数化路径，RM41核验数值关联。
- `src/theorems/bound_application.py`、`src/theorems/models/model_054.py` → 模型编排。增加derive_midpoint_from_roots显式模式候选与入口，沿用原子属性提交；旧derive_endpoint_sums保持不变。
- `tests/test_bound_root_midpoint.py` → 新增13项验证，覆盖原题／轴交换、重排／重复、来源缺失、过期原式、非仿射回代、幂等、部分补齐、冲突和退化。

原题固定78→41→54得(1,2)，显式模式derive_midpoint_from_roots与旧端点和模式并存；查询只读两项已提交属性。此前规划状态由[规格46](../docs/开发规格/46_ID1827正向中点实现.md)更新，符号模式另批。

## 下一批通径契约（未实现）

RM19／6057及RM20／6770拟复用标准参数和线段弦身份，新增焦点在线段上、垂直轴资格及Length(L)只读查询。6770弱标签19需另记正确执行模型20，原数据不改。规格见[47](../docs/开发规格/47_RM19_RM20通径有限案例契约.md)。

## RM19／RM20通径已接入

- `src/state/latus_facts.py` → 新增有限资格解析。LatusEvidence保存线段、焦点／垂直目标和来源；collect_latus_facts读取原始关系，拒绝跨曲线绑定；SegmentLengthQuery只表达线段长度目标。
- `src/state/segment_chord_facts.py`、`src/state/transition_state.py` → 扩展抛物线线段弦身份、资格容器和Length(L)只读查询；给定抛物线中点仍拒绝。
- `src/solver/latus_operations.py` → 新增公共计算。latus_length核验有限正参数，返回2b²/a或2p，不写状态。
- `src/theorems/latus_proposals.py` → 新增模型资格及提案。check_latus_binding核对弦与方程；derive_latus读取标准参数、轴向和关系来源，验证过焦点且垂直正确轴，提出弦级chord_length。
- `src/theorems/models/model_019.py`、`src/theorems/models/model_020.py`、`src/theorems/theorem_library.py`、`src/theorems/bound_application.py` → 扩展RM19绑定入口，新增并注册RM20，生成候选；实际属性写入继续由原应用器原子提交。
- `tests/test_bound_latus.py` → 新增真实题与方向、缺资格、重排重复、冲突回滚测试。

模式derive_latus_length输出弦级chord_length，Length(L)只读；6057／6770已验证固定链。先前规划由[规格48](../docs/开发规格/48_RM19_RM20通径实现.md)更新，后置范围不变。

## RM32设计入口（后续实现见下节）

选998／1552数值椭圆焦点三角形周长，复用标准参数／RM11，新增无序焦点对身份和只读周长查询。需先提交c²，不强制执行RM0；周长为三段距离和，不产生非退化资格。见[规格49](../docs/开发规格/49_RM32焦点三角形周长契约.md)。

## RM32数值周长已接入

- `src/state/focal_perimeter_facts.py` → 新增焦点身份及查询。FocusPair保存曲线、无序焦点对和声明来源；collect_focus_pairs合并反序重复、拒绝歧义；FocalPerimeterQuery保存三个顶点，read_perimeter只读取唯一角色绑定的结果。
- `src/state/transition_state.py` → 扩展焦点对容器、事实收集和周长查询分派，不求焦点坐标。
- `src/solver/focal_perimeter_operations.py` → 新增公共计算与核验。focal_perimeter返回2√a²+2√c²；verify_coordinates核验已有点在椭圆上、焦点属于标准焦点集合且两焦点不重合，不写状态。
- `src/theorems/focal_perimeter_proposals.py` → 新增绑定和提案。check_perimeter_binding核对曲线、焦点对、第三点及归属；derive_focal_perimeter读取已提交参数与来源，提出角色身份键下perimeter，交应用器提交。
- `src/theorems/bound_application.py`、`src/theorems/models/model_032.py` → 扩展RM32候选和绑定入口，复用原子提交与回滚，保留旧模型入口。
- `tests/test_bound_focal_perimeter.py` → 新增17项，覆盖真实题、换轴、反序重复重排、缺c²／来源、错绑、已有坐标、退化求和、幂等及冲突回滚。

模式derive_focal_perimeter读取同曲线标准参数、c²及来源，输出角色级perimeter；Perimeter(TriangleOf(...))只读取唯一匹配结果。详情见[规格50](../docs/开发规格/50_RM32焦点三角形周长实现.md)。

## RM30设计入口（最新实现见下节）

选3174／3900／6748，复用焦点对、点归属与标准参数，新增顶点明确的弧度夹角事实及只读面积查询。要求0<θ<π且a²sin²(θ/2)≤c²，允许最大角等号；与RM32退化求和分开。见[规格51](../docs/开发规格/51_RM30焦点三角形面积契约.md)。

## RM30面积已接入

- `src/state/focal_area_facts.py` → 新增角度事实和面积目标。AngleFact保留顶点、无序两侧点、弧度值及来源，collect_angles合并反序重复并拒绝矛盾；FocalAreaQuery与read_area只定位、读取唯一面积结果。
- `src/state/transition_state.py` → 扩展角度容器、解析及面积查询分派，pi仅在角度解析环境中作为常量提供。
- `src/solver/focal_area_operations.py` → 新增公共资格与计算。focal_area验证非退化和可达性后返回面积及余量；verify_point_angle以已有点坐标核对真实夹角，不提交焦点坐标。
- `src/theorems/focal_area_proposals.py` → 新增RM30绑定与提案。检查焦点对、归属、参数与角度来源，复用已有坐标归属核验，提出独立area身份下的面积；应用器负责提交。
- `src/theorems/models/model_030.py`、`src/theorems/theorem_library.py`、`src/theorems/bound_application.py` → 新增并注册RM30绑定入口与候选，沿用原子提交和回滚。
- `tests/test_bound_focal_area.py` → 新增23项，验证三题、轴向、角身份、来源、可达性、坐标矛盾、歧义、幂等和回滚。

模式derive_focal_area要求已提交参数及匹配角度，输出area属性；只读查询与周长分离。详见[规格52](../docs/开发规格/52_RM30数值焦点面积实现.md)。

## RM22设计入口（最新实现见下节）

选3200／891，复用标准参数和来源，新增同曲线Focus／Asymptote共同距离查询；拟用RM5/6→RM22，输出曲线级focus_asymptote_distance，查询只读。四成员组合距离相同不等于支持通用集合距离。见[规格53](../docs/开发规格/53_RM22焦点到渐近线距离契约.md)。

## RM22数值共同距离已接入

- `src/state/focus_asymptote_query.py` → 新增同曲线查询。FocusAsymptoteDistanceQuery保存双曲线身份；read_focus_asymptote_distance仅从唯一曲线方程且来源匹配的已提交属性读取结果，不进行几何推导。
- `src/state/transition_state.py` → 扩展查询解析及分派，拒绝跨曲线Focus／Asymptote组合，不扩展通用集合距离。
- `src/solver/focus_asymptote_operations.py` → 新增公共计算。focus_asymptote_distance检查正数值参数并返回√b²；verify_asymptote用规范化直线核验已有渐近线，不修改状态。
- `src/theorems/focus_asymptote_proposals.py` → 新增RM22绑定与提案。核验唯一曲线方程、已提交参数／框架和来源；检查已有c²及同曲线渐近线，提出focus_asymptote_distance，交应用器原子提交。
- `src/theorems/models/model_022.py`、`src/theorems/bound_application.py` → 接入RM22绑定入口和候选，保留旧入口；提交／冲突回滚复用原机制。
- `tests/test_bound_focus_asymptote.py` → 新增14项，覆盖真实题、换轴、不同a²同b²、多曲线隔离、缺来源、过期原式、渐近线矛盾、幂等和回滚。

模式derive_focus_asymptote_distance输出曲线级距离，同曲线查询只读。详见[规格54](../docs/开发规格/54_RM22数值共同距离实现.md)。

## RM24数值等轴性质已接入

- `src/solver/equal_axis_operations.py` → 新增数值资格计算。equal_axis_eccentricity核验有限正半轴平方且a²=b²，返回√2，供模型提案使用，不修改状态。
- `src/theorems/equal_axis_proposals.py` → 新增RM24绑定与提案。check_equal_axis_binding核对唯一双曲线方程；derive_equal_axis_eccentricity复用参数／框架核验，检查来源及已有c²一致性，提出eccentricity属性和等轴核验证据，交应用器提交。
- `src/theorems/models/model_024.py` → 扩展模型入口。propose_bound调用严格数值提案，保留旧入口隔离，不复用旧can_apply的放宽资格。
- `src/theorems/bound_application.py` → 扩展动作编排。enumerate_actions产生绑定曲线／方程的RM24候选，check_binding分派资格检查；属性提交、幂等和冲突回滚复用既有应用器。
- `tests/test_bound_equal_axis.py` → 新增19项测试。核验两题、换轴、缩放、非等轴、多曲线隔离、来源、过期原式、c²／e矛盾、重复及回滚，并对照既有离心率链。

650／1412固定RM5→RM24均√2，y轴用RM6；复用离心率查询，不生成c²、不依赖RM12／13。详情见[规格56](../docs/开发规格/56_RM24数值等轴性质实现.md)。下一步回到职责表选有限案例，后置范围不变。

## RM28设计入口（最新实现见下节）

2779拟用RM5→RM12→RM28输出两条准线x=±1/2。复用标准参数、c²及方程提交；新增双准线身份和集合只读查询，不能沿用抛物线单准线键。1834右准线选择延期。输入／输出及失败边界见[规格57](../docs/开发规格/57_RM28数值双准线契约.md)。

- `scripts/audit/directrix_pair_contract.py` → 新增有限审查。CASES保存首批与延期案例；probe执行既有参数子链并独立核验双准线偏移及顶点距离比；audit保存原始输入、查询缺口和数据哈希，供RM28实现核对。
- `docs/开发规格/artifacts/directrix_pair_contract.json` → 保存参数事实投影及独立数学证据，不是RM28执行轨迹。

## RM28数值双准线已接入

- `src/state/directrix_pair_query.py` → 新增双准线只读身份。DirectrixPairQuery保存曲线；pair_keys区分正负轴侧两条直线；pair_snapshot保存为EquationFact.source中的输入／输出摘要；read_directrix_pair核对来源及快照后返回规范化方程frozenset，不推导准线。
- `src/state/transition_state.py` → 扩展原始查询解析、方程目标分类和结果分派。Expression(Directrix(G))在G为Hyperbola时定位双准线；初态无结果，抛物线路径不变。
- `src/solver/directrix_pair_operations.py` → 新增公共计算。directrix_pair核验有限正参数及c²=a²+b²，返回实轴两侧的直线表达式，供提案使用，不提交状态。
- `src/theorems/directrix_pair_proposals.py` → 新增绑定与提案。check_directrix_binding复用唯一双曲线绑定检查；derive_directrix_pair核验参数来源及已有直线，提出缺失方程；等价已有结果保留，矛盾或过期拒绝。
- `src/theorems/models/model_028.py`、`src/theorems/theorem_library.py`、`src/theorems/bound_application.py` → 新增并注册RM28绑定入口及候选。propose_bound调用数值提案；原应用器负责双直线原子提交、幂等与回滚，不启用旧状态执行。
- `tests/test_bound_directrix_pair.py` → 新增23项验证，覆盖原题、换轴、缩放、多曲线、缺参数／来源、过期原式、部分补齐、冲突回滚、只读性和排除范围。
- `scripts/audit/directrix_pair_contract.py` → 更新既有审查。audit允许记录已支持的查询身份，不再强制断言原始查询失败；仍不执行RM28。

2779固定5→12→28得到x=±1/2；结果为无序直线集合，快照失效拒读。详情见[规格58](../docs/开发规格/58_RM28数值双准线实现.md)，后置范围不变。

## RM51设计入口（最新实现见下节）

3057／6347拟走RM78→RM41→RM51，复用消元、根关系、弦长属性及只读查询。新增有限斜率资格和根变量到x坐标差转换；RM51不依赖RM50，竖直弦继续由RM50处理。见[规格59](../docs/开发规格/59_RM51有限斜率弦长契约.md)。

- `scripts/audit/slope_chord_contract.py` → 新增有限审查。CASES保存两题ID；probe执行已有RM78→RM41参数子链，独立计算有限斜率弦长，并用显式根坐标距离及RM50结果交叉核验；audit汇总原输入、弱标签、数据哈希及诊断。显式解根只用于审查，不是未来RM51的执行步骤。
- `docs/开发规格/artifacts/slope_chord_contract.json` → 保存根变量、回代映射、和积、斜率和数值核验证据，供实现时对照；不是RM51轨迹。

## RM51有限斜率弦长已接入

- `src/theorems/intersection_proposals.py` → 扩展弦长模型提案。抽提verified_root_pair供RM50／51检查已有和积、判别式及两实根资格，不补缺失事实；新增derive_slope_chord_length核验来源和当前原式／回代一致性，提出已有chord_length属性，交应用器提交。
- `src/solver/intersection_operations.py` → 扩展公共计算。新增slope_chord_length，复用数值仿射与根差检查，读取α、γ，计算k=γ/α及|Δx|=|α|√(S²−4P)，返回长度及计算记录；α=0拒绝，不生成点坐标或状态。
- `src/theorems/bound_application.py` → 扩展动作编排。check_binding与enumerate_actions接入RM51的曲线／直线／消元关系绑定；提交、幂等和回滚复用原机制。
- `src/theorems/models/model_051.py` → 扩展模型入口。propose_bound调用独立数值提案，保留旧入口，不调用RM50模型。
- `tests/test_bound_slope_chord.py` → 新增26项验证。覆盖两题、联合／分步韦达、主变量交换、水平与竖直弦、缩放、多曲线、缺来源、过期原式、退化及冲突回滚。

3057／6347固定78→41→51分别√15、8；结果查询复用，竖直弦保持RM50路径。详情见[规格60](../docs/开发规格/60_RM51有限斜率弦长实现.md)。

## RM73设计入口（最新实现见下节）

1168／1199仅取两点坐标事实投影，诊断构造LineOf(A,B)；原题最值／轨迹另批。复用NamedLine、点坐标与只读直线查询，拟新增双坐标动作绑定、行列式计算与RM73结果快照检查。见[规格61](../docs/开发规格/61_RM73数值两点直线契约.md)。

- `scripts/audit/two_point_line_contract.py` → 新增有限审查。CASES保存两题ID；audit明确抽取A、B声明与坐标并保留原题查询；probe核验既有无序直线身份、独立行列式直线和两端点归属，供RM73实现对照，不提交状态。
- `docs/开发规格/artifacts/two_point_line_contract.json` → 保存原始输入、事实投影、诊断查询及水平／竖直证据；不是RM73轨迹或原题求解结果。

## RM73数值两点直线已接入

- `src/solver/two_point_line_operations.py` → 新增公共计算。two_point_line核验两组有限实坐标不重合，计算并规范化行列式直线，返回表达式，不改状态。
- `src/state/two_point_line_facts.py` → 新增双坐标来源与快照核验。point_pair_inputs按无序端点身份读取当前坐标及来源；coordinate_snapshot绑定输入，line_snapshot将输入／输出摘要存入EquationFact.source；fresh_two_point_line仅核对来源和快照，供只读查询使用。
- `src/state/transition_state.py` → 扩展普通坐标输入和直线读取。坐标解析补记点声明来源；NamedLineQuery对RM73结果检查新鲜度，过期返回None，不重算直线，旧直线读取保持原语义。
- `src/theorems/two_point_line_proposals.py` → 新增绑定及提案。check_two_point_binding核验双坐标ID与动作快照；derive_two_point_line核对已有线，提出一条缺失直线，等价已有线不重复创建，冲突拒绝。
- `src/theorems/bound_application.py` → 扩展动作及提交。BoundAction新增可选coordinate_ids和coordinate_snapshot，其他模型拒绝携带；候选保存当前双坐标绑定，提交仅放行RM73正确身份／owner／role及快照的直线，原事务负责幂等与回滚。
- `src/theorems/models/model_073.py`、`src/theorems/theorem_library.py` → 新增并注册RM73。propose_bound调用数值两点提案，不接入旧状态执行。
- `tests/test_bound_two_point_line.py` → 新增28项验证，覆盖两题坐标、反序／重排、水平／竖直、缺坐标／来源、旧动作与结果失效、等价／冲突、多线歧义、隔离和幂等。

1168／1199完成坐标事实投影，不代表原题求解；快照保护RM73动作及只读结果。详情见[规格62](../docs/开发规格/62_RM73数值两点直线实现.md)。

## RM73→RM52距离设计入口（最新实现见下节）

870／3239三点事实投影拟接Distance(P,LineOf(A,B))。复用RM73身份／快照与RM52计算，新增复合查询入口及距离依赖证据。当前RM52未检查RM73快照，距离读取未检查目标点变化，已由审查复现；不能将现有计算能力视为可信消费闭环。见[规格63](../docs/开发规格/63_RM73_RM52派生直线距离消费契约.md)。

- `scripts/audit/named_line_distance_contract.py` → 新增消费链审查。CASES选择870／3239三点投影；probe通过内部类型化查询诊断RM73→RM52，用坐标行列式距离交叉核验，并记录目标点变化及派生直线过期后的当前行为；audit保存原题、投影与数据哈希。
- `docs/开发规格/artifacts/named_line_distance_contract.json` → 保存原始查询缺口、数值基线及过期状态反例，供后续实现验收；不是原题求解报告，内部查询绕过明确标记。

## RM73→RM52派生直线距离已接入

- `src/state/named_distance_evidence.py` → 新增距离依赖证据。DistanceSnapshot保存点／线／坐标／方程ID、依赖摘要及距离值；distance_inputs核验唯一新鲜RM73直线与数值目标坐标；make_distance_snapshot组织证据，read_named_distance只核对来源、快照和结果，不计算距离。
- `src/state/transition_state.py` → 扩展复合查询及证据容器。Distance(P,LineOf(A,B))复用无序直线身份和PointLineDistanceQuery；distance_snapshots保存已提交证据，相关距离读取经新鲜度检查，初态／过期返回None。
- `src/theorems/distance_proposals.py` → 扩展RM52消费提案。计算前核验派生线和目标来源，提出距离及匹配证据；已有数值缺证据或依赖过期拒绝补造，数值冲突拒绝，旧显式线／准线分支不变。
- `src/theorems/bound_application.py` → 扩展事务提交。Proposal增加distance_snapshots；应用器核对模型、绑定键、提案数值与当前依赖摘要，将证据和距离一起写入delta及状态，重复幂等、冲突回滚。
- `tests/test_bound_named_distance.py` → 新增21项测试。覆盖两题原始诊断查询、反序重排、点在线上为零、竖线／缩放、旧点／旧线／缺证据、多线歧义、隔离及回滚。

870／3239完成坐标事实投影；原始复合查询解析、消费前核验、证据提交与只读失效检查均接入。详见[规格64](../docs/开发规格/64_RM73_RM52派生直线距离实现.md)，不代表原题求解。

## RM53设计入口（最新实现见下节）

1199／5211仅取双坐标事实投影，诊断目标Distance(A,B)／Distance(E,F)。复用坐标来源与证据事务思路，拟新增点对查询、绑定及独立结果快照；同坐标或同一点距离允许0，不依赖RM73直线身份。见[规格65](../docs/开发规格/65_RM53数值两点距离契约.md)。

- `scripts/audit/point_pair_distance_contract.py` → 新增有限审查。CASES定位1199／5211；probe读取已有坐标与来源，计算距离平方和非负距离，并用独立几何距离核验；audit保留原题、投影及数据哈希，不执行RM53或提交结果。
- `docs/开发规格/artifacts/point_pair_distance_contract.json` → 保存两题坐标投影、查询入口缺口、反序与零距离等诊断证据，供后续实现验收；非原题求解或RM53轨迹。

## RM53数值两点距离已接入

- `src/state/point_pair_distance.py` → 新增点对查询与证据。PointPairDistanceQuery按排序二元组表达距离目标并保留重复点；pair_inputs核验数值坐标／来源并生成摘要；PointPairDistanceSnapshot保存点对、坐标ID、摘要及结果，read_pair_distance只核验并读取，不推导距离。
- `src/solver/point_pair_operations.py` → 新增公共计算。point_pair_distance返回非负距离、坐标差及平方和；允许同一点／同坐标为0，不写状态。
- `src/theorems/point_pair_proposals.py` → 新增RM53绑定及提案。check_point_pair_binding核验双坐标ID和动作快照；derive_point_distance提出距离及证据，拒绝旧值缺证据／依赖过期和冲突，不创建直线。
- `src/state/transition_state.py` → 扩展类型分派与证据容器。两个声明Point的Distance解析为点对查询；point_pair_snapshots保存提交证据，读取过期返回None，既有点线／焦点查询继续按类型分派。
- `src/theorems/bound_application.py` → 扩展动作和事务。新增points二元组，仅RM53可用；复用coordinate_ids／coordinate_snapshot，候选由点对查询产生。Proposal增加点对证据映射，应用器核验绑定、键及摘要，将距离与证据原子提交并记录delta。
- `src/theorems/models/model_053.py` → 扩展已有模型入口。propose_bound调用独立数值点对提案，旧入口保留。
- `tests/test_bound_point_pair_distance.py` → 新增25项，验证两题、零距离、反序重排、水平／竖直、来源失效、相同距离不同坐标、隔离和回滚；`tests/test_bound_line_distance.py`调整旧语法断言，确认合法同点查询在点线专用切片中为inapplicable。

1199／5211完成双坐标投影，允许零距离；不依赖RM73／RM52。见[规格66](../docs/开发规格/66_RM53数值两点距离实现.md)。
