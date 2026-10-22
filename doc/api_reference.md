# 关键接口参考

更新：2026-10-03。本页描述当前可调用接口；完整设计见[开发规格](../docs/开发规格/02_状态表示与应用器接口.md)，模块导航见[实现地图](project_structure.md)。新绑定执行接口与旧流程并存，不可直接混用两套状态。

## 新绑定执行接口：当前开发入口

| 接口（导入路径） | 输入与输出／职责 |
| --- | --- |
| `TransitionState.from_facts(facts, query)`（`src.state.transition_state`） | 事实字符串与已支持的查询（或 None）→ 初态；只解析显式事实与定义域，不执行定理。非法／不支持的输入可抛出解析异常 |
| `BoundAction`（`src.theorems.bound_application`） | `model_id, mode`；曲线模式使用 `curve`，独立直线 RM52 使用 `line` 且 `curve/equation_id=None`；曲线模式的 `equation_id=None` 仅限无曲线方程的普通参数模式；其他可选 `line_equation_id / relation_id / peer_curve / peer_equation_id / point / coordinate_id`；明确模型、应用方式和所属对象／方程 |
| `enumerate_actions(state, model_id, mode=None)`（同上） | 枚举结构绑定候选，目前支持 RM2–13、RM17、RM21、RM29、RM33、RM39、RM42/43、RM50、RM52、RM55、RM72、RM78；可按模式过滤；不保证候选已满足所有数学前提 |
| `TheoremModel.propose_bound(state, action)`（`src.theorems.base_model`） | 模型提出 `Proposal`；基类默认未实现，目前 RM2–13、RM17、RM21、RM29、RM33、RM39、RM42/43、RM50、RM52、RM55、RM72、RM78 提供有限模式实现 |
| `BoundApplicator(library=None).apply(state, action)`（`src.theorems.bound_application`） | 在隔离副本上调用模型，校验候选后提交到传入状态，返回 `TransitionResult` |
| `state.abstract(curve)` | 返回既有 `AbstractState` 的兼容视图；不是新对象感知编码器 |
| `state.extract_answer()` | 按查询类型读取已提交的标量、渐近线、焦半径、点／焦点到直线距离、离心率、切线方程或弦长；未确定返回 `None`，不在此推导 |
| `solve_asymptote_slice(facts, query)`（`src.reasoning.bound_slice`） | 固定 RM5/RM6→RM21，返回 `SliceResult(status, state, transitions, diagnostic)`，通过 `.answer` 读取答案 |
| `solve_shared_focus_slice(facts, query)`（同上） | 固定 RM3/RM4→RM11→RM5/RM6→RM12；要求唯一椭圆—双曲线共焦点绑定，返回 `SliceResult` |
| `solve_forward_asymptote_slice(facts, query)`（同上） | 固定 RM5/RM6→RM21 正向，按渐近线查询对象绑定，返回 `SliceResult` |
| `solve_parabola_focal_slice(facts, query)`（同上） | 唯一点—曲线—方程绑定，预检 RM7–10 参数恢复方向，再回放所选标准模型→RM17 |
| `solve_parabola_definition_slice(facts, query)`（同上） | 复用方向预检，固定标准模型→RM29→RM52→RM2；不调用 RM17 |
| `solve_point_line_distance_slice(facts, query)`（同上） | 按独立点／直线查询过滤 RM52 候选，唯一绑定时执行一步；缺失或多方程返回 undetermined |
| `solve_directrix_alias_distance_slice(facts, query)`（同上） | 原始准线别名查询，预检标准方向后固定 RM7–10→RM29→RM52 |
| `replay_actions(state, actions)`（同上） | 指定动作诊断回放；保留失败尝试，首个失败处停止，不是选择器 |

### 核心函数的实际用途

`*_proposal(s).py` 中的函数组织模型应用，返回 `Proposal`，由应用器统一提交。`bound` 表示已指定对象和方程，不表示数学上的“有界”。以下是近期新增／扩展的核心函数，不列内部辅助函数全集。

