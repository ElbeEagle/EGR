

---

## 2026.01.10上午

工作1:将数据集train.json提取出process项
> 存储定位："data/train_process.txt"

工作2:从process项中，已初步总结出常见的定理、操作
> 存储定位："model/model.md"

**下一步**：需确定最终要选取的定理和操作，一起设定为模型库，建立模型库id的json文件
**后续还需的工作**：再建立模型库的json文件，构建好每个模型的id, input, output, constraints(匹配条件)

## 2026.01.10下午

确定最终的定理、操作，建立模型库id的json文件。
> 存储定位："model/conic_model_ids.json"

**已确定80个模型，覆盖90%的题目**
```
一、曲线定义模型（ID: 0-2）
二、标准方程模型（ID: 3-10）
三、参数关系与离心率（ID: 11-15）
四、焦半径与通径（ID: 16-20）
五、渐近线相关（ID: 21-24）
六、第二定义与准线（ID: 25-29）
七、焦点三角形（ID: 30-32）
八、抛物线焦点弦（ID: 33-36）
九、参数方程与切线（ID: 37-40）
十、韦达定理系列（ID: 41-43）
十一、点差法（ID: 44-46）
十二、三角形定理（ID: 47-49）
十三、弦长公式（ID: 50-51）
十四、距离与坐标（ID: 52-55）
十五、三角形面积（ID: 56-58）
十六、向量运算（ID: 59-62）
十七、不等式（ID: 63-64）
十八、判别式（ID: 65-67）
十九、三角形特殊定理（ID: 68-71）
二十、直线方程（ID: 72-74）
二十一、圆相关（ID: 75-76）
二十二、高级技巧（ID: 77-79）
```
**下一步**：将process转换为模型的序列组合。

## 2026.01.10晚上

工作1：将 train_process.txt 拆分为10份 (par1~part10)
> 存储定位："data/data_process/train_process_part_1.txt"，共10个文件。

工作2：调用LLM仔细分析每一个process的推理过程，将它们转换为模型序列。
> 存储定位："data/data_process/process_models_part_1.json"，共10个文件。

eg:
```json
"2": "双曲线\frac{x^{2}}{4}-\frac{y^{2}}{m2}=1(m>0)的渐近线方程为y=\pm\frac{m}{2}x直线5x-2y=0的方程可化为y=\frac{5}{2}x,所以,m=5."
```
转换为：
```json
"2": [5, 7, 9, 21],
```

**下一步**：
* 将10个转换后的 模型序列组合 文件，进行合并，并与原数据集进行整合。
* 同时还需检验 转换后的 模型序列组合 文件，是否正确。（待考虑）

---

## 2026.01.11下午

工作1: 修正 "process_models_part_1.json" 部分的潜在问题。

工作2: 将10个 "process_models_part_x" 合并到 "train.json" 中，形成 "train_with_models.json"。
> 存储定位："data/train_with_models.json"，共10个文件。




## 2026.01.11晚上

验证定理序列提取是否准确：

将相关文件 "conic_model_ids.json" "train_with_models.json" "train.json" 经由 "sample_problems.py" 抽样得到 "sampled_problems.md"。

再交由LLM分析得到"verification_report.md"。

> 存储定位："scripts/process_to_model/sample_problems.py"

> 存储定位："data/sampled_problems.md" "data/verification_report.md"

发现有~80%正确率，部分术语如各个双曲线、平行垂直有一点混淆，有时会漏抓取一点步骤。

---

## 2026.01.12晚上

通过关键字检索（圆锥曲线名称，关键信息），发现有680个样本有明显错误（双曲线认错、序列为空）

> 存储定位："scripts/process_to_model/analyze_alignment.py"
> 存储定位："data/verify_doc/analysis_report.md" "data/verify_doc/analysis_results.json"

此外抽样了500个样本由LLM进行细致分析，有些小问题

> 存储定位："data/verify_doc/sampled_problems.md"
> 存储定位："data/verify_doc/detailed_sequence_analysis.md"


## 2026.01.12晚上

工作1:将680个有明显错误的样本，提取出"text"和"process"，形成一个json文件，让LLM来重新分析process对应的models，避免之前的错误。
> 存储定位："data/data_process/train_process_error.json"

工作2:让LLM来重新分析process对应的models，针对之前出现的问题，这次特别注意了：
* 切线/判别式模型：正确添加了模型 76（圆切线条件）、65-67（判别式相关）
* 离心率模型：确保包含模型 13（离心率公式）和 77（齐次化求离心率）
* 曲线类型识别：准确区分双曲线（模型5、6、12、21等）、椭圆（模型3、4、11等）、抛物线（模型7-10、2等）
> 存储定位："data/data_process/process_models_error.json"


