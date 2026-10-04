from copy import deepcopy
import json
from pathlib import Path
import pytest
import sympy as sp
from src.state.transition_state import TransitionState
from src.state.named_line_facts import NamedLineQuery
from src.theorems.bound_application import enumerate_actions


def row():
    return next(r for r in json.loads(Path('data/train_with_models_v3.json').read_text()) if r['id']==56)


def test_original_input_no_inference():
    r=row();s=TransitionState.from_facts(r['fact_expressions'],r['query_expressions'])
    assert s.query==NamedLineQuery('@line:A:B')
    assert s.named_lines['@line:A:B'].endpoints==('A','B')
    f,=s.named_intersections.values()
    assert (f.line,f.curve,f.points)==('@line:A:B','G',('A','B'))
    c,=s.slope_sums.values()
    assert c.base_point=='O' and c.value==1
    assert c.nonzero_x_differences==( ('A','O'), ('B','O') )
    assert s.coordinates['O'].xy==(0,0) and s.coordinates['O'].source=='O: Origin'
    assert set(s.coordinates)=={'O','M'}
    assert len(s.equations)==1 and not s.intersection_reductions
    assert not s.values and not s.properties and not s.history and s.revision==0
    assert not enumerate_actions(s,78,'substitute_line') # No explicit numeric line equation.
    before=deepcopy(s);assert s.extract_answer() is None and s==before
    assert len(s.incidences)==5
    for key in s.incidences:
        if key!= 'f7': assert s.provenance[key]==('f8',)


def test_permuted_endpoints_and_slope_terms():
    r=row();facts=r['fact_expressions'].replace('LineOf(A,B)','LineOf(B,A)').replace('{A, B}','{B, A}')
    facts=facts.replace('Slope(LineSegmentOf(O, A))+Slope(LineSegmentOf(O, B))',
                        'Slope(LineSegmentOf(O, B))+Slope(LineSegmentOf(O, A))')
    s=TransitionState.from_facts(facts,r['query_expressions'])
    assert list(s.named_lines)==['@line:A:B']
    assert next(iter(s.named_intersections.values())).points==('A','B')
    assert next(iter(s.slope_sums.values())).endpoints==('A','B')


def test_query_identity_does_not_assert_intersections():
    s=TransitionState.from_facts('A: Point;B: Point','Expression(LineOf(A,B))')
    assert s.query.line=='@line:A:B' and not s.incidences and not s.named_intersections
    assert not s.equations and s.extract_answer() is None


@pytest.mark.parametrize('old,new',[
    ('LineOf(A,B)','LineOf(A,A)'), ('A: Point','A: Line'),
    ('{A, B}','{A, M}'), ('{A, B}','{A, A}'),
    ('G: Parabola','G: Line'), ('PointOnCurve(M,','PointOnCurve(Z,'),
    ('LineSegmentOf(O, B)','LineSegmentOf(M, B)'),
    ('LineSegmentOf(O, B)','LineSegmentOf(O, O)'),
    (' = 1',' = z'),
])
def test_invalid_references_rejected(old,new):
    r=row()
    with pytest.raises(ValueError):
        TransitionState.from_facts(r['fact_expressions'].replace(old,new),r['query_expressions'])


def test_distinct_line_references_do_not_merge():
    s=TransitionState.from_facts('A: Point;B: Point;C: Point;M: Point;PointOnCurve(M,LineOf(A,B));PointOnCurve(M,LineOf(A,C))',None)
    assert set(s.named_lines)=={'@line:A:B','@line:A:C'}


def test_origin_duplicate_coordinates_rejected_in_either_order():
    for facts in ('O: Origin;Coordinate(O)=(1,0)', 'Coordinate(O)=(1,0);O: Origin'):
        with pytest.raises(ValueError): TransitionState.from_facts(facts,None)