| 定义（所在模块） | 具体操作与结果 |
| --- | --- |
| `instantiate_shared_focus`（`transition_primitives.py`） | 核验两曲线框架相容，将共焦点关系实例化为目标曲线的 c² 值及操作记录，供 RM12 使用 |
| `standard_proposal`（`standard_proposals.py`） | 从标准椭圆／双曲线方程提取半轴平方、轴向及条件，返回 RM3–6 参数提案 |
| `parameter_proposal`（`parameter_proposals.py`） | 利用 a²、b²、c² 恒等式计算缺失参数或求标量查询，返回 RM11/RM12 提案 |
| `parabola_coefficient / substitute_point / parabola_geometry`（`parabola_operations.py`） | 分别提取抛物线标准系数、计算点代入残差、由系数和方向计算 p 与焦点；仅返回计算结果 |
| `standard_parabola_proposal`（`parabola_proposals.py`） | 提取参数，或利用已知曲线上点恢复参数；提出 p、焦点、框架，以及有显式别名时的命名焦点坐标 |
| `focal_radius_proposal / directrix_proposal / definition_proposal`（同上） | 分别组织 RM17 焦半径计算、RM29 准线方程计算、RM2 从既有准线距离读取焦半径的提案 |
| `point_to_line_distance`（`distance_operations.py`） | 从数值点坐标和一般直线方程计算精确距离，供距离提案调用 |
| `point_line_distance_proposal / focus_line_distance_proposal`（`distance_proposals.py`） | 分别读取命名点坐标／已提交焦点属性，调用距离公式并提出 RM52 距离属性 |
| `recover_line_from_point`（`line_proposals.py`） | 用已知点满足直线方程这一条件恢复一个参数，提出 RM72 参数值及斜率／截距 |
| `derive_eccentricity`（`eccentricity_proposals.py`） | 核验已有平方参数后计算 e=√(c²/a²)，返回 RM13 离心率属性提案 |
| `derive_parabola_tangent`（`tangent_proposals.py`） | 核验已知点在抛物线上，用标准属性计算切线方程，返回 RM39 派生方程提案 |
| `substitute_line_in_parabola`（`intersection_operations.py`） | 将直线改写并代入抛物线，返回一元方程及坐标还原映射，不求根 |
| `substitute_bound_line`（`intersection_proposals.py`） | 核验指定曲线／直线，调用上述消元函数，返回含消元记录与来源的 RM78 提案 |

### 状态与结果约定

以下类型均保存信息；计算、解析和提交由相应函数完成。查询类型只表示“要求什么”，答案统一由 `state.extract_answer()` 读取。

- `EquationFact`（对象所属方程记录）：`fact_id / owner / role / expression / source`，表达式按左侧减右侧等于零保存。
- `TransitionState`（题目及推理过程的当前状态）：`entities / symbols / equations / constraints / query` 为题目信息；`properties[(对象, 属性)]` 保存对象属性，`values[Symbol]` 保存标量赋值；另有 `provenance / history / revision`。
- `AsymptoteQuery(curve)`（指定曲线的渐近线方程查询）：由 `Expression(Asymptote(G))` 解析；只读取已生成的完整方程对，题目给出的一条渐近线不算完整答案。
- `PointCoordinates` 与 `PointOnCurve`：给定或模型生成的坐标／显式点归属事实，分别保存于 `coordinates[point]`、`incidences[fact_id]`；初态只解析，不代入求参数。
- `FocalDistanceQuery(point, curve)`（指定点到曲线焦点的距离查询）：由 `Distance(A, Focus(G))` 解析；只读 `properties[(G, focal_radius:A)]`。
- `PointLineDistanceQuery(point, line)`（指定点到指定直线的距离查询）：由 `Distance(A, l)` 解析，要求 Point／Line 类型；直线的方程 role 为 `line`。只读唯一所属方程对应的距离属性，多方程不任意选取。
- `FocusEquality`（两曲线共焦点关系记录）：关系事实 ID、两个曲线名称和原表达；`state.relations` 保存给定关系，不在初态自动实例化。
- `CurveFrame`（曲线方程的几何框架记录）：绑定的方程 ID、中心和轴向；`state.frames` 由标准模型生成，当前支持原点中心、`axis=x/y`；a² 始终对应长半轴／实半轴平方。抛物线用原点顶点框架，另记 `direction=right/left/up/down`，不把顶点解释为对称中心。
- `Proposal`（待提交的状态更新提案）：保存 properties、values、constraints、frames、equations、coordinates、intersection_reductions 等变化及读取来源／操作。由模型生成，应用器统一校验提交。
- `TransitionResult`（一次动作的执行结果记录）：状态、绑定动作、前后版本、`delta`、读取事实 ID、操作、候选解和诊断。只有成功提交进入 `state.history`；失败尝试需由调用方保留返回结果。

