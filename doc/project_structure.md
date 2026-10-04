# 当前实现地图

更新：2026-10-03。开发前先读本文，再按任务阅读[关键接口](api_reference.md)、[开发记录](../dev_record.md)及[开发规格](../docs/开发规格/README.md)。本文记录当前代码事实，规格中的设计不自动视为已实现。

## 目标与当前阶段

以题目状态和推理模型的状态转换完成圆锥曲线求解：双层状态 → 模型选择与对象绑定 → 模型应用／公共符号操作 → 新状态 → 答案。

- **已有基础**：旧状态构造、定理库、选择器训练、推理／搜索、符号求解与评估模块均有代码；不代表全库数学正确性或端到端质量已验证。
- **独立验证**：新绑定接口已跑通 ID 2 的 RM5→RM21（m=5）及 ID 9 的 RM3→RM11→RM5→RM12（t=9）；另已验证 ID 65/200/353/380/549 的正向渐近线链；ID 1516 仅验证椭圆参数子链；ID 5 的标准模型→RM17 及标准模型→RM29→RM52→RM2 均得到 5/4；ID 3723 原始查询经 RM9→RM29→RM52 得到 65/16；ID 946/1793 经同链及焦点坐标实例化得到 1/8、1/4；ID 7260 原始查询经 RM7→RM72→RM52 得到 2√5/5；均为固定链与模式预检，不是自主选择模型。
- **尚未接入**：新状态与旧状态没有自动双向同步；新应用器尚未接入旧求解器、轨迹构建器和选择器。ID 51 仍为数学／规格案例；ID 56 已支持结构化输入和 RM78 参数化子步骤，后续求参链未接入。
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
| [named_line_facts.py](../src/state/named_line_facts.py) | 命名直线输入：规范 LineOf 身份，保存无序交点集合、斜率和及分母要求，供后续参数化与斜率推理使用 |
| [transition_state.py](../src/state/transition_state.py) | 题目状态与事实定义：解析已给信息，保存对象、方程、关系、模型结果及来源；表示查询目标并读取已提交答案 |
| [transition_primitives.py](../src/solver/transition_primitives.py) | 受限解析、椭圆／双曲线标准形式、共焦点实例化、斜率、实根与条件检查 |
| [standard_proposals.py](../src/theorems/standard_proposals.py) | 标准椭圆／双曲线参数提案：从绑定方程提取半轴平方、轴向及类型条件，供 RM3–6 使用 |
| [parabola_operations.py](../src/solver/parabola_operations.py) | 抛物线公共计算：提取标准式系数、将数值点代入方程、由系数和方向计算 p 与焦点 |
| [parabola_proposals.py](../src/theorems/parabola_proposals.py) | 抛物线模型提案：组织参数提取／点恢复、焦点坐标实例化、焦半径、准线及定义路径，供 RM2/7–10/17/29 使用 |
| [distance_operations.py](../src/solver/distance_operations.py) | 一般点到直线精确距离；RM52 调用，数值输入边界与定义路径由 `tests/test_bound_parabola_definition.py` 验证 |
| [distance_proposals.py](../src/theorems/distance_proposals.py) | RM52 共用命名点／焦点属性到直线的距离提案；`test_bound_line_distance.py` 覆盖解析、查询隔离及真实事实子案例 |
| [line_proposals.py](../src/theorems/line_proposals.py) | 直线参数恢复提案：利用已知点与直线方程的一致性求一个参数，并提出斜率／截距结果，供 RM72 使用 |
| [eccentricity_proposals.py](../src/theorems/eccentricity_proposals.py) | 离心率计算提案：核验已有 a²、b²、c² 后计算 e，向 RM13 返回待提交属性与来源 |
| [intersection_operations.py](../src/solver/intersection_operations.py) | 交点相关公共计算：将直线代入标准抛物线，支持过点未知直线族及水平分支检查，计算数值二次根关系／实根数，并由根关系及坐标映射计算弦长；不生成命名交点 |
| [intersection_proposals.py](../src/theorems/intersection_proposals.py) | RM78/42/43/50 提案：绑定消元事实，组织数值消元、命名直线参数化、根关系及弦长计算，包装结果与来源供应用器提交 |
| [tangent_proposals.py](../src/theorems/tangent_proposals.py) | 抛物线切线提案：验证给定点在曲线上，计算四方向切线方程并返回待提交结果，供 RM39 使用 |
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

1. RM4/RM6 与 y 轴框架、渐近线及参数关系已验证，见[本批记录](../docs/开发规格/10_Y轴标准模型实现记录.md)。ID 5 已完成标准参数恢复与焦半径闭环，见[记录](../docs/开发规格/11_ID5抛物线实现记录.md)。定义路径已完成，见[记录](../docs/开发规格/12_ID5定义路径实现记录.md)。RM52 已支持独立直线绑定／距离查询；ID 5882/1253 仅验证显式事实子案例，见[记录](../docs/开发规格/13_一般直线距离实现记录.md)。ID 3723 已完成原始查询闭环，见[记录](../docs/开发规格/14_ID3723准线别名实现记录.md)。ID 946/1793 焦点别名坐标实例化已验证，见[记录](../docs/开发规格/15_焦点别名坐标实现记录.md)。ID 7260 已完成[职责设计](../docs/开发规格/16_ID7260交点与参数恢复设计.md)，D5 已确认，交点事实及 RM7／RM72 参数子链已验证，见[记录](../docs/开发规格/17_ID7260参数子链实现记录.md)；Focus(G) 距离原始查询现已接通，见[记录](../docs/开发规格/18_ID7260焦点距离闭环.md)；全库选型已完成，下一批为 RM13 正向离心率与 ID 5988/7488/1586/4528，见[选型规格](../docs/开发规格/19_模型覆盖审计与下一组选型.md)；四题 RM13 原始查询已验证，见[实现记录](../docs/开发规格/20_RM13正向离心率实现记录.md)。RM39 切点验证、派生切线及 ID 2106 原始查询已验证，见[记录](../docs/开发规格/21_RM39抛物线切线实现记录.md)。ID 6347 的[消元与根关联契约](../docs/开发规格/22_ID6347消元与根关联契约.md)及 RM78 数值消元子步骤已完成；RM42/43 实根资格与 RM50 弦长查询现已完成，ID 6347 原题得到 8，见[闭环记录](../docs/开发规格/23_ID6347根关系与弦长闭环.md)；ID 56 的[参数化契约与结构化输入](../docs/开发规格/24_ID56命名直线与参数化契约.md)已完成；RM78 方向检查、局部参数与根对关联已完成，见[记录](../docs/开发规格/25_ID56参数化与命名根关联实现.md)；下一批扩展符号 RM42/43，再接 RM55；暂不扩展离心率范围或反向模式。
2. 分批覆盖全部 80 个模型，抽提公共运算；同时形成可回放轨迹，处理弱标注顺序问题。
3. 统一状态初始化、轨迹构建与求解入口，再开展选择器训练和系统评估；Entropy、LLM 工作另行安排。
4. 历次详细案例与验证见[开发记录](../dev_record.md)及[规格导航](../docs/开发规格/README.md)。

每次只更新受影响的模块行、接入状态和后续步骤；接口细节放 API 文档，变更经过放开发记录，避免重复维护三份功能清单。
