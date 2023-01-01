import flask

from . import db_commands

all = {
    "migrate-db": db_commands.migrate,
    "purge-db": db_commands.purge,
}

def register_commands(app: flask.Flask):
    for name, func in all.items():
        command_builder = app.cli.command(name)
        command_builder(func)
