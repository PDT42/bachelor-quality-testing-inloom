"""
:Author: Paul Erlenwein
:Since: 2020/11/20

This is the module containing the TestDataSet datatype.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import List
from uuid import uuid4

from data_types.evaluation import AutoEval, ManEval


@dataclass
class TestDataSet:
    """This is a ``TestDataSet``. It is the representation
    of a comparison of a **manEval** and an **autoEval**.
    """

    # Identifying Attributes
    exercise_id: str
    expert_solution_id: str
    student_id: str

    auto_evals: List[AutoEval] = field(default_factory=list)
    man_evals: List[ManEval] = field(default_factory=list)

    test_data_set_id: str = field(default_factory=lambda: str(uuid4()))
    created_time: int = field(default_factory=lambda: int(datetime.now().timestamp()))
