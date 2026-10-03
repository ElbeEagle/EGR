# 关键接口参考

更新：2026-10-03。本页描述当前可调用接口；完整设计见[开发规格](../docs/开发规格/02_状态表示与应用器接口.md)，模块导航见[实现地图](project_structure.md)。新绑定执行接口与旧流程并存，不可直接混用两套状态。

## 新绑定执行接口：当前开发入口

| 接口（导入路径） | 输入与输出／职责 |
| --- | --- |
| `TransitionState.from_facts(facts, query)`（`src.state.transition_state`） | 事实字符串与标量／渐近线集合／抛物线焦点距离／点到独立直线查询 → 初态；只解析显式事实与定义域，不执行定理。非法／不支持的输入可抛出解析异常 |
| `BoundAction`（`src.theorems.bound_application`） | `model_id, mode`；曲线模式使用 `curve`，独立直线 RM52 使用 `line` 且 `curve/equation_id=None`；曲线模式的 `equation_id=None` 仅限无曲线方程的普通参数模式；其他可选 `line_equation_id / relation_id / peer_curve / peer_equation_id / point / coordinate_id`；明确模型、应用方式和所属对象／方程 |
| `enumerate_actions(state, model_id, mode=None)`（同上） | 枚举结构绑定候选，目前支持 RM2–13、RM17、RM21、RM29、RM52；可按模式过滤；不保证候选已满足所有数学前提 |
| `TheoremModel.propose_bound(state, action)`（`src.theorems.base_model`） | 模型提出 `Proposal`；基类默认未实现，目前 RM2–13、RM17、RM21、RM29、RM52 提供有限模式实现 |
| `BoundApplicator(library=None).apply(state, action)`（`src.theorems.bound_application`） | 在隔离副本上调用模型，校验候选后提交到传入状态，返回 `TransitionResult` |
| `state.abstract(curve)` | 返回既有 `AbstractState` 的兼容视图；不是新对象感知编码器 |
| `state.extract_answer()` | 读取标量赋值或模型生成的两条渐近线表达式（各自等于零），或 RM17／RM2 已提交的焦半径、RM52 已提交的点到直线距离；未确定返回 `None`，不在此求解 |
| `solve_asymptote_slice(facts, query)`（`src.reasoning.bound_slice`） | 固定 RM5/RM6→RM21，返回 `SliceResult(status, state, transitions, diagnostic)`，通过 `.answer` 读取答案 |
| `solve_shared_focus_slice(facts, query)`（同上） | 固定 RM3/RM4→RM11→RM5/RM6→RM12；要求唯一椭圆—双曲线共焦点绑定，返回 `SliceResult` |
| `solve_forward_asymptote_slice(facts, query)`（同上） | 固定 RM5/RM6→RM21 正向，按渐近线查询对象绑定，返回 `SliceResult` |
| `solve_parabola_focal_slice(facts, query)`（同上） | 唯一点—曲线—方程绑定，预检 RM7–10 参数恢复方向，再回放所选标准模型→RM17 |
| `solve_parabola_definition_slice(facts, query)`（同上） | 复用方向预检，固定标准模型→RM29→RM52→RM2；不调用 RM17 |
| `solve_point_line_distance_slice(facts, query)`（同上） | 按独立点／直线查询过滤 RM52 候选，唯一绑定时执行一步；缺失或多方程返回 undetermined |
| `solve_directrix_alias_distance_slice(facts, query)`（同上） | 原始准线别名查询，预检标准方向后固定 RM7–10→RM29→RM52 |
| `replay_actions(state, actions)`（同上） | 指定动作诊断回放；保留失败尝试，首个失败处停止，不是选择器 |

### 状态与结果约定

- `EquationFact`：`fact_id / owner / role / expression / source`，表达式按左侧减右侧等于零保存。
- `TransitionState`：`entities / symbols / equations / constraints / query` 为题目信息；`properties[(对象, 属性)]` 保存对象属性，`values[Symbol]` 保存标量赋值；另有 `provenance / history / revision`。
- `AsymptoteQuery(curve)`：由 `Expression(Asymptote(G))` 解析；只读取已生成的完整方程对，题目给出的一条渐近线不算完整答案。
- `PointCoordinates` 与 `PointOnCurve`：给定或模型生成的坐标／显式点归属事实，分别保存于 `coordinates[point]`、`incidences[fact_id]`；初态只解析，不代入求参数。
- `FocalDistanceQuery(point, curve)`：由 `Distance(A, Focus(G))` 解析；只读 `properties[(G, focal_radius:A)]`。
- `PointLineDistanceQuery(point, line)`：由 `Distance(A, l)` 解析，要求 Point／Line 类型；直线的方程 role 为 `line`。只读唯一所属方程对应的距离属性，多方程不任意选取。
- `FocusEquality`：关系事实 ID、两个曲线名称和原表达；`state.relations` 保存给定关系，不在初态自动实例化。
- `CurveFrame`：绑定的方程 ID、中心和轴向；`state.frames` 由标准模型生成，当前支持原点中心、`axis=x/y`；a² 始终对应长半轴／实半轴平方。抛物线用原点顶点框架，另记 `direction=right/left/up/down`，不把顶点解释为对称中心。
- `Proposal`：`properties / values / constraints / frames / equations / coordinates / read_facts / operations / candidates`。模型提出变化，提交由应用器统一完成。
- `TransitionResult`：状态、绑定动作、前后版本、`delta`、读取事实 ID、操作、候选解和诊断。只有成功提交进入 `state.history`；失败尝试需由调用方保留返回结果。

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

