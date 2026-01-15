"""
构建状态序列 - 为每个训练样本生成完整的状态转换序列

输入：train_with_models_1_100.json（包含models字段）
输出：train_with_state_sequences.json（包含S0, S1, S2, ...）

这是训练数据准备的核心脚本！
"""

import json
import sys
from pathlib import Path
from typing import List, Dict, Any

# 添加src目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.state_abstractor import StateAbstractor, AbstractState, SymbolicState
from src.theorems.theorem_library import TheoremLibrary


def build_state_sequences_for_dataset(
    input_file: str,
    output_file: str
):
    """
    为整个数据集构建状态序列
    
    Args:
        input_file: 输入文件路径（train_with_models.json）
        output_file: 输出文件路径（train_with_state_sequences.json）
    """
    # 初始化
    abstractor = StateAbstractor()
    theorem_library = TheoremLibrary()
    
    # 读取数据
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print(f"读取了 {len(data)} 个样本")
    
    # 处理每个样本
    results = []
    successful = 0
    failed = 0
    
    for i, sample in enumerate(data):
        try:
            result = build_state_sequence_for_sample(
                sample,
                abstractor,
                theorem_library
            )
            results.append(result)
            successful += 1
            
            if (i + 1) % 10 == 0:
                print(f"处理进度: {i+1}/{len(data)}")
        
        except Exception as e:
            print(f"样本 {sample.get('id', i)} 处理失败: {str(e)}")
            failed += 1
            # 保留原始样本，但标记为失败
            result = sample.copy()
            result['state_sequence_error'] = str(e)
            results.append(result)
    
    # 保存结果
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print("=" * 60)
    print("状态序列构建完成！")
    print(f"成功: {successful}/{len(data)}")
    print(f"失败: {failed}/{len(data)}")
    print(f"输出文件: {output_file}")
    print("=" * 60)


def build_state_sequence_for_sample(
    sample: Dict[str, Any],
    abstractor: StateAbstractor,
    theorem_library: TheoremLibrary
) -> Dict[str, Any]:
    """
    为单个样本构建状态序列
    
    Args:
        sample: 原始样本（包含fact_expressions, query_expressions, models）
        abstractor: 状态抽象器
        theorem_library: 定理库
    
    Returns:
        增强后的样本（包含state_sequence字段）
    """
    fact_expressions = sample['fact_expressions']
    query_expressions = sample['query_expressions']
    model_ids = sample.get('models', [])
    
    # 1. 解析初始状态S0
    abstract_state_0, symbolic_state_0 = abstractor.abstract_from_facts(
        fact_expressions,
        query_expressions,
        reasoning_depth=0
    )
    
    # 2. 应用模型序列，生成S1, S2, ..., Sn
    symbolic_states = theorem_library.apply_model_sequence(
        symbolic_state_0,
        model_ids
    )
    
    # 3. 为每个符号状态生成对应的抽象状态
    abstract_states = []
    for depth, symbolic_state in enumerate(symbolic_states):
        # 将符号状态重新抽象为抽象状态
        # 由于symbolic_state已经更新，需要重新构建fact_expressions
        # 简化起见，我们直接从symbolic_state提取特征
        abstract_state = abstractor.abstract_from_symbolic_state(
            symbolic_state,
            query_expressions,
            reasoning_depth=depth
        )
        abstract_states.append(abstract_state)
    
    # 4. 构建状态序列数据
    state_sequence = []
    for i in range(len(abstract_states)):
        state_info = {
            'step': i,
            'abstract_state': {
                'curve_type': abstract_states[i].curve_type.value,
                'query_type': abstract_states[i].query_type.value,
                'has_equation': abstract_states[i].has_equation,
                'has_parameters': list(abstract_states[i].has_parameters),
                'has_focus_info': abstract_states[i].has_focus_info,
                'has_asymptote_info': abstract_states[i].has_asymptote_info,
                'completeness_score': round(abstract_states[i].completeness_score, 3),
                'reasoning_depth': abstract_states[i].reasoning_depth,
                'state_hash': abstract_states[i].to_hash(),
                'state_vector': [round(x, 3) for x in abstract_states[i].to_vector()]
            },
            'symbolic_state': {
                'entities': symbolic_states[i].entities,
                'equations': symbolic_states[i].equations,
                'parameters': symbolic_states[i].parameters,
                'geometric_relations': symbolic_states[i].geometric_relations[-5:],  # 只保留最新5个
                'coordinates': {k: list(v) for k, v in symbolic_states[i].coordinates.items()}
            }
        }
        
        # 如果不是最后一步，添加应用的模型
        if i < len(model_ids):
            state_info['applied_model'] = model_ids[i]
            model = theorem_library.get_model(model_ids[i])
            if model:
                state_info['model_name'] = model.name
                state_info['model_description'] = model.description
        
        state_sequence.append(state_info)
    
    # 5. 返回增强后的样本
    result = sample.copy()
    result['state_sequence'] = state_sequence
    result['num_steps'] = len(model_ids)
    result['initial_completeness'] = round(abstract_states[0].completeness_score, 3)
    result['final_completeness'] = round(abstract_states[-1].completeness_score, 3)
    
    return result


