"""
Model 65: Discriminant_Delta
判别式Δ

公式: Δ = b² - 4ac
用于: 判断方程根的情况
"""

import re
from ..base_model import TheoremModel


class DiscriminantDelta(TheoremModel):
    """
    判别式Δ
    
    前置条件:
    - 存在二次方程
    - 或存在交点、根的讨论
    
    输出:
    - 判别式 Δ = b² - 4ac
    - Δ > 0: 两个不同实根
    - Δ = 0: 两个相等实根
    - Δ < 0: 无实根
    
    示例:
    输入: ax² + bx + c = 0
    输出: Δ = b² - 4ac
    """
    
    def __init__(self):
        super().__init__(
            model_id=65,
            name="Discriminant_Delta",
            chinese_name="判别式Δ"
        )
    
    def can_apply(self, state) -> bool:
        """
        检查是否可应用
        
        条件:
        1. 存在二次方程
        2. 或讨论交点、根的情况
        """
        # 条件1: 存在二次方程（包含 x², y² 等）
        has_quadratic = any(
            '^2' in eq for eq in state.equations
        )
        
        # 条件2: 讨论交点、根、判别式
        has_discussion = any(
            kw in rel for rel in state.geometric_relations
            for kw in ['Intersection', 'Root', 'Delta', 'Discriminant', '交点', '根', '判别式']
        )
        
        return has_quadratic or has_discussion
    
    def apply(self, state) -> None:
        """
        应用模型，计算判别式
        """
        # 查找二次方程的系数
        for eq in state.equations:
            # 简化处理：添加判别式关系
            if '^2' in eq:
                state.geometric_relations.append("Discriminant: Δ = b² - 4ac")
                state.parameters['Delta'] = "b^2 - 4*a*c"
                break
        
        # 添加判别式与根的关系
        state.geometric_relations.append("Δ > 0 => Two distinct real roots")
        state.geometric_relations.append("Δ = 0 => Two equal real roots")
        state.geometric_relations.append("Δ < 0 => No real roots")
        
        # 记录已应用的模型
        state.applied_models.append(self.model_id)
