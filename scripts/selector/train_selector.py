#!/usr/bin/env python3
"""
训练模型选择器的主脚本

使用方法:
    python scripts/selector/train_selector.py
"""

import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from src.selector import train_model, save_training_report


def main():
    """主训练函数"""
    
    print("=" * 70)
    print("MaxEntropy Model Selector - 训练")
    print("=" * 70)
    print()
    
    # 训练配置
    config = {
        'data_path': 'data/train_state_model.json',
        'num_epochs': 100,
        'batch_size': 16,
        'learning_rate': 0.001,
        'use_class_weights': False,
        'patience': 20,
        'save_path': 'checkpoints/model_selector.pth',
        'device': None  # 自动检测
    }
    
    print("训练配置:")
    for key, value in config.items():
        print(f"  {key}: {value}")
    print()
    
    # 训练模型
    model, history = train_model(**config)
    
    # 保存训练报告
    print("\n保存训练报告...")
    save_training_report(
        history=history,
        metrics=history,
        output_path='outputs/selector/training_metrics.json'
    )
    
    print("\n" + "=" * 70)
    print("✅ 训练完成!")
    print("=" * 70)
    print(f"模型保存位置: {config['save_path']}")
    print(f"训练报告位置: outputs/selector/training_metrics.json")
    print("=" * 70)


if __name__ == '__main__':
    main()
