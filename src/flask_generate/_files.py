import os

from typing import Any

from ._jinja import render_string
from ._utils import _create_app_file, _create_subdir
from ._utils import _generate_secret_key, _extract_file_extension
from ._utils import EXTENSION_DIR


def _create_template_file(app: str, dest: str, template: str, **context: Any) -> None:
    template_path = os.path.join(EXTENSION_DIR, 'templates')
    # new_file_path = os.path.join(dest, folder, file_name)

    # with open(template_path, mode='r', encoding='utf-8') as tmpl:
    #     template_content = tmpl.read()

    # content = render_string(template_content, app_name=app_name)
    # with open(new_file_path, mode='w', encoding='utf-8') as file:
    #     file.write(content)

    return _create_app_file(app, template_path, template, dest, **context)


def _get_dir_template_files(*paths: str) -> list[str]:
    template_folder_path = os.path.join(EXTENSION_DIR, *paths)
    return os.listdir(template_folder_path)


def _generate_app_structure(app_name: str, path: str, dest: str, **context: Any) -> None:
    for root, dirs, files in os.walk(os.path.join(EXTENSION_DIR, path)):
        for file in files:
            _create_app_file(app_name, root, file, dest, **context)
        if dirs:
            pass


def _make_settings_files(app_name: str, app_type: str, orm: str) -> None:
    _create_subdir(app_name, 'settings')
    templates_path = os.path.join('', 'templates', 'settings')
    dest_path = os.path.join('', 'settings')

    _generate_app_structure(app_name, templates_path, dest_path, **{
            'secret_key': _generate_secret_key(),
            'app_type': app_type,
            'orm': orm
        }
    )


def create_mvc_app_structure(app_name: str, orm: str = None) -> None:
    paths = ['blueprints', 'cli', 'forms', 'models', 'tasks']
    init_file = '__init__.py-tpl'

    os.mkdir(app_name)

    path = os.path.join('', 'templates', 'app_files')
    _generate_app_structure(app_name, path, os.path.join(''))

    _make_settings_files(app_name, app_type='mvc', orm=orm)

    for path_name in paths:
        _create_subdir(app_name, path_name)
        _create_template_file(app_name, path_name, init_file)

    _create_subdir(app_name, 'templates')
    _create_template_file(app_name, 'templates', 'base.html-tpl')


def create_blueprint_app_structure(app_name: str, orm: str = None) -> None:
    os.mkdir(app_name)
    _make_settings_files(app_name, app_type='blueprint', orm=orm)