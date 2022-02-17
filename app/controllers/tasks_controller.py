from sqlalchemy.exc import IntegrityError
from flask import request, current_app, jsonify, session
from sqlalchemy.orm.session import Session
from http import HTTPStatus

from app.models.tasks_model import TasksModel
from app.controllers.eisenhower_controller import populate_table

def create_task():

    populate_table()


    return ''