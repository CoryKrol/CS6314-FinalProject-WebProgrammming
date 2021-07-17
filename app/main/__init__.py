from flask import Blueprint

main = Blueprint('main', __name__)

# Import modules here to avoid circular dependencies until after main is defined
from . import views, errors