**下一步**：
* 再次检验这680个样本还是否有明显的错误（双曲线认错、序列为空），仍然可以仅通过关键字检索（圆锥曲线名称，关键信息）进行检验。
* 同时可能还需要再调用llm，抽样分析一下对这680个样本重新生成的models，是否会存在模型过度（冗余）的情况。

---

## 2026.01.13下午

工作1:将这680个样本替换回"train_with_models"，生成新的json文件。
> 存储定位："data/train_with_models_v2.json"

工作2:初步分析问题状态state的建模方案

---

## 2026.01.15上午

工作1:拟定了"定模型库构建"和"题目状态构建"的方案。
> 存储定位："doc/module0_model_library.md", "doc/module1_state_construct.md"

工作2:梳理了"项目整体流程框架"，及"思路+创新点"
> 存储定位："doc/project_workflow.md", "doc/创新点+论文思路.md"


## 2026.01.15下午

工作1:实现了状态模块的核心数据结构 ("SymbolicState", "AbstractState")。
> 存储定位："src/state/symbolic_state.py", "src/state/abstract_state.py"

工作2:实现了状态构造器StateConstructor，负责构建和更新双层状态表示
> 存储定位："src/state/state_constructor.py"

工作3:实现了"定理模型库"基类，实现了两个模型(Model 5-双曲线标准方程参数提取, Model 21-双曲线渐近线)
> 存储定位："src/theorems/base_model.py", "src/theorems/models/model_005.py", "src/theorems/models/model_021.py"

其他相关代码文件：
> 状态验证-"scripts/verify_state_construction.py", 
> 模型测试-"scripts/test_models.py"

**下一步**：
* 继续实现高频模型 
    * Model 3 - 椭圆标准方程
    * Model 11-13 - 参数关系+离心率
    * Model 7, 9 - 抛物线标准方程

---

## 2026.01.16

工作1: 实现了6个模型(Model 3,7,9,11,12,13)


---

## 2026.01.17下午
> 开发日志："dev_logs/stage2_models_batch6_report.md"

工作1: 到目前总共实现了30个模型: [0-13, 16, 17, 19, 21, 22, 24, 29, 41-43, 47, 53, 56, 62, 63, 75];
> 存储定位："src/theorems/models/model_xxx.py"

**下一步**：
* 增强方程解析（支持非标准形式）
* 优化前置条件（提高适用性）
* 修复已知问题（样本6, 16等）
* 目标：成功率突破60%

---

2026.01.18上午
> 开发日志："dev_logs/stage2.1_optimization_report.md"

工作1: 状态构造器增强，自动参数提取，自动应用标准方程模型 (3-10)。
> 存储定位："src/state/state_constructor.py" (_extract_equation_parameters)

工作2: 实现方程标准化（EquationNormalizer）
   - 支持 `y = x²/4` → `x² = 4y`
   - 支持 `x²/3 - y² = 1` → `x²/3 - y²/1 = 1`
   - 支持 `4x² + 9y² = 36` → `x²/9 + y²/4 = 1`
> 存储定位："src/state/equation_normalizer.py"


2026.01.18下午
> 开发日志："dev_logs/stage2.2_expansion_optimization.md"

工作1: 实现了10个高频模型: [54, 32, 57, 78, 14, 61, 46, 65, 79, 70]。到目前总共实现了40个模型。


工作2: 优化一些模型的前置条件，适应不同题目的形式，提高匹配成功率 (Model 13, 62, 63, 32, 24; Model 0, 3, 11, 9, 56, 61)

**下一步**：
* Module 3 - 训练数据构造器 / 神经网络训练

---

2026.01.19下午
> 开发日志："dev_logs/stage2.3_integration_report.md"

工作1: 核心功能实现-StateSequenceBuilder: 标准化状态序列构建器
> 存储定位："src/state/state_sequence_builder.py"

工作2: 系统化测试框架，测试了63个样本（数据集中有模型序列的全部样本），211个推理步骤全部执行，135个成功的状态转换。
> 存储定位："tests/integration_test.py", "outputs/integration_test_results.json"

**下一步**：
* 进入Module 3 - 训练数据构造器


---

2026.01.20
> 开发日志："dev_logs/module3_training_completion.md"

工作1: 核心功能实现 - 最大熵模型选择器（P(model|state) 分类器）
> 存储定位："src/selector/model_selector.py", "src/selector/trainer.py"

工作2: 构建了分类器的训练和测试的框架
> 存储定位："scripts/selector/train.py", "scripts/selector/test.py"

相关说明文档：
> "src/selector/README.md", "src/selector/USAGE.md"

**下一步**：
* 训练分类器并测试
* 准备Module 4 - 推理引擎


---

2026.02.10
> 开发日志："dev_logs/module4_stage1_completion.md"

工作1: 实现Module 4 阶段1 - 基础推理引擎
核心组件（~800行代码）:
✅ ReasoningResult - 推理结果数据结构
✅ ModelSelector - 模型选择器（Top-1 & Top-K策略）
✅ ReasoningEngine - 主推理引擎

