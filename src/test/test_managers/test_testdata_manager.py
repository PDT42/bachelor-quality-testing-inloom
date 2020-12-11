"""
:Author: Paul Erlenwein
:Since: 2020/11/20

These are tests for the testdata_manager module.
"""

import unittest
from uuid import uuid4

from data_types.evaluation import Evaluation, EvaluationType
from data_types.constraintresult import ConstraintResult, ConstraintResultCategory
from data_types.testdataset import TestDataSet
from db_connection.db_connection import SqliteConnection
from managers.constraint_results_manager import CResultManager
from managers.evaluation_manager import EvalManager
from managers.testdata_manager import TDManager
from test.test_db_connection import init_test_sqlite_connection


class TestTDManager(unittest.TestCase):
    """These are tests for the ``TDManager``."""

    # Constants
    BASE_XML_PATH: str = '../../../res/example-data/student-solutions/Aufgabe_1/Ergebnisse'
    EXPERT_MODEL_XML: str = f'{BASE_XML_PATH}/OUTPUT_Expert_OOA_Class_SoSe2018.xml'
    STUDENT_MODEL_XML: str = f'{BASE_XML_PATH}/OUTPUT_ExSS2018_student1.xml'

    TEST_TEST_DATA_SET: TestDataSet = TestDataSet(
        expert_model_id='test_expert_model_id',
        student_model_id='test_student_model_id',
        meta_model_type='test_meta_model_type',
        mcs_identifier='test_mcs_identifier',
        mcs_version='0.0.0'
    )

    INVALID_TEST_DATA_SET: TestDataSet = TestDataSet(
        expert_model_id='invalid_expert_model_id',
        student_model_id='invalid_student_model_id',
        meta_model_type='invalid_meta_model_type',
        mcs_identifier='invalid_mcs_identifier',
        mcs_version='0.0.0'
    )

    TEST_AUTO_EVAL: Evaluation = Evaluation(
        type=EvaluationType.AUTOMATIC,
        evaluator='INLOOM',
        student_model_id='test_student_model_id',
        expert_model_id='test_expert_model_id',
        results=[],
        total_points=.0,
        max_points=.0
    )

    TEST_RESULT: ConstraintResult = ConstraintResult(
        expert_element_label='expert_model_element',
        student_element_label='student_model_element',
        expert_element_type='expert_type',
        student_element_type='student_type',
        rule_id='R00000',
        result_category=ConstraintResultCategory.CORRECT,
        points=100.0,
        feedback_message='You\'re the best!',
        evaluation_id=TEST_AUTO_EVAL.evaluation_id
    )

    def setUp(self) -> None:
        """Setup test requirements."""

        init_test_sqlite_connection()

        self.test_db_connection = SqliteConnection.get()
        self.test_td_manager = TDManager.get()

    def tearDown(self) -> None:
        """Clean up after tests."""

        self.test_db_connection.close()
        SqliteConnection._instance = None
        TDManager._instance = None
        EvalManager._instance = None
        CResultManager._instance = None

    def test_insert_test_data_set(self):
        """Test TDManagers Function ``insert_test_data_sets``."""

        self.test_td_manager.insert_test_data_sets([self.TEST_TEST_DATA_SET])

        self.TEST_TEST_DATA_SET.student_model_id = 'test_student_model_id2'
        self.TEST_TEST_DATA_SET.auto_eval = self.TEST_AUTO_EVAL
        self.TEST_TEST_DATA_SET.auto_eval_id = self.TEST_AUTO_EVAL.evaluation_id
        self.test_td_manager.insert_test_data_sets([self.TEST_TEST_DATA_SET])

        self.TEST_TEST_DATA_SET.student_model_id = 'test_student_model_id3'
        self.TEST_AUTO_EVAL.evaluation_id = uuid4()
        self.TEST_RESULT.evaluation_id = self.TEST_AUTO_EVAL.evaluation_id
        self.TEST_AUTO_EVAL.results = [self.TEST_RESULT]
        self.test_td_manager.insert_test_data_sets([self.TEST_TEST_DATA_SET])

    def test_get_all_test_data_sets(self):
        """Test TDManagers Function ``get_all_test_data_sets``."""

        self.test_td_manager.insert_test_data_sets([self.TEST_TEST_DATA_SET])
        result = self.test_td_manager.get_all_test_data_sets()
        self.assertTrue(len(result) > 0)
        self.assertEqual(result[0], self.TEST_TEST_DATA_SET)

    def test_register_evaluation(self):
        """Test TDManagers Function ``register_evaluation``."""

        self.test_td_manager.register_evaluation(self.TEST_AUTO_EVAL, 'mmt', 'mcs_id', '0.0.0')
