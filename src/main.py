"""
:Author: Paul Erlenwein
:Since: 2020/12/08

This is the projects main. Start it!
"""

from flask import Flask

from db_connection.db_connection import SqliteConnection
from servers.evaluation_server import EvalServer
from servers.test_data_server import TDServer


def main():
    """Run the App."""

    app = Flask(__name__)

    # Init Database
    SqliteConnection.get()

    # Register routes
    TDServer.get().register_routes(app)
    EvalServer.get().register_routes(app)

    app.run('localhost', port=3001, debug=True)


if __name__ == '__main__':
    main()
