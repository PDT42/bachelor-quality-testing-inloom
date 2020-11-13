"""
:Author: Paul Erlenwein
:Since: 2020/11/20

This is the module containing the XMLAdapter.
"""

import os
import xml.etree.ElementTree as XML
from typing import List

from data_types.evaluation import Evaluation, EvaluationType


class XMLAdapter:
    """This is the ``XMLAdapter``, it's used for
    interactions with the result .xml files.
    """

    # Constants
    # °°°°°°°°°
    # TODO: Implement this and _has... functions as *format* class
    ROOT_TAG: str = 'TestResult'
    DATA_TAG: str = 'TestData'
    E_MODEL_TAG: str = 'ExpertModel'
    S_MODEL_TAG: str = 'TestModel'
    M_MODEL_TAG: str = 'MetaModel'
    MCS_ID_TAG: str = 'MCSIdentifier'
    MCS_VERSION_TAG: str = 'MCSVersion'
    RESULTS_TAG: str = 'Results'
    RESULT_TAG: str = 'Result'
    POINTS_TAG: str = 'ResultPoints'
    S_POINTS_TAG: str = 'TestPoints'

    ROOT_CHILDREN: List[str] = [DATA_TAG, RESULTS_TAG, POINTS_TAG]
    DATA_CHILDREN: List[str] = [E_MODEL_TAG, S_MODEL_TAG]
    POINTS_CHILDREN: List[str] = [S_POINTS_TAG]

    # Variables
    # °°°°°°°°°
    xml_path: str
    xml_tree: XML.ElementTree
    xml_root: XML.Element

    # INLOOM result xml specifics
    data_node: XML.Element
    results_node: XML.Element
    points_node: XML.Element

    # INLOOM result data attributes
    e_model_id: str
    s_model_id: str
    m_model_type: str
    mcs_id: str
    mcs_version: str

    def __init__(self, xml_path):
        """Create a new ``XMLAdapter``."""

        # Check if XML file exists
        if not os.path.exists(xml_path):
            raise FileNotFoundError(f"No file could be found at: {xml_path}!")

        # Parse XML file
        self.xml_path = xml_path
        self.xml_tree = XML.parse(xml_path)
        self.xml_root = self.xml_tree.getroot()

        # Check XML soundness and get required values
        if not self._get_required_tags():
            raise KeyError('Some of the required tags are missing from the XML file provided!')
        if not self._get_required_data_attributes():
            raise KeyError('Some of the required tag attributes are missing from the XML file provided!')

    def _get_required_tags(self) -> bool:
        """Check if all the Tags required for building a
        ``TestDataSet`` are present in the ``xml_tree``
        and store em in the appropriate adapter fields.
        """

        if not self.xml_root.tag == self.ROOT_TAG:
            return False
        if not all([(tag in [c.tag for c in self.xml_root]) for tag in self.ROOT_CHILDREN]):
            return False

        self.data_node = self.xml_root.find(self.DATA_TAG)
        if not all([(tag in [c.tag for c in self.data_node]) for tag in self.DATA_CHILDREN]):
            return False

        self.results_node = self.xml_root.find(self.RESULTS_TAG)
        if not len(list(self.results_node.findall(self.RESULT_TAG))) > 0:
            return False

        self.points_node = self.xml_root.find(self.POINTS_TAG)
        if not all([(tag in [c.tag for c in self.points_node]) for tag in self.POINTS_CHILDREN]):
            return False

        return True

    def _get_required_data_attributes(self):
        """Check if all the required tag attributes for
        building a ``TestDataSet`` are present in the
        ``xml_tree`` and store em in the appropriate
        adapter fields.
        """

        e_model_node = self.data_node.find(self.E_MODEL_TAG)
        if 'id' not in e_model_node.attrib.keys():
            return False
        self.e_model_id = e_model_node.attrib['id']

        s_model_node = self.data_node.find(self.E_MODEL_TAG)
        if 'id' not in s_model_node.attrib.keys():
            return False
        self.s_model_id = s_model_node.attrib['id']

        m_model_node = self.data_node.find(self.E_MODEL_TAG)
        if 'type' not in s_model_node.attrib.keys():
            return False
        self.m_model_type = m_model_node.attrib['type']

        mcs_id_node = self.data_node.find(self.MCS_ID_TAG)
        if 'id' not in mcs_id_node.attrib.keys():
            return False
        self.mcs_id = mcs_id_node.attrib['id']

        mcs_version_node = self.data_node.find(self.MCS_VERSION_TAG)
        if 'value' not in mcs_version_node.attrib.keys():
            return False
        self.mcs_version = mcs_version_node.attrib['value']

        return True

    def _get_required_point_values(self):
        """Check if all the required point value for
        building a ``TestDataSet`` are present in the
        ``xml_tree`` and store em in the appropriate
        adapter fields.
        """

    @staticmethod
    def eval_from_xml(
            xml_path: str,
            eval_type: EvaluationType,
            evaluator: str = 'INLOOM'
    ) -> Evaluation:
        """Create an ``Evaluation`` from the contents of the xml supplied."""

        xml_adapter = XMLAdapter(xml_path)

        # TODO

        return Evaluation(
            type=eval_type,
            evaluator=evaluator,
            student_model_id=xml_adapter.s_model_id,
            expert_model_id=xml_adapter.e_model_id,
            total_points=0,  # TODO
        )
