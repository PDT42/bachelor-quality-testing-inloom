"""
:Author: Paul Erlenwein
:Since: 2020/12/08

This is the servers package. It contains all the servers used
to provide stuff to the frontend of the software.
"""
from typing import Any, List, Mapping

from flask import make_response, Response

AUTO_EVAL_PATH: str = "../res/inloomqt-res/eval/auto/"
AUTO_EVAL_FORMATS: List[str] = ['xml']

MAN_EVAL_PATH: str = "../res/inloomqt-res/eval/man"
MAN_EVAL_FORMATS: List[str] = ['jpg', 'pdf', 'png']

EXPERT_SOL_PATH: str = "../res/inloomqt-res/expert_solutions"
EXPERT_SOL_FORMATS: List[str] = ['xml']
