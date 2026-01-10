"""
极致压缩：只保留 process，纯文本格式
适合 Cursor 200K 上下文分析
"""

import json

# 配置
INPUT_FILE = 'data/train.json'
OUTPUT_FILE = 'data/train_process_compact.txt'

# 读取数据
print(f"读取数据: {INPUT_FILE}")
with open(INPUT_FILE, 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f"总样本数: {len(data)}")

# 统计
total_samples = len(data)
samples_with_process = sum(1 for item in data if item.get('process', '').strip())
samples_without_process = total_samples - samples_with_process

print(f"有process的样本: {samples_with_process}")
print(f"空process的样本: {samples_without_process}")

# 生成极简文本（只保留有process的样本）
lines = []
for i, item in enumerate(data, 1):
    process = item.get('process', '').strip()
    if process:  # 只保留非空的
        # 格式：[样本ID] 推理过程
        lines.append(f"[{i}] {process}")
        # lines.append(f"{process}")

# 合并为文本
output_text = '\n\n'.join(lines)

# 统计
original_size = len(json.dumps(data, ensure_ascii=False))
compact_size = len(output_text)
estimated_tokens = compact_size // 2.5

print(f"\n原始JSON大小: {original_size:,} 字符")
print(f"极简文本大小: {compact_size:,} 字符")
print(f"压缩率: {(1 - compact_size/original_size)*100:.1f}%")
print(f"估算tokens: {estimated_tokens:,.0f}")

if estimated_tokens <= 180000:
    print(f"✅ 适合200K上下文（剩余约 {200000 - estimated_tokens:,.0f} tokens）")
else:
    recommended_samples = int(samples_with_process * 180000 / estimated_tokens)
    print(f"⚠️ 仍超出！建议只分析前 {recommended_samples} 个样本")

# 保存
print(f"\n保存到: {OUTPUT_FILE}")
with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
    f.write("# 圆锥曲线问题推理过程数据集\n")
    f.write(f"# 共 {samples_with_process} 个有效样本\n")
    f.write(f"# 格式：[样本ID] 推理过程\n\n")
    f.write(output_text)

print("✓ 完成！")

# 生成使用说明
print("\n" + "="*60)
print("📖 使用方法")
print("="*60)
print(f"""
1. 在 Cursor 中打开: {OUTPUT_FILE}

2. 使用以下 prompt:
---
请分析这个数学推理过程数据集，识别最常用的数学定理和代数操作。

每个样本格式：[ID] 推理过程

请输出：
1. 最常用的数学定理（Top 30）
   - 定理名称
   - 使用频率
   - 公式/定义

2. 最常用的代数操作（Top 20）
   - 操作名称
   - 使用频率

3. 按圆锥曲线类型分类的定理
---
""")