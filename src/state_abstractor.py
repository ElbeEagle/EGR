"""
状态抽象器 - 将 fact_expressions 转换为结构化的状态表示

核心功能：
1. 解析 fact_expressions 和 query_expressions
2. 提取关键信息（曲线类型、参数、几何关系等）
3. 计算信息完整度
4. 生成状态向量和哈希
"""

import re
from typing import Dict, List, Set, Any, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum


class CurveType(Enum):
    """曲线类型"""
    ELLIPSE = "Ellipse"
    HYPERBOLA = "Hyperbola"
    PARABOLA = "Parabola"
    CIRCLE = "Circle"
    UNKNOWN = "Unknown"


class QueryType(Enum):
    """查询类型"""
    ECCENTRICITY = "eccentricity"
    EQUATION = "equation"
    COORDINATE = "coordinate"
    DISTANCE = "distance"
    RANGE = "range"
    LENGTH = "length"
    AREA = "area"
    ANGLE = "angle"
    VALUE = "value"
    OTHER = "other"


@dataclass
class AbstractState:
    """抽象状态表示"""
    
    # 基础信息
    curve_type: CurveType
    query_type: QueryType
    
    # 已知信息标记
    has_equation: bool = False
    has_focus: bool = False
    has_vertex: bool = False
    has_asymptote: bool = False
    has_directrix: bool = False
    has_center: bool = False
    
    # 已知参数（符号和数值）
    known_params: Dict[str, Any] = field(default_factory=dict)
    # 例如: {'a': 'symbolic', 'b': 3.0, 'c': 'symbolic'}
    
    # 几何关系
    has_point_on_curve: bool = False
    has_tangent: bool = False
    has_perpendicular: bool = False
    has_parallel: bool = False
    has_intersection: bool = False
    
    # 约束条件
    constraints: List[str] = field(default_factory=list)
    # 例如: ['a>0', 'm>0', 'e<1']
    
    # 信息完整度 (0-1)
    completeness: float = 0.0
    
    # 原始表达式（用于调试）
    raw_facts: str = ""
    raw_query: str = ""
    
    # 状态哈希（用于索引）
    state_hash: str = ""
    
    def to_dict(self) -> Dict:
        """转换为字典"""
        return {
            'curve_type': self.curve_type.value,
            'query_type': self.query_type.value,
            'has_equation': self.has_equation,
            'has_focus': self.has_focus,
            'has_vertex': self.has_vertex,
            'has_asymptote': self.has_asymptote,
            'known_params': self.known_params,
            'has_point_on_curve': self.has_point_on_curve,
            'has_tangent': self.has_tangent,
            'has_perpendicular': self.has_perpendicular,
            'constraints': self.constraints,
            'completeness': self.completeness,
            'state_hash': self.state_hash
        }


