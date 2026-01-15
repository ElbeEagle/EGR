"""
TheoremModel - 定理模型基类

所有80个定理模型的基类
"""

from abc import ABC, abstractmethod
from typing import Optional


class TheoremModel(ABC):
    """
    定理模型基类
    
    每个定理模型必须实现两个方法：
    1. can_apply(): 检查前置条件
    2. apply(): 应用模型，更新状态
    
    核心原则：
    - 只增不减：只能向state添加信息
    - 幂等性：重复应用不出错
    - 无副作用：不依赖外部状态
    - 容错处理：输入不满足条件时安静返回
    """
    
    def __init__(self, model_id: int, name: str, chinese_name: str):
        """
        初始化模型
        
        Args:
            model_id: 模型唯一ID (0-79)
            name: 英文名称，如 "Hyperbola_Asymptote"
            chinese_name: 中文名称，如 "双曲线渐近线"
        """
        self.model_id = model_id
        self.name = name
        self.chinese_name = chinese_name
    
    @abstractmethod
    def can_apply(self, state) -> bool:
        """
        检查模型是否可应用
        
        检查前置条件，判断当前状态是否满足模型应用的要求
        
        Args:
            state: SymbolicState - 当前符号状态
        
        Returns:
            bool: 是否可应用
        """
        pass
    
    @abstractmethod
    def apply(self, state) -> None:
        """
        应用模型，直接修改state
        
        注意：
        - 直接修改传入的state对象，不返回新对象
        - 只能添加信息，不能删除或修改已有信息
        - 应用前建议先检查 can_apply()
        
        Args:
            state: SymbolicState - 当前符号状态（会被修改）
        
        Returns:
            None
        """
        pass
    
    def __repr__(self) -> str:
        """友好的字符串表示"""
        return f"TheoremModel(id={self.model_id}, name={self.name})"
