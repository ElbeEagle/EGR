"""
Model 17: Parabola_Focal_Radius
抛物线焦半径公式

对于抛物线上的点，焦半径 = 点的相应坐标 + p/2
"""

import re
from ..base_model import TheoremModel


class ParabolaFocalRadius(TheoremModel):
    """
    抛物线焦半径公式
    
    前置条件:
    - 实体包含 Parabola 类型
    - 已知参数 p
    - 有抛物线上的点
    
    输出:
    - geometric_relations: 焦半径公式
    
    示例:
    对于 y^2=2px，点P(x0,y0)在抛物线上
    焦半径 |PF| = x0 + p/2
    """
    
    def __init__(self):
        super().__init__(
            model_id=17,
            name="Parabola_Focal_Radius",
            chinese_name="抛物线焦半径"
        )
    
    def can_apply(self, state) -> bool:
        """
        检查是否可应用
        
        条件:
        1. 存在 Parabola 实体
        2. 已知参数 p
        3. 有点在抛物线上
        """
        # 条件1: 检查是否有抛物线实体
        has_parabola = any(
            entity_type.lower() == 'parabola'
            for entity_type in state.entities.values()
        )
        if not has_parabola:
            return False
        
        # 条件2: 检查是否有 p 参数
        if 'p' not in state.parameters and '2p' not in state.parameters:
            return False
        
        # 条件3: 检查是否有点在抛物线上
        for rel in state.geometric_relations:
            if 'PointOnCurve' in rel:
                return True
        
        return False
    
    def apply(self, state) -> None:
        """
        应用模型，添加焦半径公式
        """
        # 获取 p 值
        p_val = state.parameters.get('p')
        if not p_val and '2p' in state.parameters:
            try:
                two_p = float(state.parameters['2p'])
                p_val = str(two_p / 2)
            except:
                p_val = f"{state.parameters['2p']}/2"
        
        if not p_val:
            return
        
        # 判断开口方向
        direction = self._infer_direction(state)
        
        # 添加焦半径公式
        try:
            p_num = float(p_val)
            p_half = p_num / 2
            
            if direction == 'right':
                # y^2 = 2px，|PF| = x + p/2
                formula = f"焦半径公式: |PF| = x + {p_half}"
            elif direction == 'up':
                # x^2 = 2py，|PF| = y + p/2
                formula = f"焦半径公式: |PF| = y + {p_half}"
            elif direction == 'left':
                # y^2 = -2px，|PF| = -x + p/2
                formula = f"焦半径公式: |PF| = -x + {p_half}"
            elif direction == 'down':
                # x^2 = -2py，|PF| = -y + p/2
                formula = f"焦半径公式: |PF| = -y + {p_half}"
            else:
                formula = f"焦半径公式: |PF| = x + {p_half}"
            
            state.geometric_relations.append(formula)
            
        except:
            # 符号形式
            state.geometric_relations.append(f"焦半径公式: |PF| = x + {p_val}/2")
        
        # 记录已应用的模型
        state.applied_models.append(self.model_id)
    
    def _infer_direction(self, state) -> str:
        """
        推断抛物线开口方向
        
        Returns:
            str: 'right', 'left', 'up', 'down'
        """
        # 从方程推断
        for eq in state.equations:
            eq_lower = eq.lower()
            if 'y^2' in eq and '=' in eq and 'x' in eq:
                if '-' in eq.split('=')[1]:
                    return 'left'
                return 'right'
            elif 'x^2' in eq and '=' in eq and 'y' in eq:
                if '-' in eq.split('=')[1]:
                    return 'down'
                return 'up'
        
        # 默认向右
        return 'right'
