"""
状态熵估计器 (Entropy Estimator)

实现三层熵架构中的 H(S) 估计。

两种模式：
1. 启发式估计（不需要训练，立即可用）
2. 神经网络估计（需要训练）
"""

import math
from typing import Optional
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
    
    def __init__(self, mode: str = 'heuristic'):
        """
        Args:
            mode: 'heuristic'（启发式）或 'neural'（神经网络）
        """
        self.mode = mode
        self.neural_model = None  # 预留给神经网络模式
    
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
        else:
            raise ValueError(f"Unknown mode: {self.mode}")
    
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