> 存储定位：
```
src/reasoning/
├── __init__.py
├── reasoning_result.py
├── model_selector.py
└── reasoning_engine.py

scripts/reasoning/
└── test_reasoning_engine.py

dev_logs/
└── module4_stage1_completion.md (详细报告)
```

**下一步**：
* 修复初始完整度过高问题 - 某些问题初始就是1.0（StateConstructor自动应用了模型）
* 解答提取未实现 - 当前只是placeholder
* 模型应用失败 - 部分模型apply失败需要调试

---

2026.02.10
> 开发日志："dev_logs/module4_stage1_fixes.md"

工作1: 修复推理引擎3个关键问题
- ✅ 问题1: 初始完整度过高 → 提高阈值0.99 + 最小步数min_steps=1 + 基于applied_count判断
- ✅ 问题2: 解答提取未实现 → 实现QueryParser + AnswerExtractor（支持8种查询类型）
- ✅ 问题3: 模型apply失败 → 统一返回bool + 批量修复全部40个模型 + 排除已应用模型
> 新增文件："src/reasoning/query_parser.py", "src/reasoning/answer_extractor.py"

工作2: 修复推理引擎额外发现的问题
- ✅ 模型重复选择（死循环） → ModelSelector自动排除已应用模型
- ✅ completeness判断缺失LENGTH等类型 → 补全8种query_type的相关信息判断
- ✅ StateConstructor缺少update_abstract_state方法 → 新增便利方法
> 修改文件："src/reasoning/model_selector.py", "src/state/state_constructor.py"

工作3: 批量修复40个模型文件
- ✅ 全部40个模型的apply方法返回bool + try-except异常处理
> 工具脚本："scripts/utils/safe_fix_models.py"

测试结果：3/3 (100%)
- 双曲线渐近线 ✓ 答案: (y = pm*(1/sqrt(3))*x)
- 椭圆离心率 ✓ 答案: sqrt(2^2 - 1^2)/2
- 椭圆长轴长 ✓ 答案: 4

**下一步**：
* Module 4 阶段2：回溯机制、Conic10K批量测试、性能评估
* 在更多样本上验证成功率（目标40-60%）

---

2026.02.10（续）
> 开发日志："dev_logs/module4_stage2_batch_test.md"

工作1: 实现回溯机制
- ✅ apply失败时自动重试（最多3次/步），排除失败模型后选下一个候选
- ✅ 连续2步无法推进时提前终止
> 修改文件："src/reasoning/reasoning_engine.py"

工作2: 实现答案比较器
- ✅ 数值化eval（支持sqrt、分数、pm等），误差<1e-4视为正确
> 新增文件："src/reasoning/answer_comparator.py"

工作3: 批量测试 (200样本)
> 新增文件："scripts/reasoning/batch_test.py"
> 输出报告："outputs/reasoning/batch_test_report.json"

工作4: 尽力提取答案策略
- ✅ 即使completeness未达标，只要应用了模型就尝试提取答案
- ✅ 增强_evaluate_expression支持复合表达式（如 sqrt(2^2 - 1^2)）
- ✅ 改进completeness计算对LENGTH等查询类型的支持

**批量测试结果 (200样本)**:
```
推理成功率: 73.5% (147/200)
答案正确率: 2.5% (5/200)
平均推理步数: 8.2
速度: 965题/秒

按曲线类型:
  Ellipse:   69.0% 成功
  Hyperbola: 79.2% 成功
  Parabola:  82.1% 成功

答案错误分析 (142个成功但答案错):
  symbolic:          92 (参数含变量字母，无法数值化)
  numeric_mismatch:  35 (数值可算但推理路径错误)
  not_found:         15 (提取器无法定位答案)
```

**下一步**：
* 答案正确率提升：改进答案提取+符号计算
* 更多模型实现（当前40/80）→ 提升覆盖率
* 阶段3：三层熵架构

---

2026.02.10（续2）

工作1: 扩充模型库 40→52
- ✅ 实现12个高频缺失模型: [33,44,49,51,52,55,59,66,68,72,76,77]
- 涵盖: 直线方程、点到直线距离、勾股定理、弦长公式、点差法、斜率、向量点积、判别式、中线定理、圆相切、齐次化
> 新增文件: src/theorems/models/model_{033,044,049,051,052,055,059,066,068,072,076,077}.py

工作2: 三层熵架构实现
- ✅ EntropyEstimator: 启发式H(S)估计（基于completeness、参数、深度、特征覆盖度）
- ✅ InfoGain计算: H(S_current) - H(S_next)
- ✅ 综合评分策略: score = λ₁·P(Y|X) + λ₂·InfoGain - λ₃·H(Y|X)
- ✅ ModelSelector新增 'three_layer_entropy' 策略
> 新增文件: src/reasoning/entropy_estimator.py

