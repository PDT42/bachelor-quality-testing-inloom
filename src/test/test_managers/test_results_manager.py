"""
:Author: Paul Erlenwein
:Since: 2020/12/02

These are tests for the results_manager module.
"""

import unittest
from copy import deepcopy
from typing import List
from uuid import UUID, uuid4

from data_types.evaluation import Evaluation, EvaluationType
from data_types.result import Result, ResultCategory
from db_connection.db_connection import SqliteConnection
from managers.results_manager import ResultsManager
from test.test_db_connection import init_test_sqlite_connection


class TestResultsManager(unittest.TestCase):
    """These are tests for the ``ResultsManager``."""

    # Constants
    BASE_XML_PATH: str = '../../../res/example-data/student-solutions/Aufgabe_1/Ergebnisse'
    EXPERT_MODEL_XML: str = f'{BASE_XML_PATH}/OUTPUT_Expert_OOA_Class_SoSe2018.xml'
    STUDENT_MODEL_XML: str = f'{BASE_XML_PATH}/OUTPUT_ExSS2018_student1.xml'

    TEST_RESULT: Result = Result(
        expert_element_label='expert_model_element',
        student_element_label='student_model_element',
        expert_element_type='expert_type',
        student_element_type='student_type',
        rule_id='R00000',
        result_category=ResultCategory.CORRECT,
        points=100.0,
        feedback_message='You\'re the best!'
    )

    def setUp(self) -> None:
        """Setup test requirements."""

        init_test_sqlite_connection()

        self.test_db_connection = SqliteConnection.get()
        self.results_manager = ResultsManager.get()

    def tearDown(self) -> None:
        """Clean up after tests."""

        self.test_db_connection.close()
        ResultsManager._instance = None

    def test_insert_results(self):
        """Test ResultManagers Function ``insert_results``."""

        self.TEST_RESULT.evaluation_id = None
        self.assertRaises(ValueError, self.results_manager.insert_results, [self.TEST_RESULT])
        self.TEST_RESULT.evaluation_id = uuid4()
        self.results_manager.insert_results([self.TEST_RESULT])

    def test_get_one(self):
        """Test ResultManagers Function ``get_one``."""

        result_id: UUID = uuid4()
        self.TEST_RESULT.result_id = result_id
        self.TEST_RESULT.evaluation_id = uuid4()
        self.results_manager.insert_results([self.TEST_RESULT])



    def test_get_all_for(self):
        """Test ResultManagers Function ``get_all_for``."""

        invalid_evaluation_id: UUID = uuid4()
        self.TEST_RESULT.evaluation_id = invalid_evaluation_id
        self.results_manager.insert_results([self.TEST_RESULT])

        evaluation_id: UUID = uuid4()
        self.TEST_RESULT.evaluation_id = evaluation_id

        test_results: List[Result] = []
        for iterator in range(0, 10):
            self.TEST_RESULT.result_id = uuid4()
            test_results.append(deepcopy(self.TEST_RESULT))
        self.results_manager.insert_results(test_results)

        query_result: List[Result] = self.results_manager.get_all_for(evaluation_id)
        self.assertEqual(len(query_result), 10)
