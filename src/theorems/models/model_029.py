"""
Model 29: Parabola_Directrix
抛物线准线

根据焦点位置和p值，求准线方程
"""

from ..base_model import TheoremModel


class ParabolaDirectrix(TheoremModel):
    """
    抛物线准线
    
    前置条件:
    - 实体包含 Parabola 类型
    - 已知参数 p
    
    输出:
    - geometric_relations: 准线方程
    
    示例:
    输入: p=2, 开口向右
    输出: 准线: x = -1
    """
    
    def __init__(self):
        super().__init__(
            model_id=29,
            name="Parabola_Directrix",
            chinese_name="抛物线准线"
        )
    
    def can_apply(self, state) -> bool:
        """
        检查是否可应用
        
        条件:
        1. 存在 Parabola 实体
        2. 已知参数 p 或 2p
        """
        # 条件1: 检查是否有抛物线实体
        has_parabola = any(
            entity_type.lower() == 'parabola'
            for entity_type in state.entities.values()
        )
        if not has_parabola:
            return False
        
        # 条件2: 检查是否有 p 参数
        if 'p' in state.parameters or '2p' in state.parameters:
            return True
        
        return False
    
    def apply(self, state) -> bool:
        """
        应用模型，添加准线方程
        """
        try:
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
        
            # 判断开口方向（从已有的几何关系或坐标推断）
            # 默认假设开口向右（最常见）
            direction = self._infer_direction(state)
        
            # 计算准线
            try:
                p_num = float(p_val)
                p_half = p_num / 2
            
                if direction == 'right':
                    # y^2 = 2px，准线 x = -p/2
                    directrix = f"x = {-p_half}"
                elif direction == 'up':
                    # x^2 = 2py，准线 y = -p/2
                    directrix = f"y = {-p_half}"
                elif direction == 'left':
                    # y^2 = -2px，准线 x = p/2
                    directrix = f"x = {p_half}"
                elif direction == 'down':
                    # x^2 = -2py，准线 y = p/2
                    directrix = f"y = {p_half}"
                else:
                    # 默认向右
                    directrix = f"x = {-p_half}"
            
                state.geometric_relations.append(f"准线: {directrix}")
            
            except:
                # 符号形式
                state.geometric_relations.append(f"准线: x = -{p_val}/2 (或其他方向)")
        
            # 记录已应用的模型
            state.applied_models.append(self.model_id)
    
            return True

        except Exception:
            return False
    def _infer_direction(self, state) -> str:
        """
        推断抛物线开口方向
        
        Returns:
            str: 'right', 'left', 'up', 'down'
        """
        # 方法1: 从方程推断
        for eq in state.equations:
            eq_lower = eq.lower()
            if 'y^2' in eq and '=' in eq and 'x' in eq:
                # y^2 = ... x 形式，开口向右或左
                if '-' in eq.split('=')[1]:
                    return 'left'
                return 'right'
            elif 'x^2' in eq and '=' in eq and 'y' in eq:
                # x^2 = ... y 形式，开口向上或下
                if '-' in eq.split('=')[1]:
                    return 'down'
                return 'up'
        
        # 方法2: 从焦点坐标推断
        if 'Focus' in state.coordinates:
            focus = state.coordinates['Focus']
            try:
                fx = float(focus[0])
                fy = float(focus[1])
                if fx > 0 and fy == 0:
                    return 'right'
                elif fx < 0 and fy == 0:
                    return 'left'
                elif fx == 0 and fy > 0:
                    return 'up'
                elif fx == 0 and fy < 0:
                    return 'down'
            except:
                pass
        
        # 默认向右
        return 'right'
