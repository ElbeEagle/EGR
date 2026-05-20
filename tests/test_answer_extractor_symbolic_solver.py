import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.reasoning import AnswerExtractor
from src.reasoning.answer_comparator import compare_answers
from src.state import StateConstructor
from src.state.symbolic_state import SymbolicState
from src.theorems import TheoremLibrary


@pytest.fixture(scope="module")
def extractor():
    return AnswerExtractor()


@pytest.fixture(scope="module")
def constructor():
    return StateConstructor(theorem_library=TheoremLibrary())


REGRESSION_CASES = [
    (
        "C: Parabola;P: Point;Q: Point;F: Point;M: Point;N: Point;R: Point;l: Line;Expression(C) = (y^2 = 4*x);Focus(C) = F;Directrix(C) = l;PointOnCurve(P, C);IsPerpendicular(LineSegmentOf(P,Q),l);FootPoint(LineSegmentOf(P,Q),l)=Q;MidPoint(LineSegmentOf(P,Q))=M;MidPoint(LineSegmentOf(P,F))=N;Intersection(LineSegmentOf(M,N),xAxis)=R;AngleOf(N, R, F) = ApplyUnit(60, degree)",
        "LineSegmentOf(F, R)",
        "2",
    ),
    (
        "G: Parabola;Expression(G) = (y^2 = 4*x);A: Point;B: Point;IsChordOf(LineSegmentOf(A, B), G) = True;P: Point;Coordinate(P) = (1, 1);MidPoint(LineSegmentOf(A, B)) = P",
        "Slope(OverlappingLine(LineSegmentOf(A, B)))",
        "2",
    ),
    (
        "G: Hyperbola;H: Parabola;Expression(G) = (x^2/16 - y^2/9 = 1);LeftVertex(G) = Vertex(H);Focus(H) = RightFocus(G)",
        "Expression(H)",
        "y^2=-36*(x-4)",
    ),
    (
        "G: Ellipse;Expression(G) = (x^2/(2 - a) + y^2/(a - 1) = 1);a: Number",
        "Range(a)",
        "(1, 3/2)+(3/2, 2)",
    ),
    (
        "G: Hyperbola;a: Real;Expression(G) = (x^2/2 - y^2/a^2 = 1);Expression(OneOf(Asymptote(G))) = (y = sqrt(2)*x)",
        "a",
        "pm*2",
    ),
    (
        "G: Parabola;P: Point;Expression(G) = (y^2 = x);PointOnCurve(P, G);Distance(P, Focus(G)) = 2",
        "Coordinate(P)",
        "(7/4, pm*sqrt(7)/2)",
    ),
    (
        "G: Hyperbola;m: Number;Expression(G) = (m*y^2 + x^2 = 1);Length(ImageinaryAxis(G))*3 = FocalLength(G)",
        "m",
        "-8",
    ),
    (
        "G: Hyperbola;Expression(G) = (-y^2/b^2 + x^2/a^2 = 1);b: Number;a: Number;a>0;b>0;FocalLength(G) = 2*sqrt(5);2*Length(ImageinaryAxis(G)) = Length(RealAxis(G))",
        "Expression(G)",
        "x^2/4-y^2=1",
    ),
    (
        "G: Ellipse;Expression(G) = (4*x^2 + 9*y^2 = 36);G1: Ellipse;Focus(G) = Focus(G1);H: Point;Coordinate(H) = (-3, 2);PointOnCurve(H, G1) = True",
        "Expression(G1)",
        "x^2/15+y^2/10=1",
    ),
    (
        "G: Hyperbola;O: Origin;Center(G) = O;PointOnCurve(Focus(G),axis) = True;Eccentricity(G) = sqrt(2);H: Point;Coordinate(H) = (4, -sqrt(10));PointOnCurve(H,G) = True",
        "Expression(G)",
        "x^2/6-y^2/6=1",
    ),
    (
        "H: Ellipse;Expression(H) = (x^2 + 4*y^2 = 16);G: Hyperbola;Focus(G) = Focus(H);Expression(OneOf(Asymptote(G))) = (x + sqrt(3)*y = 0)",
        "Eccentricity(H);Expression(G)",
        "sqrt(3)/2\nx^2/9-y^2/3=1",
    ),
    (
        "C: Ellipse;Expression(C) = (y^2/b^2 + x^2/a^2 = 1);b: Number;a: Number;a > b;b > 0;F1: Point;F2: Point;Focus(C) = {F1, F2};H: Line;PointOnCurve(F1, H);A: Point;B: Point;Intersection(H, C) = {A, B};Perimeter(TriangleOf(A, B, F2)) = 12;Eccentricity(C) = sqrt(2)/3",
        "Expression(C)",
        "x^2/9+y^2/7=1",
    ),
    (
        "G: Hyperbola;H: Curve;k: Number;Expression(H) = (x^2/(k + 4) + y^2/(1 - k) = 1);H = G",
        "Range(k)",
        "(-oo, -4)+(1, +oo)",
    ),
    (
        "G: Hyperbola;a: Number;H: Parabola;a>0;Expression(G) = (-y^2/3 + x^2/a^2 = 1);Expression(H) = (y^2 = 8*x);Focus(H) = RightFocus(G)",
        "Expression(Asymptote(G))",
        "y=pm*sqrt(3)*x",
    ),
    (
        "G: Ellipse;b: Number;a: Number;A: Point;H:LineSegment;a > b;b > 0;Expression(G) = (x^2/b^2 + y^2/a^2 = 1);Coordinate(A) = (1, 0);RightVertex(G)=A;PointOnCurve(Focus(G),H);IsPerpendicular(H,MajorAxis(G));Length(H)=1;IsChordOf(l,G)",
        "Expression(G)",
        "y^2/4+x^2=1",
    ),
    (
        "G: Hyperbola;m: Number;Expression(G) = (x^2/16 + y^2/m = 1);Eccentricity(G) = 5/4",
        "m",
        "-9",
    ),
    (
        "H: Ellipse;Expression(H) = (x^2 + 4*y^2 = 16)",
        "Eccentricity(H)",
        "sqrt(3)/2",
    ),
    (
        "H: Ellipse;Expression(H) = (x^2 + 4*y^2 = 16)",
        "Coordinate(Focus(H))",
        "(pm*2*sqrt(3), 0)",
    ),
    (
        "G: Parabola;Expression(G) = (y^2 = 4*x)",
        "Distance(Focus(G), Directrix(G))",
        "2",
    ),
    (
        "G: Hyperbola;Expression(G) = (x^2/9 - y^2/4 = 1)",
        "Expression(Asymptote(G))",
        "y=pm*2/3*x",
    ),
    (
        "l: Line;C: Parabola;A: Point;B: Point;F: Point;Expression(C) = (y^2 = 4*x);Focus(C) = F;Expression(l) = (y = x - 1);Intersection(l, C) = {A, B}",
        "Abs(LineSegmentOf(A, B))",
        "8",
    ),
    (
        "G: Parabola;Expression(G) = (x^2 = 8*y);P: Point;PointOnCurve(P, G);A: Point;Coordinate(A) = (-2, 4);F: Point;Focus(G) = F",
        "Min(Abs(LineSegmentOf(P, A)) + Abs(LineSegmentOf(P, F)))",
        "6",
    ),
    (
        "G: Parabola;P: Point;F: Point;Expression(G) = (y^2 = 8*x);Focus(G) = F;PointOnCurve(P, G);XCoordinate(P)=4",
        "Abs(LineSegmentOf(P, F))",
        "6",
    ),
    (
        "G: Parabola;P: Point;F: Point;Expression(G) = (y^2 = 16*x);PointOnCurve(P, G);Distance(P, xAxis) = 12;Focus(G)=F;Distance(P,F)=Abs(LineSegmentOf(P,F))",
        "Abs(LineSegmentOf(P,F))",
        "13",
    ),
    (
        "l: Line;G: Parabola;A: Point;B: Point;F: Point;M: Point;Expression(G) = (y^2 = 8*x);Focus(G) = F;PointOnCurve(F, l);Intersection(l, G) = {A, B};MidPoint(LineSegmentOf(A, B)) = M;Distance(M, Directrix(G)) = 8",
        "Slope(l)",
        "pm*1",
    ),
    (
        "G: Parabola;Expression(G) = (y^2 = 2*(p*x));p: Number;p>0;P: Point;Q: Point;IsChordOf(LineSegmentOf(P, Q), G);x0: Number;y0: Number;Negation(y0=0);M: Point;Coordinate(M) = (x0, y0);MidPoint(LineSegmentOf(P, Q)) = M",
        "Slope(LineOf(P, Q))",
        "p/y0",
    ),
    (
        "G: Parabola;B: Point;A: Point;M: Point;Expression(G) = (x^2 = 4*y);Coordinate(M) = (2, 2);PointOnCurve(A, G);PointOnCurve(B, G);MidPoint(LineSegmentOf(A,B)) = M",
        "Abs(LineSegmentOf(A, B))",
        "4*sqrt(2)",
    ),
    (
        "G: Ellipse;k: Real;Expression(G) = (k*y^2 + 5*x^2 = 5);Coordinate(OneOf(Focus(G))) = (0, 2)",
        "k",
        "1",
    ),
]


