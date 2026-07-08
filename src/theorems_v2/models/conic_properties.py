"""Second-batch concrete conic property models for theorem v2."""

from __future__ import annotations

from typing import Any, Dict, Iterable, List, Tuple

from ..base import TheoremModelV2
from ..expressions import ConservativeSolver, add, div, equation, mul, neg
from ..schema import AxisLine, Derivation, Fact, StandardConicForm, StateDelta, Term
from ..state import InformationState
from .common import entities_of_type, parameter_fact, parameter_term, theorem_fact


def _form(state: InformationState, curve: str) -> tuple[Fact, StandardConicForm] | None:
    fact = state.get("ConicStandardForm", curve)
    if fact is None or not isinstance(fact.value, StandardConicForm):
        return None
    return fact, fact.value


def _point_facts(state: InformationState, curve: str) -> List[Fact]:
    return [
        fact
        for fact in state.find("PointOnCurve")
        if len(fact.arguments) == 2 and fact.arguments[1] == curve
    ]


class EccentricityRangeV2(TheoremModelV2):
    def __init__(self, model_id: int, curve_type: str):
        self.model_id = model_id
        self.curve_type = curve_type
        self.name = f"{curve_type}_Eccentricity_Range_V2"

    def match(self, state: InformationState) -> List[Dict[str, Any]]:
        return [{"G": curve} for curve in entities_of_type(state, self.curve_type)]

    def derive(self, state, binding, solver):
        curve = binding["G"]
        eccentricity = parameter_term(curve, "eccentricity")
        if self.curve_type == "Ellipse":
            relations = (
                Term("gt", (eccentricity, 0)),
                Term("lt", (eccentricity, 1)),
            )
        else:
            relations = (Term("gt", (eccentricity, 1)),)
        facts = tuple(
            theorem_fact(
                self.model_id,
                "OrderConstraint",
                relation,
            )
            for relation in relations
        )
        return Derivation(StateDelta(add_facts=facts))


class EllipseFocalRadiusV2(TheoremModelV2):
    model_id = 16
    name = "Ellipse_Focal_Radius_V2"

    def match(self, state):
        matches = []
        for curve in entities_of_type(state, "Ellipse"):
            form = _form(state, curve)
            a = parameter_fact(state, curve, "semi_axis_a")
            e = parameter_fact(state, curve, "eccentricity")
            c = parameter_fact(state, curve, "focal_half_distance")
            if form is None or a is None or (e is None and c is None):
                continue
            eccentricity = (
                e.value if e is not None else div(c.value, a.value)
            )
            parameter_evidence = e if e is not None else c
            for point in _point_facts(state, curve):
                matches.append(
                    {
                        "G": curve,
                        "P": point.arguments[0],
                        "form": form[1],
                        "a": a.value,
                        "e": eccentricity,
                        "_evidence": (form[0], a, parameter_evidence, point),
                    }
                )
        return matches

    def derive(self, state, binding, solver):
        point = binding["P"]
        coordinate = (
            Term("x_coordinate", (point,))
            if binding["form"].orientation == "horizontal"
            else Term("y_coordinate", (point,))
        )
        offset = solver.mul(binding["e"], coordinate)
        distances = (
            equation(Term("focal_radius", (binding["G"], point, "positive")), solver.add(binding["a"], offset)),
            equation(Term("focal_radius", (binding["G"], point, "negative")), solver.sub(binding["a"], offset)),
        )
        evidence = binding["_evidence"]
        fact = theorem_fact(
            self.model_id,
            "FocalRadiusRelation",
            binding["G"],
            point,
            value=distances,
            evidence=evidence,
        )
        return Derivation(StateDelta(add_facts=(fact,)), self.evidence(*evidence))


