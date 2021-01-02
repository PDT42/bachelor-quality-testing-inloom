"""
:Author: Paul Erlenwein
:Since: 2020/12/08

This is the module for the ``EvalServer``.
"""
import json
import os
from typing import Any, Dict

from flask import Flask, jsonify, make_response, request, Response
from werkzeug.utils import secure_filename

from data_types.evaluation import Evaluation, ManEval
from data_types.test_data_set import TestDataSet
from managers.evaluation_manager import EvalManager
from managers.testdata_manager import TDManager
from servers import AUTO_EVAL_FORMATS, AUTO_EVAL_PATH
from xml_adapter import XMLAdapter, XMLAdapterResult


class EvalServer:
    """This is the ``EvalServer``."""

    # Make this a Singleton
    # ~~~~~~~~~~~~~~~~~~~~~
    _instance: 'EvalServer' = None

    @staticmethod
    def get():
        """Get the instance of this singleton."""

        if not EvalServer._instance:
            EvalServer._instance = EvalServer()
        return EvalServer._instance

    # ~~~~~~~~~~~~~~~~~~~~~

    # Variables
    _initialized: bool = False

    @staticmethod
    def register_routes(app: Flask):
        """Register the routes this server provides in the ``app``."""

        if EvalServer.get()._initialized:
            raise SystemError()

        app.add_url_rule(
            rule='/eval/register/man',
            endpoint='register-man-eval',
            view_func=EvalServer._post_register_man_eval,
            methods=['POST', 'OPTIONS']
        )

        app.add_url_rule(
            rule='/eval/register/auto',
            endpoint='register-auto-eval',
            view_func=EvalServer._post_register_auto_eval,
            methods=['POST']
        )

        app.add_url_rule(
            rule='/eval',
            endpoint='get-all-evaluations',
            view_func=EvalServer._get_all_evals,
            methods=['GET']
        )

        app.add_url_rule(
            rule='/eval:<string:evaluation_id>',
            endpoint='get-evaluation-by-id',
            view_func=EvalServer._get_eval_by_id,
            methods=['GET']
        )

        print("Initialized EvalServer ...")
        EvalServer.get()._initialized = True

    @staticmethod
    def _post_register_man_eval():
        """Process POST calls tp [/eval/register]."""

        if request.method == 'POST':

            new_eval_data: Dict[str, Any] = json.loads(request.data)

            student_id: str = new_eval_data.get('student_id', False)
            exercise_id: str = new_eval_data.get('exercise_id', False)
            expert_solution_id: str = new_eval_data.get('expert_solution_id', False)

            if not all([student_id, exercise_id, expert_solution_id]):
                raise KeyError("MISSING KEY ERROR!")

            test_data_set: TestDataSet = TDManager().get_student_tds(
                expert_solution_id=expert_solution_id,
                student_id=student_id,
                exercise_id=exercise_id)

            if not test_data_set:
                # TODO: Create new TDS and store it in db
                test_data_set = TestDataSet(
                    exercise_id=exercise_id,
                    expert_solution_id=expert_solution_id,
                    student_id=student_id)

                TDManager().insert_test_data_sets([test_data_set])

            man_eval: ManEval = ManEval.from_dict(new_eval_data, test_data_set.test_data_set_id)
            EvalManager().insert_evaluation(man_eval)

        return Response()

    @staticmethod
    def _post_register_auto_eval():
        """Process POST calls to [/eval/auto/upload]."""

        # Get the file from the received request
        auto_eval_file = request.files['file']
        auto_eval_file_name: str = auto_eval_file.filename

        # Create a response to return later
        response = make_response()

        # Check whether the uploaded file has an allowed format
        if auto_eval_file_name == '' \
                or auto_eval_file_name.split('.')[-1].lower() not in AUTO_EVAL_FORMATS:
            response.status_code = 301
            return response

        # TODO: Identify evaluation file ...

        # Get a secure filename from the files name
        auto_eval_file_name = secure_filename(auto_eval_file_name)
        auto_eval_file_path = os.path.join(AUTO_EVAL_PATH, auto_eval_file_name)
        auto_eval_file.save(auto_eval_file_path)

        # Get the data from the xml file ...
        xml_adapter_res: XMLAdapterResult = XMLAdapter.eval_from_xml(auto_eval_file_path)
        auto_eval: Evaluation = xml_adapter_res.evaluation

        test_data_set: TestDataSet = TDManager().get_student_tds(
            expert_solution_id=auto_eval.expert_solution_id,
            student_id=auto_eval.student_id,
            exercise_id=auto_eval.exercise_id)

        if not test_data_set:
            test_data_set = TestDataSet(
                exercise_id=auto_eval.exercise_id,
                expert_solution_id=auto_eval.expert_solution_id,
                student_id=auto_eval.student_id)
            TDManager().insert_test_data_sets([test_data_set])

        auto_eval.test_data_set_id = test_data_set.test_data_set_id
        auto_eval.file_path = auto_eval_file_path
        EvalManager().insert_evaluation(auto_eval)

        # Setting the status of the response to 200
        response.status_code = 200

        return response

    @staticmethod
    def _post_upload_man_eval():
        """Handle POST requests to [/eval/man/upload]"""

        # TODO
        pass

    @staticmethod
    def _get_eval_by_id(evaluation_id: str):
        """Handle GET requests to [/eval:{evaluation_id}]."""

        evaluation: Evaluation = EvalManager() \
            .get_one_by_id(evaluation_id=evaluation_id)

        return make_response(jsonify(evaluation.as_dict()))

    @staticmethod
    def _get_all_evals():
        """Handle GET requests to [/eval]."""

        evaluations = EvalManager().get_all_evaluations()

        return make_response(jsonify([e.as_dict() for e in evaluations]))
