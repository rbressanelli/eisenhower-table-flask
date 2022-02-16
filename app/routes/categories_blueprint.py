from flask import Blueprint

from app.controllers.categories_controller import create_category


bp_categories = Blueprint("bp_categories", __name__,  url_prefix="/categories")

bp_categories.post("")(create_category)
