"""
:Author: Paul Erlenwein
:Since: 2020/12/11

This is the module for the ``ResultCategory`` enumeration.
"""

from enum import Enum


class ResultCategory(Enum):
    """These are the possible result categories."""

    MISSING = 'M'
    ERROR = 'E'
    WARNING = 'W'
    CORRECT = 'C'
    INFO = 'I'
