"""Correction rules enabled by the expanded concrete executor batch."""

from __future__ import annotations

from typing import Optional

from .correction import SequenceCorrector
from .state import InformationState


class ExpandedSequenceCorrector(SequenceCorrector):
    """Use state evidence to correct all conic orientation model IDs 3-10."""

    DIRECTIONAL_PARABOLA_IDS = tuple(range(3, 11))

    def _direction_from_state(self, state: InformationState) -> Optional[int]:
        matches = []
        for model_id in self.DIRECTIONAL_PARABOLA_IDS:
            model = self.library.get_model(model_id)
            if model.match(state):
                matches.append(model_id)
        return matches[0] if len(matches) == 1 else None
