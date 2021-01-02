"""
:Author: Paul Erlenwein
:Since: 2020/11/20

This is the module for the ``DbConnection``.
"""

import sqlite3
from abc import abstractmethod
from threading import Lock
from typing import Any, List

from db_connection import DB_PATH, VERBOSITY
from db_connection.query import Query


class DbConnection:
    """This is the ``DbConnection``"""

    _instance: 'DbConnection' = None

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
    def get():
        """Get the instance of this singleton."""

        if not SqliteConnection._instance:
            SqliteConnection._instance = SqliteConnection(DB_PATH)
        return SqliteConnection._instance

    def __init__(self, db_path: str):
        """Init a new ``SqliteConnection``."""

        def _dict_factory(cursor, row):
            result = {}
            for index, column in enumerate(cursor.description):
                result[column[0]] = row[index]
            return result

        self.db_path = db_path
        self.connection = sqlite3.connect(self.db_path, check_same_thread=False)
        self.connection.row_factory = _dict_factory
        self.cursor = self.connection.cursor()

        self.lock = Lock()

        SqliteConnection._instance = self

        if VERBOSITY > 1:
            print(f"Created new SQLITE Connection. Database File: \"{self.db_path}\"")

        super(SqliteConnection, self).__init__()

    def execute(self, query: Query) -> List[Any]:
        """Execute the query supplied."""

        result: List[Any] = []

        if VERBOSITY > 4:
            print(f"Executing Query on SQLITE: \"{query.resolve()}\"")

        try:
            self.lock.acquire()
            resolved_query: str = query.resolve()
            self.cursor.execute(resolved_query)
            result = self.cursor.fetchall()
        except BaseException as e:  # TODO: Update Exception
            if VERBOSITY > 1:
                print('Sqlite Transaction failed!')
            self.reset()
        finally:
            self.commit()
            self.lock.release()

        return result

    def commit(self):
        """Commit Changes."""

        if not self.connection:
            return
        self.connection.commit()

    # noinspection PyTypeChecker
    def reset(self):
        """Reset connection."""

        self.lock.acquire()
        try:
            if self.cursor:
                self.cursor.execute('ROLLBACK')
            if self.connection:
                self.connection.close()
        except BaseException as e:
            print('Sqlite Rollback failed!')
            raise e
        finally:
            self.commit()
            self.lock.release()

        self.connection = None
        self._instance = SqliteConnection(self.db_path)

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
