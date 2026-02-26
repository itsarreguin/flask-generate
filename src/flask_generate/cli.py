import os
import click

from flask import current_app
from flask.cli import with_appcontext

from ._files import create_template_file, generate_structure
from ._utils import _get_app_name, _to_snake_case


@click.group('generate')
def generate():
    """ Handle app scaffolding. """
    pass


@generate.command()
@click.argument('name')
@with_appcontext
def blueprint(name: str):
    app_name: str = _get_app_name(current_app.name)
    app_type: str = current_app.config['GENERATE_APP_TYPE']
    bp_name: str = _to_snake_case(string=name)
    context = { 'blueprint_name': bp_name }

    if app_type == 'blueprint':
        template_root_path = os.path.join('', 'templates', 'blueprint')
        os.mkdir(os.path.join(app_name, bp_name))

        generate_structure(app_name, template_root_path, bp_name, **context)
    else:
        template: str = 'blueprint.py-tpl'
        dest: str = 'blueprints'
        create_template_file(app_name, dest, template, bp_name, **context)


@generate.command()
@click.argument('name', type=str)
@click.argument('fields', nargs=-1, type=str)
@click.option('-d', '--dest', help='Form destination file/blueprint')
@with_appcontext
def form(name: str, fields: list[str], dest: str | None):
    app_name = _get_app_name(current_app.name)
    app_type = current_app.config['GENERATE_APP_TYPE']

    if app_type == 'blueprint':
        pass
    else:
        template: str = 'form.py-tpl'
        create_template_file(app_name, 'forms', template, dest, **{
            'form_name': name,
            'fields': fields
        })


@generate.command()
@click.argument('name', type=str)
@click.argument('fields', nargs=-1, type=str)
@click.option('-d', '--dest', default=None, help='Model destination file/blueprint')
@with_appcontext
def model(name: str, fields: list[str], file: str | None):
    pass


@generate.command()
@click.argument('name', type=str)
@click.argument('model', type=str)
@click.argument('fields', nargs=-1, type=str)
@with_appcontext
def scaffold(name: str, model: str, fields: list[str]):
    pass