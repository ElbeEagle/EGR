"""Y-axis conics: real cases, axis symmetry, and incompatible bindings."""
from copy import deepcopy
from dataclasses import replace
import json
from pathlib import Path

import pytest
import sympy as sp

from src.reasoning.bound_slice import (
    solve_forward_asymptote_slice, solve_asymptote_slice, solve_shared_focus_slice,
    select_standard_action,
)
from src.state.transition_state import TransitionState
from src.theorems.bound_application import BoundAction, BoundApplicator, enumerate_actions

DATA = Path(__file__).resolve().parents[1] / 'data/train_with_models_v3.json'


def state_for(kind, equation):
    return TransitionState.from_facts(f'G: {kind};t: Real;Expression(G)=({equation})', 't')


@pytest.mark.parametrize('pid,slope', [(380, sp.sqrt(2)/2), (549, sp.sqrt(5)/2)])
def test_real_y_hyperbola_forward(pid, slope):
    row = next(r for r in json.loads(DATA.read_text()) if r['id'] == pid)
    result = solve_forward_asymptote_slice(row['fact_expressions'], row['query_expressions'])
    assert result.status == 'solved'
    assert [t.action.model_id for t in result.transitions] == [6, 21]
    assert result.state.frames['G'].axis == 'y'
    x, y = result.state.symbols['x'], result.state.symbols['y']
    assert all(sp.simplify(a-b) == 0 for a, b in zip(result.answer, (y-slope*x, y+slope*x)))
    assert result.transitions[-1].operations[0]['axis'] == 'y'


def test_real_id1516_parameter_subchain_only():
    row = next(r for r in json.loads(DATA.read_text()) if r['id'] == 1516)
    # Original length query is outside this parser. Add only a diagnostic scalar
    # declaration, not a derived mathematical fact or an answer from the record.
    s = TransitionState.from_facts(row['fact_expressions'] + ';probe: Real', 'probe')
    app = BoundApplicator()
    action = select_standard_action(s, 'G', next(iter(s.equations)))
    assert action.model_id == 4 and not s.properties and not s.history
    assert app.apply(s, action).status == 'applied'
    assert app.apply(s, BoundAction(11, 'derive_c_sq', 'G', action.equation_id)).status == 'applied'
    assert s.properties == {('G', 'a_sq'): 25, ('G', 'b_sq'): 16, ('G', 'c_sq'): 9}
    assert s.extract_answer() is None


@pytest.mark.parametrize('mid,kind,eq,params', [
    (4, 'Ellipse', 'y^2/25+x^2/9=1', (25, 9, 16)),
    (6, 'Hyperbola', 'y^2/9-x^2/16=1', (9, 16, 25)),
])
@pytest.mark.parametrize('target', ['a_sq', 'b_sq', 'c_sq'])
def test_y_axis_reuses_all_parameter_directions(mid, kind, eq, params, target):
    s, app = state_for(kind, eq), BoundApplicator()
    extract = enumerate_actions(s, mid)[0]
    assert app.apply(s, extract).status == 'applied'
    relation_id = 11 if kind == 'Ellipse' else 12
    assert app.apply(s, BoundAction(relation_id, 'derive_c_sq', 'G', extract.equation_id)).status == 'applied'
    del s.properties['G', target]
    result = app.apply(s, BoundAction(relation_id, 'derive_' + target, 'G', extract.equation_id))
    assert result.status == 'applied'
    assert tuple(s.properties['G', k] for k in ('a_sq', 'b_sq', 'c_sq')) == params


def test_y_axis_parameter_constraint_solves_symbol():
    s, app = state_for('Hyperbola', 'y^2/7-x^2/t=1'), BoundApplicator()
    extract = enumerate_actions(s, 6)[0]
    assert app.apply(s, extract).status == 'applied'
    s.properties['G', 'c_sq'] = sp.Integer(16)  # Explicit upstream fixture.
    result = app.apply(s, BoundAction(12, 'constrain_parameters', 'G', extract.equation_id))
    assert result.status == 'applied' and s.extract_answer() == 9


@pytest.mark.parametrize('condition,answer,roots', [('', None, (-3, 3)), (';m>0', 3, (3,)), (';m<0', -3, (-3,))])
def test_y_inverse_uses_reciprocal_slope_relation(condition, answer, roots):
    result = solve_asymptote_slice(
        'G: Hyperbola;m: Real;Expression(G)=(y^2/4-x^2/m^2=1);'
        'Expression(OneOf(Asymptote(G)))=(2*x-3*y=0)' + condition, 'm')
    assert result.answer == answer
    assert result.transitions[-1].candidates == roots
    assert result.transitions[0].action.model_id == 6


