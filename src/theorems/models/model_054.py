"""
Model 54: Midpoint_Formula
中点公式

公式: M = ((x1+x2)/2, (y1+y2)/2)
用于: 计算两点的中点坐标
"""

import re
from ..base_model import TheoremModel


class MidpointFormula(TheoremModel):
    """
    中点公式
    
    前置条件:
    - 已知两个点的坐标
    
    输出:
    - 中点坐标
    
    示例:
    输入: A(1, 2), B(3, 4)
    输出: M(2, 3)
    """
    
    def __init__(self):
        super().__init__(
            model_id=54,
            name="Midpoint_Formula",
            chinese_name="中点公式"
        )
    
    def can_apply(self, state) -> bool:
        """
        检查是否可应用
        
        条件:
        1. 至少有两个点的坐标
        2. 或存在中点关系的几何关系
        """
        # 条件1: 至少有2个点的坐标
        if len(state.coordinates) >= 2:
            return True
        
        # 条件2: 存在中点关系
        for rel in state.geometric_relations:
            if 'MidPoint' in rel or 'Midpoint' in rel or '中点' in rel:
                return True
        
        return False
    
    def apply(self, state) -> None:
        """
        应用模型，计算中点
        """
        # 查找中点关系
        for rel in state.geometric_relations:
            if 'MidPoint' in rel or 'Midpoint' in rel:
                # 提取中点关系: MidPoint(A, B) = M
                match = re.search(r'MidPoint\((\w+),\s*(\w+)\)\s*=\s*(\w+)', rel)
                if match:
                    point1 = match.group(1)
                    point2 = match.group(2)
                    midpoint = match.group(3)
                    
                    # 如果两个点的坐标已知，计算中点
                    if point1 in state.coordinates and point2 in state.coordinates:
                        coord1 = state.coordinates[point1]
                        coord2 = state.coordinates[point2]
                        
                        # 计算中点坐标
                        mid_x = f"({coord1[0]} + {coord2[0]})/2"
                        mid_y = f"({coord1[1]} + {coord2[1]})/2"
                        
                        state.coordinates[midpoint] = (mid_x, mid_y)
                        state.geometric_relations.append(f"Coordinate({midpoint}) = ({mid_x}, {mid_y})")
        
        # 如果有线段AB的中点M的描述
        for rel in state.geometric_relations:
            # 模式: M是AB的中点
            if '中点' in rel:
                # 尝试提取相关点
                # 简化处理：如果有足够的坐标信息，添加中点关系
                pass
        
        # 记录已应用的模型
        state.applied_models.append(self.model_id)
