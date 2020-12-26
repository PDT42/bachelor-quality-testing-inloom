"""
:Author: Paul Erlenwein
:Since: 2020/12/22

This is the module for the ``ExpertSolution``.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List


@dataclass
class ExpertSolution:
    """This is an expert solution."""

    expert_solution_id: str
    file: str
    exercise_id: str
    elements: Dict[str, List[str]] = None
    created_time: int = field(default_factory=lambda: int(datetime.now().timestamp()))
