# 关键接口参考

更新：2026-09-24。本页描述当前可调用接口；完整设计见[开发规格](../docs/开发规格/02_状态表示与应用器接口.md)，模块导航见[实现地图](project_structure.md)。新绑定执行接口与旧流程并存，不可直接混用两套状态。

## 新绑定执行接口：当前开发入口

| 接口（导入路径） | 输入与输出／职责 |
| --- | --- |
| `TransitionState.from_facts(facts, query)`（`src.state.transition_state`） | 事实字符串与标量／渐近线集合查询 → 初态；只解析显式事实与定义域，不执行定理。非法／不支持的输入可抛出解析异常 |
| `BoundAction`（`src.theorems.bound_application`） | `model_id, mode, curve`；`equation_id=None` 仅限无曲线方程的普通参数模式；其他可选 `line_equation_id / relation_id / peer_curve / peer_equation_id`；明确模型、应用方式和所属对象／方程 |
| `enumerate_actions(state, model_id, mode=None)`（同上） | 枚举结构绑定候选，目前支持 RM3/5/11/12/21；可按模式过滤；不保证候选已满足所有数学前提 |
| `TheoremModel.propose_bound(state, action)`（`src.theorems.base_model`） | 模型提出 `Proposal`；基类默认未实现，目前 RM3/5/11/12/21 提供有限模式实现 |
| `BoundApplicator(library=None).apply(state, action)`（`src.theorems.bound_application`） | 在隔离副本上调用模型，校验候选后提交到传入状态，返回 `TransitionResult` |
| `state.abstract(curve)` | 返回既有 `AbstractState` 的兼容视图；不是新对象感知编码器 |
| `state.extract_answer()` | 读取标量赋值或模型生成的两条渐近线表达式（各自等于零），未确定返回 `None`；不在此求解 |
| `solve_asymptote_slice(facts, query)`（`src.reasoning.bound_slice`） | 固定 RM5→RM21，返回 `SliceResult(status, state, transitions, diagnostic)`，通过 `.answer` 读取答案 |
| `solve_shared_focus_slice(facts, query)`（同上） | 固定 RM3→RM11→RM5→RM12；要求唯一椭圆—双曲线共焦点绑定，返回 `SliceResult` |
| `solve_forward_asymptote_slice(facts, query)`（同上） | 固定 RM5→RM21 正向，按渐近线查询对象绑定，返回 `SliceResult` |
| `replay_actions(state, actions)`（同上） | 指定动作诊断回放；保留失败尝试，首个失败处停止，不是选择器 |

### 状态与结果约定

- `EquationFact`：`fact_id / owner / role / expression / source`，表达式按左侧减右侧等于零保存。
- `TransitionState`：`entities / symbols / equations / constraints / query` 为题目信息；`properties[(对象, 属性)]` 保存对象属性，`values[Symbol]` 保存标量赋值；另有 `provenance / history / revision`。
- `AsymptoteQuery(curve)`：由 `Expression(Asymptote(G))` 解析；只读取已生成的完整方程对，题目给出的一条渐近线不算完整答案。
- `FocusEquality`：关系事实 ID、两个曲线名称和原表达；`state.relations` 保存给定关系，不在初态自动实例化。
- `CurveFrame`：绑定的方程 ID、中心和轴向；`state.frames` 由标准模型生成，当前只支持原点中心／x 轴。
- `Proposal`：`properties / values / constraints / frames / equations / read_facts / operations / candidates`。模型提出变化，提交由应用器统一完成。
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
| RM3 `extract_parameters` | 标准椭圆且 a²>b²>0 可判定 → 对象参数、中心和轴向 |
| RM11/RM12 `derive_a_sq / derive_b_sq / derive_c_sq` | 同一曲线任意另两个平方参数 → 目标平方参数；检查三者正值及已有事实一致性 |
| RM11/RM12 `constrain_parameters` | 同一曲线 a²、b²、c² 的三个表达式 → 利用参数恒等式求标量查询，筛选正值条件；多解不提交 |
| RM5 `extract_parameters` | x² 分母已知为正的标准双曲线 → 参数、中心和轴向；必要时由类型推导 b²>0 并记录条件来源 |
| RM12 `constrain_shared_focus` | 两曲线标准参数／框架、给定共焦点关系、另一椭圆已有 c² → 公共关系实例化及 c²=a²+b² 参数求解 |
| RM21 `derive_asymptotes` | 已有双曲线参数与标准框架 → 两条对象所属渐近线方程，不推导 c 或离心率 |
| RM21 `constrain_parameters` | RM5 属性、同一曲线的已知渐近线及条件 → 渐近线斜率约束、实根筛选、唯一标量赋值 |

当前解析只覆盖切片需要的声明、算术、等式、比较条件、已知渐近线和 `Focus(G)=Focus(H)`；查询支持已声明标量和上述渐近线集合。参数求解限至多二次的一元实多项式。ID 2 缺少 m>0 时保留 ±5，不默认取正根。各固定链要求相应绑定唯一；尚无多分支搜索或通用超时。共焦点模式仍限原有椭圆—双曲线组合。

普通参数模式消费已有 `properties[(curve, a_sq/b_sq/c_sq)]`；本批未扩展自然语言长度事实的解析。无曲线方程时可仅绑定对象；若存在方程，必须显式绑定并具有已建立的标准框架。公式为椭圆 a²=b²+c²、双曲线 c²=a²+b²；目标未能证明为正时返回未确定，零／负值拒绝。正向渐近线仍限原点中心、x 轴焦向；重复提交按稳定派生方程 ID 去重，不承诺全局等价方程合并。

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

扩展模型时，在原模型类增加绑定模式，复用 `transition_primitives.py` 中的公共计算；RM11/RM12 共用 `src/theorems/parameter_proposals.py` 构造参数提案，通过 `Proposal` 交给应用器；不要为每个模型另建状态或提交逻辑。跨曲线关系已实现上述有限共焦点模式；其他关系、分支状态及统一训练 schema 仍需按规格逐批实现。

快速检查：`python3 -m pytest -q tests/test_bound_transition_slice.py tests/test_bound_shared_focus.py tests/test_bound_parameter_modes.py`。

ID 9 回放：`python3 -m src.reasoning.bound_slice --mode shared-focus --problem-id 9`。正向回放：`python3 -m src.reasoning.bound_slice --mode asymptote-forward --problem-id 65`。当前 CLI 输出 `bound-slice-v3`（新增派生方程 delta 与方程对答案）；旧 v1/v2 trace 保留为历史证据。
涉及旧符号／模型兼容时，追加 `tests/test_theorem_missing_models.py`、`tests/test_solver_symbolic.py`、`tests/test_answer_extractor_symbolic_solver.py`；涉及评估口径时追加 `tests/test_evaluation_protocol.py`。

仅在签名、行为或适用范围变化时更新本页；测试数量和批次结果写入开发记录。
