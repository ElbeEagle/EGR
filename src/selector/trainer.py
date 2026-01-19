"""
模型训练器 (Model Trainer)

训练 MaxEntropyClassifier，评估性能，保存模型。
"""

import os
import json
import time
from datetime import datetime
from typing import Dict, List, Tuple, Optional

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader

from .model_selector import MaxEntropyClassifier
from .data_loader import load_training_data, prepare_dataloaders, get_class_weights


class Trainer:
    """训练器类"""
    
    def __init__(
        self,
        model: MaxEntropyClassifier,
        device: str = 'cpu',
        learning_rate: float = 0.001,
        use_class_weights: bool = False,
        class_weights: Optional[torch.Tensor] = None
    ):
        """
        Args:
            model: 待训练的模型
            device: 训练设备
            learning_rate: 学习率
            use_class_weights: 是否使用类别权重
            class_weights: 类别权重张量
        """
        self.model = model.to(device)
        self.device = device
        self.learning_rate = learning_rate
        
        # 损失函数 (CrossEntropy = 最大熵学习)
        if use_class_weights and class_weights is not None:
            class_weights = class_weights.to(device)
            self.criterion = nn.CrossEntropyLoss(weight=class_weights)
            print(f"[Trainer] 使用加权损失函数")
        else:
            self.criterion = nn.CrossEntropyLoss()
            print(f"[Trainer] 使用标准损失函数")
        
        # 优化器
        self.optimizer = optim.Adam(model.parameters(), lr=learning_rate)
        
        # 训练历史
        self.history = {
            'train_loss': [],
            'train_acc': [],
            'val_loss': [],
            'val_acc': [],
            'val_top3_acc': [],
            'val_top5_acc': [],
        }
        
        self.best_val_acc = 0.0
        self.best_epoch = 0
    
    def train_epoch(self, train_loader: DataLoader) -> Tuple[float, float]:
        """
        训练一个epoch
        
        Returns:
            (avg_loss, accuracy)
        """
        self.model.train()
        
        total_loss = 0.0
        correct = 0
        total = 0
        
        for states, labels in train_loader:
            states = states.to(self.device)
            labels = labels.to(self.device)
            
            # 前向传播
            self.optimizer.zero_grad()
            probs = self.model(states)
            
            # 计算损失 (需要logits，不是probs)
            # 但我们的模型输出是probs，需要转换回logits
            logits = torch.log(probs + 1e-10)  # 避免log(0)
            loss = self.criterion(logits, labels)
            
            # 反向传播
            loss.backward()
            self.optimizer.step()
            
            # 统计
            total_loss += loss.item() * states.size(0)
            pred = probs.argmax(dim=1)
            correct += (pred == labels).sum().item()
            total += states.size(0)
        
        avg_loss = total_loss / total
        accuracy = correct / total
        
        return avg_loss, accuracy
    
    def evaluate(self, val_loader: DataLoader) -> Dict[str, float]:
        """
        评估模型
        
        Returns:
            metrics: {'loss', 'top1_acc', 'top3_acc', 'top5_acc'}
        """
        self.model.eval()
        
        total_loss = 0.0
        correct_top1 = 0
        correct_top3 = 0
        correct_top5 = 0
        total = 0
        
        with torch.no_grad():
            for states, labels in val_loader:
                states = states.to(self.device)
                labels = labels.to(self.device)
                
                # 前向传播
                probs = self.model(states)
                
                # 计算损失
                logits = torch.log(probs + 1e-10)
                loss = self.criterion(logits, labels)
                total_loss += loss.item() * states.size(0)
                
                # Top-1准确率
                pred_top1 = probs.argmax(dim=1)
                correct_top1 += (pred_top1 == labels).sum().item()
                
                # Top-3准确率
                _, pred_top3 = torch.topk(probs, k=3, dim=1)
                correct_top3 += (pred_top3 == labels.unsqueeze(1)).any(dim=1).sum().item()
                
                # Top-5准确率
                _, pred_top5 = torch.topk(probs, k=5, dim=1)
                correct_top5 += (pred_top5 == labels.unsqueeze(1)).any(dim=1).sum().item()
                
                total += states.size(0)
        
        metrics = {
            'loss': total_loss / total,
            'top1_acc': correct_top1 / total,
            'top3_acc': correct_top3 / total,
            'top5_acc': correct_top5 / total,
        }
        
        return metrics
    
    def fit(
        self,
        train_loader: DataLoader,
        val_loader: DataLoader,
        num_epochs: int = 100,
        patience: int = 20,
        save_path: str = 'checkpoints/model_selector.pth',
        log_interval: int = 10
    ) -> Dict:
        """
        训练模型
        
        Args:
            train_loader: 训练数据加载器
            val_loader: 验证数据加载器
            num_epochs: 训练轮数
            patience: Early stopping耐心值
            save_path: 模型保存路径
            log_interval: 日志打印间隔
        
        Returns:
            history: 训练历史
        """
        print("\n" + "=" * 70)
        print("开始训练 MaxEntropy Model Selector")
        print("=" * 70)
        print(f"训练轮数: {num_epochs}")
        print(f"Early stopping patience: {patience}")
        print(f"学习率: {self.learning_rate}")
        print(f"设备: {self.device}")
        print(f"保存路径: {save_path}")
        print("=" * 70)
        
        epochs_no_improve = 0
        start_time = time.time()
        
        for epoch in range(1, num_epochs + 1):
            # 训练
            train_loss, train_acc = self.train_epoch(train_loader)
            
            # 验证
            val_metrics = self.evaluate(val_loader)
            
            # 记录历史
            self.history['train_loss'].append(train_loss)
            self.history['train_acc'].append(train_acc)
            self.history['val_loss'].append(val_metrics['loss'])
            self.history['val_acc'].append(val_metrics['top1_acc'])
            self.history['val_top3_acc'].append(val_metrics['top3_acc'])
            self.history['val_top5_acc'].append(val_metrics['top5_acc'])
            
            # 打印日志
            if epoch % log_interval == 0 or epoch == 1:
                print(f"Epoch {epoch:3d}/{num_epochs} | "
                      f"Train Loss: {train_loss:.4f} Acc: {train_acc:.3f} | "
                      f"Val Loss: {val_metrics['loss']:.4f} "
                      f"Top1: {val_metrics['top1_acc']:.3f} "
                      f"Top3: {val_metrics['top3_acc']:.3f} "
                      f"Top5: {val_metrics['top5_acc']:.3f}")
            
            # 保存最佳模型
            if val_metrics['top1_acc'] > self.best_val_acc:
                self.best_val_acc = val_metrics['top1_acc']
                self.best_epoch = epoch
                
                # 确保目录存在
                os.makedirs(os.path.dirname(save_path), exist_ok=True)
                
                # 保存模型
                torch.save({
                    'epoch': epoch,
                    'model_state_dict': self.model.state_dict(),
                    'optimizer_state_dict': self.optimizer.state_dict(),
                    'best_val_acc': self.best_val_acc,
                    'history': self.history,
                }, save_path)
                
                epochs_no_improve = 0
                print(f"  → 保存最佳模型 (Val Top-1 Acc: {self.best_val_acc:.3f})")
            else:
                epochs_no_improve += 1
            
            # Early stopping
            if epochs_no_improve >= patience:
                print(f"\nEarly stopping at epoch {epoch}")
                print(f"最佳验证准确率: {self.best_val_acc:.3f} (Epoch {self.best_epoch})")
                break
        
        elapsed_time = time.time() - start_time
        
        print("\n" + "=" * 70)
        print("训练完成!")
        print("=" * 70)
        print(f"总用时: {elapsed_time:.2f}秒")
        print(f"最佳Epoch: {self.best_epoch}")
        print(f"最佳验证Top-1准确率: {self.best_val_acc:.3f}")
        print(f"最终验证Top-3准确率: {self.history['val_top3_acc'][self.best_epoch-1]:.3f}")
        print(f"最终验证Top-5准确率: {self.history['val_top5_acc'][self.best_epoch-1]:.3f}")
        print("=" * 70)
        
        return self.history


