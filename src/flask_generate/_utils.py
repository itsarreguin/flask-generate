import os
import re
import secrets

from pathlib import Path


EXTENSION_DIR = Path(__file__).resolve().parent


def _create_subdir(app_name: str, *paths: str) -> None:
    path = os.path.join(app_name, *paths)
    os.mkdir(path)


def _extract_file_extension(file: str) -> list[str]:
    file_ext = file.rsplit('.')[1]
    match file_ext:
        case 'py-tpl':
            return ['py-tpl', 'py']
        case 'html-tpl':
            return ['html-tpl', 'html.jinja']
        case 'md-tpl':
            return ['md-tpl', 'md']


def _generate_secret_key(length: int = 48) -> str:
    chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    special_chars = '@&-_─^~#*'
    return ''.join(secrets.choice(chars + special_chars) for _ in range(length))


def _get_app_name(value: str) -> str:
    return value.split('.')[0] if '.' in value else value


def _get_required_settings(current_app) -> list[str]:
    app_name = _get_app_name(current_app.name)
    app_dir = current_app.config['APP_DIR']
    app_type = current_app.config['GENERATE_APP_TYPE']
    orm = current_app.config['GENERATE_ORM']

    return [app_name, app_dir, app_type, orm]


def _to_snake_case(string: str) -> str:
    return re.sub(r'[^\w]+', '_', string.lower())


def snake_to_title(value: str) -> str:
    return value.replace('_', ' ').title()


def _get_field_name_and_type(value: str) -> str:
    field_name, field_type = value.split(':')
    field_name = _to_snake_case(field_name)
    return field_name, field_type.lower()