"""
:Author: Paul Erlenwein
:Since: 2020/11/20

This is the module for the ``EvaluationManager``.
"""
from typing import Any, List, Mapping

from data_types.evaluation import Evaluation
from db_connection.db_column import DbColumn
from db_connection.db_connection import DbConnection, SqliteConnection
from db_connection.db_data_types import FLOAT, VARCHAR
from db_connection.db_table import DbTable
from db_connection.filter import Filter, FilterOperation
from db_connection.query import CREATEQuery, INSERTQuery, Query, SELECTQuery
from managers.results_manager import ResultsManager


class EvaluationManager:
    """This is the ``EvaluationManager``."""

    # Make this a Singleton
    # ~~~~~~~~~~~~~~~~~~~~~
    _instance: 'EvaluationManager' = None

    @staticmethod
    def get():
        """Get the _instance of this singleton."""
        if not EvaluationManager._instance:
            EvaluationManager._instance = EvaluationManager()
        return EvaluationManager._instance

    # ~~~~~~~~~~~~~~~~~~~~~

    # Constants
    EVALUATION_TABLE_NAME: str = 'evaluations'
    TYPE_COLUMN: DbColumn = DbColumn('type', VARCHAR())
    EVALUATOR_COLUMN: DbColumn = DbColumn('evaluator', VARCHAR())
    EXPERT_MODEL_ID_COLUMN: DbColumn = DbColumn('expert_model_id', VARCHAR())
    STUDENT_MODEL_ID_COLUMN: DbColumn = DbColumn('student_model_id', VARCHAR())
    MAX_POINTS_COLUMN: DbColumn = DbColumn('max_points', FLOAT())

    # Variables
    db_connection: DbConnection
    evaluations_table: DbTable
    evaluations_table_columns: List[DbColumn]
    results_manager: ResultsManager

    def __init__(self):
        """Create a new ``EvaluationManager``."""

        self.db_connection = SqliteConnection.get()
        self._init_database_table()

        self.results_manager = ResultsManager.get()

    def insert_evaluations(self, evaluations: List[Evaluation]):
        """Insert a list of ``Evaluations`` into the database."""

        query: Query = INSERTQuery(self.evaluations_table, evaluations)
        self.db_connection.execute(query)

        for evaluation in evaluations:
            if len(evaluation.results) > 0:
                self.results_manager.insert_results(evaluation.results)

    def get_all_evaluations(self):
        """Get all ``Evaluations`` available  in the database."""

        raise NotImplementedError()

    def get_one_by_evaluation_id(self, evaluation_id: str):
        """Get an ``Evaluation`` by its ``evaluation_id``."""

        raise NotImplementedError()

    def get_one_that_equals(self, evaluation: Evaluation):
        """Get àn ``Evaluation`` that would __equals__ ``evaluation``."""

        equals: FilterOperation = FilterOperation.EQUALS
        query: Query = SELECTQuery(self.evaluations_table) \
            .where(Filter(self.TYPE_COLUMN, equals, evaluation.type)) \
            .where(Filter(self.EVALUATOR_COLUMN, equals, evaluation.evaluator)) \
            .where(Filter(self.EXPERT_MODEL_ID_COLUMN, equals, evaluation.expert_model_id)) \
            .where(Filter(self.STUDENT_MODEL_ID_COLUMN, equals, evaluation.student_model_id)) \
            .where(Filter(self.MAX_POINTS_COLUMN, equals, evaluation.max_points))
        results: List[Mapping[str, Any]] = self.db_connection.execute(query)

        if not results:
            return None
        elif isinstance(results, list) and len(results) > 1:
            raise ValueError("This Evaluation was duplicated!")
        else:
            return Evaluation(**results[0])

    def _init_database_table(self):
        """Initialize the table required for storing
        ``TestDataSets`` in the database.
        """

        self.evaluations_table_columns = [
            self.TYPE_COLUMN,
            self.EVALUATOR_COLUMN,
            self.STUDENT_MODEL_ID_COLUMN,
            self.EXPERT_MODEL_ID_COLUMN,
            DbColumn('total_points', FLOAT()),
            self.MAX_POINTS_COLUMN,
            DbColumn('evaluation_id', VARCHAR(), primary_key=True)
        ]
        self.evaluations_table = DbTable(
            self.EVALUATION_TABLE_NAME, columns=self.evaluations_table_columns)
        self.db_connection.execute(CREATEQuery(self.evaluations_table))
