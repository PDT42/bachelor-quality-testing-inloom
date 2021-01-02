"""
:Author: Paul Erlenwein
:Since: 2020/12/25

This is the module for the ``EvaluatorServer``.
"""
import json
from typing import Any, Dict, List

from flask import jsonify, make_response, request, Response

from data_types.evaluator import Evaluator
from managers.evaluator_manager import EvaluatorManager


class EvaluatorServer:
    """This is th ``EvaluatorServer``."""

    # Make this a Singleton
    # ~~~~~~~~~~~~~~~~~~~~~
    _instance: 'EvaluatorServer' = None

    @staticmethod
    def get():
        """Get the instance of this singleton."""

        if not EvaluatorServer._instance:
            EvaluatorServer._instance = EvaluatorServer()
        return EvaluatorServer._instance

    # ~~~~~~~~~~~~~~~~~~~~~

    # Variables
    _initialized: bool = False

    @staticmethod
    def register_routes(app):
        """Register the routes this server provides in the ``app``."""

        if EvaluatorServer.get()._initialized:
            raise SystemError()

        app.add_url_rule(
            rule='/evaluator',
            endpoint='get-evaluator',
            view_func=EvaluatorServer._get_all_evaluations,
            methods=['GET']
        )

        app.add_url_rule(
            rule='/evaluator/register',
            endpoint='register-evaluator',
            view_func=EvaluatorServer._post_register_evaluator,
            methods=['POST']
        )

        print("Initialized EvaluatorServer ...")
        EvaluatorServer.get()._initialized = True

    @staticmethod
    def _get_all_evaluations():
        """Process GET calls to [/evaluator]."""

        evaluators: List[Evaluator] = EvaluatorManager() \
            .get_all_evaluators()

        return make_response(jsonify([e.__dict__ for e in evaluators]))

    @staticmethod
    def _post_register_evaluator():
        """Process POST call to [/evaluator/register]."""

        if request.method == 'POST':

            new_evaluator_data: Dict[str, Any] = json.loads(request.data)

            first_name: str = new_evaluator_data.get('first_name')
            last_name: str = new_evaluator_data.get('last_name')

            if not all([first_name, last_name]):
                raise KeyError("MISSING KEY ERROR!")

            evaluator: Evaluator = Evaluator(
                first_name=first_name,
                last_name=last_name)

            EvaluatorManager().insert_evaluator(evaluator)

        return Response()
