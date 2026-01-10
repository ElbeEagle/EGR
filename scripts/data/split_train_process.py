"""
将 train_process.txt 数据集，分割成 10 个文件，每个文件包含 536 个样本。
"""

import os

def split_train_process(input_file, output_dir, num_parts=10):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # 提取所有样本项（跳过注释行和空行）
    items = [line for line in lines if line.strip() and line.startswith('[')]
    
    total_items = len(items)
    size = total_items // num_parts
    remainder = total_items % num_parts

    start = 0
    for i in range(num_parts):
        # 均匀分配剩余项
        end = start + size + (1 if i < remainder else 0)
        part_items = items[start:end]
        
        output_file = os.path.join(output_dir, f'train_process_part_{i+1}.txt')
        with open(output_file, 'w', encoding='utf-8') as f_out:
            f_out.writelines(part_items)
        
        print(f"Saved {len(part_items)} items to {output_file}")
        start = end

if __name__ == "__main__":
    split_train_process('data/train_process.txt', 'data/data_process/')