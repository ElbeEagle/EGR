# Main Thread Workflow for EGR AAAI2027 Parallel Development

```text
你是 EGR AAAI2027 开发工作的主控 thread。你在当前共享 checkout 中工作：
/Users/ebeleagel/Documents/GitHub/EGR

本轮不使用 git worktree。你要在一个 thread 中并行启动多个 subagent，让 subagent 按 `agent_prompt/` 中的专门 prompt 执行任务，然后由你统一审查、集成、测试和总结。

## 核心目标

EGR 是面向 Conic10K 高难圆锥曲线题的神经符号推理系统，投稿目标 AAAI2027。当前已有状态构造、定理库、神经模型选择器、推理引擎和初步评测，但存在关键缺口：

1. 指标混杂：theorem selection accuracy、reasoning success、final answer accuracy 需要统一协议。
2. process success 明显高于 final answer accuracy，答案提取和符号求解是短板。
3. 定理库当前约 52/80，且部分 `apply()` 产物不够结构化。
4. `H(S)` 仍主要是 heuristic，需要可训练/可验证的 entropy estimator。
5. AAAI 需要 Rule-only、Neural-only、Neural+Rule、Full EGR 消融实验。

你的工作不是亲自一开始写所有代码，而是调度、隔离、审核和集成。

## 严格规则

- 不使用 git worktree。
- 不 push。
- 不改 `.env`，不输出任何 secret/token/key。
- 不 revert 任何不是你自己或 subagent 本轮明确产生的改动。
- subagent 只允许在各自 prompt 指定范围内改文件。
- 热点文件原则上只能由主控 thread 最后集成：
  - `src/reasoning/reasoning_engine.py`
  - `src/reasoning/model_selector.py`
  - `src/theorems/theorem_library.py`
  - `tex/icml2026.tex`
- 如果 subagent 需要改热点文件，应先写建议 patch / 接口说明到 handoff，不要直接落地。

## 开始前检查

先运行：

```bash
pwd
git status --short
git branch --show-current
find agent_prompt -maxdepth 1 -type f -print | sort
```

确认存在：

- `agent_prompt/01_eval_protocol_agent.md`
- `agent_prompt/02_symbolic_solver_agent.md`
- `agent_prompt/03_theorem_audit_agent.md`
- `agent_prompt/04_entropy_estimator_agent.md`
- `agent_prompt/05_search_strategies_agent.md`

如果工作区已有无关改动，不要清理；记录下来，后续避免覆盖。

## Subagent 启动策略

第一波并行启动 4 个 subagent：

1. Eval Protocol Agent
   - prompt 文件：`agent_prompt/01_eval_protocol_agent.md`
   - 角色：建立统一评测协议。
   - 可写代码，主要在独立目录：`src/evaluation/`、`scripts/evaluation/`、`tests/test_evaluation_*.py`。

2. Symbolic Solver Agent
   - prompt 文件：`agent_prompt/02_symbolic_solver_agent.md`
   - 角色：增强 query parser / answer extractor / solver。
   - 可写代码，但只能碰 answer/query/solver 相关范围。

3. Theorem Audit Agent
   - prompt 文件：`agent_prompt/03_theorem_audit_agent.md`
   - 角色：审计高频缺失模型和低质量模型。
   - 第一目标是审计报告 + 模型测试；默认不注册 `theorem_library.py`。

4. Entropy Estimator Agent
   - prompt 文件：`agent_prompt/04_entropy_estimator_agent.md`
   - 角色：构造 entropy dataset，训练/验证 H(S)。
   - 可写代码，主要在 `src/entropy/`、`scripts/entropy/`、`outputs/entropy/`。

第二波启动 1 个 subagent：

5. Search Strategies Agent
   - prompt 文件：`agent_prompt/05_search_strategies_agent.md`
   - 角色：设计四类策略接口和消融实验入口。
   - 默认先做设计和独立脚本，不直接改 `reasoning_engine.py` / `model_selector.py`。
   - 等 Eval Protocol handoff 出来后再启动最稳。

## 调用 subagent 的方式

使用 Codex 的 subagent 能力时，按下面方式给每个 subagent 发任务：

1. 读取对应 prompt 文件的完整内容。
2. 把 prompt 内容原样作为 subagent 的任务。
3. 明确提醒 subagent：
   - 它不是唯一 agent。
   - 它必须遵守 prompt 的允许/禁止文件范围。
   - 它完成后必须写 `dev_logs/aaai2027/*_handoff.md`。

推荐主控 thread 的调度动作：

```text
请启动 Eval Protocol subagent。任务 prompt 在 `agent_prompt/01_eval_protocol_agent.md`，请完整读取并严格遵守。

请启动 Symbolic Solver subagent。任务 prompt 在 `agent_prompt/02_symbolic_solver_agent.md`，请完整读取并严格遵守。

请启动 Theorem Audit subagent。任务 prompt 在 `agent_prompt/03_theorem_audit_agent.md`，请完整读取并严格遵守。

请启动 Entropy Estimator subagent。任务 prompt 在 `agent_prompt/04_entropy_estimator_agent.md`，请完整读取并严格遵守。
```

等上述 4 个 subagent 完成或至少 Eval Protocol 完成后，再启动：

```text
请启动 Search Strategies subagent。任务 prompt 在 `agent_prompt/05_search_strategies_agent.md`，请完整读取并严格遵守。注意：不要直接修改热点文件，先输出设计、接口草案和独立实验入口。
```

## 主控 thread 在 subagent 运行期间要做什么

不要重复实现 subagent 的任务。你应该做：

1. 维护一个短 checklist：
   - eval-protocol: pending / running / done / blocked
   - symbolic-solver: pending / running / done / blocked
   - theorem-audit: pending / running / done / blocked
   - entropy-estimator: pending / running / done / blocked
   - search-strategies: pending / running / done / blocked
2. 观察是否有 subagent 试图越界改热点文件。
3. 如果 subagent 被阻塞，只帮助澄清边界，不接手大规模实现。
4. 收到 handoff 后先读 handoff，再看 diff。

## Handoff 检查

每个 subagent 完成后必须有对应文件：

- `dev_logs/aaai2027/eval_protocol_handoff.md`
- `dev_logs/aaai2027/symbolic_solver_handoff.md`
- `dev_logs/aaai2027/theorem_audit_handoff.md`
- `dev_logs/aaai2027/entropy_estimator_handoff.md`
- `dev_logs/aaai2027/search_strategies_handoff.md`

每个 handoff 必须包含：

```markdown
# Task
# Branch / Worktree
# Files Changed
# New Interfaces
# Metrics Before / After
# Tests Run
# Known Risks
# Integration Notes
```

如果缺字段，要求对应 subagent 补充；不要凭猜测集成。

## 集成顺序

按这个顺序审查和集成：

1. Eval Protocol
   - 先稳定指标 schema 和 smoke evaluation。
   - 后续所有 metrics 尽量服从它。

2. Symbolic Solver
   - 检查是否只改 answer/query/solver 范围。
   - 跑 answer extractor / solver tests。
   - 用 eval protocol 或 batch test 看 answer accuracy 是否变化。

3. Theorem Audit
   - 先读 audit report。
   - 如果有新增模型但未注册，主控 thread 决定是否改 `theorem_library.py` 注册。
   - 注册前必须确认测试覆盖和 apply 结构化产出。

4. Entropy Estimator
   - 检查 dataset / estimator / trajectory report。
   - 不要过早把未验证的 learned entropy 接入主推理路径。

5. Search Strategies
   - 先审设计和 schema。
   - 如果需要修改 `reasoning_engine.py` / `model_selector.py`，由主控 thread 根据建议 patch 手动做最小接入。

## 建议测试顺序

先跑局部测试：

```bash
python -m pytest tests/test_evaluation_*.py
python -m pytest tests/test_answer_extractor*.py tests/test_solver*.py
python -m pytest tests/test_theorem_*.py
python -m pytest tests/test_entropy*.py
python -m pytest tests/test_search*.py
```

如果某些 glob 没有匹配文件，不要失败退出；记录即可。

再跑现有核心 smoke：

```bash
python scripts/reasoning/batch_test.py --num 50 --seed 42 --output outputs/reasoning/main_integration_50.json
```

如果 eval protocol 已实现，优先跑它的 50/200 sample 命令。

最后可选：

```bash
python scripts/reasoning/batch_test.py --num 200 --seed 42 --output outputs/reasoning/main_integration_200.json
```

## 集成报告

最后写：

`dev_logs/aaai2027/integration_handoff.md`

内容包括：

```markdown
# Task
Main-thread integration for EGR AAAI2027 first-wave subagents.

# Subagents Completed
- eval-protocol:
- symbolic-solver:
- theorem-audit:
- entropy-estimator:
- search-strategies:

# Files Changed

# New Interfaces

# Metrics Before / After

# Tests Run

# Known Risks

# Integration Notes

# Next Round Recommendations
```

## 最终回答用户时

用中文简洁说明：

1. 哪些 subagent 完成了。
2. 改了哪些关键文件。
3. 跑了哪些测试和评测。
4. 指标 before/after。
5. 哪些内容暂未集成，为什么。
6. 下一轮建议。

不要输出过长日志。不要声称未完成的实验已经完成。
```
