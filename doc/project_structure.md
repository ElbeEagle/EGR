## 📂 项目目录结构

```
EGR/
├── Conic10K/                    # 数据集
│   └── conic10k/
│       ├── train.json
│       ├── dev.json
│       └── test.json
│
├── src/                         # 源代码
│   ├── state_abstractor.py     # 模块1
│   ├── data_constructor.py     # 模块2
│   ├── theorem_applicator.py   # 模块4
│   ├── reasoning_engine.py     # 模块5
│   ├── evaluation.py           # 模块6
│   ├── models/
│   │   ├── egr_model.py        # 模块3
│   │   └── tokenizer.py
│   └── theorems/
│       ├── theorem_library.py  # 模块0
│       └── basic_theorems.py
│
├── configs/                     # 配置文件
│   ├── model_config.yaml
│   └── training_config.yaml
│
├── tests/                       # 单元测试
│   ├── test_state_abstractor.py
│   ├── test_theorem_applicator.py
│   └── ...
│
├── notebooks/                   # 实验分析
│   ├── data_analysis.ipynb
│   └── results_analysis.ipynb
│
├── outputs/                     # 输出结果
│   ├── models/                  # 训练好的模型
│   ├── results/                 # 评估结果
│   └── logs/                    # 训练日志
│
└── doc/                         # 文档
    ├── phase1_project_workflow.md  # 本文档
    ├── theorem_library_spec.md     # 定理库规范
    └── paper_draft.md              # 论文草稿
```