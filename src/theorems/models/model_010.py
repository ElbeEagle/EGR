"""
Model 10: Parabola_Equation_Standard_Down
抛物线标准方程(开口向下)

从抛物线方程 x² = -2py (p > 0) 提取参数 p
"""

import re
from ..base_model import TheoremModel


class ParabolaEquationStandardDown(TheoremModel):
    """
    抛物线标准方程(开口向下)
    
    前置条件:
    - 实体包含 Parabola 类型
    - 方程形式为 x² = -2py 或 x² + 2py = 0
    
    输出:
    - parameters: p, 2p
    - geometric_relations: 开口方向
    
    示例:
    输入: x^2 = -8y
    输出: 2p=8, p=4, 开口向下
    """
    
    def __init__(self):
        super().__init__(
            model_id=10,
            name="Parabola_Equation_Standard_Down",
            chinese_name="抛物线标准方程(开口向下)"
        )
    
    def can_apply(self, state) -> bool:
        """
        检查是否可应用
        
        条件:
        1. 存在 Parabola 实体
        2. 方程形式为 x² = -...y（负号表示开口向下）
        """
        # 条件1: 检查是否有抛物线实体
        has_parabola = any(
            entity_type.lower() == 'parabola'
            for entity_type in state.entities.values()
        )
        if not has_parabola:
            return False
        
        # 条件2: 检查方程
        for eq in state.equations:
            # 匹配 x^2 = -...y 形式
            if 'x^2' in eq and 'y' in eq:
                # 检查是否有负号
                if re.search(r'x\^2\s*=\s*-\s*\d*\s*\*?y', eq):
                    return True
                # 或者 x^2 + ...y = 0 形式
                if re.search(r'x\^2\s*\+\s*\d+\s*\*?y\s*=\s*0', eq):
                    return True
        
        return False
    
    def apply(self, state) -> None:
        """
        应用模型，提取抛物线参数
        """
        for eq in state.equations:
            if 'x^2' in eq and 'y' in eq:
                coef = self._extract_coefficient(eq)
                
                if coef:
                    # x² = -2py，coef 就是 2p
                    state.parameters['2p'] = coef
                    
                    # 计算 p
                    try:
                        two_p = float(coef)
                        p_val = two_p / 2
                        
                        if p_val == int(p_val):
                            state.parameters['p'] = str(int(p_val))
                        else:
                            state.parameters['p'] = str(p_val)
                    except:
                        # 符号形式
                        state.parameters['p'] = f"{coef}/2"
                    
                    # 添加几何关系
                    state.geometric_relations.append("抛物线开口向下")
                    
                    break
        
        # 记录已应用的模型
        state.applied_models.append(self.model_id)
    
    def _extract_coefficient(self, eq: str):
        """
        从方程中提取系数
        
        Returns:
            coef: 2p的值
        """
        # 匹配 x^2 = -8y → 2p=8
        patterns = [
            # x^2 = -8*y 或 x^2 = -8y
            r'x\^2\s*=\s*-\s*(\d+\.?\d*)\s*\*?\s*y',
            # x^2 + 8y = 0
            r'x\^2\s*\+\s*(\d+\.?\d*)\s*\*?\s*y\s*=\s*0',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, eq)
            if match:
                return match.group(1)
        
        return None
