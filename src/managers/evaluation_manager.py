"""
:Author: Paul Erlenwein
:Since: 2020/11/20

This is the module for the ``EvalManager``.
"""
from typing import Any, Dict, List, Mapping, MutableMapping

from data_types.evaluation import AutoEval, Evaluation, ManEval
from db_connection.db_column import DbColumn
from db_connection.db_connection import DbConnection, SqliteConnection
from db_connection.db_data_types import FLOAT, INTEGER, VARCHAR
from db_connection.db_table import DbTable
from db_connection.filter import Filter, FilterOperation
from db_connection.query import CREATEQuery, INSERTQuery, Query, SELECTQuery
from managers.results_manager import ResultManager


class EvalManager:
    """This is the ``EvalManager``."""

    # Constants
    EVAL_TABLE_NAME: str = 'evaluations'
    MAN_EVAL_TABLE_NAME: str = 'manual_evaluations'
    AUTO_EVAL_TABLE_NAME: str = 'automatic_evaluations'

    TEST_DATA_SET_ID_COLUMN: DbColumn = DbColumn('test_data_set_id', VARCHAR(), not_null=True)
    EXERCISE_ID_COLUMN: DbColumn = DbColumn('exercise_id', VARCHAR(), not_null=True)
    EXPERT_SOLUTION_ID_COLUMN: DbColumn = DbColumn('expert_solution_id', VARCHAR(), not_null=True)
    STUDENT_ID_COLUMN: DbColumn = DbColumn('student_id', VARCHAR(), not_null=True)
    EVAL_TYPE_COLUMN: DbColumn = DbColumn('evaluation_type', VARCHAR(), not_null=True)
    META_MODEL_TYPE_COLUMN: DbColumn = DbColumn('meta_model_type', VARCHAR())
    FILE_PATH_COLUMN: DbColumn = DbColumn('file_path', VARCHAR())
    TOTAL_POINTS_COLUMN: DbColumn = DbColumn('total_points', FLOAT(), not_null=True)
    MAX_POINTS_COLUMN: DbColumn = DbColumn('max_points', FLOAT(), not_null=True)
    EVALUATION_ID_COLUMN: DbColumn = DbColumn('evaluation_id', VARCHAR(), primary_key=True)
    CREATED_TIME_COLUMN: DbColumn = DbColumn('created_time', INTEGER(), not_null=True)

    # Variables
    db_connection: DbConnection
    eval_table: DbTable
    eval_tables: MutableMapping[type, DbTable]

    results_manager: ResultManager

    def __init__(self):
        """Create a new ``EvalManager``."""

        self.db_connection = SqliteConnection.get()

        self.results_manager = ResultManager()

    def insert_evaluation(self, evaluation):
        """Insert one ``Evaluation`` into the database."""

        # Inserting the Evaluation of this eval into the database
        parent_eval: Evaluation = Evaluation.from_child(evaluation)
        query: Query = INSERTQuery(db_table=self.eval_table, values=parent_eval)
        self.db_connection.execute(query)

        # Inserting the typed Eval of this eval into the database
        query: Query = INSERTQuery(db_table=self.eval_tables.get(type(evaluation)), values=evaluation)
        self.db_connection.execute(query)

        if len(evaluation.results) > 0:
            self.results_manager.insert_results(evaluation.results)

    def insert_evaluations(self, evaluations: List[Evaluation]):
        """Insert a list of ``Evaluations`` into the database."""

        # Insert ``Evaluations``
        _evaluations: List[Evaluation] = [
            Evaluation.from_child(new_eval) for new_eval in evaluations
        ]
        query: Query = INSERTQuery(
            db_table=self.eval_table,
            values=_evaluations)
        self.db_connection.execute(query)

        # Insert child - either AutoEval or ManEval
        query: Query = INSERTQuery(
            db_table=self.eval_tables.get(type(evaluations[0])),
            values=evaluations)
        self.db_connection.execute(query)

        # For the new evaluations, check whether any results
        # need to be entered into the database and enter them
        # if necessary.
        for evaluation in evaluations:

            if len(evaluation.results) > 0:
                self.results_manager.insert_results(evaluation.results)

    def _get_one(self, evaluation: Evaluation):
        """Common get one functionality."""

        equals: FilterOperation = FilterOperation.EQUALS

        eval_class: type = {'A': AutoEval, 'M': ManEval}.get(evaluation.evaluation_type, None)
        if not eval_class:
            raise ValueError("UNKNOWN VALUE: The supplied evaluation_type is unknown!")

        eval_table: DbTable = self.eval_tables.get(eval_class, None)
        query: Query = SELECTQuery(eval_table) \
            .where(Filter(self.EVALUATION_ID_COLUMN, equals, evaluation.evaluation_id))
        db_results: List[Mapping[str, Any]] = self.db_connection.execute(query)

        if not db_results:
            return None
        elif isinstance(db_results, list) and len(db_results) > 1:
            raise ValueError(f"CONSTRAINT ERROR: This {eval_class.__name__} was duplicated!")

        result_eval_dict: MutableMapping = {}
        result_eval_dict.update(db_results[0])
        result_eval_dict.update(evaluation.__dict__)

        return eval_class(**result_eval_dict)

    def get_one_by_id(self, evaluation_id: str):
        """Get an ``Evaluation`` by its ``evaluation_id``."""

        query: Query = SELECTQuery(self.eval_table) \
            .where(Filter(self.EVALUATION_ID_COLUMN, FilterOperation.EQUALS, evaluation_id))
        db_results: List[Mapping[str, Any]] = self.db_connection.execute(query)

        if not db_results:
            return None
        elif isinstance(db_results, list) and len(db_results) > 1:
            raise ValueError(f"CONSTRAINT ERROR: This Evaluation was duplicated!")

        return self._get_one(Evaluation(**db_results[0]))

    def _get_all_evaluations(self, query: Query, required_type: type = None):
        """Common get all functionality."""

        id_column: str = self.EVALUATION_ID_COLUMN.column_name
        equals: FilterOperation = FilterOperation.EQUALS

        if required_type == AutoEval:
            query.where(Filter(self.EVAL_TYPE_COLUMN, equals, 'A'))
        if required_type == ManEval:
            query.where(Filter(self.EVAL_TYPE_COLUMN, equals, 'M'))

        # Executing the query
        db_results = self.db_connection.execute(query)

        # Processing the result -> {eval_id: Evaluation, ..}
        eval_dicts: Dict[str, Mapping[str, Any]] = {}
        for item in db_results:
            eval_id = item.pop(id_column)
            eval_dicts[eval_id] = item

        # Getting additional data and collecting evaluations
        evaluations: List[Evaluation] = []

        if required_type in [None, AutoEval]:
            query: Query = SELECTQuery(self.eval_tables.get(AutoEval))
            auto_eval_dicts: List[Mapping[str, Any]] = self.db_connection.execute(query)
            evaluations.extend([
                AutoEval(**item, **eval_dicts[item[id_column]])
                for item in auto_eval_dicts if item[id_column] in eval_dicts
            ])

        if required_type in [None, ManEval]:
            query: Query = SELECTQuery(self.eval_tables.get(ManEval))
            man_eval_dicts: List[Mapping[str, Any]] = self.db_connection.execute(query)
            evaluations.extend([
                ManEval(**item, **eval_dicts[item[id_column]])
                for item in man_eval_dicts if item[id_column] in eval_dicts
            ])

        # Appending results to the evaluation
        for evaluation in evaluations:
            evaluation.results = ResultManager.get() \
                .get_all_for(evaluation.evaluation_id)

        return evaluations

    def get_all_evaluations(self, required_type: type = None):
        """Get all ``Evaluations`` available  in the database."""

        # Creating a query to get all required Evals
        query: Query = SELECTQuery(self.eval_table)

        return self._get_all_evaluations(query, required_type)

    def get_all_of(self, test_data_set_id: str, required_type: type = None):
        """Get all ``Evaluations`` with ``test_data_set_id``."""

        # Creating a query to get all required Evals
        query: Query = SELECTQuery(self.eval_table)
        query = query.where(Filter(self.TEST_DATA_SET_ID_COLUMN, FilterOperation.EQUALS, test_data_set_id))

        return self._get_all_evaluations(query, required_type)

    def _init_database_tables(self):
        """Initialize the table required for storing
        ``TestDataSets`` in the database.
        """

        # Create Table for Evaluations
        eval_table_columns: List[DbColumn] = [
            self.TEST_DATA_SET_ID_COLUMN,
            self.EXERCISE_ID_COLUMN,
            self.EXPERT_SOLUTION_ID_COLUMN,
            self.STUDENT_ID_COLUMN,
            self.EVAL_TYPE_COLUMN,
            self.META_MODEL_TYPE_COLUMN,
            self.FILE_PATH_COLUMN,
            self.TOTAL_POINTS_COLUMN,
            self.MAX_POINTS_COLUMN,
            self.EVALUATION_ID_COLUMN,
            self.CREATED_TIME_COLUMN
        ]

        self.eval_table = DbTable(
            table_name=self.EVAL_TABLE_NAME,
            columns=eval_table_columns)
        self.db_connection.execute(CREATEQuery(self.eval_table))

        # Init type specific table registry
        self.eval_tables = {}

        # Create table for AutoEvals
        auto_eval_table_columns: List[DbColumn] = [
            DbColumn('mcs_identifier', VARCHAR()),
            DbColumn('mcs_version', VARCHAR()),
            self.EVALUATION_ID_COLUMN
        ]

        self.eval_tables[AutoEval] = auto_eval_table = DbTable(
            table_name=self.AUTO_EVAL_TABLE_NAME,
            columns=auto_eval_table_columns)
        self.db_connection.execute(CREATEQuery(auto_eval_table))

        # Create table for ManEvals
        man_eval_table_columns: List[DbColumn] = [
            DbColumn('evaluator_id', VARCHAR()),
            self.EVALUATION_ID_COLUMN
        ]

        self.eval_tables[ManEval] = man_eval_table = DbTable(
            table_name=self.MAN_EVAL_TABLE_NAME,
            columns=man_eval_table_columns)
        self.db_connection.execute(CREATEQuery(man_eval_table))
