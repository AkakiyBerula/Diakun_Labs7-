from flask import Blueprint

contract_activities_blueprint = Blueprint('contracts', __name__, template_folder="templates/contract_activities")

from . import views