def test_y_shared_focus_chain_and_original_x_chain_are_symmetric():
    facts = ('G: Hyperbola;t: Real;H: Ellipse;Expression(G)=(y^2/7-x^2/t=1);'
             'Expression(H)=(y^2/25+x^2/9=1);Focus(G)=Focus(H)')
    result = solve_shared_focus_slice(facts, 't')
    assert result.answer == 9
    assert [r.action.model_id for r in result.transitions] == [4, 11, 6, 12]
    assert all(f.axis == 'y' for f in result.state.frames.values())
    operation = result.transitions[-1].operations[0]
    assert operation['operation'] == 'instantiate_shared_focus' and operation['axis'] == 'y'


def test_different_focal_axes_cannot_share_focal_parameter():
    facts = ('G: Hyperbola;t: Real;H: Ellipse;Expression(G)=(y^2/7-x^2/t=1);'
             'Expression(H)=(x^2/25+y^2/9=1);Focus(G)=Focus(H)')
    result = solve_shared_focus_slice(facts, 't')
    assert result.status == 'inapplicable' and result.answer is None
    assert ('G', 'c_sq') not in result.state.properties
    assert len(result.state.history) == 3


@pytest.mark.parametrize('mid,kind,eq', [(4, 'Ellipse', 'x^2/25+y^2/9=1'),
                                       (6, 'Hyperbola', 'x^2/9-y^2/16=1'),
                                       (4, 'Ellipse', 'x^2/9+y^2/9=1'),
                                       (6, 'Hyperbola', '(y-1)^2/9-x^2/16=1'),
                                       (6, 'Hyperbola', 'y^2/9-x^2/16+x*y=1')])
def test_wrong_or_unsupported_geometry_is_atomic(mid, kind, eq):
    s, app = state_for(kind, eq), BoundApplicator()
    before = deepcopy(s)
    assert app.apply(s, enumerate_actions(s, mid)[0]).status == 'inapplicable' and s == before


def test_undetermined_axis_does_not_mutate_state():
    s = state_for('Hyperbola', 'x^2/t-y^2/t=1')
    before = deepcopy(s)
    from src.solver.transition_primitives import TransitionError
    with pytest.raises(TransitionError) as error:
        select_standard_action(s, 'G', next(iter(s.equations)))
    assert error.value.status == 'undetermined' and s == before


@pytest.mark.parametrize('equation', ['-x^2/24+y^2/12=1', 'x^2/24-y^2/12=-1', '2*y^2- x^2=24'])
def test_equivalent_y_equations_and_repetition(equation):
    s, app = state_for('Hyperbola', equation), BoundApplicator()
    extract = enumerate_actions(s, 6)[0]
    assert app.apply(s, extract).status == 'applied'
    forward = enumerate_actions(s, 21, 'derive_asymptotes')[0]
    assert app.apply(s, forward).status == 'applied'
    before = deepcopy(s)
    assert app.apply(s, extract).status == app.apply(s, forward).status == 'no_op'
    assert s == before and s.properties['G', 'a_sq'] == 12 and s.properties['G', 'b_sq'] == 24


def test_mode_filter_is_not_overwritten_by_enumeration():
    s = state_for('Ellipse', 'y^2/25+x^2/9=1')
    modes = {a.mode for a in enumerate_actions(s, 11)}
    assert modes == {'derive_a_sq', 'derive_b_sq', 'derive_c_sq', 'constrain_parameters'}
    assert all(a.mode == 'derive_b_sq' for a in enumerate_actions(s, 11, 'derive_b_sq'))
    assert enumerate_actions(s, 4, 'unsupported') == []


def test_frame_axis_tampering_does_not_invert_asymptote_silently():
    s, app = state_for('Hyperbola', 'y^2/9-x^2/16=1'), BoundApplicator()
    app.apply(s, enumerate_actions(s, 6)[0])
    s.frames['G'] = replace(s.frames['G'], axis='x')
    before = deepcopy(s)
    assert app.apply(s, enumerate_actions(s, 21, 'derive_asymptotes')[0]).status == 'inapplicable'
    assert s == before


@pytest.mark.parametrize('mid,kind,equation', [(4, 'Ellipse', 'y^2/25+x^2/9=1'),
                                             (6, 'Hyperbola', 'y^2/9-x^2/16=1')])
def test_legacy_y_models_remain_callable(mid, kind, equation):
    from src.state.symbolic_state import SymbolicState
    from src.theorems.theorem_library import TheoremLibrary
    s = SymbolicState(entities={'G': kind}, equations=[f'Expression(G) = ({equation})'])
    model = TheoremLibrary().get_model(mid)
    assert model.can_apply(s) and model.apply(s)
