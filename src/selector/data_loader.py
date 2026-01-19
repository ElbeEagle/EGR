"""
训练数据加载器 (Training Data Loader)

从 train_state_model.json 加载训练数据，提取 (state_vector, model_id) 对。
"""

import json
import torch
from torch.utils.data import Dataset, DataLoader, random_split
from typing import Tuple, List, Dict, Any
from collections import Counter


class StateModelDataset(Dataset):
    """状态-模型对数据集"""
    
    def __init__(self, state_vectors: List[List[float]], model_ids: List[int]):
        """
        Args:
            state_vectors: 状态向量列表 [[28维], [28维], ...]
            model_ids: 模型ID列表 [0-79]
        """
        self.state_vectors = torch.tensor(state_vectors, dtype=torch.float32)
        self.model_ids = torch.tensor(model_ids, dtype=torch.long)
        
        assert len(self.state_vectors) == len(self.model_ids), \
            f"数据长度不匹配: {len(self.state_vectors)} vs {len(self.model_ids)}"
        assert self.state_vectors.shape[1] == 28, \
            f"状态向量维度应为28，实际为{self.state_vectors.shape[1]}"
    
    def __len__(self) -> int:
        return len(self.state_vectors)
    
    def __getitem__(self, idx: int) -> Tuple[torch.Tensor, torch.Tensor]:
        """返回 (state_vector, model_id)"""
        return self.state_vectors[idx], self.model_ids[idx]


def load_training_data(data_path: str = 'data/train_state_model.json') -> Tuple[List[List[float]], List[int]]:
    """
    从 train_state_model.json 加载训练数据
    
    Args:
        data_path: 数据文件路径
    
    Returns:
        (state_vectors, model_ids): 状态向量列表和模型ID列表
    """
    with open(data_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    state_vectors = []
    model_ids = []
    
    # 提取所有成功的转换
    for sample in data['sample_results']:
        for trans in sample['transitions']:
            if trans['status'] == 'success':
                state_vectors.append(trans['state_vector'])
                model_ids.append(trans['model_id'])
    
    print(f"[Data Loader] 加载数据完成:")
    print(f"  - 文件: {data_path}")
    print(f"  - 样本数: {len(state_vectors)}")
    print(f"  - 特征维度: {len(state_vectors[0]) if state_vectors else 0}")
    print(f"  - 模型ID范围: [{min(model_ids)}, {max(model_ids)}]")
    
    # 统计模型分布
    model_counter = Counter(model_ids)
    print(f"  - 使用的模型数: {len(model_counter)}/80")
    print(f"  - Top 5高频模型: {model_counter.most_common(5)}")
    
    return state_vectors, model_ids


def prepare_dataloaders(
    state_vectors: List[List[float]], 
    model_ids: List[int],
    train_ratio: float = 0.8,
    batch_size: int = 16,
    shuffle: bool = True,
    seed: int = 42
) -> Tuple[DataLoader, DataLoader]:
    """
    准备训练集和验证集的DataLoader
    
    Args:
        state_vectors: 状态向量列表
        model_ids: 模型ID列表
        train_ratio: 训练集比例 (默认0.8)
        batch_size: 批大小 (默认16，适合小数据集)
        shuffle: 是否打乱数据
        seed: 随机种子
    
    Returns:
        (train_loader, val_loader): 训练集和验证集的DataLoader
    """
    # 创建数据集
    dataset = StateModelDataset(state_vectors, model_ids)
    
    # 划分训练集和验证集
    total_size = len(dataset)
    train_size = int(total_size * train_ratio)
    val_size = total_size - train_size
    
    # 设置随机种子以确保可复现
    torch.manual_seed(seed)
    train_dataset, val_dataset = random_split(dataset, [train_size, val_size])
    
    # 创建DataLoader
    train_loader = DataLoader(
        train_dataset,
        batch_size=batch_size,
        shuffle=shuffle,
        num_workers=0  # 小数据集不需要多进程
    )
    
    val_loader = DataLoader(
        val_dataset,
        batch_size=batch_size,
        shuffle=False,
        num_workers=0
    )
    
    print(f"[Data Loader] 数据划分完成:")
    print(f"  - 训练集: {train_size} 样本 ({train_size/total_size*100:.1f}%)")
    print(f"  - 验证集: {val_size} 样本 ({val_size/total_size*100:.1f}%)")
    print(f"  - Batch size: {batch_size}")
    
    return train_loader, val_loader


def get_class_weights(model_ids: List[int], num_classes: int = 80) -> torch.Tensor:
    """
    计算类别权重，用于处理类别不平衡
    
    使用反频率加权: weight[c] = total / count[c]
    
    Args:
        model_ids: 模型ID列表
        num_classes: 类别总数 (默认80)
    
    Returns:
        class_weights: 类别权重张量 [80]
    """
    counter = Counter(model_ids)
    total = len(model_ids)
    
    weights = torch.ones(num_classes, dtype=torch.float32)
    
    for model_id, count in counter.items():
        weights[model_id] = total / count
    
    # 归一化权重
    weights = weights / weights.sum() * num_classes
    
    print(f"[Data Loader] 类别权重计算完成:")
    print(f"  - 最高权重: {weights.max():.2f}")
    print(f"  - 最低权重: {weights.min():.2f}")
    print(f"  - 平均权重: {weights.mean():.2f}")
    
    return weights


if __name__ == '__main__':
    # 测试数据加载
    print("=" * 60)
    print("测试训练数据加载器")
    print("=" * 60)
    
    # 加载数据
    X, y = load_training_data('../../data/train_state_model.json')
    
    print("\n" + "=" * 60)
    print("测试DataLoader创建")
    print("=" * 60)
    
    # 创建DataLoader
    train_loader, val_loader = prepare_dataloaders(X, y, batch_size=8)
    
    # 测试一个batch
    print("\n" + "=" * 60)
    print("测试Batch读取")
    print("=" * 60)
    
    for states, labels in train_loader:
        print(f"  - Batch states shape: {states.shape}")
        print(f"  - Batch labels shape: {labels.shape}")
        print(f"  - States dtype: {states.dtype}")
        print(f"  - Labels dtype: {labels.dtype}")
        print(f"  - Sample label: {labels[0].item()}")
        break
    
    print("\n✅ 数据加载器测试完成!")
