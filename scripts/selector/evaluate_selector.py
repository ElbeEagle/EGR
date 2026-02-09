#!/usr/bin/env python3
"""
模型选择器评估脚本

测试训练好的模型在实际问题上的表现：
1. 加载训练好的模型
2. 在真实状态序列上进行推理
3. 对比预测结果与实际使用的模型
4. 分析Top-1/3/5命中率
"""

import sys
import json
from pathlib import Path
from typing import List, Dict, Tuple

import torch

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.selector import MaxEntropyClassifier
from src.theorems.theorem_library import TheoremLibrary


def load_model(model_path: str, device: str = 'cpu') -> MaxEntropyClassifier:
    """加载训练好的模型"""
    model = MaxEntropyClassifier()
    checkpoint = torch.load(model_path, map_location=device)
    model.load_state_dict(checkpoint['model_state_dict'])
    model.eval()
    return model


def load_test_data(data_path: str) -> List[Dict]:
    """加载测试数据"""
    with open(data_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data['sample_results']


def evaluate_predictions(
    model: MaxEntropyClassifier,
    samples: List[Dict],
    theorem_library: TheoremLibrary,
    num_samples: int = 10
) -> Dict:
    """
    评估模型预测
    
    Args:
        model: 训练好的模型
        samples: 测试样本列表
        theorem_library: 定理库
        num_samples: 评估前N个样本
    
    Returns:
        评估结果统计
    """
    stats = {
        'total_predictions': 0,
        'top1_hits': 0,
        'top3_hits': 0,
        'top5_hits': 0,
        'predictions_detail': []
    }
    
    print("=" * 80)
    print("模型推理评估")
    print("=" * 80)
    print()
    
    for i, sample in enumerate(samples[:num_samples]):
        sample_id = sample['sample_id']
        print(f"【样本 {sample_id}】")
        print(f"问题: {sample.get('problem', 'N/A')[:60]}...")
        print()
        
        sample_stats = {
            'sample_id': sample_id,
            'problem': sample.get('problem', ''),
            'predictions': []
        }
        
        # 遍历每个转换
        for trans in sample['transitions']:
            state_vector = torch.tensor(trans['state_vector'], dtype=torch.float32)
            actual_model_id = trans['model_id']
            actual_model_name = trans['model_name']
            
            # 模型推理
            with torch.no_grad():
                probs, best_model, entropy = model.predict(state_vector)
                top5_probs, top5_ids = model.get_top_k(state_vector, k=5)
            
            # 检查命中情况
            top5_list = top5_ids.tolist()
            is_top1 = (best_model == actual_model_id)
            is_top3 = (actual_model_id in top5_list[:3])
            is_top5 = (actual_model_id in top5_list[:5])
            
            # 统计
            stats['total_predictions'] += 1
            if is_top1:
                stats['top1_hits'] += 1
            if is_top3:
                stats['top3_hits'] += 1
            if is_top5:
                stats['top5_hits'] += 1
            
            # 打印预测结果
            print(f"  步骤 {trans['step']}: 预测模型选择")
            print(f"    实际使用: Model {actual_model_id} - {actual_model_name}")
            print(f"    Top-1预测: Model {best_model} (prob={probs[best_model]:.3f}) " + 
                  ("✓" if is_top1 else "✗"))
            
            # 显示Top-5
            print(f"    Top-5候选:")
            for rank, (prob, mid) in enumerate(zip(top5_probs, top5_list), 1):
                model_obj = theorem_library.get_model(mid)
                name = model_obj.name if model_obj else f"Model_{mid}"
                marker = " ← 实际" if mid == actual_model_id else ""
                print(f"      {rank}. Model {mid:2d} (prob={prob:.3f}) - {name}{marker}")
            
            print(f"    预测熵: H(Y|X) = {entropy:.3f}")
            print(f"    命中: Top-1={is_top1} Top-3={is_top3} Top-5={is_top5}")
            print()
            
            # 记录详细信息
            sample_stats['predictions'].append({
                'step': trans['step'],
                'actual_model': actual_model_id,
                'predicted_model': best_model,
                'top5': top5_list,
                'is_top1_hit': is_top1,
                'is_top3_hit': is_top3,
                'is_top5_hit': is_top5,
                'entropy': entropy
            })
        
        stats['predictions_detail'].append(sample_stats)
        print("-" * 80)
        print()
    
    return stats


def print_summary(stats: Dict):
    """打印评估总结"""
    total = stats['total_predictions']
    
    print()
    print("=" * 80)
    print("评估总结")
    print("=" * 80)
    print()
    
    print(f"总预测数: {total}")
    print()
    
    print("准确率统计:")
    print(f"  Top-1准确率: {stats['top1_hits']}/{total} = {stats['top1_hits']/total*100:.1f}%")
    print(f"  Top-3准确率: {stats['top3_hits']}/{total} = {stats['top3_hits']/total*100:.1f}%")
    print(f"  Top-5准确率: {stats['top5_hits']}/{total} = {stats['top5_hits']/total*100:.1f}%")
    print()
    
    print("价值分析:")
    top5_reduction = 5 / 80 * 100
    print(f"  - Top-5将搜索空间从80个缩小到5个 ({top5_reduction:.1f}%)")
    print(f"  - {stats['top5_hits']/total*100:.1f}%的情况下，只需搜索5个候选")
    print(f"  - 期望搜索候选数: {5 * stats['top5_hits']/total + 80 * (1 - stats['top5_hits']/total):.1f} (vs 80)")
    print()
    
    print("=" * 80)


def main():
    """主函数"""
    print("模型选择器推理测试")
    print()
    
    # 配置
    model_path = project_root / 'checkpoints' / 'model_selector.pth'
    data_path = project_root / 'data' / 'train_state_model.json'
    num_samples = 5  # 测试前5个样本
    
    print(f"模型路径: {model_path}")
    print(f"数据路径: {data_path}")
    print(f"测试样本数: {num_samples}")
    print()
    
    # 加载模型
    print("加载模型...")
    model = load_model(str(model_path))
    print(f"✓ 模型加载成功")
    print()
    
    # 加载数据
    print("加载测试数据...")
    samples = load_test_data(str(data_path))
    print(f"✓ 加载了 {len(samples)} 个样本")
    print()
    
    # 加载定理库
    theorem_library = TheoremLibrary()
    
    # 评估
    stats = evaluate_predictions(model, samples, theorem_library, num_samples)
    
    # 打印总结
    print_summary(stats)
    
    # 保存结果
    output_path = project_root / 'outputs' / 'selector' / 'evaluation_results.json'
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(stats, f, indent=2, ensure_ascii=False)
    
    print(f"详细结果已保存: {output_path}")


if __name__ == '__main__':
    main()
