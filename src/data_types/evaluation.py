"""
:Author: Paul Erlenwein
:Since: 2020/11/20

This is the module containing the ``Evaluations``.
"""
from abc import abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Union
from uuid import uuid4

from data_types.result import Result


@dataclass
class Evaluation:
    """This is the representation of an AutoEval."""

    exercise_id: str
    expert_solution_id: str
    student_id: str

    evaluation_type: str

    test_data_set_id: str

    total_points: float = None

    file_path: str = None

    results: List[Result] = field(default_factory=list)

    evaluation_id: str = field(default_factory=lambda: str(uuid4()))
    created_time: int = field(default_factory=lambda: int(datetime.now().timestamp()))

    def __hash__(self):
        return self.evaluation_id

    def __str__(self):
        return f"{self.evaluation_type}-{self.exercise_id}-" + \
               f"{self.student_id}-{self.expert_solution_id}"

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        """Check if ``self`` is ``equal`` to other."""

        return True if all([
            other.exercise_id == self.exercise_id,
            other.expert_solution_id == self.expert_solution_id,
            other.student_id == self.student_id,
            other.evaluation_type == self.evaluation_type
        ]) else False

    def as_dict(self):
        _dict: Dict[str, Any] = self.__dict__
        _dict['results'] = [r.as_dict() for r in self.results]

        return _dict

    @staticmethod
    def from_child(child: Union['AutoEval', 'ManEval', dataclass]):
        """Create an Evaluation from an instance of one of its children."""

        return Evaluation(**{
            key: child.__dict__[key] for key in child.__dataclass_fields__.keys()
        })


class AutoEval(Evaluation):
    """This is the representation of an AutoEval."""

    mcs_identifier: str
    mcs_version: str

    def __init__(self, **kwargs):
        """Create a new ``ManEval``."""

        kwargs.update({'evaluation_type': 'A'})

        self.mcs_identifier = kwargs.pop('mcs_identifier', False)
        self.mcs_version = kwargs.pop('mcs_version', False)

        super(AutoEval, self).__init__(**kwargs)

    def __str__(self):
        return f"Auto-Eval-{super().__str__()}"

    def __eq__(self, other):
        """Check if ``self`` is ``equal`` to other."""

        return True if all([
            isinstance(other, AutoEval),
            other.mcs_identifier == self.mcs_identifier,
            other.mcs_version == self.mcs_version
        ]) and super().__eq__(other) else False


class ManEval(Evaluation):
    """This is the representation of a manual
    evaluation of a student model."""

    evaluator_id: str

    def __init__(self, **kwargs):
        """Create a new ``ManEval``."""

        kwargs.update({'evaluation_type': 'M'})

        self.evaluator_id = kwargs.pop('evaluator_id', False)

        if not self.evaluator_id:
            raise KeyError('MISSING KEY in result data: \'evaluator_id\'')

        super(ManEval, self).__init__(**kwargs)

    def __hash__(self):
        return self.evaluation_id

    def __str__(self):
        return f"Man-Eval-{super().__str__()}"

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        """Check if ``self`` is ``equal`` to other."""

        return True if all([
            isinstance(other, ManEval),
            other.evaluator_id == self.evaluator_id
        ]) and super().__eq__(other) else False

    @staticmethod
    def from_dict(man_eval_dict: Dict[str, Any], test_data_set_id):
        """Get a new ManEval from a dict."""

        eval_id: str = str(uuid4())

        return ManEval(
            evaluation_id=eval_id,
            exercise_id=str(man_eval_dict['exercise_id']),
            expert_solution_id=str(man_eval_dict['expert_solution_id']),
            student_id=str(man_eval_dict['student_id']),
            evaluator_id=str(man_eval_dict['evaluator_id']),
            evaluation_type=str(man_eval_dict['evaluation_type']),
            test_data_set_id=test_data_set_id,
            total_points=float(man_eval_dict['total_points']),
            results=[
                Result.from_dict(res, eval_id) for res in man_eval_dict['results']
            ])

