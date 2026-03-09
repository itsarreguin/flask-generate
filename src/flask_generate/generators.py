import os

from typing import Any

from ._files import generate_structure, create_templ_file
from ._files import append_content, has_content, PathLike
from ._utils import _to_snake_case, _generate_secret_key, _create_subdir


def create_blueprint_structure(app_name: str, orm: str = None) -> str:
    app_name = _to_snake_case(string=app_name)
    os.mkdir(app_name)
    path = os.path.join('', 'templates', 'app_template')

    generate_structure(app_name, path, os.path.join(''), **{
        'secret_key': _generate_secret_key(),
        'app_type': 'blueprint',
        'orm': orm
    })

    _create_subdir(app_name, 'templates')
    create_templ_file(app_name, 'templates', 'base.html-tpl')

    return app_name


def create_mvc_structure(app_name: str, orm: str = None) -> list[str]:
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

    return [app_name, paths]


def generate_blueprint_pkg(name: str, app_name: str, template: str, **context: Any) -> None:
    template_root_path = os.path.join('', 'templates', template)
    name = _to_snake_case(name)
    os.mkdir(os.path.join(app_name, name))

    _create_subdir(app_name, name, 'templates')
    _create_subdir(app_name, name, 'templates', name)

    generate_structure(app_name, template_root_path, name, **context)


def create_form(app_name: str, path: PathLike, dest: str, filename: str, **context: Any):
    template: str = 'forms/form.py-tpl'
    overwrite: str = 'forms/base.py-tpl'

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


def blueprint_scaffold(attributes: list[str], **context: Any) -> None:
    app_name, _, _, orm = attributes
    bp_name: str = context.get('blueprint_name')

    generate_blueprint_pkg(
        name=bp_name,
        app_name=app_name,
        template=os.path.join('', 'scaffolding', 'blueprint'),
        **{ 'orm': orm, **context }
    )
    create_model(
        app_name=app_name,
        orm=orm,
        path=os.path.join(app_name, bp_name, 'models.py'),
        dest=bp_name,
        filename='models',
        **context
    )
    create_form(
        app_name=app_name,
        path=os.path.join(app_name, bp_name, 'forms.py'),
        dest=bp_name,
        filename='forms',
        **context
    )
    generate_structure(
        app_name=app_name,
        path=os.path.join('', 'templates', 'jinja_templates'),
        dest=os.path.join(bp_name, 'templates', bp_name),
        **context
    )


def mvc_scaffold(attributes: list[str], **context: Any) -> None:
    app_name, _, _, orm = attributes
    destination = context['blueprint_name']

    os.mkdir(os.path.join(app_name, 'templates', destination))
    create_model(
        app_name=app_name,
        orm=orm,
        path=os.path.join(app_name, 'models', f'{destination}.py'),
        dest='models',
        filename=destination,
        **context
    )
    create_form(
        app_name=app_name,
        path=os.path.join(app_name, 'forms', f'{destination}.py'),
        dest='forms',
        filename=destination,
        **context
    )
    generate_structure(
        app_name=app_name,
        path=os.path.join('', 'templates', 'jinja_templates'),
        dest=os.path.join('templates', destination),
        **context
    )
    create_templ_file(
        app=app_name,
        dest='blueprints',
        template=os.path.join('', 'scaffolding', 'blueprint.py-tpl'),
        filename=destination,
        **{ 'orm': orm, **context }
    )