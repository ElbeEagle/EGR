"""
Model 63: Basic_Inequality
基本不等式

公式: 
  a + b ≥ 2√(ab) (a, b > 0)
  等号成立条件: a = b
"""

from ..base_model import TheoremModel


class BasicInequality(TheoremModel):
    """
    基本不等式
    
    前置条件:
    - 需要求最值
    - 或有和积关系
    
    输出:
    - geometric_relations: 基本不等式公式
    
    示例:
    已知a + b = 常数，求ab的最大值
    已知ab = 常数，求a + b的最小值
    """
    
    def __init__(self):
        super().__init__(
            model_id=63,
            name="Basic_Inequality",
            chinese_name="基本不等式"
        )
    
    def can_apply(self, state) -> bool:
        """
        检查是否可应用
        
        条件:
        1. 需要求最值
        2. 有不等式相关信息
        """
        # 检查最值关键词
        for rel in state.geometric_relations:
            if any(keyword in rel for keyword in [
                '最大', '最小', 'maximum', 'minimum', 'max', 'min',
                '最值', 'extremum', '最大值', '最小值'
            ]):
                return True
        
        # 检查不等式关键词
        for rel in state.geometric_relations:
            if any(keyword in rel for keyword in [
                '不等式', 'inequality', '≥', '≤', '>=', '<='
            ]):
                return True
        
        # 检查query中是否有最值需求
        # （这里简化处理，实际可能需要更复杂的判断）
        return False
    
    def apply(self, state) -> None:
        """
        应用模型，添加基本不等式
        """
        # 添加基本不等式公式
        formulas = [
            "基本不等式:",
            "  a + b ≥ 2√(ab) (a, b > 0)",
            "  等号成立条件: a = b",
            "",
            "常用变形:",
            "  (a + b)/2 ≥ √(ab) (算术平均 ≥ 几何平均)",
            "  a + b ≥ 2√(ab) ⟺ (√a - √b)² ≥ 0",
        ]
        
        for formula in formulas:
            if formula not in state.geometric_relations:
                state.geometric_relations.append(formula)
        
        # 添加应用技巧
        state.geometric_relations.append(
            "应用场景: 已知和求积的最值，或已知积求和的最值"
        )
        
        # 记录已应用的模型
        state.applied_models.append(self.model_id)