工作3: 重新训练模型选择器 (v2)
- ✅ 全量训练数据生成: 5359样本 → 12460个训练样本（之前135个，增长92x）
- ✅ 训练完成: Top-1=57.1%, Top-3=78.8%, Top-5=86.0%
> 新增文件: data/train_state_model_v2.json, checkpoints/model_selector_v2.pth

**v2批量测试结果 (200样本)**:
```
推理成功率: 78.5% (157/200)  ← v1: 73.5%
答案正确率: 2.5% (5/200)
Equation成功率: 67.4%  ← v1: 55.8%
Value成功率: 93.0%  ← v1: 90.1%
```

**下一步**：
* 答案正确率提升（核心瓶颈：符号参数无法数值化）
* 三层熵策略性能优化（deepcopy开销大）
* 实现剩余28个模型

---


## 2026-09-23｜RM5→RM21 绑定执行小闭环

- **变更**：ID 2 固定执行 RM5→RM21，求得 m=5；加入对象／方程绑定、前提与实根筛选、事务提交、来源记录和受限回代。重复动作不新增状态，失败／多解不误提交。
- **新增文件**：`src/state/transition_state.py`、`src/solver/transition_primitives.py`、`src/theorems/bound_application.py`、`src/reasoning/bound_slice.py`、`tests/test_bound_transition_slice.py`。
- **更新文件**：`src/theorems/base_model.py`、`src/theorems/models/model_005.py`、`model_021.py`；同步开发规格，并保存诊断 trace。
- **验证**：当批记录为 79 passed（25 项新测试及 54 项相关回归）；命令、证据和范围见[实现记录](docs/开发规格/07_RM5_RM21实现记录.md)。不作为全系统准确率。
- **限制／下一步**：尚未接入旧求解器、轨迹构建器和选择器；RM21 新接口仅实现反向模式。建议下一批以 ID 9 检验多曲线关系，再分批扩展模型和轨迹。
- **释义补充（2026-10-03）**：`TransitionState` 保存题目与推理状态；`BoundAction` 指定模型及作用对象；`Proposal` 保存待提交变化；`BoundApplicator.apply` 校验并写入状态；`TransitionResult` 保存执行结果。`bound_slice.py` 组织固定动作回放，`transition_primitives.py` 提供解析／条件检查／实根筛选等计算。


## 2026-09-24｜整理开发导航与维护约定

- **变更**：重写 [实现地图](doc/project_structure.md) 与 [关键接口](doc/api_reference.md)，区分前期原型、新绑定切片和后续计划；新增根目录 [AGENTS.md](AGENTS.md)，约定开发前回顾及开发后同步维护。旧开发记录原样保留，历史指标不作为当前结果。
- **范围**：仅上述三份文档及本日志，不修改运行时代码、数据或模型定义。
- **验证**：关键签名已对照代码；本地链接、API 最小示例、旧日志前缀保留检查及 `git diff --check` 通过。`python3 -m pytest -q tests/test_bound_transition_slice.py`：25 passed。
- **下一步**：按实现地图分批扩展；每批只更新受影响条目，避免重复维护完整功能清单。

## 2026-09-24｜ID 9 多曲线共焦点绑定执行

- **变更**：复用绑定／事务机制，新增共焦点关系与曲线框架、可追溯的类型条件；RM3→RM11→RM5→RM12 求得 t=9。关系实例化作为公共操作，由 RM12 显式调用。
- **文件**：更新 `src/state/transition_state.py`、`src/solver/transition_primitives.py`、`src/theorems/bound_application.py`、`models/model_003/005/011/012.py`（位于 `src/theorems/`）、`src/reasoning/bound_slice.py`；新增 `tests/test_bound_shared_focus.py`，调整旧绑定测试；同步 API、实现地图及规格，保存 v2 trace。
- **验证**：两条绑定链与相关旧接口回归合计 113 passed。命令、证据和范围见[ID 9 实现记录](docs/开发规格/08_ID9共焦点实现记录.md)。
- **限制／下一步**：仅原点中心、x 轴的标准椭圆—双曲线共焦点固定链，未接入旧求解器／选择器。下一批建议补 RM21 正向和 RM11/RM12 普通参数关系模式；再按案例扩展。
- **释义补充（2026-10-03）**：`FocusEquality` 记录两曲线共焦点关系，`CurveFrame` 记录所属方程的中心／轴向；`instantiate_shared_focus` 核验框架相容，将另一曲线已有 c² 用于目标曲线，并返回来源操作。关系记录自身不计算参数。


## 2026-09-24｜RM21 正向及 RM11/RM12 普通参数模式

