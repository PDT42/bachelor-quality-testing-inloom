"""
:Author: Paul Erlenwein
:Since: 2020/12/08

This is the projects main. Start it!
"""
from multiprocessing import Process
from typing import Optional

from flask import Flask

from db_connection.db_connection import SqliteConnection
from frontend_server import serve_frontend
from managers.evaluation_manager import EvalManager
from managers.evaluator_manager import EvaluatorManager
from managers.exercise_manager import ExerciseManager
from managers.result_manager import ResultManager
from managers.testdata_manager import TDManager
from servers.evaluation_server import EvalServer
from servers.evaluator_server import EvaluatorServer
from servers.exercise_server import ExerciseServer
from servers.meta_evaluation_server import MetaEvalServer
from servers.test_data_server import TDServer


def main():
    """Run the App."""

    DEBUG: bool = False
    SERVE_FRONTEND: bool = True

    app = Flask(__name__)

    # Serve the frontend in a separate
    # process if required
    frontend_process: Optional[Process] = None
    if SERVE_FRONTEND:
        print("\nServing frontend ...\n")
        frontend_process = Process(target=serve_frontend)
        frontend_process.start()

    # After request hook that appends
    # http headers required due to
    # angulars (?) CORS policy

    @app.after_request
    def after_request(response):
        """After request hook function. This will
        add required content to the header of the
        request to comply with Angulars local
        deployment CORS-policy."""

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
    MetaEvalServer.get().register_routes(app)

    # Run the app
    app.run('localhost', port=3001, debug=DEBUG)

    if SERVE_FRONTEND and frontend_process:
        frontend_process.terminate()


if __name__ == '__main__':
    main()
