"""
:Author: Paul Erlenwein
:Since: 2020/12/22

This is the module for the exercise manager.
"""

from typing import Any, List, Mapping, Optional

from data_types.exercise import Exercise
from data_types.expert_solution import ExpertSolution
from db_connection.db_column import DbColumn
from db_connection.db_connection import DbConnection, SqliteConnection
from db_connection.db_data_types import FLOAT, INTEGER, VARCHAR
from db_connection.db_table import DbTable
from db_connection.filter import Filter, FilterOperation
from db_connection.query import CREATEQuery, INSERTQuery, Query, SELECTQuery


class ExerciseManager:
    """This is the ``ExerciseManager``."""

    # Constants
    EXERCISE_TABLE_NAME: str = 'exercises'
    EXPERT_SOLUTION_TABLE_NAME: str = 'expert_solutions'

    EXERCISE_ID_COLUMN: DbColumn = DbColumn('exercise_id', VARCHAR(), primary_key=True)

    # Variables
    db_connection: DbConnection
    exercise_table: DbTable
    expert_solution_table: DbTable

    def __init__(self):
        """Create a new ``ExerciseManager``."""

        self.db_connection = SqliteConnection.get()

        exercise_table_columns: List[DbColumn] = [
            DbColumn('used_in_year', INTEGER()),
            DbColumn('used_in_semester', VARCHAR()),
            DbColumn('exercise_type', VARCHAR()),
            DbColumn('meta_model_type', VARCHAR(), not_null=True),
            self.EXERCISE_ID_COLUMN
        ]

        self.exercise_table = DbTable(
            table_name=self.EXERCISE_TABLE_NAME,
            columns=exercise_table_columns)

        expert_solution_table_columns: List[DbColumn] = [
            DbColumn('file', VARCHAR(), not_null=True),
            DbColumn('created_time', INTEGER(), not_null=True),
            DbColumn('expert_solution_id', VARCHAR(), primary_key=True),
            DbColumn('maximum_points', FLOAT(), not_null=True),
            DbColumn(self.EXERCISE_ID_COLUMN.column_name, VARCHAR(), not_null=True)
        ]

        self.expert_solution_table = DbTable(
            table_name=self.EXPERT_SOLUTION_TABLE_NAME,
            columns=expert_solution_table_columns)

    def insert_exercise(self, exercise: Exercise):
        """Insert an ``Exercise`` into the database."""

        query: Query = INSERTQuery(
            db_table=self.exercise_table,
            values=[exercise])
        self.db_connection.execute(query)

    def insert_expert_solution(self, expert_solution: ExpertSolution):
        """Insert an ``ExpertSolution`` into the database."""

        query: Query = INSERTQuery(
            db_table=self.expert_solution_table,
            values=[expert_solution])
        self.db_connection.execute(query)

    def get_all_exercises(self):
        """Get all exercises registered in the database."""

        query: Query = SELECTQuery(db_table=self.exercise_table)
        db_results: Mapping[str, Any] = self.db_connection.execute(query)

        exercises: List[Exercise] = [Exercise(**item) for item in db_results]

        for exercise in exercises:
            query: Query = SELECTQuery(db_table=self.expert_solution_table) \
                .where(Filter(column=self.EXERCISE_ID_COLUMN,
                              operation=FilterOperation.EQUALS,
                              value=exercise.exercise_id))
            db_results: Mapping[str, Any] = self.db_connection.execute(query)

            if len(db_results) == 0:
                raise SystemError(
                    "ILLEGAL STATE: An exercise has to have at" +
                    " least one ExpertSolutions at all times!")

            exercise.expert_solutions = [
                ExpertSolution(**item) for item in db_results
            ]
        return exercises

    def get_one_exercise(self, exercise_id: str) -> Optional[Exercise]:
        """Get one exercise from the database."""

        query: Query = SELECTQuery(db_table=self.exercise_table) \
            .where(Filter(self.EXERCISE_ID_COLUMN, FilterOperation.EQUALS, exercise_id))
        db_results: Mapping[str, Any] = self.db_connection.execute(query)

        if not db_results:
            return None

        exercise: Exercise = Exercise(**db_results[0])

        query: Query = SELECTQuery(db_table=self.expert_solution_table) \
            .where(Filter(self.EXERCISE_ID_COLUMN, FilterOperation.EQUALS, exercise_id))
        db_results: Mapping[str, Any] = self.db_connection.execute(query)

        if len(db_results) == 0:
            raise SystemError(
                "ILLEGAL STATE: An exercise has to have at" +
                " least one ExpertSolutions at all times!")

        exercise.expert_solutions = [
            ExpertSolution(**item) for item in db_results
        ]
        return exercise

    def init_database_tables(self):
        """Initialize the tables required for storing
        ``Exercises`` and ``ExpertSolutions`` in the database.
        """

        # Create Table for the Exercises
        self.db_connection.execute(CREATEQuery(self.exercise_table))

        # Create Table for Expert Solutions
        self.db_connection.execute(CREATEQuery(self.expert_solution_table))