## 扩展与验证

扩展模型时，在原模型类增加绑定模式，复用 `transition_primitives.py` 中的公共计算；RM3–6 共用 `src/theorems/standard_proposals.py`；RM11/RM12 共用 `src/theorems/parameter_proposals.py` 构造参数提案，通过 `Proposal` 交给应用器；不要为每个模型另建状态或提交逻辑。跨曲线关系已实现上述有限共焦点模式；其他关系、分支状态及统一训练 schema 仍需按规格逐批实现。

快速检查：`python3 -m pytest -q tests/test_bound_transition_slice.py tests/test_bound_shared_focus.py tests/test_bound_parameter_modes.py tests/test_bound_y_axis.py tests/test_bound_parabola.py`。

ID 9 回放：`python3 -m src.reasoning.bound_slice --mode shared-focus --problem-id 9`。正向回放：`python3 -m src.reasoning.bound_slice --mode asymptote-forward --problem-id 65`。y 轴案例将 `--problem-id` 改为 `380`。ID 5：`python3 -m src.reasoning.bound_slice --mode parabola-focal --problem-id 5`。当前 CLI 输出 `bound-slice-v7`（新增 point_role 属性点绑定）；旧 v1–v6 trace 保留为历史证据。
涉及旧符号／模型兼容时，追加 `tests/test_theorem_missing_models.py`、`tests/test_solver_symbolic.py`、`tests/test_answer_extractor_symbolic_solver.py`；涉及评估口径时追加 `tests/test_evaluation_protocol.py`。

仅在签名、行为或适用范围变化时更新本页；测试数量和批次结果写入开发记录。

### 准线与公共距离操作

`src.solver.distance_operations.point_to_line_distance(expression, x, y, xy)` 计算一般 Ax+By+C=0 的精确距离，支持水平／竖直／斜线及零距离；目前系数和坐标必须为有限实数，拒绝非线性、退化或未定输入。RM52 同时支持 `Line` 声明＋`Expression(l)=(...)` 的独立直线和对象所属准线。一般模式显式绑定 `line / line_equation_id / point / coordinate_id`；不要求抛物线或框架。距离属性依赖不可绕过应用器随意改写；RM2 消费已提交事实，准线身份与点归属仍单独核验。

定义路径：`python3 -m src.reasoning.bound_slice --mode parabola-definition --problem-id 5`。原定义路径的 v4 证据保留，新运行输出 v5。测试增加 `tests/test_bound_parabola_definition.py`。


一般直线入口示例：

```python
from src.reasoning.bound_slice import solve_point_line_distance_slice
r = solve_point_line_distance_slice(
    "l: Line;Expression(l)=(y=-2);F: Point;Coordinate(F)=(0,2)",
    "Distance(F, l)",
)
assert r.status == "solved" and r.answer == 4
```

RM52 提案统一位于 `src/theorems/distance_proposals.py`，沿用已有公共公式；新增测试 `tests/test_bound_line_distance.py`。仅支持显式命名点／直线距离，支持下述抛物线准线别名，支持下述抛物线焦点别名，不自动解析坐标轴、轨迹或距离范围。CLI `--mode point-line-distance` 要求数据记录本身符合该输入范围；本批真实案例是显式事实子案例，不能直接用原题查询冒充整题回放。


### 抛物线准线别名

`DirectrixAlias(fact_id, curve, line, source)` 存于 `state.directrix_aliases`，解析 `Directrix(G)=l`，要求 G 为 Parabola、l 为 Line；初态不计算准线。`state.line_bindings(line)` 只解析对象身份，返回 `(EquationFact, alias_fact_id或None)`；准线别名必须已有 RM29 的 `derived:{curve}:directrix`。不复制方程，也不改变其 owner／role。

RM52 命名准线动作使用 `line=l`、`line_equation_id=derived:G:directrix`、`relation_id=别名事实ID`，仍令 curve/equation_id 为空；别名关系与方程均记入读取来源。距离存于 l 所属属性；查询只读。重复别名、多曲线共用一个别名、别名同时带独立方程暂不合并，固定链返回 undetermined，直接绑定不适用。

原题回放：`python3 -m src.reasoning.bound_slice --mode directrix-alias-distance --problem-id 3723`。沿用已有动作字段，alias 解析操作和坐标增量见 v6；测试 `tests/test_bound_directrix_alias.py`。命名准线身份解析与 RM52 距离计算共用原有入口，专用固定链负责显式执行标准模型及 RM29 前置步骤。


### 抛物线焦点坐标实例化

