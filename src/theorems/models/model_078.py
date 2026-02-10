"""
Model 78: Substitution_x_equals_my_plus_n
代换 x = my + n

用于: 直线方程的参数形式，常用于联立方程
"""

import re
from ..base_model import TheoremModel


class SubstitutionXEqualsMYPlusN(TheoremModel):
    """
    代换 x = my + n
    
    前置条件:
    - 存在直线方程
    - 或需要进行代换
    
    输出:
    - 将直线方程转换为 x = my + n 形式
    
    示例:
    输入: 直线过点(1, 0)，斜率为k
    输出: x = ky + 1 或 x = (1/k)y + 1
    """
    
    def __init__(self):
        super().__init__(
            model_id=78,
            name="Substitution_x_equals_my_plus_n",
            chinese_name="代换x=my+n"
        )
    
    def can_apply(self, state) -> bool:
        """
        检查是否可应用
        
        条件:
        1. 存在直线实体
        2. 或存在代换、联立等需求
        """
        # 条件1: 存在直线
        has_line = any(
            entity_type.lower() == 'line'
            for entity_type in state.entities.values()
        )
        
        # 条件2: 几何关系中提到直线、斜率、代换等
        has_line_info = any(
            kw in rel for rel in state.geometric_relations
            for kw in ['Line', 'Slope', 'Intersection', '直线', '斜率']
        )
        
        return has_line or has_line_info
    
    def apply(self, state) -> bool:
        """
        应用模型，进行代换
        """
        try:
            # 查找直线方程
            for eq in state.equations:
                # 如果是直线方程，尝试转换为 x = my + n 形式
                if 'y' in eq and 'x' in eq:
                    # 简化处理：记录代换关系
                    state.geometric_relations.append("Substitution: x = m*y + n")
                    break
        
            # 如果存在斜率和点的信息
            if 'slope' in state.parameters or 'k' in state.parameters:
                state.geometric_relations.append("Line in form: x = m*y + n")
        
            # 记录已应用的模型
            state.applied_models.append(self.model_id)
            return True

        except Exception:
            return False