def train_model(
    data_path: str = 'data/train_state_model.json',
    num_epochs: int = 100,
    batch_size: int = 16,
    learning_rate: float = 0.001,
    use_class_weights: bool = False,
    patience: int = 20,
    save_path: str = 'checkpoints/model_selector.pth',
    device: str = None
) -> Tuple[MaxEntropyClassifier, Dict]:
    """
    完整训练流程
    
    Args:
        data_path: 训练数据路径
        num_epochs: 训练轮数
        batch_size: 批大小
        learning_rate: 学习率
        use_class_weights: 是否使用类别权重
        patience: Early stopping耐心值
        save_path: 模型保存路径
        device: 训练设备 (None=自动检测)
    
    Returns:
        (model, history): 训练好的模型和训练历史
    """
    # 设备检测
    if device is None:
        device = 'cuda' if torch.cuda.is_available() else 'cpu'
    print(f"使用设备: {device}")
    
    # 加载数据
    print("\n[1/4] 加载训练数据...")
    X, y = load_training_data(data_path)
    
    # 准备DataLoader
    print("\n[2/4] 准备DataLoader...")
    train_loader, val_loader = prepare_dataloaders(
        X, y, 
        train_ratio=0.8,
        batch_size=batch_size,
        shuffle=True
    )
    
    # 创建模型
    print("\n[3/4] 创建模型...")
    from .model_selector import create_model
    model = create_model(device=device)
    model.summary()
    
    # 类别权重（可选）
    class_weights = None
    if use_class_weights:
        print("\n计算类别权重...")
        class_weights = get_class_weights(y, num_classes=80)
    
    # 训练
    print("\n[4/4] 开始训练...")
    trainer = Trainer(
        model=model,
        device=device,
        learning_rate=learning_rate,
        use_class_weights=use_class_weights,
        class_weights=class_weights
    )
    
    history = trainer.fit(
        train_loader=train_loader,
        val_loader=val_loader,
        num_epochs=num_epochs,
        patience=patience,
        save_path=save_path,
        log_interval=10
    )
    
    return model, history


