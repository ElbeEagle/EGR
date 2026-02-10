"""
Model 66: Discriminant_Tangent_Condition
判别式相切条件

公式: Δ = b² - 4ac = 0 (相切时判别式为零)
用于: 直线与圆锥曲线相切的判定
"""

import re
from ..base_model import TheoremModel


class DiscriminantTangentCondition(TheoremModel):
    """
    判别式相切条件
    
    前置条件:
    - 存在判别式相关信息 (Delta, Δ)
    - 或几何关系中包含相切条件
    - 或存在联立后的代换方程
    
    输出:
    - 相切条件: Δ = b² - 4ac = 0
    - 添加到 geometric_relations 和 constraints
    
    示例:
    输入: 联立方程得 (1+k²)x² + 2kbx + b²-a² = 0，相切
    输出: Δ = 4k²b² - 4(1+k²)(b²-a²) = 0
    """
    
    def __init__(self):
        super().__init__(
            model_id=66,
            name="Discriminant_Tangent_Condition",
            chinese_name="判别式相切条件"
        )
    
    def can_apply(self, state) -> bool:
        """
        检查是否可应用
        
        条件 (满足任一):
        1. 存在判别式相关参数 (Delta, Δ)
        2. 几何关系中包含相切条件 (Tangent)
        3. 存在联立后的代换方程 (含 x² 或 y² 的一元二次方程)
        """
        # 条件1: 判别式相关参数
        has_discriminant = ('Delta' in state.parameters
                           or 'delta' in state.parameters
                           or 'Δ' in state.parameters)
        if has_discriminant:
            return True
        
        # 条件2: 几何关系中包含相切条件
        tangent_keywords = ['Tangent', 'IsTangent', '相切', '切线',
                            'tangent', 'TangentLine']
        has_tangent = any(
            kw in rel for rel in state.geometric_relations
            for kw in tangent_keywords
        )
        if has_tangent:
            return True
        
        # 条件3: 存在联立后的方程 (一元二次)
        # 检查是否有代换后产生的二次方程
        has_substitution_eq = False
        for eq in state.equations:
            # 检查是否包含类似 Ax^2 + Bx + C = 0 的形式
            if re.search(r'x\^2.*x.*=\s*0', eq) or re.search(r'y\^2.*y.*=\s*0', eq):
                has_substitution_eq = True
                break
            # 检查含参数的二次方程
            if re.search(r'\w+\*?x\^2', eq) or re.search(r'\w+\*?y\^2', eq):
                # 需要同时有相切相关的信息
                if has_tangent:
                    has_substitution_eq = True
                    break
        
        # 联立方程 + 相切 = 可应用
        if has_substitution_eq:
            return True
        
        # 也检查是否同时有曲线和直线（联立后可能需要判别式）
        has_curve = any(
            entity_type.lower() in ('ellipse', 'hyperbola', 'parabola', 'circle')
            for entity_type in state.entities.values()
        )
        has_line = any(
            entity_type.lower() == 'line'
            for entity_type in state.entities.values()
        )
        if has_curve and has_line and has_tangent:
            return True
        
        return False
    
    def apply(self, state) -> bool:
        """
        应用判别式相切条件
        
        步骤:
        1. 添加相切条件 Δ = 0
        2. 如果能提取二次方程系数，计算具体判别式
        3. 添加到 geometric_relations 和 constraints
        """
        try:
            # 添加核心相切条件
            state.geometric_relations.append(
                "TangentCondition: Δ = b² - 4ac = 0"
            )
            state.constraints.append("Delta = 0")
            
            # 设置判别式参数
            state.parameters.setdefault('Delta', '0')
            
            # 尝试从方程中提取二次方程系数
            extracted = False
            for eq in state.equations:
                coeffs = self._extract_quadratic_coefficients(eq)
                if coeffs:
                    coeff_a, coeff_b, coeff_c = coeffs
                    discriminant_expr = (
                        f"({coeff_b})^2 - 4*({coeff_a})*({coeff_c})"
                    )
                    state.geometric_relations.append(
                        f"Δ = {discriminant_expr} = 0"
                    )
                    state.equations.append(
                        f"{discriminant_expr} = 0"
                    )
                    state.parameters['Delta_expr'] = discriminant_expr
                    extracted = True
                    break
            
            # 如果没有提取到具体系数，添加通用形式
            if not extracted:
                state.geometric_relations.append(
                    "After substitution: Ax² + Bx + C = 0, "
                    "tangent condition: B² - 4AC = 0"
                )
            
            # 添加相切的几何意义
            state.geometric_relations.append(
                "TangentMeaning: Line touches curve at exactly one point"
            )
            
            # 记录已应用的模型
            state.applied_models.append(self.model_id)
            return True
        
        except Exception:
            return False
    
    def _extract_quadratic_coefficients(self, eq: str):
        """
        从方程中提取二次方程 Ax² + Bx + C = 0 的系数
        
        Returns:
            (A, B, C) 系数元组，失败返回 None
        """
        try:
            # 模式: a*x^2 + b*x + c = 0
            # 匹配 (coeff)x^2 + (coeff)x + (const) = 0
            
            # 标准形式: 数字系数
            match = re.search(
                r'([+-]?\s*\d*\.?\d*)\s*\*?\s*x\^2\s*'
                r'([+-]\s*\d*\.?\d*)\s*\*?\s*x\s*'
                r'([+-]\s*\d*\.?\d+)\s*=\s*0',
                eq
            )
            if match:
                a_str = match.group(1).replace(' ', '') or '1'
                b_str = match.group(2).replace(' ', '') or '0'
                c_str = match.group(3).replace(' ', '') or '0'
                return a_str, b_str, c_str
            
            # 含参数的形式，例如: (1+k^2)*x^2 + 2kb*x + (b^2-a^2) = 0
            match = re.search(
                r'\(([^)]+)\)\s*\*?\s*x\^2\s*[+-]\s*'
                r'([^*]+)\s*\*?\s*x\s*[+-]\s*'
                r'\(([^)]+)\)\s*=\s*0',
                eq
            )
            if match:
                return match.group(1), match.group(2), match.group(3)
            
            return None
        except Exception:
            return None
