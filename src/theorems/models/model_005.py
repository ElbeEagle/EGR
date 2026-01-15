"""
Model 5: Hyperbola_Equation_Standard_X
双曲线标准方程（焦点在x轴）参数提取

公式: x^2/a^2 - y^2/b^2 = 1
提取: a, b, a^2, b^2
"""

import re
from ..base_model import TheoremModel


class HyperbolaEquationStandardX(TheoremModel):
    """
    双曲线标准方程（焦点在x轴）参数提取
    
    前置条件:
    - 实体包含 Hyperbola 类型
    - 方程形式: x^2/A - y^2/B = 1
    
    输出:
    - parameters: a^2, b^2, a, b
    - geometric_relations: a^2=A, b^2=B, 焦点在x轴
    
    示例:
    输入: Expression(G) = (x^2/4 - y^2/m^2 = 1)
    输出: a^2=4, b^2=m^2, a=2, b=m
    """
    
    def __init__(self):
        super().__init__(
            model_id=5,
            name="Hyperbola_Equation_Standard_X",
            chinese_name="双曲线标准方程(焦点在x轴)"
        )
    
    def can_apply(self, state) -> bool:
        """
        检查是否可应用
        
        条件:
        1. 存在 Hyperbola 实体
        2. 存在形如 x^2/A - y^2/B = 1 的方程
        """
        # 条件1: 检查是否有双曲线实体
        has_hyperbola = any(
            entity_type.lower() == 'hyperbola'
            for entity_type in state.entities.values()
        )
        if not has_hyperbola:
            return False
        
        # 条件2: 检查是否有标准方程
        for eq in state.equations:
            # 匹配模式: x^2/A - y^2/B = 1
            # 支持多种写法
            if self._is_standard_hyperbola_x(eq):
                return True
        
        return False
    
    def apply(self, state) -> None:
        """
        应用模型，提取参数
        """
        # 查找标准方程
        for eq in state.equations:
            if not self._is_standard_hyperbola_x(eq):
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
    
    def _is_standard_hyperbola_x(self, equation: str) -> bool:
        """
        判断是否为标准双曲线方程（x项为正）
        
        匹配模式：
        - x^2/A - y^2/B = 1
        - x^2/a^2 - y^2/b^2 = 1
        - -y^2/B + x^2/A = 1
        """
        # 去除空格
        eq = equation.replace(' ', '')
        
        # 模式1: x^2/A - y^2/B = 1
        pattern1 = r'x\^2/([^\s\-\+]+).*?-.*?y\^2/([^\s=\)]+).*?=.*?1'
        if re.search(pattern1, eq):
            return True
        
        # 模式2: -y^2/B + x^2/A = 1
        pattern2 = r'-y\^2/([^\s\+]+).*?\+.*?x\^2/([^\s=\)]+).*?=.*?1'
        if re.search(pattern2, eq):
            return True
        
        return False
    
    def _extract_parameters(self, equation: str) -> tuple:
        """
        从方程中提取 a^2 和 b^2
        
        Returns:
            tuple: (a_squared, b_squared)
        """
        eq = equation.replace(' ', '')
        
        # 模式1: x^2/A - y^2/B = 1
        pattern1 = r'x\^2/([^\s\-\+\)]+).*?-.*?y\^2/([^\s=\)]+)'
        match1 = re.search(pattern1, eq)
        if match1:
            a_squared = match1.group(1)
            b_squared = match1.group(2)
            return self._clean_parameter(a_squared), self._clean_parameter(b_squared)
        
        # 模式2: -y^2/B + x^2/A = 1
        pattern2 = r'-y\^2/([^\s\+\)]+).*?\+.*?x\^2/([^\s=\)]+)'
        match2 = re.search(pattern2, eq)
        if match2:
            b_squared = match2.group(1)
            a_squared = match2.group(2)
            return self._clean_parameter(a_squared), self._clean_parameter(b_squared)
        
        return None, None
    
    def _clean_parameter(self, param: str) -> str:
        """清理参数字符串"""
        # 移除括号
        param = param.strip('()')
        return param
    
    def _simplify_sqrt(self, value: str) -> str:
        """
        简化平方根
        
        例如:
        - "4" -> "2"
        - "9" -> "3"
        - "m^2" -> "m"
        - "a^2" -> "a"
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
        
        # 情况3: 形如 (something)^2
        match = re.match(r'\((.+)\)\^2$', value)
        if match:
            return match.group(1)
        
        # 其他情况: 保持符号形式
        return f"sqrt({value})"