class ParabolaFocalRadiusV2(TheoremModelV2):
    model_id = 17
    name = "Parabola_Focal_Radius_V2"

    def match(self, state):
        matches = []
        for curve in entities_of_type(state, "Parabola"):
            form = _form(state, curve)
            if form is None or form[1].focus_offset is None:
                continue
            for point in _point_facts(state, curve):
                matches.append(
                    {"G": curve, "P": point.arguments[0], "form": form[1], "_evidence": (form[0], point)}
                )
        return matches

    def derive(self, state, binding, solver):
        form = binding["form"]
        point = binding["P"]
        axis = "x_coordinate" if form.orientation in {"right", "left"} else "y_coordinate"
        coordinate = Term(axis, (point,))
        signed_coordinate = neg(coordinate) if form.orientation in {"left", "down"} else coordinate
        relation = equation(
            Term("distance_to_focus", (point, binding["G"])),
            solver.add(signed_coordinate, form.focus_offset),
        )
        evidence = binding["_evidence"]
        fact = theorem_fact(self.model_id, "FocalRadiusRelation", binding["G"], point, value=relation, evidence=evidence)
        return Derivation(StateDelta(add_facts=(fact,)), self.evidence(*evidence))


class LatusRectumV2(TheoremModelV2):
    def __init__(self, model_id: int, curve_type: str):
        self.model_id = model_id
        self.curve_type = curve_type
        self.name = f"{curve_type}_Latus_Rectum_V2"

    def match(self, state):
        matches = []
        for curve in entities_of_type(state, self.curve_type):
            form = _form(state, curve)
            if form is not None:
                matches.append({"G": curve, "form": form[1], "_evidence": (form[0],)})
        return matches

    def derive(self, state, binding, solver):
        form = binding["form"]
        if self.curve_type == "Parabola":
            length = form.two_p
        else:
            length = solver.div(solver.mul(2, form.b2), solver.sqrt_positive(form.a2))
        evidence = binding["_evidence"]
        fact = theorem_fact(self.model_id, "LatusRectumLengthOf", binding["G"], value=length, evidence=evidence)
        return Derivation(StateDelta(add_facts=(fact,)), self.evidence(*evidence))


class HyperbolaFocusAsymptoteDistanceV2(TheoremModelV2):
    model_id = 22
    name = "Hyperbola_Focus_To_Asymptote_Distance_V2"

    def match(self, state):
        matches = []
        for curve in entities_of_type(state, "Hyperbola"):
            form = _form(state, curve)
            if form is not None:
                matches.append({"G": curve, "form": form[1], "_evidence": (form[0],)})
        return matches

    def derive(self, state, binding, solver):
        evidence = binding["_evidence"]
        distance = solver.sqrt_positive(binding["form"].b2)
        fact = theorem_fact(self.model_id, "FocusAsymptoteDistanceOf", binding["G"], value=distance, evidence=evidence)
        return Derivation(StateDelta(add_facts=(fact,)), self.evidence(*evidence))


class HyperbolaCommonAsymptoteSystemV2(TheoremModelV2):
    model_id = 23
    name = "Hyperbola_Common_Asymptote_System_V2"

    def match(self, state):
        return [{"G": curve, "form": form[1], "_evidence": (form[0],)} for curve in entities_of_type(state, "Hyperbola") if (form := _form(state, curve)) is not None]

    def derive(self, state, binding, solver):
        form = binding["form"]
        relation = Term("common_asymptote_system", (binding["G"], form.a2, form.b2, Term("symbol", ("lambda",))))
        evidence = binding["_evidence"]
        fact = theorem_fact(self.model_id, "CommonAsymptoteSystemOf", binding["G"], value=relation, evidence=evidence)
        return Derivation(StateDelta(add_facts=(fact,)), self.evidence(*evidence))


class HyperbolaEqualAxisV2(TheoremModelV2):
    model_id = 24
    name = "Hyperbola_Equal_Axis_V2"

    def match(self, state):
        matches = []
        solver = ConservativeSolver()
        for curve in entities_of_type(state, "Hyperbola"):
            form = _form(state, curve)
            if form is not None and solver.equivalent(form[1].a2, form[1].b2):
                matches.append({"G": curve, "_evidence": (form[0],)})
        return matches

    def derive(self, state, binding, solver):
        evidence = binding["_evidence"]
        facts = (
            theorem_fact(self.model_id, "EqualAxisOf", binding["G"], value=True, evidence=evidence),
            theorem_fact(self.model_id, "ParameterOf", binding["G"], "eccentricity", value=Term("sqrt_positive", (2,)), evidence=evidence),
        )
        return Derivation(StateDelta(add_facts=facts), self.evidence(*evidence))