def evaluate_model(
    model_path: str = 'checkpoints/model_selector.pth',
    data_path: str = 'data/train_state_model.json',
    device: str = None
) -> Dict:
    """
    评估已训练的模型
    
    Args:
        model_path: 模型权重路径
        data_path: 测试数据路径
        device: 评估设备
    
    Returns:
        metrics: 评估指标
    """
    if device is None:
        device = 'cuda' if torch.cuda.is_available() else 'cpu'
    
    print(f"加载模型: {model_path}")
    
    # 加载模型
    from .model_selector import create_model
    model = create_model(device=device)
    
    checkpoint = torch.load(model_path, map_location=device)
    model.load_state_dict(checkpoint['model_state_dict'])
    model.eval()
    
    print(f"模型训练于Epoch {checkpoint['epoch']}")
    print(f"最佳验证准确率: {checkpoint['best_val_acc']:.3f}")
    
    # 加载数据
    X, y = load_training_data(data_path)
    _, val_loader = prepare_dataloaders(X, y, batch_size=16)
    
    # 评估
    trainer = Trainer(model, device=device)
    metrics = trainer.evaluate(val_loader)
    
    print("\n评估结果:")
    print(f"  Loss: {metrics['loss']:.4f}")
    print(f"  Top-1 Acc: {metrics['top1_acc']:.3f}")
    print(f"  Top-3 Acc: {metrics['top3_acc']:.3f}")
    print(f"  Top-5 Acc: {metrics['top5_acc']:.3f}")
    
    return metrics


def save_training_report(
    history: Dict,
    metrics: Dict,
    output_path: str = 'outputs/selector/training_metrics.json'
):
    """
    保存训练报告
    
    Args:
        history: 训练历史
        metrics: 最终评估指标
        output_path: 输出路径
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    report = {
        'timestamp': datetime.now().isoformat(),
        'best_epoch': len(history['train_loss']),
        'final_metrics': {
            'train_loss': float(history['train_loss'][-1]),
            'train_acc': float(history['train_acc'][-1]),
            'val_loss': float(history['val_loss'][-1]),
            'val_top1_acc': float(history['val_acc'][-1]),
            'val_top3_acc': float(history['val_top3_acc'][-1]),
            'val_top5_acc': float(history['val_top5_acc'][-1]),
        },
        'best_metrics': {
            'val_top1_acc': max(history['val_acc']),
            'val_top3_acc': max(history['val_top3_acc']),
            'val_top5_acc': max(history['val_top5_acc']),
        },
        'history': history
    }
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    print(f"\n训练报告已保存: {output_path}")


if __name__ == '__main__':
    # 完整训练流程
    print("=" * 70)
    print("MaxEntropy Model Selector - 训练脚本")
    print("=" * 70)
    
    model, history = train_model(
        data_path='../../data/train_state_model.json',
        num_epochs=100,
        batch_size=16,
        learning_rate=0.001,
        use_class_weights=False,
        patience=20,
        save_path='../../checkpoints/model_selector.pth',
        device=None  # 自动检测
    )
    
    # 保存报告
    save_training_report(
        history=history,
        metrics=history,
        output_path='../../outputs/selector/training_metrics.json'
    )
    
    print("\n✅ 训练完成!")
