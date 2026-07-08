"""Predicate contracts for constructed-geometry executors."""

from __future__ import annotations

from .catalog import THEOREM_CATALOG, TheoremRequirement


_OVERRIDES = {
    44: (
        ("IntersectionOf", "ExpressionPolynomial"),
        ("PointDifferenceRelationOf",),
        (),
    ),
    45: (
        ("IntersectionOf", "ExpressionPolynomial"),
        ("EllipsePointDifferenceRelationOf",),
        (44,),
    ),
    46: (
        ("IntersectionOf", "ExpressionPolynomial"),
        ("HyperbolaPointDifferenceRelationOf",),
        (44,),
    ),
    47: (("AngleValueOf",), ("CosineLawRelationOf",), ()),
    48: (("AngleValueOf",), ("SineLawRelationOf",), ()),
    49: (("RightAngleOf",), ("PythagoreanRelationOf",), ()),
    50: (
        ("QuadraticPolynomialOf", "LineNormalFormOf"),
        ("ChordLengthFormulaOf",),
        (78, 42, 43),
    ),
    51: (
        ("QuadraticPolynomialOf", "LineNormalFormOf"),
        ("ChordLengthWithKFormulaOf",),
        (78, 42, 43),
    ),
    56: (
        ("RequestedAreaOf",),
        ("AreaBaseHeightFormulaOf", "EquationConstraint"),
        (),
    ),
    57: (
        ("RequestedAreaOf", "AngleValueOf"),
        ("AreaWithSinFormulaOf",),
        (),
    ),
    58: (
        ("RequestedAreaOf", "PointPositionOf"),
        ("CoordinateAreaFormulaOf", "EquationConstraint"),
        (),
    ),
}


def constructed_geometry_requirement(model_id: int) -> TheoremRequirement:
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
