"""
Model 7: Parabola_Equation_Standard_Right
抛物线标准方程（开口向右）参数提取

公式: y^2 = 2px (p > 0)
提取: p, 焦点坐标, 准线方程
"""

import re
from ..base_model import TheoremModel


class ParabolaEquationStandardRight(TheoremModel):
    """
    抛物线标准方程（开口向右）参数提取
    
    前置条件:
    - 实体包含 Parabola 类型
    - 方程形式: y^2 = Kx 或 y^2 = K*x (K > 0)
    
    输出:
    - parameters: p, 2p
    - coordinates: Focus坐标 (p/2, 0)
    - geometric_relations: 准线方程 x = -p/2
    
    示例:
    输入: Expression(G) = (y^2 = 4*x)
    输出: 2p=4, p=2, Focus=(1, 0), 准线: x=-1
    """
    
    def __init__(self):
        super().__init__(
            model_id=7,
            name="Parabola_Equation_Standard_Right",
            chinese_name="抛物线标准方程(开口向右)"
        )
    
    def can_apply(self, state) -> bool:
        """
        检查是否可应用
        
        条件:
        1. 存在 Parabola 实体
        2. 存在形如 y^2 = Kx 的方程
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
            if self._is_standard_parabola_right(eq):
                return True
        
        return False
    
    def apply(self, state) -> bool:
        """
        应用模型，提取参数
        """
        try:
            # 查找标准方程
            for eq in state.equations:
                if not self._is_standard_parabola_right(eq):
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
                
                    # 焦点坐标 (p/2, 0)
                    focus_x = p_num / 2
                    state.coordinates['Focus'] = (str(focus_x) if focus_x != int(focus_x) else str(int(focus_x)), '0')
                
                    # 准线方程 x = -p/2
                    directrix_x = -p_num / 2
                    state.geometric_relations.append(f"准线: x = {directrix_x}")
                    state.geometric_relations.append(f"焦点: ({focus_x}, 0)")
                
                except:
                    state.parameters['p'] = f"{k_val}/2"
                    state.coordinates['Focus'] = (f"{k_val}/4", '0')
                    state.geometric_relations.append(f"准线: x = -{k_val}/4")
            
                # 记录已应用的模型
                state.applied_models.append(self.model_id)
            
                # 只处理第一个匹配的方程
                break
    
            return True

        except Exception:
            return False
    def _is_standard_parabola_right(self, equation: str) -> bool:
        """
        判断是否为标准抛物线方程（开口向右）
        
        匹配模式：
        - y^2 = Kx
        - y^2 = K*x
        """
        eq = equation.replace(' ', '')
        
        # 模式: y^2 = K*x 或 y^2 = Kx
        pattern = r'y\^2\s*=\s*([^=\)]+)\*?x'
        if re.search(pattern, eq):
            return True
        
        return False
    
    def _extract_coefficient(self, equation: str) -> str:
        """
        从方程中提取系数 K
        
        例如:
        - y^2 = 4*x -> "4"
        - y^2 = 2*p*x -> "2*p"
        """
        eq = equation.replace(' ', '')
        
        # 模式: y^2 = K*x 或 y^2 = Kx
        pattern = r'y\^2\s*=\s*([^=\)]+?)\*?x'
        match = re.search(pattern, eq)
        if match:
            coef = match.group(1).strip('*')
            return coef
        
        return None
