"""
:Author: Paul Erlenwein
:Since: 2020/11/20

This is the module containing the TestDataSet datatype.
"""

from dataclasses import dataclass
from uuid import uuid4

from data_types.evaluation import Evaluation


@dataclass
class TestDataSet:
    """This is a ``TestDataSet``. It is the representation
    of a comparison of a **manEval** and an **autoEval**.
    """

    # Identifying Attributes
    expert_model_id: str
    student_model_id: str
    meta_model_type: str
    mcs_identifier: str
    mcs_version: str
    auto_eval_id: str
    man_eval_id: str

    # Evaluations
    auto_eval: Evaluation
    man_eval: Evaluation