| 转换状态 | 含义 |
| --- | --- |
| `applied` | 存在有效增量，已提交并递增版本 |
| `no_op` | 没有新增信息，状态不变 |
| `inapplicable` | 绑定／前提不适用 |
| `undetermined` | 多个可行根或条件尚不能判定，不选择分支 |
| `conflict` | 候选与已有事实或约束冲突 |
| `failed` | 已捕获的解析／实现错误；不承诺将所有程序异常都转成该状态 |

非 `applied` 返回不提交状态变化。新增条件／几何框架／派生方程与属性、赋值一起校验并提交，纳入 delta 和来源；条件矛盾检查目前限可判定的常量／一元条件。已知标量回代归约已有属性及模型生成的方程，保留题目原方程并记录操作，不引入新定理或要求选择器额外预测 RM78。
入口 `SliceResult.status` 另外使用 `solved / unresolved`；不要与单步转换状态混淆。

### 已支持的模型模式与边界

| 模型／模式 | 前提 → 输出 |
| --- | --- |
| RM7–10 `extract_parameters / recover_from_point` | 标准式 v²=2pu；可从已知系数提取，或绑定数值坐标点实例化归属、恢复唯一参数后确认方向；提交 p、focus_x/y 和框架，不生成准线 |
| RM29 `derive_directrix` | 已有且与方程匹配的 p／焦点／方向 → `derived:{curve}:directrix` 方程，role 为 directrix |
| RM52 `point_line_distance` | 显式绑定数值点与独立直线或同曲线所属准线 → `properties[(owner, point_line_distance:{point}:{line_id})]`；owner 分别为 line 或 curve，无需点归属 |
| RM2 `focal_from_directrix` | 核验标准框架、准线匹配及点归属，读取已有点到准线距离 → focal_radius；不重新计算距离 |
| RM17 `focal_radius` | 已有抛物线参数／焦点／方向及同一曲线上的数值点 → u+p/2，提交对象所属焦半径 |
| RM3/RM4 `extract_parameters` | 对应 x/y 轴标准椭圆且 a²>b²>0 可判定 → 对象参数、中心和轴向 |
| RM11/RM12 `derive_a_sq / derive_b_sq / derive_c_sq` | 同一曲线任意另两个平方参数 → 目标平方参数；检查三者正值及已有事实一致性 |
| RM11/RM12 `constrain_parameters` | 同一曲线 a²、b²、c² 的三个表达式 → 利用参数恒等式求标量查询，筛选正值条件；多解不提交 |
| RM5/RM6 `extract_parameters` | 对应 x/y 焦轴分母已知为正的标准双曲线 → 参数、中心和轴向；必要时由类型推导 b²>0 并记录条件来源 |
| RM12 `constrain_shared_focus` | 两曲线标准参数／框架、给定共焦点关系、另一椭圆已有 c² → 公共关系实例化及 c²=a²+b² 参数求解 |
| RM21 `derive_asymptotes` | 已有双曲线参数与标准框架 → 两条对象所属渐近线方程，不推导 c 或离心率 |
| RM21 `constrain_parameters` | RM5/RM6 属性、同一曲线的已知渐近线及条件 → 渐近线斜率约束、实根筛选、唯一标量赋值 |

