

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

- **开发记录**：[docs/开发规格/07_RM5_RM21实现记录.md](docs/开发规格/07_RM5_RM21实现记录.md)
- **变更**：ID 2 固定执行 RM5→RM21，求得 m=5；加入对象／方程绑定、前提与实根筛选、事务提交、来源记录和受限回代。重复动作不新增状态，失败／多解不误提交。
- **新增文件**：`src/state/transition_state.py`、`src/solver/transition_primitives.py`、`src/theorems/bound_application.py`、`src/reasoning/bound_slice.py`、`tests/test_bound_transition_slice.py`。
- **更新文件**：`src/theorems/base_model.py`、`src/theorems/models/model_005.py`、`model_021.py`；同步开发规格，并保存诊断 trace。
- **验证**：当批记录为 79 passed（25 项新测试及 54 项相关回归）；命令、证据和范围见[开发记录](docs/开发规格/07_RM5_RM21实现记录.md)。不作为全系统准确率。
- **限制／下一步**：尚未接入旧求解器、轨迹构建器和选择器；RM21 新接口仅实现反向模式。建议下一批以 ID 9 检验多曲线关系，再分批扩展模型和轨迹。
- **释义补充（2026-10-03）**：`TransitionState` 保存题目与推理状态；`BoundAction` 指定模型及作用对象；`Proposal` 保存待提交变化；`BoundApplicator.apply` 校验并写入状态；`TransitionResult` 保存执行结果。`bound_slice.py` 组织固定动作回放，`transition_primitives.py` 提供解析／条件检查／实根筛选等计算。


## 2026-09-24｜整理开发导航与维护约定

- **开发记录**：无独立开发记录（文档维护）；
- **变更**：重写 [实现地图](doc/project_structure.md) 与 [关键接口](doc/api_reference.md)，区分前期原型、新绑定切片和后续计划；新增根目录 [AGENTS.md](AGENTS.md)，约定开发前回顾及开发后同步维护。旧开发记录原样保留，历史指标不作为当前结果。
- **范围**：仅上述三份文档及本日志，不修改运行时代码、数据或模型定义。
- **验证**：关键签名已对照代码；本地链接、API 最小示例、旧日志前缀保留检查及 `git diff --check` 通过。`python3 -m pytest -q tests/test_bound_transition_slice.py`：25 passed。
- **下一步**：按实现地图分批扩展；每批只更新受影响条目，避免重复维护完整功能清单。

## 2026-09-24｜ID 9 多曲线共焦点绑定执行

- **开发记录**：[docs/开发规格/08_ID9共焦点实现记录.md](docs/开发规格/08_ID9共焦点实现记录.md)
- **变更**：复用绑定／事务机制，新增共焦点关系与曲线框架、可追溯的类型条件；RM3→RM11→RM5→RM12 求得 t=9。关系实例化作为公共操作，由 RM12 显式调用。
- **文件**：更新 `src/state/transition_state.py`、`src/solver/transition_primitives.py`、`src/theorems/bound_application.py`、`models/model_003/005/011/012.py`（位于 `src/theorems/`）、`src/reasoning/bound_slice.py`；新增 `tests/test_bound_shared_focus.py`，调整旧绑定测试；同步 API、实现地图及规格，保存 v2 trace。
- **验证**：两条绑定链与相关旧接口回归合计 113 passed。命令、证据和范围见[ID 9 开发记录](docs/开发规格/08_ID9共焦点实现记录.md)。
- **限制／下一步**：仅原点中心、x 轴的标准椭圆—双曲线共焦点固定链，未接入旧求解器／选择器。下一批建议补 RM21 正向和 RM11/RM12 普通参数关系模式；再按案例扩展。
- **释义补充（2026-10-03）**：`FocusEquality` 记录两曲线共焦点关系，`CurveFrame` 记录所属方程的中心／轴向；`instantiate_shared_focus` 核验框架相容，将另一曲线已有 c² 用于目标曲线，并返回来源操作。关系记录自身不计算参数。


## 2026-09-24｜RM21 正向及 RM11/RM12 普通参数模式

- **开发记录**：[docs/开发规格/09_参数关系与渐近线正向实现记录.md](docs/开发规格/09_参数关系与渐近线正向实现记录.md)
- **变更**：RM11/RM12 共用参数提案，支持任意两个平方参数求第三个及三项表达式约束求标量；RM21 正向生成两条渐近线。应用器支持派生方程的原子提交与受限回代，查询读取完整方程对。
- **文件**：新增 `src/theorems/parameter_proposals.py`、`tests/test_bound_parameter_modes.py`；更新状态、应用器、RM11/12/21、固定链入口及接口／实现地图／开发规格，保存 ID 65 v3 trace。
- **验证**：本批 32 项测试；相关回归共 145 passed。真实题 ID 65、200、353 正向链通过，ID 2、ID 9 原链保持通过。命令及完整边界见[开发记录](docs/开发规格/09_参数关系与渐近线正向实现记录.md)。
- **限制／下一步**：参数模式消费已有平方参数事实，未扩展全部文本解析；渐近线正向仍限原点中心、x 轴。下一批建议补 y 轴 RM4/RM6；仍不接入选择器训练。
- **释义补充（2026-10-03）**：`parameter_proposals.py` 的 `parameter_proposal` 利用平方参数恒等式补全参数或求标量，返回更新提案；应用器负责提交。渐近线查询读取已生成的两条方程。


## 2026-09-24｜RM4/RM6 与 y 轴框架、渐近线

- **开发记录**：[docs/开发规格/10_Y轴标准模型实现记录.md](docs/开发规格/10_Y轴标准模型实现记录.md)
- **变更**：RM3–6 抽提共享标准参数提案；新增 RM4/RM6 绑定模式。框架、RM11/RM12 和 RM21 正反向支持 x/y 轴；固定链预检标准方向。修复动作枚举覆盖 `mode` 过滤参数的问题。
- **文件**：新增 `src/theorems/standard_proposals.py`、`tests/test_bound_y_axis.py`；更新公共运算、应用器、参数提案、RM3/4/5/6/21、固定链入口及文档；保存 ID 380 trace。
- **验证**：相关回归 173 passed，其中本批 28 项。ID 380/549 渐近线整链通过；ID 1516 仅参数子链通过，不计整题求解。详见[本批记录](docs/开发规格/10_Y轴标准模型实现记录.md)。
- **限制／下一步**：仍限原点中心、坐标轴对齐；未接入选择器。下一批建议明确 ID 5 抛物线及点归属参数恢复的执行模式后开发。
- **释义补充（2026-10-03）**：`standard_proposals.py` 的 `standard_proposal` 从绑定的椭圆／双曲线方程提取半轴平方、轴向和类型条件，供 RM3–6 共用；返回提案而非直接修改状态。


## 2026-09-27｜ID 5 抛物线参数恢复与焦半径

