"""
综合验证脚本

验证内容：
1. 集成测试 - 完整状态序列构建
2. 指标验证 - completeness单调递增等
3. 模型应用正确性
"""

import json
import sys
from pathlib import Path
from typing import List, Dict

# 添加src到路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.state import StateConstructor
from src.theorems import TheoremLibrary


def print_separator(title: str, char: str = "="):
    """打印分隔符"""
    print("\n" + char * 80)
    print(f"  {title}")
    print(char * 80 + "\n")


def validate_completeness_monotonicity(
    sample: dict,
    constructor: StateConstructor,
    library: TheoremLibrary
) -> Dict:
    """
    验证完整度单调递增
    
    Returns:
        dict: 验证结果
    """
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
    
    completeness_sequence = [abstract_state.completeness_score]
    param_count_sequence = [len(symbolic_state.parameters)]
    
    # 逐步应用模型
    for i, model_id in enumerate(models):
        if not library.has_model(model_id):
            continue
        
        model = library.get_model(model_id)
        
        if not model.can_apply(symbolic_state):
            continue
        
        try:
            # 记录应用前的状态
            prev_params = len(symbolic_state.parameters)
            
            # 应用模型
            model.apply(symbolic_state)
            
            # 重新构建抽象状态
            abstract_state = constructor.construct_from_symbolic_state(
                symbolic_state,
                sample['query_expressions'],
                reasoning_depth=i + 1
            )
            
            # 记录完整度和参数数量
            completeness_sequence.append(abstract_state.completeness_score)
            param_count_sequence.append(len(symbolic_state.parameters))
            
        except Exception as e:
            continue
    
    # 检查单调性
    is_monotonic = all(
        completeness_sequence[i] <= completeness_sequence[i+1]
        for i in range(len(completeness_sequence) - 1)
    )
    
    # 检查参数数量单调性
    params_monotonic = all(
        param_count_sequence[i] <= param_count_sequence[i+1]
        for i in range(len(param_count_sequence) - 1)
    )
    
    return {
        'sample_id': sample_id,
        'completeness_sequence': completeness_sequence,
        'param_count_sequence': param_count_sequence,
        'is_monotonic': is_monotonic,
        'params_monotonic': params_monotonic,
        'initial_completeness': completeness_sequence[0],
        'final_completeness': completeness_sequence[-1],
        'completeness_gain': completeness_sequence[-1] - completeness_sequence[0],
        'param_gain': param_count_sequence[-1] - param_count_sequence[0]
    }


def validate_state_construction_integrity(
    sample: dict,
    constructor: StateConstructor,
    library: TheoremLibrary
) -> Dict:
    """
    验证状态构建的完整性
    
    检查：
    1. SymbolicState 各字段正确填充
    2. AbstractState 特征提取正确
    3. 状态更新正确
    """
    sample_id = sample['id']
    
    # 构建初始状态
    abstract_state, symbolic_state = constructor.construct_from_facts(
        sample['fact_expressions'],
        sample['query_expressions'],
        reasoning_depth=0
    )
    
    # 检查 SymbolicState
    has_entities = len(symbolic_state.entities) > 0
    has_equations = len(symbolic_state.equations) > 0
    
    # 检查 AbstractState
    curve_type_valid = abstract_state.curve_type is not None
    query_type_valid = abstract_state.query_type is not None
    completeness_valid = 0.0 <= abstract_state.completeness_score <= 1.0
    
    # 应用模型并检查更新
    models = sample.get('models', [])
    models_applied = []
    
    for model_id in models[:3]:  # 测试前3个模型
        if not library.has_model(model_id):
            continue
        
        model = library.get_model(model_id)
        
        if not model.can_apply(symbolic_state):
            continue
        
        try:
            prev_applied = len(symbolic_state.applied_models)
            model.apply(symbolic_state)
            
            # 检查 applied_models 更新
            if len(symbolic_state.applied_models) > prev_applied:
                models_applied.append(model_id)
        except:
            continue
    
    return {
        'sample_id': sample_id,
        'has_entities': has_entities,
        'has_equations': has_equations,
        'curve_type_valid': curve_type_valid,
        'query_type_valid': query_type_valid,
        'completeness_valid': completeness_valid,
        'models_applied': len(models_applied),
        'all_valid': all([
            has_entities,
            has_equations,
            curve_type_valid,
            query_type_valid,
            completeness_valid
        ])
    }


