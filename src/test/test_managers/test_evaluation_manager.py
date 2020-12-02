"""
:Author: Paul Erlenwein
:Since: 2020/12/02

These are tests for the evaluation_manager module.
"""

import unittest

from data_types.evaluation import Evaluation, EvaluationType
from data_types.result import Result, ResultCategory
from db_connection.db_connection import SqliteConnection
from managers.evaluation_manager import EvaluationManager
from test.test_db_connection import init_test_sqlite_connection


class TestEvaluationManager(unittest.TestCase):
    """These are tests for the ``EvaluationManager``."""

    # Constants
    BASE_XML_PATH: str = '../../../res/example-data/student-solutions/Aufgabe_1/Ergebnisse'
    EXPERT_MODEL_XML: str = f'{BASE_XML_PATH}/OUTPUT_Expert_OOA_Class_SoSe2018.xml'
    STUDENT_MODEL_XML: str = f'{BASE_XML_PATH}/OUTPUT_ExSS2018_student1.xml'

    TEST_AUTO_EVAL: Evaluation = Evaluation(
        type=EvaluationType.AUTOMATIC,
        evaluator='INLOOM',
        student_model_id='test_student_model_id',
        expert_model_id='test_expert_model_id',
        results=[],
        total_points=.0,
        max_points=.0
    )

    TEST_RESULT: Result = Result(
        expert_element_label='expert_model_element',
        student_element_label='student_model_element',
        expert_element_type='expert_type',
        student_element_type='student_type',
        rule_id='R00000',
        result_category=ResultCategory.CORRECT,
        points=100.0,
        feedback_message='You\'re the best!',
        evaluation_id=TEST_AUTO_EVAL.evaluation_id
    )

    def setUp(self) -> None:
        """Setup test requirements."""

        init_test_sqlite_connection()

        self.test_db_connection = SqliteConnection.get()
        self.test_eval_manager = EvaluationManager.get()

        pass

    def tearDown(self) -> None:
        """Clean up after tests."""

        self.test_db_connection.close()
        EvaluationManager._instance = None

    def test_insert_evaluations(self):
        """Test EvaluationManagers Function ``insert_evaluation``."""

        self.TEST_AUTO_EVAL.results = [self.TEST_RESULT]
        self.test_eval_manager.insert_evaluations([self.TEST_AUTO_EVAL])