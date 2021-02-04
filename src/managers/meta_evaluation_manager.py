"""
:Author: Paul Erlenwein
:Since: 2020/12/30

This is the module for the ``MetaEvalManager``.
"""

from collections import defaultdict
from functools import partial
from statistics import mean
from typing import Any, Dict, List, Mapping, MutableMapping, Set, Tuple

from data_types.evaluation import AutoEval, Evaluation, ManEval
from data_types.expert_solution import ExpertSolution
from data_types.result import Result
from data_types.test_data_set import TestDataSet
from managers.evaluation_manager import EvalManager
from managers.exercise_manager import ExerciseManager
from managers.testdata_manager import TDManager


class MetaEvalManager:
    """This is the ``MetaEvalManager``."""

    # CONSTANTS
    AVG_MAN_EVAL_KEY = 'avg-man-eval'
    LATEST_AUTO_EVAL_KEY = 'latest-auto-eval'

    # Data Collection on the Evaluation Level
    # _______________________________________

    def _collect_information(self, evaluation: Evaluation, expert_solution: ExpertSolution) -> Mapping:
        """Collect information about an evaluation."""

        stats: Dict[str, Any] = {}

        # Run all listed functions on the list of results

        for _func in [
            self._collect_points_per_element_type,
            self._collect_points_per_result_category,
            self._count_category_flags,
            partial(self._calculate_grade, expert_solution)
        ]:
            key, value = _func(evaluation)
            stats[key] = value

        # Add data for convenience
        stats['total-points'] = evaluation.total_points
        stats['created'] = evaluation.created_time
        stats['type'] = evaluation.evaluation_type

        return stats

    # Collection functions
    # ~~~~~~~~~~~~~~~~~~~~

    @staticmethod
    def _collect_points_per_element_type(evaluation: Evaluation) -> Tuple[str, Mapping]:
        """Sum up the points awarded for a certain element type."""

        point_map: Dict[str, float] = defaultdict(float)

        for result in evaluation.results:
            point_map[result.expert_element_type] += result.points

        return 'points-per-expert-element-type', point_map

    @staticmethod
    def _collect_points_per_result_category(evaluation: Evaluation) -> Tuple[str, Mapping]:

        point_map: Dict[str, float] = defaultdict(float)

        for result in evaluation.results:
            point_map[result.result_category] += result.points

        return 'points-per-result-category', point_map

    @staticmethod
    def _count_category_flags(evaluation: Evaluation) -> Tuple[str, Mapping]:
        """Count the number of times a particular category flag was assigned by an eval."""

        category_count: Dict[str, int] = defaultdict(lambda: int())

        for result in evaluation.results:

            category_count[result.result_category] += 1

        return 'category-count', category_count

    @staticmethod
    def _calculate_grade(expert_solution: ExpertSolution, evaluation: Evaluation):

        return 'grade', (evaluation.total_points * 100) / expert_solution.maximum_points

    # Data Collection on the TDS Level
    # ________________________________

    def get_tds_meta_eval(self, test_data_set_id: str) -> Mapping:
        """Get meta eval for a test data set."""

        # Creating a dict to store the results in
        tds_meta_eval: Dict = {}

        # Get all evaluations for this tds from the database
        auto_evals: List[AutoEval] = EvalManager() \
            .get_all_of(test_data_set_id, AutoEval)
        man_evals: List[ManEval] = EvalManager() \
            .get_all_of(test_data_set_id, ManEval)

        # Can only go on if at least one man and
        # auto eval were recorded in the database
        if len(auto_evals) and len(man_evals):
            # Get the ExpertSolution employed
            expert_solution: ExpertSolution = ExerciseManager() \
                .get_one_expert_solution(
                auto_evals[0].exercise_id,
                auto_evals[0].expert_solution_id)

            # Collect the stats for the Evaluations
            # {.., evalId -> {stat: {..}, ..}, ..}

            tds_meta_eval['eval-stats'] = {}

            # Collect stats for AutoEvals
            auto_eval_stats: Mapping[str, MutableMapping] = {
                auto_eval.evaluation_id: self._collect_information(auto_eval, expert_solution)
                for auto_eval in auto_evals
            }
            tds_meta_eval['eval-stats'].update(auto_eval_stats)

            # Collect stats for ManEvals
            man_eval_stats: Mapping[str, MutableMapping] = {
                man_eval.evaluation_id: self._collect_information(man_eval, expert_solution)
                for man_eval in man_evals
            }
            tds_meta_eval['eval-stats'].update(man_eval_stats)

            # Get the latest AutoEval from the available ones
            # Sort the Evals by time inc. and get the last item
            auto_evals: List[AutoEval] = sorted(
                auto_evals, key=lambda e: e.created_time)
            latest_auto_eval: Evaluation = auto_evals[-1]

            # Calculate average points
            avg_man_total_points: float = mean([e.total_points for e in man_evals])
            latest_auto_total_points: float = latest_auto_eval.total_points

            # Adding stats on the latest auto eval
            latest_auto_eval_stats: MutableMapping = auto_eval_stats.get(latest_auto_eval.evaluation_id)
            latest_auto_eval_stats['total-points'] = latest_auto_total_points
            latest_auto_eval_stats['grade'] = (latest_auto_total_points * 100) / expert_solution.maximum_points
            tds_meta_eval['eval-stats']['latest-auto-eval'] = latest_auto_eval_stats

            # Adding stats on an average man eval
            avg_man_eval_stats: MutableMapping = self \
                ._calculate_dict_average(man_eval_stats)
            avg_man_eval_stats['total-points'] = avg_man_total_points
            avg_man_eval_stats['grade'] = (avg_man_total_points * 100) / expert_solution.maximum_points
            tds_meta_eval['eval-stats'][self.AVG_MAN_EVAL_KEY] = avg_man_eval_stats

            # Calculate TDS Level Statistics
            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

            # Calculate Comparison Stats
            tds_meta_eval['comparison-stats'] = self.calculate_comparison_stats(
                auto_evals, man_evals, avg_man_total_points, latest_auto_total_points, expert_solution)

            # Append id attributes
            tds_meta_eval['student-id'] = latest_auto_eval.student_id
            tds_meta_eval['expert-solution-id'] = latest_auto_eval.expert_solution_id
            tds_meta_eval['exercise-id'] = latest_auto_eval.exercise_id

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

    # TDS Level Calculations
    # ______________________

    def calculate_comparison_stats(
            self, auto_evals: List[AutoEval], man_evals: List[ManEval],
            avg_man_total_points: float, latest_auto_total_points: float,
            expert_solution: ExpertSolution
    ) -> Mapping[str, Mapping]:
        """Calculate the grade quotient of each combination
        of evaluations one might wish to compare."""

        # Dictionary to collect calculated values in
        comparison_stats: Dict[str, Dict[str, Any]] = defaultdict(lambda: dict())

        # Check each combination of ...
        for auto_eval in auto_evals:
            for man_eval in man_evals:
                # Create a unique key for the comparison
                # by combining the key of the evaluations
                comparison_key: str = \
                    auto_eval.evaluation_id + man_eval.evaluation_id

                # Calculate grade quotient
                comparison_stats['grade-quotients'][comparison_key] = \
                    auto_eval.total_points / man_eval.total_points

                comparison_stats['grade-quotients-pct'][comparison_key] = \
                    (auto_eval.total_points / man_eval.total_points) * 100

                # Calculate point differences
                comparison_stats['point-diffs'][comparison_key] = \
                    auto_eval.total_points - man_eval.total_points

                # Get category combinations
                comparison_stats['category-combinations'][comparison_key] = \
                    self._collect_category_matches(auto_eval, man_eval)

                # Count category Matches/Mismatches
                comparison_stats['category-matches'][comparison_key] = \
                    self._count_category_matches(comparison_stats['category-combinations'][comparison_key])

        # Append comparison Avg. vs Latest
        comparison_stats['grade-quotients'][self.LATEST_AUTO_EVAL_KEY + self.AVG_MAN_EVAL_KEY] = \
            latest_auto_total_points / avg_man_total_points

        comparison_stats['grade-quotients-pct'][self.LATEST_AUTO_EVAL_KEY + self.AVG_MAN_EVAL_KEY] = \
            (latest_auto_total_points / avg_man_total_points) * 100

        comparison_stats['point-diffs'][self.LATEST_AUTO_EVAL_KEY + self.AVG_MAN_EVAL_KEY] = \
            latest_auto_total_points - avg_man_total_points

        # Calculate pct differences
        percentage_differences: Dict[str, float] = {
            comparison_key: (pt_diff * 100) / expert_solution.maximum_points
            for comparison_key, pt_diff in comparison_stats['point-diffs'].items()
        }
        comparison_stats['point-pct-diffs'] = percentage_differences

        return comparison_stats

    @staticmethod
    def _collect_category_matches(auto_eval: AutoEval, man_eval: ManEval):
        """Count the category pairings found in the compared evaluations."""

        element_category_flags: Dict[str, Dict[str, str]] = defaultdict(lambda: dict())

        def element(_result: Result):
            return f"{_result.expert_element_type} - {_result.expert_element_label}"

        for result in auto_eval.results:
            element_category_flags[element(result)]['auto'] = result.result_category

        for result in man_eval.results:
            element_category_flags[element(result)]['man'] = result.result_category

        return element_category_flags

    @staticmethod
    def _count_category_matches(element_category_flags: Dict[str, Dict[str, str]]):
        """Count the number of times the categories matched."""

        category_matches: Dict[str, float] = defaultdict(lambda: int())

        for element, flags in element_category_flags.items():
            if flags.get('auto') != flags.get('man'):
                category_matches['mismatch'] += 1
            else:
                category_matches['match'] += 1

        category_matches['total'] = category_matches['match'] + category_matches['mismatch']
        category_matches['pct-matched'] = (category_matches['match'] * 100) / category_matches['total']

        return category_matches

    @staticmethod
    def _calculate_dict_average(stats: Mapping[str, Mapping[str, Mapping]]):
        """Calculate the average for every key in a dict and
        reconstruct a dictionary with the same structure."""

        # TODO: Use a more general approach

        eval_stat_keys: Set[str] = set()

        for stat in stats.values():
            for key, value in stat.items():
                if isinstance(value, Mapping):
                    eval_stat_keys.add(key)

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

    # Data Collection on the Exercise Level
    # _____________________________________

    def get_exercise_meta_eval(self, exercise_id: str) -> Mapping:
        """Get a meta_eval on the exercise level."""

        # TODO: This feels ULTRA clumsy. Calculating the tds meta evals
        # TODO: several times should not be necessary. Update this!

        # Get the test data sets of this exercise
        test_data_sets: List[TestDataSet] = TDManager() \
            .get_exercise_tds(exercise_id)

        # Collect values from all tds of the exercise
        _exc_meta_eval_values: Dict[str, List] = defaultdict(lambda: list())
        for tds in test_data_sets:  # iterate over all tds of exc
            tds_meta_eval: Mapping = self.get_tds_meta_eval(tds.test_data_set_id)

            # Collect TDS Level KPI of all TDS of an exercise

            # Collect avg-man-eval grades
            if tds_avg_man_grade := tds_meta_eval.get('eval-stats', {}).get(self.AVG_MAN_EVAL_KEY, {}).get('grade'):
                _exc_meta_eval_values['avg-grades'].append(tds_avg_man_grade)

            comparison_stats: Mapping[str, Mapping] = tds_meta_eval.get('comparison-stats', {})

            # Collect avg-man-eval grade quotients
            if tds_avg_grade_quotient := comparison_stats.get('grade-quotients').get(
                    self.LATEST_AUTO_EVAL_KEY + self.AVG_MAN_EVAL_KEY):
                _exc_meta_eval_values['avg-grade-quotient'].append(abs(tds_avg_grade_quotient))

            # Collect avg-man-eval pct diff
            if tds_avg_man_pct_diff := comparison_stats.get('point-pct-diffs', {}).get(
                    self.LATEST_AUTO_EVAL_KEY + self.AVG_MAN_EVAL_KEY):
                _exc_meta_eval_values['avg-percentage-differences'].append(abs(tds_avg_man_pct_diff))

            # Collect avg-man-eval pt diff
            if tds_avg_man_pt_diff := comparison_stats.get('point-diffs', {}).get(
                    self.LATEST_AUTO_EVAL_KEY + self.AVG_MAN_EVAL_KEY):
                _exc_meta_eval_values['avg-point-differences'].append(abs(tds_avg_man_pt_diff))

        # Calculate the mean of each collection
        exc_meta_eval = {
            key: mean(clct) for key, clct in _exc_meta_eval_values.items()
        }

        return exc_meta_eval