- **开发记录**：[docs/开发规格/11_ID5抛物线实现记录.md](docs/开发规格/11_ID5抛物线实现记录.md)
- **变更**：明确标准模型恢复参数／确认方向／输出焦点、RM17 计算焦半径、查询只读的边界。ID 5 固定 RM9→RM17 得到 5/4；四方向共用实现，不按方向假设过滤参数根。
- **文件**：新增 `src/solver/parabola_operations.py`、`src/theorems/parabola_proposals.py`、`tests/test_bound_parabola.py`；更新状态、绑定、RM7–10/17 和固定链入口；同步文档并保存 ID 5 v4 trace。
- **验证**：相关回归 204 passed，其中本批 31 项；覆盖真实题、四方向、条件不足、多解、冲突回滚及旧接口。测试辅助函数曾误用 pytest 的 setup 名称，重命名后消除启动错误。详见[开发记录](docs/开发规格/11_ID5抛物线实现记录.md)。
- **限制／下一步**：仅原点顶点、数值坐标点、一元系数恢复；未扩展准线或通用距离，也未接入选择器。下一批建议补 RM29 准线及点到直线距离，验证定义路径。
- **释义补充（2026-10-03）**：`parabola_operations.py` 提供标准系数提取、点代入残差及 p／焦点计算；`parabola_proposals.py` 的 `standard_parabola_proposal` 组织参数提取／点恢复，`focal_radius_proposal` 组织 RM17 焦半径计算。`PointCoordinates` 保存坐标，`PointOnCurve` 保存归属，`FocalDistanceQuery` 表示求点到焦点的距离。


## 2026-09-27｜ID 5 准线定义路径与公共距离操作

- **开发记录**：[docs/开发规格/12_ID5定义路径实现记录.md](docs/开发规格/12_ID5定义路径实现记录.md)
- **变更**：增加 RM29 准线、RM52 点到准线距离和 RM2 定义转换；复用并抽提抛物线标准属性校验，保留原 RM17 路径。ID 5 新固定链 RM9→RM29→RM52→RM2 得到 5/4。
- **文件**：新增 `src/solver/distance_operations.py`、`tests/test_bound_parabola_definition.py`；更新抛物线提案、绑定应用器、RM2/29/52、回放入口及 API／实现地图／规格，保存独立 v4 trace。
- **验证**：新增 23 项测试，相关回归 227 passed；真实 CLI 回放成功。详见[开发记录](docs/开发规格/12_ID5定义路径实现记录.md)。
- **限制／下一步**：公共距离支持一般数值直线，绑定入口暂限抛物线准线；下一批建议扩展真实一般直线案例和距离查询。未接入选择器／旧求解器。
- **释义补充（2026-10-03）**：`distance_operations.py` 的 `point_to_line_distance` 由数值点和直线方程计算精确距离；`directrix_proposal` 提出准线方程，`definition_proposal` 核验点及准线后，将既有准线距离作为焦半径提出。


## 2026-09-27｜RM52 独立直线绑定与距离查询

- **开发记录**：[docs/开发规格/13_一般直线距离实现记录.md](docs/开发规格/13_一般直线距离实现记录.md)
- **变更**：解析独立 Line 与点到直线查询；BoundAction 增加 line，RM52 复用通用距离提案，保留准线兼容；新增单步回放，trace 升为 v5。
- **文件**：新增 distance_proposals.py、test_bound_line_distance.py；更新 transition_state.py、bound_application.py、parabola_proposals.py、model_052.py、bound_slice.py 及接口／实现地图／规格和诊断轨迹。
- **验证**：新增 24 项，相关回归 251 passed；ID 5882/1253 显式事实投影距离为 4／10，仅诊断，不计原题求解。详见[开发记录](docs/开发规格/13_一般直线距离实现记录.md)。
- **限制／下一步**：仍限数值点到显式直线距离；建议下一批通过 ID 3723 衔接准线别名与 RM29 输出，继续暂缓选择器训练。
- **释义补充（2026-10-03）**：`distance_proposals.py` 的 `point_line_distance_proposal` 读取绑定点／线并调用公共距离计算，返回距离属性提案；`PointLineDistanceQuery` 记录要求哪个点到哪条直线的距离，不执行计算。


## 2026-09-29｜ID 3723 准线别名原题闭环

- **开发记录**：[docs/开发规格/14_ID3723准线别名实现记录.md](docs/开发规格/14_ID3723准线别名实现记录.md)
- **变更**：增加 DirectrixAlias 与共用身份解析；RM52 绑定并记录别名事实和 RM29 准线输出，查询只读。原题 RM9→RM29→RM52 得到 65/16，不改写输入或复制方程。
- **文件**：更新 transition_state.py、bound_application.py、distance_proposals.py、bound_slice.py；新增 test_bound_directrix_alias.py，同步 API／实现地图／规格及 ID 3723 v5 轨迹。
- **验证**：新增 16 项，相关回归 267 passed；原始 CLI 回放成功，见[开发记录](docs/开发规格/14_ID3723准线别名实现记录.md)。
- **限制／下一步**：多重别名和别名附加独立方程暂不合并；下一批建议明确焦点别名坐标实例化（ID 946／1793），继续复用距离链。
- **释义补充（2026-10-03）**：`DirectrixAlias` 保存“G 的准线就是 l”的身份关系；`line_bindings` 查找 l 对应的已有准线方程，供 RM52 使用，不重新计算准线。


## 2026-09-29｜ID 946／1793 焦点别名坐标实例化

- **开发记录**：[docs/开发规格/15_焦点别名坐标实现记录.md](docs/开发规格/15_焦点别名坐标实现记录.md)
- **变更**：FocusAlias 初态只记录身份；RM7–10 同步提出命名焦点坐标，应用器原子提交并记录来源。原准线固定链按提交后的坐标绑定 RM52，两道原题分别得到 1/8、1/4。
- **文件**：更新 transition_state.py、parabola_proposals.py、bound_application.py、bound_slice.py；新增 test_bound_focus_alias.py，维护接口／实现地图／规格，保存两份 v6 轨迹。
- **验证**：新增 15 项，相关回归 282 passed；已有坐标冲突整步回滚，来源与重复执行验证通过。详见[开发记录](docs/开发规格/15_焦点别名坐标实现记录.md)。
- **限制／下一步**：限抛物线有限实数焦点坐标，同一点多别名暂不合并；建议下一批先明确 ID 7260 的交点参数恢复职责。
- **释义补充（2026-10-03）**：`FocusAlias` 保存“G 的焦点就是 F”的身份关系；标准抛物线提案依据已计算的焦点位置提出 F 的 `PointCoordinates`，应用器检查一致性后提交。


## 2026-10-02｜ID 7260 交点事实与参数恢复职责设计

- **开发记录**：[docs/开发规格/16_ID7260交点与参数恢复设计.md](docs/开发规格/16_ID7260交点与参数恢复设计.md)
- **结论**：交点坐标是给定事实；抛物线恢复复用 RM7，直线恢复推荐 D5：RM72 点斜式一致性的受限反向模式，不将任意代入归为 RM78。D5 尚待确认。
- **文件**：新增 [ID 7260 设计](docs/开发规格/16_ID7260交点与参数恢复设计.md)，更新规格导航与实现地图；运行时代码／API 未改。
- **验证**：独立 SymPy 核验 a=2、p=2、焦点(1,0)、距离 2√5/5，两个恢复顺序均成立；不是执行器结果，本批未运行代码回归。
- **下一步**：确认 D5 后小批实现交点解析与参数恢复，再接通 Focus(G) 距离查询。


