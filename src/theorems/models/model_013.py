"""
Model 13: Eccentricity_Formula
离心率公式

公式: e = c/a
已知 c 和 a，求离心率 e
"""

import re
from ..base_model import TheoremModel


class EccentricityFormula(TheoremModel):
    """
    离心率公式
    
    前置条件:
    - 参数中有 c 和 a
    
    输出:
    - parameters: e (离心率)
    - geometric_relations: e = c/a
    
    示例:
    输入: c=1, a=2
    输出: e=1/2
    """
    
    def __init__(self):
        super().__init__(
            model_id=13,
            name="Eccentricity_Formula",
            chinese_name="离心率公式"
        )
    
    def can_apply(self, state) -> bool:
        """
        检查是否可应用
        
        条件（放宽）:
        - 参数中有 c 和 a（直接计算）
        - 或有 a, b（可以计算c）
        - 或有 a^2, b^2（可以计算c）
        - 或存在圆锥曲线实体且讨论离心率
        """
        params = state.parameters
        
        # 条件1: 直接有 c 和 a
        if 'c' in params and 'a' in params:
            return True
        
        # 条件2: 有 a 和 b，可以计算 c（椭圆或双曲线）
        if 'a' in params and 'b' in params:
            # 检查曲线类型
            has_conic = any(
                entity_type.lower() in ['ellipse', 'hyperbola']
                for entity_type in state.entities.values()
            )
            if has_conic:
                return True
        
        # 条件3: 有 a^2 和 b^2
        if 'a^2' in params and 'b^2' in params:
            has_conic = any(
                entity_type.lower() in ['ellipse', 'hyperbola']
                for entity_type in state.entities.values()
            )
            if has_conic:
                return True
        
        # 条件4: 至少有 a，且讨论离心率
        if 'a' in params or 'a^2' in params:
            has_eccentricity_query = any(
                'Eccentricity' in rel or '离心率' in rel
                for rel in state.geometric_relations
            )
            if has_eccentricity_query:
                return True
        
        return False
    
    def apply(self, state) -> bool:
        """
        应用模型，计算离心率
        
        Returns:
            bool: 应用是否成功
        """
        try:
            params = state.parameters
            
            # 获取 c 和 a（可能需要计算）
            c_val = params.get('c')
            a_val = params.get('a')
            
            # 如果没有 c，尝试从 a, b 计算
            if not c_val and 'a' in params and 'b' in params:
                a_val = params['a']
                b_val = params['b']
                
                # 判断是椭圆还是双曲线
                is_ellipse = any(entity_type.lower() == 'ellipse' for entity_type in state.entities.values())
                is_hyperbola = any(entity_type.lower() == 'hyperbola' for entity_type in state.entities.values())
                
                if is_ellipse:
                    # 椭圆: c² = a² - b²
                    c_val = f"sqrt({a_val}^2 - {b_val}^2)"
                    params['c'] = c_val
                elif is_hyperbola:
                    # 双曲线: c² = a² + b²
                    c_val = f"sqrt({a_val}^2 + {b_val}^2)"
                    params['c'] = c_val
            
            # 如果没有 a，从 a^2 获取
            if not a_val and 'a^2' in params:
                a_squared = params['a^2']
                a_val = f"sqrt({a_squared})"
                params['a'] = a_val
            
            # 如果仍然没有 c 和 a，无法计算
            if not c_val or not a_val:
                state.applied_models.append(self.model_id)
                return False
            
            # 符号形式
            e_expr = f"{c_val}/{a_val}"
            
            # 尝试数值计算
            try:
                c_num = self._eval_expr(c_val)
                a_num = self._eval_expr(a_val)
                
                # 检查除数不为0
                if abs(a_num) < 1e-10:
                    return False
                
                e_num = c_num / a_num
                
                # 常见离心率值的简化
                if abs(e_num - 0.5) < 1e-6:
                    state.parameters['e'] = "1/2"
                elif abs(e_num - 2**0.5) < 1e-6:
                    state.parameters['e'] = "sqrt(2)"
                elif abs(e_num - 2**0.5 / 2) < 1e-6:
                    state.parameters['e'] = "sqrt(2)/2"
                elif abs(e_num - 3**0.5 / 2) < 1e-6:
                    state.parameters['e'] = "sqrt(3)/2"
                elif abs(e_num - 3**0.5 / 3) < 1e-6:
                    state.parameters['e'] = "sqrt(3)/3"
                elif e_num == int(e_num):
                    state.parameters['e'] = str(int(e_num))
                else:
                    state.parameters['e'] = self._simplify_fraction(c_num, a_num)
            except Exception:
                state.parameters['e'] = e_expr
            
            # 添加几何关系
            state.geometric_relations.append(f"e = {c_val}/{a_val}")
            
            # 记录已应用的模型
            state.applied_models.append(self.model_id)
            return True
            
        except Exception:
            return False
    
    def _eval_expr(self, expr: str) -> float:
        """
        计算表达式的数值
        
        支持：
        - 数字: "2", "3.5"
        - 平方根: "sqrt(5)"
        - 分数: "1/2"
        """
        expr = str(expr).strip()
        
        # 纯数字
        try:
            return float(expr)
        except:
            pass
        
        # sqrt形式
        match = re.match(r'sqrt\((\d+(?:\.\d+)?)\)', expr)
        if match:
            num = float(match.group(1))
            return num ** 0.5
        
        # 分数形式
        match = re.match(r'(\d+(?:\.\d+)?)/(\d+(?:\.\d+)?)', expr)
        if match:
            num = float(match.group(1))
            den = float(match.group(2))
            return num / den
        
        raise ValueError(f"Cannot evaluate: {expr}")
    
    def _simplify_fraction(self, numerator: float, denominator: float) -> str:
        """
        简化分数
        
        例如:
        - 1, 2 -> "1/2"
        - 2, 1 -> "2"
        - 1, 3 -> "1/3"
        """
        if denominator == 0:
            return "undefined"
        
        result = numerator / denominator
        
        # 如果是整数
        if result == int(result):
            return str(int(result))
        
        # 尝试表示为简单分数
        from fractions import Fraction
        try:
            frac = Fraction(numerator).limit_denominator(100) / Fraction(denominator).limit_denominator(100)
            if frac.denominator == 1:
                return str(frac.numerator)
            else:
                return f"{frac.numerator}/{frac.denominator}"
        except:
            return f"{numerator}/{denominator}"
