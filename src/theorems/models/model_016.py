"""
Model 16: Ellipse_Focal_Radius
椭圆焦半径公式

公式: 
  |PF₁| = a + ex₀ (P在椭圆上，焦点在x轴)
  |PF₂| = a - ex₀
或
  |PF₁| = a + ey₀ (P在椭圆上，焦点在y轴)
  |PF₂| = a - ey₀
"""

from ..base_model import TheoremModel


class EllipseFocalRadius(TheoremModel):
    """
    椭圆焦半径公式
    
    前置条件:
    - 实体包含 Ellipse 类型
    - 已知参数 a 和 e（或 c）
    - 有椭圆上的点
    
    输出:
    - geometric_relations: 焦半径公式
    
    示例:
    对于焦点在x轴的椭圆，点P(x₀, y₀)在椭圆上
    |PF₁| = a + ex₀
    |PF₂| = a - ex₀
    """
    
    def __init__(self):
        super().__init__(
            model_id=16,
            name="Ellipse_Focal_Radius",
            chinese_name="椭圆焦半径"
        )
    
    def can_apply(self, state) -> bool:
        """
        检查是否可应用
        
        条件:
        1. 存在 Ellipse 实体
        2. 已知 a 和 e（或 c）
        3. 有点在椭圆上
        """
        # 条件1: 检查是否有椭圆实体
        has_ellipse = any(
            entity_type.lower() == 'ellipse'
            for entity_type in state.entities.values()
        )
        if not has_ellipse:
            return False
        
        # 条件2: 检查是否有 a 和 e（或 c）
        has_a = 'a' in state.parameters or 'a^2' in state.parameters
        has_e = 'e' in state.parameters
        has_c = 'c' in state.parameters or 'c^2' in state.parameters
        
        if not has_a:
            return False
        
        if not (has_e or has_c):
            return False
        
        # 条件3: 检查是否有点在椭圆上
        for rel in state.geometric_relations:
            if 'PointOnCurve' in rel or '在椭圆上' in rel:
                return True
        
        # 或者有焦点距离需求
        for rel in state.geometric_relations:
            if 'PF' in rel or 'Distance' in rel and 'F' in rel:
                return True
        
        return False
    
    def apply(self, state) -> None:
        """
        应用模型，添加椭圆焦半径公式
        """
        # 获取参数
        a_val = state.parameters.get('a')
        e_val = state.parameters.get('e')
        
        # 如果没有e，从c和a计算
        if not e_val and 'c' in state.parameters and a_val:
            try:
                c_num = float(state.parameters['c'])
                a_num = float(a_val)
                e_val = str(c_num / a_num)
            except:
                e_val = f"{state.parameters['c']}/{a_val}"
        
        # 判断焦点位置
        focal_on_x = self._is_focal_on_x_axis(state)
        
        if focal_on_x:
            # 焦点在x轴
            if a_val and e_val:
                state.geometric_relations.append(
                    f"椭圆焦半径公式: |PF₁| = {a_val} + {e_val}·x₀, |PF₂| = {a_val} - {e_val}·x₀"
                )
            else:
                state.geometric_relations.append(
                    "椭圆焦半径公式: |PF₁| = a + e·x₀, |PF₂| = a - e·x₀"
                )
        else:
            # 焦点在y轴
            if a_val and e_val:
                state.geometric_relations.append(
                    f"椭圆焦半径公式: |PF₁| = {a_val} + {e_val}·y₀, |PF₂| = {a_val} - {e_val}·y₀"
                )
            else:
                state.geometric_relations.append(
                    "椭圆焦半径公式: |PF₁| = a + e·y₀, |PF₂| = a - e·y₀"
                )
        
        # 添加通用说明
        state.geometric_relations.append(
            "其中P(x₀, y₀)或P(x₀, y₀)为椭圆上的点"
        )
        
        # 记录已应用的模型
        state.applied_models.append(self.model_id)
    
    def _is_focal_on_x_axis(self, state) -> bool:
        """
        判断焦点是否在x轴上
        
        Returns:
            bool: True表示焦点在x轴，False表示在y轴
        """
        # 方法1: 从几何关系推断
        for rel in state.geometric_relations:
            if '焦点在x轴' in rel or 'focal_on_x' in rel.lower():
                return True
            if '焦点在y轴' in rel or 'focal_on_y' in rel.lower():
                return False
        
        # 方法2: 从方程推断（x²/a² + y²/b² = 1，如果a²对应x²，焦点在x轴）
        for eq in state.equations:
            if 'x^2' in eq and 'y^2' in eq:
                # 简单假设：第一个出现的是长轴
                if eq.index('x^2') < eq.index('y^2'):
                    return True
                else:
                    return False
        
        # 默认假设焦点在x轴
        return True
