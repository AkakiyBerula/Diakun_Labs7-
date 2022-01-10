from flask import Blueprint
from flask_restful import Api

api_v2_blueprint = Blueprint('api_v2', __name__, template_folder="templates")
api = Api(api_v2_blueprint)

from . import views