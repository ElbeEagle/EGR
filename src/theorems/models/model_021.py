"""
Model 21: Hyperbola_Asymptote
双曲线渐近线

公式: y = ±(b/a)x
前提: 已知 a 和 b
"""

import re
from ..base_model import TheoremModel


class HyperbolaAsymptote(TheoremModel):
    """
    双曲线渐近线
    
    前置条件:
    - 实体包含 Hyperbola 类型
    - 参数中有 a 和 b
    
    输出:
    - equations: 渐近线方程 y = ±(b/a)x
    - geometric_relations: 渐近线关系
    
    示例:
    输入: a=2, b=m
    输出: Expression(Asymptote(G)) = (y = pm*(m/2)*x)
    """
    
    def __init__(self):
        super().__init__(
            model_id=21,
            name="Hyperbola_Asymptote",
            chinese_name="双曲线渐近线"
        )
    
    def can_apply(self, state) -> bool:
        """
        检查是否可应用
        
        条件:
        1. 存在 Hyperbola 实体
        2. 参数中有 a 和 b
        """
        # 条件1: 检查是否有双曲线实体
        has_hyperbola = any(
            entity_type.lower() == 'hyperbola'
            for entity_type in state.entities.values()
        )
        if not has_hyperbola:
            return False
        
        # 条件2: 检查是否有 a 和 b 参数
        if 'a' not in state.parameters or 'b' not in state.parameters:
            return False
        
        return True
    
    def apply(self, state) -> bool:
        """
        应用模型，添加渐近线方程
        """
        try:
            a_val = state.parameters['a']
            b_val = state.parameters['b']
        
            # 查找双曲线实体名称
            hyperbola_name = None
            for name, type_ in state.entities.items():
                if type_.lower() == 'hyperbola':
                    hyperbola_name = name
                    break
        
            if hyperbola_name is None:
                hyperbola_name = 'G'  # 默认名称
        
            # 构建渐近线方程
            # 格式: y = pm*(b/a)*x  其中pm表示±
            asymptote_eq = f"y = pm*({b_val}/{a_val})*x"
        
            # 添加到方程列表
            equation_str = f"Expression(Asymptote({hyperbola_name})) = ({asymptote_eq})"
            state.equations.append(equation_str)
        
            # 添加几何关系（便于人类阅读）
            state.geometric_relations.append(f"渐近线: y = ±({b_val}/{a_val})x")
        
            # 尝试简化渐近线斜率
            slope = self._simplify_fraction(b_val, a_val)
            if slope:
                state.geometric_relations.append(f"渐近线斜率: ±{slope}")
        
            # 记录已应用的模型
            state.applied_models.append(self.model_id)
    
            return True

        except Exception:
            return False
    def _simplify_fraction(self, numerator: str, denominator: str) -> str:
        """
        简化分数
        
        例如:
        - "m", "2" -> "m/2"
        - "4", "2" -> "2"
        """
        # 尝试数值简化
        try:
            num_val = float(numerator)
            den_val = float(denominator)
            result = num_val / den_val
            if result == int(result):
                return str(int(result))
            else:
                return f"{numerator}/{denominator}"
        except:
            # 符号形式
            if denominator == "1":
                return numerator
            else:
                return f"{numerator}/{denominator}"
