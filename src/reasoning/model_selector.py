"""
模型选择器 (Model Selector)

结合神经网络和规则系统选择下一个要应用的模型。
支持三种策略：neural_top1, neural_topk, three_layer_entropy
"""

import copy
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
        device: str = 'cpu',
        state_constructor=None,
        lambda_weights: Tuple[float, float, float] = (0.6, 0.3, 0.1)
    ):
        """
        初始化模型选择器
        
        Args:
            neural_network: 训练好的MaxEntropyClassifier
            theorem_library: 定理库
            strategy: 选择策略 ('neural_top1', 'neural_topk', 'three_layer_entropy')
            device: 计算设备
            state_constructor: 状态构造器（三层熵策略需要）
            lambda_weights: 三层熵的权重 (λ₁_P_Y_X, λ₂_InfoGain, λ₃_H_Y_X)
        """
        self.neural_network = neural_network
        self.theorem_library = theorem_library
        self.strategy = strategy
        self.device = device
        self.state_constructor = state_constructor
        self.lambda_weights = lambda_weights
        
        # 熵估计器（三层熵策略）
        self.entropy_estimator = None
        if strategy == 'three_layer_entropy':
            from src.reasoning.entropy_estimator import EntropyEstimator
            self.entropy_estimator = EntropyEstimator(mode='heuristic')
        
        # 确保神经网络在正确的设备上并处于eval模式
        self.neural_network.to(device)
        self.neural_network.eval()
    
    def select(
        self,
        symbolic_state: SymbolicState,
        abstract_state: AbstractState,
        top_k: int = 10,
        excluded_models: Optional[set] = None
    ) -> Tuple[Optional[TheoremModel], Dict]:
        """
        选择下一个要应用的模型
        
        Args:
            symbolic_state: 符号状态（用于can_apply检查）
            abstract_state: 抽象状态（用于神经网络预测）
            top_k: Top-K候选数量
            excluded_models: 要排除的模型ID集合（已应用过的模型）
        
        Returns:
            (selected_model, selection_info): 选择的模型和选择信息
        """
        # 自动排除已应用过的模型
        if excluded_models is None:
            excluded_models = set(getattr(symbolic_state, 'applied_models', []))
        
        if self.strategy == 'neural_top1':
            return self._neural_top1_strategy(symbolic_state, abstract_state, excluded_models)
        elif self.strategy == 'neural_topk':
            return self._neural_topk_strategy(symbolic_state, abstract_state, top_k, excluded_models)
        elif self.strategy == 'three_layer_entropy':
            return self._three_layer_entropy_strategy(symbolic_state, abstract_state, top_k, excluded_models)
        else:
            raise ValueError(f"Unknown strategy: {self.strategy}")
    
    def _neural_top1_strategy(
        self,
        symbolic_state: SymbolicState,
        abstract_state: AbstractState,
        excluded_models: set = None
    ) -> Tuple[Optional[TheoremModel], Dict]:
        """
        策略1: 神经网络Top-1 + can_apply过滤
        
        流程：
        1. 神经网络预测Top-1
        2. 如果已排除则跳过
        3. 检查can_apply
        4. 如果可用返回，否则返回None
        
        Returns:
            (model, info): 模型对象和选择信息
        """
        if excluded_models is None:
            excluded_models = set()
        
        # 1. 获取状态向量
        state_vector = torch.tensor(
            abstract_state.to_vector(),
            dtype=torch.float32,
            device=self.device
        )
        
        # 2. 神经网络预测Top-K（扩大范围以跳过已排除的）
        with torch.no_grad():
            probs, _, entropy = self.neural_network.predict(state_vector)
            top_k_probs, top_k_ids = self.neural_network.get_top_k(state_vector, k=10)
        
        # 3. 找到第一个未排除且可用的模型
        for model_id in top_k_ids.tolist():
            if model_id in excluded_models:
                continue
            
            model = self.theorem_library.get_model(model_id)
            
            can_apply = False
            if model is not None:
                try:
                    can_apply = model.can_apply(symbolic_state)
                except Exception:
                    can_apply = False
            
            if model is not None and can_apply:
                selection_info = {
                    'strategy': 'neural_top1',
                    'predicted_model_id': model_id,
                    'predicted_confidence': float(probs[model_id]),
                    'prediction_entropy': float(entropy),
                    'can_apply': True,
                    'model_available': True,
                    'excluded_count': len(excluded_models)
                }
                return model, selection_info
        
        # 没有可用的
        selection_info = {
            'strategy': 'neural_top1',
            'prediction_entropy': float(entropy),
            'can_apply': False,
            'excluded_count': len(excluded_models)
        }
        return None, selection_info
    
    def _neural_topk_strategy(
        self,
        symbolic_state: SymbolicState,
        abstract_state: AbstractState,
        k: int = 10,
        excluded_models: set = None
    ) -> Tuple[Optional[TheoremModel], Dict]:
        """
        策略2: 神经网络Top-K + can_apply过滤 + 排除已应用模型
        
        流程：
        1. 神经网络预测Top-K
        2. 跳过已排除的模型
        3. 逐个检查can_apply
        4. 返回第一个可用的模型
        
        Returns:
            (model, info): 模型对象和选择信息
        """
        if excluded_models is None:
            excluded_models = set()
        
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
            # 跳过已排除的模型
            excluded = model_id in excluded_models
            
            model = self.theorem_library.get_model(model_id)
            
            can_apply = False
            if model is not None and not excluded:
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
                'model_available': model is not None,
                'excluded': excluded
            })
            
            # 选择第一个未排除且可用的
            if selected_model is None and model is not None and can_apply and not excluded:
                selected_model = model
                selected_rank = rank + 1
        
        # 4. 构建选择信息
        selection_info = {
            'strategy': 'neural_topk',
            'top_k': k,
            'prediction_entropy': float(entropy),
            'candidates': candidates_info,
            'selected_rank': selected_rank,
            'selected_model_id': selected_model.model_id if selected_model else None,
            'excluded_count': len(excluded_models)
        }
        
        if selected_model:
            selection_info['predicted_confidence'] = float(probs[selected_model.model_id])
        
        return selected_model, selection_info
    
    def _three_layer_entropy_strategy(
        self,
        symbolic_state: SymbolicState,
        abstract_state: AbstractState,
        k: int = 10,
        excluded_models: set = None
    ) -> Tuple[Optional[TheoremModel], Dict]:
        """
        策略3: 三层熵架构
        
        综合评分 = λ₁·P(Y|X) + λ₂·InfoGain - λ₃·H(Y|X)
        
        Layer 1: P(Y|X) — 神经网络模型选择概率
        Layer 2: InfoGain = H(S_current) - H(S_next) — 信息增益
        Layer 3: H(Y|X) — 预测不确定性惩罚
        """
        if excluded_models is None:
            excluded_models = set()
        
        if self.entropy_estimator is None:
            from src.reasoning.entropy_estimator import EntropyEstimator
            self.entropy_estimator = EntropyEstimator(mode='heuristic')
        
        λ1, λ2, λ3 = self.lambda_weights
        
        # 1. 神经网络预测
        state_vector = torch.tensor(
            abstract_state.to_vector(),
            dtype=torch.float32,
            device=self.device
        )
        
        with torch.no_grad():
            probs, _, entropy = self.neural_network.predict(state_vector)
            top_k_probs, top_k_ids = self.neural_network.get_top_k(state_vector, k=k)
        
        h_y_x = float(entropy)  # Layer 3: 预测熵
        h_current = self.entropy_estimator.estimate(abstract_state)  # 当前状态熵
        
        # 2. 对每个候选模型计算综合评分
        candidates = []
        
        for model_id in top_k_ids.tolist():
            if model_id in excluded_models:
                continue
            
            model = self.theorem_library.get_model(model_id)
            if model is None:
                continue
            
            try:
                can_apply = model.can_apply(symbolic_state)
            except Exception:
                can_apply = False
            
            if not can_apply:
                continue
            
            # Layer 1: P(Y|X)
            p_y_x = float(probs[model_id])
            
            # Layer 2: InfoGain（模拟应用，估计新状态熵）
            info_gain = 0.0
            if self.state_constructor:
                try:
                    sim_state = copy.deepcopy(symbolic_state)
                    apply_result = model.apply(sim_state)
                    if apply_result is None or apply_result:
                        sim_abstract = self.state_constructor.update_abstract_state(
                            sim_state, abstract_state
                        )
                        h_next = self.entropy_estimator.estimate(sim_abstract)
                        info_gain = h_current - h_next
                except Exception:
                    info_gain = 0.0
            
            # 综合评分
            score = λ1 * p_y_x + λ2 * info_gain - λ3 * h_y_x
            
            candidates.append({
                'model_id': model_id,
                'model': model,
                'score': score,
                'p_y_x': p_y_x,
                'info_gain': info_gain,
                'h_y_x': h_y_x,
            })
        
        # 3. 选择最高分
        if not candidates:
            return None, {
                'strategy': 'three_layer_entropy',
                'h_current': h_current,
                'h_y_x': h_y_x,
                'excluded_count': len(excluded_models),
            }
        
        best = max(candidates, key=lambda c: c['score'])
        
        selection_info = {
            'strategy': 'three_layer_entropy',
            'predicted_confidence': best['p_y_x'],
            'prediction_entropy': best['h_y_x'],
            'info_gain': best['info_gain'],
            'score': best['score'],
            'h_current': h_current,
            'candidates_evaluated': len(candidates),
            'lambda_weights': list(self.lambda_weights),
        }
        
        return best['model'], selection_info
    
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