class StateAbstractor:
    """
    状态抽象器
    
    将原始的 fact_expressions 和 query_expressions 
    抽象为结构化的 AbstractState
    """
    
    def __init__(self):
        """初始化"""
        # 参数名称集合
        self.param_names = {'a', 'b', 'c', 'e', 'p', 'm', 'n', 't', 'k'}
        
        # 统计信息
        self.total_abstracted = 0
        self.failed_count = 0
    
    def abstract(self, fact_expressions: str, query_expressions: str) -> AbstractState:
        """
        抽象一个问题状态
        
        Args:
            fact_expressions: 原始fact表达式
            query_expressions: 原始query表达式
            
        Returns:
            AbstractState对象
        """
        try:
            # 1. 识别曲线类型
            curve_type = self._extract_curve_type(fact_expressions)
            
            # 2. 识别查询类型
            query_type = self._classify_query(query_expressions)
            
            # 3. 提取已知信息
            info_flags = self._extract_info_flags(fact_expressions)
            
            # 4. 提取已知参数
            known_params = self._extract_parameters(fact_expressions)
            
            # 5. 提取几何关系
            geo_relations = self._extract_geometric_relations(fact_expressions)
            
            # 6. 提取约束条件
            constraints = self._extract_constraints(fact_expressions)
            
            # 7. 计算信息完整度
            completeness = self._estimate_completeness(
                curve_type, query_type, info_flags, known_params
            )
            
            # 8. 生成状态哈希
            state_hash = self._compute_state_hash(
                curve_type, query_type, info_flags, known_params
            )
            
            # 9. 构造状态对象
            state = AbstractState(
                curve_type=curve_type,
                query_type=query_type,
                has_equation=info_flags['has_equation'],
                has_focus=info_flags['has_focus'],
                has_vertex=info_flags['has_vertex'],
                has_asymptote=info_flags['has_asymptote'],
                has_directrix=info_flags['has_directrix'],
                has_center=info_flags['has_center'],
                known_params=known_params,
                has_point_on_curve=geo_relations['has_point_on_curve'],
                has_tangent=geo_relations['has_tangent'],
                has_perpendicular=geo_relations['has_perpendicular'],
                has_parallel=geo_relations['has_parallel'],
                has_intersection=geo_relations['has_intersection'],
                constraints=constraints,
                completeness=completeness,
                raw_facts=fact_expressions,
                raw_query=query_expressions,
                state_hash=state_hash
            )
            
            self.total_abstracted += 1
            return state
            
        except Exception as e:
            self.failed_count += 1
            print(f"Warning: Failed to abstract state: {e}")
            # 返回一个默认状态
            return AbstractState(
                curve_type=CurveType.UNKNOWN,
                query_type=QueryType.OTHER,
                raw_facts=fact_expressions,
                raw_query=query_expressions
            )
    
    def _extract_curve_type(self, facts: str) -> CurveType:
        """提取曲线类型"""
        if 'Ellipse' in facts:
            return CurveType.ELLIPSE
        elif 'Hyperbola' in facts:
            return CurveType.HYPERBOLA
        elif 'Parabola' in facts:
            return CurveType.PARABOLA
        elif 'Circle' in facts:
            return CurveType.CIRCLE
        else:
            return CurveType.UNKNOWN
    
    def _classify_query(self, query: str) -> QueryType:
        """分类查询类型"""
        if 'Eccentricity' in query:
            return QueryType.ECCENTRICITY
        elif 'Expression' in query:
            return QueryType.EQUATION
        elif 'Coordinate' in query:
            return QueryType.COORDINATE
        elif 'Distance' in query or 'Abs' in query:
            return QueryType.DISTANCE
        elif 'Range' in query:
            return QueryType.RANGE
        elif 'Length' in query:
            return QueryType.LENGTH
        elif 'Area' in query:
            return QueryType.AREA
        elif 'Angle' in query:
            return QueryType.ANGLE
        else:
            # 如果query是单个变量名，说明是求值
            if query.strip() in self.param_names or re.match(r'^[a-z]$', query.strip()):
                return QueryType.VALUE
            return QueryType.OTHER
    
    def _extract_info_flags(self, facts: str) -> Dict[str, bool]:
        """提取信息标记"""
        return {
            'has_equation': 'Expression(' in facts,
            'has_focus': 'Focus(' in facts,
            'has_vertex': 'Vertex(' in facts,
            'has_asymptote': 'Asymptote(' in facts,
            'has_directrix': 'Directrix(' in facts,
            'has_center': 'Center(' in facts
        }
    
    def _extract_parameters(self, facts: str) -> Dict[str, Any]:
        """
        提取已知参数
        
        识别模式：
        1. 数值型：a: Number (符号)
        2. 方程提取：Expression(G) = (x^2/4 + ...) → a=2
        """
        params = {}
        
        # 模式1：声明为Number的变量（符号化）
        for param in self.param_names:
            if f'{param}: Number' in facts or f'{param}: Real' in facts:
                params[param] = 'symbolic'
        
        # 模式2：从标准方程提取数值
        # 椭圆/双曲线: x^2/a^2 ± y^2/b^2 = 1
        equation_match = re.search(
            r'x\^2/(\d+(?:\.\d+)?)\s*[+-]\s*y\^2/(\d+(?:\.\d+)?)\s*=\s*1',
            facts
        )
        if equation_match:
            a_squared = float(equation_match.group(1))
            b_squared = float(equation_match.group(2))
            params['a'] = a_squared ** 0.5
            params['b'] = b_squared ** 0.5
        
        # 模式3：焦距 FocalLength = 值
        focal_match = re.search(r'FocalLength\([^)]+\)\s*=\s*(\d+(?:\.\d+)?)', facts)
        if focal_match:
            focal_length = float(focal_match.group(1))
            params['2c'] = focal_length  # 焦距 = 2c
            if '2c' in params:
                params['c'] = params['2c'] / 2
        
        # 模式4：离心率 Eccentricity = 值
        ecc_match = re.search(r'Eccentricity\([^)]+\)\s*=\s*([0-9./sqrt()]+)', facts)
        if ecc_match:
            params['e'] = ecc_match.group(1)  # 保留为字符串（可能是分数或sqrt）
        
        return params
    
    def _extract_geometric_relations(self, facts: str) -> Dict[str, bool]:
        """提取几何关系"""
        return {
            'has_point_on_curve': 'PointOnCurve(' in facts,
            'has_tangent': 'IsTangent(' in facts or 'Tangent' in facts,
            'has_perpendicular': 'IsPerpendicular(' in facts or 'Perpendicular' in facts,
            'has_parallel': 'IsParallel(' in facts,
            'has_intersection': 'Intersection(' in facts
        }
    
    def _extract_constraints(self, facts: str) -> List[str]:
        """提取约束条件"""
        constraints = []
        
        # 匹配 变量>数字 或 变量<数字
        constraint_patterns = [
            r'([a-z])>(\d+)',
            r'([a-z])<(\d+)',
            r'([a-z])>0',
        ]
        
        for pattern in constraint_patterns:
            matches = re.findall(pattern, facts)
            for match in matches:
                if isinstance(match, tuple):
                    constraints.append(f"{match[0]}>{match[1]}")
                else:
                    constraints.append(match)
        
        return constraints
    
    def _estimate_completeness(
        self, 
        curve_type: CurveType, 
        query_type: QueryType,
        info_flags: Dict[str, bool],
        known_params: Dict[str, Any]
    ) -> float:
        """
        估计信息完整度 (0-1)
        
        启发式规则：
        1. 有方程 → +0.3
        2. 有焦点信息 → +0.2
        3. 已知参数个数 → +0.1 per param (最多0.4)
        4. 查询相关信息 → +0.1
        """
        score = 0.0
        
        # 1. 方程信息
        if info_flags.get('has_equation', False):
            score += 0.3
        
        # 2. 焦点信息
        if info_flags.get('has_focus', False):
            score += 0.2
        
        # 3. 已知参数
        concrete_params = [p for p in known_params.values() if p != 'symbolic']
        param_score = min(len(concrete_params) * 0.1, 0.4)
        score += param_score
        
        # 4. 查询相关性
        if query_type == QueryType.ECCENTRICITY:
            if 'e' in known_params or ('a' in known_params and 'c' in known_params):
                score += 0.1
        elif query_type == QueryType.EQUATION:
            if info_flags.get('has_equation', False):
                score += 0.1
        
        return min(score, 1.0)
    
    def _compute_state_hash(
        self,
        curve_type: CurveType,
        query_type: QueryType,
        info_flags: Dict[str, bool],
        known_params: Dict[str, Any]
    ) -> str:
        """
        计算状态哈希
        
        格式：CURVE_INFO_PARAMS_QUERY
        例如：ELL_EQ_AB_ECCENT
        """
        # 曲线类型缩写
        curve_abbr = {
            CurveType.ELLIPSE: 'ELL',
            CurveType.HYPERBOLA: 'HYP',
            CurveType.PARABOLA: 'PAR',
            CurveType.CIRCLE: 'CIR',
            CurveType.UNKNOWN: 'UNK'
        }
        
        # 信息标记
        info_parts = []
        if info_flags.get('has_equation'):
            info_parts.append('EQ')
        if info_flags.get('has_focus'):
            info_parts.append('FOC')
        if info_flags.get('has_asymptote'):
            info_parts.append('ASY')
        
        # 参数
        param_str = ''.join(sorted([p.upper() for p in known_params.keys()]))
        if not param_str:
            param_str = 'NONE'
        
        # 查询类型缩写
        query_abbr = {
            QueryType.ECCENTRICITY: 'ECCENT',
            QueryType.EQUATION: 'EQTN',
            QueryType.COORDINATE: 'COORD',
            QueryType.DISTANCE: 'DIST',
            QueryType.VALUE: 'VAL',
            QueryType.OTHER: 'OTH'
        }
        
        hash_parts = [
            curve_abbr[curve_type],
            '_'.join(info_parts) if info_parts else 'NOINFO',
            param_str,
            query_abbr.get(query_type, 'OTH')
        ]
        
        return '_'.join(hash_parts)
    
    def get_statistics(self) -> Dict[str, int]:
        """获取统计信息"""
        return {
            'total_abstracted': self.total_abstracted,
            'failed_count': self.failed_count,
            'success_rate': (self.total_abstracted - self.failed_count) / self.total_abstracted 
                           if self.total_abstracted > 0 else 0.0
        }


def create_state_abstractor() -> StateAbstractor:
    """创建状态抽象器实例"""
    return StateAbstractor()

