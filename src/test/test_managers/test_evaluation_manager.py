"""
:Author: Paul Erlenwein
:Since: 2020/12/02

These are tests for the evaluation_manager module.
"""

import unittest

from data_types.evaluation import AutoEval
from data_types.result import Result
from data_types.result_category import ResultCategory
from db_connection.db_connection import SqliteConnection
from managers.evaluation_manager import EvalManager
from managers.results_manager import ResultManager
from managers.testdata_manager import TDManager
from test.test_db_connection import init_test_sqlite_connection


class TestEvaluationManager(unittest.TestCase):
    """These are tests for the ``EvalManager``."""

    # Constants
    BASE_XML_PATH: str = '../../../res/example-data/student-solutions/Aufgabe_1/Ergebnisse'
    EXPERT_MODEL_XML: str = f'{BASE_XML_PATH}/OUTPUT_Expert_OOA_Class_SoSe2018.xml'
    STUDENT_MODEL_XML: str = f'{BASE_XML_PATH}/OUTPUT_ExSS2018_student1.xml'

    TEST_AUTO_EVAL: AutoEval = AutoEval(
        exercise_id='test_exercise_id',
        expert_solution_id='test_expert_model_id',
        student_id='test_student',
        evaluation_type='A',
        test_data_set_id='test_test_data_set',
        total_points=4.20,
        file_path='test_path',
        #
        mcs_identifier='test_mcs_id',
        mcs_version='test_mcs_version'
    )

    TEST_RESULT: Result = Result(
        expert_element_label='test_expert_element_label',
        expert_element_type='test_expert_element_type',
        student_element_label='test_student_element_label',
        student_element_type='test_student_element_type',
        result_type='CONSTRAINT',
        graded_feature_id='R00000',
        result_category=ResultCategory.CORRECT,
        points=100.0,
        feedback_message='You\'re the best!',
        evaluation_id=TEST_AUTO_EVAL.evaluation_id
    )

    def setUp(self) -> None:
        """Setup test requirements."""

        init_test_sqlite_connection()

        self.test_db_connection = SqliteConnection.get()
        self.test_eval_manager = EvalManager()
        self.test_eval_manager.init_database_tables()
        self.test_eval_manager.results_manager.init_database_table()

    def tearDown(self) -> None:
        """Clean up after tests."""

        self.test_db_connection.close()
        SqliteConnection._instance = None
        TDManager._instance = None
        EvalManager._instance = None
        ResultManager._instance = None

    def test_insert_evaluations(self):
        """Test EvaluationManagers Function ``insert_evaluation``."""

        self.TEST_AUTO_EVAL.results = [self.TEST_RESULT]
        self.test_eval_manager.insert_evaluations([self.TEST_AUTO_EVAL])
