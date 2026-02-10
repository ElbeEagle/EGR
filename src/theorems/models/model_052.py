"""
Model 52: Point_To_Line_Distance
点到直线距离

公式: d = |Ax₀ + By₀ + C| / √(A² + B²)
用于: 已知点坐标和直线方程，计算点到直线的距离
"""

import re
import math
from ..base_model import TheoremModel


class PointToLineDistance(TheoremModel):
    """
    点到直线距离
    
    前置条件:
    - 存在至少一个点的坐标
    - 存在直线方程（equations 或 geometric_relations）
    
    输出:
    - geometric_relations: 点到直线距离公式
    - parameters: 具体距离值（如果可以计算）
    
    示例:
    输入: P(1, 2), 直线: 3x + 4y - 5 = 0
    输出: d = |3×1 + 4×2 - 5| / √(9+16) = 6/5
    """
    
    def __init__(self):
        super().__init__(
            model_id=52,
            name="Point_To_Line_Distance",
            chinese_name="点到直线距离"
        )
    
    def can_apply(self, state) -> bool:
        """
        检查是否可应用
        
        条件:
        1. 至少有一个点的坐标
        2. 存在直线方程（equations 或 geometric_relations 中）
        """
        # 条件1: 至少有一个点的坐标
        has_point = len(state.coordinates) >= 1
        
        if not has_point:
            return False
        
        # 条件2a: equations 中有直线方程
        for eq in state.equations:
            if self._is_line_equation(eq):
                return True
        
        # 条件2b: geometric_relations 中有直线方程或直线信息
        for rel in state.geometric_relations:
            if any(kw in rel for kw in ['Line', 'line', '直线', '距离']):
                return True
            if self._is_line_equation(rel):
                return True
        
        # 条件2c: entities 中有直线
        for entity_type in state.entities.values():
            if 'Line' in str(entity_type) or '直线' in str(entity_type):
                return True
        
        return False
    
    def apply(self, state) -> bool:
        """
        应用模型，计算点到直线距离
        """
        try:
            # 添加通用距离公式
            general_formula = "点到直线距离公式: d = |Ax₀ + By₀ + C| / √(A² + B²)"
            if general_formula not in state.geometric_relations:
                state.geometric_relations.append(general_formula)
            
            # 尝试从方程中解析直线 Ax + By + C = 0
            lines = []
            for eq in state.equations:
                parsed = self._parse_line_equation(eq)
                if parsed is not None:
                    lines.append((eq, parsed))
            
            for rel in state.geometric_relations:
                parsed = self._parse_line_equation(rel)
                if parsed is not None:
                    lines.append((rel, parsed))
            
            # 对每条直线和每个点，计算距离
            coord_list = list(state.coordinates.items())
            
            for line_str, (A, B, C) in lines:
                for point_name, point_coord in coord_list:
                    distance = self._calculate_distance(
                        A, B, C, point_coord[0], point_coord[1]
                    )
                    
                    if distance is not None:
                        dist_key = f"dist_{point_name}_to_line"
                        state.parameters[dist_key] = str(distance)
                        
                        rel_str = (
                            f"Distance({point_name}, {line_str}) = "
                            f"|{A}*{point_coord[0]} + {B}*{point_coord[1]} + {C}| "
                            f"/ √({A}² + {B}²) = {distance}"
                        )
                        if rel_str not in state.geometric_relations:
                            state.geometric_relations.append(rel_str)
            
            # 如果没有解析出具体直线，仍然添加符号公式
            if not lines and len(coord_list) >= 1:
                for point_name, point_coord in coord_list:
                    symbolic_rel = (
                        f"Distance({point_name}, Ax+By+C=0) = "
                        f"|A*{point_coord[0]} + B*{point_coord[1]} + C| / √(A² + B²)"
                    )
                    if symbolic_rel not in state.geometric_relations:
                        state.geometric_relations.append(symbolic_rel)
            
            # 记录已应用的模型
            state.applied_models.append(self.model_id)
            return True
        
        except Exception:
            return False
    
    def _is_line_equation(self, expr):
        """
        判断是否为直线方程
        
        支持的形式:
        - Ax + By + C = 0
        - y = kx + b
        - x = c
        """
        expr_lower = expr.lower().strip()
        # 匹配 y = kx + b 或 ax + by + c = 0 等形式
        if re.search(r'[xy]\s*=', expr_lower):
            return True
        if re.search(r'\d*\s*x\s*[+\-]\s*\d*\s*y', expr_lower):
            return True
        if 'line' in expr_lower or '直线' in expr_lower:
            return True
        return False
    
    def _parse_line_equation(self, expr):
        """
        解析直线方程为 Ax + By + C = 0 的系数
        
        Returns:
            (A, B, C) 或 None
        """
        try:
            expr = expr.strip()
            
            # 形式1: Ax + By + C = 0
            match = re.search(
                r'([+-]?\s*\d*\.?\d*)\s*\*?\s*x\s*([+-]\s*\d*\.?\d*)\s*\*?\s*y\s*([+-]\s*\d*\.?\d*)\s*=\s*0',
                expr
            )
            if match:
                A = self._parse_coeff(match.group(1))
                B = self._parse_coeff(match.group(2))
                C = self._parse_coeff(match.group(3))
                if A is not None and B is not None and C is not None:
                    return (A, B, C)
            
            # 形式2: y = kx + b => kx - y + b = 0
            match = re.search(
                r'y\s*=\s*([+-]?\s*\d*\.?\d*)\s*\*?\s*x\s*([+-]\s*\d*\.?\d*)',
                expr
            )
            if match:
                k = self._parse_coeff(match.group(1))
                b = self._parse_coeff(match.group(2))
                if k is not None and b is not None:
                    return (k, -1, b)
            
            # 形式3: y = kx => kx - y = 0
            match = re.search(r'y\s*=\s*([+-]?\s*\d*\.?\d*)\s*\*?\s*x\s*$', expr)
            if match:
                k = self._parse_coeff(match.group(1))
                if k is not None:
                    return (k, -1, 0)
            
            # 形式4: x = c => x - c = 0
            match = re.search(r'^x\s*=\s*([+-]?\s*\d+\.?\d*)\s*$', expr)
            if match:
                c = float(match.group(1))
                return (1, 0, -c)
            
            return None
        except Exception:
            return None
    
    def _parse_coeff(self, coeff_str):
        """解析系数字符串"""
        try:
            s = coeff_str.replace(' ', '')
            if s == '' or s == '+':
                return 1.0
            elif s == '-':
                return -1.0
            else:
                return float(s)
        except (ValueError, TypeError):
            return None
    
    def _calculate_distance(self, A, B, C, x0, y0):
        """
        计算点到直线距离 d = |Ax0+By0+C| / sqrt(A^2+B^2)
        
        Returns:
            distance 或 None
        """
        try:
            A = float(A)
            B = float(B)
            C = float(C)
            x0 = float(x0)
            y0 = float(y0)
            
            denom = math.sqrt(A ** 2 + B ** 2)
            if denom == 0:
                return None
            
            distance = abs(A * x0 + B * y0 + C) / denom
            
            # 格式化输出
            if distance == int(distance):
                return int(distance)
            else:
                return round(distance, 4)
        except (ValueError, TypeError):
            return None
