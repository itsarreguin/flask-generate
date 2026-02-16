from flask import Blueprint, render_template


bp_name: str = 'flask_generate'

path = Blueprint(bp_name, __name__, 'static', template_folder='templates')


@path.route('/')
def index():
    return render_template('generate/index.html.jinja')