- **变更**：RM11/RM12 共用参数提案，支持任意两个平方参数求第三个及三项表达式约束求标量；RM21 正向生成两条渐近线。应用器支持派生方程的原子提交与受限回代，查询读取完整方程对。
- **文件**：新增 `src/theorems/parameter_proposals.py`、`tests/test_bound_parameter_modes.py`；更新状态、应用器、RM11/12/21、固定链入口及接口／实现地图／开发规格，保存 ID 65 v3 trace。
- **验证**：本批 32 项测试；相关回归共 145 passed。真实题 ID 65、200、353 正向链通过，ID 2、ID 9 原链保持通过。命令及完整边界见[实现记录](docs/开发规格/09_参数关系与渐近线正向实现记录.md)。
- **限制／下一步**：参数模式消费已有平方参数事实，未扩展全部文本解析；渐近线正向仍限原点中心、x 轴。下一批建议补 y 轴 RM4/RM6；仍不接入选择器训练。
- **释义补充（2026-10-03）**：`parameter_proposals.py` 的 `parameter_proposal` 利用平方参数恒等式补全参数或求标量，返回更新提案；应用器负责提交。渐近线查询读取已生成的两条方程。


## 2026-09-24｜RM4/RM6 与 y 轴框架、渐近线

- **变更**：RM3–6 抽提共享标准参数提案；新增 RM4/RM6 绑定模式。框架、RM11/RM12 和 RM21 正反向支持 x/y 轴；固定链预检标准方向。修复动作枚举覆盖 `mode` 过滤参数的问题。
- **文件**：新增 `src/theorems/standard_proposals.py`、`tests/test_bound_y_axis.py`；更新公共运算、应用器、参数提案、RM3/4/5/6/21、固定链入口及文档；保存 ID 380 trace。
- **验证**：相关回归 173 passed，其中本批 28 项。ID 380/549 渐近线整链通过；ID 1516 仅参数子链通过，不计整题求解。详见[本批记录](docs/开发规格/10_Y轴标准模型实现记录.md)。
- **限制／下一步**：仍限原点中心、坐标轴对齐；未接入选择器。下一批建议明确 ID 5 抛物线及点归属参数恢复的执行模式后开发。
- **释义补充（2026-10-03）**：`standard_proposals.py` 的 `standard_proposal` 从绑定的椭圆／双曲线方程提取半轴平方、轴向和类型条件，供 RM3–6 共用；返回提案而非直接修改状态。


## 2026-09-27｜ID 5 抛物线参数恢复与焦半径

- **变更**：明确标准模型恢复参数／确认方向／输出焦点、RM17 计算焦半径、查询只读的边界。ID 5 固定 RM9→RM17 得到 5/4；四方向共用实现，不按方向假设过滤参数根。
- **文件**：新增 `src/solver/parabola_operations.py`、`src/theorems/parabola_proposals.py`、`tests/test_bound_parabola.py`；更新状态、绑定、RM7–10/17 和固定链入口；同步文档并保存 ID 5 v4 trace。
- **验证**：相关回归 204 passed，其中本批 31 项；覆盖真实题、四方向、条件不足、多解、冲突回滚及旧接口。测试辅助函数曾误用 pytest 的 setup 名称，重命名后消除启动错误。详见[实现记录](docs/开发规格/11_ID5抛物线实现记录.md)。
- **限制／下一步**：仅原点顶点、数值坐标点、一元系数恢复；未扩展准线或通用距离，也未接入选择器。下一批建议补 RM29 准线及点到直线距离，验证定义路径。
- **释义补充（2026-10-03）**：`parabola_operations.py` 提供标准系数提取、点代入残差及 p／焦点计算；`parabola_proposals.py` 的 `standard_parabola_proposal` 组织参数提取／点恢复，`focal_radius_proposal` 组织 RM17 焦半径计算。`PointCoordinates` 保存坐标，`PointOnCurve` 保存归属，`FocalDistanceQuery` 表示求点到焦点的距离。


## 2026-09-27｜ID 5 准线定义路径与公共距离操作

- **变更**：增加 RM29 准线、RM52 点到准线距离和 RM2 定义转换；复用并抽提抛物线标准属性校验，保留原 RM17 路径。ID 5 新固定链 RM9→RM29→RM52→RM2 得到 5/4。
- **文件**：新增 `src/solver/distance_operations.py`、`tests/test_bound_parabola_definition.py`；更新抛物线提案、绑定应用器、RM2/29/52、回放入口及 API／实现地图／规格，保存独立 v4 trace。
- **验证**：新增 23 项测试，相关回归 227 passed；真实 CLI 回放成功。详见[实现记录](docs/开发规格/12_ID5定义路径实现记录.md)。
- **限制／下一步**：公共距离支持一般数值直线，绑定入口暂限抛物线准线；下一批建议扩展真实一般直线案例和距离查询。未接入选择器／旧求解器。
- **释义补充（2026-10-03）**：`distance_operations.py` 的 `point_to_line_distance` 由数值点和直线方程计算精确距离；`directrix_proposal` 提出准线方程，`definition_proposal` 核验点及准线后，将既有准线距离作为焦半径提出。


