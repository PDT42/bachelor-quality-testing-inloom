"""
:Author: Paul Erlenwein
:Since: 2020/11/20

This is the module for the ``TDManager``.
"""

from typing import Any, List, Mapping

from data_types.evaluation import Evaluation, EvaluationType
from data_types.testdataset import TestDataSet
from db_connection.db_column import DbColumn
from db_connection.db_connection import DbConnection, SqliteConnection
from db_connection.db_data_types import VARCHAR
from db_connection.db_table import DbTable
from db_connection.filter import Filter, FilterOperation
from db_connection.query import CREATEQuery, INSERTQuery, Query, SELECTQuery, UPDATEQuery
from managers.evaluation_manager import EvalManager


class TDManager:
    """This is the ``TDManager``."""

    # Make this a Singleton
    # ~~~~~~~~~~~~~~~~~~~~~
    _instance: 'TDManager' = None

    @staticmethod
    def get():
        """Get the _instance of this singleton."""
        if not TDManager._instance:
            TDManager._instance = TDManager()
        return TDManager._instance

    # ~~~~~~~~~~~~~~~~~~~~~

    # Constants
    STUDENT_MODEL_COL: DbColumn = DbColumn('student_model_id', VARCHAR(), primary_key=True)

    # Variables
    db_connection: DbConnection
    test_data_set_table: DbTable
    test_data_set_table_columns: List[DbColumn]

    def __init__(self):
        """Create a new ``TDManager``."""

        self.db_connection = SqliteConnection.get()
        self._init_database_table()

        self.eval_manager = EvalManager.get()

    def get_all_test_data_sets(self) -> List[TestDataSet]:
        """Get all TestDataSets to which the filters apply."""

        query: Query = SELECTQuery(self.test_data_set_table)
        results: List[Mapping[str, Any]] = self.db_connection.execute(query)

        test_data_sets: List[TestDataSet] = [TestDataSet(**item) for item in results]

        for tds in test_data_sets:
            if tds.auto_eval_id is not None:
                tds.auto_eval = self.eval_manager.get_one_by_id(tds.auto_eval_id)
            elif tds.man_eval_id is not None:
                tds.man_eval = self.eval_manager.get_one_by_id(tds.man_eval_id)

        return test_data_sets

    def insert_test_data_sets(self, test_data_sets: List[TestDataSet]):
        """Insert a list of ``TestDataSets`` into the database."""

        query: Query = INSERTQuery(self.test_data_set_table, test_data_sets)
        self.db_connection.execute(query)

        for test_data_set in test_data_sets:
            evaluations: List[Evaluation] = []
            if test_data_set.auto_eval is not None:
                evaluations.append(test_data_set.auto_eval)
            if test_data_set.man_eval is not None:
                evaluations.append(test_data_set.man_eval)

            if len(evaluations) > 0:
                self.eval_manager.insert_evaluations(evaluations)

    def update_test_data_set(self, test_data_set: TestDataSet):
        """Update a TDS in the database."""

        # Check if the test_data_set exists
        query: Query = UPDATEQuery(self.test_data_set_table, test_data_set) \
            .where(self._create_student_model_filter(test_data_set.student_model_id))
        self.db_connection.execute(query)

    def update_insert_test_data_set(self, test_data_set: TestDataSet):
        """Update a TestDataSet in the database, if it does not exist, add it."""

        query: Query = SELECTQuery(self.test_data_set_table, [self.STUDENT_MODEL_COL]) \
            .where(self._create_student_model_filter(test_data_set.student_model_id))
        results: List[Mapping[str, Any]] = self.db_connection.execute(query)

        # The TDS already exists -> update it
        if len(results) == 1:
            self.update_test_data_set(test_data_set)
        elif len(results) > 1:
            raise KeyError('CONSTRAINT ERROR: There was a duplication of TestDataSets!')
        else:
            self.insert_test_data_sets([test_data_set])

    def register_evaluation(
            self, evaluation: Evaluation,
            meta_model_type: str,
            mcs_identifier: str,
            mcs_version: str
    ) -> None:
        """Register an Evaluation in the database."""

        # Getting all test data sets from the database where the
        # 'student_model_id' equals that of the 'evaluation' supplied.
        query: Query = SELECTQuery(self.test_data_set_table) \
            .where(self._create_student_model_filter(evaluation.student_model_id))
        results: List[Mapping[str, Any]] = self.db_connection.execute(query)
        test_data_sets: List[TestDataSet] = [TestDataSet(**item) for item in results]

        # Check if the evaluation already exists - else store it in the database
        if self.eval_manager.get_one_that_equals(evaluation) is not None:
            raise KeyError('CONSTRAINT ERROR: An Evaluation like that already exists in the database!')
        self.eval_manager.insert_evaluations([evaluation])

        # There should never be more than one TD with the same SM_ID
        if len(test_data_sets) > 1:
            raise KeyError('CONSTRAINT ERROR: There was a duplication of TestDataSets!')

        # No TestDataSet with the SM_ID was
        # found and one needs to be created
        elif len(test_data_sets) < 1:

            # Creating a new TestDataSet
            test_data_set: TestDataSet = TestDataSet(
                expert_model_id=evaluation.expert_model_id,
                student_model_id=evaluation.student_model_id,
                meta_model_type=meta_model_type,
                mcs_identifier=mcs_identifier,
                mcs_version=mcs_version
            )

        # There is exactly one TDS with the correct SM_ID in the database
        else:
            test_data_set: TestDataSet = test_data_sets[0]

        # Checking what kind of evaluation we are registering
        if evaluation.type is EvaluationType.AUTOMATIC:
            test_data_set.auto_eval_id = evaluation.evaluation_id
            test_data_set.auto_eval = evaluation
        elif evaluation.type is EvaluationType.MANUAL:
            test_data_set.man_eval_id = evaluation.evaluation_id
            test_data_set.man_eval = evaluation
        else:
            raise SystemError("ILLEGAL STATE: There are only auto- and manEvals!")

        self.update_insert_test_data_set(test_data_set)

    def _init_database_table(self):
        """Initialize the table required for storing
        ``TestDataSets`` in the database.
        """

        self.test_data_set_table_columns = [
            DbColumn('expert_model_id', VARCHAR()),
            self.STUDENT_MODEL_COL,
            DbColumn('meta_model_type', VARCHAR()),
            DbColumn('mcs_identifier', VARCHAR()),
            DbColumn('mcs_version', VARCHAR()),
            DbColumn('auto_eval_id', VARCHAR()),
            DbColumn('man_eval_id', VARCHAR())
        ]
        self.test_data_set_table = DbTable(
            'inloom_quality_test_data_sets',
            columns=self.test_data_set_table_columns)
        self.db_connection.execute(CREATEQuery(self.test_data_set_table))

    def _create_student_model_filter(self, value: str) -> Filter:
        """Create a Filter for the student_model_id."""

        return Filter(
            column=self.STUDENT_MODEL_COL,
            operation=FilterOperation.EQUALS,
            value=value)
