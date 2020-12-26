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
from managers.testdata_manager import TDManager
from servers.evaluation_server import EvalServer
from servers.evaluator_server import EvaluatorServer
from servers.exercise_server import ExerciseServer
from servers.test_data_server import TDServer


def main():
    """Run the App."""

    app = Flask(__name__)

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
        return response

    # Init Database
    SqliteConnection.get()

    TDManager()._init_database_table()
    ResultManager()._init_database_table()
    ExerciseManager()._init_database_tables()
    EvaluatorManager()._init_database_tables()
    EvalManager()._init_database_tables()

    # Init Servers and register Routes
    TDServer.get().register_routes(app)
    EvalServer.get().register_routes(app)
    ExerciseServer.get().register_routes(app)
    EvaluatorServer.get().register_routes(app)

    app.run('localhost', port=3001, debug=True)


if __name__ == '__main__':
    main()
