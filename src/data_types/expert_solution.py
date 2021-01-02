"""
:Author: Paul Erlenwein
:Since: 2020/12/22

This is the module for the ``ExpertSolution``.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, Set


@dataclass
class ExpertElement:
    """This is an expert element."""

    element_type: str
    element_name: str
    element_label: str

    def __hash__(self):
        return hash(
            f"{self.element_type}" + \
            f"{self.element_name}" + \
            f"{self.element_label}"
        )


@dataclass
class ExpertSolution:
    """This is an expert solution."""

    expert_solution_id: str
    file: str
    exercise_id: str
    maximum_points: float
    elements: Dict[str, Set[ExpertElement]] = field(default_factory=dict)
    created_time: int = field(default_factory=lambda: int(datetime.now().timestamp()))

    def as_dict(self):
        _dict: Dict[str, Any] = self.__dict__
        _dict['elements'] = {
            key: [e.__dict__ for e in value] for key, value in self.elements.items()
        }

        return _dict
