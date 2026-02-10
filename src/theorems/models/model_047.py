"""
Model 47: Cosine_Law
余弦定理

公式: c² = a² + b² - 2ab·cosC
用于计算三角形的边长或角度
"""

import re
from ..base_model import TheoremModel


class CosineLaw(TheoremModel):
    """
    余弦定理
    
    前置条件:
    - 存在三角形相关信息
    - 需要计算边长或角度
    
    输出:
    - geometric_relations: 余弦定理公式
    
    示例:
    已知三角形两边和夹角，求第三边
    """
    
    def __init__(self):
        super().__init__(
            model_id=47,
            name="Cosine_Law",
            chinese_name="余弦定理"
        )
    
    def can_apply(self, state) -> bool:
        """
        检查是否可应用
        
        条件:
        1. 存在三角形（特别是焦点三角形）
        2. 有角度或边长信息
        """
        # 检查是否有三角形相关信息
        for rel in state.geometric_relations:
            # 焦点三角形
            if 'Triangle' in rel or '三角形' in rel:
                return True
            # 角度信息
            if 'angle' in rel.lower() or '角' in rel or '∠' in rel:
                return True
        
        # 检查是否有焦点（隐含三角形）
        if 'F1' in state.coordinates or 'F2' in state.coordinates:
            # 有焦点和曲线上的点，可能需要余弦定理
            for entity_type in state.entities.values():
                if entity_type.lower() in ['ellipse', 'hyperbola']:
                    return True
        
        return False
    
    def apply(self, state) -> bool:
        """
        应用模型，添加余弦定理
        """
        try:
            # 添加通用余弦定理公式
            relation = "余弦定理: c² = a² + b² - 2ab·cosC"
        
            if relation not in state.geometric_relations:
                state.geometric_relations.append(relation)
        
            # 对于焦点三角形，添加更具体的形式
            has_focal_triangle = any(
                'F1' in rel or 'F2' in rel or '焦点' in rel
                for rel in state.geometric_relations
            )
        
            if has_focal_triangle:
                state.geometric_relations.append(
                    "焦点三角形: |PF₁|² + |PF₂|² - 2|PF₁||PF₂|·cosθ = |F₁F₂|²"
                )
                state.geometric_relations.append(
                    "其中: |F₁F₂| = 2c, θ = ∠F₁PF₂"
                )
        
            # 记录已应用的模型
            state.applied_models.append(self.model_id)
            return True

        except Exception:
            return False
