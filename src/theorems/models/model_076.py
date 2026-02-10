"""
Model 76: Circle_Tangent_Condition
直线与圆相切条件

公式: d = r (圆心到直线的距离等于半径)
其中 d = |Ax₀ + By₀ + C| / √(A² + B²)
"""

import re
from ..base_model import TheoremModel


class CircleTangentCondition(TheoremModel):
    """
    直线与圆相切条件
    
    前置条件:
    - 存在 Circle 实体，或存在圆的方程
    - 或存在 IsTangent 等相切相关的几何关系
    
    输出:
    - 相切条件: d = r
    - 距离公式: d = |Ax₀ + By₀ + C| / √(A² + B²)
    - 如果圆的参数已知，添加具体关系
    
    示例:
    输入: 圆 x² + y² = 4, 直线 y = kx + m
    输出: d = |m| / √(1 + k²) = 2
    """
    
    def __init__(self):
        super().__init__(
            model_id=76,
            name="Circle_Tangent_Condition",
            chinese_name="直线与圆相切条件"
        )
    
    def can_apply(self, state) -> bool:
        """
        检查是否可应用
        
        条件 (满足任一):
        1. 存在 Circle 实体
        2. 方程中包含圆的方程形式
        3. 几何关系中存在相切 (IsTangent) 相关描述
        """
        # 条件1: 存在圆实体
        has_circle = any(
            entity_type.lower() == 'circle'
            for entity_type in state.entities.values()
        )
        if has_circle:
            return True
        
        # 条件2: 方程中包含圆的方程 (x^2 + y^2 形式，系数相同)
        for eq in state.equations:
            if 'x^2' in eq and 'y^2' in eq:
                # 简单检查: 如果 x^2 和 y^2 系数相同 (圆)
                if re.search(r'x\^2\s*\+\s*y\^2', eq):
                    return True
                # (x-h)^2 + (y-k)^2 = r^2 形式
                if re.search(r'\(x[+-].*\)\^2\s*\+\s*\(y[+-].*\)\^2', eq):
                    return True
        
        # 条件3: 几何关系中存在相切描述
        tangent_keywords = ['IsTangent', 'Tangent', '相切', '切线',
                            'tangent', 'TangentLine', '外切', '内切']
        has_tangent = any(
            kw in rel for rel in state.geometric_relations
            for kw in tangent_keywords
        )
        if has_tangent:
            return True
        
        return False
    
    def apply(self, state) -> bool:
        """
        应用模型，添加相切条件
        
        步骤:
        1. 添加通用相切条件 d = r
        2. 如果已知圆心和半径，添加具体距离公式
        3. 如果已知直线方程，代入距离公式
        """
        try:
            # 添加通用相切条件
            state.geometric_relations.append(
                "TangentCondition: d(center, line) = r"
            )
            state.geometric_relations.append(
                "DistanceFormula: d = |A*x0 + B*y0 + C| / sqrt(A^2 + B^2)"
            )
            
            # 获取圆的参数
            center_x = state.parameters.get('circle_center_x')
            center_y = state.parameters.get('circle_center_y')
            radius = state.parameters.get('circle_radius') or state.parameters.get('r')
            
            # 尝试从坐标中获取圆心
            if center_x is None and 'CircleCenter' in state.coordinates:
                center_x, center_y = state.coordinates['CircleCenter']
            
            # 如果圆的参数已知，添加具体关系
            if center_x is not None and center_y is not None and radius is not None:
                state.geometric_relations.append(
                    f"TangentCondition: d(({center_x}, {center_y}), line) = {radius}"
                )
                state.constraints.append(
                    f"d(({center_x}, {center_y}), line) = {radius}"
                )
            elif radius is not None:
                # 只知道半径
                state.constraints.append(f"d(center, line) = {radius}")
            else:
                # 检查是否可以从方程中提取
                self._extract_and_add_from_equation(state)
            
            # 如果是原点为圆心的圆 (x^2 + y^2 = r^2)
            for eq in state.equations:
                match = re.search(r'x\^2\s*\+\s*y\^2\s*=\s*(\S+)', eq)
                if match:
                    r_sq = match.group(1)
                    try:
                        r_sq_val = float(r_sq)
                        r_val = r_sq_val ** 0.5
                        if r_val == int(r_val):
                            r_val = int(r_val)
                        state.parameters.setdefault('r', str(r_val))
                        state.parameters.setdefault('r^2', str(r_sq))
                    except (ValueError, TypeError):
                        state.parameters.setdefault('r^2', r_sq)
                    
                    state.geometric_relations.append(
                        f"CircleAtOrigin: x^2 + y^2 = {r_sq}, "
                        f"TangentCondition: |C|/sqrt(A^2+B^2) = sqrt({r_sq})"
                    )
                    break
            
            # 记录已应用的模型
            state.applied_models.append(self.model_id)
            return True
        
        except Exception:
            return False
    
    def _extract_and_add_from_equation(self, state) -> None:
        """
        从圆方程中提取参数并添加相切条件
        """
        for eq in state.equations:
            # (x-h)^2 + (y-k)^2 = r^2 形式
            match = re.search(
                r'\(x([+-]\S+?)\)\^2\s*\+\s*\(y([+-]\S+?)\)\^2\s*=\s*(\S+)',
                eq
            )
            if match:
                h_part, k_part, r_sq = match.groups()
                # (x-h) 中 h_part 是 -h，所以圆心 x = -h_part
                try:
                    h = -float(h_part)
                    k = -float(k_part)
                    state.parameters.setdefault('circle_center_x', str(h))
                    state.parameters.setdefault('circle_center_y', str(k))
                except (ValueError, TypeError):
                    pass
                
                state.parameters.setdefault('r^2', r_sq)
                state.constraints.append(
                    f"d(center, line)^2 = {r_sq}"
                )
                break
