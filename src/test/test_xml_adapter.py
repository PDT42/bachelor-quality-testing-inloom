"""
:Author: Paul Erlenwein
:Since: 2020/11/20

These are tests intended for the ``XMLAdapter`` class.
"""

import unittest
from uuid import uuid4

from data_types.result import Result
from xml_adapter import XMLAdapter, XMLAdapterResult


# TODO: Implement actual tests

class TestXMLAdapter(unittest.TestCase):
    """TestCase for the XMLAdapter."""

    # Constants
    BASE_XML_PATH: str = '../../res/evaluations/automatic-evaluations/exam-st-2018'
    EXPERT_MODEL_XML: str = f'{BASE_XML_PATH}/OUTPUT_Expert_OOA_Class_SoSe2018.xml'
    STUDENT_MODEL_XML: str = f'{BASE_XML_PATH}/OUTPUT_ExSS2018_student1.xml'

    # Variables
    expert_adapter: XMLAdapter
    student_adapter: XMLAdapter

    def setUp(self) -> None:
        """Setup test requirements."""

        self.expert_adapter = XMLAdapter(self.EXPERT_MODEL_XML)
        self.student_adapter = XMLAdapter(self.STUDENT_MODEL_XML)

    def tearDown(self) -> None:
        """Clean up after tests."""

        pass

    def test_get_required_tags(self):
        """Test XMLAdapters Function ``_get_required_tags``."""

        self.expert_adapter._get_required_tags()

    def test_get_required_data_attributes(self):
        """Test XMLAdapters Function ``get_required_data_attributes``."""

        self.expert_adapter._get_required_data_attributes()

    def test_get_required_results_contents(self):
        """Test XMLAdapters Function ``get_required_results_content``."""

        expert_element_name: str = 'r1'
        expert_element_type: str = 'Relationship'
        student_element_label: str = 'r1'
        student_element_type: str = 'Relationship'
        result_category: str = 'CORRECT'
        points: float = 1.0
        feedback_message: str = 'A Relationship between Paper and Paper was found (Type: Association).'
        result_type: str = 'CONSTRAINT'
        graded_feature_id: str = 'R080101'

        self.expert_adapter._get_required_results_contents()
        first_adapter_result: Result = self.expert_adapter.results[0]

        self.assertEqual(first_adapter_result.expert_element_name, expert_element_name)
        self.assertEqual(first_adapter_result.expert_element_type, expert_element_type)
        self.assertEqual(first_adapter_result.student_element_label, student_element_label)
        self.assertEqual(first_adapter_result.student_element_type, student_element_type)
        self.assertEqual(first_adapter_result.result_category.name, result_category)
        self.assertEqual(first_adapter_result.points, points)
        self.assertEqual(first_adapter_result.feedback_message, feedback_message)
        self.assertEqual(first_adapter_result.result_type, result_type)
        self.assertEqual(first_adapter_result.graded_feature_id, graded_feature_id)

    def test_eval_from_xml(self):
        """Test XMLAdapters Function ``eval_from_xml``."""

        test_data_set_id: str = str(uuid4())

        exp_auto_eval: XMLAdapterResult = XMLAdapter.eval_from_xml(xml_path=self.EXPERT_MODEL_XML)
        stud_auto_eval: XMLAdapterResult = XMLAdapter.eval_from_xml(xml_path=self.EXPERT_MODEL_XML)
