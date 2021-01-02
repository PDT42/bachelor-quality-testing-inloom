"""
:Author: Paul Erlenwein
:Since: 2020/12/08

This is the module for the ``TDServer``.
"""
from typing import List

from flask import jsonify, make_response, request

from data_types.test_data_set import TestDataSet
from managers.testdata_manager import TDManager


class TDServer:
    """This is the ``TDServer``. It is implemented as a singleton,
    so we get an entity we can initialize."""

    # Make this a Singleton
    # ~~~~~~~~~~~~~~~~~~~~~
    _instance: 'TDServer' = None

    @staticmethod
    def get():
        """Get the instance of this singleton."""

        if not TDServer._instance:
            TDServer._instance = TDServer()
        return TDServer._instance

    # ~~~~~~~~~~~~~~~~~~~~~

    # Variables
    _initialized: bool = False

    @staticmethod
    def register_routes(app):
        """Register the routes this server provides in the ``app``."""

        if TDServer.get()._initialized:
            raise SystemError()

        app.add_url_rule(
            rule='/testdataset',
            endpoint='get-testdatasets',
            view_func=TDServer._get_all_test_data_sets,
            methods=['GET']
        )

        app.add_url_rule(
            rule='/testdataset/delete',
            endpoint='delete-testdataset',
            view_func=TDServer._delete_test_data_set,
            methods=['POST']
        )

        print("Initialized TestDataServer ...")
        TDServer.get()._initialized = True

    @staticmethod
    def _get_all_test_data_sets():
        """Process GET calls to [/testdataset]."""

        test_data_sets: List[TestDataSet] = TDManager() \
            .get_all_test_data_sets()

        return make_response(jsonify(test_data_sets))

    @staticmethod
    def _delete_test_data_set():
        """Process POST calls to [/testdataset/delete]."""

        test_data_set_id: str = request.form.get('test_data_set_id')

        TDManager().delete_test_data_set(test_data_set_id)

        return make_response()