`FocusAlias(fact_id, curve, point, source)` 存于 `state.focus_aliases`，解析 `Focus(G)=F`，限 Parabola／Point。初态不生成坐标；原有 `Focus(G)=Focus(H)` 共焦点关系保持独立。

RM7–10 在提取／恢复标准参数的同一次提案中，针对所绑定曲线的显式焦点别名生成 `Proposal.coordinates[point]`，稳定 ID 为 `derived:{curve}:focus:{point}`，操作记为 `instantiate_focus_alias`。应用器校验别名、焦点属性及有限实数坐标，和所有其他增量一起提交；delta.coordinates 与 provenance 记录坐标来源（曲线方程、别名及 action）。已有相同坐标保留原 ID／source，不同坐标 conflict，符号未定坐标或同一点多个焦点声明 undetermined，均不提交。

`solve_directrix_alias_distance_slice` 复用标准模型→RM29→RM52；坐标可以显式给定，也可由同一抛物线标准模型生成。RM52 在前两步成功后绑定实际坐标 ID，查询仍只读。不新增几何推导模型或将实例化单独计为选择器动作。

回放 ID 946／1793：`python3 -m src.reasoning.bound_slice --mode directrix-alias-distance --problem-id 946`（另一题改为 1793）。测试：`tests/test_bound_focus_alias.py`。


### RM72 参数恢复与交点事实（D5 已确认）

`TransitionState.from_facts(facts, None)` 可创建无查询诊断初态，extract_answer 返回 None。新增 `Coordinate(OneOf(Intersection(H,G)))=(x0,y0)`，限 Line—Parabola：按原事实 ID 创建内部点 `@intersection:{fact_id}`，复用坐标及两项归属；不执行求参。PointOnCurve 现支持 Line。

`enumerate_actions(state,72,'recover_from_point')` 枚举直线／点／归属绑定。动作使用 line、line_equation_id、point、coordinate_id、relation_id，curve/equation_id 为空。RM72 提案位于 `src/theorems/line_proposals.py`，由 y=kx+b 与点斜式的一致性恢复一个参数，同时提交 slope/intercept。y 系数须非零可证明；水平线可用，竖直线不支持；多根不提交，条件不足 undetermined，无解 conflict。

应用器保留与当前赋值无关的未定条件，但涉及赋值的约束必须验证，已为假的约束一律拒绝。既有 RM7 点恢复与公共数值代入／实根筛选复用。参数恢复接口可独立用于子链，原题现已由下述焦点到直线入口接通。正向 RM72 旧接口保留，未新增正向绑定实现。


### 焦点属性到独立直线距离

`FocusLineDistanceQuery(curve,line)` 解析 `Distance(Focus(G),H)`，要求 Parabola／Line；初态不计算焦点或参数。查询只读取 `properties[(H, focus_line_distance:G:{line_equation_id})]`，直线方程缺失或不唯一时返回 None。

RM52 新增 `focus_line_distance` 模式，BoundAction 使用 `point_role='focus'`、curve/equation_id、line/line_equation_id；point/coordinate_id/relation_id 留空，不生成命名点。枚举是结构候选；执行须已有匹配曲线方程的框架、p 与 focus_x/y，复用 bound_parabola 校验。只代入已有 values 后调用公共距离公式，缺失参数不求解。来源包含焦点属性、框架、曲线和直线方程以及标量值。

`solve_intersection_focus_distance_slice(facts,query)` 固定选择唯一共享已知点，预检标准方向，回放 RM7–10 recover_from_point→RM72 recover_from_point→RM52；不是学习型选择器，不读 models/process/答案。原始 ID 7260 命令：`python3 -m src.reasoning.bound_slice --mode intersection-focus-distance --problem-id 7260`。

本模式限抛物线焦点与独立 Line 方程；公共距离支持竖直线，但固定链的 RM72 恢复仍限非竖直线。测试 `tests/test_bound_focus_line_distance.py`。既有命名点／别名路径保持兼容。


### RM13 正向离心率

`EccentricityQuery(curve)` 解析 Ellipse／Hyperbola 的 `Eccentricity(G)`，只读 properties[(G,eccentricity)]。`enumerate_actions(state,13,'derive_eccentricity')` 产生曲线／方程绑定；其他点线绑定字段不适用。

RM13 必须已有 a_sq、b_sq、c_sq 和匹配标准框架；复用 bound_parameters，检查有限实数、正值及参数恒等式后，仅提交 e=√(c²/a²)。缺 c² 返回 inapplicable，不暗中执行 RM11/12；冲突回滚，重复 no_op。首批限非圆标准椭圆／非退化双曲线、原点中心与 x/y 轴，符号值返回 undetermined，不处理范围和反向求参。

`solve_eccentricity_slice(facts,query)` 固定执行标准模型→RM11/12 derive_c_sq→RM13；唯一方程及轴向预检，无模型预测。命令：`python3 -m src.reasoning.bound_slice --mode eccentricity --problem-id 5988`（其余 ID：7488、1586、4528）。动作 schema 不变，继续 v7 trace。实现 `eccentricity_proposals.py`，测试 `test_bound_eccentricity.py`。
