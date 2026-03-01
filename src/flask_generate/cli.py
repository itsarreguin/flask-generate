import os
import click

from flask import current_app
from flask.cli import with_appcontext

from ._files import create_templ_file
from ._utils import _get_required_settings, _to_snake_case
from .generators import create_form, create_model, generate_blueprint_pkg
from .generators import blueprint_scaffold, mvc_scaffold


@click.group('generate')
def generate():
    """ Handle app scaffolding. """
    pass


@generate.command()
@click.argument('name')
@with_appcontext
def blueprint(name: str):
    app_name, _, app_type, _ = _get_required_settings(current_app)
    bp_name: str = _to_snake_case(string=name)
    context = { 'blueprint_name': bp_name }

    if app_type == 'blueprint':
        generate_blueprint_pkg(bp_name, app_name, 'blueprint', **context)
    else:
        template: str = 'blueprint.py-tpl'
        dest: str = 'blueprints'
        create_templ_file(app_name, dest, template, bp_name, **context)


@generate.command()
@click.argument('name', type=str)
@click.argument('fields', nargs=-1, type=str)
@click.option('-d', '--dest', default='forms', help='Form destination file/blueprint')
@with_appcontext
def form(name: str, fields: list[str], dest: str | None):
    app_name, app_dir, app_type, _ = _get_required_settings(current_app)

    dest = _to_snake_case(dest)
    context = { 'form_name': name, 'fields': fields }

    if app_type == 'blueprint' and dest in os.listdir(app_dir):
        file_path = os.path.join(app_name, dest, 'forms.py')
        return create_form(app_name, file_path, dest, 'forms.py', **context)
    else:
        filename = f'{dest}.py'
        file_path = os.path.join(app_name, 'forms', filename)

        return create_form(app_name, file_path, 'forms', dest, **context)


@generate.command()
@click.argument('name', type=str)
@click.argument('fields', nargs=-1, type=str)
@click.option('-d', '--dest', default='models', help='Model destination file/blueprint')
@with_appcontext
def model(name: str, fields: list[str], dest: str | None):
    app_name, app_dir, app_type, orm = _get_required_settings(current_app)

    dest = _to_snake_case(dest)
    context = { 'model_name': name, 'fields': fields }

    if app_type == 'blueprint' and dest in os.listdir(app_dir):
        file_path = os.path.join(app_name, dest, 'models.py')
        return create_model(app_name, orm, file_path, dest, 'models', **context)
    else:
        filename: str = f'{dest}.py'
        file_path = os.path.join(app_name, 'models', filename)

        return create_model(app_name, orm, file_path, 'models', dest, **context)


@generate.command()
@click.argument('name', type=str)
@click.argument('model', type=str)
@click.argument('fields', nargs=-1, type=str)
@with_appcontext
def scaffold(name: str, model: str, fields: list[str]):
    _, _, app_type, orm = _get_required_settings(current_app)
    context = {
        'blueprint_name': _to_snake_case(name),
        'model_name': model,
        'fields': fields,
        'form_name': model,
    }

    if app_type == 'blueprint':
        blueprint_scaffold(_get_required_settings(current_app), **context)
    else:
        mvc_scaffold(_get_required_settings(current_app), **context)