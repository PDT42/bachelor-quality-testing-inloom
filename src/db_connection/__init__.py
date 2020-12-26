"""
:Author: Paul Erlenwein
:Since: 2020/11/20

This is the db_connection package.
"""
from datetime import datetime
from enum import Enum
from typing import Any
from uuid import UUID

from data_types.result_category import ResultCategory

DB_PATH: str = "../res/inloomqt-res/database.db"
VERBOSITY = 5


def sqlite_convert(item: Any) -> str:
    """Make an item insertable."""

    # Converting Primitives
    if isinstance(item, str):
        return f"\"{item}\""
    elif item is None:
        return "null"
    elif isinstance(item, bool):
        return str(int(item))
    elif isinstance(item, datetime):
        return str(int(item.timestamp()))

    # Converting complex types
    elif isinstance(item, UUID):
        return f"\"{str(item)}\""

    # Converting Enums
    elif isinstance(item, ResultCategory):
        return f"\"{item.value}\""
    elif isinstance(item, Enum):
        return sqlite_convert(item.value)

    # Hoping for the best
    else:
        return str(item)
