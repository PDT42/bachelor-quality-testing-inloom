"""
:Author: Paul Erlenwein
:Since: 2020/12/08

This is the module for the ``EvalServer``.
"""

import os

from flask import Flask, make_response, request
from werkzeug.utils import secure_filename

from managers.evaluation_manager import EvalManager
from managers.testdata_manager import TDManager
from servers import AUTO_EVAL_PATH
from xml_adapter import XMLAdapter, XMLAdapterResult


class EvalServer:
    """This is the ``EvalServer``."""

    # Make this a Singleton
    # ~~~~~~~~~~~~~~~~~~~~~
    _instance: 'EvalServer' = None

    @staticmethod
    def get():
        """Get the instance of this singleton."""

        if not EvalServer._instance:
            EvalServer._instance = EvalServer()
        return EvalServer._instance

    # ~~~~~~~~~~~~~~~~~~~~~

    # Variables
    _initialized: bool = False

    td_manager: TDManager = None
    eval_manager: EvalManager = None

    def __init__(self):
        """Create a new ``EvalServer``."""

        self.td_manager = TDManager.get()
        self.eval_manager = EvalManager.get()

    @staticmethod
    def register_routes(app: Flask):
        """Register the routes this server provides in the ``app``."""

        if EvalServer.get()._initialized:
            raise SystemError()

        app.add_url_rule(
            rule='/eval/auto/upload',
            endpoint='upload-auto-eval',
            view_func=EvalServer._post_upload_auto_eval,
            methods=['POST']
        )

        print("Initialized EvalServer ...")
        EvalServer.get()._initialized = True

    @staticmethod
    def _post_upload_auto_eval():
        """Process POST calls to [/eval/auto/upload]"""

        auto_eval_file = request.files['file']
        auto_eval_file_name: str = auto_eval_file.filename

        response = make_response()
        response.headers.add('Access-Control-Allow-Origin', '*')

        if auto_eval_file_name == '' or auto_eval_file_name.split('.')[-1] != 'xml':
            response.headers.add('status', '400')
            return response

        # TODO: Identify evaluation file ...

        auto_eval_file_name = secure_filename(auto_eval_file_name)
        auto_eval_file_path = os.path.join(AUTO_EVAL_PATH, auto_eval_file_name)
        auto_eval_file.save(auto_eval_file_path)

        xml_adapter_res: XMLAdapterResult = XMLAdapter.eval_from_xml(auto_eval_file_path)
        EvalServer.get().td_manager.register_evaluation(
            evaluation=xml_adapter_res.evaluation,
            meta_model_type=xml_adapter_res.meta_model_type,
            mcs_identifier=xml_adapter_res.mcs_id,
            mcs_version=xml_adapter_res.mcs_version)

        return response

    @staticmethod
    def _get_eval_by_id():
        """Handle """
