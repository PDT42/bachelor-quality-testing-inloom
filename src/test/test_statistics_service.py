"""
:Author: Paul Erlenwein
:Since: 2020/11/20

These are tests for the ``StatisticsService``.
"""

import unittest
from typing import List
from uuid import uuid4

from data_types.evaluation import AutoEval
from statistics_service import StatisticsService
from xml_adapter import XMLAdapter


class TestStatisticsService(unittest.TestCase):
    """TestCase for the StatisticsService."""

    # Constants
    BASE_XML_PATH: str = '../../res/evaluations/automatic-evaluations/exam-st-2018/'
    EXPERT_MODEL_XML: str = f'{BASE_XML_PATH}/OUTPUT_Expert_OOA_Class_SoSe2018.xml'
    STUDENT_MODEL_XML: str = f'{BASE_XML_PATH}/OUTPUT_ExSS2018_student1.xml'

    # Variables
    expert_eval: AutoEval
    student_eval: AutoEval

    def setUp(self):
        """Setup test requirements."""

        test_data_set_id: str = str(uuid4())

        self.expert_eval = XMLAdapter.eval_from_xml(self.EXPERT_MODEL_XML).evaluation
        self.student_eval = XMLAdapter.eval_from_xml(self.STUDENT_MODEL_XML).evaluation

    def tearDown(self) -> None:
        """Clean up after tests."""

        pass

    def test_append_statistic(self):
        """Test StatisticService's Function ``append_statistic``."""

        self.expert_eval = StatisticsService.append_statistic(self.expert_eval)
        self.student_eval = StatisticsService.append_statistic(self.student_eval)
