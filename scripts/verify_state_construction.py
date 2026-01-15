"""
验证状态构建的正确性

读取 train_with_models_1_100.json，打印前5个样本的解析结果
"""

import json
import sys
from pathlib import Path

# 添加src到路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.state import StateConstructor


def load_data(data_path: str):
    """加载数据集"""
    with open(data_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data


def print_separator(title: str):
    """打印分隔符"""
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80 + "\n")


def verify_sample(sample: dict, constructor: StateConstructor):
    """验证单个样本"""
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
    
    # 构建状态
    try:
        abstract_state, symbolic_state = constructor.construct_from_facts(
            fact_expr,
            query_expr,
            reasoning_depth=0
        )
        
        print("\n" + "-" * 40)
        print("SymbolicState:")
        print(f"  实体: {dict(list(symbolic_state.entities.items())[:5])}")
        if len(symbolic_state.entities) > 5:
            print(f"        ... 共 {len(symbolic_state.entities)} 个")
        
        print(f"  方程: {symbolic_state.equations[:2]}")
        if len(symbolic_state.equations) > 2:
            print(f"        ... 共 {len(symbolic_state.equations)} 个")
        
        print(f"  参数: {symbolic_state.parameters}")
        print(f"  坐标: {symbolic_state.coordinates}")
        print(f"  约束: {symbolic_state.constraints}")
        print(f"  关系: {len(symbolic_state.geometric_relations)} 个")
        
        print("\n" + "-" * 40)
        print("AbstractState:")
        print(f"  曲线类型: {abstract_state.curve_type.value}")
        print(f"  查询类型: {abstract_state.query_type.value}")
        print(f"  有方程: {abstract_state.has_equation}")
        print(f"  已知参数: {abstract_state.has_parameters}")
        print(f"  有焦点信息: {abstract_state.has_focus_info}")
        print(f"  有渐近线信息: {abstract_state.has_asymptote_info}")
        print(f"  完整度: {abstract_state.completeness_score:.2f}")
        print(f"  推理深度: {abstract_state.reasoning_depth}")
        
        print("\n" + "-" * 40)
        print("特征向量:")
        vector = abstract_state.to_vector()
        print(f"  维度: {len(vector)}")
        print(f"  前10维: {[f'{v:.2f}' for v in vector[:10]]}")
        
        print("\n" + "-" * 40)
        print("状态哈希:")
        state_hash = abstract_state.to_hash()
        print(f"  {state_hash}")
        
        print("\n✅ 解析成功")
        return True
        
    except Exception as e:
        print(f"\n❌ 解析失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """主函数"""
    # 数据路径
    data_path = project_root / "data" / "train_with_models_1_100.json"
    
    if not data_path.exists():
        print(f"错误：数据文件不存在: {data_path}")
        return
    
    print_separator("状态构建验证工具")
    print(f"数据路径: {data_path}")
    
    # 加载数据
    print("\n正在加载数据...")
    data = load_data(str(data_path))
    print(f"✓ 加载完成，共 {len(data)} 个样本")
    
    # 创建构造器
    constructor = StateConstructor()
    
    # 验证前5个有模型序列的样本
    print_separator("开始验证样本")
    
    success_count = 0
    total_count = 0
    
    for sample in data:
        # 跳过没有模型序列的样本
        if not sample.get('models'):
            continue
        
        print_separator(f"样本 {total_count + 1}")
        success = verify_sample(sample, constructor)
        
        if success:
            success_count += 1
        total_count += 1
        
        # 只验证前5个
        if total_count >= 5:
            break
    
    # 统计结果
    print_separator("验证结果汇总")
    print(f"总样本数: {total_count}")
    print(f"成功数: {success_count}")
    print(f"失败数: {total_count - success_count}")
    print(f"成功率: {success_count / total_count * 100:.1f}%")
    
    if success_count == total_count:
        print("\n🎉 所有样本解析成功！")
    else:
        print(f"\n⚠️  有 {total_count - success_count} 个样本解析失败")


if __name__ == "__main__":
    main()
