# EGR Annotated Bibliography v2

Last updated: 2026-07-09

Source: Zotero My Library collection `AI4Math`, subcollections `Math-Reasoning` and `Neuro-Symbolic`, read through the local Zotero API. This is a breadth-first, EGR-oriented screening pass, not a full-paper close reading. Duplicate titles are merged; Zotero item keys are retained for traceability.

Priority means usefulness for the EGR paper, not the intrinsic quality of the paper.

EGR lens: every paper is evaluated by whether it can support one sentence in the EGR paper: reliable mathematical reasoning should be modeled as state-conditioned theorem-model prediction and executable symbolic state transition, with process-level diagnostics for selection, applicability, execution, termination, and extraction.

## 1. Breadth Search Index / 初筛索引

| No. | Collection | Title | Authors | Venue/Year | Link | Research problem / 研究问题 | Core method / 核心方法一句话 | EGR relation | Supports EGR claim |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | Math-Reasoning | A Survey of Mathematical Reasoning in the Era of Multimodal Large Language Model: Benchmark, Method & Challenges | Yibo Yan, Jiamin Su, Jianxiang He et al. | Findings 2025, 2025 | [link](https://aclanthology.org/2025.findings-acl.614/) | 该工作整理数学推理任务、数据集、基准或领域挑战。 / It organizes math reasoning tasks, datasets, benchmarks, or field challenges. | 通过综述、基准构建、数据集设计或多维评测揭示当前模型局限。 / It uses surveys, benchmark construction, dataset design, or multi-dimensional evaluation to reveal model limitations. | Medium / 中相关 | Related Work: surveys and position papers map the field and standard terminology. |
| 2 | Math-Reasoning | AceMath: Advancing Frontier Math Reasoning with Post-Training and Reward Modeling | Zihan Liu, Yang Chen, Mohammad Shoeybi et al. | Findings 2025, 2025 | [link](https://aclanthology.org/2025.findings-acl.206/) | 该工作研究如何通过数据合成、后训练、奖励模型、强化学习或样本选择提升数学推理表现。 / It studies how data synthesis, post-training, reward modeling, RL, or sample selection improves math reasoning performance. | 构造数学数据、筛选样本、训练奖励/策略模型，或进行数学专门后训练。 / It builds math data, selects samples, trains reward/policy models, or applies math-specific post-training. | Medium / 中相关 | Experiments: data, RL, reward, and tool-augmented systems inform baselines and ablations. |
| 3 | Math-Reasoning | Active Prompting with Chain-of-Thought for Large Language Models | Shizhe Diao, Pengcheng Wang, Yong Lin et al. | ACL 2024, 2024 | [link](https://aclanthology.org/2024.acl-long.73/) | 该工作研究如何让 LLM 生成、搜索或组织更好的中间推理路径。 / It studies how LLMs generate, search, or organize better intermediate reasoning paths. | 通过 CoT、路径搜索、提示选择、guided exploration 或多范式推理改进生成式推理。 / It improves generative reasoning through CoT, path search, prompt selection, guided exploration, or multi-paradigm reasoning. | Medium / 中相关 | Introduction: text-chain reasoning improves LLM math but leaves mathematical validity implicit. |
| 4 | Math-Reasoning | Augmenting Math Word Problems via Iterative Question Composing | Haoxiong Liu, Yifan Zhang, Yifan Luo et al. | Proceedings of the AAAI Conference on Artificial Intelligence, 2025 | [link](https://ojs.aaai.org/index.php/AAAI/article/view/34640) | 该工作研究如何通过数据合成、后训练、奖励模型、强化学习或样本选择提升数学推理表现。 / It studies how data synthesis, post-training, reward modeling, RL, or sample selection improves math reasoning performance. | 构造数学数据、筛选样本、训练奖励/策略模型，或进行数学专门后训练。 / It builds math data, selects samples, trains reward/policy models, or applies math-specific post-training. | Medium / 中相关 | Experiments: data, RL, reward, and tool-augmented systems inform baselines and ablations. |
| 5 | Math-Reasoning | Chain-of-Reasoning: Towards Unified Mathematical Reasoning in Large Language Models via a Multi-Paradigm Perspective | Yiyao Yu, Yuxiang Zhang, Dongdong Zhang et al. | ACL 2025, 2025 | [link](https://aclanthology.org/2025.acl-long.1213/) | 该工作研究如何让 LLM 生成、搜索或组织更好的中间推理路径。 / It studies how LLMs generate, search, or organize better intermediate reasoning paths. | 通过 CoT、路径搜索、提示选择、guided exploration 或多范式推理改进生成式推理。 / It improves generative reasoning through CoT, path search, prompt selection, guided exploration, or multi-paradigm reasoning. | Medium / 中相关 | Introduction: text-chain reasoning improves LLM math but leaves mathematical validity implicit. |
| 6 | Math-Reasoning | CoMAT: Chain of Mathematically Annotated Thought Improves Mathematical Reasoning | Joshua Ong Jun Leang, Aryo Pradipta Gema, Shay B. Cohen et al. | EMNLP 2025, 2025 | [link](https://aclanthology.org/2025.emnlp-main.1024/) | 该工作研究如何把 LLM 数学推理从纯文本转成可执行、可验证的符号表示。 / It studies how to convert LLM math reasoning from prose into executable and verifiable symbolic representations. | 由 LLM 生成逻辑式、形式语言、符号规则、程序或公式结构，再交给求解器/验证器执行。 / The LLM produces logic forms, formal language, symbolic rules, programs, or formula structures that a solver/verifier executes. | Strong / 强相关 | Method motivation: neural proposal should be separated from symbolic execution and verification. |
| 7 | Math-Reasoning | CogMath: Assessing LLMs’ Authentic Mathematical Ability from a Human Cognitive Perspective | Jiayu Liu, Zhenya Huang, Wei Dai et al. | International Conference on Machine Learning, 2025 | [link](https://proceedings.mlr.press/v267/liu25ab.html) | 该工作研究最终答案正确率无法解释中间推理可靠性的问题。 / It addresses why final-answer accuracy cannot diagnose intermediate reasoning reliability. | 使用步骤级反馈、过程监督、验证、错误分类、纠错或元认知评测来分析/改进推理。 / It uses step-level feedback, process supervision, verification, error classification, correction, or metacognitive evaluation. | Strong / 强相关 | Introduction/Experiments: final-answer accuracy is insufficient; process-level reliability must be measured. |
| 8 | Math-Reasoning | Diverse Multi-tool Aggregation with Large Language Models for Enhanced Math Reasoning | Bohan Yao, Vikas Yadav | journalArticle, n.d. | Zotero metadata incomplete | 该工作研究 LLM 能提出求解思路但计算/执行不稳定的问题。 / It addresses the gap between LLM-generated solution plans and unreliable computation/execution. | 让 LLM 生成程序、工具调用或可执行中间步骤，并把精确计算交给外部工具。 / It lets LLMs generate programs, tool calls, or executable intermediate steps and delegates exact computation to external tools. | Strong / 强相关 | Method motivation: neural proposal should be separated from symbolic execution and verification. |
| 9 | Math-Reasoning | Empowering Multi-step Reasoning across Languages via Program-Aided Language Models | Leonardo Ranaldi, Giulia Pucci, Barry Haddow et al. | EMNLP 2024, 2024 | [link](https://aclanthology.org/2024.emnlp-main.678/) | 该工作研究 LLM 能提出求解思路但计算/执行不稳定的问题。 / It addresses the gap between LLM-generated solution plans and unreliable computation/execution. | 让 LLM 生成程序、工具调用或可执行中间步骤，并把精确计算交给外部工具。 / It lets LLMs generate programs, tool calls, or executable intermediate steps and delegates exact computation to external tools. | Strong / 强相关 | Method motivation: neural proposal should be separated from symbolic execution and verification. |
| 10 | Math-Reasoning | Enhancing Mathematical Reasoning in LLMs by Stepwise Correction | Zhenyu Wu, Qingkai Zeng, Zhihan Zhang et al. | ACL 2025, 2025 | [link](https://aclanthology.org/2025.acl-long.1048/) | 该工作研究最终答案正确率无法解释中间推理可靠性的问题。 / It addresses why final-answer accuracy cannot diagnose intermediate reasoning reliability. | 使用步骤级反馈、过程监督、验证、错误分类、纠错或元认知评测来分析/改进推理。 / It uses step-level feedback, process supervision, verification, error classification, correction, or metacognitive evaluation. | Strong / 强相关 | Introduction/Experiments: final-answer accuracy is insufficient; process-level reliability must be measured. |
| 11 | Math-Reasoning | Error Classification of Large Language Models on Math Word Problems: A Dynamically Adaptive Framework | Zhangyue Yin, Yuhong Sun, Xuanjing Huang et al. | journalArticle, n.d. | Zotero metadata incomplete | 该工作研究最终答案正确率无法解释中间推理可靠性的问题。 / It addresses why final-answer accuracy cannot diagnose intermediate reasoning reliability. | 使用步骤级反馈、过程监督、验证、错误分类、纠错或元认知评测来分析/改进推理。 / It uses step-level feedback, process supervision, verification, error classification, correction, or metacognitive evaluation. | Strong / 强相关 | Introduction/Experiments: final-answer accuracy is insufficient; process-level reliability must be measured. |
| 12 | Math-Reasoning | FLAIR: Steering LLM Mathematical Problem Solving based on A Fuzzy-Logic-AssIsted Reasoner | Hao Wu, Hongru Sun, Wanqing Li et al. | ACL 2026, 2026 | [link](https://aclanthology.org/2026.acl-long.1790/) | 该工作研究如何把 LLM 数学推理从纯文本转成可执行、可验证的符号表示。 / It studies how to convert LLM math reasoning from prose into executable and verifiable symbolic representations. | 由 LLM 生成逻辑式、形式语言、符号规则、程序或公式结构，再交给求解器/验证器执行。 / The LLM produces logic forms, formal language, symbolic rules, programs, or formula structures that a solver/verifier executes. | Strong / 强相关 | Method motivation: neural proposal should be separated from symbolic execution and verification. |
| 13 | Math-Reasoning | Fewer is More: Boosting Math Reasoning with Reinforced Context Pruning | Xijie Huang, Li Lyna Zhang, Kwang-Ting Cheng et al. | EMNLP 2024, 2024 | [link](https://aclanthology.org/2024.emnlp-main.758/) | 该工作研究如何通过数据合成、后训练、奖励模型、强化学习或样本选择提升数学推理表现。 / It studies how data synthesis, post-training, reward modeling, RL, or sample selection improves math reasoning performance. | 构造数学数据、筛选样本、训练奖励/策略模型，或进行数学专门后训练。 / It builds math data, selects samples, trains reward/policy models, or applies math-specific post-training. | Medium / 中相关 | Experiments: data, RL, reward, and tool-augmented systems inform baselines and ablations. |
| 14 | Math-Reasoning | Forward-Backward Reasoning in Large Language Models for Mathematical Verification | Weisen Jiang, Han Shi, Longhui Yu et al. | Findings 2024, 2024 | [link](https://aclanthology.org/2024.findings-acl.397/) | 该工作研究最终答案正确率无法解释中间推理可靠性的问题。 / It addresses why final-answer accuracy cannot diagnose intermediate reasoning reliability. | 使用步骤级反馈、过程监督、验证、错误分类、纠错或元认知评测来分析/改进推理。 / It uses step-level feedback, process supervision, verification, error classification, correction, or metacognitive evaluation. | Strong / 强相关 | Introduction/Experiments: final-answer accuracy is insufficient; process-level reliability must be measured. |
| 15 | Math-Reasoning | GRPO-LEAD: A Difficulty-Aware Reinforcement Learning Approach for Concise Mathematical Reasoning in Language Models | Jixiao Zhang, Chunsheng Zuo, Christos Christodoulopoulos et al. | EMNLP 2025, 2025 | [link](https://aclanthology.org/2025.emnlp-main.287/) | 该工作研究如何通过数据合成、后训练、奖励模型、强化学习或样本选择提升数学推理表现。 / It studies how data synthesis, post-training, reward modeling, RL, or sample selection improves math reasoning performance. | 构造数学数据、筛选样本、训练奖励/策略模型，或进行数学专门后训练。 / It builds math data, selects samples, trains reward/policy models, or applies math-specific post-training. | Medium / 中相关 | Experiments: data, RL, reward, and tool-augmented systems inform baselines and ablations. |
| 16 | Math-Reasoning | Key-Point-Driven Data Synthesis with Its Enhancement on Mathematical Reasoning | Yiming Huang, Xiao Liu, Yeyun Gong et al. | Proceedings of the AAAI Conference on Artificial Intelligence, 2025 | [link](https://ojs.aaai.org/index.php/AAAI/article/view/34593) | 该工作研究如何通过数据合成、后训练、奖励模型、强化学习或样本选择提升数学推理表现。 / It studies how data synthesis, post-training, reward modeling, RL, or sample selection improves math reasoning performance. | 构造数学数据、筛选样本、训练奖励/策略模型，或进行数学专门后训练。 / It builds math data, selects samples, trains reward/policy models, or applies math-specific post-training. | Medium / 中相关 | Experiments: data, RL, reward, and tool-augmented systems inform baselines and ablations. |
| 17 | Math-Reasoning | Knowledge-Centered Dual-Process Reasoning for Math Word Problems With Large Language Models | Jiayu Liu, Zhenya Huang, Qi Liu et al. | IEEE Transactions on Knowledge and Data Engineering, 2025 | [link](https://ieeexplore.ieee.org/abstract/document/10946242) | 该工作研究如何让 LLM 生成、搜索或组织更好的中间推理路径。 / It studies how LLMs generate, search, or organize better intermediate reasoning paths. | 通过 CoT、路径搜索、提示选择、guided exploration 或多范式推理改进生成式推理。 / It improves generative reasoning through CoT, path search, prompt selection, guided exploration, or multi-paradigm reasoning. | Medium / 中相关 | Introduction: text-chain reasoning improves LLM math but leaves mathematical validity implicit. |
| 18 | Math-Reasoning | LLMs can Find Mathematical Reasoning Mistakes by Pedagogical Chain-of-Thought | Zhuoxuan Jiang, Haoyuan Peng, Shanshan Feng et al. | preprint, 2025 | [link](http://arxiv.org/abs/2405.06705) | 该工作研究最终答案正确率无法解释中间推理可靠性的问题。 / It addresses why final-answer accuracy cannot diagnose intermediate reasoning reliability. | 使用步骤级反馈、过程监督、验证、错误分类、纠错或元认知评测来分析/改进推理。 / It uses step-level feedback, process supervision, verification, error classification, correction, or metacognitive evaluation. | Strong / 强相关 | Introduction/Experiments: final-answer accuracy is insufficient; process-level reliability must be measured. |
| 19 | Math-Reasoning + Neuro-Symbolic | LeanDojo: Theorem Proving with Retrieval-Augmented Language Models | Kaiyu Yang, Aidan Swope, Alex Gu et al. | Advances in Neural Information Processing Systems, 2023 | [link](https://proceedings.neurips.cc/paper_files/paper/2023/hash/4441469427094f8873d0fecb0c4e1cee-Abstract-Datasets_and_Benchmarks.html) | 该工作研究形式化数学中 proof state、premise/tactic 选择和可验证推理的问题。 / It studies proof states, premise/tactic selection, and verifiable reasoning in formal mathematics. | 用学习模型指导证明搜索、premise retrieval、tactic generation 或形式化验证。 / It uses learned models to guide proof search, premise retrieval, tactic generation, or formal verification. | Strong / 强相关 | Method motivation: mathematical reasoning can be modeled as state/action, premise/tactic, or theorem-model selection. |
| 20 | Math-Reasoning | Learning to Reason Deductively: Math Word Problem Solving as Complex Relation Extraction | Zhanming Jie, Jierui Li, Wei Lu et al. | ACL 2022, 2022 | [link](https://aclanthology.org/2022.acl-long.410/) | 该工作研究如何把 LLM 数学推理从纯文本转成可执行、可验证的符号表示。 / It studies how to convert LLM math reasoning from prose into executable and verifiable symbolic representations. | 由 LLM 生成逻辑式、形式语言、符号规则、程序或公式结构，再交给求解器/验证器执行。 / The LLM produces logic forms, formal language, symbolic rules, programs, or formula structures that a solver/verifier executes. | Strong / 强相关 | Method motivation: neural proposal should be separated from symbolic execution and verification. |
| 21 | Math-Reasoning | Let's Reason Formally: Natural-Formal Hybrid Reasoning Enhances LLM's Math Capability | Ruida Wang, Yuxin Li, Yi R. Fung et al. | EMNLP 2025, 2025 | [link](https://aclanthology.org/2025.emnlp-main.850/) | 该工作研究如何把 LLM 数学推理从纯文本转成可执行、可验证的符号表示。 / It studies how to convert LLM math reasoning from prose into executable and verifiable symbolic representations. | 由 LLM 生成逻辑式、形式语言、符号规则、程序或公式结构，再交给求解器/验证器执行。 / The LLM produces logic forms, formal language, symbolic rules, programs, or formula structures that a solver/verifier executes. | Strong / 强相关 | Method motivation: neural proposal should be separated from symbolic execution and verification. |
| 22 | Math-Reasoning | MARGE: Improving Math Reasoning with Guided Exploration | Jingyue Gao, Runji Lin, Keming Lu et al. | International Conference on Machine Learning, 2025 | [link](https://proceedings.mlr.press/v267/gao25h.html) | 该工作研究如何让 LLM 生成、搜索或组织更好的中间推理路径。 / It studies how LLMs generate, search, or organize better intermediate reasoning paths. | 通过 CoT、路径搜索、提示选择、guided exploration 或多范式推理改进生成式推理。 / It improves generative reasoning through CoT, path search, prompt selection, guided exploration, or multi-paradigm reasoning. | Medium / 中相关 | Introduction: text-chain reasoning improves LLM math but leaves mathematical validity implicit. |
| 23 | Math-Reasoning | MATHSENSEI: A Tool-Augmented Large Language Model for Mathematical Reasoning | Debrup Das, Debopriyo Banerjee, Somak Aditya et al. | NAACL-HLT 2024, 2024 | [link](https://aclanthology.org/2024.naacl-long.54/) | 该工作研究 LLM 能提出求解思路但计算/执行不稳定的问题。 / It addresses the gap between LLM-generated solution plans and unreliable computation/execution. | 让 LLM 生成程序、工具调用或可执行中间步骤，并把精确计算交给外部工具。 / It lets LLMs generate programs, tool calls, or executable intermediate steps and delegates exact computation to external tools. | Strong / 强相关 | Method motivation: neural proposal should be separated from symbolic execution and verification. |
| 24 | Math-Reasoning | Markov Chain of Thought for Efficient Mathematical Reasoning | Wen Yang, Minpeng Liao, Kai Fan et al. | NAACL-HLT 2025, 2025 | [link](https://aclanthology.org/2025.naacl-long.365/) | 该工作研究如何让 LLM 生成、搜索或组织更好的中间推理路径。 / It studies how LLMs generate, search, or organize better intermediate reasoning paths. | 通过 CoT、路径搜索、提示选择、guided exploration 或多范式推理改进生成式推理。 / It improves generative reasoning through CoT, path search, prompt selection, guided exploration, or multi-paradigm reasoning. | Medium / 中相关 | Introduction: text-chain reasoning improves LLM math but leaves mathematical validity implicit. |
| 25 | Math-Reasoning | MathFusion: Enhancing Mathematical Problem-solving of LLM through Instruction Fusion | Qizhi Pei, Lijun Wu, Zhuoshi Pan et al. | ACL 2025, 2025 | [link](https://aclanthology.org/2025.acl-long.367/) | 该工作研究如何通过数据合成、后训练、奖励模型、强化学习或样本选择提升数学推理表现。 / It studies how data synthesis, post-training, reward modeling, RL, or sample selection improves math reasoning performance. | 构造数学数据、筛选样本、训练奖励/策略模型，或进行数学专门后训练。 / It builds math data, selects samples, trains reward/policy models, or applies math-specific post-training. | Medium / 中相关 | Experiments: data, RL, reward, and tool-augmented systems inform baselines and ablations. |
| 26 | Math-Reasoning | Measuring Mathematical Problem Solving With the MATH Dataset | Dan Hendrycks, Collin Burns, Saurav Kadavath et al. | preprint, 2021 | [link](http://arxiv.org/abs/2103.03874) | 该工作整理数学推理任务、数据集、基准或领域挑战。 / It organizes math reasoning tasks, datasets, benchmarks, or field challenges. | 通过综述、基准构建、数据集设计或多维评测揭示当前模型局限。 / It uses surveys, benchmark construction, dataset design, or multi-dimensional evaluation to reveal model limitations. | Medium / 中相关 | Related Work: surveys and position papers map the field and standard terminology. |
| 27 | Math-Reasoning | Measuring Multimodal Mathematical Reasoning with MATH-Vision Dataset | Ke Wang, Junting Pan, Weikang Shi et al. | Advances in Neural Information Processing Systems, 2024 | [link](https://proceedings.neurips.cc/paper_files/paper/2024/hash/ad0edc7d5fa1a783f063646968b7315b-Abstract-Datasets_and_Benchmarks_Track.html) | 该工作整理数学推理任务、数据集、基准或领域挑战。 / It organizes math reasoning tasks, datasets, benchmarks, or field challenges. | 通过综述、基准构建、数据集设计或多维评测揭示当前模型局限。 / It uses surveys, benchmark construction, dataset design, or multi-dimensional evaluation to reveal model limitations. | Medium / 中相关 | Related Work: surveys and position papers map the field and standard terminology. |
| 28 | Math-Reasoning | MetaMath: Bootstrap Your Own Mathematical Questions for Large Language Models | Longhui Yu, Weisen Jiang, Han Shi et al. | International Conference on Learning Representations, 2024 | [link](https://proceedings.iclr.cc/paper_files/paper/2024/hash/c400474e8a36d0812fdee52739288b12-Abstract-Conference.html) | 该工作研究如何通过数据合成、后训练、奖励模型、强化学习或样本选择提升数学推理表现。 / It studies how data synthesis, post-training, reward modeling, RL, or sample selection improves math reasoning performance. | 构造数学数据、筛选样本、训练奖励/策略模型，或进行数学专门后训练。 / It builds math data, selects samples, trains reward/policy models, or applies math-specific post-training. | Medium / 中相关 | Experiments: data, RL, reward, and tool-augmented systems inform baselines and ablations. |
| 29 | Math-Reasoning | Metacognitive Capabilities of LLMs: An Exploration in Mathematical Problem Solving | Aniket Didolkar, Anirudh Goyal, Nan R. Ke et al. | Advances in Neural Information Processing Systems, 2024 | [link](https://proceedings.neurips.cc/paper_files/paper/2024/hash/2318d75a06437eaa257737a5cf3ab83c-Abstract-Conference.html) | 该工作研究最终答案正确率无法解释中间推理可靠性的问题。 / It addresses why final-answer accuracy cannot diagnose intermediate reasoning reliability. | 使用步骤级反馈、过程监督、验证、错误分类、纠错或元认知评测来分析/改进推理。 / It uses step-level feedback, process supervision, verification, error classification, correction, or metacognitive evaluation. | Strong / 强相关 | Introduction/Experiments: final-answer accuracy is insufficient; process-level reliability must be measured. |
| 30 | Math-Reasoning + Neuro-Symbolic | Neural-Symbolic Architectural Axioms of Integration: A Manifesto | Connor Pryor, Lise Getoor | Conference on Neurosymbolic Learning and Reasoning, 2025 | [link](https://proceedings.mlr.press/v284/pryor25a.html) | 该工作研究 neuro-symbolic 系统的结构、原则、比较维度或可解释性。 / It studies the structure, principles, comparison dimensions, or interpretability of neuro-symbolic systems. | 提出框架、设计原则、比较分析、符号表示或神经符号推理结构。 / It proposes frameworks, design principles, comparative analyses, symbolic representations, or neurosymbolic reasoning structures. | Medium / 中相关 | Method motivation: representation and neural-symbolic interface design are core to reliable reasoning. |
| 31 | Math-Reasoning | PAL: Program-aided Language Models | Luyu Gao, Aman Madaan, Shuyan Zhou et al. | International Conference on Machine Learning, 2023 | [link](https://proceedings.mlr.press/v202/gao23f.html) | 该工作研究 LLM 能提出求解思路但计算/执行不稳定的问题。 / It addresses the gap between LLM-generated solution plans and unreliable computation/execution. | 让 LLM 生成程序、工具调用或可执行中间步骤，并把精确计算交给外部工具。 / It lets LLMs generate programs, tool calls, or executable intermediate steps and delegates exact computation to external tools. | Strong / 强相关 | Method motivation: neural proposal should be separated from symbolic execution and verification. |
| 32 | Math-Reasoning | Position: Formal Mathematical Reasoning—A New Frontier in AI | Kaiyu Yang, Gabriel Poesia, Jingxuan He et al. | International Conference on Machine Learning, 2025 | [link](https://proceedings.mlr.press/v267/yang25az.html) | 该工作研究形式化数学中 proof state、premise/tactic 选择和可验证推理的问题。 / It studies proof states, premise/tactic selection, and verifiable reasoning in formal mathematics. | 用学习模型指导证明搜索、premise retrieval、tactic generation 或形式化验证。 / It uses learned models to guide proof search, premise retrieval, tactic generation, or formal verification. | Strong / 强相关 | Method motivation: mathematical reasoning can be modeled as state/action, premise/tactic, or theorem-model selection. |
| 33 | Math-Reasoning | Premise-Augmented Reasoning Chains Improve Error Identification in Math reasoning with LLMs | Sagnik Mukherjee, Abhinav Chinta, Takyoung Kim et al. | preprint, 2025 | [link](http://arxiv.org/abs/2502.02362) | 该工作研究最终答案正确率无法解释中间推理可靠性的问题。 / It addresses why final-answer accuracy cannot diagnose intermediate reasoning reliability. | 使用步骤级反馈、过程监督、验证、错误分类、纠错或元认知评测来分析/改进推理。 / It uses step-level feedback, process supervision, verification, error classification, correction, or metacognitive evaluation. | Strong / 强相关 | Introduction/Experiments: final-answer accuracy is insufficient; process-level reliability must be measured. |
| 34 | Math-Reasoning | Program of Thoughts Prompting: Disentangling Computation from Reasoning for Numerical Reasoning Tasks | Wenhu Chen, Xueguang Ma, Xinyi Wang et al. | preprint, 2023 | [link](http://arxiv.org/abs/2211.12588) | 该工作研究 LLM 能提出求解思路但计算/执行不稳定的问题。 / It addresses the gap between LLM-generated solution plans and unreliable computation/execution. | 让 LLM 生成程序、工具调用或可执行中间步骤，并把精确计算交给外部工具。 / It lets LLMs generate programs, tool calls, or executable intermediate steps and delegates exact computation to external tools. | Strong / 强相关 | Method motivation: neural proposal should be separated from symbolic execution and verification. |
| 35 | Math-Reasoning | Safe: Enhancing Mathematical Reasoning in Large Language Models via Retrospective Step-aware Formal Verification | Chengwu Liu, Ye Yuan, Yichun Yin et al. | ACL 2025, 2025 | [link](https://aclanthology.org/2025.acl-long.594/) | 该工作研究如何把 LLM 数学推理从纯文本转成可执行、可验证的符号表示。 / It studies how to convert LLM math reasoning from prose into executable and verifiable symbolic representations. | 由 LLM 生成逻辑式、形式语言、符号规则、程序或公式结构，再交给求解器/验证器执行。 / The LLM produces logic forms, formal language, symbolic rules, programs, or formula structures that a solver/verifier executes. | Strong / 强相关 | Method motivation: neural proposal should be separated from symbolic execution and verification. |
| 36 | Math-Reasoning | Specialized Mathematical Solving by a Step-By-Step Expression Chain Generation | Wenqi Zhang, Yongliang Shen, Guiyang Hou et al. | IEEE/ACM Transactions on Audio, Speech, and Language Processing, 2024 | [link](https://ieeexplore.ieee.org/abstract/document/10552332) | 该工作研究如何让 LLM 生成、搜索或组织更好的中间推理路径。 / It studies how LLMs generate, search, or organize better intermediate reasoning paths. | 通过 CoT、路径搜索、提示选择、guided exploration 或多范式推理改进生成式推理。 / It improves generative reasoning through CoT, path search, prompt selection, guided exploration, or multi-paradigm reasoning. | Medium / 中相关 | Introduction: text-chain reasoning improves LLM math but leaves mathematical validity implicit. |
| 37 | Math-Reasoning | Step Guided Reasoning: Improving Mathematical Reasoning using Guidance Generation and Step Reasoning | Lang Cao, Yingtian Zou, Chao Peng et al. | EMNLP 2025, 2025 | [link](https://aclanthology.org/2025.emnlp-main.1068/) | 该工作研究最终答案正确率无法解释中间推理可靠性的问题。 / It addresses why final-answer accuracy cannot diagnose intermediate reasoning reliability. | 使用步骤级反馈、过程监督、验证、错误分类、纠错或元认知评测来分析/改进推理。 / It uses step-level feedback, process supervision, verification, error classification, correction, or metacognitive evaluation. | Strong / 强相关 | Introduction/Experiments: final-answer accuracy is insufficient; process-level reliability must be measured. |
| 38 | Math-Reasoning | Step-KTO: Optimizing Mathematical Reasoning through Stepwise Binary Feedback | Yen-Ting Lin, Di Jin, Tengyu Xu et al. | Proceedings of The 3rd Workshop on Mathematical Natural Language Processing (MathNLP 2025), 2025 | [link](https://aclanthology.org/2025.mathnlp-main.2/) | 该工作研究最终答案正确率无法解释中间推理可靠性的问题。 / It addresses why final-answer accuracy cannot diagnose intermediate reasoning reliability. | 使用步骤级反馈、过程监督、验证、错误分类、纠错或元认知评测来分析/改进推理。 / It uses step-level feedback, process supervision, verification, error classification, correction, or metacognitive evaluation. | Strong / 强相关 | Introduction/Experiments: final-answer accuracy is insufficient; process-level reliability must be measured. |
| 39 | Math-Reasoning | Step-by-Step Correction of LLM-based Math Word Problems Solutions | Yiyao Li, Dhanish Musharraf Ubaidali, Lu Wang et al. | ICASSP 2025 - 2025 IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP), 2025 | [link](https://ieeexplore.ieee.org/abstract/document/10889273) | 该工作研究最终答案正确率无法解释中间推理可靠性的问题。 / It addresses why final-answer accuracy cannot diagnose intermediate reasoning reliability. | 使用步骤级反馈、过程监督、验证、错误分类、纠错或元认知评测来分析/改进推理。 / It uses step-level feedback, process supervision, verification, error classification, correction, or metacognitive evaluation. | Strong / 强相关 | Introduction/Experiments: final-answer accuracy is insufficient; process-level reliability must be measured. |
| 40 | Math-Reasoning | Tree of Thoughts: Deliberate Problem Solving with Large Language Models | Shunyu Yao, Dian Yu, Jeffrey Zhao et al. | Advances in Neural Information Processing Systems, 2023 | [link](https://proceedings.neurips.cc/paper/2023/hash/271db9922b8d1f4dd7aaef84ed5ac703-Abstract.html) | 该工作研究如何让 LLM 生成、搜索或组织更好的中间推理路径。 / It studies how LLMs generate, search, or organize better intermediate reasoning paths. | 通过 CoT、路径搜索、提示选择、guided exploration 或多范式推理改进生成式推理。 / It improves generative reasoning through CoT, path search, prompt selection, guided exploration, or multi-paradigm reasoning. | Medium / 中相关 | Introduction: text-chain reasoning improves LLM math but leaves mathematical validity implicit. |
| 41 | Math-Reasoning | UDfSolver : Uniform representation and decoupled inference strategy for text-diagram function problems solving | Feng Xiong, Xinguo Yu, Litian Huang et al. | Expert Systems with Applications, 2026 | [link](https://www.sciencedirect.com/science/article/pii/S095741742602138X) | 该工作是 EGR 作者前序图文函数题求解方向，帮助界定连续性与差异。 / It is prior work on text-diagram function problem solving and helps define continuity and difference for EGR. | 通过统一表示和解耦推理处理函数类题目。 / It solves function problems through uniform representation and decoupled inference. | Strong / 强相关 | Related Work: prior text-diagram/function solvers clarify EGR continuity and novelty. |
| 42 | Math-Reasoning | What Do Learning Dynamics Reveal About Generalization in LLM Mathematical Reasoning? | Katie Kang, Amrith Setlur, Dibya Ghosh et al. | International Conference on Machine Learning, 2025 | [link](https://proceedings.mlr.press/v267/kang25f.html) | 该工作研究如何通过数据合成、后训练、奖励模型、强化学习或样本选择提升数学推理表现。 / It studies how data synthesis, post-training, reward modeling, RL, or sample selection improves math reasoning performance. | 构造数学数据、筛选样本、训练奖励/策略模型，或进行数学专门后训练。 / It builds math data, selects samples, trains reward/policy models, or applies math-specific post-training. | Medium / 中相关 | Experiments: data, RL, reward, and tool-augmented systems inform baselines and ablations. |
| 43 | Math-Reasoning | WizardMath: Empowering Mathematical Reasoning for Large Language Models via Reinforced Evol-Instruct | Haipeng Luo, Qingfeng Sun, Can Xu et al. | preprint, 2025 | [link](http://arxiv.org/abs/2308.09583) | 该工作研究如何通过数据合成、后训练、奖励模型、强化学习或样本选择提升数学推理表现。 / It studies how data synthesis, post-training, reward modeling, RL, or sample selection improves math reasoning performance. | 构造数学数据、筛选样本、训练奖励/策略模型，或进行数学专门后训练。 / It builds math data, selects samples, trains reward/policy models, or applies math-specific post-training. | Medium / 中相关 | Experiments: data, RL, reward, and tool-augmented systems inform baselines and ablations. |
| 44 | Math-Reasoning | rStar-Math: Small LLMs Can Master Math Reasoning with Self-Evolved Deep Thinking | Xinyu Guan, Li Lyna Zhang, Yifei Liu et al. | International Conference on Machine Learning, 2025 | [link](https://proceedings.mlr.press/v267/guan25f.html) | 该工作研究如何通过数据合成、后训练、奖励模型、强化学习或样本选择提升数学推理表现。 / It studies how data synthesis, post-training, reward modeling, RL, or sample selection improves math reasoning performance. | 构造数学数据、筛选样本、训练奖励/策略模型，或进行数学专门后训练。 / It builds math data, selects samples, trains reward/policy models, or applies math-specific post-training. | Medium / 中相关 | Experiments: data, RL, reward, and tool-augmented systems inform baselines and ablations. |
| 45 | Neuro-Symbolic | A Comparative Study of Neurosymbolic AI Approaches to Interpretable Logical Reasoning | Michael K. Chen | Conference on Neurosymbolic Learning and Reasoning, 2025 | [link](https://proceedings.mlr.press/v284/chen25b.html) | 该工作研究 neuro-symbolic 系统的结构、原则、比较维度或可解释性。 / It studies the structure, principles, comparison dimensions, or interpretability of neuro-symbolic systems. | 提出框架、设计原则、比较分析、符号表示或神经符号推理结构。 / It proposes frameworks, design principles, comparative analyses, symbolic representations, or neurosymbolic reasoning structures. | Medium / 中相关 | Method motivation: representation and neural-symbolic interface design are core to reliable reasoning. |
| 46 | Neuro-Symbolic | A Neuro-Symbolic Approach for Reliable Proof Generation with LLMs: A Case Study in Euclidean Geometry | Oren Sultan, Eitan Stern, Dafna Shahaf | preprint, 2026 | [link](http://arxiv.org/abs/2505.14479) | 该工作研究几何或奥林匹克几何中的神经符号推理和可验证证明。 / It studies neural-symbolic reasoning and verifiable proof in geometry or Olympiad geometry. | 用神经模型指导构造、搜索或证明，由符号几何引擎完成推理验证。 / It uses neural models to guide construction, search, or proof, while a symbolic geometry engine verifies reasoning. | Strong / 强相关 | Introduction/Related Work: geometry and theorem proving validate state-conditioned neural-symbolic reasoning. |
| 47 | Neuro-Symbolic | AXIOM: A Trust-First Neuro-Symbolic Execution Architecture for Verifiable Mathematical Reasoning | Alessio Bruno | preprint, 2026 | [link](http://arxiv.org/abs/2606.00671) | 该工作研究如何把 LLM 数学推理从纯文本转成可执行、可验证的符号表示。 / It studies how to convert LLM math reasoning from prose into executable and verifiable symbolic representations. | 由 LLM 生成逻辑式、形式语言、符号规则、程序或公式结构，再交给求解器/验证器执行。 / The LLM produces logic forms, formal language, symbolic rules, programs, or formula structures that a solver/verifier executes. | Strong / 强相关 | Method motivation: neural proposal should be separated from symbolic execution and verification. |
| 48 | Neuro-Symbolic | Advanced Weakly-Supervised Formula Exploration for Neuro-Symbolic Mathematical Reasoning | Yuxuan Wu, Hideki Nakayama | preprint, 2025 | [link](http://arxiv.org/abs/2502.00629) | 该工作研究如何把 LLM 数学推理从纯文本转成可执行、可验证的符号表示。 / It studies how to convert LLM math reasoning from prose into executable and verifiable symbolic representations. | 由 LLM 生成逻辑式、形式语言、符号规则、程序或公式结构，再交给求解器/验证器执行。 / The LLM produces logic forms, formal language, symbolic rules, programs, or formula structures that a solver/verifier executes. | Strong / 强相关 | Method motivation: neural proposal should be separated from symbolic execution and verification. |
| 49 | Neuro-Symbolic | Artificial Intelligence for Mathematical Reasoning: An Integrated Survey of Language Models, Neuro-symbolic Systems, and Verified Discovery | Syed Rifat Raiyan, Mohsinul Kabir, Hasan Mahmud et al. | preprint, 2026 | [link](http://arxiv.org/abs/2606.08728) | 该工作整理数学推理任务、数据集、基准或领域挑战。 / It organizes math reasoning tasks, datasets, benchmarks, or field challenges. | 通过综述、基准构建、数据集设计或多维评测揭示当前模型局限。 / It uses surveys, benchmark construction, dataset design, or multi-dimensional evaluation to reveal model limitations. | Medium / 中相关 | Related Work: surveys and position papers map the field and standard terminology. |
| 50 | Neuro-Symbolic | Evaluating Neuro-Symbolic AI Architectures: Design Principles, Qualitative Benchmark, Comparative Analysis and Results | Oualid Bougzime, Samir Jabbar, Christophe Cruz et al. | Conference on Neurosymbolic Learning and Reasoning, 2025 | [link](https://proceedings.mlr.press/v284/bougzime25a.html) | 该工作研究 neuro-symbolic 系统的结构、原则、比较维度或可解释性。 / It studies the structure, principles, comparison dimensions, or interpretability of neuro-symbolic systems. | 提出框架、设计原则、比较分析、符号表示或神经符号推理结构。 / It proposes frameworks, design principles, comparative analyses, symbolic representations, or neurosymbolic reasoning structures. | Medium / 中相关 | Method motivation: representation and neural-symbolic interface design are core to reliable reasoning. |
| 51 | Neuro-Symbolic | Gold-medalist Performance in Solving Olympiad Geometry with AlphaGeometry2 | Yuri Chervonyi, Trieu H. Trinh, Miroslav Olšák et al. | Journal of Machine Learning Research, 2025 | [link](http://jmlr.org/papers/v26/25-1654.html) | 该工作研究几何或奥林匹克几何中的神经符号推理和可验证证明。 / It studies neural-symbolic reasoning and verifiable proof in geometry or Olympiad geometry. | 用神经模型指导构造、搜索或证明，由符号几何引擎完成推理验证。 / It uses neural models to guide construction, search, or proof, while a symbolic geometry engine verifies reasoning. | Strong / 强相关 | Introduction/Related Work: geometry and theorem proving validate state-conditioned neural-symbolic reasoning. |
| 52 | Neuro-Symbolic | Improving Rule-based Reasoning in LLMs using Neurosymbolic Representations | Varun Dhanraj, Chris Eliasmith, Christos Christodoulopoulos et al. | EMNLP 2025, 2025 | [link](https://aclanthology.org/2025.emnlp-main.1556/) | 该工作研究 neuro-symbolic 系统的结构、原则、比较维度或可解释性。 / It studies the structure, principles, comparison dimensions, or interpretability of neuro-symbolic systems. | 提出框架、设计原则、比较分析、符号表示或神经符号推理结构。 / It proposes frameworks, design principles, comparative analyses, symbolic representations, or neurosymbolic reasoning structures. | Medium / 中相关 | Method motivation: representation and neural-symbolic interface design are core to reliable reasoning. |
| 53 | Neuro-Symbolic | Intermediate Languages Matter: Formal Languages and LLMs affect Neurosymbolic Reasoning | Alexander Beiser, David Penz, Nysret Musliu | preprint, 2025 | [link](http://arxiv.org/abs/2509.04083) | 该工作研究中间语言、领域知识或表示接口如何影响神经符号推理可靠性。 / It studies how intermediate languages, domain knowledge, or representation interfaces affect neurosymbolic reliability. | 比较形式语言、引入 ontology/领域知识，或分析 LLM 与符号系统之间的表示接口。 / It compares formal languages, introduces ontology/domain knowledge, or analyzes the interface between LLMs and symbolic systems. | Strong / 强相关 | Method motivation: representation and neural-symbolic interface design are core to reliable reasoning. |
| 54 | Neuro-Symbolic | Logic-LM: Empowering Large Language Models with Symbolic Solvers for Faithful Logical Reasoning | Liangming Pan, Alon Albalak, Xinyi Wang et al. | Findings 2023, 2023 | [link](https://aclanthology.org/2023.findings-emnlp.248/) | 该工作研究如何把 LLM 数学推理从纯文本转成可执行、可验证的符号表示。 / It studies how to convert LLM math reasoning from prose into executable and verifiable symbolic representations. | 由 LLM 生成逻辑式、形式语言、符号规则、程序或公式结构，再交给求解器/验证器执行。 / The LLM produces logic forms, formal language, symbolic rules, programs, or formula structures that a solver/verifier executes. | Strong / 强相关 | Method motivation: neural proposal should be separated from symbolic execution and verification. |
| 55 | Neuro-Symbolic | Neural Theorem Proving: Generating and Structuring Proofs for Formal Verification | Balaji Rao, William Eiers, Carlo Lipizzi | Conference on Neurosymbolic Learning and Reasoning, 2025 | [link](https://proceedings.mlr.press/v284/rao25a.html) | 该工作研究形式化数学中 proof state、premise/tactic 选择和可验证推理的问题。 / It studies proof states, premise/tactic selection, and verifiable reasoning in formal mathematics. | 用学习模型指导证明搜索、premise retrieval、tactic generation 或形式化验证。 / It uses learned models to guide proof search, premise retrieval, tactic generation, or formal verification. | Strong / 强相关 | Method motivation: mathematical reasoning can be modeled as state/action, premise/tactic, or theorem-model selection. |
| 56 | Neuro-Symbolic | Neuro-Symbolic AI in 2024: A Systematic Review | Brandon C. Colelough, William Regli | preprint, 2025 | [link](http://arxiv.org/abs/2501.05435) | 该工作研究 neuro-symbolic 系统的结构、原则、比较维度或可解释性。 / It studies the structure, principles, comparison dimensions, or interpretability of neuro-symbolic systems. | 提出框架、设计原则、比较分析、符号表示或神经符号推理结构。 / It proposes frameworks, design principles, comparative analyses, symbolic representations, or neurosymbolic reasoning structures. | Medium / 中相关 | Method motivation: representation and neural-symbolic interface design are core to reliable reasoning. |
| 57 | Neuro-Symbolic | NeuroProlog: Multi-Task Fine-Tuning for Neurosymbolic Mathematical Reasoning via the Cocktail Effect | Pratibha Zunjare, Michael Hsiao | preprint, 2026 | [link](http://arxiv.org/abs/2603.02504) | 该工作研究如何把 LLM 数学推理从纯文本转成可执行、可验证的符号表示。 / It studies how to convert LLM math reasoning from prose into executable and verifiable symbolic representations. | 由 LLM 生成逻辑式、形式语言、符号规则、程序或公式结构，再交给求解器/验证器执行。 / The LLM produces logic forms, formal language, symbolic rules, programs, or formula structures that a solver/verifier executes. | Strong / 强相关 | Method motivation: neural proposal should be separated from symbolic execution and verification. |
| 58 | Neuro-Symbolic | Ontology-Guided Neuro-Symbolic Inference: Grounding Language Models with Mathematical Domain Knowledge | Marcelo Labre | preprint, 2026 | [link](http://arxiv.org/abs/2602.17826) | 该工作研究中间语言、领域知识或表示接口如何影响神经符号推理可靠性。 / It studies how intermediate languages, domain knowledge, or representation interfaces affect neurosymbolic reliability. | 比较形式语言、引入 ontology/领域知识，或分析 LLM 与符号系统之间的表示接口。 / It compares formal languages, introduces ontology/domain knowledge, or analyzes the interface between LLMs and symbolic systems. | Strong / 强相关 | Method motivation: representation and neural-symbolic interface design are core to reliable reasoning. |
| 59 | Neuro-Symbolic | Rethinking Reasoning in LLMs: Neuro-Symbolic Local RetoMaton Beyond CoT and ICL | Rushitha Santhoshi Mamidala, Anshuman Chhabra, Ankur Mali | Conference on Neurosymbolic Learning and Reasoning, 2025 | [link](https://proceedings.mlr.press/v284/mamidala25a.html) | 该工作研究 neuro-symbolic 系统的结构、原则、比较维度或可解释性。 / It studies the structure, principles, comparison dimensions, or interpretability of neuro-symbolic systems. | 提出框架、设计原则、比较分析、符号表示或神经符号推理结构。 / It proposes frameworks, design principles, comparative analyses, symbolic representations, or neurosymbolic reasoning structures. | Medium / 中相关 | Method motivation: representation and neural-symbolic interface design are core to reliable reasoning. |
| 60 | Neuro-Symbolic | Solving Math Word Problems by Combining Language Models With Symbolic Solvers | Joy He-Yueya, Gabriel Poesia, Rose E. Wang et al. | preprint, 2023 | [link](http://arxiv.org/abs/2304.09102) | 该工作研究如何把 LLM 数学推理从纯文本转成可执行、可验证的符号表示。 / It studies how to convert LLM math reasoning from prose into executable and verifiable symbolic representations. | 由 LLM 生成逻辑式、形式语言、符号规则、程序或公式结构，再交给求解器/验证器执行。 / The LLM produces logic forms, formal language, symbolic rules, programs, or formula structures that a solver/verifier executes. | Strong / 强相关 | Method motivation: neural proposal should be separated from symbolic execution and verification. |
| 61 | Neuro-Symbolic | Solving olympiad geometry without human demonstrations | Trieu H. Trinh, Yuhuai Wu, Quoc V. Le et al. | Nature, 2024 | [link](https://www.nature.com/articles/s41586-023-06747-5) | 该工作研究几何或奥林匹克几何中的神经符号推理和可验证证明。 / It studies neural-symbolic reasoning and verifiable proof in geometry or Olympiad geometry. | 用神经模型指导构造、搜索或证明，由符号几何引擎完成推理验证。 / It uses neural models to guide construction, search, or proof, while a symbolic geometry engine verifies reasoning. | Strong / 强相关 | Introduction/Related Work: geometry and theorem proving validate state-conditioned neural-symbolic reasoning. |
| 62 | Neuro-Symbolic | SymCode: A Neurosymbolic Approach to Mathematical Reasoning via Verifiable Code Generation | Sina Bagheri Nezhad, Yao Li, Ameeta Agrawal et al. | Findings 2026, 2026 | [link](https://aclanthology.org/2026.findings-eacl.76/) | 该工作研究如何把 LLM 数学推理从纯文本转成可执行、可验证的符号表示。 / It studies how to convert LLM math reasoning from prose into executable and verifiable symbolic representations. | 由 LLM 生成逻辑式、形式语言、符号规则、程序或公式结构，再交给求解器/验证器执行。 / The LLM produces logic forms, formal language, symbolic rules, programs, or formula structures that a solver/verifier executes. | Strong / 强相关 | Method motivation: neural proposal should be separated from symbolic execution and verification. |
| 63 | Neuro-Symbolic | Toward a Clearer Characterization of Neuro-Symbolic Frameworks: A Brief Comparative Analysis | Sania Sinha, Tanawan Premsri, Parisa Kordjamshidi | Conference on Neurosymbolic Learning and Reasoning, 2025 | [link](https://proceedings.mlr.press/v284/sinha25a.html) | 该工作研究 neuro-symbolic 系统的结构、原则、比较维度或可解释性。 / It studies the structure, principles, comparison dimensions, or interpretability of neuro-symbolic systems. | 提出框架、设计原则、比较分析、符号表示或神经符号推理结构。 / It proposes frameworks, design principles, comparative analyses, symbolic representations, or neurosymbolic reasoning structures. | Medium / 中相关 | Method motivation: representation and neural-symbolic interface design are core to reliable reasoning. |
| 64 | Neuro-Symbolic | Towards Learning to Reason: Comparing LLMs With Neuro-Symbolic on Arithmetic Relations in Abstract Reasoning | Michael Hersche, Giacomo Camposampiero, Roger Wattenhofer et al. | Neurosymbolic Artificial Intelligence, 2026 | [link](https://doi.org/10.1177/29498732261419316) | 该工作研究 neuro-symbolic 系统的结构、原则、比较维度或可解释性。 / It studies the structure, principles, comparison dimensions, or interpretability of neuro-symbolic systems. | 提出框架、设计原则、比较分析、符号表示或神经符号推理结构。 / It proposes frameworks, design principles, comparative analyses, symbolic representations, or neurosymbolic reasoning structures. | Medium / 中相关 | Method motivation: representation and neural-symbolic interface design are core to reliable reasoning. |

## 2. EGR-Oriented Annotated Bibliography / 面向 EGR 的双语条目

### 01. A Survey of Mathematical Reasoning in the Era of Multimodal Large Language Model: Benchmark, Method & Challenges

- Title: A Survey of Mathematical Reasoning in the Era of Multimodal Large Language Model: Benchmark, Method & Challenges
- Authors / 作者: Yibo Yan, Jiamin Su, Jianxiang He, Fangteng Fu, Xu Zheng, Yuanhuiyi Lyu, Kun Wang, Shen Wang et al.
- Venue/Year / 会议年份: Findings 2025, 2025
- Zotero key(s) / Zotero 条目键: `ZH6F95F3`
- Collection / 子集: Math-Reasoning
- Link / 链接: https://aclanthology.org/2025.findings-acl.614/
- Problem: CN: 该工作整理数学推理任务、数据集、基准或领域挑战。 | EN: It organizes math reasoning tasks, datasets, benchmarks, or field challenges.
- Method: CN: 通过综述、基准构建、数据集设计或多维评测揭示当前模型局限。 | EN: It uses surveys, benchmark construction, dataset design, or multi-dimensional evaluation to reveal model limitations.
- Key claim/evidence: CN: 说明数学推理仍是 LLM 的核心挑战，并为 EGR 的问题设定提供背景。 | EN: It shows that mathematical reasoning remains a core challenge and provides background for EGR's problem setting.
- How EGR can cite it: CN: 用于 Introduction/Related Work 的领域背景，尤其是说明为什么仅看最终答案或通用 benchmark 不够。 | EN: Use it as Introduction/Related Work background, especially to explain why final answers or generic benchmarks are insufficient.
- What EGR should learn: CN: EGR 应把 conic-section 写成受控但非平凡的验证场景，并清楚说明评价维度。 | EN: EGR should present conic sections as a controlled but nontrivial testbed and define evaluation dimensions clearly.
- Figure/writing implication: CN: 支持 problem setting 图或 related-work map 的背景层。 | EN: Useful for a problem-setting figure or the background layer of a related-work map.
- Priority: Medium

### 02. AceMath: Advancing Frontier Math Reasoning with Post-Training and Reward Modeling

- Title: AceMath: Advancing Frontier Math Reasoning with Post-Training and Reward Modeling
- Authors / 作者: Zihan Liu, Yang Chen, Mohammad Shoeybi, Bryan Catanzaro, Wei Ping, Wanxiang Che, Joyce Nabende, Ekaterina Shutova et al.
- Venue/Year / 会议年份: Findings 2025, 2025
- Zotero key(s) / Zotero 条目键: `SLMVBR43`
- Collection / 子集: Math-Reasoning
- Link / 链接: https://aclanthology.org/2025.findings-acl.206/
- Problem: CN: 该工作研究如何通过数据合成、后训练、奖励模型、强化学习或样本选择提升数学推理表现。 | EN: It studies how data synthesis, post-training, reward modeling, RL, or sample selection improves math reasoning performance.
- Method: CN: 构造数学数据、筛选样本、训练奖励/策略模型，或进行数学专门后训练。 | EN: It builds math data, selects samples, trains reward/policy models, or applies math-specific post-training.
- Key claim/evidence: CN: 说明 LLM 数学能力持续提升，但这一路线通常不显式建模 theorem selection 与 symbolic execution。 | EN: It shows LLM math ability is improving, but usually without explicit theorem selection and symbolic execution.
- How EGR can cite it: CN: 用于 baseline 与实验背景，避免把 EGR 写成单纯追求 SOTA accuracy 的模型扩展。 | EN: Use it for baselines and experimental context, while avoiding framing EGR as just another accuracy-scaling method.
- What EGR should learn: CN: EGR 可把这些模型作为 backbone/baseline，但核心卖点应是可检查过程和状态转移。 | EN: EGR can use these systems as backbones/baselines, but its core value is checkable process and state transition.
- Figure/writing implication: CN: 放在 related-work map 的 data/RL scaling 区域。 | EN: Place it in the data/RL scaling region of the related-work map.
- Priority: Medium

### 03. Active Prompting with Chain-of-Thought for Large Language Models

- Title: Active Prompting with Chain-of-Thought for Large Language Models
- Authors / 作者: Shizhe Diao, Pengcheng Wang, Yong Lin, Rui Pan, Xiang Liu, Tong Zhang, Lun-Wei Ku, Andre Martins et al.
- Venue/Year / 会议年份: ACL 2024, 2024
- Zotero key(s) / Zotero 条目键: `3CKAMGT2`
- Collection / 子集: Math-Reasoning
- Link / 链接: https://aclanthology.org/2024.acl-long.73/
- Problem: CN: 该工作研究如何让 LLM 生成、搜索或组织更好的中间推理路径。 | EN: It studies how LLMs generate, search, or organize better intermediate reasoning paths.
- Method: CN: 通过 CoT、路径搜索、提示选择、guided exploration 或多范式推理改进生成式推理。 | EN: It improves generative reasoning through CoT, path search, prompt selection, guided exploration, or multi-paradigm reasoning.
- Key claim/evidence: CN: 证明中间推理单元很重要，同时暴露文本 thought 仍不等于可执行数学 action。 | EN: It shows intermediate reasoning units matter, while textual thoughts are still not executable mathematical actions.
- How EGR can cite it: CN: 用于引出 EGR 的范式转向：from next-token/thought generation to next-model transition。 | EN: Use it to motivate EGR's shift from next-token/thought generation to next-model transition.
- What EGR should learn: CN: EGR 应强调自己不是更长 CoT，而是改变了推理单元的类型。 | EN: EGR should stress that it is not longer CoT, but a change in the type of reasoning unit.
- Figure/writing implication: CN: 放在范式对比图左侧：textual reasoning path。 | EN: Place it on the left side of the paradigm figure as textual reasoning paths.
- Priority: Medium

### 04. Augmenting Math Word Problems via Iterative Question Composing

- Title: Augmenting Math Word Problems via Iterative Question Composing
- Authors / 作者: Haoxiong Liu, Yifan Zhang, Yifan Luo, Andrew C. Yao
- Venue/Year / 会议年份: Proceedings of the AAAI Conference on Artificial Intelligence, 2025
- Zotero key(s) / Zotero 条目键: `UMTJUUID`
- Collection / 子集: Math-Reasoning
- Link / 链接: https://ojs.aaai.org/index.php/AAAI/article/view/34640
- Problem: CN: 该工作研究如何通过数据合成、后训练、奖励模型、强化学习或样本选择提升数学推理表现。 | EN: It studies how data synthesis, post-training, reward modeling, RL, or sample selection improves math reasoning performance.
- Method: CN: 构造数学数据、筛选样本、训练奖励/策略模型，或进行数学专门后训练。 | EN: It builds math data, selects samples, trains reward/policy models, or applies math-specific post-training.
- Key claim/evidence: CN: 说明 LLM 数学能力持续提升，但这一路线通常不显式建模 theorem selection 与 symbolic execution。 | EN: It shows LLM math ability is improving, but usually without explicit theorem selection and symbolic execution.
- How EGR can cite it: CN: 用于 baseline 与实验背景，避免把 EGR 写成单纯追求 SOTA accuracy 的模型扩展。 | EN: Use it for baselines and experimental context, while avoiding framing EGR as just another accuracy-scaling method.
- What EGR should learn: CN: EGR 可把这些模型作为 backbone/baseline，但核心卖点应是可检查过程和状态转移。 | EN: EGR can use these systems as backbones/baselines, but its core value is checkable process and state transition.
- Figure/writing implication: CN: 放在 related-work map 的 data/RL scaling 区域。 | EN: Place it in the data/RL scaling region of the related-work map.
- Priority: Medium

### 05. Chain-of-Reasoning: Towards Unified Mathematical Reasoning in Large Language Models via a Multi-Paradigm Perspective

- Title: Chain-of-Reasoning: Towards Unified Mathematical Reasoning in Large Language Models via a Multi-Paradigm Perspective
- Authors / 作者: Yiyao Yu, Yuxiang Zhang, Dongdong Zhang, Xiao Liang, Hengyuan Zhang, Xingxing Zhang, Mahmoud Khademi, Hany Hassan Awadalla et al.
- Venue/Year / 会议年份: ACL 2025, 2025
- Zotero key(s) / Zotero 条目键: `79V7PHHT`
- Collection / 子集: Math-Reasoning
- Link / 链接: https://aclanthology.org/2025.acl-long.1213/
- Problem: CN: 该工作研究如何让 LLM 生成、搜索或组织更好的中间推理路径。 | EN: It studies how LLMs generate, search, or organize better intermediate reasoning paths.
- Method: CN: 通过 CoT、路径搜索、提示选择、guided exploration 或多范式推理改进生成式推理。 | EN: It improves generative reasoning through CoT, path search, prompt selection, guided exploration, or multi-paradigm reasoning.
- Key claim/evidence: CN: 证明中间推理单元很重要，同时暴露文本 thought 仍不等于可执行数学 action。 | EN: It shows intermediate reasoning units matter, while textual thoughts are still not executable mathematical actions.
- How EGR can cite it: CN: 用于引出 EGR 的范式转向：from next-token/thought generation to next-model transition。 | EN: Use it to motivate EGR's shift from next-token/thought generation to next-model transition.
- What EGR should learn: CN: EGR 应强调自己不是更长 CoT，而是改变了推理单元的类型。 | EN: EGR should stress that it is not longer CoT, but a change in the type of reasoning unit.
- Figure/writing implication: CN: 放在范式对比图左侧：textual reasoning path。 | EN: Place it on the left side of the paradigm figure as textual reasoning paths.
- Priority: Medium

### 06. CoMAT: Chain of Mathematically Annotated Thought Improves Mathematical Reasoning

- Title: CoMAT: Chain of Mathematically Annotated Thought Improves Mathematical Reasoning
- Authors / 作者: Joshua Ong Jun Leang, Aryo Pradipta Gema, Shay B. Cohen, Christos Christodoulopoulos, Tanmoy Chakraborty, Carolyn Rose, Violet Peng
- Venue/Year / 会议年份: EMNLP 2025, 2025
- Zotero key(s) / Zotero 条目键: `XW3KDRD4`
- Collection / 子集: Math-Reasoning
- Link / 链接: https://aclanthology.org/2025.emnlp-main.1024/
- Problem: CN: 该工作研究如何把 LLM 数学推理从纯文本转成可执行、可验证的符号表示。 | EN: It studies how to convert LLM math reasoning from prose into executable and verifiable symbolic representations.
- Method: CN: 由 LLM 生成逻辑式、形式语言、符号规则、程序或公式结构，再交给求解器/验证器执行。 | EN: The LLM produces logic forms, formal language, symbolic rules, programs, or formula structures that a solver/verifier executes.
- Key claim/evidence: CN: 支持“神经模型负责提出，符号层负责执行/验证”的分工。 | EN: It supports the division where neural models propose and symbolic modules execute or verify.
- How EGR can cite it: CN: 用于说明 EGR 的 applicator 是可靠推理的核心执行层，而不是事后检查器。 | EN: Use it to argue that EGR's applicator is a core execution layer, not merely a post-hoc checker.
- What EGR should learn: CN: EGR 需要把 theorem model 定义为 precondition + symbolic transition。 | EN: EGR should define theorem models as precondition plus symbolic transition.
- Figure/writing implication: CN: 启发 “selector -> theorem model -> applicator -> new symbolic state” 方法图。 | EN: Useful for the method figure: selector -> theorem model -> applicator -> new symbolic state.
- Priority: High

### 07. CogMath: Assessing LLMs’ Authentic Mathematical Ability from a Human Cognitive Perspective

- Title: CogMath: Assessing LLMs’ Authentic Mathematical Ability from a Human Cognitive Perspective
- Authors / 作者: Jiayu Liu, Zhenya Huang, Wei Dai, Cheng Cheng, Jinze Wu, Jing Sha, Song Li, Qi Liu et al.
- Venue/Year / 会议年份: International Conference on Machine Learning, 2025
- Zotero key(s) / Zotero 条目键: `NQIJFS82`
- Collection / 子集: Math-Reasoning
- Link / 链接: https://proceedings.mlr.press/v267/liu25ab.html
- Problem: CN: 该工作研究最终答案正确率无法解释中间推理可靠性的问题。 | EN: It addresses why final-answer accuracy cannot diagnose intermediate reasoning reliability.
- Method: CN: 使用步骤级反馈、过程监督、验证、错误分类、纠错或元认知评测来分析/改进推理。 | EN: It uses step-level feedback, process supervision, verification, error classification, correction, or metacognitive evaluation.
- Key claim/evidence: CN: 直接支持 EGR 把 selection、applicability、execution、termination、extraction 分开评测。 | EN: It directly supports EGR's separate evaluation of selection, applicability, execution, termination, and extraction.
- How EGR can cite it: CN: 用于证明 EGR 不应只报告 final answer accuracy，而应报告过程级指标和错误归因。 | EN: Use it to justify reporting process-level metrics and failure attribution, not only final answer accuracy.
- What EGR should learn: CN: EGR 的实验应包含 transition-level 诊断，并把失败定位到具体决策。 | EN: EGR experiments should include transition-level diagnosis and attribute failures to specific decisions.
- Figure/writing implication: CN: 启发错误分类图和 process-supervision related-work map。 | EN: Useful for an error-taxonomy figure and a process-supervision related-work map.
- Priority: High

### 08. Diverse Multi-tool Aggregation with Large Language Models for Enhanced Math Reasoning

- Title: Diverse Multi-tool Aggregation with Large Language Models for Enhanced Math Reasoning
- Authors / 作者: Bohan Yao, Vikas Yadav
- Venue/Year / 会议年份: journalArticle, n.d.
- Zotero key(s) / Zotero 条目键: `7YT5H2V6`
- Collection / 子集: Math-Reasoning
- Link / 链接: Zotero metadata incomplete
- Problem: CN: 该工作研究 LLM 能提出求解思路但计算/执行不稳定的问题。 | EN: It addresses the gap between LLM-generated solution plans and unreliable computation/execution.
- Method: CN: 让 LLM 生成程序、工具调用或可执行中间步骤，并把精确计算交给外部工具。 | EN: It lets LLMs generate programs, tool calls, or executable intermediate steps and delegates exact computation to external tools.
- Key claim/evidence: CN: 支持 predict-and-execute 分工，但其执行单元通常是代码或工具而不是 theorem model。 | EN: It supports predict-and-execute, but its execution unit is usually code or tools rather than theorem models.
- How EGR can cite it: CN: 用于把 EGR 定位为 theorem-model execution：不是执行任意代码，而是执行数学定理模型。 | EN: Use it to position EGR as theorem-model execution: executing mathematical theorem models rather than arbitrary code.
- What EGR should learn: CN: EGR 要突出 action space 更数学化、状态更显式、失败更可归因。 | EN: EGR should emphasize a more mathematical action space, explicit state, and clearer failure attribution.
- Figure/writing implication: CN: 适合做 PAL/PoT/tool methods vs EGR 的 comparison table。 | EN: Good for a PAL/PoT/tool methods vs EGR comparison table.
- Priority: Medium

### 09. Empowering Multi-step Reasoning across Languages via Program-Aided Language Models

- Title: Empowering Multi-step Reasoning across Languages via Program-Aided Language Models
- Authors / 作者: Leonardo Ranaldi, Giulia Pucci, Barry Haddow, Alexandra Birch, Yaser Al-Onaizan, Mohit Bansal, Yun-Nung Chen
- Venue/Year / 会议年份: EMNLP 2024, 2024
- Zotero key(s) / Zotero 条目键: `CGJFJTXH`
- Collection / 子集: Math-Reasoning
- Link / 链接: https://aclanthology.org/2024.emnlp-main.678/
- Problem: CN: 该工作研究 LLM 能提出求解思路但计算/执行不稳定的问题。 | EN: It addresses the gap between LLM-generated solution plans and unreliable computation/execution.
- Method: CN: 让 LLM 生成程序、工具调用或可执行中间步骤，并把精确计算交给外部工具。 | EN: It lets LLMs generate programs, tool calls, or executable intermediate steps and delegates exact computation to external tools.
- Key claim/evidence: CN: 支持 predict-and-execute 分工，但其执行单元通常是代码或工具而不是 theorem model。 | EN: It supports predict-and-execute, but its execution unit is usually code or tools rather than theorem models.
- How EGR can cite it: CN: 用于把 EGR 定位为 theorem-model execution：不是执行任意代码，而是执行数学定理模型。 | EN: Use it to position EGR as theorem-model execution: executing mathematical theorem models rather than arbitrary code.
- What EGR should learn: CN: EGR 要突出 action space 更数学化、状态更显式、失败更可归因。 | EN: EGR should emphasize a more mathematical action space, explicit state, and clearer failure attribution.
- Figure/writing implication: CN: 适合做 PAL/PoT/tool methods vs EGR 的 comparison table。 | EN: Good for a PAL/PoT/tool methods vs EGR comparison table.
- Priority: Medium

### 10. Enhancing Mathematical Reasoning in LLMs by Stepwise Correction

- Title: Enhancing Mathematical Reasoning in LLMs by Stepwise Correction
- Authors / 作者: Zhenyu Wu, Qingkai Zeng, Zhihan Zhang, Zhaoxuan Tan, Chao Shen, Meng Jiang, Wanxiang Che, Joyce Nabende et al.
- Venue/Year / 会议年份: ACL 2025, 2025
- Zotero key(s) / Zotero 条目键: `59SU9ZNS`
- Collection / 子集: Math-Reasoning
- Link / 链接: https://aclanthology.org/2025.acl-long.1048/
- Problem: CN: 该工作研究最终答案正确率无法解释中间推理可靠性的问题。 | EN: It addresses why final-answer accuracy cannot diagnose intermediate reasoning reliability.
- Method: CN: 使用步骤级反馈、过程监督、验证、错误分类、纠错或元认知评测来分析/改进推理。 | EN: It uses step-level feedback, process supervision, verification, error classification, correction, or metacognitive evaluation.
- Key claim/evidence: CN: 直接支持 EGR 把 selection、applicability、execution、termination、extraction 分开评测。 | EN: It directly supports EGR's separate evaluation of selection, applicability, execution, termination, and extraction.
- How EGR can cite it: CN: 用于证明 EGR 不应只报告 final answer accuracy，而应报告过程级指标和错误归因。 | EN: Use it to justify reporting process-level metrics and failure attribution, not only final answer accuracy.
- What EGR should learn: CN: EGR 的实验应包含 transition-level 诊断，并把失败定位到具体决策。 | EN: EGR experiments should include transition-level diagnosis and attribute failures to specific decisions.
- Figure/writing implication: CN: 启发错误分类图和 process-supervision related-work map。 | EN: Useful for an error-taxonomy figure and a process-supervision related-work map.
- Priority: High

### 11. Error Classification of Large Language Models on Math Word Problems: A Dynamically Adaptive Framework

- Title: Error Classification of Large Language Models on Math Word Problems: A Dynamically Adaptive Framework
- Authors / 作者: Zhangyue Yin, Yuhong Sun, Xuanjing Huang, Xipeng Qiu, Hui Zhao
- Venue/Year / 会议年份: journalArticle, n.d.
- Zotero key(s) / Zotero 条目键: `X67RQWLU`
- Collection / 子集: Math-Reasoning
- Link / 链接: Zotero metadata incomplete
- Problem: CN: 该工作研究最终答案正确率无法解释中间推理可靠性的问题。 | EN: It addresses why final-answer accuracy cannot diagnose intermediate reasoning reliability.
- Method: CN: 使用步骤级反馈、过程监督、验证、错误分类、纠错或元认知评测来分析/改进推理。 | EN: It uses step-level feedback, process supervision, verification, error classification, correction, or metacognitive evaluation.
- Key claim/evidence: CN: 直接支持 EGR 把 selection、applicability、execution、termination、extraction 分开评测。 | EN: It directly supports EGR's separate evaluation of selection, applicability, execution, termination, and extraction.
- How EGR can cite it: CN: 用于证明 EGR 不应只报告 final answer accuracy，而应报告过程级指标和错误归因。 | EN: Use it to justify reporting process-level metrics and failure attribution, not only final answer accuracy.
- What EGR should learn: CN: EGR 的实验应包含 transition-level 诊断，并把失败定位到具体决策。 | EN: EGR experiments should include transition-level diagnosis and attribute failures to specific decisions.
- Figure/writing implication: CN: 启发错误分类图和 process-supervision related-work map。 | EN: Useful for an error-taxonomy figure and a process-supervision related-work map.
- Priority: High

### 12. FLAIR: Steering LLM Mathematical Problem Solving based on A Fuzzy-Logic-AssIsted Reasoner

- Title: FLAIR: Steering LLM Mathematical Problem Solving based on A Fuzzy-Logic-AssIsted Reasoner
- Authors / 作者: Hao Wu, Hongru Sun, Wanqing Li, Xinguo Yu, Hao Ming, Xiao Luo, Wenbin Zhang, Jiahong Zhao et al.
- Venue/Year / 会议年份: ACL 2026, 2026
- Zotero key(s) / Zotero 条目键: `NMI988FA`
- Collection / 子集: Math-Reasoning
- Link / 链接: https://aclanthology.org/2026.acl-long.1790/
- Problem: CN: 该工作研究如何把 LLM 数学推理从纯文本转成可执行、可验证的符号表示。 | EN: It studies how to convert LLM math reasoning from prose into executable and verifiable symbolic representations.
- Method: CN: 由 LLM 生成逻辑式、形式语言、符号规则、程序或公式结构，再交给求解器/验证器执行。 | EN: The LLM produces logic forms, formal language, symbolic rules, programs, or formula structures that a solver/verifier executes.
- Key claim/evidence: CN: 支持“神经模型负责提出，符号层负责执行/验证”的分工。 | EN: It supports the division where neural models propose and symbolic modules execute or verify.
- How EGR can cite it: CN: 用于说明 EGR 的 applicator 是可靠推理的核心执行层，而不是事后检查器。 | EN: Use it to argue that EGR's applicator is a core execution layer, not merely a post-hoc checker.
- What EGR should learn: CN: EGR 需要把 theorem model 定义为 precondition + symbolic transition。 | EN: EGR should define theorem models as precondition plus symbolic transition.
- Figure/writing implication: CN: 启发 “selector -> theorem model -> applicator -> new symbolic state” 方法图。 | EN: Useful for the method figure: selector -> theorem model -> applicator -> new symbolic state.
- Priority: High

### 13. Fewer is More: Boosting Math Reasoning with Reinforced Context Pruning

- Title: Fewer is More: Boosting Math Reasoning with Reinforced Context Pruning
- Authors / 作者: Xijie Huang, Li Lyna Zhang, Kwang-Ting Cheng, Fan Yang, Mao Yang, Yaser Al-Onaizan, Mohit Bansal, Yun-Nung Chen
- Venue/Year / 会议年份: EMNLP 2024, 2024
- Zotero key(s) / Zotero 条目键: `DMJCNYPH`
- Collection / 子集: Math-Reasoning
- Link / 链接: https://aclanthology.org/2024.emnlp-main.758/
- Problem: CN: 该工作研究如何通过数据合成、后训练、奖励模型、强化学习或样本选择提升数学推理表现。 | EN: It studies how data synthesis, post-training, reward modeling, RL, or sample selection improves math reasoning performance.
- Method: CN: 构造数学数据、筛选样本、训练奖励/策略模型，或进行数学专门后训练。 | EN: It builds math data, selects samples, trains reward/policy models, or applies math-specific post-training.
- Key claim/evidence: CN: 说明 LLM 数学能力持续提升，但这一路线通常不显式建模 theorem selection 与 symbolic execution。 | EN: It shows LLM math ability is improving, but usually without explicit theorem selection and symbolic execution.
- How EGR can cite it: CN: 用于 baseline 与实验背景，避免把 EGR 写成单纯追求 SOTA accuracy 的模型扩展。 | EN: Use it for baselines and experimental context, while avoiding framing EGR as just another accuracy-scaling method.
- What EGR should learn: CN: EGR 可把这些模型作为 backbone/baseline，但核心卖点应是可检查过程和状态转移。 | EN: EGR can use these systems as backbones/baselines, but its core value is checkable process and state transition.
- Figure/writing implication: CN: 放在 related-work map 的 data/RL scaling 区域。 | EN: Place it in the data/RL scaling region of the related-work map.
- Priority: Medium

### 14. Forward-Backward Reasoning in Large Language Models for Mathematical Verification

- Title: Forward-Backward Reasoning in Large Language Models for Mathematical Verification
- Authors / 作者: Weisen Jiang, Han Shi, Longhui Yu, Zhengying Liu, Yu Zhang, Zhenguo Li, James Kwok, Lun-Wei Ku et al.
- Venue/Year / 会议年份: Findings 2024, 2024
- Zotero key(s) / Zotero 条目键: `A53BDS2C`
- Collection / 子集: Math-Reasoning
- Link / 链接: https://aclanthology.org/2024.findings-acl.397/
- Problem: CN: 该工作研究最终答案正确率无法解释中间推理可靠性的问题。 | EN: It addresses why final-answer accuracy cannot diagnose intermediate reasoning reliability.
- Method: CN: 使用步骤级反馈、过程监督、验证、错误分类、纠错或元认知评测来分析/改进推理。 | EN: It uses step-level feedback, process supervision, verification, error classification, correction, or metacognitive evaluation.
- Key claim/evidence: CN: 直接支持 EGR 把 selection、applicability、execution、termination、extraction 分开评测。 | EN: It directly supports EGR's separate evaluation of selection, applicability, execution, termination, and extraction.
- How EGR can cite it: CN: 用于证明 EGR 不应只报告 final answer accuracy，而应报告过程级指标和错误归因。 | EN: Use it to justify reporting process-level metrics and failure attribution, not only final answer accuracy.
- What EGR should learn: CN: EGR 的实验应包含 transition-level 诊断，并把失败定位到具体决策。 | EN: EGR experiments should include transition-level diagnosis and attribute failures to specific decisions.
- Figure/writing implication: CN: 启发错误分类图和 process-supervision related-work map。 | EN: Useful for an error-taxonomy figure and a process-supervision related-work map.
- Priority: High

### 15. GRPO-LEAD: A Difficulty-Aware Reinforcement Learning Approach for Concise Mathematical Reasoning in Language Models

- Title: GRPO-LEAD: A Difficulty-Aware Reinforcement Learning Approach for Concise Mathematical Reasoning in Language Models
- Authors / 作者: Jixiao Zhang, Chunsheng Zuo, Christos Christodoulopoulos, Tanmoy Chakraborty, Carolyn Rose, Violet Peng
- Venue/Year / 会议年份: EMNLP 2025, 2025
- Zotero key(s) / Zotero 条目键: `KKNXNMWD`
- Collection / 子集: Math-Reasoning
- Link / 链接: https://aclanthology.org/2025.emnlp-main.287/
- Problem: CN: 该工作研究如何通过数据合成、后训练、奖励模型、强化学习或样本选择提升数学推理表现。 | EN: It studies how data synthesis, post-training, reward modeling, RL, or sample selection improves math reasoning performance.
- Method: CN: 构造数学数据、筛选样本、训练奖励/策略模型，或进行数学专门后训练。 | EN: It builds math data, selects samples, trains reward/policy models, or applies math-specific post-training.
- Key claim/evidence: CN: 说明 LLM 数学能力持续提升，但这一路线通常不显式建模 theorem selection 与 symbolic execution。 | EN: It shows LLM math ability is improving, but usually without explicit theorem selection and symbolic execution.
- How EGR can cite it: CN: 用于 baseline 与实验背景，避免把 EGR 写成单纯追求 SOTA accuracy 的模型扩展。 | EN: Use it for baselines and experimental context, while avoiding framing EGR as just another accuracy-scaling method.
- What EGR should learn: CN: EGR 可把这些模型作为 backbone/baseline，但核心卖点应是可检查过程和状态转移。 | EN: EGR can use these systems as backbones/baselines, but its core value is checkable process and state transition.
- Figure/writing implication: CN: 放在 related-work map 的 data/RL scaling 区域。 | EN: Place it in the data/RL scaling region of the related-work map.
- Priority: Medium

### 16. Key-Point-Driven Data Synthesis with Its Enhancement on Mathematical Reasoning

- Title: Key-Point-Driven Data Synthesis with Its Enhancement on Mathematical Reasoning
- Authors / 作者: Yiming Huang, Xiao Liu, Yeyun Gong, Zhibin Gou, Yelong Shen, Nan Duan, Weizhu Chen
- Venue/Year / 会议年份: Proceedings of the AAAI Conference on Artificial Intelligence, 2025
- Zotero key(s) / Zotero 条目键: `2HFHGWSK`
- Collection / 子集: Math-Reasoning
- Link / 链接: https://ojs.aaai.org/index.php/AAAI/article/view/34593
- Problem: CN: 该工作研究如何通过数据合成、后训练、奖励模型、强化学习或样本选择提升数学推理表现。 | EN: It studies how data synthesis, post-training, reward modeling, RL, or sample selection improves math reasoning performance.
- Method: CN: 构造数学数据、筛选样本、训练奖励/策略模型，或进行数学专门后训练。 | EN: It builds math data, selects samples, trains reward/policy models, or applies math-specific post-training.
- Key claim/evidence: CN: 说明 LLM 数学能力持续提升，但这一路线通常不显式建模 theorem selection 与 symbolic execution。 | EN: It shows LLM math ability is improving, but usually without explicit theorem selection and symbolic execution.
- How EGR can cite it: CN: 用于 baseline 与实验背景，避免把 EGR 写成单纯追求 SOTA accuracy 的模型扩展。 | EN: Use it for baselines and experimental context, while avoiding framing EGR as just another accuracy-scaling method.
- What EGR should learn: CN: EGR 可把这些模型作为 backbone/baseline，但核心卖点应是可检查过程和状态转移。 | EN: EGR can use these systems as backbones/baselines, but its core value is checkable process and state transition.
- Figure/writing implication: CN: 放在 related-work map 的 data/RL scaling 区域。 | EN: Place it in the data/RL scaling region of the related-work map.
- Priority: Medium

### 17. Knowledge-Centered Dual-Process Reasoning for Math Word Problems With Large Language Models

- Title: Knowledge-Centered Dual-Process Reasoning for Math Word Problems With Large Language Models
- Authors / 作者: Jiayu Liu, Zhenya Huang, Qi Liu, Zhiyuan Ma, Chengxiang Zhai, Enhong Chen
- Venue/Year / 会议年份: IEEE Transactions on Knowledge and Data Engineering, 2025
- Zotero key(s) / Zotero 条目键: `D44U5NQ7`
- Collection / 子集: Math-Reasoning
- Link / 链接: https://ieeexplore.ieee.org/abstract/document/10946242
- Problem: CN: 该工作研究如何让 LLM 生成、搜索或组织更好的中间推理路径。 | EN: It studies how LLMs generate, search, or organize better intermediate reasoning paths.
- Method: CN: 通过 CoT、路径搜索、提示选择、guided exploration 或多范式推理改进生成式推理。 | EN: It improves generative reasoning through CoT, path search, prompt selection, guided exploration, or multi-paradigm reasoning.
- Key claim/evidence: CN: 证明中间推理单元很重要，同时暴露文本 thought 仍不等于可执行数学 action。 | EN: It shows intermediate reasoning units matter, while textual thoughts are still not executable mathematical actions.
- How EGR can cite it: CN: 用于引出 EGR 的范式转向：from next-token/thought generation to next-model transition。 | EN: Use it to motivate EGR's shift from next-token/thought generation to next-model transition.
- What EGR should learn: CN: EGR 应强调自己不是更长 CoT，而是改变了推理单元的类型。 | EN: EGR should stress that it is not longer CoT, but a change in the type of reasoning unit.
- Figure/writing implication: CN: 放在范式对比图左侧：textual reasoning path。 | EN: Place it on the left side of the paradigm figure as textual reasoning paths.
- Priority: Medium

### 18. LLMs can Find Mathematical Reasoning Mistakes by Pedagogical Chain-of-Thought

- Title: LLMs can Find Mathematical Reasoning Mistakes by Pedagogical Chain-of-Thought
- Authors / 作者: Zhuoxuan Jiang, Haoyuan Peng, Shanshan Feng, Fan Li, Dongsheng Li
- Venue/Year / 会议年份: preprint, 2025
- Zotero key(s) / Zotero 条目键: `P993QP49`
- Collection / 子集: Math-Reasoning
- Link / 链接: http://arxiv.org/abs/2405.06705
- Problem: CN: 该工作研究最终答案正确率无法解释中间推理可靠性的问题。 | EN: It addresses why final-answer accuracy cannot diagnose intermediate reasoning reliability.
- Method: CN: 使用步骤级反馈、过程监督、验证、错误分类、纠错或元认知评测来分析/改进推理。 | EN: It uses step-level feedback, process supervision, verification, error classification, correction, or metacognitive evaluation.
- Key claim/evidence: CN: 直接支持 EGR 把 selection、applicability、execution、termination、extraction 分开评测。 | EN: It directly supports EGR's separate evaluation of selection, applicability, execution, termination, and extraction.
- How EGR can cite it: CN: 用于证明 EGR 不应只报告 final answer accuracy，而应报告过程级指标和错误归因。 | EN: Use it to justify reporting process-level metrics and failure attribution, not only final answer accuracy.
- What EGR should learn: CN: EGR 的实验应包含 transition-level 诊断，并把失败定位到具体决策。 | EN: EGR experiments should include transition-level diagnosis and attribute failures to specific decisions.
- Figure/writing implication: CN: 启发错误分类图和 process-supervision related-work map。 | EN: Useful for an error-taxonomy figure and a process-supervision related-work map.
- Priority: High

### 19. LeanDojo: Theorem Proving with Retrieval-Augmented Language Models

- Title: LeanDojo: Theorem Proving with Retrieval-Augmented Language Models
- Authors / 作者: Kaiyu Yang, Aidan Swope, Alex Gu, Rahul Chalamala, Peiyang Song, Shixing Yu, Saad Godil, Ryan J. Prenger et al.
- Venue/Year / 会议年份: Advances in Neural Information Processing Systems, 2023
- Zotero key(s) / Zotero 条目键: `NDL89MZG`
- Collection / 子集: Math-Reasoning + Neuro-Symbolic
- Link / 链接: https://proceedings.neurips.cc/paper_files/paper/2023/hash/4441469427094f8873d0fecb0c4e1cee-Abstract-Datasets_and_Benchmarks.html
- Problem: CN: 该工作研究形式化数学中 proof state、premise/tactic 选择和可验证推理的问题。 | EN: It studies proof states, premise/tactic selection, and verifiable reasoning in formal mathematics.
- Method: CN: 用学习模型指导证明搜索、premise retrieval、tactic generation 或形式化验证。 | EN: It uses learned models to guide proof search, premise retrieval, tactic generation, or formal verification.
- Key claim/evidence: CN: 支持把数学推理写成状态空间中的动作选择，而不是一次性答案预测。 | EN: It supports writing mathematical reasoning as action selection in a state space, not one-shot answer prediction.
- How EGR can cite it: CN: 用于支撑 EGR 的 `P(M_t | S_t)` 选择器和 theorem-model trajectory 表述。 | EN: Use it to support EGR's `P(M_t | S_t)` selector and theorem-model trajectory formulation.
- What EGR should learn: CN: EGR 应借用 state/action/search 的严谨语言，但避免声称自己是通用 theorem prover。 | EN: EGR should borrow the rigorous language of state/action/search while avoiding the claim of being a general theorem prover.
- Figure/writing implication: CN: 适合与 EGR 的 theorem-action trajectory 放在同一对比图。 | EN: Good for a comparison figure with EGR's theorem-action trajectory.
- Priority: High

### 20. Learning to Reason Deductively: Math Word Problem Solving as Complex Relation Extraction

- Title: Learning to Reason Deductively: Math Word Problem Solving as Complex Relation Extraction
- Authors / 作者: Zhanming Jie, Jierui Li, Wei Lu, Smaranda Muresan, Preslav Nakov, Aline Villavicencio
- Venue/Year / 会议年份: ACL 2022, 2022
- Zotero key(s) / Zotero 条目键: `5AZYWK5Y`
- Collection / 子集: Math-Reasoning
- Link / 链接: https://aclanthology.org/2022.acl-long.410/
- Problem: CN: 该工作研究如何把 LLM 数学推理从纯文本转成可执行、可验证的符号表示。 | EN: It studies how to convert LLM math reasoning from prose into executable and verifiable symbolic representations.
- Method: CN: 由 LLM 生成逻辑式、形式语言、符号规则、程序或公式结构，再交给求解器/验证器执行。 | EN: The LLM produces logic forms, formal language, symbolic rules, programs, or formula structures that a solver/verifier executes.
- Key claim/evidence: CN: 支持“神经模型负责提出，符号层负责执行/验证”的分工。 | EN: It supports the division where neural models propose and symbolic modules execute or verify.
- How EGR can cite it: CN: 用于说明 EGR 的 applicator 是可靠推理的核心执行层，而不是事后检查器。 | EN: Use it to argue that EGR's applicator is a core execution layer, not merely a post-hoc checker.
- What EGR should learn: CN: EGR 需要把 theorem model 定义为 precondition + symbolic transition。 | EN: EGR should define theorem models as precondition plus symbolic transition.
- Figure/writing implication: CN: 启发 “selector -> theorem model -> applicator -> new symbolic state” 方法图。 | EN: Useful for the method figure: selector -> theorem model -> applicator -> new symbolic state.
- Priority: Medium

### 21. Let's Reason Formally: Natural-Formal Hybrid Reasoning Enhances LLM's Math Capability

- Title: Let's Reason Formally: Natural-Formal Hybrid Reasoning Enhances LLM's Math Capability
- Authors / 作者: Ruida Wang, Yuxin Li, Yi R. Fung, Tong Zhang, Christos Christodoulopoulos, Tanmoy Chakraborty, Carolyn Rose, Violet Peng
- Venue/Year / 会议年份: EMNLP 2025, 2025
- Zotero key(s) / Zotero 条目键: `UMFBQ2IA`
- Collection / 子集: Math-Reasoning
- Link / 链接: https://aclanthology.org/2025.emnlp-main.850/
- Problem: CN: 该工作研究如何把 LLM 数学推理从纯文本转成可执行、可验证的符号表示。 | EN: It studies how to convert LLM math reasoning from prose into executable and verifiable symbolic representations.
- Method: CN: 由 LLM 生成逻辑式、形式语言、符号规则、程序或公式结构，再交给求解器/验证器执行。 | EN: The LLM produces logic forms, formal language, symbolic rules, programs, or formula structures that a solver/verifier executes.
- Key claim/evidence: CN: 支持“神经模型负责提出，符号层负责执行/验证”的分工。 | EN: It supports the division where neural models propose and symbolic modules execute or verify.
- How EGR can cite it: CN: 用于说明 EGR 的 applicator 是可靠推理的核心执行层，而不是事后检查器。 | EN: Use it to argue that EGR's applicator is a core execution layer, not merely a post-hoc checker.
- What EGR should learn: CN: EGR 需要把 theorem model 定义为 precondition + symbolic transition。 | EN: EGR should define theorem models as precondition plus symbolic transition.
- Figure/writing implication: CN: 启发 “selector -> theorem model -> applicator -> new symbolic state” 方法图。 | EN: Useful for the method figure: selector -> theorem model -> applicator -> new symbolic state.
- Priority: High

### 22. MARGE: Improving Math Reasoning with Guided Exploration

- Title: MARGE: Improving Math Reasoning with Guided Exploration
- Authors / 作者: Jingyue Gao, Runji Lin, Keming Lu, Bowen Yu, Junyang Lin, Jianyu Chen
- Venue/Year / 会议年份: International Conference on Machine Learning, 2025
- Zotero key(s) / Zotero 条目键: `KC3L639T`
- Collection / 子集: Math-Reasoning
- Link / 链接: https://proceedings.mlr.press/v267/gao25h.html
- Problem: CN: 该工作研究如何让 LLM 生成、搜索或组织更好的中间推理路径。 | EN: It studies how LLMs generate, search, or organize better intermediate reasoning paths.
- Method: CN: 通过 CoT、路径搜索、提示选择、guided exploration 或多范式推理改进生成式推理。 | EN: It improves generative reasoning through CoT, path search, prompt selection, guided exploration, or multi-paradigm reasoning.
- Key claim/evidence: CN: 证明中间推理单元很重要，同时暴露文本 thought 仍不等于可执行数学 action。 | EN: It shows intermediate reasoning units matter, while textual thoughts are still not executable mathematical actions.
- How EGR can cite it: CN: 用于引出 EGR 的范式转向：from next-token/thought generation to next-model transition。 | EN: Use it to motivate EGR's shift from next-token/thought generation to next-model transition.
- What EGR should learn: CN: EGR 应强调自己不是更长 CoT，而是改变了推理单元的类型。 | EN: EGR should stress that it is not longer CoT, but a change in the type of reasoning unit.
- Figure/writing implication: CN: 放在范式对比图左侧：textual reasoning path。 | EN: Place it on the left side of the paradigm figure as textual reasoning paths.
- Priority: Medium

### 23. MATHSENSEI: A Tool-Augmented Large Language Model for Mathematical Reasoning

- Title: MATHSENSEI: A Tool-Augmented Large Language Model for Mathematical Reasoning
- Authors / 作者: Debrup Das, Debopriyo Banerjee, Somak Aditya, Ashish Kulkarni, Kevin Duh, Helena Gomez, Steven Bethard
- Venue/Year / 会议年份: NAACL-HLT 2024, 2024
- Zotero key(s) / Zotero 条目键: `QYD82P5Z`
- Collection / 子集: Math-Reasoning
- Link / 链接: https://aclanthology.org/2024.naacl-long.54/
- Problem: CN: 该工作研究 LLM 能提出求解思路但计算/执行不稳定的问题。 | EN: It addresses the gap between LLM-generated solution plans and unreliable computation/execution.
- Method: CN: 让 LLM 生成程序、工具调用或可执行中间步骤，并把精确计算交给外部工具。 | EN: It lets LLMs generate programs, tool calls, or executable intermediate steps and delegates exact computation to external tools.
- Key claim/evidence: CN: 支持 predict-and-execute 分工，但其执行单元通常是代码或工具而不是 theorem model。 | EN: It supports predict-and-execute, but its execution unit is usually code or tools rather than theorem models.
- How EGR can cite it: CN: 用于把 EGR 定位为 theorem-model execution：不是执行任意代码，而是执行数学定理模型。 | EN: Use it to position EGR as theorem-model execution: executing mathematical theorem models rather than arbitrary code.
- What EGR should learn: CN: EGR 要突出 action space 更数学化、状态更显式、失败更可归因。 | EN: EGR should emphasize a more mathematical action space, explicit state, and clearer failure attribution.
- Figure/writing implication: CN: 适合做 PAL/PoT/tool methods vs EGR 的 comparison table。 | EN: Good for a PAL/PoT/tool methods vs EGR comparison table.
- Priority: High

### 24. Markov Chain of Thought for Efficient Mathematical Reasoning

- Title: Markov Chain of Thought for Efficient Mathematical Reasoning
- Authors / 作者: Wen Yang, Minpeng Liao, Kai Fan, Luis Chiruzzo, Alan Ritter, Lu Wang
- Venue/Year / 会议年份: NAACL-HLT 2025, 2025
- Zotero key(s) / Zotero 条目键: `4CDHQM7K`
- Collection / 子集: Math-Reasoning
- Link / 链接: https://aclanthology.org/2025.naacl-long.365/
- Problem: CN: 该工作研究如何让 LLM 生成、搜索或组织更好的中间推理路径。 | EN: It studies how LLMs generate, search, or organize better intermediate reasoning paths.
- Method: CN: 通过 CoT、路径搜索、提示选择、guided exploration 或多范式推理改进生成式推理。 | EN: It improves generative reasoning through CoT, path search, prompt selection, guided exploration, or multi-paradigm reasoning.
- Key claim/evidence: CN: 证明中间推理单元很重要，同时暴露文本 thought 仍不等于可执行数学 action。 | EN: It shows intermediate reasoning units matter, while textual thoughts are still not executable mathematical actions.
- How EGR can cite it: CN: 用于引出 EGR 的范式转向：from next-token/thought generation to next-model transition。 | EN: Use it to motivate EGR's shift from next-token/thought generation to next-model transition.
- What EGR should learn: CN: EGR 应强调自己不是更长 CoT，而是改变了推理单元的类型。 | EN: EGR should stress that it is not longer CoT, but a change in the type of reasoning unit.
- Figure/writing implication: CN: 放在范式对比图左侧：textual reasoning path。 | EN: Place it on the left side of the paradigm figure as textual reasoning paths.
- Priority: Medium

### 25. MathFusion: Enhancing Mathematical Problem-solving of LLM through Instruction Fusion

- Title: MathFusion: Enhancing Mathematical Problem-solving of LLM through Instruction Fusion
- Authors / 作者: Qizhi Pei, Lijun Wu, Zhuoshi Pan, Yu Li, Honglin Lin, Chenlin Ming, Xin Gao, Conghui He et al.
- Venue/Year / 会议年份: ACL 2025, 2025
- Zotero key(s) / Zotero 条目键: `XURYAHGX`
- Collection / 子集: Math-Reasoning
- Link / 链接: https://aclanthology.org/2025.acl-long.367/
- Problem: CN: 该工作研究如何通过数据合成、后训练、奖励模型、强化学习或样本选择提升数学推理表现。 | EN: It studies how data synthesis, post-training, reward modeling, RL, or sample selection improves math reasoning performance.
- Method: CN: 构造数学数据、筛选样本、训练奖励/策略模型，或进行数学专门后训练。 | EN: It builds math data, selects samples, trains reward/policy models, or applies math-specific post-training.
- Key claim/evidence: CN: 说明 LLM 数学能力持续提升，但这一路线通常不显式建模 theorem selection 与 symbolic execution。 | EN: It shows LLM math ability is improving, but usually without explicit theorem selection and symbolic execution.
- How EGR can cite it: CN: 用于 baseline 与实验背景，避免把 EGR 写成单纯追求 SOTA accuracy 的模型扩展。 | EN: Use it for baselines and experimental context, while avoiding framing EGR as just another accuracy-scaling method.
- What EGR should learn: CN: EGR 可把这些模型作为 backbone/baseline，但核心卖点应是可检查过程和状态转移。 | EN: EGR can use these systems as backbones/baselines, but its core value is checkable process and state transition.
- Figure/writing implication: CN: 放在 related-work map 的 data/RL scaling 区域。 | EN: Place it in the data/RL scaling region of the related-work map.
- Priority: Medium

### 26. Measuring Mathematical Problem Solving With the MATH Dataset

- Title: Measuring Mathematical Problem Solving With the MATH Dataset
- Authors / 作者: Dan Hendrycks, Collin Burns, Saurav Kadavath, Akul Arora, Steven Basart, Eric Tang, Dawn Song, Jacob Steinhardt
- Venue/Year / 会议年份: preprint, 2021
- Zotero key(s) / Zotero 条目键: `DLPVE96H`
- Collection / 子集: Math-Reasoning
- Link / 链接: http://arxiv.org/abs/2103.03874
- Problem: CN: 该工作整理数学推理任务、数据集、基准或领域挑战。 | EN: It organizes math reasoning tasks, datasets, benchmarks, or field challenges.
- Method: CN: 通过综述、基准构建、数据集设计或多维评测揭示当前模型局限。 | EN: It uses surveys, benchmark construction, dataset design, or multi-dimensional evaluation to reveal model limitations.
- Key claim/evidence: CN: 说明数学推理仍是 LLM 的核心挑战，并为 EGR 的问题设定提供背景。 | EN: It shows that mathematical reasoning remains a core challenge and provides background for EGR's problem setting.
- How EGR can cite it: CN: 用于 Introduction/Related Work 的领域背景，尤其是说明为什么仅看最终答案或通用 benchmark 不够。 | EN: Use it as Introduction/Related Work background, especially to explain why final answers or generic benchmarks are insufficient.
- What EGR should learn: CN: EGR 应把 conic-section 写成受控但非平凡的验证场景，并清楚说明评价维度。 | EN: EGR should present conic sections as a controlled but nontrivial testbed and define evaluation dimensions clearly.
- Figure/writing implication: CN: 支持 problem setting 图或 related-work map 的背景层。 | EN: Useful for a problem-setting figure or the background layer of a related-work map.
- Priority: High

### 27. Measuring Multimodal Mathematical Reasoning with MATH-Vision Dataset

- Title: Measuring Multimodal Mathematical Reasoning with MATH-Vision Dataset
- Authors / 作者: Ke Wang, Junting Pan, Weikang Shi, Zimu Lu, Houxing Ren, Aojun Zhou, Mingjie Zhan, Hongsheng Li
- Venue/Year / 会议年份: Advances in Neural Information Processing Systems, 2024
- Zotero key(s) / Zotero 条目键: `AKRDZ2FN`
- Collection / 子集: Math-Reasoning
- Link / 链接: https://proceedings.neurips.cc/paper_files/paper/2024/hash/ad0edc7d5fa1a783f063646968b7315b-Abstract-Datasets_and_Benchmarks_Track.html
- Problem: CN: 该工作整理数学推理任务、数据集、基准或领域挑战。 | EN: It organizes math reasoning tasks, datasets, benchmarks, or field challenges.
- Method: CN: 通过综述、基准构建、数据集设计或多维评测揭示当前模型局限。 | EN: It uses surveys, benchmark construction, dataset design, or multi-dimensional evaluation to reveal model limitations.
- Key claim/evidence: CN: 说明数学推理仍是 LLM 的核心挑战，并为 EGR 的问题设定提供背景。 | EN: It shows that mathematical reasoning remains a core challenge and provides background for EGR's problem setting.
- How EGR can cite it: CN: 用于 Introduction/Related Work 的领域背景，尤其是说明为什么仅看最终答案或通用 benchmark 不够。 | EN: Use it as Introduction/Related Work background, especially to explain why final answers or generic benchmarks are insufficient.
- What EGR should learn: CN: EGR 应把 conic-section 写成受控但非平凡的验证场景，并清楚说明评价维度。 | EN: EGR should present conic sections as a controlled but nontrivial testbed and define evaluation dimensions clearly.
- Figure/writing implication: CN: 支持 problem setting 图或 related-work map 的背景层。 | EN: Useful for a problem-setting figure or the background layer of a related-work map.
- Priority: Medium

### 28. MetaMath: Bootstrap Your Own Mathematical Questions for Large Language Models

- Title: MetaMath: Bootstrap Your Own Mathematical Questions for Large Language Models
- Authors / 作者: Longhui Yu, Weisen Jiang, Han Shi, Jincheng Yu, Zhengying Liu, Yu Zhang, James Kwok, Zhenguo Li et al.
- Venue/Year / 会议年份: International Conference on Learning Representations, 2024
- Zotero key(s) / Zotero 条目键: `FJ9TYZGT`
- Collection / 子集: Math-Reasoning
- Link / 链接: https://proceedings.iclr.cc/paper_files/paper/2024/hash/c400474e8a36d0812fdee52739288b12-Abstract-Conference.html
- Problem: CN: 该工作研究如何通过数据合成、后训练、奖励模型、强化学习或样本选择提升数学推理表现。 | EN: It studies how data synthesis, post-training, reward modeling, RL, or sample selection improves math reasoning performance.
- Method: CN: 构造数学数据、筛选样本、训练奖励/策略模型，或进行数学专门后训练。 | EN: It builds math data, selects samples, trains reward/policy models, or applies math-specific post-training.
- Key claim/evidence: CN: 说明 LLM 数学能力持续提升，但这一路线通常不显式建模 theorem selection 与 symbolic execution。 | EN: It shows LLM math ability is improving, but usually without explicit theorem selection and symbolic execution.
- How EGR can cite it: CN: 用于 baseline 与实验背景，避免把 EGR 写成单纯追求 SOTA accuracy 的模型扩展。 | EN: Use it for baselines and experimental context, while avoiding framing EGR as just another accuracy-scaling method.
- What EGR should learn: CN: EGR 可把这些模型作为 backbone/baseline，但核心卖点应是可检查过程和状态转移。 | EN: EGR can use these systems as backbones/baselines, but its core value is checkable process and state transition.
- Figure/writing implication: CN: 放在 related-work map 的 data/RL scaling 区域。 | EN: Place it in the data/RL scaling region of the related-work map.
- Priority: Medium

### 29. Metacognitive Capabilities of LLMs: An Exploration in Mathematical Problem Solving

- Title: Metacognitive Capabilities of LLMs: An Exploration in Mathematical Problem Solving
- Authors / 作者: Aniket Didolkar, Anirudh Goyal, Nan R. Ke, Siyuan Guo, Michal Valko, Timothy Lillicrap, Danilo Rezende, Yoshua Bengio et al.
- Venue/Year / 会议年份: Advances in Neural Information Processing Systems, 2024
- Zotero key(s) / Zotero 条目键: `WSNF4XPK`
- Collection / 子集: Math-Reasoning
- Link / 链接: https://proceedings.neurips.cc/paper_files/paper/2024/hash/2318d75a06437eaa257737a5cf3ab83c-Abstract-Conference.html
- Problem: CN: 该工作研究最终答案正确率无法解释中间推理可靠性的问题。 | EN: It addresses why final-answer accuracy cannot diagnose intermediate reasoning reliability.
- Method: CN: 使用步骤级反馈、过程监督、验证、错误分类、纠错或元认知评测来分析/改进推理。 | EN: It uses step-level feedback, process supervision, verification, error classification, correction, or metacognitive evaluation.
- Key claim/evidence: CN: 直接支持 EGR 把 selection、applicability、execution、termination、extraction 分开评测。 | EN: It directly supports EGR's separate evaluation of selection, applicability, execution, termination, and extraction.
- How EGR can cite it: CN: 用于证明 EGR 不应只报告 final answer accuracy，而应报告过程级指标和错误归因。 | EN: Use it to justify reporting process-level metrics and failure attribution, not only final answer accuracy.
- What EGR should learn: CN: EGR 的实验应包含 transition-level 诊断，并把失败定位到具体决策。 | EN: EGR experiments should include transition-level diagnosis and attribute failures to specific decisions.
- Figure/writing implication: CN: 启发错误分类图和 process-supervision related-work map。 | EN: Useful for an error-taxonomy figure and a process-supervision related-work map.
- Priority: High

### 30. Neural-Symbolic Architectural Axioms of Integration: A Manifesto

- Title: Neural-Symbolic Architectural Axioms of Integration: A Manifesto
- Authors / 作者: Connor Pryor, Lise Getoor
- Venue/Year / 会议年份: Conference on Neurosymbolic Learning and Reasoning, 2025
- Zotero key(s) / Zotero 条目键: `W5CBVKDV, ZTBUQ26X`
- Collection / 子集: Math-Reasoning + Neuro-Symbolic
- Link / 链接: https://proceedings.mlr.press/v284/pryor25a.html
- Problem: CN: 该工作研究 neuro-symbolic 系统的结构、原则、比较维度或可解释性。 | EN: It studies the structure, principles, comparison dimensions, or interpretability of neuro-symbolic systems.
- Method: CN: 提出框架、设计原则、比较分析、符号表示或神经符号推理结构。 | EN: It proposes frameworks, design principles, comparative analyses, symbolic representations, or neurosymbolic reasoning structures.
- Key claim/evidence: CN: 帮助 EGR 避免泛泛说 hybrid，而是明确 neural/symbolic 分工和接口。 | EN: It helps EGR avoid a vague hybrid claim and specify neural/symbolic roles and interfaces.
- How EGR can cite it: CN: 用于 Related Work 中定义 EGR 属于哪一类 NeSy framework。 | EN: Use it in Related Work to define what kind of NeSy framework EGR is.
- What EGR should learn: CN: EGR 应强调 selector、applicator、state representation、trace 四个结构接口。 | EN: EGR should emphasize four structural interfaces: selector, applicator, state representation, and trace.
- Figure/writing implication: CN: 启发 neural-symbolic boundary 和 architecture overview。 | EN: Useful for the neural-symbolic boundary and architecture overview.
- Priority: Medium

### 31. PAL: Program-aided Language Models

- Title: PAL: Program-aided Language Models
- Authors / 作者: Luyu Gao, Aman Madaan, Shuyan Zhou, Uri Alon, Pengfei Liu, Yiming Yang, Jamie Callan, Graham Neubig
- Venue/Year / 会议年份: International Conference on Machine Learning, 2023
- Zotero key(s) / Zotero 条目键: `YPTJGGN2`
- Collection / 子集: Math-Reasoning
- Link / 链接: https://proceedings.mlr.press/v202/gao23f.html
- Problem: CN: 该工作研究 LLM 能提出求解思路但计算/执行不稳定的问题。 | EN: It addresses the gap between LLM-generated solution plans and unreliable computation/execution.
- Method: CN: 让 LLM 生成程序、工具调用或可执行中间步骤，并把精确计算交给外部工具。 | EN: It lets LLMs generate programs, tool calls, or executable intermediate steps and delegates exact computation to external tools.
- Key claim/evidence: CN: 支持 predict-and-execute 分工，但其执行单元通常是代码或工具而不是 theorem model。 | EN: It supports predict-and-execute, but its execution unit is usually code or tools rather than theorem models.
- How EGR can cite it: CN: 用于把 EGR 定位为 theorem-model execution：不是执行任意代码，而是执行数学定理模型。 | EN: Use it to position EGR as theorem-model execution: executing mathematical theorem models rather than arbitrary code.
- What EGR should learn: CN: EGR 要突出 action space 更数学化、状态更显式、失败更可归因。 | EN: EGR should emphasize a more mathematical action space, explicit state, and clearer failure attribution.
- Figure/writing implication: CN: 适合做 PAL/PoT/tool methods vs EGR 的 comparison table。 | EN: Good for a PAL/PoT/tool methods vs EGR comparison table.
- Priority: High

### 32. Position: Formal Mathematical Reasoning—A New Frontier in AI

- Title: Position: Formal Mathematical Reasoning—A New Frontier in AI
- Authors / 作者: Kaiyu Yang, Gabriel Poesia, Jingxuan He, Wenda Li, Kristin E. Lauter, Swarat Chaudhuri, Dawn Song
- Venue/Year / 会议年份: International Conference on Machine Learning, 2025
- Zotero key(s) / Zotero 条目键: `VXC57ZI4`
- Collection / 子集: Math-Reasoning
- Link / 链接: https://proceedings.mlr.press/v267/yang25az.html
- Problem: CN: 该工作研究形式化数学中 proof state、premise/tactic 选择和可验证推理的问题。 | EN: It studies proof states, premise/tactic selection, and verifiable reasoning in formal mathematics.
- Method: CN: 用学习模型指导证明搜索、premise retrieval、tactic generation 或形式化验证。 | EN: It uses learned models to guide proof search, premise retrieval, tactic generation, or formal verification.
- Key claim/evidence: CN: 支持把数学推理写成状态空间中的动作选择，而不是一次性答案预测。 | EN: It supports writing mathematical reasoning as action selection in a state space, not one-shot answer prediction.
- How EGR can cite it: CN: 用于支撑 EGR 的 `P(M_t | S_t)` 选择器和 theorem-model trajectory 表述。 | EN: Use it to support EGR's `P(M_t | S_t)` selector and theorem-model trajectory formulation.
- What EGR should learn: CN: EGR 应借用 state/action/search 的严谨语言，但避免声称自己是通用 theorem prover。 | EN: EGR should borrow the rigorous language of state/action/search while avoiding the claim of being a general theorem prover.
- Figure/writing implication: CN: 适合与 EGR 的 theorem-action trajectory 放在同一对比图。 | EN: Good for a comparison figure with EGR's theorem-action trajectory.
- Priority: High

### 33. Premise-Augmented Reasoning Chains Improve Error Identification in Math reasoning with LLMs

- Title: Premise-Augmented Reasoning Chains Improve Error Identification in Math reasoning with LLMs
- Authors / 作者: Sagnik Mukherjee, Abhinav Chinta, Takyoung Kim, Tarun Anoop Sharma, Dilek Hakkani-Tür
- Venue/Year / 会议年份: preprint, 2025
- Zotero key(s) / Zotero 条目键: `Q3YU3IE6`
- Collection / 子集: Math-Reasoning
- Link / 链接: http://arxiv.org/abs/2502.02362
- Problem: CN: 该工作研究最终答案正确率无法解释中间推理可靠性的问题。 | EN: It addresses why final-answer accuracy cannot diagnose intermediate reasoning reliability.
- Method: CN: 使用步骤级反馈、过程监督、验证、错误分类、纠错或元认知评测来分析/改进推理。 | EN: It uses step-level feedback, process supervision, verification, error classification, correction, or metacognitive evaluation.
- Key claim/evidence: CN: 直接支持 EGR 把 selection、applicability、execution、termination、extraction 分开评测。 | EN: It directly supports EGR's separate evaluation of selection, applicability, execution, termination, and extraction.
- How EGR can cite it: CN: 用于证明 EGR 不应只报告 final answer accuracy，而应报告过程级指标和错误归因。 | EN: Use it to justify reporting process-level metrics and failure attribution, not only final answer accuracy.
- What EGR should learn: CN: EGR 的实验应包含 transition-level 诊断，并把失败定位到具体决策。 | EN: EGR experiments should include transition-level diagnosis and attribute failures to specific decisions.
- Figure/writing implication: CN: 启发错误分类图和 process-supervision related-work map。 | EN: Useful for an error-taxonomy figure and a process-supervision related-work map.
- Priority: High

### 34. Program of Thoughts Prompting: Disentangling Computation from Reasoning for Numerical Reasoning Tasks

- Title: Program of Thoughts Prompting: Disentangling Computation from Reasoning for Numerical Reasoning Tasks
- Authors / 作者: Wenhu Chen, Xueguang Ma, Xinyi Wang, William W. Cohen
- Venue/Year / 会议年份: preprint, 2023
- Zotero key(s) / Zotero 条目键: `5BJKB53Z`
- Collection / 子集: Math-Reasoning
- Link / 链接: http://arxiv.org/abs/2211.12588
- Problem: CN: 该工作研究 LLM 能提出求解思路但计算/执行不稳定的问题。 | EN: It addresses the gap between LLM-generated solution plans and unreliable computation/execution.
- Method: CN: 让 LLM 生成程序、工具调用或可执行中间步骤，并把精确计算交给外部工具。 | EN: It lets LLMs generate programs, tool calls, or executable intermediate steps and delegates exact computation to external tools.
- Key claim/evidence: CN: 支持 predict-and-execute 分工，但其执行单元通常是代码或工具而不是 theorem model。 | EN: It supports predict-and-execute, but its execution unit is usually code or tools rather than theorem models.
- How EGR can cite it: CN: 用于把 EGR 定位为 theorem-model execution：不是执行任意代码，而是执行数学定理模型。 | EN: Use it to position EGR as theorem-model execution: executing mathematical theorem models rather than arbitrary code.
- What EGR should learn: CN: EGR 要突出 action space 更数学化、状态更显式、失败更可归因。 | EN: EGR should emphasize a more mathematical action space, explicit state, and clearer failure attribution.
- Figure/writing implication: CN: 适合做 PAL/PoT/tool methods vs EGR 的 comparison table。 | EN: Good for a PAL/PoT/tool methods vs EGR comparison table.
- Priority: High

### 35. Safe: Enhancing Mathematical Reasoning in Large Language Models via Retrospective Step-aware Formal Verification

- Title: Safe: Enhancing Mathematical Reasoning in Large Language Models via Retrospective Step-aware Formal Verification
- Authors / 作者: Chengwu Liu, Ye Yuan, Yichun Yin, Yan Xu, Xin Xu, Zaoyu Chen, Yasheng Wang, Lifeng Shang et al.
- Venue/Year / 会议年份: ACL 2025, 2025
- Zotero key(s) / Zotero 条目键: `XPVZUZZQ`
- Collection / 子集: Math-Reasoning
- Link / 链接: https://aclanthology.org/2025.acl-long.594/
- Problem: CN: 该工作研究如何把 LLM 数学推理从纯文本转成可执行、可验证的符号表示。 | EN: It studies how to convert LLM math reasoning from prose into executable and verifiable symbolic representations.
- Method: CN: 由 LLM 生成逻辑式、形式语言、符号规则、程序或公式结构，再交给求解器/验证器执行。 | EN: The LLM produces logic forms, formal language, symbolic rules, programs, or formula structures that a solver/verifier executes.
- Key claim/evidence: CN: 支持“神经模型负责提出，符号层负责执行/验证”的分工。 | EN: It supports the division where neural models propose and symbolic modules execute or verify.
- How EGR can cite it: CN: 用于说明 EGR 的 applicator 是可靠推理的核心执行层，而不是事后检查器。 | EN: Use it to argue that EGR's applicator is a core execution layer, not merely a post-hoc checker.
- What EGR should learn: CN: EGR 需要把 theorem model 定义为 precondition + symbolic transition。 | EN: EGR should define theorem models as precondition plus symbolic transition.
- Figure/writing implication: CN: 启发 “selector -> theorem model -> applicator -> new symbolic state” 方法图。 | EN: Useful for the method figure: selector -> theorem model -> applicator -> new symbolic state.
- Priority: High

### 36. Specialized Mathematical Solving by a Step-By-Step Expression Chain Generation

- Title: Specialized Mathematical Solving by a Step-By-Step Expression Chain Generation
- Authors / 作者: Wenqi Zhang, Yongliang Shen, Guiyang Hou, Kuangyi Wang, Weiming Lu
- Venue/Year / 会议年份: IEEE/ACM Transactions on Audio, Speech, and Language Processing, 2024
- Zotero key(s) / Zotero 条目键: `3NJHJNZ5`
- Collection / 子集: Math-Reasoning
- Link / 链接: https://ieeexplore.ieee.org/abstract/document/10552332
- Problem: CN: 该工作研究如何让 LLM 生成、搜索或组织更好的中间推理路径。 | EN: It studies how LLMs generate, search, or organize better intermediate reasoning paths.
- Method: CN: 通过 CoT、路径搜索、提示选择、guided exploration 或多范式推理改进生成式推理。 | EN: It improves generative reasoning through CoT, path search, prompt selection, guided exploration, or multi-paradigm reasoning.
- Key claim/evidence: CN: 证明中间推理单元很重要，同时暴露文本 thought 仍不等于可执行数学 action。 | EN: It shows intermediate reasoning units matter, while textual thoughts are still not executable mathematical actions.
- How EGR can cite it: CN: 用于引出 EGR 的范式转向：from next-token/thought generation to next-model transition。 | EN: Use it to motivate EGR's shift from next-token/thought generation to next-model transition.
- What EGR should learn: CN: EGR 应强调自己不是更长 CoT，而是改变了推理单元的类型。 | EN: EGR should stress that it is not longer CoT, but a change in the type of reasoning unit.
- Figure/writing implication: CN: 放在范式对比图左侧：textual reasoning path。 | EN: Place it on the left side of the paradigm figure as textual reasoning paths.
- Priority: Medium

### 37. Step Guided Reasoning: Improving Mathematical Reasoning using Guidance Generation and Step Reasoning

- Title: Step Guided Reasoning: Improving Mathematical Reasoning using Guidance Generation and Step Reasoning
- Authors / 作者: Lang Cao, Yingtian Zou, Chao Peng, Renhong Chen, Wu Ning, Yitong Li, Christos Christodoulopoulos, Tanmoy Chakraborty et al.
- Venue/Year / 会议年份: EMNLP 2025, 2025
- Zotero key(s) / Zotero 条目键: `LPJBHT5B`
- Collection / 子集: Math-Reasoning
- Link / 链接: https://aclanthology.org/2025.emnlp-main.1068/
- Problem: CN: 该工作研究最终答案正确率无法解释中间推理可靠性的问题。 | EN: It addresses why final-answer accuracy cannot diagnose intermediate reasoning reliability.
- Method: CN: 使用步骤级反馈、过程监督、验证、错误分类、纠错或元认知评测来分析/改进推理。 | EN: It uses step-level feedback, process supervision, verification, error classification, correction, or metacognitive evaluation.
- Key claim/evidence: CN: 直接支持 EGR 把 selection、applicability、execution、termination、extraction 分开评测。 | EN: It directly supports EGR's separate evaluation of selection, applicability, execution, termination, and extraction.
- How EGR can cite it: CN: 用于证明 EGR 不应只报告 final answer accuracy，而应报告过程级指标和错误归因。 | EN: Use it to justify reporting process-level metrics and failure attribution, not only final answer accuracy.
- What EGR should learn: CN: EGR 的实验应包含 transition-level 诊断，并把失败定位到具体决策。 | EN: EGR experiments should include transition-level diagnosis and attribute failures to specific decisions.
- Figure/writing implication: CN: 启发错误分类图和 process-supervision related-work map。 | EN: Useful for an error-taxonomy figure and a process-supervision related-work map.
- Priority: High

### 38. Step-KTO: Optimizing Mathematical Reasoning through Stepwise Binary Feedback

- Title: Step-KTO: Optimizing Mathematical Reasoning through Stepwise Binary Feedback
- Authors / 作者: Yen-Ting Lin, Di Jin, Tengyu Xu, Tianhao Wu, Sainbayar Sukhbaatar, Chen Zhu, Yun He, Yun-Nung Chen et al.
- Venue/Year / 会议年份: Proceedings of The 3rd Workshop on Mathematical Natural Language Processing (MathNLP 2025), 2025
- Zotero key(s) / Zotero 条目键: `7JVRALZR`
- Collection / 子集: Math-Reasoning
- Link / 链接: https://aclanthology.org/2025.mathnlp-main.2/
- Problem: CN: 该工作研究最终答案正确率无法解释中间推理可靠性的问题。 | EN: It addresses why final-answer accuracy cannot diagnose intermediate reasoning reliability.
- Method: CN: 使用步骤级反馈、过程监督、验证、错误分类、纠错或元认知评测来分析/改进推理。 | EN: It uses step-level feedback, process supervision, verification, error classification, correction, or metacognitive evaluation.
- Key claim/evidence: CN: 直接支持 EGR 把 selection、applicability、execution、termination、extraction 分开评测。 | EN: It directly supports EGR's separate evaluation of selection, applicability, execution, termination, and extraction.
- How EGR can cite it: CN: 用于证明 EGR 不应只报告 final answer accuracy，而应报告过程级指标和错误归因。 | EN: Use it to justify reporting process-level metrics and failure attribution, not only final answer accuracy.
- What EGR should learn: CN: EGR 的实验应包含 transition-level 诊断，并把失败定位到具体决策。 | EN: EGR experiments should include transition-level diagnosis and attribute failures to specific decisions.
- Figure/writing implication: CN: 启发错误分类图和 process-supervision related-work map。 | EN: Useful for an error-taxonomy figure and a process-supervision related-work map.
- Priority: High

### 39. Step-by-Step Correction of LLM-based Math Word Problems Solutions

- Title: Step-by-Step Correction of LLM-based Math Word Problems Solutions
- Authors / 作者: Yiyao Li, Dhanish Musharraf Ubaidali, Lu Wang, Wenyu Zhang
- Venue/Year / 会议年份: ICASSP 2025 - 2025 IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP), 2025
- Zotero key(s) / Zotero 条目键: `A8XMXLZ6`
- Collection / 子集: Math-Reasoning
- Link / 链接: https://ieeexplore.ieee.org/abstract/document/10889273
- Problem: CN: 该工作研究最终答案正确率无法解释中间推理可靠性的问题。 | EN: It addresses why final-answer accuracy cannot diagnose intermediate reasoning reliability.
- Method: CN: 使用步骤级反馈、过程监督、验证、错误分类、纠错或元认知评测来分析/改进推理。 | EN: It uses step-level feedback, process supervision, verification, error classification, correction, or metacognitive evaluation.
- Key claim/evidence: CN: 直接支持 EGR 把 selection、applicability、execution、termination、extraction 分开评测。 | EN: It directly supports EGR's separate evaluation of selection, applicability, execution, termination, and extraction.
- How EGR can cite it: CN: 用于证明 EGR 不应只报告 final answer accuracy，而应报告过程级指标和错误归因。 | EN: Use it to justify reporting process-level metrics and failure attribution, not only final answer accuracy.
- What EGR should learn: CN: EGR 的实验应包含 transition-level 诊断，并把失败定位到具体决策。 | EN: EGR experiments should include transition-level diagnosis and attribute failures to specific decisions.
- Figure/writing implication: CN: 启发错误分类图和 process-supervision related-work map。 | EN: Useful for an error-taxonomy figure and a process-supervision related-work map.
- Priority: Medium

### 40. Tree of Thoughts: Deliberate Problem Solving with Large Language Models

- Title: Tree of Thoughts: Deliberate Problem Solving with Large Language Models
- Authors / 作者: Shunyu Yao, Dian Yu, Jeffrey Zhao, Izhak Shafran, Tom Griffiths, Yuan Cao, Karthik Narasimhan
- Venue/Year / 会议年份: Advances in Neural Information Processing Systems, 2023
- Zotero key(s) / Zotero 条目键: `HQEF6LB7`
- Collection / 子集: Math-Reasoning
- Link / 链接: https://proceedings.neurips.cc/paper/2023/hash/271db9922b8d1f4dd7aaef84ed5ac703-Abstract.html
- Problem: CN: 该工作研究如何让 LLM 生成、搜索或组织更好的中间推理路径。 | EN: It studies how LLMs generate, search, or organize better intermediate reasoning paths.
- Method: CN: 通过 CoT、路径搜索、提示选择、guided exploration 或多范式推理改进生成式推理。 | EN: It improves generative reasoning through CoT, path search, prompt selection, guided exploration, or multi-paradigm reasoning.
- Key claim/evidence: CN: 证明中间推理单元很重要，同时暴露文本 thought 仍不等于可执行数学 action。 | EN: It shows intermediate reasoning units matter, while textual thoughts are still not executable mathematical actions.
- How EGR can cite it: CN: 用于引出 EGR 的范式转向：from next-token/thought generation to next-model transition。 | EN: Use it to motivate EGR's shift from next-token/thought generation to next-model transition.
- What EGR should learn: CN: EGR 应强调自己不是更长 CoT，而是改变了推理单元的类型。 | EN: EGR should stress that it is not longer CoT, but a change in the type of reasoning unit.
- Figure/writing implication: CN: 放在范式对比图左侧：textual reasoning path。 | EN: Place it on the left side of the paradigm figure as textual reasoning paths.
- Priority: High

### 41. UDfSolver : Uniform representation and decoupled inference strategy for text-diagram function problems solving

- Title: UDfSolver : Uniform representation and decoupled inference strategy for text-diagram function problems solving
- Authors / 作者: Feng Xiong, Xinguo Yu, Litian Huang, Dian Yu
- Venue/Year / 会议年份: Expert Systems with Applications, 2026
- Zotero key(s) / Zotero 条目键: `N3JRKGF8`
- Collection / 子集: Math-Reasoning
- Link / 链接: https://www.sciencedirect.com/science/article/pii/S095741742602138X
- Problem: CN: 该工作是 EGR 作者前序图文函数题求解方向，帮助界定连续性与差异。 | EN: It is prior work on text-diagram function problem solving and helps define continuity and difference for EGR.
- Method: CN: 通过统一表示和解耦推理处理函数类题目。 | EN: It solves function problems through uniform representation and decoupled inference.
- Key claim/evidence: CN: 可说明 EGR 从函数题统一表示推进到圆锥曲线 theorem-action transition。 | EN: It can show that EGR advances from unified function representation to conic theorem-action transitions.
- How EGR can cite it: CN: 可作为自引/前序系统说明，但不要把旧工作 claim 混入 EGR 主贡献。 | EN: Can be cited as prior work, but do not merge earlier claims into EGR's main contribution.
- What EGR should learn: CN: EGR 应突出 conic-specific facts/queries、theorem model pool、select/execute 分离。 | EN: EGR should emphasize conic-specific facts/queries, theorem-model pool, and select/execute separation.
- Figure/writing implication: CN: 可做 prior work -> EGR 的演化图。 | EN: Useful for a prior-work-to-EGR evolution figure.
- Priority: High

### 42. What Do Learning Dynamics Reveal About Generalization in LLM Mathematical Reasoning?

- Title: What Do Learning Dynamics Reveal About Generalization in LLM Mathematical Reasoning?
- Authors / 作者: Katie Kang, Amrith Setlur, Dibya Ghosh, Jacob Steinhardt, Claire Tomlin, Sergey Levine, Aviral Kumar
- Venue/Year / 会议年份: International Conference on Machine Learning, 2025
- Zotero key(s) / Zotero 条目键: `PPG2R798`
- Collection / 子集: Math-Reasoning
- Link / 链接: https://proceedings.mlr.press/v267/kang25f.html
- Problem: CN: 该工作研究如何通过数据合成、后训练、奖励模型、强化学习或样本选择提升数学推理表现。 | EN: It studies how data synthesis, post-training, reward modeling, RL, or sample selection improves math reasoning performance.
- Method: CN: 构造数学数据、筛选样本、训练奖励/策略模型，或进行数学专门后训练。 | EN: It builds math data, selects samples, trains reward/policy models, or applies math-specific post-training.
- Key claim/evidence: CN: 说明 LLM 数学能力持续提升，但这一路线通常不显式建模 theorem selection 与 symbolic execution。 | EN: It shows LLM math ability is improving, but usually without explicit theorem selection and symbolic execution.
- How EGR can cite it: CN: 用于 baseline 与实验背景，避免把 EGR 写成单纯追求 SOTA accuracy 的模型扩展。 | EN: Use it for baselines and experimental context, while avoiding framing EGR as just another accuracy-scaling method.
- What EGR should learn: CN: EGR 可把这些模型作为 backbone/baseline，但核心卖点应是可检查过程和状态转移。 | EN: EGR can use these systems as backbones/baselines, but its core value is checkable process and state transition.
- Figure/writing implication: CN: 放在 related-work map 的 data/RL scaling 区域。 | EN: Place it in the data/RL scaling region of the related-work map.
- Priority: Medium

### 43. WizardMath: Empowering Mathematical Reasoning for Large Language Models via Reinforced Evol-Instruct

- Title: WizardMath: Empowering Mathematical Reasoning for Large Language Models via Reinforced Evol-Instruct
- Authors / 作者: Haipeng Luo, Qingfeng Sun, Can Xu, Pu Zhao, Jianguang Lou, Chongyang Tao, Xiubo Geng, Qingwei Lin et al.
- Venue/Year / 会议年份: preprint, 2025
- Zotero key(s) / Zotero 条目键: `DCEE427L`
- Collection / 子集: Math-Reasoning
- Link / 链接: http://arxiv.org/abs/2308.09583
- Problem: CN: 该工作研究如何通过数据合成、后训练、奖励模型、强化学习或样本选择提升数学推理表现。 | EN: It studies how data synthesis, post-training, reward modeling, RL, or sample selection improves math reasoning performance.
- Method: CN: 构造数学数据、筛选样本、训练奖励/策略模型，或进行数学专门后训练。 | EN: It builds math data, selects samples, trains reward/policy models, or applies math-specific post-training.
- Key claim/evidence: CN: 说明 LLM 数学能力持续提升，但这一路线通常不显式建模 theorem selection 与 symbolic execution。 | EN: It shows LLM math ability is improving, but usually without explicit theorem selection and symbolic execution.
- How EGR can cite it: CN: 用于 baseline 与实验背景，避免把 EGR 写成单纯追求 SOTA accuracy 的模型扩展。 | EN: Use it for baselines and experimental context, while avoiding framing EGR as just another accuracy-scaling method.
- What EGR should learn: CN: EGR 可把这些模型作为 backbone/baseline，但核心卖点应是可检查过程和状态转移。 | EN: EGR can use these systems as backbones/baselines, but its core value is checkable process and state transition.
- Figure/writing implication: CN: 放在 related-work map 的 data/RL scaling 区域。 | EN: Place it in the data/RL scaling region of the related-work map.
- Priority: Medium

### 44. rStar-Math: Small LLMs Can Master Math Reasoning with Self-Evolved Deep Thinking

- Title: rStar-Math: Small LLMs Can Master Math Reasoning with Self-Evolved Deep Thinking
- Authors / 作者: Xinyu Guan, Li Lyna Zhang, Yifei Liu, Ning Shang, Youran Sun, Yi Zhu, Fan Yang, Mao Yang
- Venue/Year / 会议年份: International Conference on Machine Learning, 2025
- Zotero key(s) / Zotero 条目键: `P6EWQUD8`
- Collection / 子集: Math-Reasoning
- Link / 链接: https://proceedings.mlr.press/v267/guan25f.html
- Problem: CN: 该工作研究如何通过数据合成、后训练、奖励模型、强化学习或样本选择提升数学推理表现。 | EN: It studies how data synthesis, post-training, reward modeling, RL, or sample selection improves math reasoning performance.
- Method: CN: 构造数学数据、筛选样本、训练奖励/策略模型，或进行数学专门后训练。 | EN: It builds math data, selects samples, trains reward/policy models, or applies math-specific post-training.
- Key claim/evidence: CN: 说明 LLM 数学能力持续提升，但这一路线通常不显式建模 theorem selection 与 symbolic execution。 | EN: It shows LLM math ability is improving, but usually without explicit theorem selection and symbolic execution.
- How EGR can cite it: CN: 用于 baseline 与实验背景，避免把 EGR 写成单纯追求 SOTA accuracy 的模型扩展。 | EN: Use it for baselines and experimental context, while avoiding framing EGR as just another accuracy-scaling method.
- What EGR should learn: CN: EGR 可把这些模型作为 backbone/baseline，但核心卖点应是可检查过程和状态转移。 | EN: EGR can use these systems as backbones/baselines, but its core value is checkable process and state transition.
- Figure/writing implication: CN: 放在 related-work map 的 data/RL scaling 区域。 | EN: Place it in the data/RL scaling region of the related-work map.
- Priority: Medium

### 45. A Comparative Study of Neurosymbolic AI Approaches to Interpretable Logical Reasoning

- Title: A Comparative Study of Neurosymbolic AI Approaches to Interpretable Logical Reasoning
- Authors / 作者: Michael K. Chen
- Venue/Year / 会议年份: Conference on Neurosymbolic Learning and Reasoning, 2025
- Zotero key(s) / Zotero 条目键: `HDT5C2KI`
- Collection / 子集: Neuro-Symbolic
- Link / 链接: https://proceedings.mlr.press/v284/chen25b.html
- Problem: CN: 该工作研究 neuro-symbolic 系统的结构、原则、比较维度或可解释性。 | EN: It studies the structure, principles, comparison dimensions, or interpretability of neuro-symbolic systems.
- Method: CN: 提出框架、设计原则、比较分析、符号表示或神经符号推理结构。 | EN: It proposes frameworks, design principles, comparative analyses, symbolic representations, or neurosymbolic reasoning structures.
- Key claim/evidence: CN: 帮助 EGR 避免泛泛说 hybrid，而是明确 neural/symbolic 分工和接口。 | EN: It helps EGR avoid a vague hybrid claim and specify neural/symbolic roles and interfaces.
- How EGR can cite it: CN: 用于 Related Work 中定义 EGR 属于哪一类 NeSy framework。 | EN: Use it in Related Work to define what kind of NeSy framework EGR is.
- What EGR should learn: CN: EGR 应强调 selector、applicator、state representation、trace 四个结构接口。 | EN: EGR should emphasize four structural interfaces: selector, applicator, state representation, and trace.
- Figure/writing implication: CN: 启发 neural-symbolic boundary 和 architecture overview。 | EN: Useful for the neural-symbolic boundary and architecture overview.
- Priority: Medium

### 46. A Neuro-Symbolic Approach for Reliable Proof Generation with LLMs: A Case Study in Euclidean Geometry

- Title: A Neuro-Symbolic Approach for Reliable Proof Generation with LLMs: A Case Study in Euclidean Geometry
- Authors / 作者: Oren Sultan, Eitan Stern, Dafna Shahaf
- Venue/Year / 会议年份: preprint, 2026
- Zotero key(s) / Zotero 条目键: `JTQV2CXK`
- Collection / 子集: Neuro-Symbolic
- Link / 链接: http://arxiv.org/abs/2505.14479
- Problem: CN: 该工作研究几何或奥林匹克几何中的神经符号推理和可验证证明。 | EN: It studies neural-symbolic reasoning and verifiable proof in geometry or Olympiad geometry.
- Method: CN: 用神经模型指导构造、搜索或证明，由符号几何引擎完成推理验证。 | EN: It uses neural models to guide construction, search, or proof, while a symbolic geometry engine verifies reasoning.
- Key claim/evidence: CN: 证明几何是神经符号数学推理的高价值场景，可为 EGR 的 conic-section 选择背书。 | EN: It shows geometry is a high-value setting for neural-symbolic mathematical reasoning, supporting EGR's conic-section choice.
- How EGR can cite it: CN: 用于说明圆锥曲线题不是 toy domain，而是结构化几何概念与符号代数执行交汇的验证场景。 | EN: Use it to argue conic sections are not a toy domain but a testbed where structured geometry meets symbolic algebraic execution.
- What EGR should learn: CN: EGR 要区分自己与 Euclidean proof systems：重点在解析几何状态、定理模型、代数执行和答案抽取。 | EN: EGR should distinguish itself from Euclidean proof systems by emphasizing analytic-geometry state, theorem models, algebraic execution, and answer extraction.
- Figure/writing implication: CN: 适合做 AlphaGeometry/geometry prover vs EGR 的并列图。 | EN: Good for a side-by-side AlphaGeometry/geometry prover vs EGR figure.
- Priority: High

### 47. AXIOM: A Trust-First Neuro-Symbolic Execution Architecture for Verifiable Mathematical Reasoning

- Title: AXIOM: A Trust-First Neuro-Symbolic Execution Architecture for Verifiable Mathematical Reasoning
- Authors / 作者: Alessio Bruno
- Venue/Year / 会议年份: preprint, 2026
- Zotero key(s) / Zotero 条目键: `PKMQPGAQ`
- Collection / 子集: Neuro-Symbolic
- Link / 链接: http://arxiv.org/abs/2606.00671
- Problem: CN: 该工作研究如何把 LLM 数学推理从纯文本转成可执行、可验证的符号表示。 | EN: It studies how to convert LLM math reasoning from prose into executable and verifiable symbolic representations.
- Method: CN: 由 LLM 生成逻辑式、形式语言、符号规则、程序或公式结构，再交给求解器/验证器执行。 | EN: The LLM produces logic forms, formal language, symbolic rules, programs, or formula structures that a solver/verifier executes.
- Key claim/evidence: CN: 支持“神经模型负责提出，符号层负责执行/验证”的分工。 | EN: It supports the division where neural models propose and symbolic modules execute or verify.
- How EGR can cite it: CN: 用于说明 EGR 的 applicator 是可靠推理的核心执行层，而不是事后检查器。 | EN: Use it to argue that EGR's applicator is a core execution layer, not merely a post-hoc checker.
- What EGR should learn: CN: EGR 需要把 theorem model 定义为 precondition + symbolic transition。 | EN: EGR should define theorem models as precondition plus symbolic transition.
- Figure/writing implication: CN: 启发 “selector -> theorem model -> applicator -> new symbolic state” 方法图。 | EN: Useful for the method figure: selector -> theorem model -> applicator -> new symbolic state.
- Priority: High

### 48. Advanced Weakly-Supervised Formula Exploration for Neuro-Symbolic Mathematical Reasoning

- Title: Advanced Weakly-Supervised Formula Exploration for Neuro-Symbolic Mathematical Reasoning
- Authors / 作者: Yuxuan Wu, Hideki Nakayama
- Venue/Year / 会议年份: preprint, 2025
- Zotero key(s) / Zotero 条目键: `SCARFSQN`
- Collection / 子集: Neuro-Symbolic
- Link / 链接: http://arxiv.org/abs/2502.00629
- Problem: CN: 该工作研究如何把 LLM 数学推理从纯文本转成可执行、可验证的符号表示。 | EN: It studies how to convert LLM math reasoning from prose into executable and verifiable symbolic representations.
- Method: CN: 由 LLM 生成逻辑式、形式语言、符号规则、程序或公式结构，再交给求解器/验证器执行。 | EN: The LLM produces logic forms, formal language, symbolic rules, programs, or formula structures that a solver/verifier executes.
- Key claim/evidence: CN: 支持“神经模型负责提出，符号层负责执行/验证”的分工。 | EN: It supports the division where neural models propose and symbolic modules execute or verify.
- How EGR can cite it: CN: 用于说明 EGR 的 applicator 是可靠推理的核心执行层，而不是事后检查器。 | EN: Use it to argue that EGR's applicator is a core execution layer, not merely a post-hoc checker.
- What EGR should learn: CN: EGR 需要把 theorem model 定义为 precondition + symbolic transition。 | EN: EGR should define theorem models as precondition plus symbolic transition.
- Figure/writing implication: CN: 启发 “selector -> theorem model -> applicator -> new symbolic state” 方法图。 | EN: Useful for the method figure: selector -> theorem model -> applicator -> new symbolic state.
- Priority: Medium

### 49. Artificial Intelligence for Mathematical Reasoning: An Integrated Survey of Language Models, Neuro-symbolic Systems, and Verified Discovery

- Title: Artificial Intelligence for Mathematical Reasoning: An Integrated Survey of Language Models, Neuro-symbolic Systems, and Verified Discovery
- Authors / 作者: Syed Rifat Raiyan, Mohsinul Kabir, Hasan Mahmud, Md Kamrul Hasan, Sophia Ananiadou
- Venue/Year / 会议年份: preprint, 2026
- Zotero key(s) / Zotero 条目键: `MZK3EBLT`
- Collection / 子集: Neuro-Symbolic
- Link / 链接: http://arxiv.org/abs/2606.08728
- Problem: CN: 该工作整理数学推理任务、数据集、基准或领域挑战。 | EN: It organizes math reasoning tasks, datasets, benchmarks, or field challenges.
- Method: CN: 通过综述、基准构建、数据集设计或多维评测揭示当前模型局限。 | EN: It uses surveys, benchmark construction, dataset design, or multi-dimensional evaluation to reveal model limitations.
- Key claim/evidence: CN: 说明数学推理仍是 LLM 的核心挑战，并为 EGR 的问题设定提供背景。 | EN: It shows that mathematical reasoning remains a core challenge and provides background for EGR's problem setting.
- How EGR can cite it: CN: 用于 Introduction/Related Work 的领域背景，尤其是说明为什么仅看最终答案或通用 benchmark 不够。 | EN: Use it as Introduction/Related Work background, especially to explain why final answers or generic benchmarks are insufficient.
- What EGR should learn: CN: EGR 应把 conic-section 写成受控但非平凡的验证场景，并清楚说明评价维度。 | EN: EGR should present conic sections as a controlled but nontrivial testbed and define evaluation dimensions clearly.
- Figure/writing implication: CN: 支持 problem setting 图或 related-work map 的背景层。 | EN: Useful for a problem-setting figure or the background layer of a related-work map.
- Priority: Medium

### 50. Evaluating Neuro-Symbolic AI Architectures: Design Principles, Qualitative Benchmark, Comparative Analysis and Results

- Title: Evaluating Neuro-Symbolic AI Architectures: Design Principles, Qualitative Benchmark, Comparative Analysis and Results
- Authors / 作者: Oualid Bougzime, Samir Jabbar, Christophe Cruz, Frédéric Demoly
- Venue/Year / 会议年份: Conference on Neurosymbolic Learning and Reasoning, 2025
- Zotero key(s) / Zotero 条目键: `62TGMMWF`
- Collection / 子集: Neuro-Symbolic
- Link / 链接: https://proceedings.mlr.press/v284/bougzime25a.html
- Problem: CN: 该工作研究 neuro-symbolic 系统的结构、原则、比较维度或可解释性。 | EN: It studies the structure, principles, comparison dimensions, or interpretability of neuro-symbolic systems.
- Method: CN: 提出框架、设计原则、比较分析、符号表示或神经符号推理结构。 | EN: It proposes frameworks, design principles, comparative analyses, symbolic representations, or neurosymbolic reasoning structures.
- Key claim/evidence: CN: 帮助 EGR 避免泛泛说 hybrid，而是明确 neural/symbolic 分工和接口。 | EN: It helps EGR avoid a vague hybrid claim and specify neural/symbolic roles and interfaces.
- How EGR can cite it: CN: 用于 Related Work 中定义 EGR 属于哪一类 NeSy framework。 | EN: Use it in Related Work to define what kind of NeSy framework EGR is.
- What EGR should learn: CN: EGR 应强调 selector、applicator、state representation、trace 四个结构接口。 | EN: EGR should emphasize four structural interfaces: selector, applicator, state representation, and trace.
- Figure/writing implication: CN: 启发 neural-symbolic boundary 和 architecture overview。 | EN: Useful for the neural-symbolic boundary and architecture overview.
- Priority: Medium

### 51. Gold-medalist Performance in Solving Olympiad Geometry with AlphaGeometry2

- Title: Gold-medalist Performance in Solving Olympiad Geometry with AlphaGeometry2
- Authors / 作者: Yuri Chervonyi, Trieu H. Trinh, Miroslav Olšák, Xiaomeng Yang, Hoang H. Nguyen, Marcelo Menegali, Junehyuk Jung, Junsu Kim et al.
- Venue/Year / 会议年份: Journal of Machine Learning Research, 2025
- Zotero key(s) / Zotero 条目键: `62DDQGKL`
- Collection / 子集: Neuro-Symbolic
- Link / 链接: http://jmlr.org/papers/v26/25-1654.html
- Problem: CN: 该工作研究几何或奥林匹克几何中的神经符号推理和可验证证明。 | EN: It studies neural-symbolic reasoning and verifiable proof in geometry or Olympiad geometry.
- Method: CN: 用神经模型指导构造、搜索或证明，由符号几何引擎完成推理验证。 | EN: It uses neural models to guide construction, search, or proof, while a symbolic geometry engine verifies reasoning.
- Key claim/evidence: CN: 证明几何是神经符号数学推理的高价值场景，可为 EGR 的 conic-section 选择背书。 | EN: It shows geometry is a high-value setting for neural-symbolic mathematical reasoning, supporting EGR's conic-section choice.
- How EGR can cite it: CN: 用于说明圆锥曲线题不是 toy domain，而是结构化几何概念与符号代数执行交汇的验证场景。 | EN: Use it to argue conic sections are not a toy domain but a testbed where structured geometry meets symbolic algebraic execution.
- What EGR should learn: CN: EGR 要区分自己与 Euclidean proof systems：重点在解析几何状态、定理模型、代数执行和答案抽取。 | EN: EGR should distinguish itself from Euclidean proof systems by emphasizing analytic-geometry state, theorem models, algebraic execution, and answer extraction.
- Figure/writing implication: CN: 适合做 AlphaGeometry/geometry prover vs EGR 的并列图。 | EN: Good for a side-by-side AlphaGeometry/geometry prover vs EGR figure.
- Priority: High

### 52. Improving Rule-based Reasoning in LLMs using Neurosymbolic Representations

- Title: Improving Rule-based Reasoning in LLMs using Neurosymbolic Representations
- Authors / 作者: Varun Dhanraj, Chris Eliasmith, Christos Christodoulopoulos, Tanmoy Chakraborty, Carolyn Rose, Violet Peng
- Venue/Year / 会议年份: EMNLP 2025, 2025
- Zotero key(s) / Zotero 条目键: `2JRWFDPS`
- Collection / 子集: Neuro-Symbolic
- Link / 链接: https://aclanthology.org/2025.emnlp-main.1556/
- Problem: CN: 该工作研究 neuro-symbolic 系统的结构、原则、比较维度或可解释性。 | EN: It studies the structure, principles, comparison dimensions, or interpretability of neuro-symbolic systems.
- Method: CN: 提出框架、设计原则、比较分析、符号表示或神经符号推理结构。 | EN: It proposes frameworks, design principles, comparative analyses, symbolic representations, or neurosymbolic reasoning structures.
- Key claim/evidence: CN: 帮助 EGR 避免泛泛说 hybrid，而是明确 neural/symbolic 分工和接口。 | EN: It helps EGR avoid a vague hybrid claim and specify neural/symbolic roles and interfaces.
- How EGR can cite it: CN: 用于 Related Work 中定义 EGR 属于哪一类 NeSy framework。 | EN: Use it in Related Work to define what kind of NeSy framework EGR is.
- What EGR should learn: CN: EGR 应强调 selector、applicator、state representation、trace 四个结构接口。 | EN: EGR should emphasize four structural interfaces: selector, applicator, state representation, and trace.
- Figure/writing implication: CN: 启发 neural-symbolic boundary 和 architecture overview。 | EN: Useful for the neural-symbolic boundary and architecture overview.
- Priority: Medium

### 53. Intermediate Languages Matter: Formal Languages and LLMs affect Neurosymbolic Reasoning

- Title: Intermediate Languages Matter: Formal Languages and LLMs affect Neurosymbolic Reasoning
- Authors / 作者: Alexander Beiser, David Penz, Nysret Musliu
- Venue/Year / 会议年份: preprint, 2025
- Zotero key(s) / Zotero 条目键: `35N8EJKK`
- Collection / 子集: Neuro-Symbolic
- Link / 链接: http://arxiv.org/abs/2509.04083
- Problem: CN: 该工作研究中间语言、领域知识或表示接口如何影响神经符号推理可靠性。 | EN: It studies how intermediate languages, domain knowledge, or representation interfaces affect neurosymbolic reliability.
- Method: CN: 比较形式语言、引入 ontology/领域知识，或分析 LLM 与符号系统之间的表示接口。 | EN: It compares formal languages, introduces ontology/domain knowledge, or analyzes the interface between LLMs and symbolic systems.
- Key claim/evidence: CN: 直接支持 EGR 的 dual-state 设计：AbstractState 服务预测，SymbolicState 服务执行。 | EN: It directly supports EGR's dual-state design: AbstractState for prediction and SymbolicState for execution.
- How EGR can cite it: CN: 用于说明状态表示不是 feature engineering，而是 EGR 神经-符号接口的核心。 | EN: Use it to argue that state representation is not feature engineering but the core neural-symbolic interface of EGR.
- What EGR should learn: CN: EGR 应明确自然语言、抽象状态、符号状态、theorem model 之间的边界。 | EN: EGR should clearly separate natural language, abstract state, symbolic state, and theorem models.
- Figure/writing implication: CN: 启发 dual-state interface 图。 | EN: Useful for the dual-state interface figure.
- Priority: High

### 54. Logic-LM: Empowering Large Language Models with Symbolic Solvers for Faithful Logical Reasoning

- Title: Logic-LM: Empowering Large Language Models with Symbolic Solvers for Faithful Logical Reasoning
- Authors / 作者: Liangming Pan, Alon Albalak, Xinyi Wang, William Wang, Houda Bouamor, Juan Pino, Kalika Bali
- Venue/Year / 会议年份: Findings 2023, 2023
- Zotero key(s) / Zotero 条目键: `NLS7KG7U`
- Collection / 子集: Neuro-Symbolic
- Link / 链接: https://aclanthology.org/2023.findings-emnlp.248/
- Problem: CN: 该工作研究如何把 LLM 数学推理从纯文本转成可执行、可验证的符号表示。 | EN: It studies how to convert LLM math reasoning from prose into executable and verifiable symbolic representations.
- Method: CN: 由 LLM 生成逻辑式、形式语言、符号规则、程序或公式结构，再交给求解器/验证器执行。 | EN: The LLM produces logic forms, formal language, symbolic rules, programs, or formula structures that a solver/verifier executes.
- Key claim/evidence: CN: 支持“神经模型负责提出，符号层负责执行/验证”的分工。 | EN: It supports the division where neural models propose and symbolic modules execute or verify.
- How EGR can cite it: CN: 用于说明 EGR 的 applicator 是可靠推理的核心执行层，而不是事后检查器。 | EN: Use it to argue that EGR's applicator is a core execution layer, not merely a post-hoc checker.
- What EGR should learn: CN: EGR 需要把 theorem model 定义为 precondition + symbolic transition。 | EN: EGR should define theorem models as precondition plus symbolic transition.
- Figure/writing implication: CN: 启发 “selector -> theorem model -> applicator -> new symbolic state” 方法图。 | EN: Useful for the method figure: selector -> theorem model -> applicator -> new symbolic state.
- Priority: High

### 55. Neural Theorem Proving: Generating and Structuring Proofs for Formal Verification

- Title: Neural Theorem Proving: Generating and Structuring Proofs for Formal Verification
- Authors / 作者: Balaji Rao, William Eiers, Carlo Lipizzi
- Venue/Year / 会议年份: Conference on Neurosymbolic Learning and Reasoning, 2025
- Zotero key(s) / Zotero 条目键: `BKWH3V9M`
- Collection / 子集: Neuro-Symbolic
- Link / 链接: https://proceedings.mlr.press/v284/rao25a.html
- Problem: CN: 该工作研究形式化数学中 proof state、premise/tactic 选择和可验证推理的问题。 | EN: It studies proof states, premise/tactic selection, and verifiable reasoning in formal mathematics.
- Method: CN: 用学习模型指导证明搜索、premise retrieval、tactic generation 或形式化验证。 | EN: It uses learned models to guide proof search, premise retrieval, tactic generation, or formal verification.
- Key claim/evidence: CN: 支持把数学推理写成状态空间中的动作选择，而不是一次性答案预测。 | EN: It supports writing mathematical reasoning as action selection in a state space, not one-shot answer prediction.
- How EGR can cite it: CN: 用于支撑 EGR 的 `P(M_t | S_t)` 选择器和 theorem-model trajectory 表述。 | EN: Use it to support EGR's `P(M_t | S_t)` selector and theorem-model trajectory formulation.
- What EGR should learn: CN: EGR 应借用 state/action/search 的严谨语言，但避免声称自己是通用 theorem prover。 | EN: EGR should borrow the rigorous language of state/action/search while avoiding the claim of being a general theorem prover.
- Figure/writing implication: CN: 适合与 EGR 的 theorem-action trajectory 放在同一对比图。 | EN: Good for a comparison figure with EGR's theorem-action trajectory.
- Priority: High

### 56. Neuro-Symbolic AI in 2024: A Systematic Review

- Title: Neuro-Symbolic AI in 2024: A Systematic Review
- Authors / 作者: Brandon C. Colelough, William Regli
- Venue/Year / 会议年份: preprint, 2025
- Zotero key(s) / Zotero 条目键: `VS6IYHHK`
- Collection / 子集: Neuro-Symbolic
- Link / 链接: http://arxiv.org/abs/2501.05435
- Problem: CN: 该工作研究 neuro-symbolic 系统的结构、原则、比较维度或可解释性。 | EN: It studies the structure, principles, comparison dimensions, or interpretability of neuro-symbolic systems.
- Method: CN: 提出框架、设计原则、比较分析、符号表示或神经符号推理结构。 | EN: It proposes frameworks, design principles, comparative analyses, symbolic representations, or neurosymbolic reasoning structures.
- Key claim/evidence: CN: 帮助 EGR 避免泛泛说 hybrid，而是明确 neural/symbolic 分工和接口。 | EN: It helps EGR avoid a vague hybrid claim and specify neural/symbolic roles and interfaces.
- How EGR can cite it: CN: 用于 Related Work 中定义 EGR 属于哪一类 NeSy framework。 | EN: Use it in Related Work to define what kind of NeSy framework EGR is.
- What EGR should learn: CN: EGR 应强调 selector、applicator、state representation、trace 四个结构接口。 | EN: EGR should emphasize four structural interfaces: selector, applicator, state representation, and trace.
- Figure/writing implication: CN: 启发 neural-symbolic boundary 和 architecture overview。 | EN: Useful for the neural-symbolic boundary and architecture overview.
- Priority: Medium

### 57. NeuroProlog: Multi-Task Fine-Tuning for Neurosymbolic Mathematical Reasoning via the Cocktail Effect

- Title: NeuroProlog: Multi-Task Fine-Tuning for Neurosymbolic Mathematical Reasoning via the Cocktail Effect
- Authors / 作者: Pratibha Zunjare, Michael Hsiao
- Venue/Year / 会议年份: preprint, 2026
- Zotero key(s) / Zotero 条目键: `3DZ8JYKG`
- Collection / 子集: Neuro-Symbolic
- Link / 链接: http://arxiv.org/abs/2603.02504
- Problem: CN: 该工作研究如何把 LLM 数学推理从纯文本转成可执行、可验证的符号表示。 | EN: It studies how to convert LLM math reasoning from prose into executable and verifiable symbolic representations.
- Method: CN: 由 LLM 生成逻辑式、形式语言、符号规则、程序或公式结构，再交给求解器/验证器执行。 | EN: The LLM produces logic forms, formal language, symbolic rules, programs, or formula structures that a solver/verifier executes.
- Key claim/evidence: CN: 支持“神经模型负责提出，符号层负责执行/验证”的分工。 | EN: It supports the division where neural models propose and symbolic modules execute or verify.
- How EGR can cite it: CN: 用于说明 EGR 的 applicator 是可靠推理的核心执行层，而不是事后检查器。 | EN: Use it to argue that EGR's applicator is a core execution layer, not merely a post-hoc checker.
- What EGR should learn: CN: EGR 需要把 theorem model 定义为 precondition + symbolic transition。 | EN: EGR should define theorem models as precondition plus symbolic transition.
- Figure/writing implication: CN: 启发 “selector -> theorem model -> applicator -> new symbolic state” 方法图。 | EN: Useful for the method figure: selector -> theorem model -> applicator -> new symbolic state.
- Priority: High

### 58. Ontology-Guided Neuro-Symbolic Inference: Grounding Language Models with Mathematical Domain Knowledge

- Title: Ontology-Guided Neuro-Symbolic Inference: Grounding Language Models with Mathematical Domain Knowledge
- Authors / 作者: Marcelo Labre
- Venue/Year / 会议年份: preprint, 2026
- Zotero key(s) / Zotero 条目键: `896595VC`
- Collection / 子集: Neuro-Symbolic
- Link / 链接: http://arxiv.org/abs/2602.17826
- Problem: CN: 该工作研究中间语言、领域知识或表示接口如何影响神经符号推理可靠性。 | EN: It studies how intermediate languages, domain knowledge, or representation interfaces affect neurosymbolic reliability.
- Method: CN: 比较形式语言、引入 ontology/领域知识，或分析 LLM 与符号系统之间的表示接口。 | EN: It compares formal languages, introduces ontology/domain knowledge, or analyzes the interface between LLMs and symbolic systems.
- Key claim/evidence: CN: 直接支持 EGR 的 dual-state 设计：AbstractState 服务预测，SymbolicState 服务执行。 | EN: It directly supports EGR's dual-state design: AbstractState for prediction and SymbolicState for execution.
- How EGR can cite it: CN: 用于说明状态表示不是 feature engineering，而是 EGR 神经-符号接口的核心。 | EN: Use it to argue that state representation is not feature engineering but the core neural-symbolic interface of EGR.
- What EGR should learn: CN: EGR 应明确自然语言、抽象状态、符号状态、theorem model 之间的边界。 | EN: EGR should clearly separate natural language, abstract state, symbolic state, and theorem models.
- Figure/writing implication: CN: 启发 dual-state interface 图。 | EN: Useful for the dual-state interface figure.
- Priority: Medium

### 59. Rethinking Reasoning in LLMs: Neuro-Symbolic Local RetoMaton Beyond CoT and ICL

- Title: Rethinking Reasoning in LLMs: Neuro-Symbolic Local RetoMaton Beyond CoT and ICL
- Authors / 作者: Rushitha Santhoshi Mamidala, Anshuman Chhabra, Ankur Mali
- Venue/Year / 会议年份: Conference on Neurosymbolic Learning and Reasoning, 2025
- Zotero key(s) / Zotero 条目键: `XDJBTER9`
- Collection / 子集: Neuro-Symbolic
- Link / 链接: https://proceedings.mlr.press/v284/mamidala25a.html
- Problem: CN: 该工作研究 neuro-symbolic 系统的结构、原则、比较维度或可解释性。 | EN: It studies the structure, principles, comparison dimensions, or interpretability of neuro-symbolic systems.
- Method: CN: 提出框架、设计原则、比较分析、符号表示或神经符号推理结构。 | EN: It proposes frameworks, design principles, comparative analyses, symbolic representations, or neurosymbolic reasoning structures.
- Key claim/evidence: CN: 帮助 EGR 避免泛泛说 hybrid，而是明确 neural/symbolic 分工和接口。 | EN: It helps EGR avoid a vague hybrid claim and specify neural/symbolic roles and interfaces.
- How EGR can cite it: CN: 用于 Related Work 中定义 EGR 属于哪一类 NeSy framework。 | EN: Use it in Related Work to define what kind of NeSy framework EGR is.
- What EGR should learn: CN: EGR 应强调 selector、applicator、state representation、trace 四个结构接口。 | EN: EGR should emphasize four structural interfaces: selector, applicator, state representation, and trace.
- Figure/writing implication: CN: 启发 neural-symbolic boundary 和 architecture overview。 | EN: Useful for the neural-symbolic boundary and architecture overview.
- Priority: Medium

### 60. Solving Math Word Problems by Combining Language Models With Symbolic Solvers

- Title: Solving Math Word Problems by Combining Language Models With Symbolic Solvers
- Authors / 作者: Joy He-Yueya, Gabriel Poesia, Rose E. Wang, Noah D. Goodman
- Venue/Year / 会议年份: preprint, 2023
- Zotero key(s) / Zotero 条目键: `TNLY6B5L`
- Collection / 子集: Neuro-Symbolic
- Link / 链接: http://arxiv.org/abs/2304.09102
- Problem: CN: 该工作研究如何把 LLM 数学推理从纯文本转成可执行、可验证的符号表示。 | EN: It studies how to convert LLM math reasoning from prose into executable and verifiable symbolic representations.
- Method: CN: 由 LLM 生成逻辑式、形式语言、符号规则、程序或公式结构，再交给求解器/验证器执行。 | EN: The LLM produces logic forms, formal language, symbolic rules, programs, or formula structures that a solver/verifier executes.
- Key claim/evidence: CN: 支持“神经模型负责提出，符号层负责执行/验证”的分工。 | EN: It supports the division where neural models propose and symbolic modules execute or verify.
- How EGR can cite it: CN: 用于说明 EGR 的 applicator 是可靠推理的核心执行层，而不是事后检查器。 | EN: Use it to argue that EGR's applicator is a core execution layer, not merely a post-hoc checker.
- What EGR should learn: CN: EGR 需要把 theorem model 定义为 precondition + symbolic transition。 | EN: EGR should define theorem models as precondition plus symbolic transition.
- Figure/writing implication: CN: 启发 “selector -> theorem model -> applicator -> new symbolic state” 方法图。 | EN: Useful for the method figure: selector -> theorem model -> applicator -> new symbolic state.
- Priority: High

### 61. Solving olympiad geometry without human demonstrations

- Title: Solving olympiad geometry without human demonstrations
- Authors / 作者: Trieu H. Trinh, Yuhuai Wu, Quoc V. Le, He He, Thang Luong
- Venue/Year / 会议年份: Nature, 2024
- Zotero key(s) / Zotero 条目键: `29YALYRP`
- Collection / 子集: Neuro-Symbolic
- Link / 链接: https://www.nature.com/articles/s41586-023-06747-5
- Problem: CN: 该工作研究几何或奥林匹克几何中的神经符号推理和可验证证明。 | EN: It studies neural-symbolic reasoning and verifiable proof in geometry or Olympiad geometry.
- Method: CN: 用神经模型指导构造、搜索或证明，由符号几何引擎完成推理验证。 | EN: It uses neural models to guide construction, search, or proof, while a symbolic geometry engine verifies reasoning.
- Key claim/evidence: CN: 证明几何是神经符号数学推理的高价值场景，可为 EGR 的 conic-section 选择背书。 | EN: It shows geometry is a high-value setting for neural-symbolic mathematical reasoning, supporting EGR's conic-section choice.
- How EGR can cite it: CN: 用于说明圆锥曲线题不是 toy domain，而是结构化几何概念与符号代数执行交汇的验证场景。 | EN: Use it to argue conic sections are not a toy domain but a testbed where structured geometry meets symbolic algebraic execution.
- What EGR should learn: CN: EGR 要区分自己与 Euclidean proof systems：重点在解析几何状态、定理模型、代数执行和答案抽取。 | EN: EGR should distinguish itself from Euclidean proof systems by emphasizing analytic-geometry state, theorem models, algebraic execution, and answer extraction.
- Figure/writing implication: CN: 适合做 AlphaGeometry/geometry prover vs EGR 的并列图。 | EN: Good for a side-by-side AlphaGeometry/geometry prover vs EGR figure.
- Priority: High

### 62. SymCode: A Neurosymbolic Approach to Mathematical Reasoning via Verifiable Code Generation

- Title: SymCode: A Neurosymbolic Approach to Mathematical Reasoning via Verifiable Code Generation
- Authors / 作者: Sina Bagheri Nezhad, Yao Li, Ameeta Agrawal, Vera Demberg, Kentaro Inui, Lluís Marquez
- Venue/Year / 会议年份: Findings 2026, 2026
- Zotero key(s) / Zotero 条目键: `QFMAC38N`
- Collection / 子集: Neuro-Symbolic
- Link / 链接: https://aclanthology.org/2026.findings-eacl.76/
- Problem: CN: 该工作研究如何把 LLM 数学推理从纯文本转成可执行、可验证的符号表示。 | EN: It studies how to convert LLM math reasoning from prose into executable and verifiable symbolic representations.
- Method: CN: 由 LLM 生成逻辑式、形式语言、符号规则、程序或公式结构，再交给求解器/验证器执行。 | EN: The LLM produces logic forms, formal language, symbolic rules, programs, or formula structures that a solver/verifier executes.
- Key claim/evidence: CN: 支持“神经模型负责提出，符号层负责执行/验证”的分工。 | EN: It supports the division where neural models propose and symbolic modules execute or verify.
- How EGR can cite it: CN: 用于说明 EGR 的 applicator 是可靠推理的核心执行层，而不是事后检查器。 | EN: Use it to argue that EGR's applicator is a core execution layer, not merely a post-hoc checker.
- What EGR should learn: CN: EGR 需要把 theorem model 定义为 precondition + symbolic transition。 | EN: EGR should define theorem models as precondition plus symbolic transition.
- Figure/writing implication: CN: 启发 “selector -> theorem model -> applicator -> new symbolic state” 方法图。 | EN: Useful for the method figure: selector -> theorem model -> applicator -> new symbolic state.
- Priority: High

### 63. Toward a Clearer Characterization of Neuro-Symbolic Frameworks: A Brief Comparative Analysis

- Title: Toward a Clearer Characterization of Neuro-Symbolic Frameworks: A Brief Comparative Analysis
- Authors / 作者: Sania Sinha, Tanawan Premsri, Parisa Kordjamshidi
- Venue/Year / 会议年份: Conference on Neurosymbolic Learning and Reasoning, 2025
- Zotero key(s) / Zotero 条目键: `J7E47TNE`
- Collection / 子集: Neuro-Symbolic
- Link / 链接: https://proceedings.mlr.press/v284/sinha25a.html
- Problem: CN: 该工作研究 neuro-symbolic 系统的结构、原则、比较维度或可解释性。 | EN: It studies the structure, principles, comparison dimensions, or interpretability of neuro-symbolic systems.
- Method: CN: 提出框架、设计原则、比较分析、符号表示或神经符号推理结构。 | EN: It proposes frameworks, design principles, comparative analyses, symbolic representations, or neurosymbolic reasoning structures.
- Key claim/evidence: CN: 帮助 EGR 避免泛泛说 hybrid，而是明确 neural/symbolic 分工和接口。 | EN: It helps EGR avoid a vague hybrid claim and specify neural/symbolic roles and interfaces.
- How EGR can cite it: CN: 用于 Related Work 中定义 EGR 属于哪一类 NeSy framework。 | EN: Use it in Related Work to define what kind of NeSy framework EGR is.
- What EGR should learn: CN: EGR 应强调 selector、applicator、state representation、trace 四个结构接口。 | EN: EGR should emphasize four structural interfaces: selector, applicator, state representation, and trace.
- Figure/writing implication: CN: 启发 neural-symbolic boundary 和 architecture overview。 | EN: Useful for the neural-symbolic boundary and architecture overview.
- Priority: Medium

### 64. Towards Learning to Reason: Comparing LLMs With Neuro-Symbolic on Arithmetic Relations in Abstract Reasoning

- Title: Towards Learning to Reason: Comparing LLMs With Neuro-Symbolic on Arithmetic Relations in Abstract Reasoning
- Authors / 作者: Michael Hersche, Giacomo Camposampiero, Roger Wattenhofer, Abu Sebastian, Abbas Rahimi
- Venue/Year / 会议年份: Neurosymbolic Artificial Intelligence, 2026
- Zotero key(s) / Zotero 条目键: `H2XJSPDG`
- Collection / 子集: Neuro-Symbolic
- Link / 链接: https://doi.org/10.1177/29498732261419316
- Problem: CN: 该工作研究 neuro-symbolic 系统的结构、原则、比较维度或可解释性。 | EN: It studies the structure, principles, comparison dimensions, or interpretability of neuro-symbolic systems.
- Method: CN: 提出框架、设计原则、比较分析、符号表示或神经符号推理结构。 | EN: It proposes frameworks, design principles, comparative analyses, symbolic representations, or neurosymbolic reasoning structures.
- Key claim/evidence: CN: 帮助 EGR 避免泛泛说 hybrid，而是明确 neural/symbolic 分工和接口。 | EN: It helps EGR avoid a vague hybrid claim and specify neural/symbolic roles and interfaces.
- How EGR can cite it: CN: 用于 Related Work 中定义 EGR 属于哪一类 NeSy framework。 | EN: Use it in Related Work to define what kind of NeSy framework EGR is.
- What EGR should learn: CN: EGR 应强调 selector、applicator、state representation、trace 四个结构接口。 | EN: EGR should emphasize four structural interfaces: selector, applicator, state representation, and trace.
- Figure/writing implication: CN: 启发 neural-symbolic boundary 和 architecture overview。 | EN: Useful for the neural-symbolic boundary and architecture overview.
- Priority: Medium

## 3. High-Priority Reading Queue / 优先精读队列

- 06. CoMAT: Chain of Mathematically Annotated Thought Improves Mathematical Reasoning - Method motivation: neural proposal should be separated from symbolic execution and verification.
- 07. CogMath: Assessing LLMs’ Authentic Mathematical Ability from a Human Cognitive Perspective - Introduction/Experiments: final-answer accuracy is insufficient; process-level reliability must be measured.
- 10. Enhancing Mathematical Reasoning in LLMs by Stepwise Correction - Introduction/Experiments: final-answer accuracy is insufficient; process-level reliability must be measured.
- 11. Error Classification of Large Language Models on Math Word Problems: A Dynamically Adaptive Framework - Introduction/Experiments: final-answer accuracy is insufficient; process-level reliability must be measured.
- 12. FLAIR: Steering LLM Mathematical Problem Solving based on A Fuzzy-Logic-AssIsted Reasoner - Method motivation: neural proposal should be separated from symbolic execution and verification.
- 14. Forward-Backward Reasoning in Large Language Models for Mathematical Verification - Introduction/Experiments: final-answer accuracy is insufficient; process-level reliability must be measured.
- 18. LLMs can Find Mathematical Reasoning Mistakes by Pedagogical Chain-of-Thought - Introduction/Experiments: final-answer accuracy is insufficient; process-level reliability must be measured.
- 19. LeanDojo: Theorem Proving with Retrieval-Augmented Language Models - Method motivation: mathematical reasoning can be modeled as state/action, premise/tactic, or theorem-model selection.
- 21. Let's Reason Formally: Natural-Formal Hybrid Reasoning Enhances LLM's Math Capability - Method motivation: neural proposal should be separated from symbolic execution and verification.
- 23. MATHSENSEI: A Tool-Augmented Large Language Model for Mathematical Reasoning - Method motivation: neural proposal should be separated from symbolic execution and verification.
- 26. Measuring Mathematical Problem Solving With the MATH Dataset - Related Work: surveys and position papers map the field and standard terminology.
- 29. Metacognitive Capabilities of LLMs: An Exploration in Mathematical Problem Solving - Introduction/Experiments: final-answer accuracy is insufficient; process-level reliability must be measured.
- 31. PAL: Program-aided Language Models - Method motivation: neural proposal should be separated from symbolic execution and verification.
- 32. Position: Formal Mathematical Reasoning—A New Frontier in AI - Method motivation: mathematical reasoning can be modeled as state/action, premise/tactic, or theorem-model selection.
- 33. Premise-Augmented Reasoning Chains Improve Error Identification in Math reasoning with LLMs - Introduction/Experiments: final-answer accuracy is insufficient; process-level reliability must be measured.
- 34. Program of Thoughts Prompting: Disentangling Computation from Reasoning for Numerical Reasoning Tasks - Method motivation: neural proposal should be separated from symbolic execution and verification.
- 35. Safe: Enhancing Mathematical Reasoning in Large Language Models via Retrospective Step-aware Formal Verification - Method motivation: neural proposal should be separated from symbolic execution and verification.
- 37. Step Guided Reasoning: Improving Mathematical Reasoning using Guidance Generation and Step Reasoning - Introduction/Experiments: final-answer accuracy is insufficient; process-level reliability must be measured.
- 38. Step-KTO: Optimizing Mathematical Reasoning through Stepwise Binary Feedback - Introduction/Experiments: final-answer accuracy is insufficient; process-level reliability must be measured.
- 40. Tree of Thoughts: Deliberate Problem Solving with Large Language Models - Introduction: text-chain reasoning improves LLM math but leaves mathematical validity implicit.
- 41. UDfSolver : Uniform representation and decoupled inference strategy for text-diagram function problems solving - Related Work: prior text-diagram/function solvers clarify EGR continuity and novelty.
- 46. A Neuro-Symbolic Approach for Reliable Proof Generation with LLMs: A Case Study in Euclidean Geometry - Introduction/Related Work: geometry and theorem proving validate state-conditioned neural-symbolic reasoning.
- 47. AXIOM: A Trust-First Neuro-Symbolic Execution Architecture for Verifiable Mathematical Reasoning - Method motivation: neural proposal should be separated from symbolic execution and verification.
- 51. Gold-medalist Performance in Solving Olympiad Geometry with AlphaGeometry2 - Introduction/Related Work: geometry and theorem proving validate state-conditioned neural-symbolic reasoning.
- 53. Intermediate Languages Matter: Formal Languages and LLMs affect Neurosymbolic Reasoning - Method motivation: representation and neural-symbolic interface design are core to reliable reasoning.
- 54. Logic-LM: Empowering Large Language Models with Symbolic Solvers for Faithful Logical Reasoning - Method motivation: neural proposal should be separated from symbolic execution and verification.
- 55. Neural Theorem Proving: Generating and Structuring Proofs for Formal Verification - Method motivation: mathematical reasoning can be modeled as state/action, premise/tactic, or theorem-model selection.
- 57. NeuroProlog: Multi-Task Fine-Tuning for Neurosymbolic Mathematical Reasoning via the Cocktail Effect - Method motivation: neural proposal should be separated from symbolic execution and verification.
- 60. Solving Math Word Problems by Combining Language Models With Symbolic Solvers - Method motivation: neural proposal should be separated from symbolic execution and verification.
- 61. Solving olympiad geometry without human demonstrations - Introduction/Related Work: geometry and theorem proving validate state-conditioned neural-symbolic reasoning.
- 62. SymCode: A Neurosymbolic Approach to Mathematical Reasoning via Verifiable Code Generation - Method motivation: neural proposal should be separated from symbolic execution and verification.
