"""Complete 80-model theorem requirement catalog for v2.

The catalog is the source of truth for dependency analysis and sequence repair.
A catalog entry does not claim executable mathematical semantics; concrete
support is tracked separately by ``CompleteTheoremLibraryV2``.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Tuple


@dataclass(frozen=True)
class TheoremRequirement:
    model_id: int
    name: str
    category: str
    formula: str
    required_types: Tuple[str, ...] = ()
    required_predicates: Tuple[str, ...] = ()
    produced_predicates: Tuple[str, ...] = ("TheoremRelation",)
    dependencies: Tuple[int, ...] = ()
    modes: Tuple[str, ...] = ("forward",)


_ROWS = (
    (0, "Ellipse_Definition", "definition", "|PF1|+|PF2|=2a"),
    (1, "Hyperbola_Definition", "definition", "||PF1|-|PF2||=2a"),
    (2, "Parabola_Definition", "definition", "|PF|=distance(P,directrix)"),
    (3, "Ellipse_Equation_Standard_X", "standard_equation", "x^2/a^2+y^2/b^2=1"),
    (4, "Ellipse_Equation_Standard_Y", "standard_equation", "y^2/a^2+x^2/b^2=1"),
    (5, "Hyperbola_Equation_Standard_X", "standard_equation", "x^2/a^2-y^2/b^2=1"),
    (6, "Hyperbola_Equation_Standard_Y", "standard_equation", "y^2/a^2-x^2/b^2=1"),
    (7, "Parabola_Equation_Standard_Right", "standard_equation", "y^2=2px"),
    (8, "Parabola_Equation_Standard_Left", "standard_equation", "y^2=-2px"),
    (9, "Parabola_Equation_Standard_Up", "standard_equation", "x^2=2py"),
    (10, "Parabola_Equation_Standard_Down", "standard_equation", "x^2=-2py"),
    (11, "Ellipse_Parameter_Relation", "parameter", "a^2=b^2+c^2"),
    (12, "Hyperbola_Parameter_Relation", "parameter", "c^2=a^2+b^2"),
    (13, "Eccentricity_Formula", "parameter", "e=c/a"),
    (14, "Ellipse_Eccentricity_Range", "parameter", "0<e<1"),
    (15, "Hyperbola_Eccentricity_Range", "parameter", "e>1"),
    (16, "Ellipse_Focal_Radius", "focal_radius", "|PF|=a+/-ex"),
    (17, "Parabola_Focal_Radius", "focal_radius", "|PF|=x+p/2"),
    (18, "Ellipse_Latus_Rectum", "latus_rectum", "length=2b^2/a"),
    (19, "Hyperbola_Latus_Rectum", "latus_rectum", "length=2b^2/a"),
    (20, "Parabola_Latus_Rectum", "latus_rectum", "length=2p"),
    (21, "Hyperbola_Asymptote", "asymptote", "y=+/-(b/a)x"),
    (22, "Hyperbola_Focus_To_Asymptote_Distance", "asymptote", "distance=b"),
    (23, "Hyperbola_Common_Asymptote_System", "asymptote", "x^2/a^2-y^2/b^2=lambda"),
    (24, "Hyperbola_Equal_Axis", "asymptote", "a=b and e=sqrt(2)"),
    (25, "Ellipse_Second_Definition", "directrix", "|PF|/d=e"),
    (26, "Hyperbola_Second_Definition", "directrix", "|PF|/d=e"),
    (27, "Ellipse_Directrix", "directrix", "x=+/-a^2/c"),
    (28, "Hyperbola_Directrix", "directrix", "x=+/-a^2/c"),
    (29, "Parabola_Directrix", "directrix", "x or y=+/-p/2"),
    (30, "Ellipse_Focal_Triangle_Area", "focal_triangle", "S=b^2*tan(theta/2)"),
    (31, "Hyperbola_Focal_Triangle_Area", "focal_triangle", "S=b^2*cot(theta/2)"),
    (32, "Ellipse_Focal_Triangle_Perimeter", "focal_triangle", "perimeter=2a+2c"),
    (33, "Parabola_Focal_Chord_Length", "focal_chord", "|AB|=x1+x2+p"),
    (34, "Parabola_Focal_Chord_Product_X", "focal_chord", "x1*x2=p^2/4"),
    (35, "Parabola_Focal_Chord_Product_Y", "focal_chord", "y1*y2=-p^2"),
    (36, "Parabola_Focal_Chord_Formula_Angle", "focal_chord", "|AB|=2p/sin(theta)^2"),
    (37, "Ellipse_Parametric_Equation", "tangent", "x=a*cos(t),y=b*sin(t)"),
    (38, "Ellipse_Tangent_Line", "tangent", "x0*x/a^2+y0*y/b^2=1"),
    (39, "Parabola_Tangent_Line", "tangent", "y0*y=2p(x+x0)"),
    (40, "Ellipse_Midpoint_Chord_Slope", "chord", "k*k_OM=-b^2/a^2"),
    (41, "Vieta_Theorem", "algebra", "root sum and product"),
    (42, "Vieta_Theorem_Sum", "algebra", "x1+x2=-b/a"),
    (43, "Vieta_Theorem_Product", "algebra", "x1*x2=c/a"),
    (44, "Point_Difference_Method", "chord", "subtract two point equations"),
    (45, "Point_Difference_Method_Ellipse", "chord", "ellipse point-difference relation"),
    (46, "Point_Difference_Method_Hyperbola", "chord", "hyperbola point-difference relation"),
    (47, "Cosine_Law", "triangle", "c^2=a^2+b^2-2ab*cos(C)"),
    (48, "Sine_Law", "triangle", "a/sin(A)=b/sin(B)=c/sin(C)"),
    (49, "Pythagorean_Theorem", "triangle", "a^2+b^2=c^2"),
    (50, "Chord_Length_Formula", "chord", "|AB|=sqrt((sum)^2-4product)*sqrt(1+k^2)"),
    (51, "Chord_Length_Formula_With_K", "chord", "|AB|=|x1-x2|*sqrt(1+k^2)"),
    (52, "Point_To_Line_Distance", "coordinate", "d=|Ax0+By0+C|/sqrt(A^2+B^2)"),
    (53, "Two_Points_Distance", "coordinate", "d=sqrt((x2-x1)^2+(y2-y1)^2)"),
    (54, "Midpoint_Formula", "coordinate", "M=((x1+x2)/2,(y1+y2)/2)"),
    (55, "Slope_Formula", "coordinate", "k=(y2-y1)/(x2-x1)"),
    (56, "Triangle_Area_Formula", "area", "S=base*height/2"),
    (57, "Triangle_Area_With_Sin", "area", "S=ab*sin(C)/2"),
    (58, "Triangle_Area_Coordinate", "area", "S=|x1*y2-x2*y1|/2"),
    (59, "Vector_Dot_Product_Algebraic", "vector", "u dot v=x1*x2+y1*y2"),
    (60, "Vector_Dot_Product_Geometric", "vector", "u dot v=|u||v|cos(theta)"),
    (61, "Vector_Perpendicular_Condition", "vector", "u dot v=0"),
    (62, "Vector_Collinear_Condition", "vector", "u=lambda*v"),
    (63, "Basic_Inequality", "inequality", "a+b>=2sqrt(ab)"),
    (64, "Basic_Inequality_Equal_Condition", "inequality", "equality iff a=b"),
    (65, "Discriminant_Delta", "discriminant", "Delta=b^2-4ac"),
    (66, "Discriminant_Tangent_Condition", "discriminant", "Delta=0"),
    (67, "Discriminant_Intersect_Condition", "discriminant", "Delta>0"),
    (68, "Triangle_Midline_Theorem", "midline", "midline=base/2"),
    (69, "Trapezoid_Midline_Theorem", "midline", "midline=(base1+base2)/2"),
    (70, "Incircle_Radius_Formula", "triangle", "r=2S/perimeter"),
    (71, "Equal_Area_Method", "area", "equal base or height area relation"),
    (72, "Line_Point_Slope_Form", "line", "y-y0=k(x-x0)"),
    (73, "Line_Two_Point_Form", "line", "(y-y1)/(y2-y1)=(x-x1)/(x2-x1)"),
    (74, "Line_Intercept_Form", "line", "x/a+y/b=1"),
    (75, "Circle_Standard_Equation", "circle", "(x-h)^2+(y-k)^2=r^2"),
    (76, "Circle_Tangent_Condition", "circle", "distance(center,line)=radius"),
    (77, "Homogenization_Eccentricity", "advanced", "divide by a^2"),
    (78, "Substitution_x_equals_my_plus_n", "advanced", "x=my+n"),
    (79, "Quadratic_Function_Maximum", "advanced", "extremum by completing square"),
)


_TYPE_BY_CATEGORY = {
    "definition": (),
    "standard_equation": (),
    "parameter": (),
    "focal_radius": ("Point",),
    "latus_rectum": (),
    "asymptote": ("Hyperbola",),
    "directrix": (),
    "focal_triangle": ("Point",),
    "focal_chord": ("Parabola", "Point"),
    "tangent": ("Point",),
    "chord": ("Point",),
    "algebra": (),
    "triangle": ("Triangle",),
    "coordinate": ("Point",),
    "area": (),
    "vector": ("Vector",),
    "inequality": (),
    "discriminant": (),
    "midline": (),
    "line": ("Line",),
    "circle": ("Circle",),
    "advanced": (),
}

_DEPENDENCIES = {
    11: (3, 4), 12: (5, 6), 13: (11, 12), 14: (13,), 15: (13,),
    16: (0, 11, 13), 17: (2, 7, 8, 9, 10), 18: (11,), 19: (12,),
    20: (7, 8, 9, 10), 21: (5, 6), 22: (21,), 23: (21,), 24: (12, 13, 21),
    25: (13, 27), 26: (13, 28), 27: (11, 13), 28: (12, 13),
    29: (7, 8, 9, 10), 30: (0, 11), 31: (1, 12), 32: (0, 11),
    33: (7, 8, 9, 10), 34: (33,), 35: (33,), 36: (33,),
    37: (3, 4), 38: (3, 4), 39: (7, 8, 9, 10), 40: (3, 4, 44),
    42: (41,), 43: (41,), 45: (44, 3, 4), 46: (44, 5, 6),
    50: (42, 43, 55), 51: (55,), 56: (52,), 58: (53,),
    61: (59,), 62: (59,), 64: (63,), 66: (65,), 67: (65,),
    70: (56,), 71: (56,), 76: (52, 75), 77: (11, 12, 13),
    78: (72,), 79: (65,),
}

_PREDICATES = {
    "standard_equation": ("ExpressionPolynomial",),
    "parameter": ("ParameterOf",),
    "focal_radius": ("PointOnCurve",),
    "latus_rectum": ("ParameterOf",),
    "asymptote": ("ConicStandardForm",),
    "directrix": ("ParameterOf",),
    "focal_triangle": ("FocusOf",),
    "focal_chord": ("PointOnCurve",),
    "tangent": ("PointOnCurve",),
    "chord": ("PointOnCurve",),
    "algebra": ("QuadraticPolynomial",),
    "triangle": ("TriangleOf",),
    "coordinate": ("CoordinateOf",),
    "area": ("TriangleOf",),
    "vector": ("VectorOf",),
    "inequality": ("OrderConstraint",),
    "discriminant": ("QuadraticPolynomial",),
    "midline": ("MidpointOf",),
    "line": ("CoordinateOf",),
    "circle": ("ExpressionPolynomial",),
    "advanced": ("EquationConstraint",),
}

_PRODUCES = {
    "definition": ("DefinitionRelation",),
    "standard_equation": ("ConicStandardForm", "ParameterOf"),
    "parameter": ("ParameterOf", "EquationConstraint"),
    "focal_radius": ("DistanceOf", "EquationConstraint"),
    "latus_rectum": ("LengthOf",),
    "asymptote": ("AsymptoteFamilyOf", "EquationConstraint"),
    "directrix": ("DirectrixExpressionOf",),
    "focal_triangle": ("AreaOf", "PerimeterOf"),
    "focal_chord": ("LengthOf", "EquationConstraint"),
    "tangent": ("ExpressionOf",),
    "chord": ("EquationConstraint",),
    "algebra": ("EquationConstraint",),
    "triangle": ("EquationConstraint",),
    "coordinate": ("CoordinateOf", "DistanceOf", "SlopeOf"),
    "area": ("AreaOf",),
    "vector": ("EquationConstraint",),
    "inequality": ("OrderConstraint",),
    "discriminant": ("DiscriminantOf", "OrderConstraint"),
    "midline": ("LengthOf",),
    "line": ("ExpressionOf",),
    "circle": ("CircleStandardForm", "ParameterOf"),
    "advanced": ("EquationConstraint",),
}

_REVERSE_MODE_IDS = set(range(0, 14)) | {21, 23, 25, 26, 27, 28, 29, 37, 72, 73, 74, 75}


def _build_catalog() -> Dict[int, TheoremRequirement]:
    result = {}
    for model_id, name, category, formula in _ROWS:
        modes = ("forward", "reverse") if model_id in _REVERSE_MODE_IDS else ("forward",)
        result[model_id] = TheoremRequirement(
            model_id=model_id,
            name=name,
            category=category,
            formula=formula,
            required_types=_TYPE_BY_CATEGORY.get(category, ()),
            required_predicates=_PREDICATES.get(category, ()),
            produced_predicates=_PRODUCES.get(category, ("TheoremRelation",)),
            dependencies=_DEPENDENCIES.get(model_id, ()),
            modes=modes,
        )
    return result


THEOREM_CATALOG: Dict[int, TheoremRequirement] = _build_catalog()
