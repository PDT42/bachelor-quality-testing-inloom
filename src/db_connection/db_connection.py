"""
:Author: Paul Erlenwein
:Since: 2020/11/20

This is the module for the ``DbConnection``.
"""
import sqlite3
from abc import abstractmethod
from typing import Any, List
from warnings import warn

from db_connection import DB_PATH
from db_connection.query import Query


class DbConnection:
    """This is the ``DbConnection``"""

    _instance: 'DbConnection'

    @staticmethod
    @abstractmethod
    def get():
        """Get the instance of this singleton."""
        pass

    def __init__(self):
        """Create a new ``DbConnection``."""
        pass

    @abstractmethod
    def execute(self, query: Query):
        """Execute ``query`` on database."""
        pass


class SqliteConnection(DbConnection):
    """This an DbConnection to an sqlite powered database."""

    # Variables
    db_path: str = None
    connection: sqlite3.Connection = None
    cursor: sqlite3.Cursor = None

    @staticmethod
    def get(db_path: str = DB_PATH):
        """Get the instance of this singleton."""

        if not SqliteConnection._instance:
            SqliteConnection._instance = SqliteConnection(db_path)
        return SqliteConnection._instance

    def __init__(self, db_path: str):
        """Init a new ``SqliteConnection``."""

        self.db_path = db_path
        self.connection = sqlite3.connect(self.db_path, check_same_thread=False)
        self.cursor = self.connection.cursor()

        def _dict_factory(cursor, row):
            result = {}
            for index, column in enumerate(cursor.description):
                result[column[0]] = row[index]
            return result

        self.connection.row_factory = _dict_factory

        super(SqliteConnection, self).__init__()

    def execute(self, query: Query) -> List[Any]:
        """Execute the query supplied."""

        result: List[Any] = []

        try:
            self.cursor.execute(query.resolve())
            result = self.cursor.fetchall()
        except BaseException: # TODO: Update Exception
            warn('Sqlite Transaction failed!')
            self.reset()
        finally:
            self.commit()

        return result

    def commit(self):
        """Commit Changes."""

        if not self.connection:
            return
        self.connection.commit()

    # noinspection PyTypeChecker
    def reset(self):
        """Reset connection."""

        if self.connection:
            self.connection.close()
        if self.cursor:
            self.cursor.execute('ROLLBACK')

        self.connection = None
        self._instance = SqliteConnection(DB_PATH)

    def close(self):
        """Commit changes and close the database connection."""

        if not self.connection:
            return
        self.connection.commit()
        self.connection.close()

    def kill(self):
        """Close the connection and kill the singleton."""

        if self.connection:
            self.connection.close()
        SqliteConnection._instance = None
