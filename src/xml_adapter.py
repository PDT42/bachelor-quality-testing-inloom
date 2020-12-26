"""
:Author: Paul Erlenwein
:Since: 2020/11/20

This is the module containing the XMLAdapter.
"""

import os
import xml.etree.ElementTree as XML
from dataclasses import dataclass
from typing import Dict, List
from uuid import uuid4

from data_types.evaluation import AutoEval, Evaluation
from data_types.expert_solution import ExpertSolution
from data_types.result import Result
from data_types.result_category import ResultCategory


@dataclass
class XMLAdapterResult:
    """This is an XMLAdapterResult"""

    evaluation: AutoEval
    max_points: float


class XMLAdapter:
    """This is the ``XMLAdapter``, it's used for
    interactions with the result .xml files.
    """

    # Constants
    # °°°°°°°°°
    # TODO: Implement this and _has... functions as *format* class
    # TODO: Outsource these to a config.ini or a config, that is
    # TODO: loaded along with the xml files.

    ROOT_TAG: str = 'TestResult'
    # \
    DATA_TAG: str = 'TestData'
    # \\
    EXP_MODEL_TAG: str = 'ExpertModel'
    STUD_MODEL_TAG: str = 'TestModel'
    META_MODEL_TAG: str = 'MetaModel'
    MCS_ID_TAG: str = 'MCSIdentifier'
    MCS_VERSION_TAG: str = 'MCSVersion'
    # \
    RESULTS_TAG: str = 'Results'
    # \\
    RESULT_TAG: str = 'Result'
    # \\\
    EXP_OBJ_TAG: str = 'ExpertObject'
    EXP_TYPE_TAG: str = 'ExpertType'
    STUD_OBJ_TAG: str = 'TestObject'
    STUD_TYPE_TAG: str = 'TestType'
    RULE_TAG: str = 'Rule'
    CATEGORY_TAG: str = 'Category'
    RESULT_POINTS_TAG: str = 'Points'
    MESSAGE_TAG: str = 'Msg'
    # \
    POINTS_TAG: str = 'ResultPoints'
    # \\
    STUD_POINTS_TAG: str = 'TestPoints'
    MAX_POINTS_TAG: str = 'MaxPoints'
    # --
    ROOT_CHILDREN: List[str] = [DATA_TAG, RESULTS_TAG, POINTS_TAG]
    DATA_CHILDREN: List[str] = [EXP_MODEL_TAG, STUD_MODEL_TAG]
    POINTS_CHILDREN: List[str] = [STUD_POINTS_TAG, MAX_POINTS_TAG]

    # Variables
    # °°°°°°°°°
    xml_path: str
    xml_tree: XML.ElementTree
    xml_root: XML.Element

    evaluation_id: str

    # INLOOM result xml specifics
    data_node: XML.Element
    results_node: XML.Element
    points_node: XML.Element

    # INLOOM result data attributes
    exp_model_id: str
    stud_model_id: str
    meta_model_type: str
    mcs_id: str
    mcs_version: str
    results: List[Result]
    student_points: float
    max_points: float

    def __init__(self, xml_path):
        """Create a new ``XMLAdapter``."""

        # Check if XML file exists
        if not os.path.exists(xml_path):
            raise FileNotFoundError(f"No file could be found at: {xml_path}!")

        self.evaluation_id = str(uuid4())

        # Parse XML file
        self.xml_path = xml_path
        self.xml_tree = XML.parse(xml_path)
        self.xml_root = self.xml_tree.getroot()

        # Check XML soundness and get required values
        if not self._get_required_tags():
            raise KeyError('Some of the required tags are missing from the XML file provided!')
        if not self._get_required_data_attributes():
            raise KeyError('Some of the required tag attributes are missing from the XML file provided!')
        if not self._get_required_point_contents():
            raise KeyError('Some of the required point values are missing from the XML file provided!')
        if not self._get_required_results_contents():
            raise KeyError('Some of the required result values are missing from the XML file provided!')

    def _get_required_tags(self) -> bool:
        """Check if all the Tags required for building a
        ``TestDataSet`` are present in the ``xml_tree``
        and store em in the appropriate adapter fields.
        """

        # TODO: Supply individual Error Messages ...
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

        # TODO: Supply individual Error Messages ...
        e_model_node: XML.Element = self.data_node.find(self.EXP_MODEL_TAG)
        if 'id' not in e_model_node.attrib.keys():
            return False
        self.exp_model_id = e_model_node.attrib['id']

        s_model_node: XML.Element = self.data_node.find(self.STUD_MODEL_TAG)
        if 'id' not in s_model_node.attrib.keys():
            return False
        self.stud_model_id = s_model_node.attrib['id']

        m_model_node: XML.Element = self.data_node.find(self.META_MODEL_TAG)
        if 'type' not in m_model_node.attrib.keys():
            return False
        self.meta_model_type = m_model_node.attrib['type']

        mcs_id_node: XML.Element = self.data_node.find(self.MCS_ID_TAG)
        if 'id' not in mcs_id_node.attrib.keys():
            return False
        self.mcs_id = mcs_id_node.attrib['id']

        mcs_version_node: XML.Element = self.data_node.find(self.MCS_VERSION_TAG)
        if 'value' not in mcs_version_node.attrib.keys():
            return False
        self.mcs_version = mcs_version_node.attrib['value']

        return True

    def _get_required_point_contents(self):
        """Check if all the required point contents for
        building a ``TestDataSet`` are present in the
        ``xml_tree`` and store em in the appropriate
        adapter fields.
        """
        test_points_node: XML.Element = self.points_node.find(self.STUD_POINTS_TAG)
        if test_points_node is None:
            return False
        self.student_points = float(test_points_node.text)

        max_points_node: XML.Element = self.points_node.find(self.MAX_POINTS_TAG)
        if max_points_node is None:
            return False
        self.max_points = float(max_points_node.text)

        return True

    def _get_required_results_contents(self):
        """Check if all the required result contents for
        building a ```TestDataSet`` are present in the
        ``xml_tree`` and store em in the appropriate
        adapter fields.
        """

        self.results = []

        self.results_node: XML.Element = self.xml_root.find(self.RESULTS_TAG)
        if self.results_node is None:
            return False

        xml_results = self.results_node.findall(self.RESULT_TAG)
        if xml_results is None or not len(xml_results) > 0:
            return False

        # Converting the found result data
        for xml_result in xml_results:
            expert_label: str = str(xml_result.find(self.EXP_OBJ_TAG).text)
            expert_type: str = str(xml_result.find(self.EXP_TYPE_TAG).text)
            expert_element: str = f"{expert_type}-{expert_label}"

            student_label: str = str(xml_result.find(self.EXP_OBJ_TAG).text)
            student_type: str = str(xml_result.find(self.EXP_TYPE_TAG).text)
            student_element: str = f"{student_type}-{student_label}"

            self.results.append(Result(
                evaluation_id=self.evaluation_id,
                expert_element_label=str(xml_result.find(self.EXP_OBJ_TAG).text),
                expert_element_type=str(xml_result.find(self.EXP_TYPE_TAG).text),
                student_element_label=str(xml_result.find(self.EXP_OBJ_TAG).text),
                student_element_type=str(xml_result.find(self.EXP_TYPE_TAG).text),
                result_category=ResultCategory[str(xml_result.find(self.CATEGORY_TAG).text)],
                points=float(xml_result.find(self.RESULT_POINTS_TAG).text),
                feedback_message=str(xml_result.find(self.MESSAGE_TAG).text),
                result_type='CONSTRAINT',
                graded_feature_id=str(xml_result.find(self.RULE_TAG).text)))

        return True

    @staticmethod
    def eval_from_xml(xml_path: str) -> XMLAdapterResult:
        """Create an ``AutoEval`` from the contents of the xml supplied."""

        xml_adapter = XMLAdapter(xml_path)

        # TODO: Ask to change expert test model id
        stud_model_id: List[str] = xml_adapter.stud_model_id.split('_')
        if len(stud_model_id) == 2:
            exercise_id, student_id = stud_model_id
        elif len(stud_model_id) == 4:
            exercise_id = f'Ex{stud_model_id[3][0]}S{stud_model_id[3][4:]}'
            student_id = '_'.join(stud_model_id[:3])
        else:
            raise ValueError("The provided test model id does not comply with the naming scheme!")
        return XMLAdapterResult(
            evaluation=AutoEval(
                test_data_set_id=None,
                exercise_id=exercise_id,
                expert_solution_id=xml_adapter.exp_model_id,
                student_id=student_id,
                results=xml_adapter.results,
                total_points=xml_adapter.student_points,
                max_points=xml_adapter.max_points,
                evaluation_id=xml_adapter.evaluation_id,
                mcs_identifier=xml_adapter.mcs_id,
                mcs_version=xml_adapter.mcs_version,
                meta_model_type=xml_adapter.meta_model_type
            ), max_points=xml_adapter.max_points)

    @staticmethod
    def expert_solution_from_xml(xml_path: str):
        """Extract the elements of an expert solution from an expert xml."""

        xml_adapter = XMLAdapter(xml_path)

        exp_model_id: str = xml_adapter.exp_model_id
        std_model_id: str = xml_adapter.stud_model_id

        if exp_model_id != std_model_id:
            raise ValueError("INVALID FILE: Please use an evaluation of a valid expert solution for this!")

        eval_expert: Evaluation = XMLAdapter.eval_from_xml(xml_path).evaluation

        elements: Dict[str, List[str]] = {}
        for result in eval_expert.results:
            if result.expert_element_type not in elements:
                elements[result.expert_element_type] = []
            elements[result.expert_element_type].append(
                result.expert_element_label)

        return ExpertSolution(
            exercise_id=eval_expert.exercise_id,
            expert_solution_id=eval_expert.expert_solution_id,
            file=xml_path, elements=elements
        ), eval_expert.meta_model_type
