"""
模型选择器模块 (Model Selector Module)

实现基于最大熵原理的定理选择神经网络。

核心组件:
- MaxEntropyClassifier: P(model | state) 分类器
- load_training_data: 训练数据加载器
- train_model: 模型训练器
"""

from .model_selector import MaxEntropyClassifier
from .data_loader import load_training_data, prepare_dataloaders
from .trainer import train_model, evaluate_model, save_training_report

__all__ = [
    'MaxEntropyClassifier',
    'load_training_data',
    'prepare_dataloaders',
    'train_model',
    'evaluate_model',
    'save_training_report',
]
