"""
:Author: Paul Erlenwein
:Since: 2020/11/20

These are tests for the different types used by the DbConnection.
"""

import unittest
from typing import List

from data_types.testdataset import TestDataSet
from db_connection.db_column import DbColumn, get_columns_from_dataclass
from db_connection.db_data_types import VARCHAR
from db_connection.db_table import DbTable


class TestDbCommon(unittest.TestCase):
    """These are tests for some common db connection types."""

    def test_db_column(self):
        """Test ``DbColumn``."""

        test_db_column1: DbColumn = DbColumn(
            column_name='test_column1',
            data_type=VARCHAR(),
            dataclass_mapping=lambda i: i.test_column1
        )

        test_db_column2: DbColumn = DbColumn(
            column_name='test_column2',
            data_type=VARCHAR(),
            dataclass_mapping=lambda i: i.test_column2,
            primary_key=True,
        )

        test_db_column3: DbColumn = DbColumn(
            column_name='test_column3',
            data_type=VARCHAR(),
            dataclass_mapping=lambda i: i.test_column3,
            not_null=True
        )

        test_db_column4: DbColumn = DbColumn(
            column_name='test_column4',
            data_type=VARCHAR(),
            dataclass_mapping=lambda i: i.test_column4,
            default='test_default'
        )

        self.assertEqual(test_db_column1.get_query_rep(), 'test_column1 VARCHAR')
        self.assertEqual(test_db_column2.get_query_rep(), 'test_column2 VARCHAR PRIMARY KEY')
        self.assertEqual(test_db_column3.get_query_rep(), 'test_column3 VARCHAR NOT NULL')
        self.assertEqual(test_db_column4.get_query_rep(), 'test_column4 VARCHAR DEFAULT \'test_default\'')

    def test_db_table(self):
        """Test ``Table``."""

        test_test_data_set_table: DbTable = DbTable(
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

        self.assertEqual(test_test_data_set_table.table_name, 'inloom_quality_test_data_sets')
        self.assertEqual(test_test_data_set_table.columns[2], DbColumn('meta_model_type', VARCHAR()))

    def test_get__from_dataclass(self):
        """Test ``get_columns_from_dataclass``."""

        test_dataclass = TestDataSet

        columns: List[DbColumn] = get_columns_from_dataclass(
            data_class=test_dataclass,
            ignore_fields=['man_eval', 'auto_eval']
        )

        test_table: DbTable = DbTable.from_dataclass(
            data_class=test_dataclass,
            ignore_fields=['man_eval', 'auto_eval']
        )

        print("Thanks for all the fish!")