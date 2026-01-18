"""
Model 70: Incircle_Radius_Formula
内切圆半径公式

公式: r = S/s，其中S是三角形面积，s是半周长
或: r = (a + b - c)/2 (直角三角形)
"""

import re
from ..base_model import TheoremModel


class IncircleRadiusFormula(TheoremModel):
    """
    内切圆半径公式
    
    前置条件:
    - 存在三角形
    - 存在内切圆
    
    输出:
    - 内切圆半径公式
    
    示例:
    输入: 三角形ABC，内切圆半径r
    输出: r = S/s，其中 s = (a+b+c)/2
    """
    
    def __init__(self):
        super().__init__(
            model_id=70,
            name="Incircle_Radius_Formula",
            chinese_name="内切圆半径公式"
        )
    
    def can_apply(self, state) -> bool:
        """
        检查是否可应用
        
        条件:
        1. 存在三角形
        2. 存在内切圆或切圆
        """
        # 条件1: 存在三角形
        has_triangle = any(
            kw in rel for rel in state.geometric_relations
            for kw in ['Triangle', '三角形']
        )
        
        # 条件2: 存在内切圆
        has_incircle = any(
            kw in rel for rel in state.geometric_relations
            for kw in ['Incircle', 'InscribedCircle', 'Tangent', '内切', '切圆']
        )
        
        return has_triangle and has_incircle
    
    def apply(self, state) -> None:
        """
        应用模型，建立内切圆半径关系
        """
        # 添加内切圆半径公式
        state.geometric_relations.append("IncircleRadius: r = S/s")
        state.geometric_relations.append("SemiPerimeter: s = (a + b + c)/2")
        state.geometric_relations.append("IncircleFormula: r = (a + b + c)/2 - (a or b or c)")
        
        # 如果是直角三角形
        state.geometric_relations.append("RightTriangle: r = (a + b - c)/2")
        
        # 添加参数
        state.parameters['incircle_radius'] = "S/s"
        
        # 记录已应用的模型
        state.applied_models.append(self.model_id)
