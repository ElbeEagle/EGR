"""
State module - 状态表示模块

包含双层状态表示：
- SymbolicState: 符号状态（细粒度）
- AbstractState: 抽象状态（粗粒度）
- StateConstructor: 状态构造器
"""

from .symbolic_state import SymbolicState
from .abstract_state import AbstractState, CurveType, QueryType
from .state_constructor import StateConstructor

__all__ = [
    'SymbolicState',
    'AbstractState',
    'CurveType',
    'QueryType',
    'StateConstructor',
]
