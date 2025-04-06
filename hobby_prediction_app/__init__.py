from flask import Blueprint

hobby_prediction_bp = Blueprint('hobby_prediction_bp', __name__,template_folder="templates")

from . import routes
