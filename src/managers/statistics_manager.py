"""
:Author: Paul Erlenwein
:Since: 2020/12/30

This is the module for the ``StatisticsManager``.
"""

from collections import defaultdict
from statistics import mean
from typing import Dict, List, Mapping, Set, Tuple

from data_types.evaluation import AutoEval, Evaluation, ManEval
from data_types.result import Result
from data_types.test_data_set import TestDataSet
from managers.evaluation_manager import EvalManager
from managers.testdata_manager import TDManager


class StatisticsManager:
    """This is the ``StatisticsManager``."""

    # Create stats
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

    # Calculations based on stats
    # ___________________________

    @staticmethod
    def _calculate_dict_average(statistics: Mapping[str, Mapping[str, Mapping]]):
        """Calculate the average for every key in a dict and
        reconstruct a dictionary with the same structure."""

        eval_stat_keys: Set[str] = set()

        for stats in statistics.values():
            eval_stat_keys.update(set(stats.keys()))

        # For each key in eval_stat_keys
        # calculate the average of the values of
        # that key in the mappings in statistics

        collected_stats: Mapping = defaultdict(lambda: defaultdict(list))

        for stats in statistics.values():
            for eval_key in eval_stat_keys:
                collection: Mapping[str, float] = stats \
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

    def get_tds_statistics(self, test_data_set_id: str):
        """Get statistics for a test data set."""

        # Get all evaluations for this tds from the database
        auto_evals: List[Evaluation] = EvalManager() \
            .get_all_of(test_data_set_id, AutoEval)
        man_evals: List[Evaluation] = EvalManager() \
            .get_all_of(test_data_set_id, ManEval)

        latest_auto_eval: Evaluation = sorted(
            auto_evals, key=lambda e: e.created_time)[-1]

        # Collect the statistics for the Evaluations
        # {evalId -> {stats, ..}, ..}
        auto_eval_stats: Mapping[str, Mapping] = {
            auto_eval.evaluation_id: self._collect_information(auto_eval)
            for auto_eval in auto_evals
        }
        man_eval_stats: Mapping[str, Mapping] = {
            man_eval.evaluation_id: self._collect_information(man_eval)
            for man_eval in man_evals
        }

        # Calculate TDS Level Statistics
        grade_quotients: Dict[str, float] = {
            e.evaluation_id: (latest_auto_eval.total_points / e.total_points)
            for e in man_evals
        }

        # Calculate average grade
        average_man_grade: float = mean([e.total_points for e in man_evals])
        grade_quotients['average-man-eval'] = \
            latest_auto_eval.total_points / average_man_grade

        # Getting stats on the latest auto eval
        latest_auto_eval_stats: Mapping = self \
            ._collect_information(latest_auto_eval)

        # Getting the average of all the
        # entries of the man eval stats
        avg_man_eval_stats: Mapping = self \
            ._calculate_dict_average(man_eval_stats)

        # Creating a dict to store the results in
        tds_statistics: Dict = {
            'auto-eval-stats': auto_eval_stats,
            'man-eval-stats': man_eval_stats,
            'grade-quotients': grade_quotients,
            'average-man-grade': average_man_grade,
            'avg-man-eval-stats': avg_man_eval_stats,
            'latest-auto-eval-stats': latest_auto_eval_stats
        }

        return tds_statistics

    def get_all_tds_statistics(self):
        """Get all statistics to all tds."""

        test_data_sets: List[TestDataSet] = TDManager() \
            .get_all_test_data_sets()

        tds_statistics: Dict = {}
        for tds in test_data_sets:
            tds_statistics[tds.test_data_set_id] = \
                self.get_tds_statistics(tds.test_data_set_id)
