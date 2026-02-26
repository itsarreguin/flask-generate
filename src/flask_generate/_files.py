import os

from os import PathLike
from typing import Any, TypeAlias

from ._jinja import render_string
from ._utils import _create_subdir, _generate_secret_key
from ._utils import _to_snake_case, _extract_file_extension
from ._utils import EXTENSION_DIR


PathType: TypeAlias = str | bytes | PathLike


def create_app_file(
    app_name: str, root: str, file: str, filename: str | None, dest: str, **context: Any
):
    extension, new_extension = _extract_file_extension(file=file)
    file_path = os.path.join(root, file)

    with open(file_path, encoding='utf-8') as template_file:
        template_content = template_file.read()

    context.update({ 'app_name': _to_snake_case(app_name) })
    template_string = render_string(template_content, **context)

    sanitized_file = file.replace(extension, new_extension)
    new_file = f'{filename}.{new_extension}' if filename is not None else ''
    new_filename = new_file if filename is not None else sanitized_file
    new_file_path = os.path.join(app_name, dest, new_filename)

    with open(new_file_path, mode='w', encoding='utf-8') as template:
        template.write(template_string)


def create_template_file(
    app: str, dest: str, template: str, filename: str | None = None, **context: Any
) -> None:
    template_path = os.path.join(EXTENSION_DIR, 'templates')
    return create_app_file(app, template_path, template, filename, dest, **context)


def get_dir_template_files(*paths: str) -> list[str]:
    template_folder_path = os.path.join(EXTENSION_DIR, *paths)
    return os.listdir(template_folder_path)


def generate_structure(app_name: str, path: PathType, dest: PathType, **context: Any) -> None:
    for root, dirs, files in os.walk(os.path.join(EXTENSION_DIR, path)):
        for file in files:
            create_app_file(app_name, root, file,  None, dest, **context)
        if dirs:
            for dir_name in dirs:
                dir_path = os.path.join(EXTENSION_DIR, path, dir_name)
                templates_list = get_dir_template_files(dir_path)
                app_dir = os.path.join(app_name)

                if dir_name not in os.listdir(app_dir):
                    _create_subdir(app_name, dir_name)

                root_dir = os.path.join(root, dir_name)
                dest = os.path.join(dir_name)

                for template in templates_list:
                    create_app_file(app_name, root_dir, template,  None, dest, **context)


def create_mvc_app_structure(app_name: str, orm: str = None) -> None:
    app_name = _to_snake_case(string=app_name)
    os.mkdir(app_name)
    paths = ['blueprints', 'cli', 'forms', 'models', 'tasks']
    init_file = '__init__.py-tpl'
    path = os.path.join('', 'templates', 'app_template')

    generate_structure(app_name, path, os.path.join(''), **{
        'secret_key': _generate_secret_key(),
        'app_type': 'mvc',
        'orm': orm
    })

    for path_name in paths:
        _create_subdir(app_name, path_name)
        create_template_file(app_name, path_name, init_file)

    _create_subdir(app_name, 'templates')
    create_template_file(app_name, 'templates', 'base.html-tpl')


def create_blueprint_app_structure(app_name: str, orm: str = None) -> None:
    app_name = _to_snake_case(string=app_name)
    os.mkdir(app_name)
    path = os.path.join('', 'templates', 'app_template')

    generate_structure(app_name, path, os.path.join(''), **{
        'secret_key': _generate_secret_key(),
        'app_type': 'blueprint',
        'orm': orm
    })