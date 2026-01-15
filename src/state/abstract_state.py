"""
AbstractState - 抽象状态

有限离散的特征表示，用于神经网络输入和状态索引
"""

from dataclasses import dataclass, field
from typing import List, Set
from enum import Enum
import hashlib
import json


class CurveType(Enum):
    """曲线类型枚举"""
    ELLIPSE = "ellipse"
    HYPERBOLA = "hyperbola"
    PARABOLA = "parabola"
    CIRCLE = "circle"
    UNKNOWN = "unknown"


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


@dataclass
class AbstractState:
    """
    抽象状态：有限离散的特征表示
    
    用于：
    - 神经网络输入
    - 状态索引和去重
    - 快速特征匹配
    
    特点：
    - 有限状态空间（约40万种）
    - 可哈希、可向量化
    - 从SymbolicState重新构建
    """
    
    # ===== 维度1: 曲线类型 (5种) =====
    curve_type: CurveType = CurveType.UNKNOWN
    """
    曲线类型枚举
    
    取值：
    - CurveType.ELLIPSE: 椭圆
    - CurveType.HYPERBOLA: 双曲线
    - CurveType.PARABOLA: 抛物线
    - CurveType.CIRCLE: 圆
    - CurveType.UNKNOWN: 未知
    
    提取规则：从 entities 中查找曲线类型实体
    """
    
    # ===== 维度2: 查询类型 (10种) =====
    query_type: QueryType = QueryType.VALUE
    """
    查询目标类型枚举
    
    取值：10种（见QueryType枚举）
    
    提取规则：从 query_expressions 关键词匹配
    """
    
    # ===== 维度3: 信息特征 (11个布尔特征) =====
    has_equation: bool = False
    """是否有曲线方程"""
    
    has_parameters: Set[str] = field(default_factory=set)
    """
    已知参数集合
    
    例如：{'a', 'b', 'c', 'e', 'm'}
    注意：只记录参数名，不记录值
    """
    
    has_focus_info: bool = False
    """是否有焦点相关信息"""
    
    has_vertex_info: bool = False
    """是否有顶点信息"""
    
    has_point_on_curve: bool = False
    """是否有曲线上的点"""
    
    has_asymptote_info: bool = False
    """是否有渐近线信息"""
    
    has_directrix_info: bool = False
    """是否有准线信息"""
    
    has_tangent_info: bool = False
    """是否有切线信息"""
    
    has_distance_constraint: bool = False
    """是否有距离约束"""
    
    has_angle_constraint: bool = False
    """是否有角度约束"""
    
    has_perpendicular: bool = False
    """是否有垂直关系"""
    
    # ===== 维度4: 完整度得分 (连续值) =====
    completeness_score: float = 0.0
    """
    信息完整度得分 (0.0 - 1.0)
    
    计算规则：
    - 0.0: 信息几乎为空
    - 0.5: 信息约半完整
    - 1.0: 信息完全，可求解
    
    估算方法：启发式规则
    """
    
    # ===== 维度5: 推理深度 (整数) =====
    reasoning_depth: int = 0
    """
    推理步数
    
    - 0: 初始状态
    - 1: 应用1个模型后
    - 2: 应用2个模型后
    - ...
    """
    
    def to_vector(self) -> List[float]:
        """
        转换为特征向量（用于神经网络）
        
        返回：长度约28的浮点数列表
        
        向量组成：
        - [0:5]   曲线类型 one-hot (5维)
        - [5:15]  查询类型 one-hot (10维)
        - [15:26] 信息特征 (11维)
        - [26:28] 完整度和深度 (2维)
        
        Returns:
            List[float]: 特征向量
        """
        vector = []
        
        # 1. 曲线类型 one-hot
        curve_types = [
            CurveType.ELLIPSE,
            CurveType.HYPERBOLA,
            CurveType.PARABOLA,
            CurveType.CIRCLE,
            CurveType.UNKNOWN
        ]
        curve_one_hot = [
            1.0 if self.curve_type == ct else 0.0
            for ct in curve_types
        ]
        vector.extend(curve_one_hot)
        
        # 2. 查询类型 one-hot
        query_types = list(QueryType)
        query_one_hot = [
            1.0 if self.query_type == qt else 0.0
            for qt in query_types
        ]
        vector.extend(query_one_hot)
        
        # 3. 信息特征
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
            float(len(self.has_parameters)) / 10.0  # 归一化
        ])
        
        # 4. 完整度和深度
        vector.extend([
            self.completeness_score,
            min(self.reasoning_depth / 10.0, 1.0)  # 归一化
        ])
        
        return vector
    
    def to_hash(self) -> str:
        """
        计算状态哈希（用于索引）
        
        注意：不包含 reasoning_depth，使相同信息状态有相同哈希
        
        Returns:
            str: MD5哈希值
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
            'completeness_level': round(self.completeness_score * 4) / 4  # 量化到0.25
        }
        
        state_str = json.dumps(state_dict, sort_keys=True)
        return hashlib.md5(state_str.encode()).hexdigest()
    
    def __repr__(self) -> str:
        """友好的字符串表示"""
        return (
            f"AbstractState(\n"
            f"  curve={self.curve_type.value},\n"
            f"  query={self.query_type.value},\n"
            f"  has_equation={self.has_equation},\n"
            f"  parameters={self.has_parameters},\n"
            f"  completeness={self.completeness_score:.2f},\n"
            f"  depth={self.reasoning_depth}\n"
            f")"
        )
