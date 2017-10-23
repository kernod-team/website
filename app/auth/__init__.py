from flask import Blueprint

main = Blueprint('auth', __name__)

from app.auth import views