## 2026-10-02｜D5 确认及 ID 7260 参数子链

- **开发记录**：[docs/开发规格/17_ID7260参数子链实现记录.md](docs/开发规格/17_ID7260参数子链实现记录.md)
- **变更**：交点事实解析为同一内部点及两项归属；新增 RM72 recover_from_point，复用 RM7／公共计算／事务。无关未定约束保留，相关约束仍必须验证。用户修改的 models=[7,72,52] 已核对，数据文件未再编辑。
- **文件**：新增 line_proposals.py、test_bound_intersection_recovery.py；更新状态、应用器、model_072.py、接口／实现地图／D5 规格，保存两条参数轨迹。
- **验证**：新增 17 项，相关回归 299 passed；两个顺序均 a=2、p=2。详见[开发记录](docs/开发规格/17_ID7260参数子链实现记录.md)。
- **限制／下一步**：仅参数子链，原始 Focus(G) 距离查询未实现；下一批扩展该查询与 RM52 属性点绑定。
- **释义补充（2026-10-03）**：`line_proposals.py` 的 `recover_line_from_point` 利用已知点满足直线方程这一条件恢复一个参数，提出参数值、斜率和截距；已给交点坐标解析复用坐标／归属结构，不是求交点运算。


## 2026-10-02｜ID 7260 原始焦点距离查询闭环

- **开发记录**：[docs/开发规格/18_ID7260焦点距离闭环.md](docs/开发规格/18_ID7260焦点距离闭环.md)
- **变更**：新增 FocusLineDistanceQuery、RM52 point_role=focus 绑定，消费已提交焦点／框架／直线参数；原始固定链 RM7→RM72→RM52 得到 2√5/5，查询只读。
- **文件**：更新状态、应用器、距离提案、bound_slice.py；新增 test_bound_focus_line_distance.py、更新参数子链测试，维护接口／实现地图／规格，保存完整 v7 trace。
- **验证**：新增 15 项，相关回归 314 passed；原题 CLI 成功，反向参数恢复顺序亦验证。见[闭环记录](docs/开发规格/18_ID7260焦点距离闭环.md)。
- **限制／下一步**：固定回放而非自主模型选择；RM52 焦点模式限抛物线。下一批按职责表选择新的模型／真实案例扩展。
- **释义补充（2026-10-03）**：`FocusLineDistanceQuery` 指定要求哪条曲线的焦点到哪条直线的距离；`focus_line_distance_proposal` 读取既有焦点属性及直线参数，调用距离公式并返回 RM52 提案，不在查询读取中求参。


## 2026-10-02｜全 80 模型审计与下一组选型

- **开发记录**：[docs/开发规格/19_模型覆盖审计与下一组选型.md](docs/开发规格/19_模型覆盖审计与下一组选型.md)
- **变更**：新增 AST／数据审计工具，扫描80 ID、5357题；16 ID有绑定方法，其余64无绑定方法（不等于可执行覆盖）。比较离心率、切线、通径、消元／根关系及距离／中点候选，选定下一批 RM13 正向。
- **文件**：新增 scripts/audit/model_binding_inventory.py、[选型规格](docs/开发规格/19_模型覆盖审计与下一组选型.md)及两份 JSON 快照，更新职责索引、实现地图、规格导航；运行时 API 未改。
- **验证**：ID5988/7488/1586/4528 已执行标准模型→RM11/12 前置子链，独立数学 e 分别 √3/2、√2/2、√5/2、2；尚无 RM13 输出，不计原题已求解。审计结构与链接检查通过。
- **下一步**：按已写前提／输出契约实现 RM13 正向、查询读取和四题原始回放；范围与反向模式另批处理。


## 2026-10-03｜RM13 正向及四题离心率闭环

- **开发记录**：[docs/开发规格/20_RM13正向离心率实现记录.md](docs/开发规格/20_RM13正向离心率实现记录.md)
- **变更**：新增 derive_eccentricity 提案，严格消费既有平方参数；EccentricityQuery 只读；solve_eccentricity_slice 串联标准模型→RM11/12→RM13，四题原始输入闭环。
- **文件**：新增 eccentricity_proposals.py、test_bound_eccentricity.py；更新状态、应用器、model_013.py、bound_slice.py、API／实现地图／规格；保存四份 v7 trace 与新的结构审计快照。
- **验证**：新增20项，相关回归334 passed；四题结果 √3/2、√2/2、√5/2、2。见[记录](docs/开发规格/20_RM13正向离心率实现记录.md)。
- **下一步**：先明确 RM39／ID2106 切线契约，暂不扩展离心率范围和反向模式。
- **释义补充（2026-10-03）**：`eccentricity_proposals.py` 的 `derive_eccentricity` 核验已有平方参数并计算 e，返回离心率属性提案；`EccentricityQuery` 只记录要求哪条曲线的离心率。


## 2026-10-03｜RM39 切点验证与 ID 2106 切线闭环

- **开发记录**：[docs/开发规格/21_RM39抛物线切线实现记录.md](docs/开发规格/21_RM39抛物线切线实现记录.md)
- **变更**：明确四方向正确切线公式，新增 derive_tangent 与只读 TangentQuery；绑定实际点／曲线，执行时验证切点，原子提交派生切线及来源。固定 RM9→RM39 得到 y=−2x−1。
- **文件**：新增 tangent_proposals.py、model_039.py、test_bound_parabola_tangent.py；更新状态、应用器、定理库与 bound_slice.py，同步 API／实现地图／规格，保存 id2106_bound_trace.json。
- **验证**：新增 17 项、相关回归 351 passed；四方向与顶点使用独立梯度公式核验。见[开发记录](docs/开发规格/21_RM39抛物线切线实现记录.md)。
- **限制／下一步**：仅标准抛物线已知数值切点；旧无绑定接口不执行，派生切线尚未接入 RM52／交点链。下一批先明确消元／根关联契约再分步推进。
- **释义补充（2026-10-03）**：`tangent_proposals.py` 的实际函数名为 `derive_parabola_tangent`，负责验证点在抛物线上并生成切线方程提案（上文 derive_tangent 是动作模式名）；`TangentQuery` 记录指定曲线及切点，`model_039.py` 提供模型入口。


## 2026-10-03｜ID 6347 契约与 RM78 消元子步骤

- **开发记录**：[docs/开发规格/22_ID6347消元与根关联契约.md](docs/开发规格/22_ID6347消元与根关联契约.md)
- **变更**：明确消元、根对资格、韦达、弦长和只读查询的职责；实现 substitute_line_in_parabola、RM78 substitute_line 及 IntersectionReduction 原子提交。ID 6347 得到 x=y+1、y²−4y−4=0；不提前生成交点或弦长。
- **文件**：新增 intersection_operations.py、intersection_proposals.py、test_bound_intersection_reduction.py；更新状态、应用器、model_078.py 与维护文档，新增[契约](docs/开发规格/22_ID6347消元与根关联契约.md)和子步骤证据。用户修改的 RM39 原公式保留，修订旧文档说明。
- **验证**：新增 24 项、相关回归 375 passed；独立联立解核验根还原，覆盖退化／相切／无实交点与事务边界。
- **限制／下一步**：仅数值标准抛物线和独立直线；原始弦长查询未接入。下一批补 RM42/43 与实根对资格，再接 RM50；未知直线和命名根关联（ID56）后置。
- **释义补充（2026-10-03）**：`intersection_operations.py` 的 `substitute_line_in_parabola` 返回消元方程及坐标还原映射；`intersection_proposals.py` 的 `substitute_bound_line` 核验绑定并包装 RM78 提案。`LineSubstitution` 是公共计算返回值；`IntersectionReduction` 是附带对象及方程来源的消元结果记录，供后续根关系计算读取，本身不执行消元。


