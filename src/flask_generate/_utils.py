import os
import secrets

from pathlib import Path
from typing import Any

from ._jinja import render_string


EXTENSION_DIR = Path(__file__).resolve().parent


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