from typing import Any

from jinja2 import Environment, Template

from ._fields import field_name, field_type, form_field, table_field


jinja_env = Environment()

jinja_env.globals.update(
    {
        'field_name': field_name,
        'field_type': field_type,
        'form_field': form_field,
        'table_field': table_field
    }
)


def _render(template: Template, context: dict[str, Any]) -> str:
    return template.render(context)


def render_string(source: str, **context: Any):
    template = jinja_env.from_string(source=source)
    return _render(template, context=context)