## 2026-10-03｜近期开发文档释义完善

- **开发记录**：无独立开发记录（文档维护）；
- **变更**：核对 09-24 至 10-03 的开发记录及 09-23 基础接口；实现地图分开解释计算与提案模块，API 补充核心函数／数据结构／查询的中文用途，旧日志保留并增加有日期的释义。
- **文件**：仅更新 doc/project_structure.md、doc/api_reference.md、dev_record.md；无运行时代码或数据变更。
- **验证**：链接、核心定义与源码对应、旧日志保留及差异格式检查；未重跑代码测试，历史测试数字不作为本次新结果。
- **后续**：每批按 AGENTS.md 的说明要求，在文档与 Commit description 中记录具体操作或保存内容。


## 2026-10-03｜ID 6347 根关系与弦长闭环

- **开发记录**：[docs/开发规格/23_ID6347根关系与弦长闭环.md](docs/开发规格/23_ID6347根关系与弦长闭环.md)
- **公共计算**：intersection_operations.py 增加 quadratic_coefficients（核验二次系数）、quadratic_root_relation（返回根和或积）、classify_quadratic_roots（返回判别式与不同实根数）；QuadraticRootStatus 保存资格计算结果。chord_length_from_relations 根据已知根和积与坐标映射计算弦长，不补做韦达。
- **模型组织与保存**：intersection_proposals.py 的 derive_root_relation 提出根关系和资格属性，derive_chord_length 消费已有属性并提出长度；model_042/043/050 负责入口转交，应用器统一提交到以消元事实 ID 为键的 properties，记录来源并处理冲突。
- **查询与回放**：ChordLengthQuery 只表示指定线／曲线的弦长目标，extract_answer 只读结果；solve_chord_length_slice 固定组织 RM78→RM42→RM43→RM50，ID 6347 原始查询得到 8。
- **文件**：新增 model_050.py、test_bound_chord_length.py、[闭环规格](docs/开发规格/23_ID6347根关系与弦长闭环.md)和 v8 轨迹；更新公共计算、提案、状态、应用器、RM42/43、定理库、回放入口及三份维护文档／规格导航。
- **验证**：新增 27 项、相关回归 402 passed；原题 CLI 成功，独立交点距离、顺序交换、水平／竖直线、相切／无实根／一次式、隔离和回滚通过。
- **限制／下一步**：数值标准抛物线与独立直线固定链；不生成命名交点，不代表自主选择。下一批明确 ID56 未知直线参数化、命名根关联与斜率非零条件。


## 2026-10-03｜ID56 参数化契约与命名直线初态

- **开发记录**：[docs/开发规格/24_ID56命名直线与参数化契约.md](docs/开发规格/24_ID56命名直线与参数化契约.md)
- **文件职责**：新增 named_line_facts.py，解析命名直线、交点集合和斜率和；更新 transition_state.py 接入这些给定结构、Origin 坐标定义和只读直线查询。新增 test_bound_named_line_input.py 验证原题及输入边界。
- **核心定义**：register_named_line 规范端点顺序与直线身份，parse_named_line_fact 记录关系；NamedLine 保存身份，NamedIntersection 保存无序点集来源，SlopeSum 保存数值斜率和及待验证非零 x 差，分别供 RM78／RM55 后续消费。NamedLineQuery 只表达目标；from_facts 不生成参数，extract_answer 不求参。
- **效果／验证**：ID56 原始 facts/query 可完整解析；14 项新增、416 项相关回归通过，保存 parsed_only 初态证据，答案仍为空、revision=0。
- **契约／下一步**：明确水平分支排除、局部参数作用域、无序根对及分母证据，见[规格](docs/开发规格/24_ID56命名直线与参数化契约.md)。下一批先实现 RM78 参数化与根对关联，再扩展符号根关系及 RM55；本批不是原题求解闭环。


## 2026-10-04｜ID56 RM78 参数化与无序根关联

- **开发记录**：[docs/开发规格/25_ID56参数化与命名根关联实现.md](docs/开发规格/25_ID56参数化与命名根关联实现.md)
- **公共计算／提案**：intersection_operations.py 的 parameterize_through_point 检查水平分支并生成过点直线族与符号消元；intersection_proposals.py 的 parameterize_named_line 包装结果和来源，model_078.py 按模式转交，均不直接提交状态。
- **保存／提交**：LineParameterization 保存局部参数、过点来源与派生方程 ID，IntersectionReduction 新字段保存无序点标签及交点来源；BoundAction.incidence_id 明确过点关系。应用器将参数、直线、消元及两根条件原子提交，冲突回滚。
- **效果**：ID56 提出 x=uy+1、y²−2uy−2=0 与 {A.y,B.y} 根集合关联；参数与原题符号隔离，答案仍为空。详见[开发记录](docs/开发规格/25_ID56参数化与命名根关联实现.md)。
- **文件／验证**：更新公共计算、提案、状态、应用器、RM78 与旧初态测试；新增 test_bound_named_parameterization.py、子步骤轨迹与规格，同步维护文档。新增14项、相关回归430项通过。
- **限制／下一步**：首批数值 x 轴标准抛物线；下一批符号 RM42/43，再接 RM55 分母验证、求参与新结构统一归约。不计整题求解。


## 2026-10-04｜ID56 符号韦达与斜率求参闭环

- **开发记录**：[docs/开发规格/26_ID56符号韦达与斜率求参闭环.md](docs/开发规格/26_ID56符号韦达与斜率求参闭环.md)
- **公共计算／提案**：intersection_operations.py 的二次系数、根关系和资格函数支持指定局部实参数；derive_root_relation 核验根关联后提出符号结果。新增 slope_proposals.py，solve_named_slope_sum 读取既有根关系、证明分母非零，再提出参数赋值；model_055.py 转交绑定应用。
- **提交／查询**：BoundAction.slope_sum_id 选择给定斜率和；应用器归约消元式与坐标映射，和赋值／直线一起提交并保留来源。solve_named_slope_slice 固定组织四步执行，既有查询只读方程。
- **效果／验证**：ID56 得到 u=−1/2、2x+y−2=0；新增18项、相关回归448项通过，独立交点斜率核验及全链重放通过，保存 v9 完整轨迹。
- **文件**：新增 slope_proposals.py、test_bound_named_slope.py、规格及轨迹；更新公共计算、根提案、应用器、RM55、回放入口、三份维护文档与规格导航／索引。
- **限制／下一步**：限数值 x 轴标准抛物线、原点斜率和及单个局部参数；回到全库选型，优先考虑 ID6347 焦点弦长备用路径 RM33，先明确过焦点前提。


