import json
from flask import Flask
from . import commands

def create_app():
    app = Flask(__name__)

    app.config.from_file("../config.json", load=json.load)

    commands.register_commands(app)

    from notes_app.data import databaseHelper
    databaseHelper.init(app)

    from .blueprints import auth, notes, errors
    auth.register(app)
    notes.register(app)
    
    app.register_error_handler(404, errors.page_not_found)
    app.register_error_handler(500, errors.internal_server_error)

    return app

