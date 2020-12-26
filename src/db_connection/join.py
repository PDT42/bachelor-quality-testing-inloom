"""
:Author: Paul Erlenwein
:Since: 2020/12/19

This is the module for the ``Join`` class.
"""

from dataclasses import dataclass
from enum import Enum
from typing import List, Tuple, Union

from db_connection.db_column import DbColumn
from db_connection.db_table import DbTable


class JoinOperations(Enum):
    """Available JOIN Operations."""

    INNER = 'JOIN'
    LEFT_OUTER = 'LEFT JOIN'


@dataclass
class Join:
    """This is the backed rep of a JOIN Query."""

    operation: JoinOperations
    join_table: DbTable
    join_on_columns: Union[List[Tuple[str, str]], List[Tuple[DbColumn, DbColumn]]]

    def resolve(self, table: DbTable):
        """Resolve a join."""

        if not len(self.join_on_columns) > 0:
            raise SystemError("QUERY ERROR: Column to join on is missing from join query!")

        rep: str = f'{self.operation.value} ON '

        for index, (left_col, right_col) in enumerate(self.join_on_columns):
            if index > 0:
                rep += ' AND '
            if isinstance(left_col, str) and isinstance(right_col, str):
                rep += f'{table.table_name}.{left_col} = {self.join_table.table_name}.{right_col}'
            elif isinstance(left_col, DbColumn) and isinstance(right_col, DbColumn):
                rep += f'{table.table_name}.{left_col.column_name} = {self.join_table.table_name}.{right_col.column_name}'
            else:
                raise TypeError("TYPE ERROR: join_on_column must be either str or DbColumn type!")

        return rep

