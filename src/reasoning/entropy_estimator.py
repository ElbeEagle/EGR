"""
状态熵估计器 (Entropy Estimator)

实现三层熵架构中的 H(S) 估计。

两种模式：
1. 启发式估计（不需要训练，立即可用）
2. 神经网络估计（需要训练）
"""

import json
from pathlib import Path
from typing import Any, Dict, Optional, Sequence

from src.state.abstract_state import AbstractState


class EntropyEstimator:
    """
    状态熵估计器
    
    H(S) 估计当前状态的不确定性/信息熵。
    H(S) ≈ 1 - completeness_score（启发式）
    
    用途：
    - 计算 InfoGain = H(S_current) - H(S_next)
    - 选择最大化信息增益的模型
    """
    
    def __init__(
        self,
        mode: str = 'heuristic',
        model_path: Optional[str] = None,
        weights: Optional[Sequence[float]] = None,
        bias: float = 0.0
    ):
        """
        Args:
            mode: 'heuristic'（启发式）或 'learned'/'linear'/'neural'（学习型线性回归器）
            model_path: learned-linear JSON模型路径
            weights: learned-linear 权重（28维）
            bias: learned-linear 偏置
        """
        self.mode = mode
        self.weights = list(weights) if weights is not None else None
        self.bias = float(bias)
        self.model_metadata: Dict[str, Any] = {}

        if model_path is not None:
            self.load_learned_model(model_path)
    
    def estimate(self, abstract_state: AbstractState) -> float:
        """
        估计状态熵 H(S)
        
        Args:
            abstract_state: 抽象状态
        
        Returns:
            float: 熵值 (0-1)，越高表示越不确定
        """
        if self.mode == 'heuristic':
            return self._heuristic_estimate(abstract_state)
        if self.mode in {'learned', 'linear', 'neural'}:
            return self.estimate_from_vector(abstract_state.to_vector())
        raise ValueError(f"Unknown mode: {self.mode}")

    def estimate_from_vector(self, state_vector: Sequence[float]) -> float:
        """
        从状态向量估计H(S)，用于训练/报告脚本复用 learned-linear 模型。
        """
        if self.mode == 'heuristic':
            raise ValueError("Heuristic mode requires an AbstractState, not a raw vector")

        if self.weights is None:
            raise ValueError("Learned entropy estimator has no loaded weights")

        if len(state_vector) != len(self.weights):
            raise ValueError(
                f"State vector dimension mismatch: {len(state_vector)} vs {len(self.weights)}"
            )

        entropy = self.bias
        for weight, value in zip(self.weights, state_vector):
            entropy += weight * value
        return max(0.0, min(1.0, float(entropy)))

    def load_learned_model(self, model_path: str) -> None:
        """
        加载由 scripts/entropy/train_entropy_estimator.py 生成的线性熵模型。
        """
        path = Path(model_path)
        with path.open('r', encoding='utf-8') as f:
            payload = json.load(f)

        weights = payload.get('weights')
        if not isinstance(weights, list) or not weights:
            raise ValueError(f"Invalid learned entropy model: missing weights in {model_path}")

        self.weights = [float(w) for w in weights]
        self.bias = float(payload.get('bias', 0.0))
        self.mode = 'learned'
        self.model_metadata = {
            key: value
            for key, value in payload.items()
            if key not in {'weights', 'bias'}
        }

    def compare(
        self,
        abstract_state: AbstractState,
        learned_model_path: Optional[str] = None
    ) -> Dict[str, float]:
        """
        返回 heuristic 与 learned estimator 的可比输出。
        """
        heuristic_entropy = self._heuristic_estimate(abstract_state)

        if learned_model_path is not None:
            learned = EntropyEstimator(mode='learned', model_path=learned_model_path)
        elif self.mode in {'learned', 'linear', 'neural'}:
            learned = self
        else:
            return {'heuristic_entropy': heuristic_entropy}

        learned_entropy = learned.estimate_from_vector(abstract_state.to_vector())
        return {
            'heuristic_entropy': heuristic_entropy,
            'learned_entropy': learned_entropy,
            'learned_minus_heuristic': learned_entropy - heuristic_entropy
        }

    @classmethod
    def from_model_file(cls, model_path: str) -> 'EntropyEstimator':
        """构造 learned-linear estimator。"""
        return cls(mode='learned', model_path=model_path)
    
    def _heuristic_estimate(self, state: AbstractState) -> float:
        """
        启发式熵估计
        
        综合考虑：
        1. 完整度（主要因素）
        2. 已知参数数量
        3. 推理深度
        4. 信息特征覆盖度
        """
        # 基础：1 - completeness
        base_entropy = 1.0 - state.completeness_score
        
        # 参数因子：参数越多，熵越低
        param_count = len(state.has_parameters) if state.has_parameters else 0
        param_factor = max(0, 1.0 - param_count * 0.08)
        
        # 深度因子：推理越深，熵越低（已经做了更多工作）
        depth_factor = max(0, 1.0 - state.reasoning_depth * 0.05)
        
        # 信息特征覆盖度
        info_features = sum([
            state.has_equation,
            state.has_focus_info,
            state.has_vertex_info,
            state.has_point_on_curve,
            state.has_asymptote_info,
            state.has_directrix_info,
            state.has_tangent_info,
            state.has_distance_constraint,
            state.has_angle_constraint,
            state.has_perpendicular,
        ])
        info_factor = max(0, 1.0 - info_features * 0.06)
        
        # 综合（加权平均）
        entropy = 0.5 * base_entropy + 0.2 * param_factor + 0.15 * depth_factor + 0.15 * info_factor
        
        return max(0.0, min(1.0, entropy))
    
    def compute_info_gain(
        self,
        current_state: AbstractState,
        next_state: AbstractState
    ) -> float:
        """
        计算信息增益
        
        InfoGain = H(S_current) - H(S_next)
        
        正值表示信息增加（好），负值表示信息减少（坏）
        
        Args:
            current_state: 当前状态
            next_state: 应用模型后的状态
        
        Returns:
            float: 信息增益
        """
        h_current = self.estimate(current_state)
        h_next = self.estimate(next_state)
        return h_current - h_next

    def compute_info_gain_from_vectors(
        self,
        current_vector: Sequence[float],
        next_vector: Sequence[float]
    ) -> float:
        """
        learned-linear 模式下直接从向量计算信息增益。
        """
        h_current = self.estimate_from_vector(current_vector)
        h_next = self.estimate_from_vector(next_vector)
        return h_current - h_next
