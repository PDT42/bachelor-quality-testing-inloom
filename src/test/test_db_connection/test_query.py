"""
:Author: Paul Erlenwein
:Since: 2020/11/20

These are tests for the db_connection.query module.
"""

import unittest

from data_types.testdataset import TestDataSet
from db_connection.db_column import DbColumn
from db_connection.db_data_types import VARCHAR
from db_connection.db_table import DbTable
from db_connection.query import CREATEQuery, Query, SELECTQuery


class TestQuery(unittest.TestCase):
    """TestCase for the ``Query``."""

    # Constants
    BASE_XML_PATH: str = '../../res/example-data/student-solutions/Aufgabe_1/Ergebnisse'
    EXPERT_MODEL_XML: str = f'{BASE_XML_PATH}/OUTPUT_Expert_OOA_Class_SoSe2018.xml'
    STUDENT_MODEL_XML: str = f'{BASE_XML_PATH}/OUTPUT_ExSS2018_student1.xml'

    def setUp(self) -> None:
        """Setup test requirements."""

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

    def test_create_query(self):
        """Test the CREATEQuery"""

        create_query: Query = CREATEQuery(self.test_test_data_set_table)

        optimal_test_query: str = f'CREATE TABLE IF NOT EXISTS {self.test_test_data_set_table.table_name} ('
        optimal_test_query += f'expert_model_id VARCHAR PRIMARY KEY, '
        optimal_test_query += f'student_model_id VARCHAR NOT NULL, '
        optimal_test_query += f'meta_model_type VARCHAR, '
        optimal_test_query += f'mcs_identifier VARCHAR, '
        optimal_test_query += f'mcs_version VARCHAR DEFAULT \'1.0.0\', '
        optimal_test_query += f'auto_eval_id VARCHAR, '
        optimal_test_query += f'man_eval_id VARCHAR)'

        self.assertEqual(create_query.resolve(), optimal_test_query)

    def test_create_query_from_dataclass(self):
        """Test CREATEQuery with table from DbTable's ``.from_dataclass``."""

        create_query: Query = CREATEQuery(DbTable.from_dataclass(
            data_class=TestDataSet,
            ignore_fields=['auto_eval', 'man_eval']
        ))

        optimal_test_query: str = f'CREATE TABLE IF NOT EXISTS {TestDataSet.__name__.lower()} ('
        optimal_test_query += f'expert_model_id VARCHAR, '
        optimal_test_query += f'student_model_id VARCHAR, '
        optimal_test_query += f'meta_model_type VARCHAR, '
        optimal_test_query += f'mcs_identifier VARCHAR, '
        optimal_test_query += f'mcs_version VARCHAR, '
        optimal_test_query += f'auto_eval_id VARCHAR, '
        optimal_test_query += f'man_eval_id VARCHAR)'

        self.assertEqual(create_query.resolve(), optimal_test_query)

    def test_select_query(self):
        """Test the SELECTQuery"""

        select_query: Query = SELECTQuery(self.test_test_data_set_table)

        optimal_test_query: str = f'SELECT expert_model_id, student_model_id, '
        optimal_test_query += f'meta_model_type, mcs_identifier, mcs_version, '
        optimal_test_query += f'auto_eval_id, man_eval_id '
        optimal_test_query += f'FROM {self.test_test_data_set_table.table_name}'

        self.assertEqual(select_query.resolve(), optimal_test_query)
