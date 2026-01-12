import json
import re
import os

def extract_error_details(txt_path, full_data_path, output_path):
    # 1. 解析 TXT 文件提取所有出现的 ID
    error_ids = []
    pattern = re.compile(r'^\[(\d+)\]') # 匹配行首的 [ID]

    if not os.path.exists(txt_path):
        print(f"错误：找不到文件 {txt_path}")
        return

    with open(txt_path, 'r', encoding='utf-8') as f:
        for line in f:
            match = pattern.match(line.strip())
            if match:
                error_ids.append(int(match.group(1)))
    
    if not error_ids:
        print("未在 TXT 文件中找到任何有效 ID。")
        return

    # 2. 加载包含完整信息的 train_with_models.json
    if not os.path.exists(full_data_path):
        print(f"错误：找不到文件 {full_data_path}")
        return

    with open(full_data_path, 'r', encoding='utf-8') as f:
        full_data = json.load(f)

    # 3. 建立 ID 索引字典，提高查找效率
    data_lookup = {item['id']: item for item in full_data if 'id' in item}

    # 4. 提取对应的 text 和 process
    result_items = []
    for eid in error_ids:
        if eid in data_lookup:
            source = data_lookup[eid]
            result_items.append({
                "id": eid,
                "text": source.get("text", ""),
                "process": source.get("process", "")
            })
        else:
            print(f"警告：ID {eid} 在 {full_data_path} 中未找到")

    # 5. 保存结果
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(result_items, f, ensure_ascii=False, indent=4)

    print(f"完成！共提取 {len(result_items)} 项数据到 {output_path}")

if __name__ == "__main__":
    extract_error_details(
        'data/data_process/train_process_error.txt', 
        'data/train_with_models.json', 
        'data/data_process/train_process_error_details.json'
    )