## 2026-09-27｜RM52 独立直线绑定与距离查询

- **变更**：解析独立 Line 与点到直线查询；BoundAction 增加 line，RM52 复用通用距离提案，保留准线兼容；新增单步回放，trace 升为 v5。
- **文件**：新增 distance_proposals.py、test_bound_line_distance.py；更新 transition_state.py、bound_application.py、parabola_proposals.py、model_052.py、bound_slice.py 及接口／实现地图／规格和诊断轨迹。
- **验证**：新增 24 项，相关回归 251 passed；ID 5882/1253 显式事实投影距离为 4／10，仅诊断，不计原题求解。详见[实现记录](docs/开发规格/13_一般直线距离实现记录.md)。
- **限制／下一步**：仍限数值点到显式直线距离；建议下一批通过 ID 3723 衔接准线别名与 RM29 输出，继续暂缓选择器训练。
- **释义补充（2026-10-03）**：`distance_proposals.py` 的 `point_line_distance_proposal` 读取绑定点／线并调用公共距离计算，返回距离属性提案；`PointLineDistanceQuery` 记录要求哪个点到哪条直线的距离，不执行计算。


## 2026-09-29｜ID 3723 准线别名原题闭环

- **变更**：增加 DirectrixAlias 与共用身份解析；RM52 绑定并记录别名事实和 RM29 准线输出，查询只读。原题 RM9→RM29→RM52 得到 65/16，不改写输入或复制方程。
- **文件**：更新 transition_state.py、bound_application.py、distance_proposals.py、bound_slice.py；新增 test_bound_directrix_alias.py，同步 API／实现地图／规格及 ID 3723 v5 轨迹。
- **验证**：新增 16 项，相关回归 267 passed；原始 CLI 回放成功，见[实现记录](docs/开发规格/14_ID3723准线别名实现记录.md)。
- **限制／下一步**：多重别名和别名附加独立方程暂不合并；下一批建议明确焦点别名坐标实例化（ID 946／1793），继续复用距离链。
- **释义补充（2026-10-03）**：`DirectrixAlias` 保存“G 的准线就是 l”的身份关系；`line_bindings` 查找 l 对应的已有准线方程，供 RM52 使用，不重新计算准线。


## 2026-09-29｜ID 946／1793 焦点别名坐标实例化

- **变更**：FocusAlias 初态只记录身份；RM7–10 同步提出命名焦点坐标，应用器原子提交并记录来源。原准线固定链按提交后的坐标绑定 RM52，两道原题分别得到 1/8、1/4。
- **文件**：更新 transition_state.py、parabola_proposals.py、bound_application.py、bound_slice.py；新增 test_bound_focus_alias.py，维护接口／实现地图／规格，保存两份 v6 轨迹。
- **验证**：新增 15 项，相关回归 282 passed；已有坐标冲突整步回滚，来源与重复执行验证通过。详见[实现记录](docs/开发规格/15_焦点别名坐标实现记录.md)。
- **限制／下一步**：限抛物线有限实数焦点坐标，同一点多别名暂不合并；建议下一批先明确 ID 7260 的交点参数恢复职责。
- **释义补充（2026-10-03）**：`FocusAlias` 保存“G 的焦点就是 F”的身份关系；标准抛物线提案依据已计算的焦点位置提出 F 的 `PointCoordinates`，应用器检查一致性后提交。


## 2026-10-02｜ID 7260 交点事实与参数恢复职责设计

- **结论**：交点坐标是给定事实；抛物线恢复复用 RM7，直线恢复推荐 D5：RM72 点斜式一致性的受限反向模式，不将任意代入归为 RM78。D5 尚待确认。
- **文件**：新增 [ID 7260 设计](docs/开发规格/16_ID7260交点与参数恢复设计.md)，更新规格导航与实现地图；运行时代码／API 未改。
- **验证**：独立 SymPy 核验 a=2、p=2、焦点(1,0)、距离 2√5/5，两个恢复顺序均成立；不是执行器结果，本批未运行代码回归。
- **下一步**：确认 D5 后小批实现交点解析与参数恢复，再接通 Focus(G) 距离查询。


## 2026-10-02｜D5 确认及 ID 7260 参数子链

- **变更**：交点事实解析为同一内部点及两项归属；新增 RM72 recover_from_point，复用 RM7／公共计算／事务。无关未定约束保留，相关约束仍必须验证。用户修改的 models=[7,72,52] 已核对，数据文件未再编辑。
- **文件**：新增 line_proposals.py、test_bound_intersection_recovery.py；更新状态、应用器、model_072.py、接口／实现地图／D5 规格，保存两条参数轨迹。
- **验证**：新增 17 项，相关回归 299 passed；两个顺序均 a=2、p=2。详见[实现记录](docs/开发规格/17_ID7260参数子链实现记录.md)。
- **限制／下一步**：仅参数子链，原始 Focus(G) 距离查询未实现；下一批扩展该查询与 RM52 属性点绑定。
- **释义补充（2026-10-03）**：`line_proposals.py` 的 `recover_line_from_point` 利用已知点满足直线方程这一条件恢复一个参数，提出参数值、斜率和截距；已给交点坐标解析复用坐标／归属结构，不是求交点运算。


