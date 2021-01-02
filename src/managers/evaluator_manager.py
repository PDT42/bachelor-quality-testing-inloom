"""
:Author: Paul Erlenwein
:Since: 2020/12/23

This is the module for the ``EvaluatorManagaer``.
"""

from typing import Any, List, Mapping

from data_types.evaluator import Evaluator
from db_connection.db_column import DbColumn
from db_connection.db_connection import DbConnection, SqliteConnection
from db_connection.db_data_types import VARCHAR
from db_connection.db_table import DbTable
from db_connection.filter import Filter, FilterOperation
from db_connection.query import CREATEQuery, INSERTQuery, Query, SELECTQuery


class EvaluatorManager:
    """This is the ``EvaluatorManager``."""

    # Constants
    EVALUATOR_TABLE_NAME: str = 'evaluators'

    EVALUATOR_ID_COLUMN: DbColumn = DbColumn('evaluator_id', VARCHAR(), primary_key=True)

    # Variables
    db_connection: DbConnection
    evaluator_table: DbTable

    def __init__(self):
        """Create a new ``EvaluatorManager``."""

        self.db_connection = SqliteConnection.get()

        evaluator_table_columns: List[DbColumn] = [
            DbColumn('first_name', VARCHAR()),
            DbColumn('last_name', VARCHAR()),
            DbColumn('created_time', VARCHAR(), not_null=True),
            self.EVALUATOR_ID_COLUMN
        ]

        self.evaluator_table = DbTable(
            table_name=self.EVALUATOR_TABLE_NAME,
            columns=evaluator_table_columns)

    def insert_evaluator(self, evaluator: Evaluator):
        """Insert an ``Evaluator`` into the database."""

        query: Query = INSERTQuery(
            db_table=self.evaluator_table,
            values=[evaluator])
        self.db_connection.execute(query)

    def get_all_evaluators(self):
        """Get all evaluators registered in the database."""

        query: Query = SELECTQuery(db_table=self.evaluator_table)
        db_results: List[Mapping[str, Any]] = self.db_connection.execute(query)

        return [Evaluator(**item) for item in db_results]

    def get_one_evaluator(self, evaluator_id: str):
        """Get one evaluator from the database."""

        query: Query = SELECTQuery(db_table=self.evaluator_table) \
            .where(Filter(self.EVALUATOR_ID_COLUMN, FilterOperation.EQUALS, evaluator_id))
        db_results: List[Mapping[str, Any]] = self.db_connection.execute(query)

        if not db_results:
            return None

        return Evaluator(**db_results[0])

    def init_database_tables(self):
        """Initialize the table required for storing
        ``TestDataSets`` in the database.
        """

        # Create Table for the Evaluators
        self.db_connection.execute(CREATEQuery(self.evaluator_table))
