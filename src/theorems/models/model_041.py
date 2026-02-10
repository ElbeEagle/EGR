"""
Model 41: Vieta_Theorem
韦达定理（根与系数关系）

对于一元二次方程 Ax² + Bx + C = 0:
- x₁ + x₂ = -B/A
- x₁ · x₂ = C/A
"""

import re
from ..base_model import TheoremModel


class VietaTheorem(TheoremModel):
    """
    韦达定理（根与系数关系）
    
    前置条件:
    - 存在二次方程（关于x或y）
    
    输出:
    - parameters: x1_plus_x2, x1_times_x2 (或 y1_plus_y2, y1_times_y2)
    - geometric_relations: 韦达定理关系式
    
    示例:
    输入: 3*x^2 + 2*x - 1 = 0
    输出: x1 + x2 = -2/3, x1 * x2 = -1/3
    """
    
    def __init__(self):
        super().__init__(
            model_id=41,
            name="Vieta_Theorem",
            chinese_name="韦达定理"
        )
    
    def can_apply(self, state) -> bool:
        """
        检查是否可应用
        
        条件:
        1. 存在二次方程（Ax² + Bx + C = 0 或 Ay² + By + C = 0）
        """
        # 检查方程中是否有二次项
        for eq in state.equations:
            # 检查是否包含 x^2 或 y^2
            if 'x^2' in eq or 'y^2' in eq:
                # 检查是否是等式
                if '=' in eq:
                    return True
        
        # 也可以从几何关系中查找
        for rel in state.geometric_relations:
            if '韦达' in rel or 'Vieta' in rel or '根与系数' in rel:
                return False  # 已经应用过
            if ('x1' in rel and 'x2' in rel) or ('y1' in rel and 'y2' in rel):
                # 可能已经有交点，可以应用韦达定理
                if 'x^2' in ' '.join(state.equations) or 'y^2' in ' '.join(state.equations):
                    return True
        
        return False
    
    def apply(self, state) -> bool:
        """
        应用模型，提取韦达定理关系
        """
        try:
            # 查找二次方程
            for eq in state.equations:
                # 尝试匹配关于 x 的二次方程
                result = self._extract_vieta_x(eq, state)
                if result:
                    continue
            
                # 尝试匹配关于 y 的二次方程
                result = self._extract_vieta_y(eq, state)
                if result:
                    continue
        
            # 如果没有找到具体方程，添加通用韦达定理关系
            if not any('韦达' in rel for rel in state.geometric_relations):
                state.geometric_relations.append("韦达定理: x₁ + x₂ = -B/A, x₁·x₂ = C/A")
        
            # 记录已应用的模型
            state.applied_models.append(self.model_id)
    
            return True

        except Exception:
            return False
    def _extract_vieta_x(self, eq: str, state) -> bool:
        """提取关于x的韦达定理"""
        # 尝试多种模式匹配
        patterns = [
            # 标准形式: A*x^2 + B*x + C = 0
            r'([^=\+\-]+)\*?x\^2\s*([+\-])\s*([^=\+\-]+)\*?x\s*([+\-])\s*([^=]+)\s*=\s*0',
            # 简化形式: x^2 + B*x + C = 0
            r'x\^2\s*([+\-])\s*([^=\+\-]+)\*?x\s*([+\-])\s*([^=]+)\s*=\s*0',
            # 一般形式: A*x^2 + B*x = -C
            r'([^=\+\-]+)\*?x\^2\s*([+\-])\s*([^=\+\-]+)\*?x\s*=\s*([^=]+)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, eq)
            if match:
                groups = match.groups()
                A, B, C = self._parse_coefficients_x(groups)
                if A and B and C:
                    self._add_vieta_relations(state, A, B, C, 'x')
                    return True
        
        return False
    
    def _extract_vieta_y(self, eq: str, state) -> bool:
        """提取关于y的韦达定理"""
        patterns = [
            r'([^=\+\-]+)\*?y\^2\s*([+\-])\s*([^=\+\-]+)\*?y\s*([+\-])\s*([^=]+)\s*=\s*0',
            r'y\^2\s*([+\-])\s*([^=\+\-]+)\*?y\s*([+\-])\s*([^=]+)\s*=\s*0',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, eq)
            if match:
                groups = match.groups()
                A, B, C = self._parse_coefficients_y(groups)
                if A and B and C:
                    self._add_vieta_relations(state, A, B, C, 'y')
                    return True
        
        return False
    
    def _parse_coefficients_x(self, groups):
        """解析x方程的系数"""
        try:
            if len(groups) == 5:
                # A*x^2 + B*x + C = 0
                A = groups[0].strip().replace('*', '')
                sign_b = groups[1]
                B = groups[2].strip().replace('*', '')
                sign_c = groups[3]
                C = groups[4].strip()
                
                if sign_b == '-':
                    B = '-' + B
                if sign_c == '-':
                    C = '-' + C
                
                return A, B, C
            elif len(groups) == 4:
                # x^2 + B*x + C = 0 或 A*x^2 + B*x = C
                if 'x^2' in groups[0]:
                    A = '1'
                    sign_b = groups[0]
                    B = groups[1].strip().replace('*', '')
                    sign_c = groups[2]
                    C = groups[3].strip()
                else:
                    A = groups[0].strip().replace('*', '')
                    sign_b = groups[1]
                    B = groups[2].strip().replace('*', '')
                    C = '-(' + groups[3].strip() + ')'
                
                if sign_b == '-':
                    B = '-' + B
                if len(groups) > 2 and sign_c == '-':
                    C = '-' + C
                
                return A, B, C
        except:
            pass
        
        return None, None, None
    
    def _parse_coefficients_y(self, groups):
        """解析y方程的系数"""
        return self._parse_coefficients_x(groups)  # 逻辑相同
    
    def _add_vieta_relations(self, state, A, B, C, var='x'):
        """添加韦达定理关系"""
        # 计算 -B/A 和 C/A
        try:
            # 尝试数值计算
            a_num = float(A) if A != '1' else 1.0
            b_num = float(B)
            c_num = float(C)
            
            sum_val = -b_num / a_num
            prod_val = c_num / a_num
            
            # 格式化输出
            if sum_val == int(sum_val):
                sum_str = str(int(sum_val))
            else:
                sum_str = str(sum_val)
            
            if prod_val == int(prod_val):
                prod_str = str(int(prod_val))
            else:
                prod_str = str(prod_val)
            
            state.parameters[f'{var}1_plus_{var}2'] = sum_str
            state.parameters[f'{var}1_times_{var}2'] = prod_str
            
            state.geometric_relations.append(f"韦达定理: {var}₁ + {var}₂ = {sum_str}")
            state.geometric_relations.append(f"韦达定理: {var}₁ · {var}₂ = {prod_str}")
            
        except:
            # 符号形式
            sum_expr = f"-({B})/({A})"
            prod_expr = f"({C})/({A})"
            
            state.parameters[f'{var}1_plus_{var}2'] = sum_expr
            state.parameters[f'{var}1_times_{var}2'] = prod_expr
            
            state.geometric_relations.append(f"韦达定理: {var}₁ + {var}₂ = {sum_expr}")
            state.geometric_relations.append(f"韦达定理: {var}₁ · {var}₂ = {prod_expr}")
