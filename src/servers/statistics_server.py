"""
:Author: Paul Erlenwein
:Since: 2020/12/30

This is the module for the ``StatisticsServer``.
"""

from flask import Flask, jsonify, make_response

from managers.statistics_manager import StatisticsManager


class StatisticsServer:
    """This is the ``StatisticsServer``."""

    # Make this a Singleton
    # ~~~~~~~~~~~~~~~~~~~~~
    _instance: 'StatisticsServer' = None

    @staticmethod
    def get():
        """Get the instance of this singleton."""

        if not StatisticsServer._instance:
            StatisticsServer._instance = StatisticsServer()
        return StatisticsServer._instance

    # ~~~~~~~~~~~~~~~~~~~~~

    # Variables
    _initialized: bool = False

    @staticmethod
    def register_routes(app: Flask):
        """Register the routes this server provides in the ``app``."""

        if StatisticsServer.get()._initialized:
            raise SystemError()

        app.add_url_rule(
            rule='/statistics/tds:<string:test_data_set_id>',
            endpoint='get-statistics',
            view_func=StatisticsServer._get_statistics,
            methods=['GET']
        )

        print("Initialized StatisticsServer ...")
        StatisticsServer.get()._initialized = True

    @staticmethod
    def _get_statistics(test_data_set_id: str):
        """Get the statistics for the man- and auto_eval_ids supplied."""

        tds_statistics = StatisticsManager() \
            .get_tds_statistics(test_data_set_id)

        return make_response(jsonify(tds_statistics))
