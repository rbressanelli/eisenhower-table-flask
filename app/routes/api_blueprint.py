from flask import Blueprint

from app.routes.categories_blueprint import bp_categories
from app.routes.tasks_blueprint import bp_tasks
from app.routes.error_blueprint import bp_error

bp_api = Blueprint("bp_api", __name__, url_prefix="/api")

bp_api.register_blueprint(bp_categories)
bp_api.register_blueprint(bp_tasks)
bp_api.register_blueprint(bp_error)
