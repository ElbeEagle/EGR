"""
EquationNormalizer - 方程标准化器

负责将非标准形式的方程转换为标准形式
"""

import re
from typing import Optional


class EquationNormalizer:
    """
    方程标准化器
    
    功能：
    1. 识别非标准形式的方程
    2. 转换为标准形式
    3. 保留原始语义
    
    支持的转换：
    - y = x²/4  →  x² = 4y
    - y² = 1    →  y²/1 = 1
    - 4x² + 9y² = 36  →  x²/9 + y²/4 = 1
    - x²/3 - y² = 1  →  x²/3 - y²/1 = 1
    """
    
    def __init__(self):
        """初始化标准化器"""
        pass
    
    def normalize_equation(self, equation: str) -> str:
        """
        标准化方程
        
        Args:
            equation: 原始方程字符串
        
        Returns:
            str: 标准化后的方程
        """
        # 移除空格
        eq = equation.replace(' ', '')
        
        # 尝试各种标准化规则
        normalized = self._normalize_parabola_y_form(eq)
        if normalized != eq:
            return normalized
        
        normalized = self._normalize_missing_denominator(eq)
        if normalized != eq:
            return normalized
        
        normalized = self._normalize_general_to_standard(eq)
        if normalized != eq:
            return normalized
        
        # 如果没有匹配的规则，返回原方程
        return equation
    
    def _normalize_parabola_y_form(self, equation: str) -> str:
        """
        转换抛物线 y = ax² 形式
        
        规则：
        - y = x²/4  →  x² = 4y
        - y = ax²   →  x² = y/a
        - y = x²    →  x² = y
        
        Args:
            equation: 输入方程
        
        Returns:
            str: 标准化后的方程
        """
        eq = equation.replace(' ', '')
        
        # 提取方程内容
        inner_eq = eq
        if 'Expression' in eq:
            match = re.search(r'Expression\([^)]+\)=\(([^)]+)\)', eq)
            if match:
                inner_eq = match.group(1)
        else:
            inner_eq = inner_eq.strip('()')
        
        # 模式1: y = x²/c
        # 例如: y = x²/4  →  x² = 4*y
        pattern1 = r'y=x\^2/(\d+\.?\d*)'
        match1 = re.search(pattern1, inner_eq)
        if match1:
            c = match1.group(1)
            # x² = c*y 即 x² = 2p*y, 其中 p = c/2
            result = f"x^2 = {c}*y"
            if 'Expression' in eq:
                prefix = eq.split('=')[0] + '= '
                return f"{prefix}({result})"
            return f"({result})"
        
        # 模式2: y = x²
        # 例如: y = x²  →  x² = y
        pattern2 = r'^y=x\^2$'
        if re.match(pattern2, inner_eq):
            result = "x^2 = y"
            if 'Expression' in eq:
                prefix = eq.split('=')[0] + '= '
                return f"{prefix}({result})"
            return f"({result})"
        
        # 模式3: y = (1/c)*x²
        # 例如: y = (1/4)*x²  →  x² = 4*y
        pattern3 = r'y=\(1/(\d+\.?\d*)\)\*x\^2'
        match3 = re.search(pattern3, inner_eq)
        if match3:
            c = match3.group(1)
            result = f"x^2 = {c}*y"
            if 'Expression' in eq:
                prefix = eq.split('=')[0] + '= '
                return f"{prefix}({result})"
            return f"({result})"
        
        return equation
    
    def _normalize_missing_denominator(self, equation: str) -> str:
        """
        补充缺失的分母
        
        规则：
        - x²/3 - y² = 1  →  x²/3 - y²/1 = 1
        - x² + y²/4 = 1  →  x²/1 + y²/4 = 1
        
        Args:
            equation: 输入方程
        
        Returns:
            str: 标准化后的方程
        """
        eq = equation.replace(' ', '')
        
        # 提取方程内容 (去除 Expression(...) = )
        inner_eq = eq
        if 'Expression' in eq:
            match = re.search(r'Expression\([^)]+\)=\(([^)]+)\)', eq)
            if match:
                inner_eq = match.group(1)
        else:
            # 去除可能的外层括号
            inner_eq = inner_eq.strip('()')
        
        # 模式1: x²/A - y² = 1  →  x²/A - y²/1 = 1
        pattern1 = r'(x\^2/[^\s\-\+]+)\s*-\s*y\^2\s*=\s*1'
        match1 = re.search(pattern1, inner_eq)
        if match1:
            x_part = match1.group(1)
            result = f"{x_part} - y^2/1 = 1"
            # 保留原始格式
            if 'Expression' in eq:
                prefix = eq.split('=')[0] + '= '
                return f"{prefix}({result})"
            return f"({result})"
        
        # 模式2: x² + y²/B = 1  →  x²/1 + y²/B = 1
        pattern2 = r'x\^2\s*\+\s*(y\^2/[^\s=\)]+)\s*=\s*1'
        match2 = re.search(pattern2, inner_eq)
        if match2:
            y_part = match2.group(1)
            result = f"x^2/1 + {y_part} = 1"
            if 'Expression' in eq:
                prefix = eq.split('=')[0] + '= '
                return f"{prefix}({result})"
            return f"({result})"
        
        # 模式3: -y² + x²/A = 1  →  -y²/1 + x²/A = 1
        pattern3 = r'-y\^2\s*\+\s*(x\^2/[^\s=\)]+)\s*=\s*1'
        match3 = re.search(pattern3, inner_eq)
        if match3:
            x_part = match3.group(1)
            result = f"-y^2/1 + {x_part} = 1"
            if 'Expression' in eq:
                prefix = eq.split('=')[0] + '= '
                return f"{prefix}({result})"
            return f"({result})"
        
        # 模式4: x²/A + y² = 1  →  x²/A + y²/1 = 1
        pattern4 = r'(x\^2/[^\s\+]+)\s*\+\s*y\^2\s*=\s*1'
        match4 = re.search(pattern4, inner_eq)
        if match4:
            x_part = match4.group(1)
            result = f"{x_part} + y^2/1 = 1"
            if 'Expression' in eq:
                prefix = eq.split('=')[0] + '= '
                return f"{prefix}({result})"
            return f"({result})"
        
        return equation
    
    def _normalize_general_to_standard(self, equation: str) -> str:
        """
        转换一般形式到标准形式
        
        规则：
        - 4x² + 9y² = 36  →  x²/9 + y²/4 = 1
        - Ax² + By² = C   →  x²/(C/A) + y²/(C/B) = 1
        
        Args:
            equation: 输入方程
        
        Returns:
            str: 标准化后的方程
        """
        eq = equation.replace(' ', '')
        
        # 提取方程内容
        inner_eq = eq
        if 'Expression' in eq:
            match = re.search(r'Expression\([^)]+\)=\(([^)]+)\)', eq)
            if match:
                inner_eq = match.group(1)
        else:
            inner_eq = inner_eq.strip('()')
        
        # 模式: Ax² + By² = C
        pattern = r'(\d+\.?\d*)\*?x\^2\s*\+\s*(\d+\.?\d*)\*?y\^2\s*=\s*(\d+\.?\d*)'
        match = re.search(pattern, inner_eq)
        if match:
            try:
                A = float(match.group(1))
                B = float(match.group(2))
                C = float(match.group(3))
                
                # 计算 x²和y²的分母
                x_denom = C / A
                y_denom = C / B
                
                # 转换为整数（如果可能）
                if x_denom == int(x_denom):
                    x_denom = int(x_denom)
                if y_denom == int(y_denom):
                    y_denom = int(y_denom)
                
                result = f"x^2/{x_denom} + y^2/{y_denom} = 1"
                
                if 'Expression' in eq:
                    prefix = eq.split('=')[0] + '= '
                    return f"{prefix}({result})"
                return f"({result})"
            except:
                pass
        
        return equation
    
    def normalize_fact_expressions(self, fact_expressions: str) -> str:
        """
        标准化整个fact_expressions字符串
        
        Args:
            fact_expressions: 原始fact表达式
        
        Returns:
            str: 标准化后的fact表达式
        """
        # 分割facts
        facts = fact_expressions.split(';')
        normalized_facts = []
        
        for fact in facts:
            fact = fact.strip()
            if not fact:
                continue
            
            # 如果包含 Expression 且有等号，进行标准化
            if 'Expression' in fact and '=' in fact:
                normalized = self.normalize_equation(fact)
                normalized_facts.append(normalized)
            else:
                normalized_facts.append(fact)
        
        return ';'.join(normalized_facts)


# 测试用例
if __name__ == "__main__":
    normalizer = EquationNormalizer()
    
    test_cases = [
        # 抛物线
        ("y = x^2/4", "(x^2 = 4*y)"),
        ("y = x^2", "(x^2 = y)"),
        
        # 缺失分母
        ("Expression(G) = (x^2/3 - y^2 = 1)", "Expression(G) = (x^2/3 - y^2/1 = 1)"),
        ("Expression(G) = (x^2 + y^2/4 = 1)", "Expression(G) = (x^2/1 + y^2/4 = 1)"),
        
        # 一般形式
        ("4*x^2 + 9*y^2 = 36", "(x^2/9 + y^2/4 = 1)"),
    ]
    
    print("方程标准化测试:")
    print("=" * 80)
    for input_eq, expected in test_cases:
        result = normalizer.normalize_equation(input_eq)
        status = "✅" if result == expected else "❌"
        print(f"{status} {input_eq}")
        print(f"   预期: {expected}")
        print(f"   实际: {result}")
        print()
