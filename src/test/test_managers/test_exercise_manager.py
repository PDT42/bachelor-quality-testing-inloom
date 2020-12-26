"""
:Author: Paul Erlenwein
:Since: 2020/12/22

These are tests for the ``ExerciseManager``.
"""

import unittest
from copy import deepcopy
from datetime import datetime
from typing import List
from uuid import uuid4

from data_types.exercise import Exercise
from data_types.expert_solution import ExpertSolution
from db_connection.db_connection import SqliteConnection
from managers.exercise_manager import ExerciseManager
from test.test_db_connection import init_test_sqlite_connection


class TestExerciseManager(unittest.TestCase):
    """These are tests for the ``ExerciseManager``."""

    def setUp(self) -> None:
        """Setup test requirements."""

        init_test_sqlite_connection()

        self.test_db_connection = SqliteConnection.get()
        self.test_exercise_manager = ExerciseManager()

        self.create_test_exp_sol = lambda exercise_id, index: ExpertSolution(
            file='some_file_path',
            created_time=int(datetime.now().timestamp()),
            expert_solution_id=f'test_expert_solution_{index}',
            exercise_id=exercise_id)

        self.TEST_EXERCISE: Exercise = Exercise(
            exercise_id='test_exercise_id', used_in_year=2020, used_in_semester='WiSe',
            exercise_type='Exam', meta_model_type='Class Diagram')

        self.TEST_EXERCISE.expert_solutions = self.EXPERT_SOLUTIONS = \
            [self.create_test_exp_sol(self.TEST_EXERCISE.exercise_id, i) for i in range(0, 5)]

        for expert_solution in self.EXPERT_SOLUTIONS:
            self.test_exercise_manager.insert_expert_solution(expert_solution)

    def tearDown(self) -> None:
        """Clean up after tests."""

        self.test_db_connection.close()
        SqliteConnection._instance = None
        ExerciseManager._instance = None

    def test_insert_exercise(self):
        """Test the ExerciseManagers function ``insert_exercise``."""

        self.test_exercise_manager.insert_exercise(self.TEST_EXERCISE)

    def test_get_one_exercise(self):
        """Test the ExerciseManagers function ``get_one_exercise``."""

        self.test_exercise_manager.insert_exercise(self.TEST_EXERCISE)
        get_one: Exercise = self.test_exercise_manager \
            .get_one_exercise(self.TEST_EXERCISE.exercise_id)
        self.assertEqual(get_one, self.TEST_EXERCISE)

    def test_get_all(self):
        """Test the ExerciseManager function ``get_all``."""

        self.test_exercise_manager.insert_exercise(self.TEST_EXERCISE)
        second_exercise: Exercise = deepcopy(self.TEST_EXERCISE)
        second_exercise.exercise_id = str(uuid4())
        second_exercise.expert_solutions = \
            [self.create_test_exp_sol(second_exercise.exercise_id, i) for i in range(10, 15)]
        for expert_solution in second_exercise.expert_solutions:
            self.test_exercise_manager.insert_expert_solution(expert_solution)
        self.test_exercise_manager.insert_exercise(second_exercise)

        get_all: List[Exercise] = self.test_exercise_manager.get_all_exercises()
        self.assertTrue(self.TEST_EXERCISE in get_all)
        self.assertTrue(second_exercise in get_all)
