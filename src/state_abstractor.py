"""
状态抽象器 - 将复杂的fact_expressions抽象为结构化状态

核心设计思想：
1. 双层状态表示：粗粒度抽象（用于状态聚类） + 细粒度符号状态（用于推理）
2. 状态可累积：应用模型后可以增量更新状态
3. 可哈希：用于状态索引和去重
"""

from typing import Dict, List, Set, Tuple, Optional, Any
from dataclasses import dataclass, field
from enum import Enum
import re
import hashlib
import json


class CurveType(Enum):
    """曲线类型枚举"""
    ELLIPSE = "Ellipse"
    HYPERBOLA = "Hyperbola"
    PARABOLA = "Parabola"
    CIRCLE = "Circle"
    UNKNOWN = "Unknown"


class QueryType(Enum):
    """查询目标类型枚举"""
    ECCENTRICITY = "eccentricity"      # 求离心率
    EQUATION = "equation"              # 求方程
    COORDINATE = "coordinate"          # 求坐标
    DISTANCE = "distance"              # 求距离
    LENGTH = "length"                  # 求长度
    RANGE = "range"                    # 求范围
    VALUE = "value"                    # 求参数值
    ANGLE = "angle"                    # 求角度
    AREA = "area"                      # 求面积
    EXPRESSION = "expression"          # 求表达式
    OTHER = "other"


@dataclass
class SymbolicState:
    """
    细粒度符号状态（用于精确推理）
    
    存储所有已知的具体信息，支持符号推理
    """
    # 实体声明（变量、点、曲线等）
    entities: Dict[str, str] = field(default_factory=dict)  # {name: type}
    # 例如: {'G': 'Hyperbola', 'm': 'Number', 'A': 'Point'}
    
    # 方程/表达式
    equations: List[str] = field(default_factory=list)
    # 例如: ['Expression(G) = (x^2/4 - y^2/m^2 = 1)', ...]
    
    # 参数值（已求出的具体值或关系）
    parameters: Dict[str, Any] = field(default_factory=dict)
    # 例如: {'a': 2, 'b': 'm', 'c': 'sqrt(a^2 + b^2)'}
    
    # 几何关系
    geometric_relations: List[str] = field(default_factory=list)
    # 例如: ['IsPerpendicular(AB, xAxis)', 'Distance(F, Asymptote) = b']
    
    # 坐标信息
    coordinates: Dict[str, Tuple] = field(default_factory=dict)
    # 例如: {'F': ('c', 0), 'A': (1, 1/4)}
    
    # 约束条件
    constraints: List[str] = field(default_factory=list)
    # 例如: ['m > 0', 'a > b', 'b > 0']
    
    def add_fact(self, fact: str):
        """添加一个新的fact到状态中"""
        # 解析fact类型并存储到对应字段
        if 'Expression' in fact and '=' in fact:
            self.equations.append(fact)
        elif any(rel in fact for rel in ['IsPerpendicular', 'Distance', 'IsTangent', 'Intersection']):
            self.geometric_relations.append(fact)
        elif 'Coordinate' in fact:
            # 解析坐标
            match = re.match(r'(\w+):\s*\w+.*Coordinate\(\1\)\s*=\s*\(([^)]+)\)', fact)
            if match:
                name, coords = match.groups()
                self.coordinates[name] = tuple(coords.split(','))
        elif re.match(r'(\w+):\s*(\w+)', fact):
            # 实体声明
            match = re.match(r'(\w+):\s*(\w+)', fact)
            if match:
                name, entity_type = match.groups()
                self.entities[name] = entity_type
        elif '>' in fact or '<' in fact or '=' in fact:
            # 约束条件
            self.constraints.append(fact)
    
    def copy(self):
        """深拷贝状态"""
        return SymbolicState(
            entities=self.entities.copy(),
            equations=self.equations.copy(),
            parameters=self.parameters.copy(),
            geometric_relations=self.geometric_relations.copy(),
            coordinates=self.coordinates.copy(),
            constraints=self.constraints.copy()
        )


