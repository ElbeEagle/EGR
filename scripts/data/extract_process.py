"""
精简 train.json 数据集，只保留 text 和 process 字段
"""

import json

# 配置
INPUT_FILE = 'data/train.json'
OUTPUT_FILE = 'data/train_process.json'

# 读取数据
print(f"读取数据: {INPUT_FILE}")
with open(INPUT_FILE, 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f"总样本数: {len(data)}")

# 精简数据
simplified_data = []
for i, item in enumerate(data, 1):
    simplified_data.append({
        'id': i,
        'text': item.get('text', ''),
        'fact_expressions': item.get('fact_expressions', ''),
        'query_expressions': item.get('query_expressions', ''),
        'answer_expressions': item.get('answer_expressions', ''),
        'process': item.get('process', '')
    })

# 统计
original_size = len(json.dumps(data, ensure_ascii=False))
simplified_size = len(json.dumps(simplified_data, ensure_ascii=False))
estimated_tokens = simplified_size // 2.5

print(f"原始大小: {original_size:,} 字符")
print(f"精简后大小: {simplified_size:,} 字符")
print(f"压缩率: {(1 - simplified_size/original_size)*100:.1f}%")
print(f"估算tokens: {estimated_tokens:,.0f}")

# 保存
print(f"\n保存到: {OUTPUT_FILE}")
with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
    json.dump(simplified_data, f, indent=2, ensure_ascii=False)

print("✓ 完成！")