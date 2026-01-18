"""
Model 14: Ellipse_Eccentricity_Range
椭圆离心率范围

公式: 0 < e < 1
用于: 椭圆离心率的取值范围约束
"""

import re
from ..base_model import TheoremModel


class EllipseEccentricityRange(TheoremModel):
    """
    椭圆离心率范围
    
    前置条件:
    - 实体为椭圆
    - 讨论离心率
    
    输出:
    - 约束条件: 0 < e < 1
    
    示例:
    输入: 椭圆离心率 e
    输出: 0 < e < 1
    """
    
    def __init__(self):
        super().__init__(
            model_id=14,
            name="Ellipse_Eccentricity_Range",
            chinese_name="椭圆离心率范围"
        )
    
    def can_apply(self, state) -> bool:
        """
        检查是否可应用
        
        条件:
        1. 存在椭圆实体
        2. 涉及离心率
        """
        # 条件1: 存在椭圆
        has_ellipse = any(
            entity_type.lower() == 'ellipse'
            for entity_type in state.entities.values()
        )
        if not has_ellipse:
            return False
        
        # 条件2: 涉及离心率
        has_eccentricity = (
            'e' in state.parameters or
            any('Eccentricity' in rel or '离心率' in rel 
                for rel in state.geometric_relations)
        )
        
        return has_eccentricity
    
    def apply(self, state) -> None:
        """
        应用模型，添加离心率范围约束
        """
        # 添加约束条件
        constraint_1 = "e > 0"
        constraint_2 = "e < 1"
        
        if constraint_1 not in state.constraints:
            state.constraints.append(constraint_1)
        
        if constraint_2 not in state.constraints:
            state.constraints.append(constraint_2)
        
        # 添加到几何关系
        state.geometric_relations.append("EccentricityRange(Ellipse) = (0, 1)")
        
        # 记录已应用的模型
        state.applied_models.append(self.model_id)
