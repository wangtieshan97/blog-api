from flask import Blueprint

api = Blueprint('api', __name__)

from main.api import upload, error, tag, note, login
