"""
:Author: Paul Erlenwein
:Since: 2020/11/20

This is the module containing the ``Evaluation``.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Mapping
from uuid import uuid4

from data_types.element_match import ElementMatch, ExpertElement, StudentElement
from data_types.result import Result, ResultCategory


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
    results: List[Result]
    total_points: float
    max_points: float

    evaluation_id: uuid4 = uuid4()

    # Collections
    # TODO: Put this into 'statistics' var?
    results_by_expert_label: Dict[str, List[Result]] = None
    results_by_expert_type: Dict[str, List[Result]] = None
    results_by_student_label: Dict[str, List[Result]] = None
    results_by_student_type: Dict[str, List[Result]] = None
    results_by_rule: Dict[str, List[Result]] = None
    results_by_category: Dict[ResultCategory, List[Result]] = None
    results_by_expert_element: Dict[ExpertElement, List[Result]] = None
    results_by_student_element: Dict[StudentElement, List[Result]] = None

    # Statistics.
    number_of_mmu: int = None  # Number of unique ElementMatches found
    flag_count: Mapping[ResultCategory, int] = None  # How often was each category flag encountered?
    element_points: Mapping[ElementMatch, int] = None  # Sum of the points/ElementMatch
    rule_count: Mapping[str, int] = None  # How often was each rule_id encountered?
    # How often was which rule flagged with which category?
    categories_by_rule: Mapping[str, Mapping[ResultCategory, int]] = None

    def __hash__(self):
        return self.evaluation_id

    def __str__(self):
        return f"{self.type.value}-Eval-Model-{self.student_model_id}"

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        """Check if ``self`` is ``equal`` to other."""

        return True if all([
            isinstance(other, Evaluation),
            other.type == self.type,
            other.evaluator == self.evaluator,
            other.expert_model_id == self.expert_model_id,
            other.student_model_id == self.student_model_id,
            other.max_points == self.max_points  # TODO: Is this necessary?
        ]) else False
