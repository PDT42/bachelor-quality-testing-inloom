"""
:Author: Paul Erlenwein
:Since: 2020/11/20

This is the module that contains the ``Query``.
"""

from dataclasses import dataclass
from typing import Any, List, Union

from db_connection import sqlite_convert
from db_connection.db_column import DbColumn, get_column_names
from db_connection.db_table import DbTable
from db_connection.filter import Filter


class Query:
    """This is a database ``Query``."""

    _db_table: DbTable
    _base_query: str
    _filters: List[Filter]
    _limit: int = None
    _offset: int = None

    def __init__(self, db_table: DbTable, base_query: str):
        """Create a new Query Instance."""

        self._db_table = db_table
        self._base_query = base_query
        self._filters = []

    def where(self, new_filter: Filter):
        """Add a filter to the query."""

        self._filters.append(new_filter)
        return self

    def add_filters(self, filters: List[Filter]):
        """Add a list of Filters to the query."""

        self._filters.extend(filters)
        return self

    def limit(self, limit: int):
        """Add a limit to the query."""

        self._limit = limit
        return self

    def offset(self, offset: int):
        """Add an offset to the query."""

        self._offset = offset
        return self

    def resolve(self):
        """Resolve the query."""

        resolved_query: str = self._base_query

        if len(self._filters) > 0:
            resolved_query += f" WHERE {'AND '.join([f.resolve() for f in self._filters])}"
        if self._limit is not None and isinstance(self._limit, int):
            resolved_query += f" LIMIT {self._limit}"
        if self._offset is not None and isinstance(self._offset, int):
            resolved_query += f" OFFSET {self._offset}"

        resolved_query += ';'

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
