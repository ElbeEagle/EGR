"""
StateConstructor - 状态构造器

负责构建和更新双层状态表示
"""

import re
from typing import Tuple, Optional, TYPE_CHECKING
from .symbolic_state import SymbolicState
from .abstract_state import AbstractState, CurveType, QueryType
from .equation_normalizer import EquationNormalizer

if TYPE_CHECKING:
    from ..theorems.theorem_library import TheoremLibrary


class StateConstructor:
    """
    状态构造器
    
    功能：
    1. 从 fact_expressions 构建初始状态
    2. 从 SymbolicState 提取 AbstractState
    3. 估计完整度得分
    4. 🆕 自动提取方程参数（标准方程模型）
    """
    
    def __init__(self, theorem_library: Optional['TheoremLibrary'] = None):
        """
        初始化构造器
        
        Args:
            theorem_library: 定理库（用于自动参数提取）
        """
        self.theorem_library = theorem_library
        self.equation_normalizer = EquationNormalizer()
    
    def construct_from_facts(
        self,
        fact_expressions: str,
        query_expressions: str,
        reasoning_depth: int = 0
    ) -> Tuple[AbstractState, SymbolicState]:
        """
        从 fact_expressions 构建初始状态
        
        Args:
            fact_expressions: 题目事实表达式
            query_expressions: 查询表达式
            reasoning_depth: 推理深度（默认0）
        
        Returns:
            Tuple[AbstractState, SymbolicState]: (抽象状态, 符号状态)
        """
        # 🆕 步骤0: 方程标准化
        normalized_facts = self.equation_normalizer.normalize_fact_expressions(fact_expressions)
        
        # 步骤1: 解析 fact_expressions
        symbolic_state = self._parse_fact_expressions(normalized_facts)
        
        # 🆕 步骤2: 自动提取方程参数
        if self.theorem_library:
            self._extract_equation_parameters(symbolic_state)
        
        # 步骤3: 提取抽象特征
        abstract_state = self._construct_abstract_features(
            symbolic_state,
            query_expressions,
            reasoning_depth
        )
        
        return abstract_state, symbolic_state
    
    def construct_from_symbolic_state(
        self,
        symbolic_state: SymbolicState,
        query_expressions: str,
        reasoning_depth: int
    ) -> AbstractState:
        """
        从 SymbolicState 重新构建 AbstractState
        
        用于模型应用后更新状态
        
        Args:
            symbolic_state: 符号状态
            query_expressions: 查询表达式
            reasoning_depth: 推理深度
        
        Returns:
            AbstractState: 抽象状态
        """
        return self._construct_abstract_features(
            symbolic_state,
            query_expressions,
            reasoning_depth
        )
    
    def update_abstract_state(
        self,
        symbolic_state: SymbolicState,
        old_abstract_state: AbstractState
    ) -> AbstractState:
        """
        更新抽象状态（推理引擎用的便利方法）
        
        从修改后的 SymbolicState 重新构建 AbstractState，
        自动递增推理深度。
        
        Args:
            symbolic_state: 更新后的符号状态
            old_abstract_state: 旧的抽象状态（用于获取query和depth）
        
        Returns:
            AbstractState: 新的抽象状态
        """
        # 从旧状态获取query信息（通过重新分类query_type反推）
        # 直接用旧的abstract_state来获取深度
        new_depth = old_abstract_state.reasoning_depth + 1
        
        # 我们需要query_expressions，但旧的abstract_state没有存储
        # 所以用一个通用的query来构建（query_type已经被计算好了）
        # 这里直接重新构建抽象特征
        new_abstract = AbstractState()
        
        # 复制曲线类型
        new_abstract.curve_type = self._extract_curve_type(symbolic_state)
        
        # 保留旧的query_type
        new_abstract.query_type = old_abstract_state.query_type
        
        # 更新信息特征
        new_abstract.has_equation = len(symbolic_state.equations) > 0
        new_abstract.has_parameters = set(symbolic_state.parameters.keys())
        new_abstract.has_focus_info = self._check_has_focus(symbolic_state)
        new_abstract.has_vertex_info = self._check_has_vertex(symbolic_state)
        new_abstract.has_point_on_curve = self._check_has_point_on_curve(symbolic_state)
        new_abstract.has_asymptote_info = self._check_has_asymptote(symbolic_state)
        new_abstract.has_directrix_info = self._check_has_directrix(symbolic_state)
        new_abstract.has_tangent_info = self._check_has_tangent(symbolic_state)
        new_abstract.has_distance_constraint = self._check_has_distance(symbolic_state)
        new_abstract.has_angle_constraint = self._check_has_angle(symbolic_state)
        new_abstract.has_perpendicular = self._check_has_perpendicular(symbolic_state)
        
        # 更新完整度（启发式估计）
        score = 0.0
        if len(symbolic_state.equations) > 0:
            score += 0.3
        param_count = len(symbolic_state.parameters)
        score += min(param_count * 0.1, 0.4)
        if len(symbolic_state.geometric_relations) > 0:
            score += 0.1
        # 根据query_type判断是否有相关信息
        if self._has_query_related_info(symbolic_state, new_abstract.query_type):
            score += 0.2
        new_abstract.completeness_score = min(score, 1.0)
        
        # 更新深度
        new_abstract.reasoning_depth = new_depth
        
        return new_abstract
    
    def _parse_fact_expressions(self, fact_expressions: str) -> SymbolicState:
        """
        解析 fact_expressions 字符串
        
        输入格式：
        "G: Hyperbola;m: Number;m>0;Expression(G) = (x^2/4 - y^2/m^2 = 1)"
        
        解析规则：
        1. 按分号分割成单个 fact
        2. 识别 fact 类型（实体声明、方程、关系、约束）
        3. 分配到对应字段
        
        Args:
            fact_expressions: 事实表达式字符串
        
        Returns:
            SymbolicState: 解析后的符号状态
        """
        state = SymbolicState()
        
        # 分割 facts
        facts = fact_expressions.split(';')
        
        for fact in facts:
            fact = fact.strip()
            if not fact:
                continue
            
            # 类型1: 实体声明 "G: Hyperbola"
            if re.match(r'^(\w+):\s*(\w+)$', fact):
                match = re.match(r'^(\w+):\s*(\w+)$', fact)
                name, type_ = match.groups()
                state.entities[name] = type_
            
            # 类型2: 方程 "Expression(...) = ..."
            elif 'Expression' in fact and '=' in fact:
                state.equations.append(fact)
            
            # 类型3: 坐标 "Coordinate(A) = (1, 2)"
            elif 'Coordinate' in fact:
                match = re.match(r'Coordinate\((\w+)\)\s*=\s*\(([^)]+)\)', fact)
                if match:
                    point_name = match.group(1)
                    coords_str = match.group(2)
                    coords = tuple(c.strip() for c in coords_str.split(','))
                    state.coordinates[point_name] = coords
                else:
                    state.geometric_relations.append(fact)
            
            # 类型4: 几何关系（各种函数调用）
            elif any(kw in fact for kw in [
                'Distance', 'IsPerpendicular', 'IsTangent', 'Intersection',
                'PointOnCurve', 'Focus', 'Vertex', 'Asymptote', 'Directrix',
                'LeftFocus', 'RightFocus', 'UpperVertex', 'LowerVertex',
                'Center', 'Radius', 'MidPoint', 'Slope', 'Length',
                'Eccentricity', 'Area', 'Perimeter', 'Angle', 'IsChordOf'
            ]):
                state.geometric_relations.append(fact)
            
            # 类型5: 约束条件 "m > 0"
            elif any(op in fact for op in ['>', '<', '>=', '<=', '!=']):
                state.constraints.append(fact)
        
        return state
    
    def _extract_equation_parameters(self, symbolic_state: SymbolicState) -> None:
        """
        🆕 从方程中自动提取参数
        
        自动应用标准方程模型 (3-10)：
        - Model 3: 椭圆标准方程(焦点在x轴)
        - Model 4: 椭圆标准方程(焦点在y轴)
        - Model 5: 双曲线标准方程(焦点在x轴)
        - Model 6: 双曲线标准方程(焦点在y轴)
        - Model 7: 抛物线标准方程(开口向右)
        - Model 8: 抛物线标准方程(开口向左)
        - Model 9: 抛物线标准方程(开口向上)
        - Model 10: 抛物线标准方程(开口向下)
        
        这些模型会在初始化时自动执行，提取基本参数。
        
        Args:
            symbolic_state: 符号状态（会被直接修改）
        """
        if not self.theorem_library:
            return
        
        # 标准方程模型ID列表
        standard_equation_models = [3, 4, 5, 6, 7, 8, 9, 10]
        
        # 尝试应用每个标准方程模型
        for model_id in standard_equation_models:
            model = self.theorem_library.models.get(model_id)
            
            # 跳过未实现的模型
            if not model:
                continue
            
            # 检查前置条件
            if not model.can_apply(symbolic_state):
                continue
            
            # 应用模型
            try:
                model.apply(symbolic_state)
                # 只应用第一个匹配的模型，避免冲突
                break
            except Exception as e:
                # 如果应用失败，继续尝试下一个模型
                continue
    
    def _construct_abstract_features(
        self,
        symbolic_state: SymbolicState,
        query_expressions: str,
        reasoning_depth: int
    ) -> AbstractState:
        """
        从符号状态构建抽象特征
        
        Args:
            symbolic_state: 符号状态
            query_expressions: 查询表达式
            reasoning_depth: 推理深度
        
        Returns:
            AbstractState: 抽象状态
        """
        abstract_state = AbstractState()
        
        # 特征1: 曲线类型
        abstract_state.curve_type = self._extract_curve_type(symbolic_state)
        
        # 特征2: 查询类型
        abstract_state.query_type = self._classify_query(query_expressions)
        
        # 特征3-13: 信息特征
        abstract_state.has_equation = len(symbolic_state.equations) > 0
        abstract_state.has_parameters = set(symbolic_state.parameters.keys())
        abstract_state.has_focus_info = self._check_has_focus(symbolic_state)
        abstract_state.has_vertex_info = self._check_has_vertex(symbolic_state)
        abstract_state.has_point_on_curve = self._check_has_point_on_curve(symbolic_state)
        abstract_state.has_asymptote_info = self._check_has_asymptote(symbolic_state)
        abstract_state.has_directrix_info = self._check_has_directrix(symbolic_state)
        abstract_state.has_tangent_info = self._check_has_tangent(symbolic_state)
        abstract_state.has_distance_constraint = self._check_has_distance(symbolic_state)
        abstract_state.has_angle_constraint = self._check_has_angle(symbolic_state)
        abstract_state.has_perpendicular = self._check_has_perpendicular(symbolic_state)
        
        # 特征14: 完整度
        abstract_state.completeness_score = self._estimate_completeness(
            symbolic_state,
            query_expressions
        )
        
        # 特征15: 深度
        abstract_state.reasoning_depth = reasoning_depth
        
        return abstract_state
    
    def _extract_curve_type(self, symbolic_state: SymbolicState) -> CurveType:
        """提取曲线类型"""
        for type_ in symbolic_state.entities.values():
            type_lower = type_.lower()
            if type_lower in ['ellipse']:
                return CurveType.ELLIPSE
            elif type_lower in ['hyperbola']:
                return CurveType.HYPERBOLA
            elif type_lower in ['parabola']:
                return CurveType.PARABOLA
            elif type_lower in ['circle']:
                return CurveType.CIRCLE
        return CurveType.UNKNOWN
    
    def _classify_query(self, query_expressions: str) -> QueryType:
        """分类查询类型"""
        query_lower = query_expressions.lower()
        
        if 'eccentricity' in query_lower:
            return QueryType.ECCENTRICITY
        elif 'equation' in query_lower or 'expression' in query_lower:
            return QueryType.EQUATION
        elif 'coordinate' in query_lower:
            return QueryType.COORDINATE
        elif 'distance' in query_lower:
            return QueryType.DISTANCE
        elif 'length' in query_lower:
            return QueryType.LENGTH
        elif 'range' in query_lower:
            return QueryType.RANGE
        elif 'angle' in query_lower:
            return QueryType.ANGLE
        elif 'area' in query_lower:
            return QueryType.AREA
        else:
            return QueryType.VALUE
    
    def _check_has_focus(self, symbolic_state: SymbolicState) -> bool:
        """检查是否有焦点信息"""
        # 方法1: 从方程中查找
        for eq in symbolic_state.equations:
            if 'Focus' in eq:
                return True
        
        # 方法2: 从几何关系中查找
        for rel in symbolic_state.geometric_relations:
            if 'Focus' in rel:
                return True
        
        return False
    
    def _check_has_vertex(self, symbolic_state: SymbolicState) -> bool:
        """检查是否有顶点信息"""
        for rel in symbolic_state.geometric_relations:
            if 'Vertex' in rel:
                return True
        return False
    
    def _check_has_point_on_curve(self, symbolic_state: SymbolicState) -> bool:
        """检查是否有曲线上的点"""
        for rel in symbolic_state.geometric_relations:
            if 'PointOnCurve' in rel:
                return True
        return False
    
    def _check_has_asymptote(self, symbolic_state: SymbolicState) -> bool:
        """检查是否有渐近线信息"""
        for eq in symbolic_state.equations:
            if 'Asymptote' in eq:
                return True
        for rel in symbolic_state.geometric_relations:
            if 'Asymptote' in rel or '渐近线' in rel:
                return True
        return False
    
    def _check_has_directrix(self, symbolic_state: SymbolicState) -> bool:
        """检查是否有准线信息"""
        for rel in symbolic_state.geometric_relations:
            if 'Directrix' in rel or '准线' in rel:
                return True
        return False
    
    def _check_has_tangent(self, symbolic_state: SymbolicState) -> bool:
        """检查是否有切线信息"""
        for rel in symbolic_state.geometric_relations:
            if 'Tangent' in rel or '切线' in rel:
                return True
        return False
    
    def _check_has_distance(self, symbolic_state: SymbolicState) -> bool:
        """检查是否有距离约束"""
        for rel in symbolic_state.geometric_relations:
            if 'Distance' in rel:
                return True
        return False
    
    def _check_has_angle(self, symbolic_state: SymbolicState) -> bool:
        """检查是否有角度约束"""
        for rel in symbolic_state.geometric_relations:
            if 'Angle' in rel:
                return True
        return False
    
    def _check_has_perpendicular(self, symbolic_state: SymbolicState) -> bool:
        """检查是否有垂直关系"""
        for rel in symbolic_state.geometric_relations:
            if 'IsPerpendicular' in rel or 'Perpendicular' in rel:
                return True
        return False
    
    def _estimate_completeness(
        self,
        symbolic_state: SymbolicState,
        query_expressions: str
    ) -> float:
        """
        估计信息完整度
        
        核心思想：根据启发式规则评分
        
        评分规则：
        1. 有方程 → +0.3
        2. 每个已知参数 → +0.1 (最多+0.4)
        3. 有查询相关的关键信息 → +0.2
        4. 有几何关系 → +0.1
        
        总分：min(各项之和, 1.0)
        
        Args:
            symbolic_state: 符号状态
            query_expressions: 查询表达式
        
        Returns:
            float: 完整度得分 (0.0-1.0)
        """
        score = 0.0
        
        # 规则1: 有方程
        if len(symbolic_state.equations) > 0:
            score += 0.3
        
        # 规则2: 已知参数
        param_count = len(symbolic_state.parameters)
        score += min(param_count * 0.1, 0.4)
        
        # 规则3: 查询相关信息
        query_type = self._classify_query(query_expressions)
        if self._has_query_related_info(symbolic_state, query_type):
            score += 0.2
        
        # 规则4: 几何关系
        if len(symbolic_state.geometric_relations) > 0:
            score += 0.1
        
        return min(score, 1.0)
    
    def _has_query_related_info(
        self,
        state: SymbolicState,
        query_type: QueryType
    ) -> bool:
        """
        判断是否有查询相关的关键信息
        
        Args:
            state: 符号状态
            query_type: 查询类型
        
        Returns:
            bool: 是否有相关信息
        """
        params = state.parameters.keys()
        
        if query_type == QueryType.ECCENTRICITY:
            # 求离心率：需要 c 和 a，或 a 和 b
            return ('c' in params and 'a' in params) or \
                   ('a' in params and 'b' in params) or \
                   'e' in params
        
        elif query_type == QueryType.EQUATION:
            # 求方程：需要足够的参数
            return len(state.parameters) >= 2
        
        elif query_type == QueryType.COORDINATE:
            # 求坐标：需要相关点的信息
            return len(state.coordinates) > 0 or \
                   any('Coordinate' in rel for rel in state.geometric_relations)
        
        elif query_type == QueryType.LENGTH:
            # 求长度（长轴长、虚轴长等）：需要a或b
            return 'a' in params or 'b' in params
        
        elif query_type == QueryType.DISTANCE:
            # 求距离：需要坐标信息或c
            return len(state.coordinates) >= 1 or 'c' in params
        
        elif query_type == QueryType.AREA:
            # 求面积：需要多个参数
            return len(state.parameters) >= 2
        
        elif query_type == QueryType.VALUE:
            # 求值：查看是否有未知量的值
            return len(state.parameters) >= 1
        
        elif query_type == QueryType.ANGLE:
            # 求角度：需要角度关系
            return any('Angle' in rel for rel in state.geometric_relations) or \
                   any('angle' in rel for rel in state.geometric_relations)
        
        elif query_type == QueryType.RANGE:
            # 求范围：需要参数和约束
            return len(state.parameters) >= 1 and len(state.constraints) >= 1
        
        return False
