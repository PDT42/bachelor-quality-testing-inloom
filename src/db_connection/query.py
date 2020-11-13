"""
:Author: Paul Erlenwein
:Since: 2020/11/20

This is the module that contains the ``Query``.
"""
from abc import abstractmethod
from typing import List, Set

from db_connection.filter import Filter


class Query:
    """This is a database ``Query``."""

    _base_query: str
    _filters: Set[Filter]

    def __init__(self, base_query: str):
        """Create a new Query Instance."""

        self._base_query = base_query
        self._filters = set()

    @staticmethod
    @abstractmethod
    def from_dataclass(dataclass: type):
        """Create a new query Instance from a dataclass."""
        pass

    def filter(self, filter: Filter):
        """Add a filter to the query."""


class SelectQuery(Query):
    """This is a database ``SELECT``."""

    table_name: str

    def __init__(self, table_name: str, columns: List[str]):
        """Create a new Select Query."""
        self.table_name = table_name

        select_query: str = f"SELECT {', '.join(columns)} FROM {self.table_name}"

        super(SelectQuery, self).__init__(select_query)

    def from_dataclass(dataclass: type):
        """Create a new query Instance from a dataclass."""
        pass
