import os
import sys

from pathlib import Path

from ._jinja import render_string


EXTENSION_DIR = Path(__file__).resolve().parent


def _create_subdir(app_name: str, *paths: str) -> None:
    path = os.path.join(app_name, *paths)
    os.mkdir(path)


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


def _make_app_files(app_name: str) -> None:
    template_files = _get_dir_template_files('templates/app_files')
    app_files = [file.replace('.py-tpl', '.py') for file in template_files]

    template_files_path = [
        os.path.join(app_name, file) for file in template_files
    ]
    app_files_path = [os.path.join(app_name, file) for file in app_files]

    for file_path in template_files_path:
        with open(file_path, mode='r') as tmpl:
            for app_file in app_files_path:
                with open(app_file, mode='w') as file:
                    file.writelines(tmpl.read())


def _create_mvc_app_structure(app_name: str) -> None:
    paths = ['blueprints', 'cli', 'forms', 'models']
    init_file = '__init__.py-tpl'

    os.mkdir(app_name)

    for path_name in paths:
        _create_subdir(app_name, path_name)
        _create_template_file(app_name, init_file, path_name, '__init__.py')

    html_file = 'base.html.jinja'
    _create_subdir(app_name, 'templates')
    _create_template_file(app_name, 'base.html-tpl', 'templates', html_file)


def _generate_app(name: str, app_type: str) -> None:
    if app_type == 'blueprint':
        pass

    _create_mvc_app_structure(app_name=name)