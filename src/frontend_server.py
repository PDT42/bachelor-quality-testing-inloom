"""
:Author: Paul Erlenwein
:Since: 2021/02/04

This is a server for the angular frontend.
"""

import os

from flask import Flask, render_template


def serve_frontend(angular_root: str = os.path.abspath('../frontend/dist/frontend')):
    """Serve the frontend."""

    app = Flask(
        import_name=__name__,
        template_folder=angular_root,
        static_folder=angular_root,
        static_url_path=''
    )

    @app.route('/', methods=['GET'])
    def index():
        # noinspection PyUnresolvedReferences
        return render_template('index.html')

    app.run('localhost', port=4200, debug=False)


if __name__ == '__main__':
    serve_frontend()
