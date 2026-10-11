"""ID1833 input contract, kept separate from symbolic model support."""
from copy import deepcopy
import json
from pathlib import Path
import pytest
from src.state.transition_state import TransitionState
from src.state.coordinate_product_facts import CoordinateProductQuery
from src.theorems.bound_application import BoundApplicator, enumerate_actions

ROW = next(r for r in json.loads(Path('data/train_with_models_v3.json').read_text()) if r['id'] == 1833)
FACTS = ROW['fact_expressions']


def apply(state, mid):
    action, = enumerate_actions(state, mid, 'extract_parameters' if mid == 7 else None)
    return BoundApplicator().apply(state, action)


def test_original_input_only_and_no_invented_positivity():
    s = TransitionState.from_facts(FACTS, ROW['query_expressions'])
    assert isinstance(s.query, CoordinateProductQuery)
    assert s.coordinate_aliases['y1'].point == 'A'
    assert s.coordinate_aliases['y2'].point == 'B'
    assert s.coordinate_aliases['y1'].fact_id == 'f11'
    assert next(iter(s.intersection_counts.values())).count == 2
    assert not s.coordinates and not s.properties and not s.values and not s.constraints
    assert s.extract_answer() is None and s.revision == 0
    before = deepcopy(s)
    assert apply(s, 7).status == 'undetermined' and s == before


def test_positive_diagnostic_is_not_symbolic_product_support():
    s = TransitionState.from_facts(FACTS + ';p>0', 'y1*y2')
    assert apply(s, 7).status == 'applied'
    before = deepcopy(s)
    assert apply(s, 35).status == 'undetermined' and s == before
    assert s.extract_answer() is None


@pytest.mark.parametrize('query', ['y1*y2', 'y2 * y1'])
@pytest.mark.parametrize('intersection', ['Intersection(H, G) = {A, B}', 'Intersection(G,H)={B,A}'])
def test_numeric_bridge_read_only(query, intersection):
    facts = FACTS.replace('2*(p*x)', '4*x').replace('Intersection(H, G) = {A, B}', intersection)
    s = TransitionState.from_facts(facts, query)
    assert s.extract_answer() is None
    assert apply(s, 7).status == 'applied'
    assert s.extract_answer() is None
    assert apply(s, 35).status == 'applied'
    before = deepcopy(s)
    assert s.extract_answer() == -4 and s == before
    assert not s.values and not s.coordinates


@pytest.mark.parametrize('replacement', [
    ('YCoordinate(B) = y2', 'XCoordinate(B)=y2'),
    ('YCoordinate(B) = y2', 'YCoordinate(A)=y2'),
    ('YCoordinate(B) = y2', 'YCoordinate(B)=y1'),
    ('YCoordinate(B) = y2', 'YCoordinate(B)=undeclared'),
    ('NumIntersection(H, G) = 2', 'NumIntersection(G,H)=1'),
    ('YCoordinate(B) = y2', 'YCoordinate(G)=y2'),
])
def test_invalid_input(replacement):
    with pytest.raises(ValueError):
        TransitionState.from_facts(FACTS.replace(*replacement), 'y1*y2')


def test_count_alone_does_not_create_endpoints():
    facts = FACTS.replace('Intersection(H, G) = {A, B};', '')
    s = TransitionState.from_facts(facts, 'y1*y2')
    assert not s.named_intersections and not enumerate_actions(s,35)
    assert s.extract_answer() is None


def test_conflicting_counts():
    with pytest.raises(ValueError):
        TransitionState.from_facts(FACTS+';NumIntersection(G,H)=0', 'y1*y2')


def test_ambiguous_pair_is_not_guessed():
    s = TransitionState.from_facts(FACTS.replace('2*(p*x)', '4*x'), 'y1*y2')
    assert apply(s,7).status == 'applied' and apply(s,35).status == 'applied'
    from dataclasses import replace
    first = next(iter(s.named_intersections.values()))
    s.named_intersections['other'] = replace(first, fact_id='other', line='J')
    assert s.extract_answer() is None


def test_known_coordinates_do_not_trigger_answer_computation():
    s = TransitionState.from_facts(FACTS+';Coordinate(A)=(1,2);Coordinate(B)=(1,-2)', 'y1*y2')
    assert s.extract_answer() is None
