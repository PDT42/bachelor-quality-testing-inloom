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

    length: int = 255

    sql_text = "VARCHAR"

    def __init__(self, length=255):
        self.length = length
        super(VARCHAR, self).__init__(self.name)


class INTEGER(DbDataType):
    """This represents a Integer-Type."""

    sql_text = "INTEGER"

    def __init__(self):
        super(INTEGER, self).__init__(self.sql_text)


class DBKEY(DbDataType):
    """This represents any kind of database key."""

    sql_text = "INTEGER"

    def __init__(self):
        super(DBKEY, self).__init__(self.sql_text)
