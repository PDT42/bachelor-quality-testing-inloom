"""
:Author: Paul Erlenwein
:Since: 2020/12/30

This is the module for the ``MetaEvalManager``.
"""

from collections import defaultdict
from statistics import mean
from typing import Dict, List, Mapping, Set, Tuple

from data_types.evaluation import AutoEval, Evaluation, ManEval
from data_types.expert_solution import ExpertSolution
from data_types.result import Result
from data_types.test_data_set import TestDataSet
from managers.evaluation_manager import EvalManager
from managers.exercise_manager import ExerciseManager
from managers.testdata_manager import TDManager


class MetaEvalManager:
    """This is the ``MetaEvalManager``."""

    # Create _stats
    # ____________

    def _collect_information(self, evaluation: Evaluation) -> Mapping:
        """Collect information about an evaluation."""

        stats: Dict[str, Mapping] = {}

        # Run all listed functions on the list of results

        for _func in [
            self._collect_points_per_element_type,
            self._collect_points_per_result_category
        ]:
            key, value = _func(evaluation.results)
            stats[key] = value

        return stats

    # Collection functions
    # ____________________

    @staticmethod
    def _collect_points_per_element_type(results: List[Result]) -> Tuple[str, Mapping]:
        """Sum up the points awarded for a certain element type."""

        point_map: Dict[str, float] = defaultdict(float)

        for result in results:
            point_map[result.expert_element_type] += result.points

        return 'points-per-expert-element-type', point_map

    @staticmethod
    def _collect_points_per_result_category(results: List[Result]) -> Tuple[str, Mapping]:

        point_map: Dict[str, float] = defaultdict(float)

        for result in results:
            point_map[result.result_category] += result.points

        return 'points-per-result-category', point_map

    # Calculations based on _stats
    # ___________________________

    @staticmethod
    def _calculate_dict_average(stats: Mapping[str, Mapping[str, Mapping]]):
        """Calculate the average for every key in a dict and
        reconstruct a dictionary with the same structure."""

        eval_stat_keys: Set[str] = set()

        for stat in stats.values():
            eval_stat_keys.update(set(stat.keys()))

        # For each key in eval_stat_keys
        # calculate the average of the values of
        # that key in the mappings in stats

        collected_stats: Mapping = defaultdict(lambda: defaultdict(list))

        for stat in stats.values():
            for eval_key in eval_stat_keys:
                collection: Mapping[str, float] = stat \
                    .get(eval_key, defaultdict(lambda: defaultdict(float)))

                for col_key, col_value in collection.items():
                    collected_stats[eval_key][col_key].append(col_value)

        average_stats: Dict[str, Mapping] = {
            key: {k: mean(v) for k, v in value.items()}
            for key, value in collected_stats.items()
        }
        return average_stats

    # Public functions
    # ________________

    def get_tds_meta_eval(self, test_data_set_id: str) -> Mapping:
        """Get meta eval for a test data set."""

        # Creating a dict to store the results in
        tds_meta_eval: Dict = {}

        # Get all evaluations for this tds from the database
        auto_evals: List[Evaluation] = EvalManager() \
            .get_all_of(test_data_set_id, AutoEval)
        man_evals: List[Evaluation] = EvalManager() \
            .get_all_of(test_data_set_id, ManEval)

        # Can only go on if at least one man and
        # auto eval were recorded in the database
        if len(auto_evals) and len(man_evals):

            # Collect the stats for the Evaluations
            # {.., evalId -> {stat: {..}, ..}, ..}
            auto_eval_stats: Mapping[str, Mapping] = {
                auto_eval.evaluation_id: self._collect_information(auto_eval)
                for auto_eval in auto_evals
            }
            tds_meta_eval['auto-eval-stats'] = auto_eval_stats

            man_eval_stats: Mapping[str, Mapping] = {
                man_eval.evaluation_id: self._collect_information(man_eval)
                for man_eval in man_evals
            }
            tds_meta_eval['man-eval-stats'] = man_eval_stats

            # Get the latest auto eval from the available ones
            auto_evals: List[Evaluation] = sorted(
                auto_evals, key=lambda e: e.created_time)

            latest_auto_eval: Evaluation = auto_evals[-1]

            # Get the ExpertSolution employed
            expert_solution: ExpertSolution = ExerciseManager() \
                .get_one_expert_solution(
                latest_auto_eval.exercise_id,
                latest_auto_eval.expert_solution_id)

            # Calculate TDS Level Statistics
            grade_quotients: Dict[str, float] = {
                m_eval.evaluation_id: (latest_auto_eval.total_points / m_eval.total_points)
                for m_eval in man_evals
            }

            # Calculate average points
            avg_man_total_points: float = mean([e.total_points for e in man_evals])
            latest_auto_total_points: float = latest_auto_eval.total_points

            # Calculate average grade
            avg_man_grade: float = avg_man_total_points / expert_solution.maximum_points
            latest_auto_grade: float = latest_auto_total_points / expert_solution.maximum_points

            # Calculate grade quotients
            grade_quotients['average-man-eval'] = \
                latest_auto_total_points / avg_man_total_points

            # Getting stats on the latest auto eval
            latest_auto_eval_stats: Mapping = self \
                ._collect_information(latest_auto_eval)

            # Getting the average of all the
            # entries of the man eval stats
            avg_man_eval_stats: Mapping = self \
                ._calculate_dict_average(man_eval_stats)

            # Append calculated values
            tds_meta_eval['grade-quotients'] = grade_quotients
            tds_meta_eval['average-man-total-points'] = avg_man_total_points
            tds_meta_eval['average-man-grade'] = avg_man_grade
            tds_meta_eval['latest-auto-total-points'] = latest_auto_total_points
            tds_meta_eval['latest-auto-grade'] = latest_auto_grade
            tds_meta_eval['avg-man-eval-stats'] = avg_man_eval_stats
            tds_meta_eval['latest-auto-eval-stats'] = latest_auto_eval_stats

        return tds_meta_eval

    def get_all_tds_meta_evals(self):
        """Get all meta_evals to all tds."""

        test_data_sets: List[TestDataSet] = TDManager() \
            .get_all_test_data_sets()

        tds_meta_evals: Dict = {}
        for tds in test_data_sets:
            tds_meta_evals[tds.test_data_set_id] = \
                self.get_tds_meta_eval(tds.test_data_set_id)

        return tds_meta_evals
