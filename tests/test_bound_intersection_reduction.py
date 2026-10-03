from copy import deepcopy
from dataclasses import replace
import json
from pathlib import Path
import pytest
import sympy as sp
from src.state.transition_state import TransitionState
from src.solver.transition_primitives import TransitionError
from src.solver.intersection_operations import substitute_line_in_parabola
from src.theorems.bound_application import BoundApplicator, enumerate_actions

FACTS = 'G: Parabola;H: Line;Expression(G)=(y^2=4*x);Expression(H)=(y=x-1)'


def apply_reduction(facts=FACTS):
    state = TransitionState.from_facts(facts, None)
    action = enumerate_actions(state, 78, 'substitute_line')[0]
    result = BoundApplicator().apply(state, action)
    return state, action, result


def test_original_substep_and_provenance():
    row = next(r for r in json.loads(Path('data/train_with_models_v3.json').read_text()) if r['id'] == 6347)
    state, action, result = apply_reduction(row['fact_expressions'])
    assert result.status == 'applied'
    fact, = state.intersection_reductions.values()
    x, y = state.symbols['x'], state.symbols['y']
    assert fact.variable == y and fact.xy == (y+1, y) and fact.polynomial == y**2-4*y-4
    assert {action.equation_id, action.line_equation_id}.issubset(state.provenance[fact.fact_id])
    assert not state.coordinates and not state.values and state.extract_answer() is None
    # Independent simultaneous solve: every lifted root gives a source-system solution.
    roots = sp.solve(fact.polynomial, fact.variable)
    points = {tuple(sp.simplify(c.subs(fact.variable, r)) for c in fact.xy) for r in roots}
    solutions = sp.solve([f.expression for f in state.equations.values()], (x,y))
    assert points == {tuple(sp.simplify(v) for v in p) for p in solutions}
    before = deepcopy(state)
    assert BoundApplicator().apply(state, action).status == 'no_op' and state == before


@pytest.mark.parametrize('curve,line,degree,discriminant_sign', [
    ('y^2=4*x', 'x=1', 2, 1),
    ('y^2=4*x', 'x=0', 2, 0),
    ('y^2=4*x', 'x=-1', 2, -1),
    ('y^2=4*x', 'y=2', 1, None),
    ('x^2=4*y', 'y=1', 2, 1),
    ('x^2=4*y', 'x=2', 1, None),
    ('y^2=-4*x', 'x=-1', 2, 1),
    ('x^2=-4*y', 'y=-1', 2, 1),
])
def test_degrees_and_no_implicit_real_intersection_claim(curve,line,degree,discriminant_sign):
    state, _, result = apply_reduction(FACTS.replace('y^2=4*x',curve).replace('y=x-1',line))
    assert result.status == 'applied'
    fact, = state.intersection_reductions.values()
    poly = sp.Poly(fact.polynomial,fact.variable)
    assert poly.degree() == degree
    if discriminant_sign is not None:
        assert sp.sign(sp.discriminant(poly.as_expr(),fact.variable)) == discriminant_sign
    assert not state.coordinates and not state.incidences
    x,y = state.symbols['x'],state.symbols['y']
    assert sp.simplify(state.equations[fact.line_equation_id].expression.subs(
        {x:fact.xy[0],y:fact.xy[1]}, simultaneous=True)) == 0


@pytest.mark.parametrize('change',[{'curve':'H'},{'line':'G'},{'equation_id':'f3'},
    {'line_equation_id':'f2'},{'point':'P'},{'relation_id':'bad'},{'mode':'inverse'}])
def test_wrong_bindings_roll_back(change):
    state = TransitionState.from_facts(FACTS,None)
    action = replace(enumerate_actions(state,78)[0],**change)
    before = deepcopy(state)
    assert BoundApplicator().apply(state,action).status == 'inapplicable' and state == before


def test_conflict_and_distinct_line_identity():
    state, action, _ = apply_reduction(FACTS+';J: Line;Expression(J)=(x=1)')
    app = BoundApplicator()
    second = next(a for a in enumerate_actions(state,78) if a.line == 'J')
    assert app.apply(state,second).status == 'applied' and len(state.intersection_reductions)==2
    key = next(k for k,v in state.intersection_reductions.items() if v.line=='H')
    state.intersection_reductions[key] = replace(state.intersection_reductions[key], polynomial=sp.S.One)
    before = deepcopy(state)
    assert app.apply(state,action).status == 'conflict' and state == before


@pytest.mark.parametrize('curve,line,status',[
    ('y**2-4*x','y-k*x','undetermined'),
    ('y**2-4*x','x*y-1','inapplicable'),
    ('y**2-4*x','0','inapplicable'),
    ('(y-1)**2-4*x','x-1','inapplicable'),
    ('x**2+y**2-1','x-1','inapplicable'),
    ('y**2-4*x','x+I*y','undetermined'),
])
def test_public_operation_rejects_unsupported(curve,line,status):
    x,y,k = sp.symbols('x y k',real=True)
    with pytest.raises(TransitionError) as exc:
        substitute_line_in_parabola(sp.sympify(curve,locals={'x':x,'y':y,'k':k}),
                                   sp.sympify(line,locals={'x':x,'y':y,'k':k}),x,y)
    assert exc.value.status == status


def test_normalization_and_existing_value_substitution():
    state,a,result = apply_reduction('k: Real;'+FACTS.replace('y=x-1','y=k*x-1'))
    assert result.status == 'undetermined' and not state.intersection_reductions
    state.values[state.symbols['k']] = sp.S.One
    result = BoundApplicator().apply(state,a)
    assert result.status == 'applied' and 'value:k' in result.read_facts
    x,y = state.symbols['x'],state.symbols['y']
    assert substitute_line_in_parabola(-3*(y*y-4*x),7*(y-x+1),x,y) == substitute_line_in_parabola(y*y-4*x,y-x+1,x,y)
