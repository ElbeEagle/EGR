"""Conservative multi-evidence dry-run repair for model sequences."""

from __future__ import annotations

from collections import Counter
from typing import Any, Dict, Iterable, List, Sequence, Tuple

from .complete_library import SupportLevel
from .quantity_closure import QuantityApplicatorV2
from .quantity_library import QuantityTheoremLibraryV2
from .quantity_raw_adapter import QuantityRawFactAdapter
from .schema import ApplicationStatus


_SUCCESS = {
    ApplicationStatus.APPLIED,
    ApplicationStatus.ALREADY_KNOWN,
}
_SEMANTIC_MODEL_IDS = {63, 64, 68, 69, 70, 71, 77, 79}
_SIBLING_GROUPS = (
    (0, 1, 2),
    tuple(range(3, 11)),
    (11, 12),
    (14, 15),
    (16, 17),
    (18, 19, 20),
    (25, 26),
    (27, 28, 29),
    (30, 31),

)
_TYPE_BY_MODEL = {
    **{model_id: "Ellipse" for model_id in (0, 3, 4, 11, 14, 16, 18, 25, 27, 30, 32, 37, 38, 40, 45)},
    **{model_id: "Hyperbola" for model_id in (1, 5, 6, 12, 15, 19, 22, 23, 24, 26, 28, 31, 46)},
    **{model_id: "Parabola" for model_id in (2, 7, 8, 9, 10, 17, 20, 29, 33, 34, 35, 36, 39)},
}
_PROCESS_CUES = {
    63: ("基本不等式", "均值不等式", ">=", "≥", "不等式"),
    64: ("当且仅当", "等号成立", "取等"),
    68: ("三角形中位线", "中位线"),
    69: ("梯形中位线", "梯形"),
    70: ("内切圆半径", "内切圆", "内切圆的半径"),
    71: ("等面积", "等底", "等高"),
    77: ("齐次化", "齐次", "同除"),
    79: ("二次函数", "配方", "最大值", "最小值", "顶点"),
}


def _sibling_group(model_id: int) -> Tuple[int, ...]:
    for group in _SIBLING_GROUPS:
        if model_id in group:
            return tuple(group)
    return ()


