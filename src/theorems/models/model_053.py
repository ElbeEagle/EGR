"""
Model 53: Two_Points_Distance
两点距离公式

公式: d = √[(x₂-x₁)² + (y₂-y₁)²]
"""

import re
from ..base_model import TheoremModel


class TwoPointsDistance(TheoremModel):
    """
    两点距离公式
    
    前置条件:
    - 存在两个点的坐标
    
    输出:
    - parameters: 距离值（如果可以计算）
    - geometric_relations: 距离公式
    
    示例:
    输入: A(1, 2), B(4, 6)
    输出: |AB| = √[(4-1)² + (6-2)²] = 5
    """
    
    def __init__(self):
        super().__init__(
            model_id=53,
            name="Two_Points_Distance",
            chinese_name="两点距离公式"
        )
    
    def can_apply(self, state) -> bool:
        """
        检查是否可应用
        
        条件:
        1. 至少有两个点的坐标
        """
        # 统计已知坐标的点数
        coord_count = len(state.coordinates)
        
        if coord_count >= 2:
            return True
        
        # 或者有距离计算需求的几何关系
        for rel in state.geometric_relations:
            if 'Distance' in rel or '距离' in rel:
                return True
        
        return False
    
    def apply(self, state) -> bool:
        """
        应用模型，添加两点距离公式
        """
        try:
            # 添加通用公式
            relation = "两点距离公式: d = √[(x₂-x₁)² + (y₂-y₁)²]"
        
            if relation not in state.geometric_relations:
                state.geometric_relations.append(relation)
        
            # 如果有具体的点坐标，计算距离
            coord_list = list(state.coordinates.items())
        
            if len(coord_list) >= 2:
                # 计算主要点对的距离
                for i in range(len(coord_list)):
                    for j in range(i + 1, min(i + 3, len(coord_list))):  # 限制计算量
                        point1_name, point1_coord = coord_list[i]
                        point2_name, point2_coord = coord_list[j]
                    
                        # 尝试计算距离
                        distance = self._calculate_distance(point1_coord, point2_coord)
                    
                        if distance is not None:
                            distance_key = f"dist_{point1_name}_{point2_name}"
                            state.parameters[distance_key] = str(distance)
                            state.geometric_relations.append(
                                f"|{point1_name}{point2_name}| = {distance}"
                            )
        
            # 记录已应用的模型
            state.applied_models.append(self.model_id)
    
            return True

        except Exception:
            return False
    def _calculate_distance(self, coord1, coord2):
        """
        计算两点间距离
        
        Args:
            coord1: (x1, y1) 或 [x1, y1]
            coord2: (x2, y2) 或 [x2, y2]
        
        Returns:
            distance: 距离值，失败返回 None
        """
        try:
            x1, y1 = float(coord1[0]), float(coord1[1])
            x2, y2 = float(coord2[0]), float(coord2[1])
            
            distance = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
            
            # 格式化输出
            if distance == int(distance):
                return int(distance)
            else:
                return round(distance, 4)
        except:
            return None