## 2026-10-05｜ID6347 RM33 焦点弦长路径

- **开发记录**：[docs/开发规格/27_ID6347焦点弦长路径.md](docs/开发规格/27_ID6347焦点弦长路径.md)
- **文件／核心定义**：新增 focal_chord_proposals.py，derive_focal_chord 读取已有标准属性与根和，验证直线过焦点，提出焦点弦长；model_033.py 新增绑定入口。应用器增加 RM33 绑定／候选，沿用事务；solve_focal_chord_slice 组织标准模型→RM78→RM42→RM33 的独立固定回放。
- **保存／效果**：沿用 chord_length 供原查询读取，focus_on_line=1 保存成功验证标记，证明残差与来源记入轨迹；ID6347 得8，不执行 RM43 或额外根积性质，不覆盖 RM50 路径。
- **验证／文件**：新增 test_bound_focal_chord.py，15项新增、463项相关回归通过；保存 v10 独立轨迹，同步 API／实现地图／日志／规格，并完成原 TODO。
- **限制／下一步**：数值标准抛物线与独立直线；回到职责表与真实数据选型，先审查 RM34/35 等关系的前提与焦点证据复用。


## 2026-10-06｜RM34/35 焦点证据审查与首批选型

- **开发记录**：[docs/开发规格/28_RM34_RM35证据审查与首批选型.md](docs/开发规格/28_RM34_RM35证据审查与首批选型.md)
- **文件／核心定义**：新增 focal_chord_candidates.py 只读审查工具；build_audit 记录候选原文、哈希和解析缺口，verify_product_identities 独立核验四方向乘积。JSON快照保存审查结果，不是执行轨迹。同步维护文档及规格导航／职责表。
- **结论**：7条RM34、6条RM35、去重11条；首批4373数值积子链，1191轴向验证，1833符号后置。1254非焦点弦；1191解答使用横向积，弱标签不能直接视作正确动作。
- **验证**：候选计数、四方向符号恒等式和首批数值关系通过；不改运行时，不作整题已解或覆盖率声明，不重跑大规模回归。
- **下一步**：补显式焦点归属与命名交点证据，支持两来源核验，再实现数值RM34/35；RM59点积查询后接。


## 2026-10-07｜RM34/35 数值焦点弦与 RM59 原点点积

- **开发记录**：[docs/开发规格/29_RM34_RM35与原点点积闭环.md](docs/开发规格/29_RM34_RM35与原点点积闭环.md)
- **输入／证据**：named_line_facts.py 与 transition_state.py 记录独立命名交点、FocusOnLine 焦点归属和 OriginDotProductQuery 目标；新增 focal_chord_evidence.py，verify_focal_chord 返回给定／计算两来源的绑定、参数和核验记录，不写状态，供 RM33/34/35 使用。
- **模型／结果**：新增 model_034.py／model_035.py 并注册；focal_chord_proposals.py 的 derive_coordinate_product 提出弦所属 x/y积，derive_origin_dot 读取两项积及原点坐标后提出点积；RM59 转交绑定提案。bound_application.py 核对绑定，沿用原子提交；extract_answer 只读结果。
- **效果／验证**：4373 原题 RM7→RM34→RM35→RM59 得−3；1191投影轴向/横向(4,−16)，6347计算证据(1,−4)，无需RM33／RM43。新增30项、相关493项通过，文档链接与差异空白检查通过。
- **文件／证据**：新增 test_bound_focal_products.py、规格29与id4373_origin_dot_trace.json；bound_slice.py 增加固定回放入口，同步三份维护文档与规格导航／索引。
- **限制／下一步**：数值标准抛物线、原点点积；1191面积未求解，未接自主选择器。回到职责表选型；1833符号参数及坐标分量别名另批。

## 2026-10-10｜ID1833 坐标别名与只读乘积查询

- **开发记录**：[docs/开发规格/30_ID1833坐标别名与乘积查询.md](docs/开发规格/30_ID1833坐标别名与乘积查询.md)
- `src/state/coordinate_product_facts.py`（新增）→ 保存给定分量身份、计数和查询目标。CoordinateComponentAlias 保存标量／点／轴向及来源；IntersectionCount 保存给定交点数；CoordinateProductQuery 表达两分量乘积。parse_coordinate_product_fact 记录结构，validate_coordinate_product_input 检查声明矛盾与查询绑定，read_coordinate_product 只定位唯一命名点对的已有坐标积，不计算。
- `src/state/transition_state.py`（扩展）→ 接入新输入与答案读取。coordinate_aliases／intersection_counts 保存解析结果；from_facts 增加入口及末尾校验，extract_answer 调用只读定位。复用已有 NamedIntersection 与 properties，不修改模型提案或应用器。
- `tests/test_bound_coordinate_products.py`（新增）→ 验证原始初态、正性边界、数值查询衔接与冲突／歧义；`docs/开发规格/artifacts/id1833_coordinate_input.json` 保存 parsed_only 初态，供后续开发复核，不是执行轨迹。
- **效果／验证**：新增16项、针对性46项、相关509项通过。1833原始输入解析成功，revision=0、answer=None；显式p>0诊断可执行已有RM7，但RM35仍拒绝符号参数。数值构造输入经RM7→RM35读得−4。差异空白、文档链接及初态证据检查通过。
- **文件／边界**：新增规格30、输入模块、测试和证据；更新状态、三份维护文档、规格导航／索引。原始数据未改，原题未求解；不将已有数值接口说成符号支持。
- **下一步**：明确符号焦点弦条件来源、原式系数与正几何参数区别；正参数诊断须显式p>0，原始1833则需非退化且方向无关的处理，不能默认正性。


## 2026-10-14｜ID1833 方向无关符号焦点弦

- **开发记录**：[docs/开发规格/31_ID1833方向无关符号焦点弦.md](docs/开发规格/31_ID1833方向无关符号焦点弦.md)
- `src/solver/parabola_operations.py` → 公共核验：新增signed_parabola_parameter，返回轴向、有符号q、Abs(q)和待提交非零条件，复用标准式提取，不写状态。
- `src/theorems/focal_chord_evidence.py` → 来源处理：新增given_focus_sources抽提直接／别名焦点归属ID，数值与符号路径复用。
- `src/theorems/symbolic_focal_proposals.py`（新增）→ 提案组织：derive_symbolic_product核验给定焦点弦，提出类型导出的q≠0及一项坐标积；显式线方程／相关坐标未核验时返回未定。
- `src/theorems/focal_chord_proposals.py` → 扩展derive_coordinate_product的符号模式转交；`src/theorems/bound_application.py` → 扩展enumerate_actions的显式符号候选，复用既有条件／属性原子提交，不改变数值模式。
- `src/reasoning/bound_slice.py` → 新增solve_symbolic_focal_product_slice固定回放RM35及v12输出；`tests/test_bound_symbolic_focal.py`（新增）→ 验证原题、符号前提、轴向、拒绝边界和事务性。
- **效果／验证**：原始1833得−p²，终态保存p≠0及来源，不默认p>0，不产生方向框架或正参数属性。新增23项、相关532项通过；保存id1833_symbolic_product_trace.json，文档链接及空白检查通过。
- **文件／边界**：新增规格31、提案模块、测试及轨迹；同步三份维护文档与导航／索引。限一个实符号数值倍数系数和已给命名焦点弦；原题已固定回放，尚未接自主选择器。已有论文改动不触碰。
- **下一步**：回到职责表选有限模型／案例，按实际需要扩展符号交叉核验，不扩大到任意符号线求交。


