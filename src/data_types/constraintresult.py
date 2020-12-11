"""
:Author: Paul Erlenwein
:Since: 2020/11/20

This is the module containing the ConstraintResult datatype.
"""

from dataclasses import dataclass, field
from enum import Enum
from uuid import uuid4


class ConstraintResultCategory(Enum):
    """These are the possible result categories."""

    MISSING = 'M'
    ERROR = 'E'
    WARNING = 'W'
    CORRECT = 'C'
    INFO = 'I'


@dataclass
class ConstraintResult:
    """This is the representation of a ConstraintResult."""

    expert_element_label: str
    student_element_label: str
    expert_element_type: str
    student_element_type: str
    rule_id: str
    result_category: ConstraintResultCategory
    points: float
    feedback_message: str
    evaluation_id: uuid4() = None
    result_id: uuid4 = field(default_factory=uuid4)

    def __eq__(self, other):
        """Check if ``self`` is ``equal`` to other."""

        return True if all([
            isinstance(other, ConstraintResult),
            other.expert_element_label == self.expert_element_label,
            other.student_element_label == self.student_element_label,
            other.expert_element_type == self.expert_element_type,
            other.student_element_type == self.student_element_type
        ]) else False
