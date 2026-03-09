import os
import pytest

from click.testing import CliRunner

from flask_generate.generators import create_blueprint_structure, create_mvc_structure


@pytest.fixture
def app():
    pass


def test_generate_blueprint_app():
    runner = CliRunner()

    with runner.isolated_filesystem():
        app_name = create_blueprint_structure('app', 'sqlalchemy')
        app_dir = os.listdir(app_name)
        settings_dir = os.listdir(os.path.join(app_name, 'settings'))

        assert app_name == 'app'
        assert 'settings' in app_dir
        assert '__init__.py' in app_dir
        assert 'extensions.py' in app_dir
        assert 'factory.py' in app_dir
        assert 'utils.py' in app_dir
        assert 'wsgi.py' in app_dir
        assert 'base.py' in settings_dir
        assert 'dev.py' in settings_dir
        assert 'prod.py' in settings_dir


def test_generate_mvc_app():
    runner = CliRunner()

    with runner.isolated_filesystem():
        app_name, paths = create_mvc_structure('app', 'sqlalchemy')

        assert app_name == 'app'
        assert 'blueprints' in paths
        assert 'cli' in paths
        assert 'forms' in paths
        assert 'models' in paths
        assert 'tasks' in paths