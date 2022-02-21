from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.session import Session
from flask import request, current_app, jsonify, session
from werkzeug.exceptions import BadRequest, NotFound
from http import HTTPStatus

from app.models.categories_model import CategoriesModel
from app.services.categories_service import check_body_request

def create_category():
    session: Session = current_app.db.session

    try:
        data = request.get_json()
        checked_data = check_body_request(data, name=str, description=str)

        category = CategoriesModel(**checked_data)
        session.add(category)

        session.commit()
        
        return jsonify(category), HTTPStatus.CREATED
        
    except IntegrityError:
        return jsonify ({
            "msg": "category already exists!" 
        }), HTTPStatus.CONFLICT 
    
    except BadRequest as err:
        return err.description, HTTPStatus.BAD_REQUEST


def get_categories():    
    
    try:
        categories = CategoriesModel.query.all()

        if not categories:
            raise NotFound
        
    except NotFound:
        return {
            'error': 'No registered categories'
        }, HTTPStatus.NOT_FOUND
        
    return jsonify([{
            "id": category.id,
            "name": category.name,
            "description": category.description,
            "tasks": [task for task in category.tasks]
        } for category in categories]), HTTPStatus.OK       
  

def update_category(id):
    session: Session = current_app.db.session

    data = request.get_json()

    category = CategoriesModel.query.get(id)
    
    if not category:
        return {
            "msg": "category not found!"
        }, HTTPStatus.NOT_FOUND

    for key, value in data.items():
        setattr(category, key, value)

    session.add(category)
    session.commit()

    return jsonify(category), HTTPStatus.OK


def delete_category(id):
    session: Session = current_app.db.session

    category = CategoriesModel.query.get(id)

    if not category:
        return {
            "msg": "category not found!"
        }, HTTPStatus.NOT_FOUND

    session.delete(category)
    session.commit()

    return '', HTTPStatus.NO_CONTENT
