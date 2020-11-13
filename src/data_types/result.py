"""
:Author: Paul Erlenwein
:Since: 2020/11/20

This is the module containing the Result datatype.
"""

from dataclasses import dataclass
from enum import Enum


class ResultCategory(Enum):
    """These are the possible result categories."""

    MISSING = 'M'
    ERROR = 'E'
    WARNING = 'W'
    CORRECT = 'C'


@dataclass
class Result:
    """This is the representation of a Result."""

    expert_element_label: str
    student_element_label: str
    expert_element_type: str
    student_element_type: str
    rule_id: str
    result_category: ResultCategory
    points: float
    feedback_message: str
