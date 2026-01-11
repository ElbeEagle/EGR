import json
import os

def merge_train_with_standard_indent(train_path, models_dir, output_path):
    # 1. 读取原始数据
    with open(train_path, 'r', encoding='utf-8') as f:
        train_data = json.load(f)

    # 2. 聚合 10 个分片的模型序列
    all_models = {}
    for i in range(1, 11):
        part_file = os.path.join(models_dir, f'process_models_part_{i}.json')
        if os.path.exists(part_file):
            with open(part_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                all_models.update({k: v for k, v in data.items() if k != "_meta"})

    # 3. 写入文件并控制字段顺序与格式
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("[\n")
        total = len(train_data)
        for i, item in enumerate(train_data):
            item_id = i + 1
            
            # 重新构建字典以确保 id 在最前面
            ordered_item = {"id": item_id}
            ordered_item.update(item)
            
            # 添加/更新 models 字段并使用占位符
            models = all_models.get(str(item_id), [])
            ordered_item['models'] = "___COMPACT_MODELS___"
            
            # 生成带 4 空格缩进的项字符串
            # 内部字段将相对于 { 缩进 4 格
            item_str = json.dumps(ordered_item, ensure_ascii=False, indent=4)
            
            # 将占位符替换为紧凑模式的列表字符串
            compact_models_str = json.dumps(models)
            item_str = item_str.replace('"___COMPACT_MODELS___"', compact_models_str)
            
            # 写入文件：
            # 1. 将整个块起始缩进 4 格
            # 2. 将块内的换行符后也补上 4 格缩进
            # 这样 { 在 4 格，内部字段在 8 格
            f.write("    " + item_str.replace("\n", "\n    "))
            
            if i < total - 1:
                f.write(",")
            f.write("\n")
        f.write("]\n")

if __name__ == "__main__":
    merge_train_with_standard_indent(
        'data/train.json', 
        'data/data_process/', 
        'data/train_with_models.json'
    )