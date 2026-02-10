"""
Model 44: Point_Difference_Method
点差法（椭圆）

用于: 椭圆中点弦问题，利用点差法求弦中点与斜率的关系
公式: 对于椭圆 x²/a² + y²/b² = 1，弦AB中点 M(x₀, y₀)
      k_chord = -b²x₀ / (a²y₀)
"""

import re
from ..base_model import TheoremModel


class PointDifferenceMethod(TheoremModel):
    """
    点差法（椭圆）
    
    前置条件:
    - 存在椭圆或双曲线实体
    - 存在弦中点信息或两个曲线上的点
    - 已知参数 a, b
    
    输出:
    - geometric_relations: 中点-斜率关系
      椭圆: k_chord = -b²x₀/(a²y₀)
      双曲线: k_chord = b²x₀/(a²y₀)
    
    示例:
    输入: 椭圆 x²/4 + y²/3 = 1, 弦中点 M(1, 1)
    输出: k = -3·1/(4·1) = -3/4
    """
    
    def __init__(self):
        super().__init__(
            model_id=44,
            name="Point_Difference_Method",
            chinese_name="点差法"
        )
    
    def can_apply(self, state) -> bool:
        """
        检查是否可应用
        
        条件:
        1. 存在圆锥曲线（椭圆或双曲线）
        2. 存在中点信息或两个曲线上的点
        3. 已知参数 a, b (或 a², b²)
        """
        # 条件1: 存在椭圆或双曲线
        has_conic = any(
            entity_type.lower() in ('ellipse', 'hyperbola')
            for entity_type in state.entities.values()
        )
        if not has_conic:
            return False
        
        # 条件2: 存在中点信息或两个曲线上的点
        has_midpoint = any(
            kw in rel for rel in state.geometric_relations
            for kw in ['MidPoint', 'Midpoint', 'Chord', '中点', '弦']
        )
        
        has_two_points = False
        # 检查是否有两个点在曲线上（例如 A, B 点）
        curve_points = []
        for rel in state.geometric_relations:
            if 'OnCurve' in rel or 'PointOn' in rel or '在曲线上' in rel:
                curve_points.append(rel)
        if len(curve_points) >= 2:
            has_two_points = True
        
        if not has_midpoint and not has_two_points:
            return False
        
        # 条件3: 已知参数 a, b
        has_params = ('a' in state.parameters or 'a^2' in state.parameters) and \
                     ('b' in state.parameters or 'b^2' in state.parameters)
        
        return has_params
    
    def apply(self, state) -> bool:
        """
        应用模型，建立中点-斜率关系
        
        椭圆 x²/a² + y²/b² = 1:
          设 A(x₁,y₁), B(x₂,y₂) 在椭圆上，代入相减得:
          (x₁²-x₂²)/a² + (y₁²-y₂²)/b² = 0
          => (x₁+x₂)(x₁-x₂)/a² + (y₁+y₂)(y₁-y₂)/b² = 0
          => k_AB = (y₁-y₂)/(x₁-x₂) = -b²(x₁+x₂) / (a²(y₁+y₂))
          => k_AB = -b²x₀ / (a²y₀)  (其中 (x₀,y₀) 为中点)
        """
        try:
            # 判断曲线类型
            curve_type = self._get_curve_type(state)
            
            # 获取参数
            a_squared = self._get_a_squared(state)
            b_squared = self._get_b_squared(state)
            
            if curve_type == 'ellipse':
                self._apply_ellipse(state, a_squared, b_squared)
            elif curve_type == 'hyperbola':
                self._apply_hyperbola(state, a_squared, b_squared)
            
            # 记录已应用的模型
            state.applied_models.append(self.model_id)
            return True

        except Exception:
            return False
    
    def _get_curve_type(self, state) -> str:
        """获取曲线类型"""
        for entity_type in state.entities.values():
            if entity_type.lower() == 'ellipse':
                return 'ellipse'
            elif entity_type.lower() == 'hyperbola':
                return 'hyperbola'
        return 'ellipse'  # 默认椭圆
    
    def _get_a_squared(self, state) -> str:
        """获取 a² 的值"""
        if 'a^2' in state.parameters:
            return state.parameters['a^2']
        elif 'a' in state.parameters:
            a_val = state.parameters['a']
            try:
                a_num = float(a_val)
                a_sq = a_num ** 2
                return str(int(a_sq)) if a_sq == int(a_sq) else str(a_sq)
            except (ValueError, TypeError):
                return f"{a_val}^2"
        return 'a^2'
    
    def _get_b_squared(self, state) -> str:
        """获取 b² 的值"""
        if 'b^2' in state.parameters:
            return state.parameters['b^2']
        elif 'b' in state.parameters:
            b_val = state.parameters['b']
            try:
                b_num = float(b_val)
                b_sq = b_num ** 2
                return str(int(b_sq)) if b_sq == int(b_sq) else str(b_sq)
            except (ValueError, TypeError):
                return f"{b_val}^2"
        return 'b^2'
    
    def _apply_ellipse(self, state, a_squared, b_squared):
        """
        椭圆点差法
        
        k_chord = -b²x₀ / (a²y₀)
        """
        # 添加通用公式
        state.geometric_relations.append(
            f"ChordSlopeFormula(Ellipse): k = -{b_squared}·x₀ / ({a_squared}·y₀)"
        )
        state.geometric_relations.append(
            "PointDifferenceMethod(Ellipse): k·k_OM = -b²/a²"
        )
        
        # 如果有中点坐标，计算具体斜率
        midpoint_coord = self._find_midpoint_coord(state)
        if midpoint_coord:
            x0, y0 = midpoint_coord
            try:
                x0_val = float(x0)
                y0_val = float(y0)
                a2_val = float(a_squared)
                b2_val = float(b_squared)
                
                if y0_val != 0 and a2_val != 0:
                    k_val = -b2_val * x0_val / (a2_val * y0_val)
                    
                    k_str = str(int(k_val)) if k_val == int(k_val) else str(round(k_val, 4))
                    state.parameters['k_chord'] = k_str
                    state.geometric_relations.append(
                        f"点差法: k_AB = -{b_squared}·{x0}/({a_squared}·{y0}) = {k_str}"
                    )
            except (ValueError, TypeError):
                # 符号形式
                state.geometric_relations.append(
                    f"点差法: k_AB = -{b_squared}·({x0})/({a_squared}·({y0}))"
                )
    
    def _apply_hyperbola(self, state, a_squared, b_squared):
        """
        双曲线点差法
        
        k_chord = b²x₀ / (a²y₀)  (注意正号，与椭圆相反)
        """
        # 添加通用公式
        state.geometric_relations.append(
            f"ChordSlopeFormula(Hyperbola): k = {b_squared}·x₀ / ({a_squared}·y₀)"
        )
        state.geometric_relations.append(
            "PointDifferenceMethod(Hyperbola): k·k_OM = b²/a²"
        )
        
        # 如果有中点坐标，计算具体斜率
        midpoint_coord = self._find_midpoint_coord(state)
        if midpoint_coord:
            x0, y0 = midpoint_coord
            try:
                x0_val = float(x0)
                y0_val = float(y0)
                a2_val = float(a_squared)
                b2_val = float(b_squared)
                
                if y0_val != 0 and a2_val != 0:
                    k_val = b2_val * x0_val / (a2_val * y0_val)
                    
                    k_str = str(int(k_val)) if k_val == int(k_val) else str(round(k_val, 4))
                    state.parameters['k_chord'] = k_str
                    state.geometric_relations.append(
                        f"点差法: k_AB = {b_squared}·{x0}/({a_squared}·{y0}) = {k_str}"
                    )
            except (ValueError, TypeError):
                # 符号形式
                state.geometric_relations.append(
                    f"点差法: k_AB = {b_squared}·({x0})/({a_squared}·({y0}))"
                )
    
    def _find_midpoint_coord(self, state):
        """
        查找中点坐标
        
        Returns:
            (x0, y0) 或 None
        """
        # 从几何关系中提取中点名称
        midpoint_name = None
        for rel in state.geometric_relations:
            if 'MidPoint' in rel or 'Midpoint' in rel or '中点' in rel:
                # 尝试提取中点名，如 MidPoint(M, A, B) 中的 M
                match = re.search(r'MidPoint\((\w+)', rel)
                if match:
                    midpoint_name = match.group(1)
                    break
                match = re.search(r'Midpoint\((\w+)', rel)
                if match:
                    midpoint_name = match.group(1)
                    break
                # 尝试匹配 "M是AB中点" 或 "中点M"
                match = re.search(r'中点(\w)', rel)
                if match:
                    midpoint_name = match.group(1)
                    break
        
        # 如果找到中点名，从坐标中获取
        if midpoint_name and midpoint_name in state.coordinates:
            coord = state.coordinates[midpoint_name]
            return (coord[0], coord[1])
        
        # 如果参数中有 x0, y0
        if 'x0' in state.parameters and 'y0' in state.parameters:
            return (state.parameters['x0'], state.parameters['y0'])
        
        # 查找常见的中点坐标名
        for name in ['M', 'N', 'P']:
            if name in state.coordinates:
                # 检查该点是否在中点关系中被提及
                for rel in state.geometric_relations:
                    if name in rel and ('MidPoint' in rel or 'Midpoint' in rel or '中点' in rel):
                        coord = state.coordinates[name]
                        return (coord[0], coord[1])
        
        return None
