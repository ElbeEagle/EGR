# 当前实现地图

更新：2026-09-24。开发前先读本文，再按任务阅读[关键接口](api_reference.md)、[开发记录](../dev_record.md)及[开发规格](../docs/开发规格/README.md)。本文记录当前代码事实，规格中的设计不自动视为已实现。

## 目标与当前阶段

以题目状态和推理模型的状态转换完成圆锥曲线求解：双层状态 → 模型选择与对象绑定 → 模型应用／公共符号操作 → 新状态 → 答案。

- **已有基础**：旧状态构造、定理库、选择器训练、推理／搜索、符号求解与评估模块均有代码；不代表全库数学正确性或端到端质量已验证。
- **独立验证**：新绑定接口已跑通 ID 2 的 RM5→RM21（m=5）及 ID 9 的 RM3→RM11→RM5→RM12（t=9）；另已验证 ID 65/200/353 的正向渐近线链；均为固定动作顺序，不是自主选择模型。
- **尚未接入**：新状态与旧状态没有自动双向同步；新应用器尚未接入旧求解器、轨迹构建器和选择器。其余三个代表案例目前是数学／规格案例。
- **当前方向**：分批完善 80 个模型的执行契约、共享操作与可信轨迹，再训练选择器。Entropy／求解进度机制和 LLM 实验后置。

## 代码导航

下列路径均相对仓库根目录；“旧流程”表示迁移前基础，不表示应删除。

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

| 文件 | 主要职责 |
| --- | --- |
| [transition_state.py](../src/state/transition_state.py) | 显式初态、对象所属方程、共焦点关系、几何框架、约束、属性、赋值与来源 |
| [transition_primitives.py](../src/solver/transition_primitives.py) | 受限解析、椭圆／双曲线标准形式、共焦点实例化、斜率、实根与条件检查 |
| [parameter_proposals.py](../src/theorems/parameter_proposals.py) | RM11/RM12 共用的普通参数关系提案及正值／一致性检查 |
| [bound_application.py](../src/theorems/bound_application.py) | 动作绑定、候选变化、冲突检查、原子提交、受限回代及执行记录 |
| `model_003.py`、`model_011.py`、`model_012.py`（`src/theorems/models/`） | 椭圆参数、普通参数关系及共焦点约束；RM11/RM12 共用 `parameter_proposals.py` |
| [model_005.py](../src/theorems/models/model_005.py)、[model_021.py](../src/theorems/models/model_021.py) | 原模型类新增 `propose_bound`；RM5 记录类型条件；RM21 支持渐近线正／反向模式，旧接口保留 |
| [bound_slice.py](../src/reasoning/bound_slice.py) | 三条固定链、指定动作回放与 v3 诊断 trace 输出 |
| [test_bound_transition_slice.py](../tests/test_bound_transition_slice.py) | 真实题、绑定隔离、重复执行、多解、条件不足、冲突与回滚测试 |

新增测试：[test_bound_parameter_modes.py](../tests/test_bound_parameter_modes.py) 覆盖普通参数关系和正向渐近线；[test_bound_shared_focus.py](../tests/test_bound_shared_focus.py)，覆盖 ID 9 及多曲线关系边界。

运行：`python3 -m src.reasoning.bound_slice --problem-id 2`。
详细结果及限制见[实现记录](../docs/开发规格/07_RM5_RM21实现记录.md)；诊断 trace 尚不是最终训练 schema。ID 9 的命令、证据及限制见[共焦点实现记录](../docs/开发规格/08_ID9共焦点实现记录.md)。

## 数据与设计依据

- `model/conic_model_ids.json`、`conic_model_descriptions.md`：80 个高层模型的 ID、名称与数学定义。`object.json`、`operators.json` 是表达语言词汇，不是已实现的运算库。
- `data/train_with_models_v3.json`：当前案例来源，按记录 `id` 定位。Opus 辅助标注的 `models` 仅作弱参考，不直接视为可执行顺序。
- [开发规格](../docs/开发规格/README.md)：已确认职责、真实案例、全库简表与运行证据；开发新模型前阅读相关条目。
- `paper/`、`docs/项目理解/`：研究目标与路线背景；不能用历史规划替代当前实现状态。
- `doc/module*.md` 等旧文档保留为历史参考，涉及现状时核对代码及本文。

## 后续顺序与维护

1. RM21 正向及 RM11/RM12 普通参数模式已验证，见[本批记录](../docs/开发规格/09_参数关系与渐近线正向实现记录.md)。下一批建议扩展 y 轴标准曲线 RM4/RM6，复用现有参数关系与渐近线契约。
2. 分批覆盖全部 80 个模型，抽提公共运算；同时形成可回放轨迹，处理弱标注顺序问题。
3. 统一状态初始化、轨迹构建与求解入口，再开展选择器训练和系统评估；Entropy、LLM 工作另行安排。

每次只更新受影响的模块行、接入状态和后续步骤；接口细节放 API 文档，变更经过放开发记录，避免重复维护三份功能清单。
