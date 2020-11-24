"""
:Author: Paul Erlenwein
:Since: 2020/11/20

This is the module that contains the ``DbDataTypes``.
"""

from dataclasses import dataclass


@dataclass
class DbDataType:
    """This is a data type."""

    sql_text: str


class VARCHAR(DbDataType):
    """This represents a Varchar-Type."""

    sql_text = "VARCHAR"

    def __init__(self):
        super(VARCHAR, self).__init__(self.sql_text)


class INTEGER(DbDataType):
    """This represents a Integer-Type."""

    sql_text = "INTEGER"

    def __init__(self):
        super(INTEGER, self).__init__(self.sql_text)


class FLOAT(DbDataType):
    """This represents a floating point number type."""

    sql_text = "NUMBER"

    def __init__(self):
        super(FLOAT, self).__init__(self.sql_text)
