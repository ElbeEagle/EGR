from fractions import Fraction

import pytest

from src.theorems_v2 import (
    ApplicationStatus,
    ApplicatorV2,
    AxisLine,
    InformationState,
    LineThroughOrigin,
    PolynomialEquation,
    TheoremLibraryV2,
)


def apply_model(library, applicator, state, model_id):
    result = applicator.apply(library.get_model(model_id), state)
    assert result.status == ApplicationStatus.APPLIED, result
    assert result.state_after is not None
    return result.state_after


def conic_state(curve_type, polynomial):
    state = InformationState().declare("G", curve_type)
    state.add_given("ExpressionPolynomial", "G", value=polynomial)
    return state


def test_v2_library_is_separate_and_registers_first_batch():
    library = TheoremLibraryV2()
    assert library.get_available_models() == [
        *range(14),
        21,
        29,
        75,
    ]


@pytest.mark.parametrize(
    ("model_id", "curve_type", "polynomial", "orientation"),
    [
        (3, "Ellipse", PolynomialEquation(x2=Fraction(1, 9), y2=Fraction(1, 5), constant=-1), "horizontal"),
        (4, "Ellipse", PolynomialEquation(x2=Fraction(1, 5), y2=Fraction(1, 9), constant=-1), "vertical"),
        (5, "Hyperbola", PolynomialEquation(x2=Fraction(1, 4), y2=Fraction(-1, 25), constant=-1), "horizontal"),
        (6, "Hyperbola", PolynomialEquation(x2=Fraction(-1, 25), y2=Fraction(1, 4), constant=-1), "vertical"),
    ],
)
def test_centered_conic_equation_models(model_id, curve_type, polynomial, orientation):
    library = TheoremLibraryV2()
    original = conic_state(curve_type, polynomial)

    result = ApplicatorV2().apply(library.get_model(model_id), original)

    assert result.status == ApplicationStatus.APPLIED
    assert original.get("ConicStandardForm", "G") is None
    state = result.state_after
    assert state.value("ConicStandardForm", "G").orientation == orientation
    assert state.value("ParameterOf", "G", "semi_axis_a_squared") == 9 if curve_type == "Ellipse" else 4


@pytest.mark.parametrize(
    ("model_id", "polynomial", "direction"),
    [
        (7, PolynomialEquation(y2=1, x=-8), "right"),
        (8, PolynomialEquation(y2=1, x=8), "left"),
        (9, PolynomialEquation(x2=1, y=-8), "up"),
        (10, PolynomialEquation(x2=1, y=8), "down"),
    ],
)
def test_parabola_direction_models(model_id, polynomial, direction):
    library = TheoremLibraryV2()
    state = apply_model(
        library,
        ApplicatorV2(),
        conic_state("Parabola", polynomial),
        model_id,
    )

    form = state.value("ConicStandardForm", "G")
    assert form.orientation == direction
    assert state.value("ParameterOf", "G", "two_p") == 8
    assert state.value("ParameterOf", "G", "p") == 4
    assert state.value("FocusOffsetOf", "G") == 2


def test_hyperbola_standard_to_asymptote_is_auditable_and_idempotent():
    library = TheoremLibraryV2()
    applicator = ApplicatorV2()
    state = conic_state(
        "Hyperbola",
        PolynomialEquation(
            x2=Fraction(1, 4), y2=Fraction(-1, 25), constant=-1
        ),
    )
    state = apply_model(library, applicator, state, 5)
    state = apply_model(library, applicator, state, 21)

    lines = state.value("AsymptoteFamilyOf", "G")
    assert lines == (
        LineThroughOrigin("y", Fraction(5, 2)),
        LineThroughOrigin("y", Fraction(-5, 2)),
    )
    repeated = applicator.apply(library.get_model(21), state)
    assert repeated.status == ApplicationStatus.ALREADY_KNOWN
    assert repeated.state_after is state


def test_ellipse_parameter_relation_then_eccentricity():
    library = TheoremLibraryV2()
    applicator = ApplicatorV2()
    state = conic_state(
        "Ellipse",
        PolynomialEquation(
            x2=Fraction(1, 9), y2=Fraction(1, 5), constant=-1
        ),
    )
    state = apply_model(library, applicator, state, 3)
    state = apply_model(library, applicator, state, 11)
    assert state.value("ParameterOf", "G", "focal_half_distance_squared") == 4
    assert state.value("ParameterOf", "G", "focal_half_distance") == 2

    state = apply_model(library, applicator, state, 13)
    assert state.value("ParameterOf", "G", "eccentricity") == Fraction(2, 3)


def test_parabola_directrix_uses_explicit_direction():
    library = TheoremLibraryV2()
    applicator = ApplicatorV2()
    state = apply_model(
        library,
        applicator,
        conic_state("Parabola", PolynomialEquation(y2=1, x=-8)),
        7,
    )
    state = apply_model(library, applicator, state, 29)

    assert state.value("DirectrixExpressionOf", "G") == AxisLine("x", -2)


def test_circle_general_equation_is_completed_by_model_75():
    library = TheoremLibraryV2()
    state = apply_model(
        library,
        ApplicatorV2(),
        conic_state(
            "Circle",
            PolynomialEquation(x2=1, y2=1, x=-6, constant=-7),
        ),
        75,
    )

    assert state.value("CenterCoordinateOf", "G") == (3, 0)
    assert state.value("ParameterOf", "G", "radius_squared") == 16
    assert state.value("ParameterOf", "G", "radius") == 4


def test_conflict_does_not_mutate_original_state():
    library = TheoremLibraryV2()
    state = conic_state(
        "Hyperbola",
        PolynomialEquation(
            x2=Fraction(1, 4), y2=Fraction(-1, 25), constant=-1
        ),
    )
    state.add_given(
        "ParameterOf", "G", "semi_axis_a_squared", value=99
    )

    result = ApplicatorV2().apply(library.get_model(5), state)

    assert result.status == ApplicationStatus.CONFLICT
    assert result.state_after is None
    assert state.value("ParameterOf", "G", "semi_axis_a_squared") == 99
    assert state.get("ConicStandardForm", "G") is None


def test_parabola_definition_requires_bound_point_focus_and_directrix():
    library = TheoremLibraryV2()
    state = InformationState()
    state.declare("G", "Parabola").declare("P", "Point")
    state.declare("F", "Point").declare("L", "Line")
    state.add_given("PointOnCurve", "P", "G", value=True)
    state.add_given("FocusOf", "G", "F", value=True)
    state.add_given("DirectrixOf", "G", "L", value=True)

    state = apply_model(library, ApplicatorV2(), state, 2)

    assert state.get("DefinitionRelation", "G", "P") is not None