class SecondDefinitionV2(TheoremModelV2):
    def __init__(self, model_id: int, curve_type: str):
        self.model_id = model_id
        self.curve_type = curve_type
        self.name = f"{curve_type}_Second_Definition_V2"

    def match(self, state):
        matches = []
        for curve in entities_of_type(state, self.curve_type):
            eccentricity = parameter_fact(state, curve, "eccentricity")
            if eccentricity is None:
                continue
            for point in _point_facts(state, curve):
                matches.append({"G": curve, "P": point.arguments[0], "e": eccentricity.value, "_evidence": (eccentricity, point)})
        return matches

    def derive(self, state, binding, solver):
        relation = equation(
            div(Term("distance_to_focus", (binding["P"], binding["G"])), Term("distance_to_directrix", (binding["P"], binding["G"]))),
            binding["e"],
        )
        evidence = binding["_evidence"]
        fact = theorem_fact(self.model_id, "SecondDefinitionRelation", binding["G"], binding["P"], value=relation, evidence=evidence)
        return Derivation(StateDelta(add_facts=(fact,)), self.evidence(*evidence))


class ConicDirectrixV2(TheoremModelV2):
    def __init__(self, model_id: int, curve_type: str):
        self.model_id = model_id
        self.curve_type = curve_type
        self.name = f"{curve_type}_Directrix_V2"

    def match(self, state):
        matches = []
        for curve in entities_of_type(state, self.curve_type):
            form = _form(state, curve)
            c = parameter_fact(state, curve, "focal_half_distance")
            a = parameter_fact(state, curve, "semi_axis_a")
            e = parameter_fact(state, curve, "eccentricity")
            if form is None:
                continue
            if c is not None:
                matches.append({"G": curve, "form": form[1], "c": c.value, "_evidence": (form[0], c)})
            elif a is not None and e is not None:
                matches.append({"G": curve, "form": form[1], "c": div(a.value, div(1, e.value)), "_evidence": (form[0], a, e)})
        return matches

    def derive(self, state, binding, solver):
        form = binding["form"]
        value = solver.div(form.a2, binding["c"])
        axis = "x" if form.orientation == "horizontal" else "y"
        lines = (AxisLine(axis, value), AxisLine(axis, neg(value)))
        evidence = binding["_evidence"]
        fact = theorem_fact(self.model_id, "DirectrixFamilyOf", binding["G"], value=lines, evidence=evidence)
        return Derivation(StateDelta(add_facts=(fact,)), self.evidence(*evidence))


class EllipseFocalTrianglePerimeterV2(TheoremModelV2):
    model_id = 32
    name = "Ellipse_Focal_Triangle_Perimeter_V2"

    def match(self, state):
        matches = []
        for curve in entities_of_type(state, "Ellipse"):
            a = parameter_fact(state, curve, "semi_axis_a")
            c = parameter_fact(state, curve, "focal_half_distance")
            if a is not None and c is not None:
                matches.append({"G": curve, "a": a.value, "c": c.value, "_evidence": (a, c)})
        return matches

    def derive(self, state, binding, solver):
        evidence = binding["_evidence"]
        value = solver.mul(2, solver.add(binding["a"], binding["c"]))
        fact = theorem_fact(self.model_id, "FocalTrianglePerimeterOf", binding["G"], value=value, evidence=evidence)
        return Derivation(StateDelta(add_facts=(fact,)), self.evidence(*evidence))