当前解析只覆盖切片需要的声明、算术、等式、比较条件、已知渐近线和 `Focus(G)=Focus(H)`；另支持 `Parabola`、`Point` 声明、`Coordinate(A)`、`PointOnCurve(A,G)` 和上述焦点距离查询。参数求解限至多二次的一元实多项式。ID 2 缺少 m>0 时保留 ±5，不默认取正根。各固定链要求相应绑定唯一；尚无多分支搜索或通用超时。共焦点模式仍限原有椭圆—双曲线组合。

普通参数模式消费已有 `properties[(curve, a_sq/b_sq/c_sq)]`；本批未扩展自然语言长度事实的解析。无曲线方程时可仅绑定对象；若存在方程，必须显式绑定并具有已建立的标准框架。公式为椭圆 a²=b²+c²、双曲线 c²=a²+b²；目标未能证明为正时返回未确定，零／负值拒绝。渐近线正反向支持原点中心、x/y 轴焦向；斜率平方分别为 b²/a² 和 a²/b²；重复提交按稳定派生方程 ID 去重，不承诺全局等价方程合并。

最小示例（仓库根目录运行）：

```python
from src.reasoning.bound_slice import solve_asymptote_slice

result = solve_asymptote_slice(
    "G: Hyperbola; m: Number; Expression(G) = (x^2/4-y^2/m^2=1); "
    "m>0; Expression(OneOf(Asymptote(G))) = (5*x-2*y=0)",
    "m",
)
assert result.status == "solved" and result.answer == 5
```

固定链通过 `select_standard_action` 在副本上检查两个方向的标准模式，只在唯一可用时回放正式动作；预检不提交状态，不读取 `models` 或答案。它是固定链内的方向判定，不是学习型选择器；预检失败目前仅返回诊断，不生成训练步骤。

抛物线恢复复用原有一元实根筛选，但不以候选方向过滤根：先按给定事实求参数，唯一解确定后才检查开口与 p>0；多根不选分支。坐标需能归约为有限实数，多未知系数、原点导致参数不定、平移／旋转暂不支持。RM17 重验点归属和标准属性；答案读取不调用 RM2/RM29 或一般距离公式。

## 旧流程：复用和迁移参考

| 接口（所在模块） | 当前行为与迁移注意点 |
| --- | --- |
| `StateConstructor(theorem_library=None).construct_from_facts(fact_expressions, query_expressions, reasoning_depth=0)`（`src.state.state_constructor`） | 返回 `(AbstractState, SymbolicState)`；配置库时初始化会自动提取方程参数，与新初态语义不同 |
| `construct_from_symbolic_state(symbolic_state, query_expressions, reasoning_depth)`（同上） | 根据旧符号状态重建抽象特征 |
| `TheoremLibrary.get_model(model_id)`（`src.theorems.theorem_library`） | 返回注册模型或 `None`；ID 范围 0–79 不代表全部模型可稳定执行 |
| `model.can_apply(state)`、`model.apply(state)` | 旧前提判断与原地修改；没有新接口的统一绑定／事务保证 |
| `TheoremLibrary.apply_model(state, model_id)` | 返回布尔值并记录模型 ID；当前未传递 `model.apply` 的返回值，不能将 `True` 等同于有效状态增量 |
| `StateSequenceBuilder(library, constructor).build_sequence(fact_expressions, query_expressions, model_ids)`（`src.state.state_sequence_builder`） | 给定顺序 → 旧 `StateTransition` 列表；不是对原标注执行顺序正确性的证明 |
| `MaxEntropyClassifier`（`src.selector.model_selector`） | 既有分类网络，默认 28 维输入、80 类输出；`forward`、`predict`、`get_top_k` 提供预测基础 |
| `ModelSelector`（`src.reasoning.model_selector`） | 旧推理时策略封装；尚不预测新 `BoundAction` 的对象绑定 |
| `ReasoningEngine(...).solve(facts, query, reasoning_depth=0)`（`src.reasoning.reasoning_engine`） | 返回 `ReasoningResult`；仍运行旧状态和模型应用流程 |
| `AnswerExtractor().extract(symbolic_state, query_expr)`（`src.reasoning.answer_extractor`） | 旧答案处理可能调用 `SymbolicSolver` 推导；不能当作新接口中“只整理答案”的实现 |

