# 关键接口参考

更新：2026-09-24。本页描述当前可调用接口；完整设计见[开发规格](../docs/开发规格/02_状态表示与应用器接口.md)，模块导航见[实现地图](project_structure.md)。新绑定执行接口与旧流程并存，不可直接混用两套状态。

## 新绑定执行接口：当前开发入口

| 接口（导入路径） | 输入与输出／职责 |
| --- | --- |
| `TransitionState.from_facts(facts, query)`（`src.state.transition_state`） | 事实字符串与已声明标量查询 → 初态；只解析显式事实与定义域，不执行定理。非法／不支持的输入可抛出解析异常 |
| `BoundAction`（`src.theorems.bound_application`） | `model_id, mode, curve, equation_id, line_equation_id=None`；明确模型、应用方式和所属对象／方程 |
| `enumerate_actions(state, model_id)`（同上） | 枚举结构绑定候选，目前仅 RM5/21；不保证候选已满足所有数学前提 |
| `TheoremModel.propose_bound(state, action)`（`src.theorems.base_model`） | 模型提出 `Proposal`；基类默认未实现，目前 RM5/21 提供实现 |
| `BoundApplicator(library=None).apply(state, action)`（`src.theorems.bound_application`） | 在隔离副本上调用模型，校验候选后提交到传入状态，返回 `TransitionResult` |
| `state.abstract(curve)` | 返回既有 `AbstractState` 的兼容视图；不是新对象感知编码器 |
| `state.extract_answer()` | 读取已确定的查询赋值，未确定返回 `None`；不在此求解 |
| `solve_asymptote_slice(facts, query)`（`src.reasoning.bound_slice`） | 固定 RM5→RM21，返回 `SliceResult(status, state, transitions, diagnostic)`，通过 `.answer` 读取答案 |

### 状态与结果约定

- `EquationFact`：`fact_id / owner / role / expression / source`，表达式按左侧减右侧等于零保存。
- `TransitionState`：`entities / symbols / equations / constraints / query` 为题目信息；`properties[(对象, 属性)]` 保存对象属性，`values[Symbol]` 保存标量赋值；另有 `provenance / history / revision`。
- `Proposal`：`properties / values / read_facts / operations / candidates`。模型提出变化，提交由应用器统一完成。
- `TransitionResult`：状态、绑定动作、前后版本、`delta`、读取事实 ID、操作、候选解和诊断。只有成功提交进入 `state.history`；失败尝试需由调用方保留返回结果。

| 转换状态 | 含义 |
| --- | --- |
| `applied` | 存在有效增量，已提交并递增版本 |
| `no_op` | 没有新增信息，状态不变 |
| `inapplicable` | 绑定／前提不适用 |
| `undetermined` | 多个可行根或条件尚不能判定，不选择分支 |
| `conflict` | 候选与已有事实或约束冲突 |
| `failed` | 已捕获的解析／实现错误；不承诺将所有程序异常都转成该状态 |

非 `applied` 返回不提交状态变化。已知标量回代仅归约已有属性并记录操作，不引入新定理或要求选择器额外预测 RM78。
入口 `SliceResult.status` 另外使用 `solved / unresolved`；不要与单步转换状态混淆。

### 已支持的模型模式与边界

| 模型／模式 | 前提 → 输出 |
| --- | --- |
| RM5 `extract_parameters` | 原点中心、焦点在 x 轴的标准双曲线及可判定的符号条件 → 对象所属的 `a_sq / b_sq` |
| RM21 `constrain_parameters` | RM5 属性、同一曲线的已知渐近线及条件 → 渐近线斜率约束、实根筛选、唯一标量赋值 |

当前解析只覆盖切片需要的声明、算术、等式、比较条件和已知渐近线表达；查询限已声明标量。参数求解限至多二次的一元实多项式。缺少 m>0 时保留 ±5，不默认取正根。入口要求唯一曲线—渐近线绑定；尚无多分支搜索、通用超时或 RM21 正向模式的新接口。

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

扩展模型时，在原模型类增加绑定模式，复用 `transition_primitives.py` 中的公共计算，通过 `Proposal` 交给应用器；不要为每个模型另建状态或提交逻辑。跨曲线关系、分支状态及统一训练 schema 仍需按规格逐批实现。

快速检查：`python3 -m pytest -q tests/test_bound_transition_slice.py`。
涉及旧符号／模型兼容时，追加 `tests/test_theorem_missing_models.py`、`tests/test_solver_symbolic.py`、`tests/test_answer_extractor_symbolic_solver.py`；涉及评估口径时追加 `tests/test_evaluation_protocol.py`。

仅在签名、行为或适用范围变化时更新本页；测试数量和批次结果写入开发记录。
