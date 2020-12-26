"""
:Author: Paul Erlenwein
:Since: 2020/11/20

This is the module for the ``StatisticsService``
"""

from itertools import groupby
from typing import Dict, List

from data_types.element_match import ElementMatch, \
    ExpertElement, StudentElement, TypeMatch
from data_types.evaluation import AutoEval
from data_types.result_category import ResultCategory
from data_types.result import Result


class StatisticsService:
    """This is the ``StatisticsService``."""

    @staticmethod
    def append_statistic(evaluation: AutoEval) -> AutoEval:
        """Perform a number of statistic surveys on a single ``AutoEval``.
        The constraint_results of these surveys are appended to the ``AutoEval``.

        Results in the INLOOM XML files have the following attributes.
        We will combine several of these attributes to make keys and
        collect constraint_results, with the same key attributes.

        | Key | XMLTag       | Description                           |
        | --- | ------------ | ------------------------------------- |
        | A   | ExpertObject | Element label in expert solution.     |
        | B   | ExpertType   | Type of Element in expert solution.   |
        | C   | TestObject   | Element label in student solution.    |
        | D   | TestType     | Type of Element in student solution.  |
        | E   | Rule         | ID of the rule that produced result.  |
        | F   | Category     | One of a set of category flags.       |
        | G   | Points       | Points awarded for found feature.     |
        | H   | Msg          | Feedback message provided to student. |

        """

        # Adding Collections to evaluation
        # °°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°

        # Collecting constraint_results by ExpertLabel A -> [CResult]
        results_by_expert_label: Dict[str, List[Result]] = {}
        for exp_label, exp_label_results in groupby(
                evaluation.results, key=lambda r: r.expert_element_label):
            results_by_expert_label[exp_label] = list(exp_label_results)
        evaluation.results_by_expert_label = results_by_expert_label

        # Collecting constraint_results by ExpertType B -> [CResult]
        results_by_expert_type: Dict[str, List[Result]] = {}
        for exp_type, exp_type_results in groupby(
                evaluation.results, key=lambda r: r.expert_element_type):
            results_by_expert_type[exp_type] = list(exp_type_results)
        evaluation.results_by_expert_type = results_by_expert_type

        # Collecting constraint_results by StudentLabel C -> [CResult]
        results_by_student_label: Dict[str, List[Result]] = {}
        for stud_label, stud_label_results in groupby(
                evaluation.results, key=lambda r: r.student_element_label):
            results_by_student_label[stud_label] = list(stud_label_results)
        evaluation.results_by_student_label = results_by_student_label

        # Collecting constraint_results by StudentType D -> [CResult]
        results_by_student_type: Dict[str, List[Result]] = {}
        for stud_type, stud_type_results in groupby(
                evaluation.results, key=lambda r: r.student_element_type):
            results_by_student_type[stud_type] = list(stud_type_results)
        evaluation.results_by_student_type = results_by_student_type

        # Collecting constraint_results by RuleId E -> [CResult]
        results_by_rule: Dict[str, List[Result]] = {}
        results_categories_by_rules: Dict[str, Dict[ResultCategory, List[Result]]] = {}
        for rule_id, rule_results in groupby(evaluation.results, key=lambda r: r.graded_feature_id):
            rule_results = list(rule_results)
            results_by_rule[rule_id] = rule_results

            # Collecting constraint_results by ResultCategory E -> (F -> [CResult])
            rule_results_by_category: Dict[ResultCategory, List[Result]] = {}
            for cat, res in groupby(rule_results, key=lambda r: r.result_category):
                rule_results_by_category[cat] = list(res)
            results_categories_by_rules[rule_id] = rule_results_by_category
        evaluation.results_by_rule = results_by_rule
        evaluation.results_categories_by_rules = results_categories_by_rules

        # Collecting constraint_results by ResultCategory F -> [CResult]
        results_by_category: Dict[ResultCategory, List[Result]] = {}
        for category, category_results in groupby(evaluation.results, key=lambda r: r.result_category):
            results_by_category[category] = list(category_results)
        evaluation.results_by_category = results_by_category

        # Collecting constraint_results by ExpertElement (A, B) -> [CResult]
        results_by_expert_element: Dict[ExpertElement, List[Result]] = {}
        for exp, exp_results in groupby(evaluation.results, key=lambda r: (
                r.expert_element_label, r.expert_element_type)):
            results_by_expert_element[ExpertElement(*exp)] = list(exp_results)
        evaluation.results_by_expert_element = results_by_expert_element

        # Collecting constraint_results by StudentElement (C, D) -> [CResult]
        results_by_student_element: Dict[StudentElement, List[Result]] = {}
        for stud, stud_results in groupby(evaluation.results, key=lambda r: (
                r.student_element_label, r.student_element_type)):
            results_by_student_element[StudentElement(*stud)] = list(stud_results)
        evaluation.results_by_student_element = results_by_student_element

        # Collecting constraint_results by StudentElement (B, C) -> [CResult]
        results_by_type_match: Dict[TypeMatch, List[Result]] = {}
        for type_match, type_match_results in groupby(evaluation.results, key=lambda r: (
                r.expert_element_type, r.student_element_type)):
            results_by_type_match[TypeMatch(*type_match)] = list(type_match_results)
        evaluation.results_by_type_match = results_by_type_match

        # Collecting constraint_results by ElementMatch (A, B, C, D) -> [CResult]
        results_by_mmu: Dict[ElementMatch, List[Result]] = {}
        for element_match, element_match_results in groupby(
                evaluation.results, key=lambda r: (
                        r.expert_element_label, r.expert_element_type,
                        r.student_element_label, r.student_element_type)):
            results_by_mmu[ElementMatch(*element_match)] = list(element_match_results)
        evaluation.results_by_mmu = results_by_mmu

        #
        # Adding info to evaluation
        # °°°°°°°°°°°°°°°°°°°°°°°°°

        # Number of unique ElementMatches found
        evaluation.number_of_mmu = len(results_by_mmu.keys())

        # How often was each category flag encountered?
        evaluation.flag_count = {flag: len(res) for flag, res in results_by_category.items()}

        # Sum of the points/ElementMatch
        evaluation.element_points = {
            em: sum(res.points for res in results_by_mmu[em]) for em in results_by_mmu}

        # How often was each rule_id encountered?
        evaluation.rule_count = {
            rule: len(results) for rule, results in results_by_rule.items()}

        # How often was which rule flagged with which category?
        evaluation.categories_by_rule = {
            rule_id: {
                cat: len(list(res)) for cat, res in groupby(rule_res, key=lambda r: r.result_category)
            } for rule_id, rule_res in results_by_rule.items()}

        return evaluation

    @staticmethod
    def append_statistics_to_all(evaluations: List[AutoEval]) -> List[AutoEval]:
        """Perform a number of statistic surveys on a list of ``Evaluations``.
        The constraint_results of these surveys are appended to the individual ``Evaluations``.
        """

        result_evaluations: List[AutoEval] = []

        for evaluation in evaluations:
            result_evaluations.append(StatisticsService.append_statistic(evaluation))

        return result_evaluations
