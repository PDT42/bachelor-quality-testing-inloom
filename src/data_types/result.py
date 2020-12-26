"""
:Author: Paul Erlenwein
:Since: 2020/11/20

This is the module containing the CResult datatype.
"""

from dataclasses import dataclass, field
from typing import Any, Dict
from uuid import uuid4

from data_types.result_category import ResultCategory


@dataclass
class Result:
    """This is a Result."""

    evaluation_id: str

    expert_element_label: str
    expert_element_type: str
    student_element_label: str
    student_element_type: str

    result_category: ResultCategory
    points: float
    feedback_message: str

    result_type: str  # Either CONSTRAINT, MANUAL TODO: Enum? Remove?
    graded_feature_id: str

    result_id: str = field(default_factory=lambda: str(uuid4()))

    def __hash__(self):
        return self.result_id

    def __eq__(self, other):
        """Check if ``self`` is ``equal`` to other."""

        return True if all([
            isinstance(other, Result),
            other.expert_element_label == self.expert_element_label,
            other.expert_element_type == self.expert_element_type,
            other.student_element_label == self.student_element_label,
            other.student_element_type == self.student_element_type,
            other.result_type == self.result_type,
            other.result_category == self.result_category,
            other.evaluation_id == self.evaluation_id
        ]) else False

    @staticmethod
    def from_dict(result_dict: Dict[str, Any], evaluation_id: str):
        """Get a new Result from a dict."""

        return Result(
            evaluation_id=evaluation_id,
            expert_element_label=str(result_dict['expert_element_label']),
            expert_element_type=str(result_dict['expert_element_type']),
            student_element_label=str(result_dict['student_element_label']),
            student_element_type=str(result_dict['student_element_type']),
            result_category=ResultCategory(result_dict['result_category']),
            points=float(result_dict['points']),
            feedback_message=str(result_dict['feedback_message']),
            result_type=str(result_dict['result_type']),
            graded_feature_id=str(result_dict['graded_feature_id']))
