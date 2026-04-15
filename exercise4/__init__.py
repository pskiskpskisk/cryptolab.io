from flask import Blueprint

ex4_bp = Blueprint('ex4', __name__, template_folder='templates')

from . import routes