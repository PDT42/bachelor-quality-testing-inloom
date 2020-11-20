"""
:Author: Paul Erlenwein
:Since: 2020/11/20

These are tests intended for the ``XMLAdapter`` class.
"""

import unittest
import xml.etree.ElementTree as XML
from typing import List

from data_types.evaluation import Evaluation
from data_types.result import Result
from xml_adapter import XMLAdapter


# TODO: Implement actual tests

class TestXMLAdapter(unittest.TestCase):
    """TestCase for the XMLAdapter."""

    # Constants
    BASE_XML_PATH: str = '../../res/example-data/student-solutions/Aufgabe_1/Ergebnisse'
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

        result_xml_string: str = \
            "<Result>" + \
            "<ExpertObject>r1</ExpertObject>" + \
            "<ExpertType>Relationship</ExpertType>" + \
            "<TestObject>r1</TestObject>" + \
            "<TestType>Relationship</TestType>" + \
            "<Rule>R080101</Rule>" + \
            "<Category>CORRECT</Category>" + \
            "<Points>1.0</Points>" + \
            "<Msg>A Relationship between Paper and Paper was found (Type: Association).</Msg>" + \
            "</Result>"

        result_root: XML.Element = XML.fromstring(result_xml_string)

        expert_element_label: str = 'r1'
        expert_element_type: str = 'Relationship'
        student_element_label: str = 'r1'
        student_element_type: str = 'Relationship'
        rule_id: str = 'R080101'
        result_category: str = 'CORRECT'
        points: float = 1.0
        feedback_message: str = 'A Relationship between Paper and Paper was found (Type: Association).'

        self.expert_adapter._get_required_results_contents()
        first_adapter_result: Result = self.expert_adapter.results[0]

        self.assertEqual(first_adapter_result.expert_element_label, expert_element_label)
        self.assertEqual(first_adapter_result.expert_element_type, expert_element_type)
        self.assertEqual(first_adapter_result.student_element_label, student_element_label)
        self.assertEqual(first_adapter_result.student_element_type, student_element_type)
        self.assertEqual(first_adapter_result.rule_id, rule_id)
        self.assertEqual(first_adapter_result.result_category.name, result_category)
        self.assertEqual(first_adapter_result.points, points)
        self.assertEqual(first_adapter_result.feedback_message, feedback_message)

    def test_eval_from_xml(self):
        """Test XMLAdapters Function ``eval_from_xml``."""

        exp_auto_eval: Evaluation = XMLAdapter.eval_from_xml(xml_path=self.EXPERT_MODEL_XML)
        stud_auto_eval: Evaluation = XMLAdapter.eval_from_xml(xml_path=self.EXPERT_MODEL_XML)

    def test_evals_from_directory(self):
        """Test XMLAdapters Function ``evals_from_directory``."""

        auto_evals: List[Evaluation] = XMLAdapter.evals_from_directory(
            directory_path=self.BASE_XML_PATH)