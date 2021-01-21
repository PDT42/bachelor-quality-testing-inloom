"""
:Author: Paul Erlenwein
:Since: 2020/11/20

This is the module for the ``ResultManager``.
"""

from typing import Any, List, Mapping

from data_types.result import Result
from db_connection.db_column import DbColumn
from db_connection.db_connection import DbConnection, SqliteConnection
from db_connection.db_data_types import FLOAT, VARCHAR
from db_connection.db_table import DbTable
from db_connection.filter import Filter, FilterOperation
from db_connection.query import CREATEQuery, DELETEQuery, INSERTQuery, Query, SELECTQuery


class ResultManager:
    """This is the ``ResultManager``."""

    # Constants
    RESULT_ID_COLUMN: DbColumn = DbColumn(
        'result_id', VARCHAR(), primary_key=True)
    EVALUATION_ID_COLUMN: DbColumn = DbColumn(
        'evaluation_id', VARCHAR(), not_null=True)

    # Variables
    db_connection: DbConnection
    results_table: DbTable
    results_table_columns: List[DbColumn]

    def __init__(self):
        """Create a new ``ResultManager``."""

        self.db_connection = SqliteConnection.get()

        self.results_table_columns = [
            DbColumn('expert_element_label', VARCHAR(), not_null=True),
            DbColumn('expert_element_name', VARCHAR(), not_null=True),
            DbColumn('expert_element_type', VARCHAR(), not_null=True),
            DbColumn('student_element_label', VARCHAR(), not_null=True),
            DbColumn('student_element_type', VARCHAR(), not_null=True),
            DbColumn('result_category', VARCHAR(), not_null=True),
            DbColumn('points', FLOAT(), not_null=True),
            DbColumn('feedback_message', VARCHAR()),
            DbColumn('result_type', VARCHAR(), not_null=True),
            DbColumn('graded_feature_id', VARCHAR(), not_null=True),
            DbColumn('created_time', VARCHAR(), not_null=True),
            self.EVALUATION_ID_COLUMN,
            self.RESULT_ID_COLUMN
        ]

        self.results_table = DbTable(
            table_name='results',
            columns=self.results_table_columns)

    def get_one(self, result_id: str):
        """Get one ``CResult`` by id."""

        query: Query = SELECTQuery(self.results_table) \
            .where(Filter(self.RESULT_ID_COLUMN, FilterOperation.EQUALS, result_id))
        results: List[Mapping[str, Any]] = self.db_connection.execute(query)

        if not results:
            return None
        elif isinstance(results, list) and len(results) > 1:
            raise ValueError("This CResult was duplicated!")
        else:
            return Result(**results[0])

    def get_all_for(self, evaluation_id: str):
        """Get all ``Results`` that belong to ``evaluation_id``."""

        query: Query = SELECTQuery(self.results_table) \
            .where(Filter(self.EVALUATION_ID_COLUMN, FilterOperation.EQUALS, evaluation_id))
        results: List[Mapping[str, Any]] = self.db_connection.execute(query)

        return [Result(**item) for item in results]

    def insert_results(self, results: List[Result]):
        """Store a ``Result`` in the database."""

        if any(r.evaluation_id is None for r in results):
            raise ValueError('AutoEval ID of CResult must not be null!')

        query: Query = INSERTQuery(self.results_table, results)
        self.db_connection.execute(query)

    def delete_eval_results(self, evaluation_id: str):
        """Delete all results with the supplied evaluation id."""

        equals: FilterOperation = FilterOperation.EQUALS

        query: Query = DELETEQuery(self.results_table) \
            .where(Filter(self.EVALUATION_ID_COLUMN, equals, evaluation_id))
        self.db_connection.execute(query)

    def init_database_table(self):
        """Initialize the table required for storing
        ``TestDataSets`` in the database.
        """

        self.db_connection.execute(CREATEQuery(self.results_table))
