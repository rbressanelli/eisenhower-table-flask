from flask import Blueprint

bp_error = Blueprint("errors", __name__)

@bp_error.app_errorhandler(404)
def not_found(e):
  return {'error': 'Page not found'}, 404
