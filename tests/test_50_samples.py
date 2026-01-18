"""
测试前50个样本的模型应用成功率
"""

import json
import sys
from pathlib import Path

# 添加src到路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.state import StateConstructor
from src.theorems import TheoremLibrary


def test_sample(sample: dict, constructor: StateConstructor, library: TheoremLibrary):
    """测试单个样本"""
    sample_id = sample['id']
    models = sample.get('models', [])
    
    if not models:
        return None
    
    # 构建初始状态
    abstract_state, symbolic_state = constructor.construct_from_facts(
        sample['fact_expressions'],
        sample['query_expressions'],
        reasoning_depth=0
    )
    
    # 逐步应用模型
    success_count = 0
    fail_count = 0
    not_implemented = 0
    
    for model_id in models:
        if not library.has_model(model_id):
            not_implemented += 1
            continue
        
        model = library.get_model(model_id)
        
        if not model.can_apply(symbolic_state):
            fail_count += 1
            continue
        
        try:
            model.apply(symbolic_state)
            success_count += 1
        except Exception as e:
            fail_count += 1
    
    return {
        'sample_id': sample_id,
        'total': len(models),
        'success': success_count,
        'fail': fail_count,
        'not_implemented': not_implemented,
        'success_rate': success_count / len(models) if len(models) > 0 else 0
    }


def main():
    """主函数"""
    # 数据路径
    data_path = project_root / "data" / "train_with_models_1_100.json"
    
    print("=" * 80)
    print("  测试前50个样本")
    print("=" * 80)
    
    # 加载数据
    with open(data_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 创建定理库和构造器
    library = TheoremLibrary()
    constructor = StateConstructor(theorem_library=library)
    
    print(f"\n定理库: {len(library.get_available_models())}/80 个模型")
    
    # 测试前50个有模型序列的样本
    results = []
    sample_count = 0
    
    for sample in data:
        if not sample.get('models'):
            continue
        
        result = test_sample(sample, constructor, library)
        if result:
            results.append(result)
            sample_count += 1
        
        if sample_count >= 50:
            break
    
    # 统计结果
    print(f"\n测试样本数: {len(results)}")
    
    total_models = sum(r['total'] for r in results)
    total_success = sum(r['success'] for r in results)
    total_fail = sum(r['fail'] for r in results)
    total_not_impl = sum(r['not_implemented'] for r in results)
    
    overall_success_rate = total_success / total_models * 100 if total_models > 0 else 0
    
    print(f"\n模型调用总数: {total_models}")
    print(f"  - 成功: {total_success} ({total_success/total_models*100:.1f}%)")
    print(f"  - 失败: {total_fail} ({total_fail/total_models*100:.1f}%)")
    print(f"  - 未实现: {total_not_impl} ({total_not_impl/total_models*100:.1f}%)")
    
    print(f"\n总体成功率: {overall_success_rate:.1f}%")
    
    # 按成功率分类
    perfect = [r for r in results if r['success'] == r['total']]
    partial = [r for r in results if 0 < r['success'] < r['total']]
    failed = [r for r in results if r['success'] == 0]
    
    print(f"\n样本分类:")
    print(f"  - 完全成功: {len(perfect)} ({len(perfect)/len(results)*100:.1f}%)")
    print(f"  - 部分成功: {len(partial)} ({len(partial)/len(results)*100:.1f}%)")
    print(f"  - 完全失败: {len(failed)} ({len(failed)/len(results)*100:.1f}%)")
    
    # 显示成功率分布
    print(f"\n成功率分布:")
    bins = [0, 0.25, 0.5, 0.75, 1.0]
    for i in range(len(bins)-1):
        count = sum(1 for r in results if bins[i] <= r['success_rate'] < bins[i+1])
        if i == len(bins)-2:  # 最后一个区间包含1.0
            count = sum(1 for r in results if bins[i] <= r['success_rate'] <= bins[i+1])
        print(f"  {int(bins[i]*100)}-{int(bins[i+1]*100)}%: {count} 个样本")
    
    print("\n" + "=" * 80)


if __name__ == "__main__":
    main()
