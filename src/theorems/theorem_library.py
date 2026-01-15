"""
TheoremLibrary - 定理库管理器

管理80个定理模型，提供统一接口
"""

from typing import Dict, Optional, List
from .base_model import TheoremModel


class TheoremLibrary:
    """
    定理库管理器
    
    功能：
    1. 注册和管理80个定理模型
    2. 根据ID获取模型
    3. 应用模型序列
    """
    
    def __init__(self):
        """初始化定理库"""
        self.models: Dict[int, TheoremModel] = {}
        self._load_models()
    
    def _load_models(self):
        """
        加载所有定理模型
        
        注意：逐步添加80个模型
        """
        # 已实现的模型
        from .models.model_005 import HyperbolaEquationStandardX
        from .models.model_021 import HyperbolaAsymptote
        
        self.register_model(HyperbolaEquationStandardX())
        self.register_model(HyperbolaAsymptote())
    
    def register_model(self, model: TheoremModel):
        """
        注册一个定理模型
        
        Args:
            model: TheoremModel实例
        """
        self.models[model.model_id] = model
    
    def get_model(self, model_id: int) -> Optional[TheoremModel]:
        """
        根据ID获取模型
        
        Args:
            model_id: 模型ID (0-79)
        
        Returns:
            Optional[TheoremModel]: 模型实例，如果不存在返回None
        """
        return self.models.get(model_id)
    
    def has_model(self, model_id: int) -> bool:
        """
        检查模型是否存在
        
        Args:
            model_id: 模型ID
        
        Returns:
            bool: 是否存在
        """
        return model_id in self.models
    
    def apply_model(self, state, model_id: int) -> bool:
        """
        应用单个模型
        
        Args:
            state: SymbolicState - 符号状态
            model_id: 模型ID
        
        Returns:
            bool: 是否成功应用
        """
        model = self.get_model(model_id)
        if model is None:
            return False
        
        if not model.can_apply(state):
            return False
        
        model.apply(state)
        state.applied_models.append(model_id)
        return True
    
    def apply_model_sequence(
        self,
        state,
        model_ids: List[int]
    ) -> List[bool]:
        """
        批量应用模型序列
        
        Args:
            state: SymbolicState - 符号状态
            model_ids: 模型ID列表
        
        Returns:
            List[bool]: 每个模型的应用结果
        """
        results = []
        for model_id in model_ids:
            success = self.apply_model(state, model_id)
            results.append(success)
        return results
    
    def get_available_models(self) -> List[int]:
        """
        获取所有已注册的模型ID列表
        
        Returns:
            List[int]: 模型ID列表
        """
        return sorted(self.models.keys())
    
    def __len__(self) -> int:
        """返回已注册的模型数量"""
        return len(self.models)
    
    def __repr__(self) -> str:
        """友好的字符串表示"""
        return f"TheoremLibrary(models={len(self.models)}/80)"
