"""
最大熵定理选择器 (MaxEntropy Model Selector)

实现 P(model | state) 分类器，基于最大熵原理。
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
from typing import Tuple


class MaxEntropyClassifier(nn.Module):
    """
    最大熵定理选择分类器
    
    架构: 28 → 64 → 128 → 64 → 80
    损失: CrossEntropyLoss (等价于最大熵学习)
    
    输入: 28维状态向量
    输出: 80维概率分布 P(model | state)
    """
    
    def __init__(
        self, 
        input_dim: int = 28, 
        output_dim: int = 80,
        hidden_dims: Tuple[int, int, int] = (64, 128, 64),
        dropout_rate: float = 0.1
    ):
        """
        Args:
            input_dim: 输入维度 (状态向量维度，默认28)
            output_dim: 输出维度 (模型数量，默认80)
            hidden_dims: 隐藏层维度 (默认 (64, 128, 64))
            dropout_rate: Dropout比率 (默认0.1)
        """
        super(MaxEntropyClassifier, self).__init__()
        
        self.input_dim = input_dim
        self.output_dim = output_dim
        self.hidden_dims = hidden_dims
        self.dropout_rate = dropout_rate
        
        # 网络层
        self.fc1 = nn.Linear(input_dim, hidden_dims[0])
        self.fc2 = nn.Linear(hidden_dims[0], hidden_dims[1])
        self.fc3 = nn.Linear(hidden_dims[1], hidden_dims[2])
        self.fc4 = nn.Linear(hidden_dims[2], output_dim)
        
        self.dropout = nn.Dropout(dropout_rate)
        
        # 初始化权重
        self._init_weights()
    
    def _init_weights(self):
        """Xavier初始化"""
        for module in self.modules():
            if isinstance(module, nn.Linear):
                nn.init.xavier_uniform_(module.weight)
                if module.bias is not None:
                    nn.init.zeros_(module.bias)
    
    def forward(self, state_vector: torch.Tensor) -> torch.Tensor:
        """
        前向传播
        
        Args:
            state_vector: [batch, 28] 状态向量
        
        Returns:
            probs: [batch, 80] 模型概率分布
        """
        x = F.relu(self.fc1(state_vector))      # [batch, 64]
        x = F.relu(self.fc2(x))                  # [batch, 128]
        x = self.dropout(x)
        x = F.relu(self.fc3(x))                  # [batch, 64]
        logits = self.fc4(x)                     # [batch, 80]
        
        # Softmax归一化为概率分布
        probs = F.softmax(logits, dim=-1)
        
        return probs
    
    def predict(self, state_vector: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor, float]:
        """
        推理接口：预测最优模型并计算不确定性
        
        Args:
            state_vector: [batch, 28] 或 [28] 状态向量
        
        Returns:
            probs: [batch, 80] 或 [80] 概率分布
            best_model: [batch] 或标量 - 最优模型ID
            entropy: 标量 - 预测熵 H(Y|X)
        """
        # 确保是2D张量
        if state_vector.dim() == 1:
            state_vector = state_vector.unsqueeze(0)
            squeeze_output = True
        else:
            squeeze_output = False
        
        # 前向传播
        with torch.no_grad():
            probs = self.forward(state_vector)
        
        # 最优模型
        best_model = probs.argmax(dim=-1)
        
        # 计算预测熵 H(Y|X) = -Σ P(y|x) log P(y|x)
        # 添加小常数避免log(0)
        entropy = -(probs * torch.log(probs + 1e-10)).sum(dim=-1).mean().item()
        
        # 如果输入是1D，输出也返回1D
        if squeeze_output:
            probs = probs.squeeze(0)
            best_model = best_model.item()
        
        return probs, best_model, entropy
    
    def get_top_k(self, state_vector: torch.Tensor, k: int = 5) -> Tuple[torch.Tensor, torch.Tensor]:
        """
        获取Top-K候选模型
        
        Args:
            state_vector: [batch, 28] 或 [28] 状态向量
            k: 返回前k个候选
        
        Returns:
            top_k_probs: [batch, k] 或 [k] Top-K概率
            top_k_ids: [batch, k] 或 [k] Top-K模型ID
        """
        with torch.no_grad():
            probs = self.forward(state_vector)
        
        top_k_probs, top_k_ids = torch.topk(probs, k=k, dim=-1)
        
        return top_k_probs, top_k_ids
    
    def count_parameters(self) -> int:
        """统计模型参数量"""
        return sum(p.numel() for p in self.parameters() if p.requires_grad)
    
    def summary(self):
        """打印模型摘要"""
        print("=" * 60)
        print("MaxEntropy Model Selector - 模型摘要")
        print("=" * 60)
        print(f"输入维度:   {self.input_dim}")
        print(f"输出维度:   {self.output_dim}")
        print(f"隐藏层维度: {self.hidden_dims}")
        print(f"Dropout率:  {self.dropout_rate}")
        print(f"参数量:     {self.count_parameters():,}")
        print("=" * 60)
        print("网络结构:")
        print(f"  Input:   [{self.input_dim}]")
        print(f"    ↓ Linear + ReLU")
        print(f"  Hidden1: [{self.hidden_dims[0]}]")
        print(f"    ↓ Linear + ReLU")
        print(f"  Hidden2: [{self.hidden_dims[1]}]")
        print(f"    ↓ Dropout({self.dropout_rate})")
        print(f"  Hidden3: [{self.hidden_dims[2]}]")
        print(f"    ↓ Linear + ReLU")
        print(f"  Output:  [{self.output_dim}]")
        print(f"    ↓ Softmax")
        print(f"  Probs:   [P(model|state)]")
        print("=" * 60)


def create_model(device: str = 'cpu') -> MaxEntropyClassifier:
    """
    创建模型实例并移动到指定设备
    
    Args:
        device: 'cpu' 或 'cuda'
    
    Returns:
        model: 初始化好的模型
    """
    model = MaxEntropyClassifier(
        input_dim=28,
        output_dim=80,
        hidden_dims=(64, 128, 64),
        dropout_rate=0.1
    )
    
    model = model.to(device)
    
    return model


if __name__ == '__main__':
    # 测试模型
    print("测试 MaxEntropyClassifier")
    print()
    
    # 创建模型
    model = create_model(device='cpu')
    model.summary()
    
    # 测试前向传播
    print("\n测试前向传播:")
    print("-" * 60)
    
    # 单个样本
    state = torch.randn(28)
    probs, best_model, entropy = model.predict(state)
    print(f"输入shape: {state.shape}")
    print(f"输出概率分布shape: {probs.shape}")
    print(f"概率和: {probs.sum():.6f}")
    print(f"最优模型ID: {best_model}")
    print(f"预测熵 H(Y|X): {entropy:.4f}")
    
    # 批量样本
    print("\n测试批量推理:")
    print("-" * 60)
    batch_states = torch.randn(8, 28)
    probs, best_models, entropy = model.predict(batch_states)
    print(f"输入shape: {batch_states.shape}")
    print(f"输出概率分布shape: {probs.shape}")
    print(f"最优模型IDs: {best_models}")
    print(f"平均预测熵: {entropy:.4f}")
    
    # 测试Top-K
    print("\n测试Top-5候选:")
    print("-" * 60)
    top_k_probs, top_k_ids = model.get_top_k(state, k=5)
    print(f"Top-5概率: {top_k_probs}")
    print(f"Top-5模型ID: {top_k_ids}")
    
    print("\n✅ 模型测试完成!")
