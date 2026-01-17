"""
Model 42: Vieta_Theorem_Sum
韦达定理 - 两根之和

对于一元二次方程 Ax² + Bx + C = 0:
x₁ + x₂ = -B/A
"""

import re
from ..base_model import TheoremModel


class VietaTheoremSum(TheoremModel):
    """
    韦达定理 - 两根之和
    
    前置条件:
    - 存在二次方程
    - 或已知需要计算两根之和
    
    输出:
    - parameters: x1_plus_x2 (或 y1_plus_y2)
    - geometric_relations: x₁ + x₂ = -B/A
    
    示例:
    输入: 3*x^2 + 6*x - 1 = 0
    输出: x1 + x2 = -2
    """
    
    def __init__(self):
        super().__init__(
            model_id=42,
            name="Vieta_Theorem_Sum",
            chinese_name="韦达定理-两根之和"
        )
    
    def can_apply(self, state) -> bool:
        """
        检查是否可应用
        
        条件:
        1. 存在二次方程
        2. 还没有计算过两根之和
        """
        # 检查是否已经有两根之和
        if 'x1_plus_x2' in state.parameters or 'y1_plus_y2' in state.parameters:
            return False
        
        # 检查是否有二次方程
        for eq in state.equations:
            if ('x^2' in eq or 'y^2' in eq) and '=' in eq:
                return True
        
        return False
    
    def apply(self, state) -> None:
        """
        应用模型，计算两根之和
        """
        # 查找二次方程并提取系数
        for eq in state.equations:
            # 尝试关于 x 的方程
            if 'x^2' in eq:
                A, B = self._extract_coefficients_x(eq)
                if A and B:
                    self._add_sum_relation(state, A, B, 'x')
                    break
            
            # 尝试关于 y 的方程
            elif 'y^2' in eq:
                A, B = self._extract_coefficients_y(eq)
                if A and B:
                    self._add_sum_relation(state, A, B, 'y')
                    break
        
        # 记录已应用的模型
        state.applied_models.append(self.model_id)
    
    def _extract_coefficients_x(self, eq: str):
        """提取关于x的二次项和一次项系数"""
        # 匹配 A*x^2 + B*x
        patterns = [
            r'([^=\+\-]+)\*?x\^2\s*([+\-])\s*([^=\+\-]+)\*?x',
            r'x\^2\s*([+\-])\s*([^=\+\-]+)\*?x',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, eq)
            if match:
                groups = match.groups()
                if len(groups) == 3:
                    A = groups[0].strip().replace('*', '')
                    sign = groups[1]
                    B = groups[2].strip().replace('*', '')
                    if sign == '-':
                        B = '-' + B
                    return A, B
                elif len(groups) == 2:
                    A = '1'
                    sign = groups[0]
                    B = groups[1].strip().replace('*', '')
                    if sign == '-':
                        B = '-' + B
                    return A, B
        
        return None, None
    
    def _extract_coefficients_y(self, eq: str):
        """提取关于y的系数"""
        # 逻辑与x相同，只是变量不同
        eq_y = eq.replace('y', 'x')
        return self._extract_coefficients_x(eq_y)
    
    def _add_sum_relation(self, state, A, B, var='x'):
        """添加两根之和关系"""
        try:
            # 尝试数值计算
            a_num = float(A) if A != '1' else 1.0
            b_num = float(B)
            
            sum_val = -b_num / a_num
            
            if sum_val == int(sum_val):
                sum_str = str(int(sum_val))
            else:
                sum_str = str(sum_val)
            
            state.parameters[f'{var}1_plus_{var}2'] = sum_str
            state.geometric_relations.append(f"{var}₁ + {var}₂ = {sum_str}")
            
        except:
            # 符号形式
            sum_expr = f"-({B})/({A})"
            state.parameters[f'{var}1_plus_{var}2'] = sum_expr
            state.geometric_relations.append(f"{var}₁ + {var}₂ = {sum_expr}")
