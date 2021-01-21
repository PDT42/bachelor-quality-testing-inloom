"""
:Author: Paul Erlenwein
:Since: 2020/11/20

This is the module for the ``TDManager``.
"""

from typing import Any, List, Mapping

from data_types.evaluation import AutoEval, Evaluation, ManEval
from data_types.test_data_set import TestDataSet
from db_connection.db_column import DbColumn
from db_connection.db_connection import DbConnection, SqliteConnection
from db_connection.db_data_types import INTEGER, VARCHAR
from db_connection.db_table import DbTable
from db_connection.filter import Filter, FilterOperation
from db_connection.query import CREATEQuery, DELETEQuery, INSERTQuery, Query, SELECTQuery, UPDATEQuery
from managers.evaluation_manager import EvalManager


class TDManager:
    """This is the ``TDManager``."""

    # Constants
    EXERCISE_ID_COLUMN: DbColumn = DbColumn('exercise_id', VARCHAR())
    STUDENT_ID_COLUMN: DbColumn = DbColumn('student_id', VARCHAR())
    EXPERT_SOL_ID_COLUMN: DbColumn = DbColumn('expert_solution_id', VARCHAR())
    TEST_DATA_SET_ID_COLUMN: DbColumn = DbColumn('test_data_set_id', VARCHAR(), primary_key=True)

    # Variables
    db_connection: DbConnection
    test_data_set_table: DbTable
    test_data_set_table_columns: List[DbColumn]

    eval_manager: EvalManager

    def __init__(self):
        """Create a new ``TDManager``."""

        self.db_connection = SqliteConnection.get()
        self.eval_manager = EvalManager()

        self.test_data_set_table_columns = [
            self.TEST_DATA_SET_ID_COLUMN,
            DbColumn('exercise_id', VARCHAR(), not_null=True),
            DbColumn('expert_solution_id', VARCHAR(), not_null=True),
            DbColumn('student_id', VARCHAR(), not_null=True),
            DbColumn('created_time', INTEGER(), not_null=True)
        ]
        self.test_data_set_table = DbTable(
            'test_data_sets', columns=self.test_data_set_table_columns)

    def get_student_tds(self, student_id: str, exercise_id: str, expert_solution_id: str):
        """Get the tds for this student- and exercise_id."""

        equals: FilterOperation = FilterOperation.EQUALS

        query: Query = SELECTQuery(self.test_data_set_table) \
            .where(Filter(self.STUDENT_ID_COLUMN, equals, student_id)) \
            .where(Filter(self.EXERCISE_ID_COLUMN, equals, exercise_id)) \
            .where(Filter(self.EXPERT_SOL_ID_COLUMN, equals, expert_solution_id))
        db_results: List[Mapping[str, Any]] = self.db_connection.execute(query)

        if not db_results:
            return None
        elif isinstance(db_results, list) and len(db_results) > 1:
            raise ValueError("CONSTRAINT ERROR: This TestDataSet was duplicated!")

        return TestDataSet(**db_results[0])

    def get_one(self, test_data_set_id: str):
        """Get one with the supplied id."""

        equals: FilterOperation = FilterOperation.EQUALS

        query: Query = SELECTQuery(self.test_data_set_table) \
            .where(Filter(self.TEST_DATA_SET_ID_COLUMN, equals, test_data_set_id))
        db_results: List[Mapping[str, Any]] = self.db_connection.execute(query)

        if not db_results:
            return None
        elif isinstance(db_results, list) and len(db_results) > 1:
            raise ValueError("CONSTRAINT ERROR: This TestDataSet was duplicated!")

        return TestDataSet(**db_results[0])

    def get_one_that_equals(self, test_data_set: TestDataSet):
        """Get a ``TestDataSet`` that would __equals__ ``test_data_set``."""

        equals: FilterOperation = FilterOperation.EQUALS

        # Getting all TestDataSets that equal the one supplied
        query: Query = SELECTQuery(self.test_data_set_table) \
            .where(Filter(self.EXERCISE_ID_COLUMN, equals, test_data_set.exercise_id)) \
            .where(Filter(self.STUDENT_ID_COLUMN, equals, test_data_set.student_id)) \
            .where(Filter(self.EXPERT_SOL_ID_COLUMN, equals, test_data_set.expert_solution_id))
        db_results: List[Mapping[str, Any]] = self.db_connection.execute(query)

        if not db_results:
            return None
        elif isinstance(db_results, list) and len(db_results) > 1:
            raise ValueError("CONSTRAINT ERROR: This TestDataSet was duplicated!")

        return TestDataSet(**db_results[0])

    def get_all_test_data_sets(self) -> List[TestDataSet]:
        """Get all TestDataSets to which the filters apply."""

        query: Query = SELECTQuery(self.test_data_set_table)
        results: List[Mapping[str, Any]] = self.db_connection.execute(query)

        test_data_sets: List[TestDataSet] = [TestDataSet(**item) for item in results]

        for tds in test_data_sets:
            tds.auto_evals = self.eval_manager.get_all_of(tds.test_data_set_id, required_type=AutoEval)
            tds.man_evals = self.eval_manager.get_all_of(tds.test_data_set_id, required_type=ManEval)

        return test_data_sets

    def insert_test_data_sets(self, test_data_sets: List[TestDataSet]):
        """Insert a list of ``TestDataSets`` into the database."""

        query: Query = INSERTQuery(self.test_data_set_table, test_data_sets)
        self.db_connection.execute(query)

    def update_test_data_set(self, test_data_set: TestDataSet):
        """Update a TDS in the database."""

        equals: FilterOperation = FilterOperation.EQUALS

        # Check if the test_data_set exists
        query: Query = UPDATEQuery(self.test_data_set_table, test_data_set) \
            .where(Filter(self.EXERCISE_ID_COLUMN, equals, test_data_set.exercise_id)) \
            .where(Filter(self.STUDENT_ID_COLUMN, equals, test_data_set.student_id)) \
            .where(Filter(self.EXPERT_SOL_ID_COLUMN, equals, test_data_set.expert_solution_id))
        self.db_connection.execute(query)

    def update_insert_test_data_set(self, test_data_set: TestDataSet):
        """Update a TestDataSet in the database, if it does not exist, add it."""

        db_test_data_set: TestDataSet = self.get_one_that_equals(test_data_set)

        # The TDS already exists -> update it
        if db_test_data_set is not None:
            self.update_test_data_set(test_data_set)
        else:
            self.insert_test_data_sets([test_data_set])

    def delete_test_data_set(self, test_data_set_id: str):
        """Delete a TestDataSet from the database."""

        db_test_data_set: TestDataSet = self.get_one(test_data_set_id)

        if not db_test_data_set:
            return

        query: Query = DELETEQuery(self.test_data_set_table)
        self.db_connection.execute(query)

        for evaluation in db_test_data_set.auto_evals + db_test_data_set.man_evals:
            self.eval_manager.delete_evaluation(evaluation.evaluation_id)

    def register_evaluation(self, evaluation: Evaluation) -> None:
        """Register an AutoEval in the database."""

        # Creating a new TestDataSet
        test_data_set: TestDataSet = TestDataSet(
            exercise_id=evaluation.exercise_id,
            expert_solution_id=evaluation.expert_solution_id,
            student_id=evaluation.student_id)

        # Checking if it already exists in the database
        db_test_data_set: TestDataSet = self.get_one_that_equals(test_data_set)

        if db_test_data_set is not None and isinstance(db_test_data_set, TestDataSet):
            test_data_set = db_test_data_set

        # Inserting the evaluation into the database
        self.eval_manager.insert_evaluation(evaluation)

        # Checking what kind of evaluation we are registering
        if isinstance(evaluation, AutoEval):
            test_data_set.auto_eval_id = evaluation.evaluation_id
            test_data_set.auto_eval = evaluation
        elif isinstance(evaluation, ManEval):
            test_data_set.man_eval_id = evaluation.evaluation_id
            test_data_set.man_eval = evaluation
        else:
            raise SystemError("ILLEGAL STATE: Evaluation must be either AutoEval or ManEval!")

        # Inserting/Updating the test_data_set in the database
        self.update_insert_test_data_set(test_data_set)

    def init_database_table(self):
        """Initialize the table required for storing
        ``TestDataSets`` in the database.
        """

        self.db_connection.execute(CREATEQuery(self.test_data_set_table))
        self.eval_manager.init_database_tables()
