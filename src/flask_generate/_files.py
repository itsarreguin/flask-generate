import os

from typing import Any
from pathlib import Path

from ._jinja import render_string
from ._utils import _create_subdir, _generate_secret_key
from ._utils import _get_file_extension


EXTENSION_DIR = Path(__file__).resolve().parent


def _create_template_file(app_name: str, template: str, folder: str, file_name: str) -> None:
    template_path = os.path.join(EXTENSION_DIR, 'templates', template)
    new_file_path = os.path.join(app_name, folder, file_name)

    with open(template_path, mode='r', encoding='utf-8') as tmpl:
        template_content = tmpl.read()

    content = render_string(template_content, app_name=app_name)
    with open(new_file_path, mode='w', encoding='utf-8') as file:
        file.write(content)


def _get_dir_template_files(*paths: str) -> list[str]:
    template_folder_path = os.path.join(EXTENSION_DIR, *paths)
    return os.listdir(template_folder_path)


def _make_initial_files(app_name: str, path: str, dest: str, **context: Any) -> None:
    for root, dirs, files in os.walk(os.path.join(EXTENSION_DIR, path)):
        for file in files:
            extension, new_extension = _get_file_extension(file=file)

            file_path = os.path.join(root, file)
            with open(file_path, encoding='utf-8') as template_file:
                template_content = template_file.read()

            context.update({ 'app_name': app_name })
            template_string = render_string(template_content, **context)

            new_file = file.replace(extension, new_extension)
            new_file_path = os.path.join(app_name, dest, new_file)
            with open(new_file_path, mode='w', encoding='utf-8') as file:
                file.write(template_string)


def _make_app_root_files(app_name: str) -> None:
    path = os.path.join('', 'templates', 'app_files')
    dest = os.path.join('')
    _make_initial_files(app_name, path, dest)


def _make_settings_files(app_name: str, app_type: str, orm: str) -> None:
    _create_subdir(app_name, 'settings')
    templates_path = os.path.join('', 'templates', 'settings')
    dest_path = os.path.join('', 'settings')

    _make_initial_files(app_name, templates_path, dest_path, **{
            'secret_key': _generate_secret_key(),
            'app_type': app_type,
            'orm': orm
        }
    )


def _make_project_root_files():
    pass


def create_mvc_app_structure(app_name: str, orm: str = None) -> None:
    paths = ['blueprints', 'cli', 'forms', 'models', 'tasks']
    init_file = '__init__.py-tpl'

    os.mkdir(app_name)
    _make_app_root_files(app_name)
    _make_settings_files(app_name, app_type='mvc', orm=orm)

    for path_name in paths:
        _create_subdir(app_name, path_name)
        _create_template_file(app_name, init_file, path_name, '__init__.py')

    html_file = 'base.html.jinja'
    _create_subdir(app_name, 'templates')
    _create_template_file(app_name, 'base.html-tpl', 'templates', html_file)


def create_blueprint_app_structure(app_name: str, orm: str = None) -> None:
    os.mkdir(app_name)
    _make_app_root_files(app_name)
    _make_settings_files(app_name, app_type='blueprint', orm=orm)