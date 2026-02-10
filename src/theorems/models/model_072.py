"""
Model 72: Line_Point_Slope_Form
点斜式直线方程

公式: y - y₀ = k(x - x₀)
用于: 已知一点和斜率，建立直线方程
"""

import re
from ..base_model import TheoremModel


class LinePointSlopeForm(TheoremModel):
    """
    点斜式直线方程
    
    前置条件:
    - 存在一个点的坐标
    - 存在斜率值（参数中的 k 或 slope，或几何关系中提到斜率）
    
    输出:
    - equations: 点斜式方程 y - y₀ = k(x - x₀)
    - geometric_relations: 直线方程信息
    
    示例:
    输入: P(1, 2), k = 3
    输出: y - 2 = 3(x - 1), 即 y = 3x - 1
    """
    
    def __init__(self):
        super().__init__(
            model_id=72,
            name="Line_Point_Slope_Form",
            chinese_name="点斜式直线方程"
        )
    
    def can_apply(self, state) -> bool:
        """
        检查是否可应用
        
        条件:
        1. 存在至少一个点的坐标
        2. 存在斜率信息（参数k/slope或几何关系中提到斜率）
        """
        # 条件1: 至少有一个点的坐标
        has_point = len(state.coordinates) >= 1
        
        if not has_point:
            return False
        
        # 条件2a: 参数中有斜率
        has_slope_param = any(
            key in ('k', 'slope') or key.startswith('k_')
            for key in state.parameters
        )
        
        if has_slope_param:
            return True
        
        # 条件2b: 几何关系中提到斜率
        for rel in state.geometric_relations:
            if any(kw in rel for kw in ['Slope', 'slope', '斜率', '点斜式']):
                return True
        
        return False
    
    def apply(self, state) -> bool:
        """
        应用模型，建立点斜式直线方程
        """
        try:
            # 添加通用公式
            general_formula = "点斜式直线方程: y - y₀ = k(x - x₀)"
            if general_formula not in state.geometric_relations:
                state.geometric_relations.append(general_formula)
            
            # 获取斜率值
            slope_value = None
            slope_key = None
            for key in ('k', 'slope'):
                if key in state.parameters:
                    slope_value = state.parameters[key]
                    slope_key = key
                    break
            
            # 也尝试从 k_XX 形式的参数中获取斜率
            slope_entries = {}
            for key, val in state.parameters.items():
                if key.startswith('k_') or key == 'k' or key == 'slope':
                    slope_entries[key] = val
            
            # 如果没有参数中的斜率，尝试从几何关系中提取
            if slope_value is None:
                for rel in state.geometric_relations:
                    # 匹配: Slope(l) = k 或 斜率 = k
                    match = re.search(r'[Ss]lope\s*[=(]\s*([^\s,)]+)', rel)
                    if match:
                        slope_value = match.group(1)
                        break
                    match = re.search(r'斜率\s*[=:：]\s*([^\s,]+)', rel)
                    if match:
                        slope_value = match.group(1)
                        break
            
            # 对每个已知坐标点，尝试建立具体方程
            coord_list = list(state.coordinates.items())
            
            if slope_value is not None and len(coord_list) >= 1:
                for point_name, point_coord in coord_list:
                    x0, y0 = point_coord[0], point_coord[1]
                    
                    # 尝试数值计算
                    specific_eq = self._build_equation(x0, y0, slope_value, point_name)
                    if specific_eq is not None:
                        if specific_eq not in state.equations:
                            state.equations.append(specific_eq)
                        
                        rel_str = f"Line through {point_name}({x0}, {y0}) with slope {slope_value}: {specific_eq}"
                        if rel_str not in state.geometric_relations:
                            state.geometric_relations.append(rel_str)
            
            # 如果有多个斜率（如 k_AB），分别处理
            for s_key, s_val in slope_entries.items():
                if s_key.startswith('k_'):
                    suffix = s_key[2:]  # e.g. "AB"
                    # 尝试找到对应的点
                    if len(suffix) >= 1:
                        first_point = suffix[0]
                        if first_point in state.coordinates:
                            x0, y0 = state.coordinates[first_point]
                            eq = self._build_equation(x0, y0, s_val, first_point)
                            if eq is not None and eq not in state.equations:
                                state.equations.append(eq)
            
            # 记录已应用的模型
            state.applied_models.append(self.model_id)
            return True
        
        except Exception:
            return False
    
    def _build_equation(self, x0, y0, slope, point_name="P"):
        """
        构建点斜式方程
        
        Args:
            x0: 点的x坐标
            y0: 点的y坐标
            slope: 斜率值
            point_name: 点名称
        
        Returns:
            str: 方程字符串，失败返回 None
        """
        try:
            x0_f = float(x0)
            y0_f = float(y0)
            k_f = float(slope)
            
            # y - y0 = k(x - x0) => y = kx - k*x0 + y0
            b_val = -k_f * x0_f + y0_f
            
            # 格式化系数
            k_str = self._format_number(k_f)
            b_str = self._format_number(b_val)
            
            # 构造 y = kx + b 形式
            if b_val == 0:
                return f"y = {k_str}*x"
            elif b_val > 0:
                return f"y = {k_str}*x + {b_str}"
            else:
                return f"y = {k_str}*x - {self._format_number(abs(b_val))}"
        except (ValueError, TypeError):
            # 无法转换为数值，返回符号形式
            return f"y - {y0} = {slope}*(x - {x0})"
    
    def _format_number(self, val):
        """格式化数值输出"""
        if val == int(val):
            return str(int(val))
        else:
            return str(round(val, 4))
