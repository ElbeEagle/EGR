#!/usr/bin/env python3
"""
测试模型选择器的功能

测试：
1. 数据加载
2. 模型创建
3. 前向传播
4. 训练流程（小规模）
"""

import sys
import os
import torch

# 添加项目根目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from src.selector import (
    load_training_data,
    prepare_dataloaders,
    MaxEntropyClassifier,
    train_model
)


def test_data_loading():
    """测试数据加载"""
    print("=" * 70)
    print("测试1: 数据加载")
    print("=" * 70)
    
    X, y = load_training_data('data/train_state_model.json')
    
    print(f"\n✅ 数据加载成功")
    print(f"   - 样本数: {len(X)}")
    print(f"   - 特征维度: {len(X[0])}")
    print(f"   - 标签范围: [{min(y)}, {max(y)}]")
    
    return X, y


def test_dataloader(X, y):
    """测试DataLoader"""
    print("\n" + "=" * 70)
    print("测试2: DataLoader创建")
    print("=" * 70)
    
    train_loader, val_loader = prepare_dataloaders(X, y, batch_size=8)
    
    # 测试一个batch
    for states, labels in train_loader:
        print(f"\n✅ DataLoader工作正常")
        print(f"   - Batch states shape: {states.shape}")
        print(f"   - Batch labels shape: {labels.shape}")
        print(f"   - States dtype: {states.dtype}")
        print(f"   - Labels dtype: {labels.dtype}")
        break
    
    return train_loader, val_loader


def test_model():
    """测试模型创建和前向传播"""
    print("\n" + "=" * 70)
    print("测试3: 模型创建和前向传播")
    print("=" * 70)
    
    # 创建模型
    model = MaxEntropyClassifier(
        input_dim=28,
        output_dim=80,
        hidden_dims=(64, 128, 64),
        dropout_rate=0.1
    )
    
    print(f"\n✅ 模型创建成功")
    print(f"   - 参数量: {model.count_parameters():,}")
    
    # 测试前向传播
    test_state = torch.randn(1, 28)
    probs, best_model, entropy = model.predict(test_state)
    
    print(f"\n✅ 前向传播正常")
    print(f"   - 输出shape: {probs.shape}")
    print(f"   - 概率和: {probs.sum():.6f}")
    print(f"   - 最优模型: {best_model}")
    print(f"   - 预测熵: {entropy:.4f}")
    
    # 测试Top-K
    top_k_probs, top_k_ids = model.get_top_k(test_state, k=5)
    print(f"\n✅ Top-K功能正常")
    print(f"   - Top-5 IDs: {top_k_ids.tolist()}")
    print(f"   - Top-5 Probs: {top_k_probs.tolist()}")
    
    return model


def test_training_mini():
    """测试训练流程（小规模）"""
    print("\n" + "=" * 70)
    print("测试4: 小规模训练流程")
    print("=" * 70)
    print("训练5个epoch进行验证...")
    
    model, history = train_model(
        data_path='data/train_state_model.json',
        num_epochs=5,
        batch_size=16,
        learning_rate=0.001,
        use_class_weights=False,
        patience=20,
        save_path='checkpoints/model_selector_test.pth',
        device='cpu'
    )
    
    print(f"\n✅ 训练流程正常")
    print(f"   - 完成epoch数: {len(history['train_loss'])}")
    print(f"   - 最终训练损失: {history['train_loss'][-1]:.4f}")
    print(f"   - 最终验证Top-1准确率: {history['val_acc'][-1]:.3f}")
    print(f"   - 最终验证Top-3准确率: {history['val_top3_acc'][-1]:.3f}")
    
    return model, history


def main():
    """运行所有测试"""
    print("=" * 70)
    print("模型选择器功能测试")
    print("=" * 70)
    print()
    
    try:
        # 测试1: 数据加载
        X, y = test_data_loading()
        
        # 测试2: DataLoader
        train_loader, val_loader = test_dataloader(X, y)
        
        # 测试3: 模型
        model = test_model()
        
        # 测试4: 训练流程
        model, history = test_training_mini()
        
        print("\n" + "=" * 70)
        print("✅ 所有测试通过!")
        print("=" * 70)
        print("\n准备进行完整训练，请运行:")
        print("  python scripts/selector/train.py")
        print("=" * 70)
        
    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()
