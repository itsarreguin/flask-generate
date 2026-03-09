import pytest

from flask import Flask
from flask_generate import Generate


@pytest.fixture
def app():
    return Flask(__name__)


def test_init_twice(app: Flask):
    generate = Generate(app)
    match_message = 'A Generate extension is already initialized on this application.'

    with pytest.raises(RuntimeError, match=match_message):
        generate.init_app(app)


def test_mvc_sqla_settings(app: Flask):
    app.config.update({
        'GENERATE_APP_TYPE': 'mvc',
        'GENERATE_ORM': 'sqlalchemy'
    })
    assert app.config['GENERATE_APP_TYPE'] != 'blueprint'
    assert app.config['GENERATE_ORM'] != 'peewee'


def test_blueprint_app_settings(app: Flask):
    app.config.update({
        'GENERATE_APP_TYPE': 'blueprint',
        'GENERATE_ORM': 'peewee'
    })
    assert app.config['GENERATE_APP_TYPE'] != 'mvc'
    assert app.config['GENERATE_ORM'] != 'sqlalchemy'