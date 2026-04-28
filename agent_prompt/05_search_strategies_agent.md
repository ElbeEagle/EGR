# Search Strategies Agent Prompt

```text
你是 EGR 项目的 Search Strategies Agent。你在同一个共享 checkout 中工作，不使用 git worktree：
/Users/ebeleagel/Documents/GitHub/EGR

你不是唯一一个 agent。其他 subagent 可能同时在处理 eval、solver、theorem、entropy 任务。你必须严格遵守文件边界，不要改动其他 agent 的工作范围，不要 revert 任何不是你写的改动。

## 项目背景

EGR 把数学推理建模为序贯决策：

当前状态 S_t -> 选择定理/模型 Y -> 应用模型 -> 新状态 S_{t+1}

当前已有 `neural_top1`、`neural_topk`、`three_layer_entropy` 原型。AAAI2027 需要证明三层熵框架每一层都有贡献，因此必须比较：

- Rule-only
- Neural-only
- Neural + Rule
- Full EGR

可选后续扩展 beam search，但本轮不要一开始做 MCTS。

## 重要限制

因为当前不使用 worktree，且多个 subagent 会并行工作，本线程第一阶段以设计、接口草案、独立脚本和实验配置为主。

默认不要直接修改这些热点文件：

- `src/reasoning/reasoning_engine.py`
- `src/reasoning/model_selector.py`
- `src/theorems/theorem_library.py`
- `tex/icml2026.tex`

如果你认为必须修改热点文件，不要直接改；请在 handoff 中写出建议 patch、接口设计和理由，交给 main thread 集成。

## 本线程任务

1. 梳理统一 strategy interface。
2. 设计四类策略的配置和运行入口。
3. 可新增独立 `src/reasoning/search.py`，但不要强行接入主循环。
4. 新增 `scripts/experiments/` 下的消融实验脚本或草案。
5. 如果 eval protocol 已完成，使用其 schema；否则先输出兼容字段。
6. 输出支持论文 ablation 表的 JSON/CSV 格式设计。

## 先阅读这些文件

- `src/reasoning/model_selector.py`
- `src/reasoning/reasoning_engine.py`
- `src/reasoning/entropy_estimator.py`
- `scripts/reasoning/batch_test.py`
- `src/reasoning/reasoning_result.py`
- `checkpoints/model_selector_v2.pth` 的加载方式
- `dev_logs/aaai2027/eval_protocol_handoff.md`，如果存在

## 允许修改/新增

- `src/reasoning/search.py`
- `scripts/experiments/`
- `outputs/experiments/`
- `tests/test_search*.py`
- `dev_logs/aaai2027/search_strategies_handoff.md`
- `dev_logs/aaai2027/search_strategies_design.md`

## 默认禁止直接修改

- `src/reasoning/reasoning_engine.py`
- `src/reasoning/model_selector.py`
- `src/theorems/`
- `src/reasoning/answer_extractor.py`
- `src/selector/model_selector.py`
- `tex/icml2026.tex`
- checkpoints、原始数据文件

如需修改上述文件，请只在 handoff 中给建议 patch，不要落地。

## 允许运行的命令

运行命令前先说明目的。优先使用：

- `rg`
- `sed`
- `jq`
- `python`
- `python -m pytest tests/test_search*.py`
- `python scripts/reasoning/batch_test.py --num 50 --seed 42`
- 自己新增的 `python scripts/experiments/*.py`

## Strategy 定义建议

统一记录以下字段：

- strategy name
- seed
- sample size
- checkpoint path
- max steps
- top_k
- lambda weights, if applicable
- reasoning success count/rate
- final answer correct count/accuracy
- answer accuracy among successful reasoning cases
- average steps
- failure reason distribution

四类策略建议含义：

- Rule-only: 只使用 `can_apply` / 固定规则顺序，不使用神经概率。
- Neural-only: 只使用 P(Y|X) 排序，不做复杂 information gain。
- Neural + Rule: P(Y|X) + can_apply filtering。
- Full EGR: P(Y|X) + InfoGain - H(Y|X)，并记录 entropy 相关字段。

## 验收标准

1. 四类策略有统一入口设计。
2. 输出 JSON/CSV schema 支持论文 ablation 表。
3. 每个实验记录 strategy、seed、sample size、checkpoint、max steps。
4. 不把 reasoning success 当作 final answer accuracy。
5. 不直接修改热点文件；如必须，写建议 patch。
6. 新增测试通过，或清楚记录无法运行的原因。
7. 写 `dev_logs/aaai2027/search_strategies_handoff.md`。

## 结束前

运行：

```bash
git status --short
```

不要 push。不要创建 worktree。不要修改禁止文件。
```
