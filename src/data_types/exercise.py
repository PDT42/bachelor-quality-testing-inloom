"""
:Author: Paul Erlenwein
:Since: 2020/12/22

This is the module for the ``Exercise``.
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List
from uuid import uuid4

from data_types.expert_solution import ExpertSolution


@dataclass
class Exercise:
    """This is an exercise."""

    exercise_id: str
    used_in_year: int
    used_in_semester: str
    exercise_type: str
    meta_model_type: str
    expert_solutions: List[ExpertSolution] = None

    def as_dict(self):
        _dict: Dict[str, Any] = self.__dict__
        _dict['expert_solutions'] = \
            [e.as_dict() for e in self.expert_solutions]

        return _dict
