from copy import deepcopy
from dataclasses import replace
import pytest
import sympy as sp
from src.state.transition_state import TransitionState, EquationFact
from src.theorems.bound_application import BoundApplicator, enumerate_actions
from src.solver.two_point_line_operations import two_point_line
from src.solver.transition_primitives import TransitionError

FACTS='A:Point;B:Point;Coordinate(A)=(0,-4);Coordinate(B)=(3,2)'


def prepare(facts=FACTS,query='Expression(LineOf(A,B))'):
    s=TransitionState.from_facts(facts,query)
    return s,enumerate_actions(s,73)[0]


@pytest.mark.parametrize('facts,expected',[(FACTS,'x-y/2-2'),('A:Point;B:Point;Coordinate(A)=(-1,0);Coordinate(B)=(2,4)','x-3*y/4+1'),('A:Point;B:Point;Coordinate(A)=(2,0);Coordinate(B)=(2,3)','x-2'),('A:Point;B:Point;Coordinate(A)=(0,2);Coordinate(B)=(3,2)','y-2')])
@pytest.mark.parametrize('reverse',[False,True])
def test_lines(facts,expected,reverse):
    if reverse:facts=';'.join(reversed(facts.split(';')))
    s,a=prepare(facts,'Expression(LineOf(B,A))' if reverse else 'Expression(LineOf(A,B))');app=BoundApplicator()
    assert s.extract_answer() is None
    t=app.apply(s,a);assert t.status=='applied',t.diagnostic
    assert sp.simplify(s.extract_answer()-sp.sympify(expected,locals=s.symbols))==0
    before=deepcopy(s);assert app.apply(s,a).status=='no_op' and s==before


@pytest.mark.parametrize('damage',['id','value','source','identity','extra','model','snapshot'])
def test_stale_binding(damage):
    s,a=prepare()
    if damage=='id':s.coordinates['A']=replace(s.coordinates['A'],fact_id='changed')
    if damage=='value':s.coordinates['A']=replace(s.coordinates['A'],xy=(sp.S.One,sp.S.Zero))
    if damage=='source':s.provenance[s.coordinates['A'].fact_id]=()
    if damage=='identity':s.provenance[f'identity:{a.line}']=()
    if damage=='extra':a=replace(a,curve='G')
    if damage=='model':a=replace(a,model_id=72)
    if damage=='snapshot':a=replace(a,coordinate_snapshot='old')
    before=deepcopy(s);assert BoundApplicator().apply(s,a).status=='inapplicable' and s==before


@pytest.mark.parametrize('damage',['coordinate','source','output','output_source'])
def test_readonly_stale(damage):
    s,a=prepare();app=BoundApplicator();assert app.apply(s,a).status=='applied'
    key=f'derived:{a.line}:two_points'
    if damage=='coordinate':s.coordinates['A']=replace(s.coordinates['A'],xy=(sp.S.One,sp.S.Zero))
    if damage=='source':s.provenance[s.coordinates['A'].fact_id]=()
    if damage=='output':s.equations[key]=replace(s.equations[key],expression=s.symbols['x']-10)
    if damage=='output_source':s.provenance[key]=()
    before=deepcopy(s);assert s.extract_answer() is None and s==before
    assert app.apply(s,a).status in ('inapplicable','conflict') and s==before


@pytest.mark.parametrize('kind',['equivalent','conflict','multiple','missing_source'])
def test_existing(kind):
    s,a=prepare();x,y=s.symbols['x'],s.symbols['y'];expr=2*x-y-4
    if kind=='conflict':expr=x-99
    s.equations['given']=EquationFact('given',a.line,'line',expr,'given')
    s.provenance['given']=('input',)
    if kind=='multiple':s.equations['other']=replace(s.equations['given'],fact_id='other')
    if kind=='missing_source':s.provenance['given']=()
    before=deepcopy(s);t=BoundApplicator().apply(s,a)
    assert t.status=={'equivalent':'no_op','conflict':'conflict','multiple':'inapplicable','missing_source':'inapplicable'}[kind] and s==before


def test_scaled_result_and_isolation():
    s,a=prepare(FACTS+';C:Point;Coordinate(C)=(9,8);PointOnCurve(C,LineOf(B,C))')
    app=BoundApplicator();assert app.apply(s,a).status=='applied'
    key=f'derived:{a.line}:two_points';s.equations[key]=replace(s.equations[key],expression=3*s.equations[key].expression)
    before=deepcopy(s);assert s.extract_answer() is not None
    assert app.apply(s,a).status=='no_op' and s==before
    assert len(s.equations)==1


@pytest.mark.parametrize('value',[sp.oo,sp.I,sp.Symbol('u',real=True)])
def test_non_numeric(value):
    x,y=sp.symbols('x y')
    with pytest.raises(TransitionError):two_point_line(x,y,(value,sp.S.Zero),(sp.S.One,sp.S.One))


def test_coincident_and_missing():
    s,a=prepare('A:Point;B:Point;Coordinate(A)=(1,1);Coordinate(B)=(1,1)');before=deepcopy(s)
    assert BoundApplicator().apply(s,a).status=='inapplicable' and s==before
    del s.coordinates['B'];assert enumerate_actions(s,73)==[]