def analyze_state_distribution(
    data_file: str,
    output_file: str
):
    """
    分析状态分布
    
    统计：
    1. 每种状态出现的频率
    2. 状态 -> 模型 的转移概率
    3. 状态聚类
    """
    with open(data_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 统计状态分布
    state_counts = {}
    state_to_model_counts = {}  # {state_hash: {model_id: count}}
    
    for sample in data:
        if 'state_sequence' not in sample:
            continue
        
        state_seq = sample['state_sequence']
        
        for i, state_info in enumerate(state_seq[:-1]):  # 不包括最后一个状态
            state_hash = state_info['abstract_state']['state_hash']
            next_model = state_info['applied_model']
            
            # 统计状态出现次数
            state_counts[state_hash] = state_counts.get(state_hash, 0) + 1
            
            # 统计状态->模型转移
            if state_hash not in state_to_model_counts:
                state_to_model_counts[state_hash] = {}
            
            state_to_model_counts[state_hash][next_model] = \
                state_to_model_counts[state_hash].get(next_model, 0) + 1
    
    # 计算转移概率
    state_to_model_probs = {}
    for state_hash, model_counts in state_to_model_counts.items():
        total = sum(model_counts.values())
        state_to_model_probs[state_hash] = {
            model_id: count / total
            for model_id, count in model_counts.items()
        }
    
    # 保存分析结果
    analysis = {
        'num_unique_states': len(state_counts),
        'state_counts': state_counts,
        'state_to_model_probs': state_to_model_probs,
        'most_common_states': sorted(
            state_counts.items(),
            key=lambda x: x[1],
            reverse=True
        )[:50]  # top 50
    }
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(analysis, f, ensure_ascii=False, indent=2)
    
    print("=" * 60)
    print("状态分布分析完成！")
    print(f"唯一状态数: {len(state_counts)}")
    print(f"最常见状态:")
    for state_hash, count in analysis['most_common_states'][:10]:
        print(f"  {state_hash[:8]}... : {count}次")
    print(f"输出文件: {output_file}")
    print("=" * 60)


def main():
    """主函数"""
    project_root = Path(__file__).parent.parent.parent
    
    # 输入输出路径
    input_file = project_root / "data" / "train_with_models_1_100.json"
    output_file = project_root / "data" / "train_with_state_sequences_1_100.json"
    analysis_file = project_root / "outputs" / "state_distribution_analysis.json"
    
    # 构建状态序列
    print("开始构建状态序列...")
    build_state_sequences_for_dataset(
        str(input_file),
        str(output_file)
    )
    
    # 分析状态分布
    print("\n开始分析状态分布...")
    analyze_state_distribution(
        str(output_file),
        str(analysis_file)
    )


if __name__ == "__main__":
    main()
