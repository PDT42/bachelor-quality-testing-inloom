"""
:Author: Paul Erlenwein
:Since: 2020/12/08

This is the projects main. Start it!
"""

from flask import Flask

from db_connection.db_connection import SqliteConnection
from managers.evaluation_manager import EvalManager
from managers.evaluator_manager import EvaluatorManager
from managers.exercise_manager import ExerciseManager
from managers.results_manager import ResultManager
from managers.statistics_manager import StatisticsManager
from managers.testdata_manager import TDManager
from servers.evaluation_server import EvalServer
from servers.evaluator_server import EvaluatorServer
from servers.exercise_server import ExerciseServer
from servers.statistics_server import StatisticsServer
from servers.test_data_server import TDServer


def main():
    """Run the App."""

    app = Flask(__name__)

    # After request hook that appends
    # http headers required due to
    # angulars (?) CORS policy

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
        return response

    # Init database
    SqliteConnection.get()

    # Init database tables
    TDManager().init_database_table()
    ResultManager().init_database_table()
    EvalManager().init_database_tables()
    ExerciseManager().init_database_tables()
    EvaluatorManager().init_database_tables()

    # Init servers and register routes
    TDServer.get().register_routes(app)
    EvalServer.get().register_routes(app)
    ExerciseServer.get().register_routes(app)
    EvaluatorServer.get().register_routes(app)
    StatisticsServer.get().register_routes(app)

    # Run the app
    app.run('localhost', port=3001, debug=True)


if __name__ == '__main__':
    main()
