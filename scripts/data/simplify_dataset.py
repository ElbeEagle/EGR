"""
精简 Conic10K 数据集，只保留题目和推理过程
用于直接传给 Cursor AI Agent 分析定理模式
"""

import json
import sys
from pathlib import Path


def simplify_dataset(
    input_path: str,
    output_path: str,
    keep_field: str = 'text',
    max_samples: int = None,
    only_with_process: bool = True
):
    """
    精简数据集，只保留关键字段
    
    Args:
        input_path: 输入文件路径 (如 Conic10K/conic10k/train.json)
        output_path: 输出文件路径 (如 scripts/data/simplified_train.json)
        keep_field: 保留的题目字段，'text' 或 'fact_expressions'
        max_samples: 最大样本数，None表示全部
        only_with_process: 是否只保留有process的样本
    """
    
    print("="*80)
    print("精简 Conic10K 数据集")
    print("="*80)
    
    # 读取数据
    print(f"\n1. 读取数据: {input_path}")
    with open(input_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print(f"   总样本数: {len(data)}")
    
    # 筛选样本
    if only_with_process:
        filtered_data = [
            item for item in data 
            if item.get('process', '').strip()
        ]
        print(f"   有process的样本: {len(filtered_data)}")
    else:
        filtered_data = data
    
    # 限制样本数
    if max_samples and len(filtered_data) > max_samples:
        filtered_data = filtered_data[:max_samples]
        print(f"   截取前 {max_samples} 个样本")
    
    # 精简数据结构
    print(f"\n2. 精简数据（保留字段: id, {keep_field}, process）")
    simplified_data = []
    
    total_chars_before = 0
    total_chars_after = 0
    
    for i, item in enumerate(filtered_data, 1):
        # 计算原始大小
        original_str = json.dumps(item, ensure_ascii=False)
        total_chars_before += len(original_str)
        
        # 创建精简版本
        simplified_item = {
            'id': i,
            'question': item.get(keep_field, ''),
            'process': item.get('process', '')
        }
        
        # 计算精简后大小
        simplified_str = json.dumps(simplified_item, ensure_ascii=False)
        total_chars_after += len(simplified_str)
        
        simplified_data.append(simplified_item)
    
    # 统计信息
    print(f"\n3. 统计信息:")
    print(f"   精简后样本数: {len(simplified_data)}")
    print(f"   原始总字符数: {total_chars_before:,}")
    print(f"   精简后字符数: {total_chars_after:,}")
    print(f"   压缩率: {(1 - total_chars_after/total_chars_before)*100:.1f}%")
    print(f"   估算tokens: {total_chars_after // 2.5:,.0f}")
    
    # 评估是否适合200K上下文
    estimated_tokens = total_chars_after // 2.5
    if estimated_tokens <= 180000:  # 留20K给prompt和输出
        print(f"   ✅ 适合200K上下文（剩余约 {200000 - estimated_tokens:,.0f} tokens）")
    else:
        print(f"   ⚠️  超出200K上下文！需要减少到约 {int(len(simplified_data) * 180000 / estimated_tokens)} 个样本")
    
    # 保存结果
    print(f"\n4. 保存到: {output_path}")
    
    # 确保输出目录存在
    output_dir = Path(output_path).parent
    output_dir.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(simplified_data, f, indent=2, ensure_ascii=False)
    
    print(f"   ✓ 保存成功")
    
    # 生成分析prompt建议
    print("\n" + "="*80)
    print("💡 使用建议")
    print("="*80)
    print(f"""
1. 在 Cursor 中打开: {output_path}

2. 使用以下 prompt 让 AI Agent 分析:

---
请分析这个数学问题数据集，识别出最常用的数学定理和代数操作。

数据格式：
- question: 问题描述
- process: 求解过程

请输出：
1. 最常用的数学定理（Top 30），按频率排序
   格式：定理名称 | 使用次数 | 定义/公式
   
2. 最常用的代数操作（Top 20），按频率排序
   格式：操作名称 | 使用次数 | 说明

3. 定理分类（按圆锥曲线类型）：
   - 椭圆相关定理
   - 双曲线相关定理
   - 抛物线相关定理
   - 通用定理

请详细分析，给出具体例子。
---

3. 或者将数据分成多批次分析：
   - 第1批: 样本 1-1000
   - 第2批: 样本 1001-2000
   - ...
""")
    
    return simplified_data


def create_batches(
    input_path: str,
    output_dir: str,
    batch_size: int = 1000,
    keep_field: str = 'text'
):
    """
    创建多个批次文件，每个批次适合200K上下文
    
    Args:
        input_path: 输入文件路径
        output_dir: 输出目录
        batch_size: 每批次样本数
        keep_field: 保留的题目字段
    """
    
    print("="*80)
    print("创建批次文件")
    print("="*80)
    
    # 读取数据
    print(f"\n读取数据: {input_path}")
    with open(input_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 筛选有process的样本
    filtered_data = [
        item for item in data 
        if item.get('process', '').strip()
    ]
    
    print(f"总样本数: {len(data)}")
    print(f"有process的样本: {len(filtered_data)}")
    
    # 计算批次数
    num_batches = (len(filtered_data) + batch_size - 1) // batch_size
    print(f"批次数: {num_batches} (每批次 {batch_size} 个样本)")
    
    # 创建输出目录
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # 生成批次文件
    for batch_idx in range(num_batches):
        start_idx = batch_idx * batch_size
        end_idx = min(start_idx + batch_size, len(filtered_data))
        
        batch_data = filtered_data[start_idx:end_idx]
        
        # 精简数据
        simplified_batch = []
        for i, item in enumerate(batch_data, start_idx + 1):
            simplified_batch.append({
                'id': i,
                'question': item.get(keep_field, ''),
                'process': item.get('process', '')
            })
        
        # 保存批次文件
        batch_file = output_path / f'batch_{batch_idx+1:02d}_samples_{start_idx+1}-{end_idx}.json'
        with open(batch_file, 'w', encoding='utf-8') as f:
            json.dump(simplified_batch, f, indent=2, ensure_ascii=False)
        
        # 统计
        batch_str = json.dumps(simplified_batch, ensure_ascii=False)
        estimated_tokens = len(batch_str) // 2.5
        
        print(f"  批次 {batch_idx+1}: {batch_file.name}")
        print(f"    样本: {start_idx+1}-{end_idx} ({len(simplified_batch)}个)")
        print(f"    估算tokens: {estimated_tokens:,.0f}")
    
    print(f"\n✓ 所有批次文件已保存到: {output_dir}")


def main():
    """主函数"""
    
    # ========== 配置 ==========
    INPUT_PATH = 'Conic10K/conic10k/train.json'
    
    # 选项1: 生成单个精简文件（推荐用于快速测试）
    OUTPUT_SINGLE = 'scripts/data/simplified_train.json'
    MAX_SAMPLES = 1000  # 约1000个样本适合200K上下文，None表示全部
    
    # 选项2: 生成多个批次文件（推荐用于完整分析）
    OUTPUT_BATCH_DIR = 'scripts/data/batches'
    BATCH_SIZE = 1000
    
    # ========== 选择执行模式 ==========
    print("请选择模式：")
    print("1. 生成单个精简文件（快速测试，默认1000个样本）")
    print("2. 生成多个批次文件（完整分析，每批次1000个样本）")
    print("3. 生成单个精简文件（全部样本）")
    
    choice = input("\n请输入选项 [1/2/3, 默认1]: ").strip() or "1"
    
    if choice == "1":
        print("\n选择: 生成单个精简文件（1000个样本）\n")
        simplify_dataset(
            input_path=INPUT_PATH,
            output_path=OUTPUT_SINGLE,
            keep_field='text',
            max_samples=MAX_SAMPLES,
            only_with_process=True
        )
    
    elif choice == "2":
        print("\n选择: 生成多个批次文件\n")
        create_batches(
            input_path=INPUT_PATH,
            output_dir=OUTPUT_BATCH_DIR,
            batch_size=BATCH_SIZE,
            keep_field='text'
        )
    
    elif choice == "3":
        print("\n选择: 生成单个精简文件（全部样本）\n")
        simplify_dataset(
            input_path=INPUT_PATH,
            output_path=OUTPUT_SINGLE,
            keep_field='text',
            max_samples=None,
            only_with_process=True
        )
    
    else:
        print("无效选项！")
        return
    
    print("\n" + "="*80)
    print("✓ 完成！")
    print("="*80)


if __name__ == '__main__':
    main()