class V3DryRunRepairer:
    def __init__(self):
        self.adapter = QuantityRawFactAdapter()
        self.library = QuantityTheoremLibraryV2()
        self.applicator = QuantityApplicatorV2()

    def repair_row(self, row: Dict[str, Any]) -> Dict[str, Any]:
        adaptation = self.adapter.adapt(
            row.get("fact_expressions", ""),
            row.get("query_expressions", ""),
        )
        original = tuple(row.get("models") or ())
        original_trace = self._replay(original, adaptation.state)
        observed, observed_trace, observed_operations = self._repair_observed(
            original, adaptation.state
        )
        executable, executable_trace, executable_operations = (
            self._complete_executable(observed, adaptation.state)
        )
        semantic_flags = self._semantic_flags(row, original)
        quality = self._quality(
            observed_trace,
            executable_trace,
            semantic_flags,
            adaptation.errors,
        )
        return {
            "id": row.get("id"),
            "original_models": list(original),
            "models_v3_observed": list(observed),
            "models_v3_executable": list(executable),
            "original_trace": original_trace,
            "observed_trace": observed_trace,
            "executable_trace": executable_trace,
            "observed_operations": observed_operations,
            "executable_operations": executable_operations,
            "semantic_flags": semantic_flags,
            "quality_candidate": quality,
            "unparsed_fact_count": len(adaptation.unparsed_facts),
            "adapter_errors": list(adaptation.errors),
        }

    def _repair_observed(self, sequence, initial_state):
        state = initial_state
        repaired: List[int] = []
        trace: List[Dict[str, Any]] = []
        operations: List[Dict[str, Any]] = []

        for index, model_id in enumerate(sequence):
            capability = self.library.get_capability(model_id)
            if capability is None:
                repaired.append(model_id)
                trace.append(self._trace(index, model_id, "UNKNOWN_MODEL"))
                continue
            if capability.support_level == SupportLevel.SPECIFICATION_ONLY:
                repaired.append(model_id)
                trace.append(self._trace(index, model_id, "SPECIFICATION_ONLY"))
                continue

            result = self.applicator.apply(
                self.library.get_model(model_id), state
            )
            if (
                repaired
                and repaired[-1] == model_id
                and result.status == ApplicationStatus.ALREADY_KNOWN
            ):
                operations.append(
                    {
                        "operation": "remove_adjacent_duplicate",
                        "index": index,
                        "before": model_id,
                        "after": None,
                        "confidence": "high",
                        "evidence": ["previous identical action already established postcondition"],
                    }
                )
                continue

            if result.status in _SUCCESS:
                repaired.append(model_id)
                trace.append(self._trace(index, model_id, result.status.value))
                if result.state_after is not None:
                    state = result.state_after
                continue

            replacement = self._unique_sibling(model_id, state)
            if replacement is not None:
                replacement_id, replacement_result = replacement
                evidence = ["unique applicable sibling executor"]
                expected_type = _TYPE_BY_MODEL.get(replacement_id)
                if expected_type and any(
                    symbol.type_name == expected_type
                    for symbol in state.symbols.values()
                ):
                    evidence.append(f"declared entity type: {expected_type}")
                operations.append(
                    {
                        "operation": "replace_misaligned_model",
                        "index": index,
                        "before": model_id,
                        "after": replacement_id,
                        "confidence": "high" if len(evidence) >= 2 else "medium",
                        "evidence": evidence,
                    }
                )
                repaired.append(replacement_id)
                trace.append(
                    self._trace(
                        index,
                        replacement_id,
                        replacement_result.status.value,
                        original_model_id=model_id,
                    )
                )
                if replacement_result.state_after is not None:
                    state = replacement_result.state_after
                continue

            repaired.append(model_id)
            trace.append(self._trace(index, model_id, result.status.value))

        return tuple(repaired), trace, operations

    def _complete_executable(self, sequence, initial_state):
        state = initial_state
        repaired: List[int] = []
        trace: List[Dict[str, Any]] = []
        operations: List[Dict[str, Any]] = []
        skip_indices = set()

        for index, model_id in enumerate(sequence):
            if index in skip_indices:
                continue
            capability = self.library.get_capability(model_id)
            if capability is None:
                repaired.append(model_id)
                trace.append(self._trace(index, model_id, "UNKNOWN_MODEL"))
                continue
            if capability.support_level == SupportLevel.SPECIFICATION_ONLY:
                repaired.append(model_id)
                trace.append(self._trace(index, model_id, "SPECIFICATION_ONLY"))
                continue

            initial_result = self.applicator.apply(
                self.library.get_model(model_id), state
            )
            if initial_result.status in _SUCCESS:
                repaired.append(model_id)
                trace.append(
                    self._trace(index, model_id, initial_result.status.value)
                )
                if initial_result.state_after is not None:
                    state = initial_result.state_after
                continue

            trial_state = state
            trial_dependencies = []
            trial_trace = []
            trial_operations = []
            trial_skip_indices = set()
            used_dependencies = set()
            final_result = initial_result

            for _ in range(8):
                candidates = self._applicable_dependencies(
                    model_id, trial_state, used_dependencies
                )
                if not candidates:
                    break
                dependency, dependency_result = candidates[0]
                used_dependencies.add(dependency)
                future_index = self._future_index(
                    sequence,
                    dependency,
                    index + 1,
                    skip_indices | trial_skip_indices,
                )
                operation = (
                    "move_dependency_before_consumer"
                    if future_index is not None
                    else "insert_verified_dependency"
                )
                if future_index is not None:
                    trial_skip_indices.add(future_index)
                trial_dependencies.append(dependency)
                trial_trace.append(
                    self._trace(
                        index,
                        dependency,
                        dependency_result.status.value,
                    )
                )
                trial_operations.append(
                    {
                        "operation": operation,
                        "index": index,
                        "future_index": future_index,
                        "consumer": model_id,
                        "dependency": dependency,
                        "confidence": "medium",
                        "evidence": [
                            "dependency executor returned APPLIED",
                            "dependency declared by predicate-level requirement",
                            "consumer succeeded after provisional dependency chain",
                        ],
                    }
                )
                if dependency_result.state_after is not None:
                    trial_state = dependency_result.state_after
                final_result = self.applicator.apply(
                    self.library.get_model(model_id), trial_state
                )
                if final_result.status in _SUCCESS:
                    break

            if final_result.status in _SUCCESS:
                repaired.extend(trial_dependencies)
                trace.extend(trial_trace)
                operations.extend(trial_operations)
                skip_indices.update(trial_skip_indices)
                repaired.append(model_id)
                trace.append(
                    self._trace(index, model_id, final_result.status.value)
                )
                if final_result.state_after is not None:
                    state = final_result.state_after
            else:
                repaired.append(model_id)
                trace.append(
                    self._trace(index, model_id, initial_result.status.value)
                )

        return tuple(repaired), trace, operations
    def _unique_sibling(self, model_id, state):
        group = _sibling_group(model_id)
        if not group:
            return None
        original_type = _TYPE_BY_MODEL.get(model_id)
        original_type_present = (
            original_type is not None
            and any(
                symbol.type_name == original_type
                for symbol in state.symbols.values()
            )
        )
        candidates = []
        for candidate_id in group:
            if candidate_id == model_id:
                continue
            candidate_type = _TYPE_BY_MODEL.get(candidate_id)
            if (
                original_type_present
                and original_type is not None
                and candidate_type != original_type
            ):
                continue
            if candidate_type is not None:
                candidate_entities = [
                    symbol
                    for symbol in state.symbols.values()
                    if symbol.type_name == candidate_type
                ]
                if len(candidate_entities) != 1:
                    continue
            capability = self.library.get_capability(candidate_id)
            if capability.support_level != SupportLevel.CONCRETE:
                continue
            result = self.applicator.apply(
                self.library.get_model(candidate_id), state
            )
            if result.status == ApplicationStatus.APPLIED:
                candidates.append((candidate_id, result))
        return candidates[0] if len(candidates) == 1 else None

    def _applicable_dependencies(self, model_id, state, excluded):
        requirement = self.library.get_requirement(model_id)
        if requirement is None:
            return []
        candidates = []
        for dependency in requirement.dependencies:
            if dependency in excluded:
                continue
            capability = self.library.get_capability(dependency)
            if capability.support_level != SupportLevel.CONCRETE:
                continue
            result = self.applicator.apply(
                self.library.get_model(dependency), state
            )
            if result.status == ApplicationStatus.APPLIED:
                candidates.append((dependency, result))
        return candidates

    def _replay(self, sequence, initial_state):
        state = initial_state
        trace = []
        for index, model_id in enumerate(sequence):
            capability = self.library.get_capability(model_id)
            if capability is None:
                trace.append(self._trace(index, model_id, "UNKNOWN_MODEL"))
                continue
            if capability.support_level == SupportLevel.SPECIFICATION_ONLY:
                trace.append(self._trace(index, model_id, "SPECIFICATION_ONLY"))
                continue
            result = self.applicator.apply(
                self.library.get_model(model_id), state
            )
            trace.append(self._trace(index, model_id, result.status.value))
            if result.state_after is not None:
                state = result.state_after
        return trace

    @staticmethod
    def _semantic_flags(row, sequence):
        process = str(row.get("process") or "")
        flags = []
        for model_id in sequence:
            if model_id not in _SEMANTIC_MODEL_IDS:
                continue
            cues = _PROCESS_CUES[model_id]
            matched = [cue for cue in cues if cue in process]
            flags.append(
                {
                    "model_id": model_id,
                    "status": (
                        "legacy_semantics_unverified"
                        if matched
                        else "likely_semantic_drift"
                    ),
                    "matched_cues": matched,
                    "selector_weight_recommendation": 0,
                }
            )
        return flags

    @staticmethod
    def _quality(observed_trace, executable_trace, semantic_flags, errors):
        observed_full = V3DryRunRepairer._fully_replayable(observed_trace)
        executable_full = V3DryRunRepairer._fully_replayable(executable_trace)
        likely_drift = any(
            flag["status"] == "likely_semantic_drift"
            for flag in semantic_flags
        )
        if observed_full and not semantic_flags and not errors:
            return "A"
        if executable_full and not semantic_flags and not errors:
            return "B"
        if not likely_drift and not errors:
            return "C"
        return "D"

    @staticmethod
    def _fully_replayable(trace):
        return bool(trace) and all(
            step["status"] in {"APPLIED", "ALREADY_KNOWN"}
            for step in trace
        )

    @staticmethod
    def _future_index(sequence, target, start, skipped):
        for index in range(start, len(sequence)):
            if index not in skipped and sequence[index] == target:
                return index
        return None

    @staticmethod
    def _trace(index, model_id, status, original_model_id=None):
        item = {
            "index": index,
            "model_id": model_id,
            "status": status,
        }
        if original_model_id is not None:
            item["original_model_id"] = original_model_id
        return item