@dataclass
class AbstractState:
    """
    粗粒度抽象状态（用于状态聚类和模型选择）
    
    将复杂的符号状态抽象为有限的离散状态空间
    """
    # 维度1: 曲线类型（4种）
    curve_type: CurveType = CurveType.UNKNOWN
    
    # 维度2: 查询目标类型（10种）
    query_type: QueryType = QueryType.OTHER
    
    # 维度3: 已知信息的类别（位向量表示）
    has_equation: bool = False           # 是否有曲线方程
    has_parameters: Set[str] = field(default_factory=set)  # 已知参数 {a, b, c, e, m, ...}
    has_focus_info: bool = False         # 是否有焦点信息
    has_vertex_info: bool = False        # 是否有顶点信息
    has_point_on_curve: bool = False     # 是否有曲线上的点
    has_asymptote_info: bool = False     # 是否有渐近线信息
    has_directrix_info: bool = False     # 是否有准线信息
    has_tangent_info: bool = False       # 是否有切线信息
    has_distance_constraint: bool = False  # 是否有距离约束
    has_angle_constraint: bool = False     # 是否有角度约束
    has_perpendicular: bool = False        # 是否有垂直关系
    
    # 维度4: 信息完整度（0.0-1.0，离散化为5个等级）
    completeness_score: float = 0.0
    
    # 维度5: 推理深度（当前是第几步）
    reasoning_depth: int = 0
    
    def to_vector(self) -> List[float]:
        """
        转换为特征向量（用于神经网络输入）
        
        返回：长度为~30的特征向量
        """
        vector = []
        
        # 1. 曲线类型 one-hot (4维)
        curve_one_hot = [0.0] * 5
        curve_types = list(CurveType)
        if self.curve_type in curve_types:
            curve_one_hot[curve_types.index(self.curve_type)] = 1.0
        vector.extend(curve_one_hot)
        
        # 2. 查询类型 one-hot (11维)
        query_one_hot = [0.0] * 11
        query_types = list(QueryType)
        if self.query_type in query_types:
            query_one_hot[query_types.index(self.query_type)] = 1.0
        vector.extend(query_one_hot)
        
        # 3. 已知信息位向量 (11维)
        vector.extend([
            float(self.has_equation),
            float(self.has_focus_info),
            float(self.has_vertex_info),
            float(self.has_point_on_curve),
            float(self.has_asymptote_info),
            float(self.has_directrix_info),
            float(self.has_tangent_info),
            float(self.has_distance_constraint),
            float(self.has_angle_constraint),
            float(self.has_perpendicular),
            float(len(self.has_parameters)) / 10.0  # 归一化参数个数
        ])
        
        # 4. 完整度和深度 (2维)
        vector.extend([
            self.completeness_score,
            min(self.reasoning_depth / 10.0, 1.0)  # 归一化深度
        ])
        
        return vector
    
    def to_hash(self) -> str:
        """
        计算状态哈希（用于状态索引）
        
        注意：不包含reasoning_depth，因为我们希望相同信息状态有相同哈希
        """
        state_dict = {
            'curve_type': self.curve_type.value,
            'query_type': self.query_type.value,
            'has_equation': self.has_equation,
            'has_parameters': sorted(list(self.has_parameters)),
            'has_focus_info': self.has_focus_info,
            'has_vertex_info': self.has_vertex_info,
            'has_point_on_curve': self.has_point_on_curve,
            'has_asymptote_info': self.has_asymptote_info,
            'has_directrix_info': self.has_directrix_info,
            'has_tangent_info': self.has_tangent_info,
            'has_distance_constraint': self.has_distance_constraint,
            'has_angle_constraint': self.has_angle_constraint,
            'has_perpendicular': self.has_perpendicular,
            'completeness_level': round(self.completeness_score * 4) / 4  # 离散化到0.25
        }
        
        state_str = json.dumps(state_dict, sort_keys=True)
        return hashlib.md5(state_str.encode()).hexdigest()
    
    def __repr__(self):
        params_str = ', '.join(sorted(self.has_parameters)) if self.has_parameters else 'none'
        return (f"AbstractState(curve={self.curve_type.value}, "
                f"query={self.query_type.value}, "
                f"params=[{params_str}], "
                f"completeness={self.completeness_score:.2f}, "
                f"depth={self.reasoning_depth})")


