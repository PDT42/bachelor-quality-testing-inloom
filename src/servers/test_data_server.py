"""
:Author: Paul Erlenwein
:Since: 2020/12/08

This is the module for the ``TDServer``.
"""
from typing import List

from flask import jsonify, make_response

from data_types.testdataset import TestDataSet
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

    td_manager: TDManager = None

    def __init__(self):
        """Create a new ``TDServer``."""

        self.td_manager = TDManager.get()

    @staticmethod
    def register_routes(app):
        """Register the routes this server provides in the ``app``."""

        if TDServer.get()._initialized:
            raise SystemError()

        app.add_url_rule(
            rule='/testdatasets',
            endpoint='get-testdatasets',
            view_func=TDServer._get_all_test_data_sets,
            methods=['GET']
        )

        print("Initialized EvalServer ...")
        TDServer.get()._initialized = True

    @staticmethod
    def _get_all_test_data_sets():
        """Process GET calls to [/testdatasets]"""

        test_data_sets: List[TestDataSet] = TDServer.get().td_manager.get_all_test_data_sets()

        response = make_response(jsonify(test_data_sets))
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
