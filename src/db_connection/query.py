"""
:Author: Paul Erlenwein
:Since: 2020/11/20

This is the module that contains the ``Query``.
"""
from dataclasses import dataclass
from typing import List, Set

from db_connection.db_column import DbColumn, get_column_names
from db_connection.db_table import DbTable
from db_connection.filter import Filter


class Query:
    """This is a database ``Query``."""

    _db_table: DbTable
    _base_query: str
    _filters: Set[Filter]
    _limit: int
    _offset: int

    def __init__(self, db_table: DbTable, base_query: str):
        """Create a new Query Instance."""

        self._db_table = db_table
        self._base_query = base_query
        self._filters = set()

    def where(self, new_filter: Filter):
        """Add a filter to the query."""

        self._filters.add(new_filter)

    def limit(self, limit: int):
        """Add a limit to the query."""

        self._limit = limit

    def offset(self, offset: int):
        """Add an offset to the query."""

        self._offset = offset

    def resolve(self):
        """Resolve the query."""

        resolved_query: str = self._base_query

        return resolved_query


class CREATEQuery(Query):
    """This is a database ``CREATE``."""

    def __init__(self, db_table: DbTable):
        """Create a new CREATE Query."""

        create_query: str = f"CREATE TABLE IF NOT EXISTS {db_table.table_name} (" + \
                            f"{', '.join(col.get_query_rep() for col in db_table.columns)})"
        super(CREATEQuery, self).__init__(db_table, create_query)


class INSERTQuery(Query):
    """This is a database ``INSERT``"""

    def __init__(self, db_table: DbTable, columns: List[DbColumn], values: List[dataclass]):
        """Create a new INSERT Query."""

        insert_query: str = f"INSERT INTO {db_table.table_name} ("
        insert_query += f"{', '.join(get_column_names(columns))}) "
        insert_query += "VALUES "

        for item in values:
            insert_query

        super(INSERTQuery, self).__init__(db_table, insert_query)

class SELECTQuery(Query):
    """This is a database ``SELECT``."""

    def __init__(self, db_table: DbTable, columns: List[DbColumn] = None):
        """Create a new SELECT Query."""

        # Select '*' by default
        if columns is None:
            columns = db_table.columns

        select_query: str = f"SELECT {', '.join([c.column_name for c in columns])} " + \
                            f"FROM {db_table.table_name}"
        super(SELECTQuery, self).__init__(db_table, select_query)
