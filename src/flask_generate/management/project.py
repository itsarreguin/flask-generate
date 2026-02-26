import click

from .._files import create_mvc_app_structure
from .._files import create_blueprint_app_structure


@click.group
def cli():
    """ Base function for flask-generate commads. """


@cli.command()
@click.argument('name', type=str)
@click.option('--type', help='App structure type', default='mvc')
@click.option('--orm', help='Choice an ORM: SQLAlchemy/Peewee', default='sqla')
def app(name: str, type: str, orm: str):
    if type == 'blueprint':
        create_blueprint_app_structure(name, orm)
    else:
        create_mvc_app_structure(name, orm)


def execute_cli():
    cli()