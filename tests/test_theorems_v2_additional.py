from fractions import Fraction

import pytest

from src.theorems_v2 import (
    ApplicationStatus,
    ApplicatorV2,
    InformationState,
    PolynomialEquation,
    TheoremLibraryV2,
)


def applied(library, state, model_id):
    result = ApplicatorV2().apply(library.get_model(model_id), state)
    assert result.status == ApplicationStatus.APPLIED, result
    return result.state_after


@pytest.mark.parametrize(
    ("model_id", "curve_type"),
    [(0, "Ellipse"), (1, "Hyperbola")],
)
def test_two_focus_definition_models(model_id, curve_type):
    library = TheoremLibraryV2()
    state = InformationState()
    for name, type_name in (
        ("G", curve_type),
        ("P", "Point"),
        ("F1", "Point"),
        ("F2", "Point"),
    ):
        state.declare(name, type_name)
    state.add_given("PointOnCurve", "P", "G", value=True)
    state.add_given("FocusOf", "G", "F1", value=True)
    state.add_given("FocusOf", "G", "F2", value=True)
    state.add_given("ParameterOf", "G", "semi_axis_a", value=5)

    state = applied(library, state, model_id)

    assert state.get("DefinitionRelation", "G", "P") is not None


def test_hyperbola_parameter_relation_then_eccentricity():
    library = TheoremLibraryV2()
    state = InformationState().declare("G", "Hyperbola")
    state.add_given(
        "ParameterOf", "G", "semi_axis_a_squared", value=4
    )
    state.add_given(
        "ParameterOf", "G", "semi_axis_b_squared", value=5
    )

    state = applied(library, state, 12)
    assert state.value("ParameterOf", "G", "focal_half_distance_squared") == 9
    assert state.value("ParameterOf", "G", "focal_half_distance") == 3

    state = applied(library, state, 13)
    assert state.value("ParameterOf", "G", "eccentricity") == Fraction(3, 2)


def test_asymptote_model_adds_given_line_matching_constraint():
    library = TheoremLibraryV2()
    state = InformationState().declare("G", "Hyperbola")
    state.add_given(
        "ExpressionPolynomial",
        "G",
        value=PolynomialEquation(
            x2=Fraction(1, 4),
            y2=Fraction(-1, 25),
            constant=-1,
        ),
    )
    state = applied(library, state, 5)
    state.declare("L", "Line")
    state.add_given("AsymptoteOf", "G", "L", value=True)
    state.add_given("SlopeOf", "L", value=Fraction(5, 2))

    state = applied(library, state, 21)

    constraints = state.find("EquationConstraint")
    assert constraints
    assert any(
        fact.provenance.source_id == "21" for fact in constraints
    )
