"""
Model 46: Point_Difference_Method_Hyperbola
点差法（双曲线）

用于: 双曲线中点弦问题，利用点差法求斜率
公式: k = b²x₀/(a²y₀)，其中(x₀, y₀)是弦中点
"""

import re
from ..base_model import TheoremModel


class PointDifferenceMethodHyperbola(TheoremModel):
    """
    点差法（双曲线）
    
    前置条件:
    - 实体为双曲线
    - 存在弦或中点
    - 已知参数 a, b
    
    输出:
    - 斜率公式: k = b²x₀/(a²y₀)
    
    示例:
    输入: 双曲线 x²/a² - y²/b² = 1，弦AB中点M(x₀, y₀)
    输出: k_AB = b²x₀/(a²y₀)
    """
    
    def __init__(self):
        super().__init__(
            model_id=46,
            name="Point_Difference_Method_Hyperbola",
            chinese_name="点差法(双曲线)"
        )
    
    def can_apply(self, state) -> bool:
        """
        检查是否可应用
        
        条件:
        1. 存在双曲线
        2. 存在中点或弦
        3. 已知参数 a, b 或 a², b²
        """
        # 条件1: 存在双曲线
        has_hyperbola = any(
            entity_type.lower() == 'hyperbola'
            for entity_type in state.entities.values()
        )
        if not has_hyperbola:
            return False
        
        # 条件2: 存在中点或弦
        has_midpoint = any(
            kw in rel for rel in state.geometric_relations
            for kw in ['MidPoint', 'Midpoint', 'Chord', '中点', '弦']
        )
        if not has_midpoint:
            return False
        
        # 条件3: 已知参数
        has_params = ('a' in state.parameters or 'a^2' in state.parameters) and \
                     ('b' in state.parameters or 'b^2' in state.parameters)
        
        return has_params
    
    def apply(self, state) -> bool:
        """
        应用模型，建立斜率关系
        """
        try:
            # 获取参数
            a_squared = state.parameters.get('a^2', f"{state.parameters.get('a', 'a')}^2")
            b_squared = state.parameters.get('b^2', f"{state.parameters.get('b', 'b')}^2")
        
            # 点差法斜率公式
            slope_formula = f"k = {b_squared} * x0 / ({a_squared} * y0)"
        
            # 添加到几何关系
            state.geometric_relations.append(f"ChordSlopeFormula(Hyperbola): {slope_formula}")
            state.geometric_relations.append("PointDifferenceMethod: k·k_OM = b²/a²")
        
            # 记录已应用的模型
            state.applied_models.append(self.model_id)
            return True

        except Exception:
            return False
