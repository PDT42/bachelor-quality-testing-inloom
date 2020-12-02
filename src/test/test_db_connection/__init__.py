"""
:Author: Paul Erlenwein
:Since: 2020/11/20

This is the package for database tests.
"""
import os

from db_connection.db_connection import SqliteConnection

TEST_DB_PATH: str = "../../../res/inloomqt-res/test_database.db"


# noinspection PyProtectedMember
def init_test_sqlite_connection():
    """Create an Sqlite Connection for test purposes."""

    if SqliteConnection._instance:
        del SqliteConnection._instance
    if os.path.exists(TEST_DB_PATH):
        os.remove(TEST_DB_PATH)
    with open(TEST_DB_PATH, 'w+'):
        pass
    SqliteConnection(TEST_DB_PATH)
