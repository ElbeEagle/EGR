from copy import deepcopy
from dataclasses import replace
import json
from pathlib import Path
import pytest
import sympy as sp
from src.state.transition_state import TransitionState
from src.state.directrix_pair_query import DirectrixPairQuery, pair_keys
from src.theorems.bound_application import BoundApplicator, enumerate_actions
from src.solver.directrix_pair_operations import directrix_pair
from src.solver.transition_primitives import TransitionError

ROW = next(r for r in json.loads(Path('data/train_with_models_v3.json').read_text()) if r['id'] == 2779)


def prepare(facts=None, standard=5):
    s = TransitionState.from_facts(facts or ROW['fact_expressions'], ROW['query_expressions'])
    assert isinstance(s.query, DirectrixPairQuery) and s.extract_answer() is None
    app = BoundApplicator()
    a = enumerate_actions(s, 28)[0]
    assert app.apply(s, a).status == 'inapplicable'
    for mid, mode in ((standard, 'extract_parameters'), (12, 'derive_c_sq')):
        action = next(a for a in enumerate_actions(s, mid, mode) if a.curve == 'G')
        t = app.apply(s, action)
        assert t.status == 'applied', t.diagnostic
    return s, a


@pytest.mark.parametrize('facts,mid,axis', [(None,5,'x'), ('G: Hyperbola;Expression(G)=(y^2-x^2/3=1)',6,'y'), ('G: Hyperbola;Expression(G)=(3*x^2-y^2=3)',5,'x')])
def test_real_axis_scale(facts, mid, axis):
    s,a = prepare(facts,mid);app = BoundApplicator()
    t = app.apply(s,a);assert t.status == 'applied',t.diagnostic
    assert s.extract_answer() == frozenset((s.symbols[axis]-sp.Rational(1,2),s.symbols[axis]+sp.Rational(1,2)))
    before=deepcopy(s);assert app.apply(s,a).status=='no_op' and s==before
    assert s.extract_answer()==before.extract_answer() and s==before


@pytest.mark.parametrize('damage', ['c','source','frame','wrong_source','stale','conflict','ambiguity'])
def test_reject_atomic(damage):
    s,a=prepare();app=BoundApplicator()
    if damage=='c':del s.properties['G','c_sq']
    if damage=='source':s.provenance['property:G:c_sq']=()
    if damage=='wrong_source':s.provenance['property:G:c_sq']=('other',)
    if damage=='frame':s.provenance['frame:G']=()
    if damage=='stale':s.equations[a.equation_id]=replace(s.equations[a.equation_id],expression=s.symbols['x']**2-s.symbols['y']**2-1)
    if damage in ('conflict','ambiguity'):
        assert app.apply(s,a).status=='applied'
        key=pair_keys('G')[1]
        if damage=='conflict':
            s.equations[key]=replace(s.equations[key],expression=s.symbols['x']-99)
            del s.equations[pair_keys('G')[0]]
        else:s.equations['extra']=replace(s.equations[key],fact_id='extra')
    before=deepcopy(s);assert app.apply(s,a).status in ('conflict','inapplicable') and s==before


def test_partial_scaled_and_read_freshness():
    s,a=prepare();app=BoundApplicator();assert app.apply(s,a).status=='applied'
    left,right=pair_keys('G');s.equations[left]=replace(s.equations[left],expression=3*s.equations[left].expression)
    assert s.extract_answer() is not None
    del s.equations[right];assert s.extract_answer() is None
    assert app.apply(s,a).status=='applied' and s.extract_answer() is not None
    assert s.equations[left].expression==3*(s.symbols['x']+sp.Rational(1,2))
    s.equations[a.equation_id]=replace(s.equations[a.equation_id],expression=s.symbols['x']**2-s.symbols['y']**2-1)
    assert s.extract_answer() is None


@pytest.mark.parametrize('damage',['source','equation_source','parameter','output'])
def test_reader_missing_or_stale(damage):
    s,a=prepare();assert BoundApplicator().apply(s,a).status=='applied'
    key=pair_keys('G')[0]
    if damage=='source':s.provenance['property:G:c_sq']=()
    if damage=='equation_source':s.provenance[key]=()
    if damage=='parameter':s.properties['G','c_sq']=sp.Integer(99)
    if damage=='output':s.equations[key]=replace(s.equations[key],expression=s.symbols['x']+99)
    before=deepcopy(s);assert s.extract_answer() is None and s==before


def test_curve_isolation():
    s,a=prepare(ROW['fact_expressions']+';H:Hyperbola;Expression(H)=(y^2-x^2=2)')
    assert BoundApplicator().apply(s,a).status=='applied'
    s.query=DirectrixPairQuery('H');assert s.extract_answer() is None
    before=deepcopy(s);assert BoundApplicator().apply(s,replace(a,curve='H')).status=='inapplicable' and s==before


@pytest.mark.parametrize('v',[sp.S.Zero,-sp.S.One,sp.oo,sp.Symbol('a',positive=True)])
def test_invalid_parameters(v):
    x,y=sp.symbols('x y')
    with pytest.raises(TransitionError):directrix_pair(x,y,v,sp.S.One,sp.Integer(2),'x')


@pytest.mark.parametrize('facts', [
    'G:Ellipse;Expression(G)=(x^2/4+y^2=1)',
    'G:Hyperbola;Expression(G)=((x-1)^2-y^2=1)',
    'G:Hyperbola;Expression(G)=(x*y=1)',
])
def test_excluded_geometries(facts):
    s=TransitionState.from_facts(facts,None)
    actions=enumerate_actions(s,28)
    if s.entities['G']=='Ellipse':assert actions==[]
    else:
        before=deepcopy(s);assert BoundApplicator().apply(s,actions[0]).status=='inapplicable' and s==before
