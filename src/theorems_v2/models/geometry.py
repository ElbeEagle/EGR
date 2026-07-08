"""High-frequency geometry models 21 and 29."""

from __future__ import annotations

from dataclasses import replace

from typing import Any, Dict, List

from ..base import TheoremModelV2
from ..expressions import ConservativeSolver, equation, mul, neg
from ..schema import (
    AxisLine,
    Derivation,
    LineThroughOrigin,
    StandardConicForm,
    StateDelta,
)
from ..state import InformationState
from .common import entities_of_type, parameter_fact, parameter_term, theorem_fact


class HyperbolaAsymptoteV2(TheoremModelV2):
    model_id = 21
    name = "Hyperbola_Asymptote_V2"

    def match(self, state: InformationState) -> List[Dict[str, Any]]:
        matches: List[Dict[str, Any]] = []
        for curve in entities_of_type(state, "Hyperbola"):
            form_fact = state.get("ConicStandardForm", curve)
            if form_fact is None or not isinstance(
                form_fact.value, StandardConicForm
            ):
                continue
            form = form_fact.value
            if form.curve_type != "hyperbola" or form.a2 is None or form.b2 is None:
                continue
            a2_fact = parameter_fact(state, curve, "semi_axis_a_squared")
            b2_fact = parameter_fact(state, curve, "semi_axis_b_squared")
            form = replace(
                form,
                a2=form.a2 if a2_fact is None else a2_fact.value,
                b2=form.b2 if b2_fact is None else b2_fact.value,
            )
            linked_lines = state.find("AsymptoteOf", curve)
            evidence = [form_fact]
            evidence.extend(linked_lines)
            for line_fact in linked_lines:
                line = line_fact.arguments[1]
                slope_fact = state.get("SlopeOf", line)
                if slope_fact is not None:
                    evidence.append(slope_fact)
            matches.append(
                {
                    "G": curve,
                    "form": form,
                    "linked_lines": tuple(linked_lines),
                    "_evidence": tuple(evidence),
                }
            )
        return matches

    def derive(
        self,
        state: InformationState,
        binding: Dict[str, Any],
        solver: ConservativeSolver,
    ) -> Derivation:
        curve = binding["G"]
        form = binding["form"]
        evidence = binding["_evidence"]
        if form.orientation == "horizontal":
            slope_squared = solver.div(form.b2, form.a2)
        elif form.orientation == "vertical":
            slope_squared = solver.div(form.a2, form.b2)
        else:
            raise ValueError(f"unknown hyperbola orientation: {form.orientation}")
        slope = solver.sqrt_positive(slope_squared)
        lines = (
            LineThroughOrigin("y", slope),
            LineThroughOrigin("y", neg(slope)),
        )
        facts = [
            theorem_fact(
                self.model_id,
                "AsymptoteFamilyOf",
                curve,
                value=lines,
                evidence=evidence,
            )
        ]
        for line_fact in binding["linked_lines"]:
            line = line_fact.arguments[1]
            slope_fact = state.get("SlopeOf", line)
            if slope_fact is None:
                continue
            given_slope_squared = solver.square(slope_fact.value)
            a2_term = parameter_term(curve, "semi_axis_a_squared")
            b2_term = parameter_term(curve, "semi_axis_b_squared")
            if form.orientation == "horizontal":
                constraint = equation(
                    mul(given_slope_squared, a2_term), b2_term
                )
            else:
                constraint = equation(
                    mul(given_slope_squared, b2_term), a2_term
                )
            axis_ratio = (
                given_slope_squared
                if form.orientation == "horizontal"
                else solver.div(1, given_slope_squared)
            )
            facts.append(
                theorem_fact(
                    self.model_id,
                    "ParameterRatioOf",
                    curve,
                    "b2_over_a2",
                    value=axis_ratio,
                    evidence=(line_fact, slope_fact),
                )
            )
            facts.append(
                theorem_fact(
                    self.model_id,
                    "EquationConstraint",
                    constraint,
                    evidence=(line_fact, slope_fact),
                )
            )
        return Derivation(
            StateDelta(add_facts=tuple(facts)), self.evidence(*evidence)
        )


class ParabolaDirectrixV2(TheoremModelV2):
    model_id = 29
    name = "Parabola_Directrix_V2"

    def match(self, state: InformationState) -> List[Dict[str, Any]]:
        matches: List[Dict[str, Any]] = []
        for curve in entities_of_type(state, "Parabola"):
            form_fact = state.get("ConicStandardForm", curve)
            if form_fact is None or not isinstance(
                form_fact.value, StandardConicForm
            ):
                continue
            form = form_fact.value
            if form.curve_type != "parabola" or form.focus_offset is None:
                continue
            directrices = state.find("DirectrixOf", curve)
            distance = state.get("FocusDirectrixDistanceOf", curve)
            matches.append(
                {
                    "G": curve,
                    "form": form,
                    "directrices": tuple(directrices),
                    "focus_directrix_distance": (
                        distance.value if distance is not None else None
                    ),
                    "_evidence": (
                        form_fact,
                        *directrices,
                        *((distance,) if distance is not None else ()),
                    ),
                }
            )
        return matches

    def derive(
        self,
        state: InformationState,
        binding: Dict[str, Any],
        solver: ConservativeSolver,
    ) -> Derivation:
        curve = binding["G"]
        form = binding["form"]
        evidence = binding["_evidence"]
        mapping = {
            "right": AxisLine("x", neg(form.focus_offset)),
            "left": AxisLine("x", form.focus_offset),
            "up": AxisLine("y", neg(form.focus_offset)),
            "down": AxisLine("y", form.focus_offset),
        }
        if form.orientation not in mapping:
            raise ValueError(f"unknown parabola direction: {form.orientation}")
        expression = mapping[form.orientation]
        facts = [
            theorem_fact(
                self.model_id,
                "DirectrixExpressionOf",
                curve,
                value=expression,
                evidence=evidence,
            )
        ]
        for directrix_fact in binding["directrices"]:
            line = directrix_fact.arguments[1]
            facts.append(
                theorem_fact(
                    self.model_id,
                    "ExpressionOf",
                    line,
                    value=expression,
                    evidence=(directrix_fact,),
                )
            )
        if binding["focus_directrix_distance"] is not None:
            facts.append(
                theorem_fact(
                    self.model_id,
                    "EquationConstraint",
                    equation(
                        parameter_term(curve, "p"),
                        binding["focus_directrix_distance"],
                    ),
                    evidence=evidence,
                )
            )
        return Derivation(
            StateDelta(add_facts=tuple(facts)), self.evidence(*evidence)
        )