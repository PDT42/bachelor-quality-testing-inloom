"""
:Author: Paul Erlenwein
:Since: 2020/12/22

This is the module for the ``Exercise``.
"""

from dataclasses import dataclass, field
from typing import List
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
