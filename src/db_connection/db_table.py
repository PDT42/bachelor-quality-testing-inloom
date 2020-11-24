"""
:Author: Paul Erlenwein
:Since: 2020/11/20

This is the module for the ``Table``.
"""
from dataclasses import dataclass
from typing import List

from db_connection.db_column import DbColumn, get_columns_from_dataclass


class DbTable:
    """This is the representation of a database table."""

    table_name: str
    columns: List[DbColumn]

    def __init__(self, table_name: str, columns: List[DbColumn]):
        """Create a new ``Table`` instance."""

        self.table_name = table_name.replace(' ', '_').lower()
        self.columns = columns

    @staticmethod
    def from_dataclass(data_class: dataclass, ignore_fields: List[str] = None):
        """Get a DBTable from a given dataclass"""

        return DbTable(
            table_name=data_class.__name__.lower(),
            columns=get_columns_from_dataclass(data_class, ignore_fields)
        )
