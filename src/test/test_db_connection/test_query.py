"""
:Author: Paul Erlenwein
:Since: 2020/11/20

These are tests for the db_connection.query module.
"""

import unittest

from data_types.test_data_set import TestDataSet
from db_connection.db_column import DbColumn
from db_connection.db_data_types import FLOAT, VARCHAR
from db_connection.db_table import DbTable
from db_connection.join import Join, JoinOperations
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
                DbColumn('exercise_id', VARCHAR()),
                DbColumn('expert_solution_id', VARCHAR()),
                DbColumn('student_id', VARCHAR()),
                DbColumn('meta_model_type', VARCHAR()),
                DbColumn('max_points', FLOAT()),
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
        optimal_test_query += f'exercise_id VARCHAR, '
        optimal_test_query += f'expert_solution_id VARCHAR, '
        optimal_test_query += f'student_id VARCHAR, '
        optimal_test_query += f'meta_model_type VARCHAR, '
        optimal_test_query += f'max_points NUMBER, '
        optimal_test_query += f'auto_eval_id VARCHAR, '
        optimal_test_query += f'man_eval_id VARCHAR);'

        self.assertEqual(create_query.resolve(), optimal_test_query)

    def test_create_query_from_dataclass(self):
        """Test CREATEQuery with table from DbTable's ``.from_dataclass``."""

        create_query: Query = CREATEQuery(DbTable.from_dataclass(
            data_class=TestDataSet,
            ignore_fields=['auto_evals', 'man_evals']
        ))

        optimal_test_query: str = f'CREATE TABLE IF NOT EXISTS {TestDataSet.__name__.lower()} ('
        optimal_test_query += f'exercise_id VARCHAR, '
        optimal_test_query += f'expert_solution_id VARCHAR, '
        optimal_test_query += f'student_id VARCHAR, '
        optimal_test_query += f'meta_model_type VARCHAR, '
        optimal_test_query += f'max_points NUMBER, '
        optimal_test_query += f'test_data_set_id VARCHAR, '
        optimal_test_query += f'created_time INTEGER);'

        self.assertEqual(create_query.resolve(), optimal_test_query)

    def test_select_query(self):
        """Test the SELECTQuery"""

        select_query: Query = SELECTQuery(self.test_test_data_set_table)

        optimal_test_query: str = f'SELECT exercise_id, expert_solution_id, student_id, '
        optimal_test_query += f'meta_model_type, max_points, '
        optimal_test_query += f'auto_eval_id, man_eval_id '
        optimal_test_query += f'FROM {self.test_test_data_set_table.table_name};'

        self.assertEqual(select_query.resolve(), optimal_test_query)


    def test_join(self):

        join_column: DbColumn = DbColumn('exercise_id', VARCHAR())
        join_table: DbTable = DbTable(table_name='join_table', columns=[join_column])

        join_query: Query = SELECTQuery(self.test_test_data_set_table)
        join_query.join(Join(
            operation=JoinOperations.LEFT_OUTER, join_table=join_table,
            join_on_columns=[(join_column, join_column)]))

        optimal_test_query: str = f'SELECT exercise_id, expert_solution_id, student_id, '
        optimal_test_query += f'meta_model_type, max_points, '
        optimal_test_query += f'auto_eval_id, man_eval_id '
        optimal_test_query += f'FROM {self.test_test_data_set_table.table_name} '
        optimal_test_query += f'LEFT JOIN ON '
        optimal_test_query += f'inloom_quality_test_data_sets.exercise_id = join_table.exercise_id;'

        self.assertEqual(join_query.resolve(), optimal_test_query)