`src.solver.symbolic_solver.SymbolicSolver` 已有曲线解析、参数求解及查询计算，可按职责复用；不得绕过新模型应用记录而把隐式求解算作模型执行。

## 数值椭圆中点弦（RM40）

- `src/state/chord_facts.py`：`parse_chord_midpoint`接受已声明Line/Ellipse的`Coordinate(MidPoint(InterceptChord(l,G)))=(m_x,m_y)`，仅有限数值坐标；保存ChordIdentity、AnonymousEndpointPair、ChordMidpoint。同弦重复合并来源，冲突拒绝，无端点坐标。
- `src/state/transition_state.py`：新增三个对应字典；`from_facts`扩展`Expression(l)`到既有NamedLineQuery，`extract_answer`只读取唯一已有线方程，缺少／多个时无答案。
- `src/solver/midpoint_operations.py`：`ellipse_midpoint_chord(x,y,dx,dy,xy)`返回ρ、法向量、规范化一次式；中心未定、非内点冲突。`canonical_numeric_line`用于数值直线等价核验，均不写状态。
- `src/theorems/midpoint_proposals.py`：`check_midpoint_binding`核验弦、匿名对、中点与方程；`derive_midpoint_chord`需已提交标准参数／框架，提出线方程及弦级midpoint_rho、normal_x/y、distinct_real_intersections=2，不直接写状态。
- `src/theorems/bound_application.py`：候选为`BoundAction(40,'derive_midpoint_chord',curve,equation_id,line=line,relation_id=chord_id)`；应用器新增绑定直线派生方程许可，其余复用事务／来源规则。已有线必须数值等价，保留原式。
- `src/reasoning/bound_slice.py`：`solve_midpoint_chord_slice(facts,query)`固定RM3/4→RM40，ID4795实际选RM4。RM54/45独立路径见下节，非强制依赖。

限中心轴对齐非圆数值椭圆；符号中点、命名端点交叉核验未接入。完整职责与验证见[规格34](../docs/开发规格/34_ID4795中点弦与RM40闭环.md)。

## 匿名端点和与椭圆点差（RM54／45）

- `src/theorems/midpoint_proposals.py`：`derive_endpoint_sums`提出`properties[(pair_id,'x_sum'/'y_sum')]`，由已有应用器保存来源；只作中点两倍关系，不生成坐标或实弦资格。`derive_point_difference_chord`必须读取同对的两项属性并核验来源／中点一致性，再使用已提交框架及半轴参数计算方向。
- `src/solver/midpoint_operations.py`：`midpoint_coordinate_sums(xy)`返回坐标和；`ellipse_point_difference(x,y,dx,dy,sums)`返回ρ、统一法向量、直线和原始点差系数，复用`verify_ellipse_midpoint`检查非中心内点。
- `src/theorems/bound_application.py`：同一弦绑定支持`(54,'derive_endpoint_sums')`及`(45,'derive_point_difference_chord')`，其他绑定字段同RM40；RM45获派生直线提交许可，RM54使用属性提交。缺和／来源不可应用，不自动补算。
- `src/reasoning/bound_slice.py`：`solve_point_difference_slice(facts,query)`固定RM3/4→RM54→RM45，CLI为point-difference；原查询只读逻辑不变。

RM54可在标准模型之前执行；RM45需要标准模型及同对坐标和。中心／非内点处理、现有线核验和有限范围见[规格35](../docs/开发规格/35_ID4795端点和与点差路径.md)。

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