class StateAbstractor:
    """
    状态抽象器：将fact_expressions抽象为双层状态表示
    """
    
    def __init__(self):
        pass
    
    def parse_fact_expressions(self, fact_expressions: str) -> SymbolicState:
        """
        解析fact_expressions字符串，构建符号状态
        
        Args:
            fact_expressions: 形如 "G: Hyperbola;m: Number;m>0;Expression(G)=..."
        
        Returns:
            SymbolicState对象
        """
        symbolic_state = SymbolicState()
        
        # 按分号分割facts
        facts = fact_expressions.split(';')
        
        for fact in facts:
            fact = fact.strip()
            if fact:
                symbolic_state.add_fact(fact)
        
        return symbolic_state
    
    def abstract_from_facts(
        self, 
        fact_expressions: str, 
        query_expressions: str,
        reasoning_depth: int = 0
    ) -> Tuple[AbstractState, SymbolicState]:
        """
        从fact_expressions和query_expressions抽象出状态
        
        Args:
            fact_expressions: 事实表达式
            query_expressions: 查询表达式
            reasoning_depth: 当前推理深度（第几步）
        
        Returns:
            (AbstractState, SymbolicState) 元组
        """
        # 1. 构建符号状态
        symbolic_state = self.parse_fact_expressions(fact_expressions)
        
        # 2. 从符号状态提取抽象特征
        abstract_state = AbstractState()
        
        # 提取曲线类型
        abstract_state.curve_type = self._extract_curve_type(symbolic_state)
        
        # 提取查询类型
        abstract_state.query_type = self._classify_query(query_expressions)
        
        # 提取已知信息
        abstract_state.has_equation = self._check_has_equation(symbolic_state)
        abstract_state.has_parameters = self._extract_known_parameters(symbolic_state)
        abstract_state.has_focus_info = self._check_has_focus(symbolic_state)
        abstract_state.has_vertex_info = self._check_has_vertex(symbolic_state)
        abstract_state.has_point_on_curve = self._check_has_point_on_curve(symbolic_state)
        abstract_state.has_asymptote_info = self._check_has_asymptote(symbolic_state)
        abstract_state.has_directrix_info = self._check_has_directrix(symbolic_state)
        abstract_state.has_tangent_info = self._check_has_tangent(symbolic_state)
        abstract_state.has_distance_constraint = self._check_has_distance(symbolic_state)
        abstract_state.has_angle_constraint = self._check_has_angle(symbolic_state)
        abstract_state.has_perpendicular = self._check_has_perpendicular(symbolic_state)
        
        # 估计信息完整度
        abstract_state.completeness_score = self._estimate_completeness(
            symbolic_state, 
            query_expressions
        )
        
        # 设置推理深度
        abstract_state.reasoning_depth = reasoning_depth
        
        return abstract_state, symbolic_state
    
    def _extract_curve_type(self, symbolic_state: SymbolicState) -> CurveType:
        """从符号状态中提取曲线类型"""
        for entity_type in symbolic_state.entities.values():
            if entity_type in ['Ellipse', 'ELLIPSE', 'ellipse']:
                return CurveType.ELLIPSE
            elif entity_type in ['Hyperbola', 'HYPERBOLA', 'hyperbola']:
                return CurveType.HYPERBOLA
            elif entity_type in ['Parabola', 'PARABOLA', 'parabola']:
                return CurveType.PARABOLA
            elif entity_type in ['Circle', 'CIRCLE', 'circle']:
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
            # 默认是求值
            return QueryType.VALUE
    
    def _check_has_equation(self, symbolic_state: SymbolicState) -> bool:
        """检查是否有方程"""
        return len(symbolic_state.equations) > 0
    
    def _extract_known_parameters(self, symbolic_state: SymbolicState) -> Set[str]:
        """提取已知参数集合"""
        params = set()
        
        # 从方程中提取参数
        for eq in symbolic_state.equations:
            # 匹配形如 x^2/a^2 的模式
            matches = re.findall(r'/([a-z])[\^²]?[²2]?', eq)
            params.update(matches)
        
        # 从参数字典中提取
        params.update(symbolic_state.parameters.keys())
        
        return params
    
    def _check_has_focus(self, symbolic_state: SymbolicState) -> bool:
        """检查是否有焦点信息"""
        return any('Focus' in rel for rel in symbolic_state.geometric_relations + symbolic_state.equations)
    
    def _check_has_vertex(self, symbolic_state: SymbolicState) -> bool:
        """检查是否有顶点信息"""
        return any('Vertex' in rel for rel in symbolic_state.geometric_relations)
    
    def _check_has_point_on_curve(self, symbolic_state: SymbolicState) -> bool:
        """检查是否有曲线上的点"""
        return any('PointOnCurve' in rel for rel in symbolic_state.geometric_relations)
    
    def _check_has_asymptote(self, symbolic_state: SymbolicState) -> bool:
        """检查是否有渐近线信息"""
        return any('Asymptote' in rel for rel in symbolic_state.geometric_relations + symbolic_state.equations)
    
    def _check_has_directrix(self, symbolic_state: SymbolicState) -> bool:
        """检查是否有准线信息"""
        return any('Directrix' in rel for rel in symbolic_state.geometric_relations)
    
    def _check_has_tangent(self, symbolic_state: SymbolicState) -> bool:
        """检查是否有切线信息"""
        return any('Tangent' in rel for rel in symbolic_state.geometric_relations)
    
    def _check_has_distance(self, symbolic_state: SymbolicState) -> bool:
        """检查是否有距离约束"""
        return any('Distance' in rel for rel in symbolic_state.geometric_relations)
    
    def _check_has_angle(self, symbolic_state: SymbolicState) -> bool:
        """检查是否有角度约束"""
        return any('Angle' in rel or 'angle' in rel for rel in symbolic_state.geometric_relations)
    
    def _check_has_perpendicular(self, symbolic_state: SymbolicState) -> bool:
        """检查是否有垂直关系"""
        return any('Perpendicular' in rel for rel in symbolic_state.geometric_relations)
    
    def _estimate_completeness(
        self, 
        symbolic_state: SymbolicState, 
        query_expressions: str
    ) -> float:
        """
        估计信息完整度（0.0-1.0）
        
        启发式规则：
        - 有方程 → +0.3
        - 每个已知参数 → +0.1
        - 有查询相关的直接信息 → +0.3
        - 有几何关系 → +0.1
        """
        score = 0.0
        
        # 1. 有方程 → +0.3
        if self._check_has_equation(symbolic_state):
            score += 0.3
        
        # 2. 已知参数个数（最多+0.4）
        params_count = len(self._extract_known_parameters(symbolic_state))
        score += min(params_count * 0.1, 0.4)
        
        # 3. 查询相关信息（+0.2）
        if self._has_query_related_info(symbolic_state, query_expressions):
            score += 0.2
        
        # 4. 几何关系（+0.1）
        if len(symbolic_state.geometric_relations) > 0:
            score += 0.1
        
        return min(score, 1.0)
    
    def _has_query_related_info(
        self, 
        symbolic_state: SymbolicState, 
        query_expressions: str
    ) -> bool:
        """判断是否有查询相关的信息"""
        query_type = self._classify_query(query_expressions)
        
        if query_type == QueryType.ECCENTRICITY:
            # 求离心率：需要a和c（或a和b）
            params = self._extract_known_parameters(symbolic_state)
            return ('a' in params and 'c' in params) or ('a' in params and 'b' in params)
        
        elif query_type == QueryType.EQUATION:
            # 求方程：需要曲线参数或定义点
            return len(self._extract_known_parameters(symbolic_state)) >= 2
        
        # 其他情况...
        return False
    
    def abstract_from_symbolic_state(
        self,
        symbolic_state: SymbolicState,
        query_expressions: str,
        reasoning_depth: int = 0
    ) -> AbstractState:
        """
        从符号状态直接构建抽象状态
        
        用于在模型应用后重新抽象状态
        
        Args:
            symbolic_state: 符号状态
            query_expressions: 查询表达式
            reasoning_depth: 推理深度
        
        Returns:
            AbstractState
        """
        abstract_state = AbstractState()
        
        # 提取特征
        abstract_state.curve_type = self._extract_curve_type(symbolic_state)
        abstract_state.query_type = self._classify_query(query_expressions)
        abstract_state.has_equation = self._check_has_equation(symbolic_state)
        abstract_state.has_parameters = self._extract_known_parameters(symbolic_state)
        abstract_state.has_focus_info = self._check_has_focus(symbolic_state)
        abstract_state.has_vertex_info = self._check_has_vertex(symbolic_state)
        abstract_state.has_point_on_curve = self._check_has_point_on_curve(symbolic_state)
        abstract_state.has_asymptote_info = self._check_has_asymptote(symbolic_state)
        abstract_state.has_directrix_info = self._check_has_directrix(symbolic_state)
        abstract_state.has_tangent_info = self._check_has_tangent(symbolic_state)
        abstract_state.has_distance_constraint = self._check_has_distance(symbolic_state)
        abstract_state.has_angle_constraint = self._check_has_angle(symbolic_state)
        abstract_state.has_perpendicular = self._check_has_perpendicular(symbolic_state)
        abstract_state.completeness_score = self._estimate_completeness(
            symbolic_state,
            query_expressions
        )
        abstract_state.reasoning_depth = reasoning_depth
        
        return abstract_state


# ========== 使用示例 ==========

def test_state_abstractor():
    """测试状态抽象器"""
    
    abstractor = StateAbstractor()
    
    # 示例1：双曲线问题（id=2）
    fact_expressions = (
        "G: Hyperbola;m: Number;m>0;"
        "Expression(G) = (x^2/4 - y^2/m^2 = 1);"
        "Expression(OneOf(Asymptote(G))) = (5*x - 2*y = 0)"
    )
    query_expressions = "m"
    
    abstract_state, symbolic_state = abstractor.abstract_from_facts(
        fact_expressions, 
        query_expressions
    )
    
    print("=" * 60)
    print("示例1：双曲线问题")
    print("-" * 60)
    print(f"抽象状态: {abstract_state}")
    print(f"状态哈希: {abstract_state.to_hash()}")
    print(f"特征向量: {abstract_state.to_vector()[:10]}...")  # 只显示前10维
    print(f"符号状态实体: {symbolic_state.entities}")
    print(f"符号状态方程: {symbolic_state.equations}")
    print()


if __name__ == "__main__":
    test_state_abstractor()
