from sqlalchemy.exc import IntegrityError
from flask import request, current_app, jsonify, session
from sqlalchemy.orm.session import Session
from http import HTTPStatus

from app.models.categories_model import CategoriesModel

def create_category():
    session: Session = current_app.db.session

    data = request.get_json()

    category = CategoriesModel(**data)

    session.add(category)

    try:
        session.commit()
    except IntegrityError:
        return {
            "msg": "category already exists!" 
        }, HTTPStatus.CONFLICT    

    return jsonify(category), HTTPStatus.CREATED


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
