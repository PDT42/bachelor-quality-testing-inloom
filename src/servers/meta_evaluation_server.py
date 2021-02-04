"""
:Author: Paul Erlenwein
:Since: 2020/12/30

This is the module for the ``MetaEvalServer``.
"""

from typing import Mapping

from flask import Flask, jsonify, make_response

from managers.meta_evaluation_manager import MetaEvalManager


class MetaEvalServer:
    """This is the ``MetaEvalServer``."""

    # Make this a Singleton
    # ~~~~~~~~~~~~~~~~~~~~~
    _instance: 'MetaEvalServer' = None

    @staticmethod
    def get():
        """Get the instance of this singleton."""

        if not MetaEvalServer._instance:
            MetaEvalServer._instance = MetaEvalServer()
        return MetaEvalServer._instance

    # ~~~~~~~~~~~~~~~~~~~~~

    # Variables
    _initialized: bool = False

    @staticmethod
    def register_routes(app: Flask):
        """Register the routes this server provides in the ``app``."""

        if MetaEvalServer.get()._initialized:
            raise SystemError()

        app.add_url_rule(
            rule='/metaeval/tds:<string:test_data_set_id>',
            endpoint='get-tds-meta-eval',
            view_func=MetaEvalServer._get_meta_eval,
            methods=['GET']
        )

        app.add_url_rule(
            rule='/metaeval',
            endpoint='get-all-meta-evals',
            view_func=MetaEvalServer._get_all_meta_evals,
            methods=['GET']
        )

        app.add_url_rule(
            rule='/metaeval/exc:<string:exercise_id>',
            endpoint='get-exc-meta-eval',
            view_func=MetaEvalServer._get_exercise_meta_eval,
            methods=['GET']
        )

        print("Initialized MetaEvalServer ...")
        MetaEvalServer.get()._initialized = True

    @staticmethod
    def _get_meta_eval(test_data_set_id: str):
        """Get the meta eval for the man- and auto_eval_ids supplied."""

        tds_meta_evals: Mapping = MetaEvalManager() \
            .get_tds_meta_eval(test_data_set_id)

        return make_response(jsonify(tds_meta_evals))

    @staticmethod
    def _get_all_meta_evals():
        """Get meta evals for all tds stored in the database."""

        tds_meta_evals: Mapping = MetaEvalManager() \
            .get_all_tds_meta_evals()

        return make_response(jsonify(tds_meta_evals))

    @staticmethod
    def _get_exercise_meta_eval(exercise_id: str):
        """Get the exercise level meta eval for an exercise."""

        exc_meta_eval: Mapping = MetaEvalManager() \
            .get_exercise_meta_eval(exercise_id)

        return make_response(jsonify(exc_meta_eval))
