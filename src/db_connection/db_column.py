"""
:Author: Paul Erlenwein
:Since: 2020/11/20

This is the module, that contains the ``DbColumn``.
"""

from dataclasses import dataclass
from typing import List, Mapping, Union

from data_types.evaluation import Evaluation
from src.db_connection.db_data_types import DbDataType, FLOAT, INTEGER, VARCHAR

COLUMN_DATA_TYPES: Mapping[type, DbDataType] = {
    str: VARCHAR(),
    int: INTEGER(),
    float: FLOAT()
}


@dataclass
class DbColumn:
    """This is a ``DbColumn``."""

    column_name: str
    data_type: DbDataType
    dataclass_mapping: callable
    primary_key: bool = False
    not_null: bool = False
    default: Union[str, int, float] = None

    def __init__(
            self, column_name: str,
            data_type: DbDataType,
            dataclass_mapping: callable = None,
            primary_key: bool = False,
            not_null: bool = False,
            default: Union[str, int, float] = None
    ) -> None:
        """Create a new ``DbColumn``."""

        self.column_name = column_name
        self.data_type = data_type
        self.dataclass_mapping = dataclass_mapping
        self.primary_key = primary_key
        self.not_null = not_null
        self.default = default

        if dataclass_mapping is None:
            self.dataclass_mapping = lambda i: i.__getattribute__[column_name]

    def __eq__(self, other):
        return True if all([
            isinstance(other, DbColumn),
            self.column_name == other.column_name,
            self.data_type == other.data_type
        ]) else False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(self.column_name + self.data_type.sql_text)

    def __str__(self):
        return f"<{self.column_name} - {self.data_type}>"

    def __repr__(self):
        return self.__str__()

    def get_query_rep(self) -> str:
        """Get the sql syntax conform rep of this column."""

        query_rep: str = f"{self.column_name} {self.data_type.sql_text}"
        query_rep += f' PRIMARY KEY,' if self.primary_key else ''
        query_rep += f' NOT NULL,' if self.not_null else ''
        query_rep += f' DEFAULT ' if self.default else ''
        query_rep += f'\'{self.default}\',' if self.default and isinstance(self.default, str) else ''
        query_rep += f'{self.default},' if self.default and not isinstance(self.default, str) else ''

        # Remove suffix ','
        if query_rep[-1] == ',':
            query_rep = query_rep[:-1]

        return query_rep


def get_column_names(db_columns: List[DbColumn]):
    """Get list of column names from list of columns."""

    return [col.column_name for col in db_columns]


def get_columns_from_dataclass(data_class: dataclass, ignore_fields: List[str] = None):
    """Get the column representation of a dataclass."""

    columns: List[DbColumn] = []

    for key, value in data_class.__annotations__.items():

        if ignore_fields is not None and key in ignore_fields:
            continue

        column_data_type: DbDataType = COLUMN_DATA_TYPES.get(value)

        if column_data_type is None:
            raise KeyError("The specified type key is unknown!")

        columns.append(DbColumn(
            column_name=key.lower(),
            data_type=column_data_type,
            dataclass_mapping=lambda i: i.__getattribute__(key)
        ))

    return columns