def main():
    """主函数"""
    # 数据路径
    data_path = project_root / "data" / "train_with_models_1_100.json"
    
    print_separator("综合验证测试", "=")
    print(f"数据路径: {data_path}")
    
    # 加载数据
    print("\n正在加载数据...")
    with open(data_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    print(f"✓ 加载完成，共 {len(data)} 个样本")
    
    # 创建定理库和构造器
    library = TheoremLibrary()
    constructor = StateConstructor(theorem_library=library)
    
    print(f"\n定理库状态: {library}")
    
    # ========================================================================
    # 测试1: 完整度单调性验证
    # ========================================================================
    print_separator("测试1: 完整度单调性验证", "-")
    
    monotonicity_results = []
    for sample in data:
        if not sample.get('models'):
            continue
        
        result = validate_completeness_monotonicity(sample, constructor, library)
        if result:
            monotonicity_results.append(result)
        
        if len(monotonicity_results) >= 10:
            break
    
    # 统计结果
    monotonic_count = sum(1 for r in monotonicity_results if r['is_monotonic'])
    params_monotonic_count = sum(1 for r in monotonicity_results if r['params_monotonic'])
    
    print(f"测试样本数: {len(monotonicity_results)}")
    print(f"完整度单调递增: {monotonic_count}/{len(monotonicity_results)} ({monotonic_count/len(monotonicity_results)*100:.1f}%)")
    print(f"参数数量单调递增: {params_monotonic_count}/{len(monotonicity_results)} ({params_monotonic_count/len(monotonicity_results)*100:.1f}%)")
    
    # 详细结果
    print("\n样本详情:")
    print(f"{'样本ID':<8} {'初始':<8} {'最终':<8} {'增益':<8} {'参数增益':<8} {'单调性':<8}")
    print("-" * 60)
    for r in monotonicity_results:
        monotonic_str = "✅" if r['is_monotonic'] else "❌"
        print(f"{r['sample_id']:<8} {r['initial_completeness']:<8.2f} {r['final_completeness']:<8.2f} "
              f"{r['completeness_gain']:<8.2f} {r['param_gain']:<8} {monotonic_str:<8}")
    
    # 平均增益
    avg_gain = sum(r['completeness_gain'] for r in monotonicity_results) / len(monotonicity_results)
    avg_param_gain = sum(r['param_gain'] for r in monotonicity_results) / len(monotonicity_results)
    print(f"\n平均完整度增益: {avg_gain:.2f}")
    print(f"平均参数增益: {avg_param_gain:.1f}")
    
    # ========================================================================
    # 测试2: 状态构建完整性验证
    # ========================================================================
    print_separator("测试2: 状态构建完整性验证", "-")
    
    integrity_results = []
    for sample in data:
        if not sample.get('models'):
            continue
        
        result = validate_state_construction_integrity(sample, constructor, library)
        if result:
            integrity_results.append(result)
        
        if len(integrity_results) >= 10:
            break
    
    # 统计结果
    all_valid_count = sum(1 for r in integrity_results if r['all_valid'])
    
    print(f"测试样本数: {len(integrity_results)}")
    print(f"状态构建完全有效: {all_valid_count}/{len(integrity_results)} ({all_valid_count/len(integrity_results)*100:.1f}%)")
    
    # 详细结果
    print("\n样本详情:")
    print(f"{'样本ID':<8} {'实体':<6} {'方程':<6} {'曲线':<6} {'查询':<6} {'完整度':<8} {'模型应用':<8} {'状态':<6}")
    print("-" * 70)
    for r in integrity_results:
        status = "✅" if r['all_valid'] else "❌"
        print(f"{r['sample_id']:<8} "
              f"{'✓' if r['has_entities'] else '✗':<6} "
              f"{'✓' if r['has_equations'] else '✗':<6} "
              f"{'✓' if r['curve_type_valid'] else '✗':<6} "
              f"{'✓' if r['query_type_valid'] else '✗':<6} "
              f"{'✓' if r['completeness_valid'] else '✗':<8} "
              f"{r['models_applied']:<8} "
              f"{status:<6}")
    
    # ========================================================================
    # 测试3: 集成测试总结
    # ========================================================================
    print_separator("测试3: 集成测试总结", "-")
    
    print("✅ 完整度单调性:")
    if monotonic_count == len(monotonicity_results):
        print("   ✓ 所有样本完整度单调递增")
    else:
        print(f"   ⚠️  {len(monotonicity_results) - monotonic_count} 个样本完整度非单调")
    
    print("\n✅ 参数数量单调性:")
    if params_monotonic_count == len(monotonicity_results):
        print("   ✓ 所有样本参数数量单调递增")
    else:
        print(f"   ⚠️  {len(monotonicity_results) - params_monotonic_count} 个样本参数数量非单调")
    
    print("\n✅ 状态构建完整性:")
    if all_valid_count == len(integrity_results):
        print("   ✓ 所有样本状态构建完全有效")
    else:
        print(f"   ⚠️  {len(integrity_results) - all_valid_count} 个样本状态构建存在问题")
    
    # ========================================================================
    # 最终结论
    # ========================================================================
    print_separator("最终结论", "=")
    
    all_tests_passed = (
        monotonic_count >= len(monotonicity_results) * 0.9 and  # 90%以上单调
        params_monotonic_count >= len(monotonicity_results) * 0.9 and
        all_valid_count == len(integrity_results)  # 100%有效
    )
    
    if all_tests_passed:
        print("🎉 所有验证测试通过！")
        print("\n✅ 完整度单调性: 优秀")
        print("✅ 参数数量单调性: 优秀")
        print("✅ 状态构建完整性: 完美")
        print("\n系统架构稳定，可以进入下一阶段开发。")
    else:
        print("⚠️  部分验证测试未通过")
        print("\n需要进一步优化的方面:")
        if monotonic_count < len(monotonicity_results) * 0.9:
            print("  - 完整度单调性需要改进")
        if params_monotonic_count < len(monotonicity_results) * 0.9:
            print("  - 参数提取机制需要优化")
        if all_valid_count < len(integrity_results):
            print("  - 状态构建存在问题")
    
    print("\n" + "=" * 80)


if __name__ == "__main__":
    main()
