"""
Model 57: Triangle_Area_With_Sin
三角形面积公式（正弦）

公式: S = (1/2) * a * b * sin(C)
用于: 已知两边和夹角求三角形面积
"""

import re
from ..base_model import TheoremModel


class TriangleAreaWithSin(TheoremModel):
    """
    三角形面积公式（正弦）
    
    前置条件:
    - 存在三角形或三角形关系
    - 已知两边长和夹角（或相关信息）
    
    输出:
    - 三角形面积 S = (1/2) * a * b * sin(C)
    
    示例:
    输入: a=3, b=4, angle_C=90°
    输出: S = 6
    """
    
    def __init__(self):
        super().__init__(
            model_id=57,
            name="Triangle_Area_With_Sin",
            chinese_name="三角形面积公式(正弦)"
        )
    
    def can_apply(self, state) -> bool:
        """
        检查是否可应用
        
        条件:
        1. 存在三角形或面积相关的描述
        2. 有角度信息或边长信息
        """
        # 条件1: 存在三角形、面积或角度相关描述
        has_triangle_info = False
        for rel in state.geometric_relations:
            if any(kw in rel for kw in ['Triangle', 'Area', 'Angle', 'Sin', 'sin', '三角形', '面积']):
                has_triangle_info = True
                break
        
        if not has_triangle_info:
            return False
        
        # 条件2: 有一些几何信息（距离、角度等）
        has_geometric_info = (
            len(state.parameters) > 0 or
            len(state.coordinates) > 0 or
            any('Distance' in rel for rel in state.geometric_relations)
        )
        
        return has_geometric_info
    
    def apply(self, state) -> None:
        """
        应用模型，计算面积
        """
        # 查找角度和边长信息
        # 如果存在焦点三角形，可能需要使用正弦面积公式
        
        # 简化处理：添加面积公式关系
        for rel in state.geometric_relations:
            # 如果提到角度和距离
            if 'Angle' in rel or 'Sin' in rel:
                # 添加面积关系
                state.geometric_relations.append("Area = (1/2) * side1 * side2 * sin(angle)")
                break
        
        # 记录已应用的模型
        state.applied_models.append(self.model_id)
