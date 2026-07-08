"""Requirements for the quantity/conic executor batch."""

from __future__ import annotations

from .catalog import THEOREM_CATALOG, TheoremRequirement


_OVERRIDES = {
    30: (
        ("AngleValueOf", "FocusOf", "ParameterOf"),
        ("FocalTriangleAreaFormulaOf", "EquationConstraint"),
        (11,),
    ),
    31: (
        ("AngleValueOf", "FocusOf", "ParameterOf"),
        ("FocalTriangleAreaFormulaOf", "EquationConstraint"),
        (12,),
    ),
    33: (
        ("IntersectionOf", "FocusOf", "ConicStandardForm"),
        ("ParabolaFocalChordLengthOf",),
        (7, 8, 9, 10),
    ),
    34: (
        ("IntersectionOf", "FocusOf", "ConicStandardForm"),
        ("FocalChordCoordinateProductOf",),
        (7, 8),
    ),
    35: (
        ("IntersectionOf", "FocusOf", "ConicStandardForm"),
        ("FocalChordCoordinateProductOf",),
        (7, 8),
    ),
    36: (
        ("IntersectionOf", "FocusOf", "ConicStandardForm", "QuantityValueOf"),
        ("FocalChordAngleLengthOf",),
        (33,),
    ),
    40: (
        ("IntersectionOf", "MidPointOf", "PointPositionOf", "LineNormalFormOf"),
        ("MidpointChordSlopeRelationOf",),
        (44,),
    ),
    60: (
        ("RequestedDotProductOf", "AngleValueOf"),
        ("GeometricDotProductOf", "EquationConstraint"),
        (),
    ),
    74: (
        ("LineNormalFormOf",),
        ("LineInterceptsOf",),
        (),
    ),
    76: (
        ("TangentRelation", "LineNormalFormOf", "QuantityValueOf"),
        ("CircleTangentConditionOf",),
        (52, 75),
    ),
}


def quantity_conic_requirement(model_id: int) -> TheoremRequirement:
    base = THEOREM_CATALOG[model_id]
    required, produced, dependencies = _OVERRIDES[model_id]
    return TheoremRequirement(
        model_id=base.model_id,
        name=base.name,
        category=base.category,
        formula=base.formula,
        required_types=base.required_types,
        required_predicates=required,
        produced_predicates=produced,
        dependencies=dependencies,
        modes=base.modes,
    )
