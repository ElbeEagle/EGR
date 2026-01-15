import json
import os

def extract_train_part(input_path, output_path, start_id, end_id):
    # 1. 读取主数据集
    if not os.path.exists(input_path):
        print(f"错误：找不到文件 {input_path}")
        return

    with open(input_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # 2. 筛选指定范围的 ID
    part_data = [item for item in data if start_id <= item['id'] <= end_id]

    # 3. 按照标准格式保存文件（ID首位，Models紧凑）
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("[\n")
        total = len(part_data)
        for i, item in enumerate(part_data):
            # 确保 id 在最前面
            ordered_item = {"id": item["id"]}
            for k, v in item.items():
                if k != "id":
                    ordered_item[k] = v
            
            # 紧凑化处理 models 字段
            models = ordered_item.get('models', [])
            ordered_item['models'] = "___COMPACT_MODELS___"
            
            # 生成带缩进的字符串
            item_str = json.dumps(ordered_item, ensure_ascii=False, indent=4)
            
            # 替换占位符
            compact_models_str = json.dumps(models)
            item_str = item_str.replace('"___COMPACT_MODELS___"', compact_models_str)
            
            # 写入并添加整体缩进
            f.write("    " + item_str.replace("\n", "\n    "))
            
            if i < total - 1:
                f.write(",")
            f.write("\n")
        f.write("]\n")

    print(f"成功！已提取 {len(part_data)} 项数据到 {output_path}")

if __name__ == "__main__":
    extract_train_part(
        'data/train_with_models_v2.json', 
        'data/train_with_models_1_100.json', 
        1, 
        100
    )