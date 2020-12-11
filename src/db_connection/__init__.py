"""
:Author: Paul Erlenwein
:Since: 2020/11/20

This is the db_connection package.
"""

from typing import Any
from uuid import UUID

from data_types.evaluation import EvaluationType
from data_types.constraintresult import ConstraintResultCategory

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

    # Converting complex types
    elif isinstance(item, UUID):
        return f"\"{str(item)}\""

    # Converting Enums
    elif isinstance(item, ConstraintResultCategory):
        return f"\"{item.value}\""
    elif isinstance(item, EvaluationType):
        return f"\"{item.value}\""

    # Hoping for the best
    else:
        return str(item)
