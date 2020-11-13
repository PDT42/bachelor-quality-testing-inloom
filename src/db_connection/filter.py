"""
:Author: Paul Erlenwein
:Since: 2020/11/20

This is the module that contains the ``Filter``.
"""

from dataclasses import dataclass

from db_connection.db_column import DbColumn


@dataclass
class Filter:
    """This is the representation of a db ``Query`` filter."""

    filter_attribute: DbColumn