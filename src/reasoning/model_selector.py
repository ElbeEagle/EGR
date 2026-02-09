"""
模型选择器 (Model Selector)

结合神经网络和规则系统选择下一个要应用的模型。
"""

import torch
from typing import Optional, List, Tuple, Dict
from src.selector.model_selector import MaxEntropyClassifier
from src.theorems.theorem_library import TheoremLibrary
from src.theorems.base_model import TheoremModel
from src.state.symbolic_state import SymbolicState
from src.state.abstract_state import AbstractState


class ModelSelector:
    """
    模型选择器
    
    封装神经网络预测 + 规则过滤的完整选择流程。
    支持多种选择策略。
    """
    
    def __init__(
        self,
        neural_network: MaxEntropyClassifier,
        theorem_library: TheoremLibrary,
        strategy: str = 'neural_top1',
        device: str = 'cpu'
    ):
        """
        初始化模型选择器
        
        Args:
            neural_network: 训练好的MaxEntropyClassifier
            theorem_library: 定理库
            strategy: 选择策略 ('neural_top1', 'neural_topk')
            device: 计算设备
        """
        self.neural_network = neural_network
        self.theorem_library = theorem_library
        self.strategy = strategy
        self.device = device
        
        # 确保神经网络在正确的设备上并处于eval模式
        self.neural_network.to(device)
        self.neural_network.eval()
    
    def select(
        self,
        symbolic_state: SymbolicState,
        abstract_state: AbstractState,
        top_k: int = 5
    ) -> Tuple[Optional[TheoremModel], Dict]:
        """
        选择下一个要应用的模型
        
        Args:
            symbolic_state: 符号状态（用于can_apply检查）
            abstract_state: 抽象状态（用于神经网络预测）
            top_k: Top-K候选数量
        
        Returns:
            (selected_model, selection_info): 选择的模型和选择信息
        """
        if self.strategy == 'neural_top1':
            return self._neural_top1_strategy(symbolic_state, abstract_state)
        elif self.strategy == 'neural_topk':
            return self._neural_topk_strategy(symbolic_state, abstract_state, top_k)
        else:
            raise ValueError(f"Unknown strategy: {self.strategy}")
    
    def _neural_top1_strategy(
        self,
        symbolic_state: SymbolicState,
        abstract_state: AbstractState
    ) -> Tuple[Optional[TheoremModel], Dict]:
        """
        策略1: 神经网络Top-1 + can_apply过滤
        
        流程：
        1. 神经网络预测Top-1
        2. 检查can_apply
        3. 如果可用返回，否则返回None
        
        Returns:
            (model, info): 模型对象和选择信息
        """
        # 1. 获取状态向量
        state_vector = torch.tensor(
            abstract_state.to_vector(),
            dtype=torch.float32,
            device=self.device
        )
        
        # 2. 神经网络预测
        with torch.no_grad():
            probs, best_model_id, entropy = self.neural_network.predict(state_vector)
        
        # 3. 获取模型对象
        model = self.theorem_library.get_model(best_model_id)
        
        # 4. 检查can_apply
        can_apply = False
        if model is not None:
            try:
                can_apply = model.can_apply(symbolic_state)
            except Exception as e:
                can_apply = False
        
        # 5. 构建选择信息
        selection_info = {
            'strategy': 'neural_top1',
            'predicted_model_id': best_model_id,
            'predicted_confidence': float(probs[best_model_id]),
            'prediction_entropy': float(entropy),
            'can_apply': can_apply,
            'model_available': model is not None
        }
        
        # 6. 返回结果
        if model is not None and can_apply:
            return model, selection_info
        else:
            return None, selection_info
    
    def _neural_topk_strategy(
        self,
        symbolic_state: SymbolicState,
        abstract_state: AbstractState,
        k: int = 5
    ) -> Tuple[Optional[TheoremModel], Dict]:
        """
        策略2: 神经网络Top-K + can_apply过滤
        
        流程：
        1. 神经网络预测Top-K
        2. 逐个检查can_apply
        3. 返回第一个可用的模型
        
        Returns:
            (model, info): 模型对象和选择信息
        """
        # 1. 获取状态向量
        state_vector = torch.tensor(
            abstract_state.to_vector(),
            dtype=torch.float32,
            device=self.device
        )
        
        # 2. 神经网络预测Top-K
        with torch.no_grad():
            probs, _, entropy = self.neural_network.predict(state_vector)
            top_k_probs, top_k_ids = self.neural_network.get_top_k(state_vector, k=k)
        
        # 3. 逐个尝试Top-K候选
        top_k_list = top_k_ids.tolist()
        top_k_probs_list = top_k_probs.tolist()
        
        candidates_info = []
        selected_model = None
        selected_rank = -1
        
        for rank, (model_id, prob) in enumerate(zip(top_k_list, top_k_probs_list)):
            model = self.theorem_library.get_model(model_id)
            
            can_apply = False
            if model is not None:
                try:
                    can_apply = model.can_apply(symbolic_state)
                except Exception:
                    can_apply = False
            
            candidates_info.append({
                'rank': rank + 1,
                'model_id': model_id,
                'model_name': model.name if model else f"Model_{model_id}",
                'probability': float(prob),
                'can_apply': can_apply,
                'model_available': model is not None
            })
            
            # 选择第一个可用的
            if selected_model is None and model is not None and can_apply:
                selected_model = model
                selected_rank = rank + 1
        
        # 4. 构建选择信息
        selection_info = {
            'strategy': 'neural_topk',
            'top_k': k,
            'prediction_entropy': float(entropy),
            'candidates': candidates_info,
            'selected_rank': selected_rank,
            'selected_model_id': selected_model.model_id if selected_model else None
        }
        
        return selected_model, selection_info
    
    def get_top_k_candidates(
        self,
        abstract_state: AbstractState,
        k: int = 5
    ) -> List[Tuple[int, float]]:
        """
        获取Top-K候选模型ID和概率
        
        Args:
            abstract_state: 抽象状态
            k: 候选数量
        
        Returns:
            [(model_id, probability), ...]: 候选列表
        """
        state_vector = torch.tensor(
            abstract_state.to_vector(),
            dtype=torch.float32,
            device=self.device
        )
        
        with torch.no_grad():
            top_k_probs, top_k_ids = self.neural_network.get_top_k(state_vector, k=k)
        
        return list(zip(top_k_ids.tolist(), top_k_probs.tolist()))
