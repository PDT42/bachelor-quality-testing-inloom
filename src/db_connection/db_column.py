"""
:Author: Paul Erlenwein
:Since: 2020/11/20

This is the module, that contains the ``DbColumn``.
"""

from dataclasses import dataclass

from src.db_connection.db_data_types import DbDataType


@dataclass
class DbColumn:
    """This is a ``DbColumn``."""

    name: str
    data_type: DbDataType
    primary_key: bool = False
