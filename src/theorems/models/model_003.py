"""
Model 3: Ellipse_Equation_Standard_X
椭圆标准方程（焦点在x轴）参数提取

公式: x^2/a^2 + y^2/b^2 = 1 (a > b)
提取: a, b, a^2, b^2
"""

import re
from ..base_model import TheoremModel


class EllipseEquationStandardX(TheoremModel):
    """
    椭圆标准方程（焦点在x轴）参数提取
    
    前置条件:
    - 实体包含 Ellipse 类型
    - 方程形式: x^2/A + y^2/B = 1，且 A > B
    
    输出:
    - parameters: a^2, b^2, a, b
    - geometric_relations: a^2=A, b^2=B, 焦点在x轴
    
    示例:
    输入: Expression(G) = (x^2/5 + y^2/4 = 1)
    输出: a^2=5, b^2=4, a=sqrt(5), b=2
    """
    
    def __init__(self):
        super().__init__(
            model_id=3,
            name="Ellipse_Equation_Standard_X",
            chinese_name="椭圆标准方程(焦点在x轴)"
        )
    
    def can_apply(self, state) -> bool:
        """
        检查是否可应用
        
        条件:
        1. 存在 Ellipse 实体
        2. 存在形如 x^2/A + y^2/B = 1 的方程
        3. A > B (焦点在x轴)
        """
        # 条件1: 检查是否有椭圆实体
        has_ellipse = any(
            entity_type.lower() == 'ellipse'
            for entity_type in state.entities.values()
        )
        if not has_ellipse:
            return False
        
        # 条件2和3: 检查是否有标准方程且A>B
        for eq in state.equations:
            if self._is_standard_ellipse_x(eq):
                return True
        
        return False
    
    def apply(self, state) -> None:
        """
        应用模型，提取参数
        """
        # 查找标准方程
        for eq in state.equations:
            if not self._is_standard_ellipse_x(eq):
                continue
            
            # 提取参数
            a_squared, b_squared = self._extract_parameters(eq)
            
            if a_squared is None or b_squared is None:
                continue
            
            # 添加参数
            state.parameters['a^2'] = a_squared
            state.parameters['b^2'] = b_squared
            
            # 尝试计算 a 和 b
            a_val = self._simplify_sqrt(a_squared)
            b_val = self._simplify_sqrt(b_squared)
            
            state.parameters['a'] = a_val
            state.parameters['b'] = b_val
            
            # 添加几何关系
            state.geometric_relations.append(f"a^2 = {a_squared}")
            state.geometric_relations.append(f"b^2 = {b_squared}")
            state.geometric_relations.append("焦点在x轴")
            
            # 记录已应用的模型
            state.applied_models.append(self.model_id)
            
            # 只处理第一个匹配的方程
            break
    
    def _is_standard_ellipse_x(self, equation: str) -> bool:
        """
        判断是否为标准椭圆方程（焦点在x轴）
        
        匹配模式：
        - x^2/A + y^2/B = 1 (A > B)
        - y^2/B + x^2/A = 1 (A > B)
        """
        eq = equation.replace(' ', '')
        
        # 模式1: x^2/A + y^2/B = 1
        pattern1 = r'x\^2/([^\s\+\)]+).*?\+.*?y\^2/([^\s=\)]+).*?=.*?1'
        match1 = re.search(pattern1, eq)
        if match1:
            a_sq_str = self._clean_parameter(match1.group(1))
            b_sq_str = self._clean_parameter(match1.group(2))
            # 检查 A > B
            if self._compare_values(a_sq_str, b_sq_str) > 0:
                return True
        
        # 模式2: y^2/B + x^2/A = 1
        pattern2 = r'y\^2/([^\s\+\)]+).*?\+.*?x\^2/([^\s=\)]+).*?=.*?1'
        match2 = re.search(pattern2, eq)
        if match2:
            b_sq_str = self._clean_parameter(match2.group(1))
            a_sq_str = self._clean_parameter(match2.group(2))
            # 检查 A > B
            if self._compare_values(a_sq_str, b_sq_str) > 0:
                return True
        
        return False
    
    def _extract_parameters(self, equation: str) -> tuple:
        """
        从方程中提取 a^2 和 b^2
        
        Returns:
            tuple: (a_squared, b_squared)
        """
        eq = equation.replace(' ', '')
        
        # 模式1: x^2/A + y^2/B = 1
        pattern1 = r'x\^2/([^\s\+\)]+).*?\+.*?y\^2/([^\s=\)]+)'
        match1 = re.search(pattern1, eq)
        if match1:
            a_squared = self._clean_parameter(match1.group(1))
            b_squared = self._clean_parameter(match1.group(2))
            if self._compare_values(a_squared, b_squared) > 0:
                return a_squared, b_squared
        
        # 模式2: y^2/B + x^2/A = 1
        pattern2 = r'y\^2/([^\s\+\)]+).*?\+.*?x\^2/([^\s=\)]+)'
        match2 = re.search(pattern2, eq)
        if match2:
            b_squared = self._clean_parameter(match2.group(1))
            a_squared = self._clean_parameter(match2.group(2))
            if self._compare_values(a_squared, b_squared) > 0:
                return a_squared, b_squared
        
        return None, None
    
    def _clean_parameter(self, param: str) -> str:
        """清理参数字符串"""
        param = param.strip('()')
        return param
    
    def _compare_values(self, val1: str, val2: str) -> int:
        """
        比较两个值的大小
        
        Returns:
            1 if val1 > val2
            -1 if val1 < val2
            0 if equal or cannot compare
        """
        try:
            num1 = float(val1)
            num2 = float(val2)
            if num1 > num2:
                return 1
            elif num1 < num2:
                return -1
            else:
                return 0
        except:
            # 无法比较符号值，假设第一个参数位置是a^2
            return 1
    
    def _simplify_sqrt(self, value: str) -> str:
        """
        简化平方根
        
        例如:
        - "4" -> "2"
        - "9" -> "3"
        - "25" -> "5"
        - "m" -> "sqrt(m)"
        """
        # 情况1: 纯数字
        try:
            num = float(value)
            sqrt_num = num ** 0.5
            if sqrt_num == int(sqrt_num):
                return str(int(sqrt_num))
            else:
                return f"sqrt({value})"
        except:
            pass
        
        # 情况2: 形如 m^2
        match = re.match(r'([a-zA-Z_]\w*)\^2$', value)
        if match:
            return match.group(1)
        
        # 其他情况: 保持符号形式
        return f"sqrt({value})"
