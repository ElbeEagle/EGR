"""
Model 32: Ellipse_Focal_Triangle_Perimeter
椭圆焦点三角形周长

公式: |PF1| + |PF2| + |F1F2| = 2a + 2c
用于: 计算椭圆上一点与两焦点构成的三角形周长
"""

import re
from ..base_model import TheoremModel


class EllipseFocalTrianglePerimeter(TheoremModel):
    """
    椭圆焦点三角形周长
    
    前置条件:
    - 实体为椭圆
    - 已知参数 a, c
    - 存在焦点三角形
    
    输出:
    - 三角形周长 = 2a + 2c
    
    示例:
    输入: 椭圆 a=5, c=3
    输出: 周长 = 16
    """
    
    def __init__(self):
        super().__init__(
            model_id=32,
            name="Ellipse_Focal_Triangle_Perimeter",
            chinese_name="椭圆焦点三角形周长"
        )
    
    def can_apply(self, state) -> bool:
        """
        检查是否可应用（放宽条件）
        
        条件:
        1. 存在椭圆实体
        2. 已知 a 和 c，或可以计算
        3. 存在焦点三角形相关的描述（放宽）
        """
        # 条件1: 存在椭圆
        has_ellipse = any(
            entity_type.lower() == 'ellipse'
            for entity_type in state.entities.values()
        )
        if not has_ellipse:
            return False
        
        # 条件2: 已知 a 和 c，或可以计算
        has_a = 'a' in state.parameters or 'a^2' in state.parameters
        has_c = 'c' in state.parameters
        has_b = 'b' in state.parameters or 'b^2' in state.parameters
        
        # 如果有 a 和 b，可以计算 c
        if has_a and has_b:
            # 检查是否有焦点或三角形相关信息
            has_focal_info = any(kw in rel for rel in state.geometric_relations
                                for kw in ['Focus', 'Triangle', 'Perimeter', '周长', '焦点'])
            if has_focal_info:
                return True
        
        # 如果有 a 和 c，直接可用
        if has_a and has_c:
            has_focal_info = any(kw in rel for rel in state.geometric_relations
                                for kw in ['Focus', 'Triangle', 'Perimeter', '周长', '焦点'])
            if has_focal_info:
                return True
        
        # 如果只有参数a或b，但明确提到焦点三角形周长
        if has_a or has_b:
            for rel in state.geometric_relations:
                if ('Perimeter' in rel or '周长' in rel) and ('Focus' in rel or '焦点' in rel):
                    return True
        
        return False
    
    def apply(self, state) -> bool:
        """
        应用模型，计算周长
        """
        try:
            a = state.parameters.get('a')
            c = state.parameters.get('c')
        
            # 计算周长: |PF1| + |PF2| + |F1F2| = 2a + 2c
            # 因为 |PF1| + |PF2| = 2a (椭圆定义)
            # |F1F2| = 2c (焦距)
            perimeter = f"2*{a} + 2*{c}"
        
            # 尝试简化
            try:
                a_val = float(a) if isinstance(a, (int, float)) or str(a).replace('.', '').isdigit() else None
                c_val = float(c) if isinstance(c, (int, float)) or str(c).replace('.', '').isdigit() else None
                if a_val and c_val:
                    perimeter = str(2*a_val + 2*c_val)
            except:
                pass
        
            # 添加到参数和关系中
            state.parameters['focal_triangle_perimeter'] = perimeter
            state.geometric_relations.append(f"FocalTrianglePerimeter = {perimeter}")
        
            # 记录已应用的模型
            state.applied_models.append(self.model_id)
            return True

        except Exception:
            return False
