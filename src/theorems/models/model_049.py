"""
Model 49: Pythagorean_Theorem
勾股定理

公式: a² + b² = c²
用于: 直角三角形中，已知两边求第三边
"""

import math
from ..base_model import TheoremModel


class PythagoreanTheorem(TheoremModel):
    """
    勾股定理
    
    前置条件:
    - 存在垂直关系 (IsPerpendicular)
    - 或存在直角信息
    - 或存在三个点的坐标（可构成直角三角形）
    
    输出:
    - geometric_relations: a² + b² = c²
    - parameters: 如果已知具体边长，计算缺失边
    
    示例:
    已知直角三角形两直角边 a=3, b=4
    输出: c = 5
    """
    
    def __init__(self):
        super().__init__(
            model_id=49,
            name="Pythagorean_Theorem",
            chinese_name="勾股定理"
        )
    
    def can_apply(self, state) -> bool:
        """
        检查是否可应用
        
        条件:
        1. 存在垂直关系 (IsPerpendicular)
        2. 或存在直角信息（角度为90°）
        3. 或存在至少三个点的坐标
        """
        # 条件1: 检查是否有垂直关系
        for rel in state.geometric_relations:
            if 'IsPerpendicular' in rel or '垂直' in rel or '⊥' in rel:
                return True
        
        # 条件2: 检查是否有直角信息
        for rel in state.geometric_relations:
            if '直角' in rel or 'RightAngle' in rel or '90°' in rel or '90度' in rel:
                return True
        
        # 条件3: 检查是否有至少三个点的坐标
        if len(state.coordinates) >= 3:
            return True
        
        return False
    
    def apply(self, state) -> bool:
        """
        应用模型，添加勾股定理关系
        """
        try:
            # 添加通用勾股定理公式
            relation = "勾股定理: a² + b² = c²"
            if relation not in state.geometric_relations:
                state.geometric_relations.append(relation)
            
            # 尝试从参数中获取已知边长并计算缺失边
            self._compute_missing_side(state)
            
            # 如果有具体的点坐标，尝试验证或计算
            if len(state.coordinates) >= 3:
                self._compute_from_coordinates(state)
            
            # 记录已应用的模型
            state.applied_models.append(self.model_id)
            return True

        except Exception:
            return False
    
    def _compute_missing_side(self, state):
        """
        根据已知的直角三角形边长，计算缺失边
        
        检查参数中是否有 a, b, c（直角三角形边长）
        """
        # 获取可能的边长参数
        side_a = state.parameters.get('side_a') or state.parameters.get('leg_a')
        side_b = state.parameters.get('side_b') or state.parameters.get('leg_b')
        hypotenuse = state.parameters.get('hypotenuse') or state.parameters.get('side_c')
        
        try:
            if side_a and side_b and not hypotenuse:
                # 已知两直角边，求斜边
                a_val = float(side_a)
                b_val = float(side_b)
                c_val = math.sqrt(a_val ** 2 + b_val ** 2)
                
                c_str = str(int(c_val)) if c_val == int(c_val) else str(round(c_val, 4))
                state.parameters['hypotenuse'] = c_str
                state.geometric_relations.append(
                    f"勾股定理: c = √({side_a}² + {side_b}²) = {c_str}"
                )
            
            elif side_a and hypotenuse and not side_b:
                # 已知一直角边和斜边，求另一直角边
                a_val = float(side_a)
                c_val = float(hypotenuse)
                if c_val > a_val:
                    b_val = math.sqrt(c_val ** 2 - a_val ** 2)
                    b_str = str(int(b_val)) if b_val == int(b_val) else str(round(b_val, 4))
                    state.parameters['side_b'] = b_str
                    state.geometric_relations.append(
                        f"勾股定理: b = √({hypotenuse}² - {side_a}²) = {b_str}"
                    )
            
            elif side_b and hypotenuse and not side_a:
                # 已知一直角边和斜边，求另一直角边
                b_val = float(side_b)
                c_val = float(hypotenuse)
                if c_val > b_val:
                    a_val = math.sqrt(c_val ** 2 - b_val ** 2)
                    a_str = str(int(a_val)) if a_val == int(a_val) else str(round(a_val, 4))
                    state.parameters['side_a'] = a_str
                    state.geometric_relations.append(
                        f"勾股定理: a = √({hypotenuse}² - {side_b}²) = {a_str}"
                    )
        except (ValueError, TypeError):
            pass
    
    def _compute_from_coordinates(self, state):
        """
        从坐标计算距离，验证是否构成直角三角形
        """
        coord_list = list(state.coordinates.items())
        
        # 取前三个点检查
        if len(coord_list) < 3:
            return
        
        for i in range(min(len(coord_list), 3)):
            for j in range(i + 1, min(len(coord_list), 4)):
                for k in range(j + 1, min(len(coord_list), 5)):
                    name_a, coord_a = coord_list[i]
                    name_b, coord_b = coord_list[j]
                    name_c, coord_c = coord_list[k]
                    
                    self._check_right_triangle(state, name_a, coord_a,
                                               name_b, coord_b,
                                               name_c, coord_c)
    
    def _check_right_triangle(self, state, name_a, coord_a, name_b, coord_b, name_c, coord_c):
        """检查三个点是否构成直角三角形，如果是则添加关系"""
        try:
            x1, y1 = float(coord_a[0]), float(coord_a[1])
            x2, y2 = float(coord_b[0]), float(coord_b[1])
            x3, y3 = float(coord_c[0]), float(coord_c[1])
            
            # 计算三边长度的平方
            d_ab_sq = (x2 - x1) ** 2 + (y2 - y1) ** 2
            d_bc_sq = (x3 - x2) ** 2 + (y3 - y2) ** 2
            d_ac_sq = (x3 - x1) ** 2 + (y3 - y1) ** 2
            
            # 检查是否满足勾股定理（允许浮点误差）
            eps = 1e-9
            
            if abs(d_ab_sq + d_bc_sq - d_ac_sq) < eps:
                # B 是直角顶点
                hyp = round(math.sqrt(d_ac_sq), 4)
                state.geometric_relations.append(
                    f"直角三角形: ∠{name_b}=90°, |{name_a}{name_c}|={hyp}"
                )
            elif abs(d_ab_sq + d_ac_sq - d_bc_sq) < eps:
                # A 是直角顶点
                hyp = round(math.sqrt(d_bc_sq), 4)
                state.geometric_relations.append(
                    f"直角三角形: ∠{name_a}=90°, |{name_b}{name_c}|={hyp}"
                )
            elif abs(d_bc_sq + d_ac_sq - d_ab_sq) < eps:
                # C 是直角顶点
                hyp = round(math.sqrt(d_ab_sq), 4)
                state.geometric_relations.append(
                    f"直角三角形: ∠{name_c}=90°, |{name_a}{name_b}|={hyp}"
                )
        except (ValueError, TypeError):
            pass
