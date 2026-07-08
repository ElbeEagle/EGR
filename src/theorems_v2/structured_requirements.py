"""Predicate-level requirements for structured third-stage executors."""

from __future__ import annotations

from .catalog import THEOREM_CATALOG, TheoremRequirement


_OVERRIDES = {
    41: (("QuadraticPolynomialOf",), ("RootSumOf", "RootProductOf"), (78,)),
    42: (("QuadraticPolynomialOf",), ("RootSumOf",), (78, 41)),
    43: (("QuadraticPolynomialOf",), ("RootProductOf",), (78, 41)),
    52: (
        ("PointPositionOf", "LineNormalFormOf", "RequestedPointLineDistanceOf"),
        ("DistanceFormulaOf", "EquationConstraint"),
        (),
    ),
    53: (
        ("PointPositionOf", "RequestedDistanceOf"),
        ("DistanceFormulaOf", "EquationConstraint"),
        (),
    ),
    54: (
        ("PointPositionOf", "MidPointOf"),
        ("PointPositionOf", "MidpointFormulaOf"),
        (),
    ),
    55: (
        ("PointPositionOf", "RequestedSlopeOf"),
        ("SlopeFormulaOf", "EquationConstraint"),
        (),
    ),
    59: (
        ("VectorOf", "RequestedDotProductOf"),
        ("DotProductFormulaOf", "EquationConstraint"),
        (),
    ),
    61: (
        ("RequestedDotProductOf",),
        ("PerpendicularVectorPair",),
        (),
    ),
    62: (
        ("VectorScaleRelation",),
        ("CollinearVectorPair", "VectorScaleOf"),
        (),
    ),
    65: (("QuadraticPolynomialOf",), ("DiscriminantOf",), (78,)),
    66: (
        ("DiscriminantOf", "IntersectionCountOf"),
        ("DiscriminantConditionOf", "OrderConstraint"),
        (65,),
    ),
    67: (
        ("DiscriminantOf", "IntersectionCountOf"),
        ("DiscriminantConditionOf", "OrderConstraint"),
        (65,),
    ),
    72: (
        ("PointPositionOf", "PointOnCurve", "SlopeOf"),
        ("LinePointSlopeFormOf",),
        (),
    ),
    73: (
        ("PointPositionOf", "PointOnCurve"),
        ("LineTwoPointFormOf",),
        (),
    ),
    78: (
        ("IntersectionOf", "LineNormalFormOf", "ExpressionPolynomial"),
        ("QuadraticPolynomialOf", "RootSetOf", "SubstitutionOf"),
        (),
    ),
}


def structured_requirement(model_id: int) -> TheoremRequirement:
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