## 2026-10-14｜RM38 椭圆切线与ID2126

- **开发记录**：[docs/开发规格/32_RM38椭圆切线与ID2126.md](docs/开发规格/32_RM38椭圆切线与ID2126.md)
- `src/solver/tangent_operations.py`（新增）→ 数值椭圆切线公共计算；ellipse_tangent核验实际分母及点归属，返回残差和隐式方程，不写状态。
- `src/theorems/tangent_proposals.py` → 新增derive_ellipse_tangent，复用已提交参数／框架核验，按轴向映射分母，提出附来源的切线；`src/theorems/models/model_038.py` → 新增propose_bound转交，旧接口保留。
- `src/theorems/bound_application.py` → 扩展check_binding／enumerate_actions到RM38，并允许其切线提案沿用事务提交；`src/state/transition_state.py` → 扩展from_facts接受椭圆TangentQuery，复用已有查询类和只读结果，不新增推导。
- `src/reasoning/bound_slice.py` → 新增solve_ellipse_tangent_slice与v13轨迹；固定预检标准方向后回放RM3/4→RM38，不读弱标注指导选择。
- `tests/test_bound_ellipse_tangent.py`（新增）→ 验证原题、二重交点、轴向、竖直／水平、缺参数、错误绑定、冲突及范围拒绝。
- **效果／验证**：ID2126原题得x/4+y/2−1=0，等价于x+2y−4=0。新增20项、相关552项通过，链接／空白／轨迹检查通过；新增id2126_ellipse_tangent_trace.json，同步三份维护文档与规格导航／索引。
- **边界／下一步**：仅原点中心轴对齐非圆数值椭圆已知点，不支持外点引切线、未知切点或符号参数。下一批先审查RM54／4795的中点身份与RM40/45弦方向职责；已有论文改动未触碰。


## 2026-10-14｜ID4795 中点身份与RM54／40／45职责审查

- **开发记录**：[docs/开发规格/33_ID4795中点身份与弦方向契约.md](docs/开发规格/33_ID4795中点身份与弦方向契约.md)
- `docs/开发规格/33_ID4795中点身份与弦方向契约.md`（新增）→ 保存弦／中点／匿名无序端点对的拟议身份、模型前提输出和实现顺序；RM54负责端点和，RM40直接消费中点，RM45为点差备选，不新增运行时定义。
- `docs/开发规格/artifacts/midpoint_chord_contract_audit.json`（新增）→ 保存原始输入、弱标签、数据哈希、当前解析阻碍及独立数学核验，供实现前复核；不是执行轨迹。
- `doc/project_structure.md`／`doc/api_reference.md` → 分别标明下一批接入顺序与尚无接口的边界；规格导航和职责索引同步链接审查。
- **结论／验证**：4795应走y轴RM4，独立核验2x+y−2=0及两实交点的中点；7439数学核验x+2y−3=0但对象语法延期。两个真实案例、5个边界探针及链接／空白检查通过；无运行时代码修改，不重跑或更新历史回归统计。
- **下一步**：先实现4795复合中点、弦身份／匿名端点对及只读Expression(l)初态；再RM4→RM40。RM54→RM45另批，处理中心未定、非内点冲突与同源绑定。现阶段不声称系统已解4795。


## 2026-10-14｜ID4795匿名中点弦与RM40闭环

- **开发记录**：[docs/开发规格/34_ID4795中点弦与RM40闭环.md](docs/开发规格/34_ID4795中点弦与RM40闭环.md)
- `src/state/chord_facts.py`（新增）→ 保存给定弦信息。`ChordIdentity`保存直线、曲线、端点对ID和来源；`AnonymousEndpointPair`保存无序端点对身份及给定来源，不能当成计算得到的根；`ChordMidpoint`保存同源中点坐标。`parse_chord_midpoint`核对声明、数值坐标及重复一致性，供RM40绑定，后续可供RM54使用。
- `src/state/transition_state.py` → 管理状态与只读答案。新增`chords/chord_endpoint_pairs/chord_midpoints`容器，扩展`from_facts`解析复合中点和独立Line查询；复用NamedLineQuery和extract_answer，不新增推导型查询。
- `src/solver/midpoint_operations.py`（新增）→ 公共数值计算。`ellipse_midpoint_chord`读取实际分母和中点，核验内点／非中心，返回ρ、法向量与直线；`canonical_numeric_line`归一化一次式，供同一直线等价核验。均不修改状态。
- `src/theorems/midpoint_proposals.py`（新增）→ 组织RM40提案。`check_midpoint_binding`核对曲线方程、弦及匿名对的同源性；`derive_midpoint_chord`读取已提交参数／框架、核验已有线方程，提出派生方程与弦级ρ、法向量、两不同实交点资格及来源，交应用器提交。
- `src/theorems/models/model_040.py`（新增）／`src/theorems/theorem_library.py` → 提供并注册RM40入口。`EllipseMidpointChord.propose_bound`转交上述提案；旧can_apply/apply保持不可用，不将绑定功能宣称已接旧求解器。
- `src/theorems/bound_application.py` → 绑定与事务提交。扩展`enumerate_actions/check_binding`按弦产生／核验候选；扩展`BoundApplicator.apply`仅接受绑定直线上的RM40派生方程，复用冲突检查、来源记录与no_op处理。
- `src/reasoning/bound_slice.py` → 固定诊断回放。新增`solve_midpoint_chord_slice`预检RM3/4方向，再回放RM40；CLI增加midpoint-chord和v14轨迹，不读取process、答案或弱标签指导动作。
- `tests/test_bound_midpoint_chord.py`（新增）→ 验证原题、初态无坐标／无答案、对象隔离、重复来源、轴向及退化边界、已有线一致性、错误绑定、事务回滚和幂等。求交仅用于独立测试核验，不进入运行时。

- **验证／效果**：新增22项、相关回归574项通过；原题固定RM4→RM40得2x+y−2=0。初态无答案，无端点坐标，保存parsed_only初态和v14轨迹。
- **文件／边界**：新增规格34及两份JSON证据，同步三份维护文档、导航和索引。限中心轴对齐数值非圆椭圆，符号／命名端点核验延期；未修改数据弱标注及用户论文文件。
- **下一步**：RM54提交同源匿名端点坐标和，RM45消费这些关系；不作为RM40强制依赖。


## 2026-10-15｜RM54匿名端点和与RM45点差闭环

