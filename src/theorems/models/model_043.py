"""
Model 43: Vieta_Theorem_Product
韦达定理 - 两根之积

对于一元二次方程 Ax² + Bx + C = 0:
x₁ · x₂ = C/A
"""

import re
from ..base_model import TheoremModel


class VietaTheoremProduct(TheoremModel):
    """
    韦达定理 - 两根之积
    
    前置条件:
    - 存在二次方程
    - 或已知需要计算两根之积
    
    输出:
    - parameters: x1_times_x2 (或 y1_times_y2)
    - geometric_relations: x₁ · x₂ = C/A
    
    示例:
    输入: 3*x^2 + 6*x - 9 = 0
    输出: x1 * x2 = -3
    """
    
    def __init__(self):
        super().__init__(
            model_id=43,
            name="Vieta_Theorem_Product",
            chinese_name="韦达定理-两根之积"
        )
    
    def can_apply(self, state) -> bool:
        """
        检查是否可应用
        
        条件:
        1. 存在二次方程
        2. 还没有计算过两根之积
        """
        # 检查是否已经有两根之积
        if 'x1_times_x2' in state.parameters or 'y1_times_y2' in state.parameters:
            return False
        
        # 检查是否有二次方程
        for eq in state.equations:
            if ('x^2' in eq or 'y^2' in eq) and '=' in eq:
                return True
        
        return False
    
    def apply(self, state) -> None:
        """
        应用模型，计算两根之积
        """
        # 查找二次方程并提取系数
        for eq in state.equations:
            # 尝试关于 x 的方程
            if 'x^2' in eq:
                A, C = self._extract_coefficients_x(eq)
                if A and C:
                    self._add_product_relation(state, A, C, 'x')
                    break
            
            # 尝试关于 y 的方程
            elif 'y^2' in eq:
                A, C = self._extract_coefficients_y(eq)
                if A and C:
                    self._add_product_relation(state, A, C, 'y')
                    break
        
        # 记录已应用的模型
        state.applied_models.append(self.model_id)
    
    def _extract_coefficients_x(self, eq: str):
        """提取关于x的二次项和常数项系数"""
        # 匹配 A*x^2 + ... + C = 0
        patterns = [
            # 完整形式: A*x^2 + B*x + C = 0
            r'([^=\+\-]+)\*?x\^2\s*[+\-]\s*[^=\+\-]+\*?x\s*([+\-])\s*([^=]+)\s*=\s*0',
            # 缺一次项: A*x^2 + C = 0
            r'([^=\+\-]+)\*?x\^2\s*([+\-])\s*([^=]+)\s*=\s*0',
            # 简化形式: x^2 + ... + C = 0
            r'x\^2\s*[+\-]\s*[^=\+\-]+\*?x\s*([+\-])\s*([^=]+)\s*=\s*0',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, eq)
            if match:
                groups = match.groups()
                if len(groups) == 3:
                    A = groups[0].strip().replace('*', '')
                    sign = groups[1]
                    C = groups[2].strip()
                    if sign == '-':
                        C = '-' + C
                    return A, C
                elif len(groups) == 2:
                    # x^2 形式或缺一次项
                    if 'x^2' in groups[0]:
                        A = '1'
                    else:
                        A = groups[0].strip().replace('*', '')
                    sign = groups[0] if 'x^2' in groups[0] else groups[1]
                    C = groups[1] if 'x^2' in groups[0] else groups[2] if len(groups) > 2 else groups[1]
                    C = C.strip()
                    if '-' in sign:
                        C = '-' + C
                    return A, C
        
        return None, None
    
    def _extract_coefficients_y(self, eq: str):
        """提取关于y的系数"""
        eq_y = eq.replace('y', 'x')
        return self._extract_coefficients_x(eq_y)
    
    def _add_product_relation(self, state, A, C, var='x'):
        """添加两根之积关系"""
        try:
            # 尝试数值计算
            a_num = float(A) if A != '1' else 1.0
            c_num = float(C)
            
            prod_val = c_num / a_num
            
            if prod_val == int(prod_val):
                prod_str = str(int(prod_val))
            else:
                prod_str = str(prod_val)
            
            state.parameters[f'{var}1_times_{var}2'] = prod_str
            state.geometric_relations.append(f"{var}₁ · {var}₂ = {prod_str}")
            
        except:
            # 符号形式
            prod_expr = f"({C})/({A})"
            state.parameters[f'{var}1_times_{var}2'] = prod_expr
            state.geometric_relations.append(f"{var}₁ · {var}₂ = {prod_expr}")
