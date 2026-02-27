import os

from typing import Any

from ._files import generate_structure, create_templ_file
from ._files import append_content, has_content, PathLike
from ._utils import _to_snake_case, _generate_secret_key, _create_subdir


def create_mvc_structure(app_name: str, orm: str = None) -> None:
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
        create_templ_file(app_name, path_name, init_file)

    _create_subdir(app_name, 'templates')
    create_templ_file(app_name, 'templates', 'base.html-tpl')


def create_blueprint_structure(app_name: str, orm: str = None) -> None:
    app_name = _to_snake_case(string=app_name)
    os.mkdir(app_name)
    path = os.path.join('', 'templates', 'app_template')

    generate_structure(app_name, path, os.path.join(''), **{
        'secret_key': _generate_secret_key(),
        'app_type': 'blueprint',
        'orm': orm
    })


def create_form(app_name: str, path: PathLike, dest: str, filename: str, **context: Any):
    template: str = 'forms/base.py-tpl'
    overwrite: str = 'forms/overwrite.py-tpl'

    if os.path.exists(path) and has_content(path):
        filename = filename if '.py' in filename else f'{filename}.py'
        return append_content(app_name, overwrite, dest, filename, **context)

    return create_templ_file(app_name, dest, template, filename, **context)


def create_model(
    app_name: str, orm: str, path: PathLike, dest: str, filename: str, **context: Any
):
    template: str = f'models/{orm}/model.py-tpl'
    overwrite: str = f'models/{orm}/append.py-tpl'
    context.update({ 'orm': orm })

    if os.path.exists(path) and has_content(path):
        filename = filename if '.py' in filename else f'{filename}.py'
        return append_content(app_name, overwrite, dest, filename, **context)

    return create_templ_file(app_name, dest, template, filename, **context)