- **开发记录**：[docs/开发规格/35_ID4795端点和与点差路径.md](docs/开发规格/35_ID4795端点和与点差路径.md)
- `src/solver/midpoint_operations.py` → 公共计算。抽提`verify_ellipse_midpoint`供两条路径核验资格；新增`midpoint_coordinate_sums`返回中点两倍，`ellipse_point_difference`读取端点和，返回ρ、法向量、直线及点差系数。均不写状态。
- `src/theorems/midpoint_proposals.py` → 模型提案。新增`derive_endpoint_sums`提出匿名对属性；新增`derive_point_difference_chord`读取同对属性及来源后组织点差计算。抽提`chord_line_proposal`核验已有线并提出统一结果，由应用器提交。复用现有properties保存`(pair_id,x_sum/y_sum)`，不是新端点坐标结构。
- `src/theorems/models/model_054.py`／`src/theorems/models/model_045.py` → 模型入口。前者新增绑定提案转交并保留旧接口；后者新增EllipsePointDifference，绑定入口转交RM45提案，旧接口不可用。
- `src/theorems/theorem_library.py` → 注册库。新增RM45注册；RM54沿用已有注册。
- `src/theorems/bound_application.py` → 候选与提交。扩展`enumerate_actions/check_binding`支持RM54/45同源弦绑定；扩展`apply`允许RM45向该弦直线提交派生方程。坐标和复用既有属性事务／来源机制。
- `src/reasoning/bound_slice.py` → 诊断编排。新增`solve_point_difference_slice`固定预检RM3/4后回放RM54→RM45；增加point-difference CLI和v15轨迹，不用弱标注、process或答案决定动作。
- `tests/test_bound_point_difference.py` → 新增20项测试，检查真实原题、坐标和依赖／来源／对象隔离、两轴与零分量、退化边界、冲突回滚及两条路径交叉幂等。

- **效果／验证**：ID4795固定RM4→RM54→RM45得到2x+y−2=0；本批20项、两路径42项、相关回归594项通过。保存v15原题轨迹，同步维护文档、导航及索引。
- **边界／下一步**：限数值匿名中点弦，不生成端点坐标，RM40无新增前置依赖，未接自主选择器。回到职责表选择有限案例；命名端点身份关联及核验另批。未修改用户论文及数据弱标注。


## 2026-10-18｜命名端点候选与身份核验契约

- **开发记录**：[docs/开发规格/36_命名端点候选与身份核验契约.md](docs/开发规格/36_命名端点候选与身份核验契约.md)
- `scripts/audit/named_chord_candidates.py`（新增）→ 候选审查；CASES保存从原事实人工转录的系数／中点与选型，audit_candidates读取原记录、探测解析并独立核验交点判别式和中点，非求解器。
- `docs/开发规格/artifacts/named_chord_candidate_audit.json`（新增）→ 保存7题原输入、弱标注、参考答案、数据哈希及独立计算，标记design_audit_only，不是模型轨迹。
- `docs/开发规格/36_命名端点候选与身份核验契约.md`（新增）→ 明确无序端点名关联现有匿名pair、来源分别保留、重排／重复／歧义处理及已有坐标核验职责；三份维护文档和导航／索引同步未实现边界。
- **效果／验证**：首批5644／3682／6164独立核验分别得2x+2y−3=0、y=x+1、2x−8y−9=0，均有两个不同实交点且中点正确；3119无实弦，7300结构化输入推得3x+4y−7=0，与参考答案不同，保留待审。不新增运行时覆盖，不更新历史594项回归统计。
- **下一步**：先解析命名关联和复合中点初态，再有限核验端点与已有直线，复用两条独立模型链。7439对象语法、命名中点别名、RM46另批；未修改数据或用户论文。


## 2026-10-18｜命名端点中点弦首批实现

- **开发记录**：[docs/开发规格/37_命名端点中点弦实现.md](docs/开发规格/37_命名端点中点弦实现.md)
- `src/state/chord_facts.py` → 输入关联。新增ChordEndpointNames保存pair_id、无序点名及交点来源；collect_named_chords两遍收集交点／复合中点，返回已处理事实位置，供主解析跳过。扩展parse_chord_midpoint合并弦来源，同时保留中点自身来源。
- `src/state/transition_state.py` → 状态与解析。新增chord_endpoint_names字典，from_facts调用上述前置收集；复用原匿名对、坐标存储和只读查询。
- `src/solver/midpoint_operations.py` → 公共核验。新增verify_chord_endpoints读取曲线、候选直线、中点及已给坐标，检查归属、不同性和中点一致性；不构造点，不修改状态。
- `src/theorems/midpoint_proposals.py` → 模型提案。check_midpoint_binding改为核对来源集合的关联，拒绝名称关联丢失或错绑；chord_line_proposal调用端点核验并记录坐标来源和核验操作；RM54／40／45读取弦来源并集，实际提交仍由原应用器完成。
- `tests/test_bound_named_midpoint.py` → 新增32项，覆盖三题两链、初态无答案、反序／重排、来源合并、身份冲突、已有数值／符号坐标、回滚及幂等。

- **效果／验证**：三原题均完成RM3→RM40和RM3→RM54→RM45，结果依次2x+2y−3=0、y=x+1、2x−8y−9=0；新增32项通过，相关回归626项通过。保存三个初态与六条轨迹，同步维护文档和导航索引。
- **边界／下一步**：数值椭圆有限关联，已有符号坐标未定，不生成端点坐标；未接自主选择器。回到职责表选型，7439线段语法、命名中点别名与RM46另批。


## 2026-10-19｜ID7439线段弦对象与原题闭环

- **开发记录**：[docs/开发规格/38_ID7439线段弦对象实现.md](docs/开发规格/38_ID7439线段弦对象实现.md)
- `src/state/segment_chord_facts.py`（新增）→ 有限线段输入关联。SegmentChord保存segment、line、curve及IsChordOf来源；collect_segment_chords两遍收集关系／中点，创建内部直线身份，返回已处理事实位置供主解析跳过，不做几何计算。
- `src/state/chord_facts.py` → 中点存储。抽提store_chord_midpoint，在对象已解析后核验数值坐标、合并来源并复用既有弦／匿名对；原parse_chord_midpoint转交该函数，保留原语法。
- `src/state/transition_state.py` → 状态与查询入口。新增segment_chords字典、LineSegment声明识别和前置收集；Expression(OverlappingLine(H))定位既有NamedLineQuery，查询不求解方程。
- `src/theorems/midpoint_proposals.py` → 绑定提案。扩展check_midpoint_binding，校验线段类型、内部直线、曲线及关系来源；允许来源为中点与身份声明并集，丢失／错绑关系则拒绝。公共计算和状态提交未新增。
- `tests/test_bound_segment_chord.py`（新增）→ 22项验证，覆盖原题两链、初态、独立交点核验、重排／重复、来源、对象隔离、退化与延期语法拒绝。

- **效果／验证**：原始7439固定RM3→RM40和RM3→RM54→RM45均得x+2y−3=0。新增22项、相关回归648项通过，保存初态及两条轨迹；同步三份维护文档、导航和模型索引。
- **边界／下一步**：仅数值椭圆复合中点，不生成端点坐标；命名中点／显式所在直线别名和RM46后置。下一批可审查命名中点的来源关联；未接自主选择器，未修改用户论文。


## 2026-10-19｜命名中点别名与RM46资格审查

