"""
训练数据加载示例

展示如何加载和使用 train_state_model.json 进行 Module 3 训练
"""

import json
from pathlib import Path

# 项目根目录
project_root = Path(__file__).parent.parent.parent


def load_training_data(data_path: str):
    """
    加载训练数据
    
    Args:
        data_path: 训练数据文件路径
    
    Returns:
        训练样本列表: [(state_vector, model_id), ...]
    """
    with open(data_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    training_samples = []
    
    for sample in data['sample_results']:
        for trans in sample['transitions']:
            training_samples.append({
                'state_vector': trans['state_vector'],      # 28维特征向量
                'model_id': trans['model_id'],              # 模型ID标签 (0-79)
                'sample_id': sample['sample_id'],           # 原始样本ID
                'step': trans['step'],                      # 推理步数
                'completeness': trans['abstract_state']['completeness_score']  # 完整度
            })
    
    return training_samples


def main():
    """演示加载和使用训练数据"""
    # 加载数据
    data_path = project_root / 'data' / 'train_state_model.json'
    print(f"加载训练数据: {data_path}\n")
    
    training_samples = load_training_data(str(data_path))
    
    print(f"{'='*60}")
    print(f"训练数据统计")
    print(f"{'='*60}\n")
    
    print(f"总训练样本数: {len(training_samples)}")
    print(f"状态向量维度: {len(training_samples[0]['state_vector'])}")
    
    # 统计模型分布
    model_counts = {}
    for sample in training_samples:
        model_id = sample['model_id']
        model_counts[model_id] = model_counts.get(model_id, 0) + 1
    
    print(f"涉及的模型数: {len(model_counts)}/80")
    
    # 显示前5个样本
    print(f"\n前5个训练样本：")
    print(f"{'='*60}\n")
    
    for i, sample in enumerate(training_samples[:5]):
        print(f"样本 {i+1}:")
        print(f"  state_vector: {sample['state_vector'][:5]}... (28维)")
        print(f"  model_id: {sample['model_id']}")
        print(f"  completeness: {sample['completeness']:.3f}")
        print()
    
    print(f"{'='*60}")
    print(f"✅ 数据加载成功！可以开始训练 Module 3")
    print(f"{'='*60}")


if __name__ == '__main__':
    main()
