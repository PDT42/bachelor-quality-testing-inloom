"""
:Author: Paul Erlenwein
:Since: 2020/12/23

This is the module for the ``Evaluator``.
"""

from dataclasses import dataclass, field
from datetime import datetime
from uuid import uuid4


@dataclass
class Evaluator:
    """This is an ``Evaluator``."""

    first_name: str
    last_name: str
    created_time: int = field(default_factory=lambda: int(datetime.now().timestamp()))
    evaluator_id: str = field(default_factory=lambda: str(uuid4()))
