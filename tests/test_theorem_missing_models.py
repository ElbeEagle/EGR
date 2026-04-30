import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.state.symbolic_state import SymbolicState
from src.theorems.models.model_018 import EllipseLatusRectum
from src.theorems.models.model_027 import EllipseDirectrix
from src.theorems.models.model_038 import EllipseTangentLine
from src.theorems.models.model_064 import BasicInequalityEqualCondition


def test_ellipse_latus_rectum_writes_structured_parameter():
    state = SymbolicState(
        entities={"E": "Ellipse"},
        parameters={"a": "2", "b^2": "3"},
    )
    model = EllipseLatusRectum()

    assert model.can_apply(state)
    assert model.apply(state)
    assert state.parameters["ellipse_latus_rectum"] == "3"
    assert state.parameters["latus_rectum"] == "3"
    assert any("EllipseLatusRectum" in rel for rel in state.geometric_relations)


def test_ellipse_directrix_uses_axis_and_derives_c():
    state = SymbolicState(
        entities={"E": "Ellipse"},
        equations=["Expression(E) = (x^2/9 + y^2/5 = 1)"],
        parameters={"a^2": "9", "b^2": "5"},
        geometric_relations=["焦点在x轴"],
    )
    model = EllipseDirectrix()

    assert model.can_apply(state)
    assert model.apply(state)
    assert state.parameters["c"] == "2"
    assert state.parameters["directrix_axis"] == "x"
    assert state.parameters["directrix_distance"] == "4.5"
    assert "Expression(Directrix(E)) = (x = pm*(4.5))" in state.equations


def test_ellipse_tangent_line_from_named_point():
    state = SymbolicState(
        entities={"E": "Ellipse", "P": "Point"},
        parameters={"a^2": "4", "b^2": "3"},
        coordinates={"P": ("1", "sqrt(3)/2")},
        geometric_relations=["PointOnCurve(P, E)", "TangentAt(P, E)"],
    )
    model = EllipseTangentLine()

    assert model.can_apply(state)
    assert model.apply(state)
    expected = "(1)*x/4 + (sqrt(3)/2)*y/3 = 1"
    assert state.parameters["tangent_point"] == "P"
    assert state.parameters["tangent_line"] == expected
    assert f"Expression(TangentLine(E, P)) = ({expected})" in state.equations


def test_basic_inequality_equal_condition_writes_constraint():
    state = SymbolicState(
        geometric_relations=["BasicInequality: a + b >= 2*sqrt(a*b)"],
        parameters={"amgm_terms": ("m", "n")},
    )
    model = BasicInequalityEqualCondition()

    assert model.can_apply(state)
    assert model.apply(state)
    assert state.parameters["basic_inequality_equality_condition"] == "m = n"
    assert "m = n" in state.constraints
    assert any(
        relation == "BasicInequalityEqualityCondition: m = n"
        for relation in state.geometric_relations
    )
