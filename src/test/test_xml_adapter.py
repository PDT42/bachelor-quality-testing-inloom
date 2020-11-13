"""
:Author: Paul Erlenwein
:Since: 2020/11/20

These are tests intended for the ``XMLAdapter`` class.
"""

import unittest

from xml_adapter import XMLAdapter


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

    def test_has_required_tags(self):
        """Test XMLAdapters Function ``_has_required_tags``."""

        self.expert_adapter._get_required_tags()
