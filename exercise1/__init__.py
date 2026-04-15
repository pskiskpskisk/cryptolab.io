from flask import Blueprint

ex1_bp = Blueprint('ex1', __name__, template_folder='templates')

from . import routes