def summarize_manifests(manifests: Iterable[Dict[str, Any]]) -> Dict[str, Any]:
    manifests = list(manifests)
    operation_counts = Counter()
    operation_confidence_counts = Counter()
    replacement_pairs = Counter()
    semantic_counts = Counter()
    status_counts = {
        "original": Counter(),
        "observed": Counter(),
        "executable": Counter(),
    }
    quality = Counter()
    changed_observed = 0
    changed_executable = 0
    full = Counter()
    unparsed = 0
    adapter_errors = 0

    for item in manifests:
        quality[item["quality_candidate"]] += 1
        unparsed += item["unparsed_fact_count"]
        adapter_errors += len(item["adapter_errors"])
        if item["original_models"] != item["models_v3_observed"]:
            changed_observed += 1
        if item["models_v3_observed"] != item["models_v3_executable"]:
            changed_executable += 1
        for operation in (
            item["observed_operations"] + item["executable_operations"]
        ):
            operation_counts[operation["operation"]] += 1
            operation_confidence_counts[
                f"{operation['operation']}:{operation['confidence']}"
            ] += 1
            if operation["operation"] == "replace_misaligned_model":
                replacement_pairs[
                    f"{operation['before']}->{operation['after']}"
                ] += 1
        for flag in item["semantic_flags"]:
            semantic_counts[
                f"{flag['model_id']}:{flag['status']}"
            ] += 1
        for name, key in (
            ("original", "original_trace"),
            ("observed", "observed_trace"),
            ("executable", "executable_trace"),
        ):
            trace = item[key]
            status_counts[name].update(step["status"] for step in trace)
            if V3DryRunRepairer._fully_replayable(trace):
                full[name] += 1

    return {
        "rows_with_models": len(manifests),
        "changed_observed_rows": changed_observed,
        "changed_executable_rows": changed_executable,
        "operation_counts": dict(operation_counts),
        "operation_confidence_counts": dict(operation_confidence_counts),
        "replacement_pairs": dict(replacement_pairs),
        "semantic_flag_counts": dict(semantic_counts),
        "quality_candidates": dict(quality),
        "fully_replayable_rows": dict(full),
        "status_counts": {
            name: dict(counts)
            for name, counts in status_counts.items()
        },
        "unparsed_fact_atoms": unparsed,
        "adapter_errors": adapter_errors,
    }
