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
        # 已实现的模型 (按模型ID排序)
        from .models.model_000 import EllipseDefinition
        from .models.model_001 import HyperbolaDefinition
        from .models.model_002 import ParabolaDefinition
        from .models.model_003 import EllipseEquationStandardX
        from .models.model_004 import EllipseEquationStandardY
        from .models.model_005 import HyperbolaEquationStandardX
        from .models.model_006 import HyperbolaEquationStandardY
        from .models.model_007 import ParabolaEquationStandardRight
        from .models.model_008 import ParabolaEquationStandardLeft
        from .models.model_009 import ParabolaEquationStandardUp
        from .models.model_010 import ParabolaEquationStandardDown
        from .models.model_011 import EllipseParameterRelation
        from .models.model_012 import HyperbolaParameterRelation
        from .models.model_013 import EccentricityFormula
        from .models.model_016 import EllipseFocalRadius
        from .models.model_017 import ParabolaFocalRadius
        from .models.model_019 import HyperbolaLatusRectum
        from .models.model_021 import HyperbolaAsymptote
        from .models.model_022 import HyperbolaFocusToAsymptoteDistance
        from .models.model_024 import HyperbolaEqualAxis
        from .models.model_029 import ParabolaDirectrix
        from .models.model_041 import VietaTheorem
        from .models.model_042 import VietaTheoremSum
        from .models.model_043 import VietaTheoremProduct
        from .models.model_047 import CosineLaw
        from .models.model_053 import TwoPointsDistance
        from .models.model_056 import TriangleAreaFormula
        from .models.model_062 import VectorCollinearCondition
        from .models.model_063 import BasicInequality
        from .models.model_075 import CircleStandardEquation
        
        # 注册模型
        self.register_model(EllipseDefinition())
        self.register_model(HyperbolaDefinition())
        self.register_model(ParabolaDefinition())
        self.register_model(EllipseEquationStandardX())
        self.register_model(EllipseEquationStandardY())
        self.register_model(HyperbolaEquationStandardX())
        self.register_model(HyperbolaEquationStandardY())
        self.register_model(ParabolaEquationStandardRight())
        self.register_model(ParabolaEquationStandardLeft())
        self.register_model(ParabolaEquationStandardUp())
        self.register_model(ParabolaEquationStandardDown())
        self.register_model(EllipseParameterRelation())
        self.register_model(HyperbolaParameterRelation())
        self.register_model(EccentricityFormula())
        self.register_model(EllipseFocalRadius())
        self.register_model(ParabolaFocalRadius())
        self.register_model(HyperbolaLatusRectum())
        self.register_model(HyperbolaAsymptote())
        self.register_model(HyperbolaFocusToAsymptoteDistance())
        self.register_model(HyperbolaEqualAxis())
        self.register_model(ParabolaDirectrix())
        self.register_model(VietaTheorem())
        self.register_model(VietaTheoremSum())
        self.register_model(VietaTheoremProduct())
        self.register_model(CosineLaw())
        self.register_model(TwoPointsDistance())
        self.register_model(TriangleAreaFormula())
        self.register_model(VectorCollinearCondition())
        self.register_model(BasicInequality())
        self.register_model(CircleStandardEquation())
    
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
