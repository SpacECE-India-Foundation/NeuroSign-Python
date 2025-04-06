from flask import Blueprint

story_bp = Blueprint('story_bp', __name__, template_folder="templates")

from . import routes
