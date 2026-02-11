from typing import Any

from jinja2 import Environment, Template


jinja_env = Environment()


def _render(template: Template, context: dict[str, Any]) -> str:
    return template.render(context)


def render_string(source: str, **context: Any):
    template = jinja_env.from_string(source=source)
    return _render(template, context=context)