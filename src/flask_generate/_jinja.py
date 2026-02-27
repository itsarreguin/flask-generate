from typing import Any

from flask import get_template_attribute
from jinja2 import Environment, Template

from ._fields import field_name, field_type, form_field, import_fields
from ._fields import table_field, table_name


jinja_env = Environment()

jinja_env.globals.update(
    {
        'field_name': field_name,
        'field_type': field_type,
        'form_field': form_field,
        'import_fields': import_fields,
        'table_field': table_field,
        'table_name': table_name
    }
)


def _render(template: Template, context: dict[str, Any]) -> str:
    return template.render(context)


def render_string(source: str, **context: Any) -> str:
    template = jinja_env.from_string(source=source)
    return _render(template, context=context)


def get_icon(attribute: str) -> str:
    return get_template_attribute('generate/icons.html.jinja', attribute)