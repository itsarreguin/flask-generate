import pytest

from pathlib import Path

from click.testing import CliRunner

from flask import Flask
from flask_generate import Generate
from flask_generate.main import app as app_command
from flask_generate.cli import generate


@pytest.fixture
def app():
    app = Flask(__name__)
    Generate(app)
    app.config['GENERATE_APP_TYPE'] = 'mvc'
    app.config['GENERATE_ORM'] = 'sqlalchemy'
    app.config['APP_DIR'] = Path(__file__).resolve().parent.parent
    return app


@pytest.fixture
def runner(app: Flask):
    return app.test_cli_runner()


def test_create_mvc_app():
    runner = CliRunner()

    with runner.isolated_filesystem():
        result = runner.invoke(
            app_command,
            ['app', '--type', 'mvc', '--orm', 'sqlalchemy']
        )
        assert not result.exception
        assert result.exit_code == 0


def test_create_blueprint_app():
    runner = CliRunner()

    with runner.isolated_filesystem():
        result = runner.invoke(
            app_command,
            ['app', '--type', 'blueprint', '--orm', 'sqlalchemy']
        )
        assert not result.exception
        assert result.exit_code == 0


def test_registered_commands(app: Flask, runner: CliRunner):
    commands = generate.list_commands(app)

    assert 'blueprint' in commands
    assert 'form' in commands
    assert 'model' in commands
    assert 'scaffold' in commands