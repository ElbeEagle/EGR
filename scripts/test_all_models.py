"""
测试所有已实现的模型

测试多个样本，验证模型序列应用
"""

import json
import sys
from pathlib import Path

# 添加src到路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.state import StateConstructor
from src.theorems import TheoremLibrary


def print_separator(title: str):
    """打印分隔符"""
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80 + "\n")


def test_sample_sequence(sample: dict, constructor: StateConstructor, library: TheoremLibrary):
    """
    测试单个样本的完整模型序列
    
    Returns:
        dict: 测试结果统计
    """
    sample_id = sample['id']
    models = sample.get('models', [])
    
    if not models:
        return None
    
    print(f"\n【样本 ID={sample_id}】")
    print(f"题目: {sample['text'][:60]}...")
    print(f"模型序列: {models}")
    
    # 构建初始状态
    abstract_state, symbolic_state = constructor.construct_from_facts(
        sample['fact_expressions'],
        sample['query_expressions'],
        reasoning_depth=0
    )
    
    print(f"初始完整度: {abstract_state.completeness_score:.2f}")
    
    # 逐步应用模型
    success_count = 0
    fail_count = 0
    not_implemented = 0
    
    for i, model_id in enumerate(models):
        # 检查模型是否存在
        if not library.has_model(model_id):
            print(f"  Model {model_id}: ❌ 未实现")
            not_implemented += 1
            continue
        
        model = library.get_model(model_id)
        
        # 检查前置条件
        if not model.can_apply(symbolic_state):
            print(f"  Model {model_id} ({model.chinese_name}): ❌ 前置条件不满足")
            fail_count += 1
            continue
        
        # 应用模型
        try:
            model.apply(symbolic_state)
            
            # 重新构建抽象状态
            abstract_state = constructor.construct_from_symbolic_state(
                symbolic_state,
                sample['query_expressions'],
                reasoning_depth=i + 1
            )
            
            print(f"  Model {model_id} ({model.chinese_name}): ✅ 完整度 {abstract_state.completeness_score:.2f}")
            success_count += 1
            
        except Exception as e:
            print(f"  Model {model_id}: ❌ 应用失败 - {str(e)}")
            fail_count += 1
    
    # 最终状态
    print(f"最终完整度: {abstract_state.completeness_score:.2f}")
    print(f"参数数量: {len(symbolic_state.parameters)}")
    print(f"已应用: {symbolic_state.applied_models}")
    
    return {
        'sample_id': sample_id,
        'total': len(models),
        'success': success_count,
        'fail': fail_count,
        'not_implemented': not_implemented,
        'completeness': abstract_state.completeness_score
    }


def main():
    """主函数"""
    # 数据路径
    data_path = project_root / "data" / "train_with_models_1_100.json"
    
    print_separator("所有模型综合测试")
    print(f"数据路径: {data_path}")
    
    # 加载数据
    print("\n正在加载数据...")
    with open(data_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    print(f"✓ 加载完成，共 {len(data)} 个样本")
    
    # 创建构造器和定理库
    constructor = StateConstructor()
    library = TheoremLibrary()
    
    print(f"\n定理库状态: {library}")
    print(f"已注册模型: {library.get_available_models()}")
    
    print_separator("开始测试样本")
    
    # 测试所有有模型序列的样本
    results = []
    for sample in data:
        if not sample.get('models'):
            continue
        
        result = test_sample_sequence(sample, constructor, library)
        if result:
            results.append(result)
        
        # 测试前10个样本
        if len(results) >= 10:
            break
    
    # 统计结果
    print_separator("测试结果汇总")
    
    total_models = sum(r['total'] for r in results)
    total_success = sum(r['success'] for r in results)
    total_fail = sum(r['fail'] for r in results)
    total_not_impl = sum(r['not_implemented'] for r in results)
    
    print(f"测试样本数: {len(results)}")
    print(f"模型调用总数: {total_models}")
    print(f"  - 成功: {total_success} ({total_success/total_models*100:.1f}%)")
    print(f"  - 失败: {total_fail} ({total_fail/total_models*100:.1f}%)")
    print(f"  - 未实现: {total_not_impl} ({total_not_impl/total_models*100:.1f}%)")
    
    # 完整度统计
    avg_completeness = sum(r['completeness'] for r in results) / len(results)
    print(f"\n平均最终完整度: {avg_completeness:.2f}")
    
    # 按样本列表
    print("\n样本详情:")
    print(f"{'样本ID':<8} {'模型数':<8} {'成功':<6} {'完整度':<8}")
    print("-" * 40)
    for r in results:
        print(f"{r['sample_id']:<8} {r['total']:<8} {r['success']:<6} {r['completeness']:<8.2f}")
    
    if total_success == total_models - total_not_impl:
        print("\n🎉 所有已实现的模型测试通过！")
    else:
        print(f"\n⚠️  {total_fail} 个模型调用失败")


if __name__ == "__main__":
    main()
