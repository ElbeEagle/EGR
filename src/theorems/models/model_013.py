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
        
        条件:
        - 参数中有 c 和 a
        """
        params = state.parameters
        return 'c' in params and 'a' in params
    
    def apply(self, state) -> None:
        """
        应用模型，计算离心率
        """
        c_val = state.parameters['c']
        a_val = state.parameters['a']
        
        # 符号形式
        e_expr = f"{c_val}/{a_val}"
        
        # 尝试数值计算
        try:
            c_num = self._eval_expr(c_val)
            a_num = self._eval_expr(a_val)
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
                # 尝试简化为分数
                state.parameters['e'] = self._simplify_fraction(c_num, a_num)
        except:
            state.parameters['e'] = e_expr
        
        # 添加几何关系
        state.geometric_relations.append(f"e = {c_val}/{a_val}")
        
        # 记录已应用的模型
        state.applied_models.append(self.model_id)
    
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