@pytest.mark.parametrize("facts,query,expected", REGRESSION_CASES)
def test_answer_extractor_regression_cases(constructor, extractor, facts, query, expected):
    _, state = constructor.construct_from_facts(facts, query)
    predicted = extractor.extract(state, query)
    assert compare_answers(predicted, expected), f"predicted={predicted!r}, expected={expected!r}"


def test_coordinate_distance_and_area_from_symbolic_state(extractor):
    state = SymbolicState(
        coordinates={
            "A": ("0", "0"),
            "B": ("3", "0"),
            "C": ("0", "4"),
        }
    )
    assert compare_answers(extractor.extract(state, "Distance(A, C)"), "4")
    assert compare_answers(extractor.extract(state, "Area(TriangleOf(A, B, C))"), "6")
    assert compare_answers(extractor.extract(state, "Coordinate(B)"), "(3, 0)")


def test_direct_relation_values_are_preferred(extractor):
    state = SymbolicState(
        geometric_relations=[
            "Area(TriangleOf(A, B, C)) = sqrt(2)",
            "Distance(A, B) = 5",
        ]
    )
    assert compare_answers(extractor.extract(state, "Area(TriangleOf(A, B, C))"), "sqrt(2)")
    assert compare_answers(extractor.extract(state, "Distance(A, B)"), "5")


def test_unsupported_nested_optimization_reports_not_found(extractor):
    state = SymbolicState()
    result = extractor.extract(state, "Max(Length(LineSegmentOf(A, B)))")
    assert "not found" in result


def test_state_constructor_keeps_axis_coordinate_facts(constructor):
    _, state = constructor.construct_from_facts(
        "G: Parabola;P: Point;Expression(G) = (y^2 = 8*x);PointOnCurve(P, G);XCoordinate(P)=4",
        "Abs(LineSegmentOf(P, Focus(G)))",
    )
    assert "XCoordinate(P)=4" in [rel.replace(" ", "") for rel in state.geometric_relations]


def test_algebraic_expression_can_use_solved_line_segments(constructor, extractor):
    _, state = constructor.construct_from_facts(
        "l: Line;C: Parabola;A: Point;B: Point;Expression(C) = (y^2 = 4*x);Expression(l) = (y = x - 1);Intersection(l, C) = {A, B}",
        "Abs(LineSegmentOf(A, B))/2",
    )
    assert compare_answers(extractor.extract(state, "Abs(LineSegmentOf(A, B))/2"), "4")
