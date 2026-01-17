"""
Model 75: Circle_Standard_Equation
圆的标准方程

公式: (x-h)² + (y-k)² = r²
其中 (h, k) 是圆心，r 是半径
"""

import re
from ..base_model import TheoremModel


class CircleStandardEquation(TheoremModel):
    """
    圆的标准方程
    
    前置条件:
    - 存在 Circle 实体
    - 或方程包含 x² + y² 形式
    
    输出:
    - parameters: h, k, r (圆心和半径)
    - geometric_relations: 圆的标准方程
    
    示例:
    输入: (x-2)² + (y-3)² = 9
    输出: 圆心 (2, 3), 半径 r = 3
    """
    
    def __init__(self):
        super().__init__(
            model_id=75,
            name="Circle_Standard_Equation",
            chinese_name="圆的标准方程"
        )
    
    def can_apply(self, state) -> bool:
        """
        检查是否可应用
        
        条件:
        1. 存在 Circle 实体
        2. 方程包含 x² + y² 形式
        """
        # 条件1: 检查是否有圆实体
        has_circle = any(
            entity_type.lower() == 'circle'
            for entity_type in state.entities.values()
        )
        if has_circle:
            return True
        
        # 条件2: 检查方程
        for eq in state.equations:
            # 检查是否有 x^2 和 y^2 且系数相同（圆）
            if 'x^2' in eq and 'y^2' in eq:
                # (x-h)^2 + (y-k)^2 = r^2 形式
                if re.search(r'\(x[+-]\d+\)\^2\s*\+\s*\(y[+-]\d+\)\^2\s*=', eq):
                    return True
                # x^2 + y^2 = r^2 形式（圆心在原点）
                if re.search(r'x\^2\s*\+\s*y\^2\s*=\s*\d+', eq):
                    return True
        
        return False
    
    def apply(self, state) -> None:
        """
        应用模型，提取圆的参数
        """
        for eq in state.equations:
            if 'x^2' in eq and 'y^2' in eq:
                # 尝试提取圆心和半径
                result = self._extract_circle_params(eq)
                
                if result:
                    h, k, r = result
                    
                    # 添加参数
                    state.parameters['circle_center_x'] = str(h)
                    state.parameters['circle_center_y'] = str(k)
                    state.parameters['circle_radius'] = str(r)
                    
                    # 添加坐标
                    state.coordinates['CircleCenter'] = (str(h), str(k))
                    
                    # 添加几何关系
                    state.geometric_relations.append(
                        f"圆: 圆心 ({h}, {k}), 半径 r = {r}"
                    )
                    
                    break
        
        # 如果没有找到具体方程，添加通用公式
        if 'circle_center_x' not in state.parameters:
            state.geometric_relations.append(
                "圆的标准方程: (x-h)² + (y-k)² = r²"
            )
        
        # 记录已应用的模型
        state.applied_models.append(self.model_id)
    
    def _extract_circle_params(self, eq: str):
        """
        从方程中提取圆心和半径
        
        Returns:
            (h, k, r): 圆心坐标和半径，失败返回 None
        """
        # 模式1: (x-h)^2 + (y-k)^2 = r^2
        pattern1 = r'\(x([+-])(\d+)\)\^2\s*\+\s*\(y([+-])(\d+)\)\^2\s*=\s*(\d+)'
        match = re.search(pattern1, eq)
        if match:
            x_sign, x_val, y_sign, y_val, r_sq = match.groups()
            
            # 注意：(x-2) 表示 h=2，(x+2) 表示 h=-2
            h = int(x_val) if x_sign == '-' else -int(x_val)
            k = int(y_val) if y_sign == '-' else -int(y_val)
            r = int(r_sq) ** 0.5
            
            if r == int(r):
                r = int(r)
            
            return h, k, r
        
        # 模式2: x^2 + y^2 = r^2 (圆心在原点)
        pattern2 = r'x\^2\s*\+\s*y\^2\s*=\s*(\d+)'
        match = re.search(pattern2, eq)
        if match:
            r_sq = int(match.group(1))
            r = r_sq ** 0.5
            
            if r == int(r):
                r = int(r)
            
            return 0, 0, r
        
        # 模式3: (x-h)^2 + (y-k)^2 = r^2，其中 h, k, r 可能是变量
        pattern3 = r'\(x-([a-zA-Z\d]+)\)\^2\s*\+\s*\(y-([a-zA-Z\d]+)\)\^2\s*=\s*([a-zA-Z\d]+)'
        match = re.search(pattern3, eq)
        if match:
            h, k, r = match.groups()
            return h, k, r
        
        return None
