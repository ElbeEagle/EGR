"""
Model 56: Triangle_Area_Formula
三角形面积公式

公式: S = (1/2) × 底 × 高
"""

import re
from ..base_model import TheoremModel


class TriangleAreaFormula(TheoremModel):
    """
    三角形面积公式
    
    前置条件:
    - 存在三角形
    - 有边长或高的信息
    
    输出:
    - geometric_relations: 三角形面积公式
    
    示例:
    S = (1/2) × 底 × 高
    S = (1/2) × a × b × sinC
    S = √[s(s-a)(s-b)(s-c)] (海伦公式)
    """
    
    def __init__(self):
        super().__init__(
            model_id=56,
            name="Triangle_Area_Formula",
            chinese_name="三角形面积公式"
        )
    
    def can_apply(self, state) -> bool:
        """
        检查是否可应用（放宽条件）
        
        条件:
        1. 存在三角形相关信息
        2. 或需要计算面积
        3. 或有多个点（可能形成三角形）
        """
        # 检查是否有三角形或面积相关
        for rel in state.geometric_relations:
            if any(kw in rel for kw in ['Triangle', '三角形', 'Area', '面积', 'Perimeter', '周长']):
                return True
        
        # 检查是否有焦点三角形（椭圆或双曲线）
        has_focal_points = any(
            'F1' in state.coordinates or 'F2' in state.coordinates or
            'F_1' in state.coordinates or 'F_2' in state.coordinates
            for _ in [1]
        )
        
        if has_focal_points:
            for entity_type in state.entities.values():
                if entity_type.lower() in ['ellipse', 'hyperbola', 'parabola']:
                    return True
        
        # 如果有至少3个点，可能需要计算三角形面积
        if len(state.coordinates) >= 3:
            return True
        
        # 如果有焦点相关的几何关系
        for rel in state.geometric_relations:
            if 'Focus' in rel or '焦点' in rel:
                return True
        
        return False
    
    def apply(self, state) -> bool:
        """
        应用模型，添加三角形面积公式
        """
        try:
            # 添加基本面积公式
            formulas = [
                "三角形面积公式:",
                "  S = (1/2) × 底 × 高",
                "  S = (1/2) × a × b × sinC",
            ]
        
            for formula in formulas:
                if formula not in state.geometric_relations:
                    state.geometric_relations.append(formula)
        
            # 对于焦点三角形，添加特殊公式
            has_ellipse = any(
                entity_type.lower() == 'ellipse'
                for entity_type in state.entities.values()
            )
            has_hyperbola = any(
                entity_type.lower() == 'hyperbola'
                for entity_type in state.entities.values()
            )
        
            if has_ellipse and 'b' in state.parameters:
                b_val = state.parameters['b']
                state.geometric_relations.append(
                    f"椭圆焦点三角形面积: S = {b_val}² × tan(θ/2), θ = ∠F₁PF₂"
                )
        
            if has_hyperbola and 'b' in state.parameters:
                b_val = state.parameters['b']
                state.geometric_relations.append(
                    f"双曲线焦点三角形面积: S = {b_val}² × cot(θ/2), θ = ∠F₁PF₂"
                )
        
            # 记录已应用的模型
            state.applied_models.append(self.model_id)
            return True

        except Exception:
            return False
