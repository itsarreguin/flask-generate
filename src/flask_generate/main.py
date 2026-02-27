import click

from .generators import create_blueprint_structure, create_mvc_structure


@click.group
def cli():
    """ Base function for flask-generate commads. """


@cli.command()
@click.argument('name', type=str)
@click.option('--type', help='App structure type', default='mvc')
@click.option('--orm', help='Choice an ORM: SQLAlchemy/Peewee', default='sqlalchemy')
def app(name: str, type: str, orm: str):
    if type == 'blueprint':
        create_blueprint_structure(name, orm)
    else:
        create_mvc_structure(name, orm)


def execute():
    cli()