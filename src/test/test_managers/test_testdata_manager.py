"""
:Author: Paul Erlenwein
:Since: 2020/11/20

These are tests for the testdata_manager module.
"""

import unittest

from data_types.evaluation import AutoEval
from data_types.result import Result
from data_types.result_category import ResultCategory
from data_types.test_data_set import TestDataSet
from db_connection.db_connection import SqliteConnection
from managers.evaluation_manager import EvalManager
from managers.result_manager import ResultManager
from managers.testdata_manager import TDManager
from test.test_db_connection import init_test_sqlite_connection


class TestTDManager(unittest.TestCase):
    """These are tests for the ``TDManager``."""

    # Constants
    BASE_XML_PATH: str = '../../../res/example-data/student-solutions/Aufgabe_1/Ergebnisse'
    EXPERT_MODEL_XML: str = f'{BASE_XML_PATH}/OUTPUT_Expert_OOA_Class_SoSe2018.xml'
    STUDENT_MODEL_XML: str = f'{BASE_XML_PATH}/OUTPUT_ExSS2018_student1.xml'

    # Test data generation
    @staticmethod
    def generate_tds(prefix: str):
        return TestDataSet(
            exercise_id=f'{prefix}_exercise_id',
            expert_solution_id=f'{prefix}_expert_solution_id',
            student_id=f'{prefix}_student_id'
        )

    @staticmethod
    def generate_auto_eval(tds_id: str):
        return AutoEval(
            test_data_set_id=tds_id,
            exercise_id='test_exercise_id',
            expert_solution_id='test_expert_model_id',
            student_id='test_student',
            total_points=.0,
            mcs_identifier='test_mcs_id',
            mcs_version='test_mcs_version',
        )

    @staticmethod
    def generate_result(eval_id: str):
        return Result(
            expert_element_label='test_expert_element_label',
            expert_element_type='test_expert_element_type',
            expert_element_name='test_expert_element_name',
            student_element_label='test_student_element_label',
            student_element_type='test_student_element_type',
            result_type='CONSTRAINT',
            graded_feature_id='R00000',
            result_category=ResultCategory.CORRECT,
            points=100.0,
            feedback_message='You\'re the best!',
            evaluation_id=eval_id
        )

    def setUp(self) -> None:
        """Setup test requirements."""

        init_test_sqlite_connection()

        self.test_db_connection = SqliteConnection.get()
        self.test_td_manager = TDManager()
        self.test_td_manager.init_database_table()

        self.TEST_TEST_DATA_SET: TestDataSet = self.generate_tds('test')
        self.TEST_AUTO_EVAL: AutoEval = self.generate_auto_eval(
            self.TEST_TEST_DATA_SET.test_data_set_id)
        self.TEST_RESULT: Result = self.generate_result(
            self.TEST_AUTO_EVAL.evaluation_id)

    def tearDown(self) -> None:
        """Clean up after tests."""

        self.test_db_connection.close()

        # Resetting singletons
        SqliteConnection._instance = None
        TDManager._instance = None
        EvalManager._instance = None
        ResultManager._instance = None

    def test_insert_test_data_set(self):
        """Test TDManagers Function ``insert_test_data_sets``."""

        self.test_td_manager.insert_test_data_sets([self.TEST_TEST_DATA_SET])

    def test_get_all_test_data_sets(self):
        """Test TDManagers Function ``get_all_test_data_sets``."""

        self.test_td_manager.insert_test_data_sets([self.TEST_TEST_DATA_SET])
        result = self.test_td_manager.get_all_test_data_sets()
        self.assertTrue(len(result) > 0)
        self.assertEqual(result[0], self.TEST_TEST_DATA_SET)

    def test_register_evaluation(self):
        """Test TDManagers Function ``register_evaluation``."""

        self.test_td_manager.register_evaluation(self.TEST_AUTO_EVAL)
