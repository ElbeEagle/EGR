"""
SymbolicState - 符号状态

存储问题的所有具体信息，用于精确推理和模型应用
"""

from dataclasses import dataclass, field
from typing import Dict, List, Tuple, Any


@dataclass
class SymbolicState:
    """
    符号状态：存储问题的所有具体信息
    
    核心原则：
    - 只增不减：只能添加信息，不能删除
    - 幂等性：重复应用同一模型不出错
    - 可追溯：记录完整推理历史
    """
    
    # ===== 字段1: 实体声明 =====
    entities: Dict[str, str] = field(default_factory=dict)
    """
    实体声明字典
    
    格式：{实体名: 实体类型}
    例如：{'G': 'Hyperbola', 'm': 'Number', 'A': 'Point', 'F': 'Point'}
    
    常见实体类型：
    - 曲线：Ellipse, Hyperbola, Parabola, Circle
    - 几何：Point, Line, LineSegment, Ray, Triangle
    - 数值：Number, Real, Angle
    - 其他：Vector, Origin, Axis
    """
    
    # ===== 字段2: 方程列表 =====
    equations: List[str] = field(default_factory=list)
    """
    方程/表达式列表
    
    格式：符号化的方程字符串
    例如：
    - 'Expression(G) = (x^2/4 - y^2/m^2 = 1)'
    - 'Expression(OneOf(Asymptote(G))) = (5*x - 2*y = 0)'
    - 'y^2 = 4*x'
    
    注意：保持原始形式，便于模式匹配
    """
    
    # ===== 字段3: 参数字典 =====
    parameters: Dict[str, Any] = field(default_factory=dict)
    """
    参数值字典（核心字段！）
    
    格式：{参数名: 参数值}
    例如：
    - {'a': 2, 'b': 'm', 'c': 'sqrt(5)'}
    - {'a^2': 4, 'b^2': 'm^2'}
    - {'e': 'sqrt(2)'}
    
    值的类型：
    - 数值：2, 3.14
    - 符号：'m', 'a', 'b'
    - 表达式：'sqrt(5)', 'm/2', 'sqrt(a^2 + b^2)'
    
    关键原则：
    ✅ 能算出具体值就算（如 a=2）
    ✅ 算不出保持符号形式（如 b='m'）
    ✅ 同时保留 a^2 和 a（如 a^2=4, a=2）
    """
    
    # ===== 字段4: 几何关系 =====
    geometric_relations: List[str] = field(default_factory=list)
    """
    几何关系列表
    
    格式：描述性的关系字符串
    例如：
    - 'Distance(P, F1) + Distance(P, F2) = 2*a'
    - 'IsPerpendicular(AB, xAxis)'
    - 'Intersection(L1, L2) = P'
    - 'a^2 = 4'
    - '渐近线: y = ±(m/2)x'
    
    用途：
    - 记录模型应用产生的关系
    - 便于人工检查推理过程
    """
    
    # ===== 字段5: 坐标信息 =====
    coordinates: Dict[str, Tuple] = field(default_factory=dict)
    """
    坐标字典
    
    格式：{点名: (x坐标, y坐标)}
    例如：
    - {'F': ('c', 0)}
    - {'A': (1, '1/4')}
    - {'P': ('x', 'y')}
    
    注意：坐标可以是符号或数值
    """
    
    # ===== 字段6: 约束条件 =====
    constraints: List[str] = field(default_factory=list)
    """
    约束条件列表
    
    格式：不等式或逻辑条件
    例如：
    - 'm > 0'
    - 'a > b'
    - 'b > 0'
    - 'e < 1'  (椭圆)
    - 'e > 1'  (双曲线)
    """
    
    # ===== 字段7: 元信息（可选）=====
    applied_models: List[int] = field(default_factory=list)
    """
    已应用的模型ID列表（用于调试和可视化）
    """
    
    def copy(self) -> 'SymbolicState':
        """
        深拷贝状态
        
        注意：必须深拷贝，否则会相互影响
        
        Returns:
            SymbolicState: 新的状态对象
        """
        return SymbolicState(
            entities=self.entities.copy(),
            equations=self.equations.copy(),
            parameters=self.parameters.copy(),
            geometric_relations=self.geometric_relations.copy(),
            coordinates={k: v for k, v in self.coordinates.items()},
            constraints=self.constraints.copy(),
            applied_models=self.applied_models.copy()
        )
    
    def __repr__(self) -> str:
        """友好的字符串表示"""
        return (
            f"SymbolicState(\n"
            f"  entities={len(self.entities)},\n"
            f"  equations={len(self.equations)},\n"
            f"  parameters={len(self.parameters)},\n"
            f"  relations={len(self.geometric_relations)},\n"
            f"  coordinates={len(self.coordinates)},\n"
            f"  constraints={len(self.constraints)},\n"
            f"  applied_models={self.applied_models}\n"
            f")"
        )