class EllipseParametricEquationV2(TheoremModelV2):
    model_id = 37
    name = "Ellipse_Parametric_Equation_V2"

    def match(self, state):
        matches = []
        for curve in entities_of_type(state, "Ellipse"):
            form = _form(state, curve)
            if form is not None:
                matches.append({"G": curve, "form": form[1], "_evidence": (form[0],)})
        return matches

    def derive(self, state, binding, solver):
        form = binding["form"]
        t = Term("symbol", ("t",))
        x = mul(solver.sqrt_positive(form.a2), Term("cos", (t,)))
        y = mul(solver.sqrt_positive(form.b2), Term("sin", (t,)))
        evidence = binding["_evidence"]
        fact = theorem_fact(self.model_id, "ParametricExpressionOf", binding["G"], value=(x, y), evidence=evidence)
        return Derivation(StateDelta(add_facts=(fact,)), self.evidence(*evidence))


class EllipseTangentLineV2(TheoremModelV2):
    model_id = 38
    name = "Ellipse_Tangent_Line_V2"

    def match(self, state):
        matches = []
        for curve in entities_of_type(state, "Ellipse"):
            form = _form(state, curve)
            if form is None:
                continue
            for point in _point_facts(state, curve):
                coordinate = state.get("CoordinateOf", point.arguments[0])
                if coordinate is not None:
                    matches.append({"G": curve, "P": point.arguments[0], "coordinate": coordinate.value, "form": form[1], "_evidence": (form[0], point, coordinate)})
        return matches

    def derive(self, state, binding, solver):
        x0, y0 = binding["coordinate"]
        relation = equation(
            add(div(mul(x0, Term("symbol", ("x",))), binding["form"].a2), div(mul(y0, Term("symbol", ("y",))), binding["form"].b2)),
            1,
        )
        evidence = binding["_evidence"]
        fact = theorem_fact(self.model_id, "TangentExpressionOf", binding["G"], binding["P"], value=relation, evidence=evidence)
        return Derivation(StateDelta(add_facts=(fact,)), self.evidence(*evidence))


class ParabolaTangentLineV2(TheoremModelV2):
    model_id = 39
    name = "Parabola_Tangent_Line_V2"

    def match(self, state):
        matches = []
        for curve in entities_of_type(state, "Parabola"):
            form = _form(state, curve)
            if form is None:
                continue
            for point in _point_facts(state, curve):
                coordinate = state.get("CoordinateOf", point.arguments[0])
                if coordinate is not None:
                    matches.append({"G": curve, "P": point.arguments[0], "coordinate": coordinate.value, "form": form[1], "_evidence": (form[0], point, coordinate)})
        return matches

    def derive(self, state, binding, solver):
        x0, y0 = binding["coordinate"]
        form = binding["form"]
        x, y = Term("symbol", ("x",)), Term("symbol", ("y",))
        if form.orientation in {"right", "left"}:
            signed_p = form.two_p if form.orientation == "right" else neg(form.two_p)
            relation = equation(mul(y0, y), mul(div(signed_p, 2), add(x, x0)))
        else:
            signed_p = form.two_p if form.orientation == "up" else neg(form.two_p)
            relation = equation(mul(x0, x), mul(div(signed_p, 2), add(y, y0)))
        evidence = binding["_evidence"]
        fact = theorem_fact(self.model_id, "TangentExpressionOf", binding["G"], binding["P"], value=relation, evidence=evidence)
        return Derivation(StateDelta(add_facts=(fact,)), self.evidence(*evidence))


def second_batch_models() -> List[TheoremModelV2]:
    return [
        EccentricityRangeV2(14, "Ellipse"),
        EccentricityRangeV2(15, "Hyperbola"),
        EllipseFocalRadiusV2(),
        ParabolaFocalRadiusV2(),
        LatusRectumV2(18, "Ellipse"),
        LatusRectumV2(19, "Hyperbola"),
        LatusRectumV2(20, "Parabola"),
        HyperbolaFocusAsymptoteDistanceV2(),
        HyperbolaCommonAsymptoteSystemV2(),
        HyperbolaEqualAxisV2(),
        SecondDefinitionV2(25, "Ellipse"),
        SecondDefinitionV2(26, "Hyperbola"),
        ConicDirectrixV2(27, "Ellipse"),
        ConicDirectrixV2(28, "Hyperbola"),
        EllipseFocalTrianglePerimeterV2(),
        EllipseParametricEquationV2(),
        EllipseTangentLineV2(),
        ParabolaTangentLineV2(),
    ]
