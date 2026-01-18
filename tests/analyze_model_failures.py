"""
分析模型失败原因和失败率
"""

import json
import sys
from pathlib import Path
from collections import Counter

# 添加src到路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.state import StateConstructor
from src.theorems import TheoremLibrary


def main():
    """主函数"""
    # 数据路径
    data_path = project_root / "data" / "train_with_models_1_100.json"
    model_ids_path = project_root / "model" / "conic_model_ids.json"
    
    print("=" * 80)
    print("  模型失败原因分析")
    print("=" * 80)
    
    # 加载数据
    with open(data_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 加载模型ID映射
    with open(model_ids_path, 'r', encoding='utf-8') as f:
        model_id_map = json.load(f)
    
    # 反向映射：ID -> 名称
    id_to_name = {v: k for k, v in model_id_map.items()}
    
    # 创建定理库和构造器
    library = TheoremLibrary()
    constructor = StateConstructor(theorem_library=library)
    
    print(f"\n已实现模型: {len(library.get_available_models())}/80")
    
    # 统计失败的模型
    model_failures = Counter()
    model_attempts = Counter()
    failure_samples = {}
    
    sample_count = 0
    for sample in data:
        if not sample.get('models'):
            continue
        
        # 构建初始状态
        abstract_state, symbolic_state = constructor.construct_from_facts(
            sample['fact_expressions'],
            sample['query_expressions'],
            reasoning_depth=0
        )
        
        # 逐步应用模型
        for model_id in sample['models']:
            if not library.has_model(model_id):
                continue
            
            model = library.get_model(model_id)
            model_attempts[model_id] += 1
            
            if not model.can_apply(symbolic_state):
                model_failures[model_id] += 1
                if model_id not in failure_samples:
                    failure_samples[model_id] = []
                failure_samples[model_id].append({
                    'sample_id': sample['id'],
                    'text': sample['text'][:80],
                    'params': list(symbolic_state.parameters.keys()),
                    'entities': list(symbolic_state.entities.values())
                })
            else:
                # 应用成功
                try:
                    model.apply(symbolic_state)
                except:
                    pass
        
        sample_count += 1
        if sample_count >= 50:
            break
    
    # 计算失败率
    failure_rates = {}
    for model_id, failures in model_failures.items():
        attempts = model_attempts[model_id]
        failure_rates[model_id] = (failures, attempts, failures / attempts * 100)
    
    # 按失败率排序
    sorted_failures = sorted(failure_rates.items(), key=lambda x: x[1][2], reverse=True)
    
    print(f"\n前50个样本统计:")
    print(f"  - 样本数: {sample_count}")
    print(f"  - 模型调用次数: {sum(model_attempts.values())}")
    print(f"  - 失败次数: {sum(model_failures.values())} ({sum(model_failures.values())/sum(model_attempts.values())*100:.1f}%)")
    
    print(f"\n模型失败率 Top 15:")
    print(f"{'排名':<6} {'模型ID':<8} {'失败次数':<10} {'调用次数':<10} {'失败率':<10} {'模型名称':<40}")
    print("-" * 90)
    
    for rank, (model_id, (failures, attempts, rate)) in enumerate(sorted_failures[:15], 1):
        model_name = id_to_name.get(model_id, "Unknown")
        print(f"{rank:<6} {model_id:<8} {failures:<10} {attempts:<10} {rate:<10.1f}% {model_name:<40}")
    
    # 显示失败次数最多的模型详情
    print(f"\n\n失败次数最多的模型详细分析:")
    for rank, (model_id, (failures, attempts, rate)) in enumerate(sorted_failures[:5], 1):
        model_name = id_to_name.get(model_id, "Unknown")
        print(f"\n{'='*80}")
        print(f"排名 {rank}: Model {model_id} - {model_name}")
        print(f"失败率: {failures}/{attempts} ({rate:.1f}%)")
        print(f"\n失败样本示例:")
        
        for i, failure in enumerate(failure_samples[model_id][:3], 1):
            print(f"\n  样本 {i} (ID={failure['sample_id']}):")
            print(f"    题目: {failure['text']}...")
            print(f"    实体: {failure['entities']}")
            print(f"    参数: {failure['params']}")
    
    print("\n" + "=" * 80)


if __name__ == "__main__":
    main()
