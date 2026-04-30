"""
Entropy dataset construction from model-state trajectories.
"""

import json
import random
import signal
from collections import Counter, defaultdict
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple

from src.reasoning.entropy_estimator import EntropyEstimator
from src.state.state_constructor import StateConstructor
from src.state.state_sequence_builder import StateSequenceBuilder, StateTransition
from src.theorems.theorem_library import TheoremLibrary

from .metrics import pearson_correlation, spearman_correlation
from .schema import SCHEMA_VERSION, make_entropy_label


def load_model_sequence_samples(input_path: str, limit: Optional[int] = None) -> List[Dict[str, Any]]:
    """Load samples with non-empty annotated model sequences."""
    with open(input_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    samples = [item for item in data if item.get('models')]
    if limit is not None:
        samples = samples[:limit]
    return samples


def write_jsonl(path: str, entries: Iterable[Dict[str, Any]]) -> None:
    output = Path(path)
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open('w', encoding='utf-8') as f:
        for entry in entries:
            f.write(json.dumps(entry, ensure_ascii=False, sort_keys=True) + '\n')


def read_jsonl(path: str) -> List[Dict[str, Any]]:
    with open(path, 'r', encoding='utf-8') as f:
        return [json.loads(line) for line in f if line.strip()]


class EntropyDatasetBuilder:
    """
    Build entropy labels from annotated model sequences and contrastive random paths.
    """

    def __init__(self, seed: int = 42, sample_timeout_seconds: Optional[float] = None):
        self.seed = int(seed)
        self.sample_timeout_seconds = sample_timeout_seconds
        self.skipped_paths: List[Dict[str, Any]] = []
        self.random = random.Random(seed)
        self.theorem_library = TheoremLibrary()
        self.state_constructor = StateConstructor(theorem_library=self.theorem_library)
        self.sequence_builder = StateSequenceBuilder(self.theorem_library, self.state_constructor)
        self.estimator = EntropyEstimator(mode='heuristic')

    def build_from_file(
        self,
        input_path: str,
        *,
        limit: Optional[int] = None,
        include_random: bool = True,
        random_paths_per_sample: int = 1,
    ) -> List[Dict[str, Any]]:
        samples = load_model_sequence_samples(input_path, limit=limit)
        return self.build_entries(
            samples,
            include_random=include_random,
            random_paths_per_sample=random_paths_per_sample,
        )

    def build_entries(
        self,
        samples: Sequence[Dict[str, Any]],
        *,
        include_random: bool = True,
        random_paths_per_sample: int = 1,
    ) -> List[Dict[str, Any]]:
        entries: List[Dict[str, Any]] = []
        implemented_model_ids = sorted(self.theorem_library.models.keys())

        for sample_index, sample in enumerate(samples):
            model_ids = [int(model_id) for model_id in sample.get('models', [])]
            if not model_ids:
                continue

            try:
                model_transitions = self._build_sequence(sample, model_ids)
            except EntropyBuildTimeout as exc:
                self._record_skip(sample, sample_index, 'model', str(exc))
                continue

            model_executable = self._is_executable(model_transitions, expected_steps=len(model_ids))

            entries.extend(
                self._entries_for_path(
                    sample=sample,
                    sample_index=sample_index,
                    path_type='model',
                    trajectory_suffix='model',
                    model_ids=model_ids,
                    transitions=model_transitions,
                    path_executable=model_executable,
                    solvable_on_path=False,
                    random_seed=None,
                )
            )

            if model_executable:
                entries.extend(
                    self._entries_for_path(
                        sample=sample,
                        sample_index=sample_index,
                        path_type='correct',
                        trajectory_suffix='correct',
                        model_ids=model_ids,
                        transitions=model_transitions,
                        path_executable=True,
                        solvable_on_path=True,
                        random_seed=None,
                    )
                )

            if include_random:
                for trial in range(random_paths_per_sample):
                    random_model_ids = [
                        self.random.choice(implemented_model_ids)
                        for _ in range(len(model_ids))
                    ]
                    try:
                        random_transitions = self._build_sequence(sample, random_model_ids)
                    except EntropyBuildTimeout as exc:
                        self._record_skip(sample, sample_index, f'random_{trial}', str(exc))
                        continue
                    random_executable = self._is_executable(
                        random_transitions,
                        expected_steps=len(random_model_ids),
                    )
                    entries.extend(
                        self._entries_for_path(
                            sample=sample,
                            sample_index=sample_index,
                            path_type='random',
                            trajectory_suffix=f'random_{trial}',
                            model_ids=random_model_ids,
                            transitions=random_transitions,
                            path_executable=random_executable,
                            solvable_on_path=False,
                            random_seed=self.seed + trial,
                        )
                    )

        return entries

    def _build_sequence(
        self,
        sample: Dict[str, Any],
        model_ids: Sequence[int],
    ) -> List[StateTransition]:
        with _time_limit(self.sample_timeout_seconds):
            return self.sequence_builder.build_sequence(
                fact_expressions=sample.get('fact_expressions', ''),
                query_expressions=sample.get('query_expressions', ''),
                model_ids=list(model_ids),
            )

    def _record_skip(
        self,
        sample: Dict[str, Any],
        sample_index: int,
        path_type: str,
        reason: str,
    ) -> None:
        self.skipped_paths.append({
            'sample_index': int(sample_index),
            'problem_id': sample.get('id', sample_index),
            'path_type': path_type,
            'reason': reason,
        })

    def _is_executable(
        self,
        transitions: Sequence[StateTransition],
        *,
        expected_steps: int,
    ) -> bool:
        if len(transitions) < expected_steps + 1:
            return False
        return all(transition.status == 'success' for transition in transitions[1:expected_steps + 1])

    def _entries_for_path(
        self,
        *,
        sample: Dict[str, Any],
        sample_index: int,
        path_type: str,
        trajectory_suffix: str,
        model_ids: Sequence[int],
        transitions: Sequence[StateTransition],
        path_executable: bool,
        solvable_on_path: bool,
        random_seed: Optional[int],
    ) -> List[Dict[str, Any]]:
        trajectory_id = f"{path_type}:{sample_index}:{trajectory_suffix}"
        sequence_length = len(model_ids)
        path_entries: List[Dict[str, Any]] = []

        for transition in transitions[:sequence_length + 1]:
            step = int(transition.step)
            next_model_id = int(model_ids[step]) if step < sequence_length else None
            next_model_name = None
            if next_model_id is not None:
                model = self.theorem_library.get_model(next_model_id)
                next_model_name = model.name if model is not None else f"Model_{next_model_id}"

            status = 'initial' if step == 0 else transition.status
            applied_model_id = int(transition.model_id) if transition.model_id is not None else None

            path_entries.append(
                make_entropy_label(
                    sample_index=sample_index,
                    problem_id=sample.get('id', sample_index),
                    trajectory_id=trajectory_id,
                    path_type=path_type,
                    random_seed=random_seed,
                    step=step,
                    sequence_length=sequence_length,
                    abstract_state=transition.abstract_state,
                    transition_status=status,
                    path_executable=path_executable,
                    solvable_on_path=solvable_on_path,
                    next_model_id=next_model_id,
                    next_model_name=next_model_name,
                    applied_model_id=applied_model_id,
                    answer_correct=None,
                    estimator=self.estimator,
                )
            )

        return path_entries


def summarize_entries(entries: Sequence[Dict[str, Any]]) -> Dict[str, Any]:
    path_type_counts = Counter(entry['path_type'] for entry in entries)
    status_counts = Counter(entry['transition_status'] for entry in entries)
    trajectory_ids = sorted({entry['trajectory_id'] for entry in entries})

    by_path_type: Dict[str, Dict[str, Any]] = {}
    for path_type in sorted(path_type_counts):
        path_entries = [entry for entry in entries if entry['path_type'] == path_type]
        targets = [entry['normalized_remaining_steps'] for entry in path_entries]
        heuristic = [entry['heuristic_entropy'] for entry in path_entries]
        trajectories = {entry['trajectory_id'] for entry in path_entries}
        executable = _trajectory_executable_rate(path_entries)
        by_path_type[path_type] = {
            'entries': len(path_entries),
            'trajectories': len(trajectories),
            'executable_rate': round(executable, 8),
            'target_mean': round(sum(targets) / len(targets), 8) if targets else 0.0,
            'heuristic_entropy_mean': round(sum(heuristic) / len(heuristic), 8) if heuristic else 0.0,
            'heuristic_vs_target_pearson': round(
                pearson_correlation(targets, heuristic), 8
            ) if len(targets) > 1 else 0.0,
            'heuristic_vs_target_spearman': round(
                spearman_correlation(targets, heuristic), 8
            ) if len(targets) > 1 else 0.0,
        }

    return {
        'schema_version': SCHEMA_VERSION,
        'entry_count': len(entries),
        'trajectory_count': len(trajectory_ids),
        'path_type_counts': dict(sorted(path_type_counts.items())),
        'transition_status_counts': dict(sorted(status_counts.items())),
        'by_path_type': by_path_type,
    }


def _trajectory_executable_rate(entries: Sequence[Dict[str, Any]]) -> float:
    by_trajectory: Dict[str, bool] = {}
    for entry in entries:
        by_trajectory[entry['trajectory_id']] = bool(entry['path_executable'])
    if not by_trajectory:
        return 0.0
    return sum(1 for value in by_trajectory.values() if value) / len(by_trajectory)


def group_entries_by_trajectory(
    entries: Sequence[Dict[str, Any]]
) -> Dict[str, List[Dict[str, Any]]]:
    grouped: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
    for entry in entries:
        grouped[entry['trajectory_id']].append(entry)
    for trajectory_entries in grouped.values():
        trajectory_entries.sort(key=lambda item: item['step'])
    return dict(grouped)


class EntropyBuildTimeout(TimeoutError):
    """Raised when one trajectory exceeds the entropy build timeout."""


@contextmanager
def _time_limit(seconds: Optional[float]):
    if seconds is None or seconds <= 0:
        yield
        return

    def _handle_timeout(_signum, _frame):
        raise EntropyBuildTimeout(f"entropy trajectory build timed out after {seconds}s")

    previous_handler = signal.signal(signal.SIGALRM, _handle_timeout)
    previous_timer = signal.setitimer(signal.ITIMER_REAL, float(seconds))
    try:
        yield
    finally:
        signal.setitimer(signal.ITIMER_REAL, 0)
        signal.signal(signal.SIGALRM, previous_handler)
        if previous_timer[0] > 0:
            signal.setitimer(signal.ITIMER_REAL, previous_timer[0], previous_timer[1])
