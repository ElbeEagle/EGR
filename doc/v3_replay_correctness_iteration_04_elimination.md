# V3 正确性迭代 04：精确消元模块

## 实现范围

新增 `ExactEliminationClosure`，作为 theorem executor 之外的独立状态闭包。

支持：

- 普通符号 `Term("symbol", ...)` 与 scoped parameter `Term("parameter", ...)`。
- 单方程线性求解。
- 多方程、多未知量精确高斯消元。
- 一元二次方程；仅在根唯一或正性事实唯一选根时提交。
- 非完全平方根保持 `sqrt_positive` 精确表达式，不转浮点。
- 欠定、多合法根、非线性超出能力时保持 unresolved。
- 常量矛盾检测和显式正性过滤。
- 求解结果写入 `SymbolValueOf` 或 `ResolvedParameterOf`，不覆盖原符号表达式。
- 求解 fact 使用 `solver/exact_linear_elimination` provenance，保留参与约束 fact id。

模块已接入 `QuantityGeometryClosure`，因此每次 theorem 应用前后都会进行固定点消元。

## 信息空间和定理调整

- `Expression(Asymptote(G))`、`Slope(OneOf(Asymptote(G)))` 进入结构化 adapter。
- 模型 21 产生 scoped equation：水平双曲线 `k^2*a^2=b^2`，竖直双曲线 `k^2*b^2=a^2`。
- 模型 21 同时产生无量纲 `ParameterRatioOf(..., b2_over_a2)`。
- 模型 13 可由 `e^2=1+b^2/a^2` 在尺度不定时求离心率。
- `Distance(Focus(G),Directrix(G))` 进入结构化 adapter。
- 抛物线标准式增加 `two_p=2p`，模型 29 将焦点到准线距离约束到 `p`。
- selector 轨迹增加 `closure_delta`，单独记录本步由消元/几何闭包新增的 fact。

## 全量收益

对 `data/train_with_models_v3_candidate.json` 的 executable 序列回放：

| 指标 | 消元前 i08 | 当前 i11 | 增量 |
|---|---:|---:|---:|
| APPLIED | 7,775 | 7,795 | +20 |
| 完整序列 | 617 | 635 | +18 |
| 最终答案正确 | 208 | 231 | +23 |
| 严格 selector 轨迹 | 198 | 220 | +22 |
| VALUE_UNRESOLVED | 334 | 328 | -6 |
| 未解析 fact atom | 3,867 | 3,742 | -125 |

答案可计算时正确率为 99.14%；两条 incorrect 仍是已确认的数据错误 ID 887 和 1834，没有新增执行器错误。

新增解出题目清单：`outputs/theorems_v2/v3_elimination_newly_solved.json`，22 条。

最新严格轨迹：`outputs/theorems_v2/v3_executable_i11_selector_usable_trajectories.jsonl`，220 条。

## 当前边界

当前消元器不会处理：

- 含多个未知量乘积的一般非线性系统。
- 三角函数、绝对值分支和任意根式方程。
- 缺少结构化 `EquationConstraint` 的自然语言几何条件。
- 多解但缺乏正性、顺序或区间证据的系统。

仓库 `requirements.txt` 声明了 SymPy，但当前运行环境未安装；本轮没有临时安装依赖，而是实现了完全精确、无外部依赖的保守核心。将来若引入 SymPy，应仍保留当前的唯一性、回代和 provenance 门槛。

## 下一步高收益接入点

1. 将垂直、共线、中点、点在曲线、面积比例转成 scoped equations。
2. 为焦点、顶点、轴长、圆心关联补齐参数方程，而不是直接赋值。
3. 对剩余 71 条“序列完整但未消元”按缺失 constraint 模板聚类。
4. 给消元器增加顺序约束检查和解后对全部原方程的显式回代报告。

验证：80 条 unittest 全部通过，源码、脚本和测试通过 `compileall`。