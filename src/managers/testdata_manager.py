"""
:Author: Paul Erlenwein
:Since: 2020/11/20

This is the module for the ``TDManager``.
"""
from typing import Any, List, Mapping

from data_types.evaluation import Evaluation
from data_types.testdataset import TestDataSet
from db_connection.db_column import DbColumn
from db_connection.db_connection import DbConnection, SqliteConnection
from db_connection.db_data_types import VARCHAR
from db_connection.db_table import DbTable
from db_connection.filter import Filter, FilterOperation
from db_connection.query import CREATEQuery, INSERTQuery, Query, SELECTQuery
from managers.evaluation_manager import EvaluationManager


class TDManager:
    """This is the ``TDManager`` singleton."""

    # Constants
    STUDENT_MODEL_COL: DbColumn = DbColumn('student_model_id', VARCHAR())

    # Make this a Singleton
    # ~~~~~~~~~~~~~~~~~~~~~
    _instance: 'TDManager' = None

    @staticmethod
    def get():
        """Get the _instance of this singleton."""
        if not TDManager._instance:
            TDManager._instance = TDManager()
        return TDManager._instance

    # ~~~~~~~~~~~~~~~~~~~~~

    # Variables
    db_connection: DbConnection
    test_data_set_table: DbTable
    test_data_set_table_columns: List[DbColumn]

    def __init__(self):
        """Create a new ``TDManager``."""

        self.db_connection = SqliteConnection.get()
        self._init_database_table()

        self.eval_manager = EvaluationManager.get()

    def get_all_test_data_sets(self):
        """Get all TestDataSets to which the filters apply."""

        query: Query = SELECTQuery(self.test_data_set_table)
        results: List[Mapping[str, Any]] = self.db_connection.execute(query)

        return [TestDataSet(**item) for item in results]

    def insert_test_data_sets(self, test_data_sets: List[TestDataSet]):
        """Insert a list of ``TestDataSets`` into the database."""

        query: Query = INSERTQuery(self.test_data_set_table, test_data_sets)
        self.db_connection.execute(query)

        for test_data_set in test_data_sets:
            evaluations: List[Evaluation] = []
            if test_data_set.auto_eval is not None:
                evaluations.append(test_data_set.auto_eval)
            if test_data_set.man_eval is not None:
                evaluations.append(test_data_set.man_eval)

            if len(evaluations) > 0:
                self.eval_manager.insert_evaluations(evaluations)

    def register_evaluation(self, evaluation: Evaluation):
        """Register an Evaluation in the database."""

        # Getting all test data sets from the
        # database where the 'student_model_id'
        # equals that of the 'evaluation' supplied.

        student_model_filter: Filter = Filter(
            column=self.STUDENT_MODEL_COL,
            operation=FilterOperation.EQUALS,
            value=evaluation.student_model_id
        )
        query: Query = SELECTQuery(self.test_data_set_table) \
            .where(student_model_filter)
        results: List[Mapping[str, Any]] = self.db_connection.execute(query)
        test_data_sets: List[TestDataSet] = [TestDataSet(**item) for item in results]

        if len(results) < 1:
            # No test dataset using the SM_ID
            # 'evaluation' uses was found in
            # the database.

            # Check if there's just no test data set
            raise NotImplementedError()

    def _init_database_table(self):
        """Initialize the table required for storing
        ``TestDataSets`` in the database.
        """

        self.test_data_set_table_columns = [
            DbColumn('expert_model_id', VARCHAR()),
            self.STUDENT_MODEL_COL,
            DbColumn('meta_model_type', VARCHAR()),
            DbColumn('mcs_identifier', VARCHAR()),
            DbColumn('mcs_version', VARCHAR()),
            DbColumn('auto_eval_id', VARCHAR()),
            DbColumn('man_eval_id', VARCHAR())
            # TODO: Add unique id?
        ]
        self.test_data_set_table = DbTable(
            'inloom_quality_test_data_sets',
            columns=self.test_data_set_table_columns)
        self.db_connection.execute(CREATEQuery(self.test_data_set_table))
