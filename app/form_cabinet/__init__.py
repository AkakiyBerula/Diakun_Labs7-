from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound

form_cabinet_blueprint = Blueprint('form_cabinet', __name__, template_folder="templates/form_cabinet")

from . import views