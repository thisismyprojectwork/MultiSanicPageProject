from typing import Any
from sanic import response
from sanic import HTTPResponse
from jinja2 import Environment, FileSystemLoader

env = Environment(loader=FileSystemLoader("./templates", encoding="utf8"))

def render_template(file_:str, **kwargs: Any) -> HTTPResponse:
    template = env.get_template(file_)
    return response.html(template.render(**kwargs))
