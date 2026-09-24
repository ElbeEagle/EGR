"""ID 9 and counterexamples for object-bound shared-focus execution."""
from copy import deepcopy
from dataclasses import replace
import json
from pathlib import Path

import pytest
import sympy as sp

from src.reasoning.bound_slice import solve_shared_focus_slice, replay_actions
from src.state.transition_state import TransitionState, CurveFrame
from src.theorems.bound_application import BoundAction, BoundApplicator, enumerate_actions

DATA = Path(__file__).resolve().parents[1] / 'data/train_with_models_v3.json'
FACTS = ('G: Hyperbola;Expression(G) = (x^2/7-y^2/t=1);t: Real;'
         'H: Ellipse;Expression(H) = (x^2/25+y^2/9=1);Focus(G) = Focus(H)')


def prepared(facts=FACTS):
    state = TransitionState.from_facts(facts, 't')
    app = BoundApplicator()
    actions = [enumerate_actions(state, mid)[0] for mid in (3, 11, 5, 12)]
    return state, app, actions


def test_real_id9_scoped_trace():
    record = next(r for r in json.loads(DATA.read_text()) if r['id'] == 9)
    result = solve_shared_focus_slice(record['fact_expressions'], record['query_expressions'])
    assert result.status == 'solved' and result.answer == 9
    assert [r.action.model_id for r in result.transitions] == [3, 11, 5, 12]
    assert all(r.status == 'applied' for r in result.transitions)
    s = result.state
    assert s.properties == {('H', 'a_sq'): 25, ('H', 'b_sq'): 9, ('H', 'c_sq'): 16,
                            ('G', 'a_sq'): 7, ('G', 'b_sq'): 9, ('G', 'c_sq'): 16}
    third = result.transitions[2]
    key, condition = next(iter(third.delta['constraints'].items()))
    assert condition == (s.query > 0) and key.startswith('derived:')
    assert s.provenance[key][-1] == 'action:3'
    assert 'entity:G' in s.provenance[key]
    last = result.transitions[-1]
    assert last.operations[0]['operation'] == 'instantiate_shared_focus'
    assert last.operations[0]['peer'] == 'H'
    assert last.action.relation_id in last.read_facts
    assert any(o['operation'] == 'restricted_substitution' for o in last.operations)
    # Independent geometric check, beyond reproducing the reference scalar.
    assert sp.sqrt(s.properties['H', 'a_sq'] - s.properties['H', 'b_sq']) == 4
    assert sp.sqrt(s.properties['G', 'a_sq'] + s.properties['G', 'b_sq']) == 4


def test_initial_state_preserves_relation_without_inference():
    s, _, _ = prepared()
    assert len(s.relations) == 1
    assert not s.properties and not s.frames and not s.values
    assert (s.query > 0) not in s.constraints.values()
    assert s.abstract('H').curve_type.name == 'ELLIPSE'


@pytest.mark.parametrize('missing', [3, 11, 5])
def test_missing_dependency_is_not_inferred(missing):
    s, app, actions = prepared()
    for a in actions[:-1]:
        if a.model_id != missing:
            app.apply(s, a)
    before = deepcopy(s)
    assert app.apply(s, actions[-1]).status == 'inapplicable'
    assert s == before


@pytest.mark.parametrize('order', [(3, 11, 5, 12), (5, 3, 11, 12), (3, 5, 11, 12)])
def test_valid_orderings_and_repeated_actions(order):
    s, app, actions = prepared()
    by_id = {a.model_id: a for a in actions}
    result = replay_actions(s, [by_id[mid] for mid in order])
    assert result.answer == 9 and s.revision == 4
    before = deepcopy(s)
    for action in actions:
        assert app.apply(s, action).status == 'no_op'
        assert s == before


@pytest.mark.parametrize('edit', [dict(relation_id='missing'), dict(peer_curve='G'),
                                 dict(peer_equation_id='f1'), dict(equation_id='f4')])
def test_wrong_binding_is_atomic(edit):
    s, app, actions = prepared()
    replay_actions(s, actions[:-1])
    before = deepcopy(s)
    assert app.apply(s, replace(actions[-1], **edit)).status == 'inapplicable'
    assert s == before


def test_third_curve_cannot_supply_unrelated_focal_parameter():
    s, app, actions = prepared(FACTS + ';K: Ellipse;Expression(K)=(x^2/100+y^2/19=1)')
    replay_actions(s, actions[:-1])
    for mid in (3, 11):
        app.apply(s, next(a for a in enumerate_actions(s, mid) if a.curve == 'K'))
    wrong = replace(actions[-1], peer_curve='K', peer_equation_id='f7')
    before = deepcopy(s)
    assert app.apply(s, wrong).status == 'inapplicable' and s == before
    assert app.apply(s, actions[-1]).status == 'applied'
    assert s.extract_answer() == 9 and s.properties['K', 'c_sq'] == 81


@pytest.mark.parametrize('ellipse', ['(x-1)^2/25+y^2/9=1', 'x^2/9+y^2/25=1',
                                    'x^2/9+y^2/9=1'])
def test_unsupported_geometry_does_not_copy_c(ellipse):
    result = solve_shared_focus_slice(FACTS.replace('x^2/25+y^2/9=1', ellipse), 't')
    assert result.status == 'inapplicable' and result.answer is None
    assert ('G', 'c_sq') not in result.state.properties


