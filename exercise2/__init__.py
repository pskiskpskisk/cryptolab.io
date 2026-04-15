from flask import Blueprint

ex2_bp = Blueprint('ex2', __name__, template_folder='templates')

from . import routes