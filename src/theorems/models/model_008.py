"""
Model 8: Parabola_Equation_Standard_Left
抛物线标准方程(开口向左)

从抛物线方程 y² = -2px (p > 0) 提取参数 p
"""

import re
from ..base_model import TheoremModel


class ParabolaEquationStandardLeft(TheoremModel):
    """
    抛物线标准方程(开口向左)
    
    前置条件:
    - 实体包含 Parabola 类型
    - 方程形式为 y² = -2px 或 y² + 2px = 0
    
    输出:
    - parameters: p, 2p
    - geometric_relations: 开口方向
    
    示例:
    输入: y^2 = -8x
    输出: 2p=8, p=4, 开口向左
    """
    
    def __init__(self):
        super().__init__(
            model_id=8,
            name="Parabola_Equation_Standard_Left",
            chinese_name="抛物线标准方程(开口向左)"
        )
    
    def can_apply(self, state) -> bool:
        """
        检查是否可应用
        
        条件:
        1. 存在 Parabola 实体
        2. 方程形式为 y² = -...x（负号表示开口向左）
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
            # 匹配 y^2 = -...x 形式
            if 'y^2' in eq and 'x' in eq:
                # 检查是否有负号
                if re.search(r'y\^2\s*=\s*-\s*\d*\s*\*?x', eq):
                    return True
                # 或者 y^2 + ...x = 0 形式
                if re.search(r'y\^2\s*\+\s*\d+\s*\*?x\s*=\s*0', eq):
                    return True
        
        return False
    
    def apply(self, state) -> bool:
        """
        应用模型，提取抛物线参数
        """
        try:
            for eq in state.equations:
                if 'y^2' in eq and 'x' in eq:
                    coef = self._extract_coefficient(eq)
                
                    if coef:
                        # y² = -2px，coef 就是 2p
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
                        state.geometric_relations.append("抛物线开口向左")
                    
                        break
        
            # 记录已应用的模型
            state.applied_models.append(self.model_id)
    
            return True

        except Exception:
            return False
    def _extract_coefficient(self, eq: str):
        """
        从方程中提取系数
        
        Returns:
            coef: 2p的值
        """
        # 匹配 y^2 = -8x → 2p=8
        patterns = [
            # y^2 = -8*x 或 y^2 = -8x
            r'y\^2\s*=\s*-\s*(\d+\.?\d*)\s*\*?\s*x',
            # y^2 + 8x = 0
            r'y\^2\s*\+\s*(\d+\.?\d*)\s*\*?\s*x\s*=\s*0',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, eq)
            if match:
                return match.group(1)
        
        return None
