import platform
from importlib import metadata

from flask import Blueprint, render_template

from ._jinja import get_icon


path = Blueprint(
    'flask_generate',
    __name__,
    static_folder='static',
    static_url_path='/flask_generate/static',
    template_folder='templates'
)


@path.route('/')
def index():
    template_name: str = 'generate/index.html.jinja'
    data = [
        {
            'title': 'Documentation',
            'icon': get_icon('book_open_fill'),
            'link': 'https://flask.palletsprojects.com/en/stable/',
            'description': 'Start learning Flask from the official framework documentation.'
        },
        {
            'title': 'Tutorial',
            'icon': get_icon('academic_cap_fill'),
            'link': 'https://flask.palletsprojects.com/en/stable/tutorial/',
            'description': 'Create your first web application using the Flask framework.'
        },
        {
            'title': 'Extensions',
            'icon': get_icon('bolt_fill'),
            'link': '',
            'description': 'Discover lost of extensions, and make your apps more powerful.'
        },
        {
            'title': 'Flask Generate',
            'icon': get_icon('command_line_fill'),
            'link': '',
            'description': 'Learn more about Flask-Generate and speed up your development.'
        }
    ]
    context = {
        'object_list': data,
        'flask_version': metadata.version('flask'),
        'py_version': platform.python_version(),
    }
    return render_template(template_name, **context)