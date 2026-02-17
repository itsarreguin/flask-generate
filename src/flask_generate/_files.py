import os

from os import PathLike
from typing import Any

from ._jinja import render_string
from ._utils import _create_app_file, _create_subdir, _generate_secret_key
from ._utils import _extract_file_extension, EXTENSION_DIR


def _create_app_file(app_name: str, root: str, file: str, dest: str, **context: Any):
    extension, new_extension = _extract_file_extension(file=file)
    file_path = os.path.join(root, file)

    with open(file_path, encoding='utf-8') as template_file:
        template_content = template_file.read()

    context.update({ 'app_name': app_name.lower() })
    template_string = render_string(template_content, **context)

    new_file = file.replace(extension, new_extension)
    new_file_path = os.path.join(app_name, dest, new_file)

    with open(new_file_path, mode='w', encoding='utf-8') as file:
        file.write(template_string)


def _create_template_file(app: str, dest: str, template: str, **context: Any) -> None:
    template_path = os.path.join(EXTENSION_DIR, 'templates')
    return _create_app_file(app, template_path, template, dest, **context)


def _get_dir_template_files(*paths: str) -> list[str]:
    template_folder_path = os.path.join(EXTENSION_DIR, *paths)
    return os.listdir(template_folder_path)


def _generate_app_structure(
    app_name: str,
    app_type: str | None = 'mvc',
    orm: str | None = 'sqla',
    path: str | bytes | PathLike = None,
    dest: str | bytes | PathLike = None,
    **context: Any
) -> None:
    os.mkdir(app_name)

    for root, dirs, files in os.walk(os.path.join(EXTENSION_DIR, path)):
        for file in files:
            _create_app_file(app_name, root, file, dest, **context)
        if dirs:
            for dir_name in dirs:
                dir_path = os.path.join(EXTENSION_DIR, path, dir_name)
                templates_list = _get_dir_template_files(dir_path)
                app_dir = os.path.join(app_name)

                if dir_name not in os.listdir(app_dir):
                    _create_subdir(app_name, dir_name)

                context = {
                    'secret_key': _generate_secret_key(),
                    'app_type': app_type,
                    'orm': orm
                }
                root_dir = os.path.join(root, dir_name)
                dest = os.path.join(dir_name)

                for template in templates_list:
                    _create_app_file(app_name, root_dir, template, dest, **context)


def create_mvc_app_structure(app_name: str, orm: str = None) -> None:
    paths = ['blueprints', 'cli', 'forms', 'models', 'tasks']
    init_file = '__init__.py-tpl'
    path = os.path.join('', 'templates', 'app_template')

    _generate_app_structure(app_name, orm=orm, path=path, dest=os.path.join(''))

    for path_name in paths:
        _create_subdir(app_name, path_name)
        _create_template_file(app_name, path_name, init_file)

    _create_subdir(app_name, 'templates')
    _create_template_file(app_name, 'templates', 'base.html-tpl')


def create_blueprint_app_structure(app_name: str, orm: str = None) -> None:
    _generate_app_structure(
        app_name=app_name,
        app_type='blueprint',
        orm=orm,
        path=os.path.join('', 'templates', 'app_template'),
        dest=os.path.join('')
    )