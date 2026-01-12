

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




---

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
> 存储定位："data/analysis_report.md" "data/analysis_results.json"

此外抽样了500个样本由LLM进行细致分析，由些小问题

> 存储定位："data/sampled_problems.md"
> 存储定位："data/detailed_sequence_analysis.md"

---
