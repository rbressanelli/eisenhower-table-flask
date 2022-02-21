from flask import Blueprint

from app.controllers.tasks_controller import (create_task, delete_task,
                                              get_tasks, update_task)

bp_tasks = Blueprint("bp_tasks", __name__, url_prefix="/tasks")


bp_tasks.post("")(create_task)

bp_tasks.patch("<id>")(update_task)

bp_tasks.delete("<id>")(delete_task)

bp_tasks.get("")(get_tasks)
