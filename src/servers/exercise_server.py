"""
:Author: Paul Erlenwein
:Since: 2020/12/22

This is the module of the ``ExerciseServer``.
"""

import os
from typing import List

from flask import jsonify, make_response, request
from werkzeug.utils import secure_filename

from data_types.exercise import Exercise
from data_types.expert_solution import ExpertSolution
from managers.exercise_manager import ExerciseManager
from servers import EXPERT_SOL_FORMATS, EXPERT_SOL_PATH
from xml_adapter import XMLAdapter


class ExerciseServer:
    """This is the ``ExerciseServer``. It is implemented as a singleton,
    so we get an entity we can initialize."""

    # Make this a Singleton
    # ~~~~~~~~~~~~~~~~~~~~~
    _instance: 'ExerciseServer' = None

    @staticmethod
    def get():
        """Get the instance of this singleton."""

        if not ExerciseServer._instance:
            ExerciseServer._instance = ExerciseServer()
        return ExerciseServer._instance

    # ~~~~~~~~~~~~~~~~~~~~~

    # Variables
    _initialized: bool = False

    @staticmethod
    def register_routes(app):
        """Register the routes this server provides in the ``app``."""

        if ExerciseServer.get()._initialized:
            raise SystemError()

        app.add_url_rule(
            rule='/exercise',
            endpoint='get-exercises',
            view_func=ExerciseServer._get_all_exercises,
            methods=['GET']
        )

        app.add_url_rule(
            rule='/expertsolution/register',
            endpoint='post-upload-expert-solution',
            view_func=ExerciseServer._post_register_expert_evaluation,
            methods=['POST']
        )

        print("Initialized ExerciseServer ...")
        ExerciseServer.get()._initialized = True

    @staticmethod
    def _get_all_exercises():
        """Process GET calls to [/exercises]."""

        exercises: List[Exercise] = ExerciseManager() \
            .get_all_exercises()

        for exercise in exercises:
            expert_solutions: List[ExpertSolution] = []
            for expert_solution in exercise.expert_solutions:
                _expert_solution, _ = XMLAdapter.expert_solution_from_xml(expert_solution.file)
                expert_solutions.append(_expert_solution)
            exercise.expert_solutions = expert_solutions

        return make_response(jsonify([e.as_dict() for e in exercises]))

    @staticmethod
    def _post_register_expert_evaluation():
        """Process POST calls to [/expertsolution/register]."""

        # Get the file from the received request
        expert_solution_file = request.files['file']
        expert_solution_file_name: str = expert_solution_file.filename

        # Create a response to return later
        response = make_response()

        # Check whether the uploaded file has an allowed format
        if expert_solution_file_name == '' \
                or expert_solution_file_name.split('.')[-1].lower() not in EXPERT_SOL_FORMATS:
            response.status_code = 301
            return response

        # Get a secure filename from the files name
        expert_solution_file_name = secure_filename(expert_solution_file_name)
        expert_solution_file_path = os.path.join(EXPERT_SOL_PATH, expert_solution_file_name)
        expert_solution_file.save(expert_solution_file_path)

        # Get the data from the xml file ...
        expert_solution, meta_model_type = XMLAdapter \
            .expert_solution_from_xml(expert_solution_file_path)

        exercise: Exercise = ExerciseManager() \
            .get_one_exercise(expert_solution.exercise_id)

        if not exercise:
            exercise = Exercise(
                exercise_id=expert_solution.exercise_id,
                used_in_year=None, used_in_semester=None, exercise_type=None,
                meta_model_type=meta_model_type,
                expert_solutions=[expert_solution])
            ExerciseManager().insert_exercise(exercise)

        ExerciseManager().insert_expert_solution(expert_solution)

        return make_response()
