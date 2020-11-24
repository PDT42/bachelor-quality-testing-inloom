"""
:Author: Paul Erlenwein
:Since: 2020/11/20

These are tests for the ``DbConnection``.
"""

import unittest

from db_connection.db_column import DbColumn
from db_connection.db_connection import DbConnection, SqliteConnection
from db_connection.db_data_types import VARCHAR
from db_connection.db_table import DbTable
from db_connection.query import CREATEQuery, Query
from test.test_db_connection import TEST_DB_PATH


class TestDbConnection(unittest.TestCase):
    """TTestCase for the ``DbConnection``."""

    def setUp(self) -> None:
        """Setup test requirements."""

        self.db_connection: DbConnection = SqliteConnection(TEST_DB_PATH)

        self.test_test_data_set_table: DbTable = DbTable(
            'inloom_quality_test_data_sets',
            columns=[
                DbColumn('expert_model_id', VARCHAR(), primary_key=True),
                DbColumn('student_model_id', VARCHAR(), not_null=True),
                DbColumn('meta_model_type', VARCHAR()),
                DbColumn('mcs_identifier', VARCHAR()),
                DbColumn('mcs_version', VARCHAR(), default='1.0.0'),
                DbColumn('auto_eval_id', VARCHAR()),
                DbColumn('man_eval_id', VARCHAR())
            ])

        return

    def tearDown(self) -> None:
        """Clean up after tests."""

        return

    def test_execute_create_table(self):
        """Test execute create table query."""

        create_query: Query = CREATEQuery(self.test_test_data_set_table)
        self.db_connection.execute(create_query)

        print('The sphinx is the riddle!')
