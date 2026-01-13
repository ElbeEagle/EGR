import json
import os

def update_models_with_corrections(original_json_path, error_json_path, output_path):
    # 1. 加载主数据集
    with open(original_json_path, 'r', encoding='utf-8') as f:
        train_data = json.load(f)

    # 2. 加载修正补丁 (ID 是字符串 Key)
    with open(error_json_path, 'r', encoding='utf-8') as f:
        error_patches = json.load(f)

    # 3. 统计更新情况并执行更新
    updated_count = 0
    for item in train_data:
        item_id_str = str(item['id'])
        if item_id_str in error_patches:
            item['models'] = error_patches[item_id_str]
            updated_count += 1

    # 4. 按照要求的格式（ID首位，Models紧凑）保存文件
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("[\n")
        total = len(train_data)
        for i, item in enumerate(train_data):
            # 重新构建字典以确保 id 在最前面
            ordered_item = {"id": item["id"]}
            # 添加除 id 以外的其他字段
            for k, v in item.items():
                if k != "id":
                    ordered_item[k] = v
            
            # 提取 models 用于紧凑化处理
            models = ordered_item.get('models', [])
            ordered_item['models'] = "___COMPACT_MODELS___"
            
            # 生成带 4 空格缩进的 JSON 块
            item_str = json.dumps(ordered_item, ensure_ascii=False, indent=4)
            
            # 替换占位符为单行列表
            compact_models_str = json.dumps(models)
            item_str = item_str.replace('"___COMPACT_MODELS___"', compact_models_str)
            
            # 写入并处理块缩进
            f.write("    " + item_str.replace("\n", "\n    "))
            
            if i < total - 1:
                f.write(",")
            f.write("\n")
        f.write("]\n")

    print(f"成功！共从 {error_json_path} 更新了 {updated_count} 条数据。")
    print(f"新文件已保存至: {output_path}")

if __name__ == "__main__":
    update_models_with_corrections(
        'data/train_with_models_v1.json', 
        'data/data_process/process_models_error.json', 
        'data/train_with_models_v2.json'  # 建议保存为 v2，确认无误后再覆盖
    )