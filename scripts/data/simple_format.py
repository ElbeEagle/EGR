"""
精简 process_models_part_2.json 数据集，只保留 _meta 和样本数据，样本数据不换行和缩紧。
"""

import json

def simplify_json_format(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write("{\n")
        
        # 处理 _meta 部分（保持缩进）
        if "_meta" in data:
            meta_str = json.dumps(data["_meta"], indent=2, ensure_ascii=False)
            f.write('  "_meta": ' + meta_str.replace('\n', '\n  ') + ',\n')
        
        # 处理样本数据（单行格式）
        items = [(k, v) for k, v in data.items() if k != "_meta"]
        for i, (k, v) in enumerate(items):
            comma = "," if i < len(items) - 1 else ""
            f.write(f'  "{k}": {json.dumps(v)}{comma}\n')
            
        f.write("}\n")

if __name__ == "__main__":
    simplify_json_format('data/data_process/process_models_part_2.json')