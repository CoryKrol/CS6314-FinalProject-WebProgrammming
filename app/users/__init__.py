from flask import Blueprint

users = Blueprint('users', __name__)

# Import modules here to avoid circular dependencies until after main is defined
from . import views
from ..models import Permission


@users.app_context_processor
def inject_permissions():
    """Make Permissions available to template engine"""
    return dict(Permission=Permission)
