"""
Model 4: Ellipse_Equation_Standard_Y
椭圆标准方程(焦点在y轴)

从椭圆方程 y²/a² + x²/b² = 1 (a > b > 0) 提取参数 a, b
"""

import re
from ..base_model import TheoremModel


class EllipseEquationStandardY(TheoremModel):
    """
    椭圆标准方程(焦点在y轴)
    
    前置条件:
    - 实体包含 Ellipse 类型
    - 方程形式为 y²/a² + x²/b² = 1
    
    输出:
    - parameters: a, b, a^2, b^2
    - 标注: 焦点在y轴
    
    示例:
    输入: y^2/9 + x^2/4 = 1
    输出: a=3, b=2, a^2=9, b^2=4
    """
    
    def __init__(self):
        super().__init__(
            model_id=4,
            name="Ellipse_Equation_Standard_Y",
            chinese_name="椭圆标准方程(焦点在y轴)"
        )
    
    def can_apply(self, state) -> bool:
        """
        检查是否可应用
        
        条件:
        1. 存在 Ellipse 实体
        2. 方程中有 y^2 和 x^2 项，且系数都为正
        3. 焦点在y轴（y²项系数较大）
        """
        # 条件1: 检查是否有椭圆实体
        has_ellipse = any(
            entity_type.lower() == 'ellipse'
            for entity_type in state.entities.values()
        )
        if not has_ellipse:
            return False
        
        # 条件2: 检查方程
        for eq in state.equations:
            # 匹配 y^2/a^2 + x^2/b^2 = 1 形式
            if 'y^2' in eq and 'x^2' in eq and '=' in eq:
                # 检查是否是加号（椭圆），不是减号（双曲线）
                if '+' in eq:
                    # 尝试提取系数，判断焦点位置
                    y_coef, x_coef = self._extract_coefficients(eq)
                    if y_coef and x_coef:
                        # 焦点在y轴：y²项系数较大（分母较大）
                        try:
                            y_val = float(y_coef)
                            x_val = float(x_coef)
                            if y_val > x_val:  # y²的分母更大
                                return True
                        except:
                            # 如果无法比较，检查是否有其他信息
                            pass
        
        return False
    
    def apply(self, state) -> None:
        """
        应用模型，提取椭圆参数
        """
        for eq in state.equations:
            if 'y^2' in eq and 'x^2' in eq and '+' in eq:
                y_coef, x_coef = self._extract_coefficients(eq)
                
                if y_coef and x_coef:
                    # a² 对应 y² 的分母，b² 对应 x² 的分母
                    state.parameters['a^2'] = y_coef
                    state.parameters['b^2'] = x_coef
                    
                    # 尝试计算 a 和 b
                    try:
                        a_sq = float(y_coef)
                        b_sq = float(x_coef)
                        
                        a_val = a_sq ** 0.5
                        b_val = b_sq ** 0.5
                        
                        if a_val == int(a_val):
                            state.parameters['a'] = str(int(a_val))
                        else:
                            state.parameters['a'] = str(a_val)
                        
                        if b_val == int(b_val):
                            state.parameters['b'] = str(int(b_val))
                        else:
                            state.parameters['b'] = str(b_val)
                    except:
                        # 符号形式
                        state.parameters['a'] = f"sqrt({y_coef})"
                        state.parameters['b'] = f"sqrt({x_coef})"
                    
                    # 添加几何关系
                    state.geometric_relations.append("椭圆焦点在y轴")
                    
                    break
        
        # 记录已应用的模型
        state.applied_models.append(self.model_id)
    
    def _extract_coefficients(self, eq: str):
        """
        从方程中提取 y² 和 x² 的系数（分母）
        
        Returns:
            (y_coef, x_coef): y²和x²的分母
        """
        # 匹配形式: y^2/a^2 + x^2/b^2 = 1
        patterns = [
            # y^2/9 + x^2/4 = 1
            r'y\^2/(\d+\.?\d*)\s*\+\s*x\^2/(\d+\.?\d*)\s*=',
            # y^2/a^2 + x^2/b^2 = 1
            r'y\^2/([a-zA-Z]\^2)\s*\+\s*x\^2/([a-zA-Z]\^2)\s*=',
            # 变量形式
            r'y\^2/(\w+)\s*\+\s*x\^2/(\w+)\s*=',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, eq)
            if match:
                y_coef = match.group(1)
                x_coef = match.group(2)
                return y_coef, x_coef
        
        return None, None
