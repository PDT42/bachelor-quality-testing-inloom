"""
:Author: Paul Erlenwein
:Since: 2020/11/20

This is the module containing the ``Evaluation``.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Mapping

from data_types.result import Result


class EvaluationType(Enum):
    """These are the possible Evaluation types."""

    MANUAL = 'M'
    AUTOMATIC = 'A'


@dataclass
class Evaluation:
    """This is the representation of an Evaluation."""

    type: EvaluationType
    evaluator: str
    student_model_id: str
    expert_model_id: str

    # Results
    results: Mapping[str, Result]
    total_points: float

    # Statistics.
    no_matched_elements: int = None
    element_points: Mapping[str, int] = None

    def get_id(self):
        """Get an unique identifier for this Eval."""
        return hash(self.student_model_id + self.expert_model_id + self.evaluator)

    def __hash__(self):
        return self.get_id()
