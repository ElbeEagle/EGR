"""
Model 9: Parabola_Equation_Standard_Up
抛物线标准方程（开口向上）参数提取

公式: x^2 = 2py (p > 0)
提取: p, 焦点坐标, 准线方程
"""

import re
from ..base_model import TheoremModel


class ParabolaEquationStandardUp(TheoremModel):
    """
    抛物线标准方程（开口向上）参数提取
    
    前置条件:
    - 实体包含 Parabola 类型
    - 方程形式: x^2 = Ky 或 x^2 = K*y (K > 0)
    
    输出:
    - parameters: p, 2p
    - coordinates: Focus坐标 (0, p/2)
    - geometric_relations: 准线方程 y = -p/2
    
    示例:
    输入: Expression(G) = (x^2 = 4*y)
    输出: 2p=4, p=2, Focus=(0, 1), 准线: y=-1
    """
    
    def __init__(self):
        super().__init__(
            model_id=9,
            name="Parabola_Equation_Standard_Up",
            chinese_name="抛物线标准方程(开口向上)"
        )
    
    def can_apply(self, state) -> bool:
        """
        检查是否可应用
        
        条件:
        1. 存在 Parabola 实体
        2. 存在形如 x^2 = Ky 的方程
        """
        # 条件1: 检查是否有抛物线实体
        has_parabola = any(
            entity_type.lower() == 'parabola'
            for entity_type in state.entities.values()
        )
        if not has_parabola:
            return False
        
        # 条件2: 检查是否有标准方程
        for eq in state.equations:
            if self._is_standard_parabola_up(eq):
                return True
        
        return False
    
    def apply(self, state) -> None:
        """
        应用模型，提取参数
        """
        # 查找标准方程
        for eq in state.equations:
            if not self._is_standard_parabola_up(eq):
                continue
            
            # 提取系数 K (2p = K)
            k_val = self._extract_coefficient(eq)
            
            if k_val is None:
                continue
            
            # 2p = K
            state.parameters['2p'] = k_val
            
            # 计算 p
            try:
                k_num = float(k_val)
                p_num = k_num / 2
                if p_num == int(p_num):
                    state.parameters['p'] = str(int(p_num))
                else:
                    state.parameters['p'] = str(p_num)
                
                # 焦点坐标 (0, p/2)
                focus_y = p_num / 2
                state.coordinates['Focus'] = ('0', str(focus_y) if focus_y != int(focus_y) else str(int(focus_y)))
                
                # 准线方程 y = -p/2
                directrix_y = -p_num / 2
                state.geometric_relations.append(f"准线: y = {directrix_y}")
                state.geometric_relations.append(f"焦点: (0, {focus_y})")
                
            except:
                state.parameters['p'] = f"{k_val}/2"
                state.coordinates['Focus'] = ('0', f"{k_val}/4")
                state.geometric_relations.append(f"准线: y = -{k_val}/4")
            
            # 记录已应用的模型
            state.applied_models.append(self.model_id)
            
            # 只处理第一个匹配的方程
            break
    
    def _is_standard_parabola_up(self, equation: str) -> bool:
        """
        判断是否为标准抛物线方程（开口向上）
        
        匹配模式：
        - x^2 = Ky
        - x^2 = K*y
        """
        eq = equation.replace(' ', '')
        
        # 模式: x^2 = K*y 或 x^2 = Ky
        pattern = r'x\^2\s*=\s*([^=\)]+)\*?y'
        if re.search(pattern, eq):
            return True
        
        return False
    
    def _extract_coefficient(self, equation: str) -> str:
        """
        从方程中提取系数 K
        
        例如:
        - x^2 = 4*y -> "4"
        - x^2 = 2*p*y -> "2*p"
        """
        eq = equation.replace(' ', '')
        
        # 模式: x^2 = K*y 或 x^2 = Ky
        pattern = r'x\^2\s*=\s*([^=\)]+?)\*?y'
        match = re.search(pattern, eq)
        if match:
            coef = match.group(1).strip('*')
            return coef
        
        return None