@pytest.mark.parametrize('frame', [CurveFrame('f4', axis='y'),
                                  CurveFrame('f4', center=(sp.S.One, sp.S.Zero))])
def test_mismatched_frame_rejected(frame):
    s, app, actions = prepared()
    replay_actions(s, actions[:-1])
    s.frames['H'] = frame
    before = deepcopy(s)
    assert app.apply(s, actions[-1]).status == 'inapplicable' and s == before


@pytest.mark.parametrize('constraint', ['t<0', 't=0', 't>10', 't>0;t<0'])
def test_inconsistent_or_excluded_solution_does_not_commit(constraint):
    result = solve_shared_focus_slice(FACTS + ';' + constraint, 't')
    assert result.status in ('conflict', 'inapplicable') and result.answer is None
    assert ('G', 'c_sq') not in result.state.properties


def test_target_c_conflict_rolls_back_value_and_substitution():
    s, app, actions = prepared()
    replay_actions(s, actions[:-1])
    s.properties['G', 'c_sq'] = sp.Integer(17)
    before = deepcopy(s)
    assert app.apply(s, actions[-1]).status == 'conflict' and s == before


@pytest.mark.parametrize('replacement,answer', [('x^2/20+y^2/8', 5), ('x^2/13+y^2/9', None)])
def test_changed_equation_changes_answer_or_rejects_nonhyperbola(replacement, answer):
    result = solve_shared_focus_slice(FACTS.replace('x^2/25+y^2/9', replacement), 't')
    assert result.answer == answer
    assert result.status == ('solved' if answer is not None else 'conflict')


def test_multiroot_parameter_retained_without_arbitrary_choice():
    result = solve_shared_focus_slice(FACTS.replace('y^2/t', 'y^2/t^2'), 't')
    assert result.status == 'undetermined' and result.answer is None
    assert result.transitions[-1].candidates == (-3, 3)
    assert ('G', 'c_sq') not in result.state.properties


def test_relation_direction_and_object_names_do_not_change_result():
    facts = FACTS.replace('Focus(G) = Focus(H)', 'Focus(H) = Focus(G)')
    facts = facts.replace('G', 'C1').replace('H:', 'C2:').replace('(H)', '(C2)')
    assert solve_shared_focus_slice(facts, 't').answer == 9


def test_no_relation_or_multiple_bindings_not_silently_selected():
    assert solve_shared_focus_slice(FACTS.split(';Focus')[0], 't').status == 'undetermined'
    facts = FACTS + ';K: Ellipse;Expression(K)=(x^2/100+y^2/19=1);Focus(G)=Focus(K)'
    assert solve_shared_focus_slice(facts, 't').status == 'undetermined'


def test_unknown_relation_entity_is_rejected():
    with pytest.raises(ValueError, match='declared curves'):
        TransitionState.from_facts(FACTS.replace('Focus(H)', 'Focus(K)'), 't')


def test_type_condition_is_idempotent_before_solving():
    s, app, actions = prepared()
    assert app.apply(s, actions[2]).status == 'applied'
    before = deepcopy(s)
    assert app.apply(s, actions[2]).status == 'no_op' and s == before
    assert s.extract_answer() is None


def test_derived_constraint_conflict_rolls_back_entire_proposal():
    from src.theorems.bound_application import Proposal
    s, app, actions = prepared(FACTS + ';t<0')
    def invalid_proposal(copy, action):
        return Proposal(properties={('G', 'a_sq'): sp.Integer(7)},
                        constraints={'test:positive': copy.query > 0},
                        frames={'G': CurveFrame(action.equation_id)})
    app.library.get_model(5).propose_bound = invalid_proposal
    before = deepcopy(s)
    assert app.apply(s, actions[2]).status == 'conflict' and s == before


def test_missing_parameter_symbol_is_not_filled_from_reference():
    facts = FACTS.replace('t: Real', 't: Real;u: Real').replace('x^2/25', 'x^2/(u+25)')
    result = solve_shared_focus_slice(facts, 't')
    assert result.status == 'undetermined' and result.answer is None


def test_focal_parameter_conflict_during_rm11_is_atomic():
    s, app, actions = prepared()
    app.apply(s, actions[0])
    s.properties['H', 'c_sq'] = sp.Integer(100)
    before = deepcopy(s)
    assert app.apply(s, actions[1]).status == 'conflict' and s == before


def test_legacy_rm3_rm11_rm12_still_execute():
    from src.state.symbolic_state import SymbolicState
    from src.theorems.theorem_library import TheoremLibrary
    library = TheoremLibrary()
    ellipse = SymbolicState(entities={'H': 'Ellipse'},
                            equations=['Expression(H) = (x^2/25 + y^2/9 = 1)'])
    for mid in (3, 11):
        assert library.get_model(mid).can_apply(ellipse)
        assert library.get_model(mid).apply(ellipse)
    hyperbola = SymbolicState(entities={'G': 'Hyperbola'}, parameters={'a': '2', 'b': '3'})
    assert library.get_model(12).can_apply(hyperbola)
    assert library.get_model(12).apply(hyperbola)
