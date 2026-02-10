"""
Model 55: Slope_Formula
斜率公式

公式: k = (y₂ - y₁) / (x₂ - x₁)
用于: 已知两点坐标，计算直线斜率
"""

import re
from itertools import combinations
from ..base_model import TheoremModel


class SlopeFormula(TheoremModel):
    """
    斜率公式
    
    前置条件:
    - 至少有两个点的坐标
    
    输出:
    - parameters: 斜率值 k 或 k_AB 等
    - geometric_relations: 斜率公式
    
    示例:
    输入: A(1, 2), B(3, 6)
    输出: k_AB = (6-2)/(3-1) = 2
    """
    
    def __init__(self):
        super().__init__(
            model_id=55,
            name="Slope_Formula",
            chinese_name="斜率公式"
        )
    
    def can_apply(self, state) -> bool:
        """
        检查是否可应用
        
        条件:
        1. 至少有两个点的坐标
        """
        return len(state.coordinates) >= 2
    
    def apply(self, state) -> bool:
        """
        应用模型，计算各点对之间的斜率
        """
        try:
            # 添加通用公式
            general_formula = "斜率公式: k = (y₂ - y₁) / (x₂ - x₁)"
            if general_formula not in state.geometric_relations:
                state.geometric_relations.append(general_formula)
            
            # 获取所有点坐标
            coord_list = list(state.coordinates.items())
            
            # 对所有点对计算斜率（限制计算量，最多处理前6个点）
            points_to_process = coord_list[:6]
            
            slopes_computed = []
            
            for (name1, coord1), (name2, coord2) in combinations(points_to_process, 2):
                slope = self._calculate_slope(coord1, coord2)
                
                # 构造参数键名
                slope_key = f"k_{name1}{name2}"
                
                if slope is not None:
                    # slope 为 "undefined" 或数值字符串
                    if slope == "undefined":
                        # 斜率不存在（垂直线）
                        rel_str = (
                            f"Slope({name1}{name2}): 斜率不存在 "
                            f"(x₁ = x₂ = {coord1[0]}，直线垂直于x轴)"
                        )
                        if rel_str not in state.geometric_relations:
                            state.geometric_relations.append(rel_str)
                        state.parameters[slope_key] = "undefined"
                    else:
                        # 斜率存在
                        state.parameters[slope_key] = str(slope)
                        rel_str = (
                            f"Slope({name1}{name2}) = "
                            f"({coord2[1]} - {coord1[1]}) / ({coord2[0]} - {coord1[0]}) "
                            f"= {slope}"
                        )
                        if rel_str not in state.geometric_relations:
                            state.geometric_relations.append(rel_str)
                        
                        slopes_computed.append((name1, name2, slope))
                else:
                    # 无法计算（符号坐标），添加符号表达
                    symbolic_rel = (
                        f"Slope({name1}{name2}) = "
                        f"({coord2[1]} - {coord1[1]}) / ({coord2[0]} - {coord1[0]})"
                    )
                    if symbolic_rel not in state.geometric_relations:
                        state.geometric_relations.append(symbolic_rel)
                    state.parameters[slope_key] = (
                        f"({coord2[1]} - {coord1[1]}) / ({coord2[0]} - {coord1[0]})"
                    )
            
            # 如果只有两个点，也设置通用 k 参数
            if len(coord_list) == 2:
                name1, coord1 = coord_list[0]
                name2, coord2 = coord_list[1]
                slope_key_general = f"k_{name1}{name2}"
                if slope_key_general in state.parameters:
                    # 同时设置通用 k（如果还没有的话）
                    if 'k' not in state.parameters:
                        state.parameters['k'] = state.parameters[slope_key_general]
            
            # 记录已应用的模型
            state.applied_models.append(self.model_id)
            return True
        
        except Exception:
            return False
    
    def _calculate_slope(self, coord1, coord2):
        """
        计算两点间斜率 k = (y2-y1)/(x2-x1)
        
        Args:
            coord1: (x1, y1)
            coord2: (x2, y2)
        
        Returns:
            数值斜率, "undefined"（垂直线）, 或 None（无法计算）
        """
        try:
            x1, y1 = float(coord1[0]), float(coord1[1])
            x2, y2 = float(coord2[0]), float(coord2[1])
            
            dx = x2 - x1
            dy = y2 - y1
            
            if dx == 0:
                return "undefined"
            
            slope = dy / dx
            
            # 格式化输出
            if slope == int(slope):
                return int(slope)
            else:
                return round(slope, 4)
        except (ValueError, TypeError):
            # 坐标包含符号表达式，无法数值计算
            return None
