import os
import secrets


def _create_subdir(app_name: str, *paths: str) -> None:
    path = os.path.join(app_name, *paths)
    os.mkdir(path)


def _generate_secret_key(length: int = 48) -> str:
    lower_chars = 'abcdefghijklmnopqrstuvwxyz'
    upper_chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    special_chars = '@&-_─^~#*'

    chars = lower_chars + upper_chars + special_chars
    return ''.join(secrets.choice(chars) for _ in range(length))


def _get_file_extension(file: str) -> list[str]:
    file_ext = file.rsplit('.')[1]
    match file_ext:
        case 'py-tpl':
            return ['py-tpl', 'py']
        case 'html-tpl':
            return ['html-tpl', 'html']
        case 'md-tpl':
            return ['md-tpl', 'md']