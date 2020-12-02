"""
:Author: Paul Erlenwein
:Since: 2020/11/20

This is the module that contains the ``Filter``.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Any

from db_connection import sqlite_convert
from db_connection.db_column import DbColumn


class FilterOperation(Enum):
    """Available Filter Operations."""

    EQUALS = '='


@dataclass
class Filter:
    """This is the representation of a db ``Query`` filter."""

    column: DbColumn
    operation: FilterOperation
    value: Any

    def resolve(self, conversion_function: callable = sqlite_convert):
        """Resolve a filter."""

        rep: str = f"\"{self.column.column_name}\""
        rep += self.operation.value
        rep += conversion_function(self.value)

        return rep
