"""
:Author: Paul Erlenwein
:Since: 2020/11/20

This is the module for the ``ElementMatch``.
"""

from dataclasses import dataclass


@dataclass
class ExpertElement:
    """."""

    expert_element_label: str
    expert_element_type: str

    def __hash__(self):
        return hash(
            self.expert_element_label +
            self.expert_element_type)

    def __eq__(self, other):
        return True if all([
            isinstance(other, ExpertElement),
            self.expert_element_label == other.expert_element_label,
            self.expert_element_type == other.expert_element_type,
        ]) else False


@dataclass
class StudentElement:
    """."""

    student_element_label: str
    student_element_type: str

    def __hash__(self):
        return hash(
            self.student_element_label +
            self.student_element_type)

    def __eq__(self, other):
        return True if all([
            isinstance(other, StudentElement),
            self.student_element_label == other.student_element_label,
            self.student_element_type == other.student_element_type
        ]) else False


@dataclass
class TypeMatch:
    """."""

    expert_element_type: str
    student_element_type: str

    def __hash__(self):
        return hash(
            self.expert_element_type +
            self.student_element_type)

    def __eq__(self, other):
        return True if all([
            isinstance(other, TypeMatch),
            self.expert_element_type == other.expert_element_type,
            self.student_element_type == other.student_element_type
        ]) else False


@dataclass
class ElementMatch:
    """This is an ``ElementMatch``.

    An ElementMatch is what a MMU a minimum
    markable unit is called in this project.
    """

    expert_element_label: str
    expert_element_type: str
    student_element_label: str
    student_element_type: str

    def __hash__(self):
        return hash(
            self.expert_element_label +
            self.student_element_label +
            self.expert_element_type +
            self.student_element_type)

    def __eq__(self, other):
        return True if all([
            isinstance(other, ElementMatch),
            self.expert_element_label == other.expert_element_label,
            self.student_element_label == other.student_element_label,
            self.expert_element_type == other.expert_element_type,
            self.student_element_type == other.student_element_type
        ]) else False
