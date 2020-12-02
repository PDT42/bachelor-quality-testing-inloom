"""
:Author: Paul Erlenwein
:Since: 2020/11/20

These are tests for the ``StatisticsService``.
"""

import unittest
from typing import List

from data_types.evaluation import Evaluation
from statistics_service import StatisticsService
from xml_adapter import XMLAdapter


class TestStatisticsService(unittest.TestCase):
    """TestCase for the StatisticsService."""

    # Constants
    BASE_XML_PATH: str = '../../res/example-data/student-solutions/Aufgabe_1/Ergebnisse'
    EXPERT_MODEL_XML: str = f'{BASE_XML_PATH}/OUTPUT_Expert_OOA_Class_SoSe2018.xml'
    STUDENT_MODEL_XML: str = f'{BASE_XML_PATH}/OUTPUT_ExSS2018_student1.xml'

    # Variables
    expert_eval: Evaluation
    student_eval: Evaluation
    test_evals: List[Evaluation]

    def setUp(self):
        """Setup test requirements."""

        self.expert_eval = XMLAdapter.eval_from_xml(self.EXPERT_MODEL_XML)
        self.student_eval = XMLAdapter.eval_from_xml(self.STUDENT_MODEL_XML)

        self.test_evals = XMLAdapter.evals_from_directory(self.BASE_XML_PATH)

    def tearDown(self) -> None:
        """Clean up after tests."""

        pass

    def test_append_statistic(self):
        """Test StatisticService's Function ``append_statistic``."""

        self.expert_eval = StatisticsService.append_statistic(self.expert_eval)
        self.student_eval = StatisticsService.append_statistic(self.student_eval)

    def test_append_statistics_to_all(self):
        """Test StatisticsService's Function ``append_statistics_to_all``."""

        self.test_evals = StatisticsService.append_statistics_to_all(self.test_evals)