- **开发记录**：[docs/开发规格/39_命名中点别名与RM46资格审查.md](docs/开发规格/39_命名中点别名与RM46资格审查.md)
- `scripts/audit/midpoint_alias_contract.py`（新增）→ 独立审查。CASES保存原事实的数值转录，numeric_probe沿点差方向代入并返回实交点／中点资格；audit保留8题输入和解析缺口、比较参考答案，检查6个双曲线边界。
- `docs/开发规格/artifacts/midpoint_alias_contract_audit.json`（新增）→ 保存原文、事实、来源数据哈希及独立结果，标记design_audit_only，不作模型轨迹。
- `docs/开发规格/39_命名中点别名与RM46资格审查.md`（新增）→ 规定弦身份、别名声明、点坐标的来源关联、解析顺序、冲突和快照复查；单列RM46有限实弦资格。三份维护文档与导航／索引同步未实现边界。
- **效果／验证**：2227／2324／3337／2290／4761独立核验与答案一致；7300原文和事实支持3x+4y−7=0，与答案不同，保留隔离。双曲线6类边界通过，1801有实弦、3119无实弦。未修改运行时或数据，不更新历史648项回归统计。
- **下一步**：仅实现三个线段命名中点别名案例及来源链核验；命名端点中点别名和RM46另批。


## 2026-10-22｜线段命名中点别名首批实现

- **开发记录**：[docs/开发规格/40_线段命名中点别名实现.md](docs/开发规格/40_线段命名中点别名实现.md)
- `src/state/midpoint_alias_facts.py`（新增）→ 别名关联与快照检查。ChordMidpointAlias保存chord_id、segment、point、声明sources及coordinate_id／xy快照。collect_midpoint_aliases收集线段别名；resolve_midpoint_aliases在原事实解析后只关联已给数值；check_midpoint_alias在绑定时核对当前记录，过期返回conflict、缺失不可应用、符号未定，均不补推坐标。
- `src/state/chord_facts.py` → 既有中点记录。扩展ChordMidpoint的可选alias_point字段，标明值来自哪个命名点，供绑定时检测别名丢失；不是新增坐标对象。
- `src/state/transition_state.py` → 状态与解析编排。新增midpoint_aliases容器，from_facts先收集别名、末尾解析坐标关联，复用PointCoordinates、弦／匿名对及只读查询。
- `src/theorems/midpoint_proposals.py` → 模型绑定。check_midpoint_binding在读取中点前调用别名快照检查；RM40／54／45计算、提案和原应用器提交不变，读取已有来源并集。
- `tests/test_bound_midpoint_alias.py`（新增）→ 48项测试，覆盖三题两链、来源、重排、缺／符号坐标、冲突、共享点隔离和三模型快照篡改回滚。
- `tests/test_bound_segment_chord.py` → 移除已过时的“命名中点必须拒绝”用例，其成功行为由新测试覆盖；其他拒绝边界保留。

- **效果／验证**：2227使用RM4，2324／3337使用RM3；两条独立链分别得到2x+y−3=0、5x+9y−14=0、x+2y−2=0。新增48项、线段相关69项、相关回归695项通过，保存三个初态及六条轨迹，维护文档和导航同步。
- **边界／下一步**：仅数值线段中点别名，缺坐标不可应用、符号未定、过期快照不自动刷新。下一批命名端点中点别名2290／4761，RM46另批；查询仍只读，未接自主选择器。


## 2026-10-22｜命名端点中点别名2290／4761

- **开发记录**：[docs/开发规格/41_命名端点中点别名实现.md](docs/开发规格/41_命名端点中点别名实现.md)
- `src/state/midpoint_alias_facts.py` → 扩展现有别名模块。ChordMidpointAlias将segment改为可空，新增pair_id、endpoints，保存命名无序对的身份快照。collect_midpoint_aliases新增端点语法并按唯一ChordEndpointNames关联；check_midpoint_alias按两种来源分别核验身份，再复用坐标快照检查。resolve_midpoint_aliases原样复用；模型计算、提案、应用器提交与查询未修改。
- `tests/test_bound_endpoint_midpoint_alias.py`（新增）→ 37项测试。验证两原题两链、来源／初态、反序／重排／重复、歧义／矛盾、缺／符号坐标、三个模型中的身份与坐标篡改回滚、已有端点核验和共享中点隔离。
- `docs/开发规格/artifacts/endpoint_midpoint_alias_traces.json`（新增）→ 保存两个初态及四条固定执行轨迹，包含端点身份、别名、原坐标快照和模型读取来源，供回放复核。

- **效果／验证**：2290采用RM4、4761采用RM3，两条独立链分别得到9x+4y−13=0和x+2y−2=0。新增37项、相关回归732项通过，保存两初态及四轨迹，同步三份维护文档、导航和索引。
- **边界／下一步**：数值椭圆唯一点对绑定，符号中点未定，查询不补推；RM46另批按独立实弦资格推进，未接自主选择器。


## 2026-10-22｜RM46有限双曲线点差实现

- **开发记录**：[docs/开发规格/42_RM46双曲线点差与实弦资格.md](docs/开发规格/42_RM46双曲线点差与实弦资格.md)
- `src/state/chord_facts.py`、`src/state/segment_chord_facts.py` → 输入身份关联。扩展既有中点／交点及线段收集函数，允许双曲线，复用弦身份、无序端点对及别名来源，不生成端点坐标。
- `src/solver/midpoint_operations.py` → 公共计算。新增 `hyperbola_point_difference`，读取带符号系数和端点坐标和，返回方向、直线、代入二次式与判别式；独立检查实弦资格，不修改状态。
- `src/theorems/midpoint_proposals.py` → 模型提案。扩展 `check_midpoint_binding` 和 `derive_point_difference_chord`，核验双曲线绑定、同对坐标和及来源；按轴向选择正负系数，提出直线及弦级 `midpoint_q`、`intersection_discriminant`，供提交和轨迹复核。
- `src/theorems/models/model_046.py`、`src/theorems/bound_application.py` → 模型入口与状态提交。新增 RM46 的 `propose_bound` 转交公共提案；扩展候选、类型隔离及派生直线提交许可，应用器沿用事务提交与冲突回滚。RM54兼容双曲线，RM40／45仍限椭圆。
- `src/reasoning/bound_slice.py` → 固定链诊断。新增 `solve_hyperbola_chord_slice` 和 `hyperbola-chord` 模式，回放 RM5/6→RM54→RM46，再读取已提交直线；不是自主选择器。
- `tests/test_bound_hyperbola_chord.py`（新增）、`tests/test_bound_segment_chord.py` → 行为验证。新增25项覆盖真实题、轴向符号、独立交点核验、退化、前提缺失、错绑与回滚；旧线段拒绝测试改用仍不支持的抛物线类型。

- **效果／验证**：1801／4359固定链得x−y−3=0；3119无实弦拒绝，不计原题已解。新增25项、针对性46项、相关回归757项通过；保存三题轨迹，同步实现地图、API、规格导航与模型索引。
- **边界／下一步**：限原点中心、坐标轴向数值双曲线；中心方向未定，未接自主选择器。回到职责表选择下一组有限案例；不存在直线的答案表达另行定契约。
