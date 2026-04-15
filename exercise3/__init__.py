# __init__.py
from flask import Blueprint

ex3_bp = Blueprint('ex3', __name__, template_folder='templates')

from . import routes