## 2026-10-02｜ID 7260 原始焦点距离查询闭环

- **变更**：新增 FocusLineDistanceQuery、RM52 point_role=focus 绑定，消费已提交焦点／框架／直线参数；原始固定链 RM7→RM72→RM52 得到 2√5/5，查询只读。
- **文件**：更新状态、应用器、距离提案、bound_slice.py；新增 test_bound_focus_line_distance.py、更新参数子链测试，维护接口／实现地图／规格，保存完整 v7 trace。
- **验证**：新增 15 项，相关回归 314 passed；原题 CLI 成功，反向参数恢复顺序亦验证。见[闭环记录](docs/开发规格/18_ID7260焦点距离闭环.md)。
- **限制／下一步**：固定回放而非自主模型选择；RM52 焦点模式限抛物线。下一批按职责表选择新的模型／真实案例扩展。
- **释义补充（2026-10-03）**：`FocusLineDistanceQuery` 指定要求哪条曲线的焦点到哪条直线的距离；`focus_line_distance_proposal` 读取既有焦点属性及直线参数，调用距离公式并返回 RM52 提案，不在查询读取中求参。


## 2026-10-02｜全 80 模型审计与下一组选型

- **变更**：新增 AST／数据审计工具，扫描80 ID、5357题；16 ID有绑定方法，其余64无绑定方法（不等于可执行覆盖）。比较离心率、切线、通径、消元／根关系及距离／中点候选，选定下一批 RM13 正向。
- **文件**：新增 scripts/audit/model_binding_inventory.py、[选型规格](docs/开发规格/19_模型覆盖审计与下一组选型.md)及两份 JSON 快照，更新职责索引、实现地图、规格导航；运行时 API 未改。
- **验证**：ID5988/7488/1586/4528 已执行标准模型→RM11/12 前置子链，独立数学 e 分别 √3/2、√2/2、√5/2、2；尚无 RM13 输出，不计原题已求解。审计结构与链接检查通过。
- **下一步**：按已写前提／输出契约实现 RM13 正向、查询读取和四题原始回放；范围与反向模式另批处理。


## 2026-10-03｜RM13 正向及四题离心率闭环

- **变更**：新增 derive_eccentricity 提案，严格消费既有平方参数；EccentricityQuery 只读；solve_eccentricity_slice 串联标准模型→RM11/12→RM13，四题原始输入闭环。
- **文件**：新增 eccentricity_proposals.py、test_bound_eccentricity.py；更新状态、应用器、model_013.py、bound_slice.py、API／实现地图／规格；保存四份 v7 trace 与新的结构审计快照。
- **验证**：新增20项，相关回归334 passed；四题结果 √3/2、√2/2、√5/2、2。见[记录](docs/开发规格/20_RM13正向离心率实现记录.md)。
- **下一步**：先明确 RM39／ID2106 切线契约，暂不扩展离心率范围和反向模式。
- **释义补充（2026-10-03）**：`eccentricity_proposals.py` 的 `derive_eccentricity` 核验已有平方参数并计算 e，返回离心率属性提案；`EccentricityQuery` 只记录要求哪条曲线的离心率。


## 2026-10-03｜RM39 切点验证与 ID 2106 切线闭环

- **变更**：明确四方向正确切线公式，新增 derive_tangent 与只读 TangentQuery；绑定实际点／曲线，执行时验证切点，原子提交派生切线及来源。固定 RM9→RM39 得到 y=−2x−1。
- **文件**：新增 tangent_proposals.py、model_039.py、test_bound_parabola_tangent.py；更新状态、应用器、定理库与 bound_slice.py，同步 API／实现地图／规格，保存 id2106_bound_trace.json。
- **验证**：新增 17 项、相关回归 351 passed；四方向与顶点使用独立梯度公式核验。见[实现记录](docs/开发规格/21_RM39抛物线切线实现记录.md)。
- **限制／下一步**：仅标准抛物线已知数值切点；旧无绑定接口不执行，派生切线尚未接入 RM52／交点链。下一批先明确消元／根关联契约再分步推进。
- **释义补充（2026-10-03）**：`tangent_proposals.py` 的实际函数名为 `derive_parabola_tangent`，负责验证点在抛物线上并生成切线方程提案（上文 derive_tangent 是动作模式名）；`TangentQuery` 记录指定曲线及切点，`model_039.py` 提供模型入口。


## 2026-10-03｜ID 6347 契约与 RM78 消元子步骤

