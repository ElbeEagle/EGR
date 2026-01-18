"""
分析未实现模型的调用频率
"""

import json
import sys
from pathlib import Path
from collections import Counter

# 添加src到路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.theorems import TheoremLibrary


def main():
    """主函数"""
    # 数据路径
    data_path = project_root / "data" / "train_with_models_1_100.json"
    model_ids_path = project_root / "model" / "conic_model_ids.json"
    
    print("=" * 80)
    print("  未实现模型调用频率分析")
    print("=" * 80)
    
    # 加载数据
    with open(data_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 加载模型ID映射
    with open(model_ids_path, 'r', encoding='utf-8') as f:
        model_id_map = json.load(f)
    
    # 反向映射：ID -> 名称
    id_to_name = {v: k for k, v in model_id_map.items()}
    
    # 创建定理库
    library = TheoremLibrary()
    implemented_models = set(library.get_available_models())
    
    print(f"\n已实现模型: {len(implemented_models)}/80")
    
    # 统计前50个样本中所有模型的调用
    all_models = []
    missing_models = []
    sample_count = 0
    
    for sample in data:
        if not sample.get('models'):
            continue
        
        models = sample['models']
        all_models.extend(models)
        
        # 找出未实现的模型
        for model_id in models:
            if model_id not in implemented_models:
                missing_models.append(model_id)
        
        sample_count += 1
        if sample_count >= 50:
            break
    
    # 统计频率
    all_counter = Counter(all_models)
    missing_counter = Counter(missing_models)
    
    print(f"\n前50个样本统计:")
    print(f"  - 样本数: {sample_count}")
    print(f"  - 模型调用总次数: {len(all_models)}")
    print(f"  - 未实现模型调用次数: {len(missing_models)} ({len(missing_models)/len(all_models)*100:.1f}%)")
    print(f"  - 涉及未实现模型种类: {len(missing_counter)}")
    
    # 显示未实现模型排名
    print(f"\n未实现模型调用频率 Top 20:")
    print(f"{'排名':<6} {'模型ID':<8} {'调用次数':<10} {'模型名称':<50}")
    print("-" * 80)
    
    for rank, (model_id, count) in enumerate(missing_counter.most_common(20), 1):
        model_name = id_to_name.get(model_id, "Unknown")
        print(f"{rank:<6} {model_id:<8} {count:<10} {model_name:<50}")
    
    # 显示高频模型（包括已实现和未实现）
    print(f"\n\n所有模型调用频率 Top 20:")
    print(f"{'排名':<6} {'模型ID':<8} {'调用次数':<10} {'状态':<10} {'模型名称':<40}")
    print("-" * 80)
    
    for rank, (model_id, count) in enumerate(all_counter.most_common(20), 1):
        model_name = id_to_name.get(model_id, "Unknown")
        status = "✅ 已实现" if model_id in implemented_models else "❌ 未实现"
        print(f"{rank:<6} {model_id:<8} {count:<10} {status:<10} {model_name:<40}")
    
    # 分析潜在收益
    print(f"\n\n潜在收益分析:")
    print(f"{'实现数量':<12} {'覆盖调用次数':<15} {'占未实现比例':<15} {'模型ID':<30}")
    print("-" * 80)
    
    cumulative = 0
    models_to_implement = []
    for model_id, count in missing_counter.most_common():
        cumulative += count
        models_to_implement.append(model_id)
        if len(models_to_implement) in [5, 10, 15, 20]:
            percentage = cumulative / len(missing_models) * 100
            print(f"{len(models_to_implement):<12} {cumulative:<15} {percentage:<15.1f}% {str(models_to_implement[-5:]):<30}")
    
    print("\n" + "=" * 80)


if __name__ == "__main__":
    main()
