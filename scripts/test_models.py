"""
测试定理模型应用

测试已实现的模型能否正确应用
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


def test_sample_with_models(sample: dict, constructor: StateConstructor, library: TheoremLibrary):
    """
    测试单个样本的模型序列应用
    """
    sample_id = sample['id']
    text = sample['text']
    fact_expr = sample['fact_expressions']
    query_expr = sample['query_expressions']
    models = sample.get('models', [])
    answer = sample['answer_expressions']
    
    print(f"【样本 ID={sample_id}】")
    print(f"题目: {text[:80]}..." if len(text) > 80 else f"题目: {text}")
    print(f"\n查询: {query_expr}")
    print(f"答案: {answer}")
    print(f"模型序列: {models}")
    
    # 构建初始状态
    print("\n" + "-" * 40)
    print("【初始状态 S0】")
    abstract_state, symbolic_state = constructor.construct_from_facts(
        fact_expr,
        query_expr,
        reasoning_depth=0
    )
    
    print(f"完整度: {abstract_state.completeness_score:.2f}")
    print(f"参数: {symbolic_state.parameters}")
    print(f"方程数: {len(symbolic_state.equations)}")
    
    # 逐步应用模型
    for i, model_id in enumerate(models):
        print("\n" + "-" * 40)
        print(f"【应用 Model {model_id}】")
        
        # 检查模型是否存在
        if not library.has_model(model_id):
            print(f"❌ 模型 {model_id} 尚未实现")
            continue
        
        model = library.get_model(model_id)
        print(f"模型名称: {model.chinese_name}")
        
        # 检查前置条件
        if not model.can_apply(symbolic_state):
            print(f"❌ 前置条件不满足，无法应用")
            continue
        
        # 应用模型
        try:
            model.apply(symbolic_state)
            print(f"✅ 应用成功")
            
            # 重新构建抽象状态
            abstract_state = constructor.construct_from_symbolic_state(
                symbolic_state,
                query_expr,
                reasoning_depth=i + 1
            )
            
            print(f"\n【更新后状态 S{i+1}】")
            print(f"完整度: {abstract_state.completeness_score:.2f}")
            print(f"参数: {symbolic_state.parameters}")
            print(f"新增关系: {symbolic_state.geometric_relations[-2:] if len(symbolic_state.geometric_relations) >= 2 else symbolic_state.geometric_relations}")
            
        except Exception as e:
            print(f"❌ 应用失败: {str(e)}")
            import traceback
            traceback.print_exc()
    
    # 最终状态
    print("\n" + "-" * 40)
    print("【最终状态】")
    print(f"完整度: {abstract_state.completeness_score:.2f}")
    print(f"参数: {symbolic_state.parameters}")
    print(f"已应用模型: {symbolic_state.applied_models}")
    
    # 检查是否包含答案相关信息
    query_lower = query_expr.lower()
    if 'm' in query_lower and 'm' in symbolic_state.parameters:
        print(f"\n✅ 参数 m = {symbolic_state.parameters.get('m', '未求出')}")
    elif 'eccentricity' in query_lower and 'e' in symbolic_state.parameters:
        print(f"\n✅ 离心率 e = {symbolic_state.parameters.get('e', '未求出')}")
    else:
        print(f"\n⚠️  查询目标尚未直接求出")


def main():
    """主函数"""
    # 数据路径
    data_path = project_root / "data" / "train_with_models_1_100.json"
    
    print_separator("定理模型测试工具")
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
    
    # 测试样本2 (ID=2, models=[5, 21])
    print_separator("测试样本2 - 双曲线渐近线问题")
    sample2 = next(s for s in data if s['id'] == 2)
    test_sample_with_models(sample2, constructor, library)
    
    print_separator("测试完成")


if __name__ == "__main__":
    main()