- **变更**：明确消元、根对资格、韦达、弦长和只读查询的职责；实现 substitute_line_in_parabola、RM78 substitute_line 及 IntersectionReduction 原子提交。ID 6347 得到 x=y+1、y²−4y−4=0；不提前生成交点或弦长。
- **文件**：新增 intersection_operations.py、intersection_proposals.py、test_bound_intersection_reduction.py；更新状态、应用器、model_078.py 与维护文档，新增[契约](docs/开发规格/22_ID6347消元与根关联契约.md)和子步骤证据。用户修改的 RM39 原公式保留，修订旧文档说明。
- **验证**：新增 24 项、相关回归 375 passed；独立联立解核验根还原，覆盖退化／相切／无实交点与事务边界。
- **限制／下一步**：仅数值标准抛物线和独立直线；原始弦长查询未接入。下一批补 RM42/43 与实根对资格，再接 RM50；未知直线和命名根关联（ID56）后置。
- **释义补充（2026-10-03）**：`intersection_operations.py` 的 `substitute_line_in_parabola` 返回消元方程及坐标还原映射；`intersection_proposals.py` 的 `substitute_bound_line` 核验绑定并包装 RM78 提案。`LineSubstitution` 是公共计算返回值；`IntersectionReduction` 是附带对象及方程来源的消元结果记录，供后续根关系计算读取，本身不执行消元。


## 2026-10-03｜近期开发文档释义完善

- **变更**：核对 09-24 至 10-03 的开发记录及 09-23 基础接口；实现地图分开解释计算与提案模块，API 补充核心函数／数据结构／查询的中文用途，旧日志保留并增加有日期的释义。
- **文件**：仅更新 doc/project_structure.md、doc/api_reference.md、dev_record.md；无运行时代码或数据变更。
- **验证**：链接、核心定义与源码对应、旧日志保留及差异格式检查；未重跑代码测试，历史测试数字不作为本次新结果。
- **后续**：每批按 AGENTS.md 的说明要求，在文档与 Commit description 中记录具体操作或保存内容。


## 2026-10-03｜ID 6347 根关系与弦长闭环

- **公共计算**：intersection_operations.py 增加 quadratic_coefficients（核验二次系数）、quadratic_root_relation（返回根和或积）、classify_quadratic_roots（返回判别式与不同实根数）；QuadraticRootStatus 保存资格计算结果。chord_length_from_relations 根据已知根和积与坐标映射计算弦长，不补做韦达。
- **模型组织与保存**：intersection_proposals.py 的 derive_root_relation 提出根关系和资格属性，derive_chord_length 消费已有属性并提出长度；model_042/043/050 负责入口转交，应用器统一提交到以消元事实 ID 为键的 properties，记录来源并处理冲突。
- **查询与回放**：ChordLengthQuery 只表示指定线／曲线的弦长目标，extract_answer 只读结果；solve_chord_length_slice 固定组织 RM78→RM42→RM43→RM50，ID 6347 原始查询得到 8。
- **文件**：新增 model_050.py、test_bound_chord_length.py、[闭环规格](docs/开发规格/23_ID6347根关系与弦长闭环.md)和 v8 轨迹；更新公共计算、提案、状态、应用器、RM42/43、定理库、回放入口及三份维护文档／规格导航。
- **验证**：新增 27 项、相关回归 402 passed；原题 CLI 成功，独立交点距离、顺序交换、水平／竖直线、相切／无实根／一次式、隔离和回滚通过。
- **限制／下一步**：数值标准抛物线与独立直线固定链；不生成命名交点，不代表自主选择。下一批明确 ID56 未知直线参数化、命名根关联与斜率非零条件。


## 2026-10-03｜ID56 参数化契约与命名直线初态

- **文件职责**：新增 named_line_facts.py，解析命名直线、交点集合和斜率和；更新 transition_state.py 接入这些给定结构、Origin 坐标定义和只读直线查询。新增 test_bound_named_line_input.py 验证原题及输入边界。
- **核心定义**：register_named_line 规范端点顺序与直线身份，parse_named_line_fact 记录关系；NamedLine 保存身份，NamedIntersection 保存无序点集来源，SlopeSum 保存数值斜率和及待验证非零 x 差，分别供 RM78／RM55 后续消费。NamedLineQuery 只表达目标；from_facts 不生成参数，extract_answer 不求参。
- **效果／验证**：ID56 原始 facts/query 可完整解析；14 项新增、416 项相关回归通过，保存 parsed_only 初态证据，答案仍为空、revision=0。
- **契约／下一步**：明确水平分支排除、局部参数作用域、无序根对及分母证据，见[规格](docs/开发规格/24_ID56命名直线与参数化契约.md)。下一批先实现 RM78 参数化与根对关联，再扩展符号根关系及 RM55；本批不是原题求解闭环。
