import flask
from flask.testing import FlaskCliRunner
import pytest

from notes_app import create_app


@pytest.fixture()
def app() -> flask.Flask:
    app = create_app()
    app.config.update({
        "TESTING": True,
        "MYSQL_DB": "flask_testing"
    })

    cli_runner = app.test_cli_runner()

    cli_runner.invoke(args="purge-db")
    cli_runner.invoke(args="migrate-db")

    yield app

    cli_runner.invoke(args="purge-db")
