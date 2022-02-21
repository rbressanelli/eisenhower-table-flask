from http import HTTPStatus

from flask import current_app, jsonify, request
from psycopg2.errors import NotNullViolation, UniqueViolation
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.session import Session
from werkzeug.exceptions import BadRequest

from app.controllers.eisenhower_controller import populate_table
from app.exc.classification_error import ClassificationError
from app.models.categories_model import CategoriesModel
from app.models.eisenhowers_model import EisenhowersModel
from app.models.tasks_model import TasksModel
from app.services.tasks_service import add_categories


def create_task():
    
    if not EisenhowersModel.query.all():
        populate_table()
        
    session: Session = current_app.db.session

    try:
        data = request.get_json()
        
                
        info_categories = [cat.lower() for cat in data.pop('categories')]
         
        new_task = TasksModel(**data)        
        importance = str(abs(data['importance']))
        urgency = str(abs(data['urgency']))
        classification = EisenhowersModel.query.filter_by(id=importance + urgency).first()        
        
        new_task.eisenhower_id = classification.id
        
        registered_categories = [cat.name for cat in CategoriesModel.query.all()]
        
        add_categories(info_categories, registered_categories, new_task)        

        session.add(new_task)
        session.commit()
        
    except IntegrityError as err:        
        if isinstance(err.orig, UniqueViolation):            
            return {'error': 'task already exists!'}, HTTPStatus.CONFLICT
        elif isinstance(err.orig, NotNullViolation):
            return {'error': 'missing `name` key!'}, HTTPStatus.BAD_REQUEST  
    except ClassificationError as err:
        return jsonify({
                        "msg": {
                            "valid_options": {
                                "importance": [1, 2],
                                "urgency": [1, 2]
                            },
                            "recieved_options": {
                                "importance": data['importance'],
                                "urgency": data['urgency']
                            }
                        }
                    }), HTTPStatus.BAD_REQUEST
    except BadRequest as err:
        return jsonify(err.description), HTTPStatus.BAD_REQUEST   
    except TypeError as err:        
        return jsonify(err.args[0]),HTTPStatus.BAD_REQUEST
        
    return jsonify({
        "id": new_task.id,
        "name": new_task.name,
        "description":new_task.description,
        "duration": new_task.duration,
        "classification": new_task.eisenhower.type,
        "categories": [category.name for category in new_task.categories]
    }), HTTPStatus.CREATED


def update_task(id):
    
    session: Session = current_app.db.session

    data = request.get_json()
    
    task = TasksModel.query.get(id) 
    
    if not task:
        return {
            "msg": "task not found!"
        }, HTTPStatus.NOT_FOUND    
    
    try:    
        info_categories = [cat.lower() for cat in data.pop('categories')]        
           
    except KeyError:        
        info_categories = []
           
    finally:
        for key, value in data.items():
            setattr(task, key, value)    
            
        importance = str(task.importance)
        urgency = str(task.urgency)    
                
        classification = EisenhowersModel.query.filter_by(id=importance + urgency).first()        
        task.eisenhower_id = classification.id  
        
        registered_categories = [cat.name for cat in CategoriesModel.query.all()]
        add_categories(info_categories, registered_categories, task)    
       
    session.add(task)
    session.commit()
    
    return jsonify({
            'id': task.id,
            "name": task.name,
            "description":task.description,
            "duration": task.duration,
            "classification": task.eisenhower.type,
            'categories': [category.name for category in task.categories]
        }), HTTPStatus.OK
    

def delete_task(id):
    session: Session = current_app.db.session
    
    task = TasksModel.query.get(id) 
    
    if not task:
        return {
            "msg": "task not found!"
        }, HTTPStatus.NOT_FOUND 
    
    session.delete(task)
    session.commit()   
    
    return "", HTTPStatus.NO_CONTENT


def get_tasks():   
    
    tasks = TasksModel.query.order_by('id').all()
    
    if not tasks:
        return jsonify({
            'error': 'No registered tasks'
        }), HTTPStatus.NOT_FOUND
    
    return jsonify([{
            'id': task.id,
            "name": task.name,
            "description":task.description,
            "duration": task.duration,
            "classification": task.eisenhower.type,
            'categories': [category.name for category in task.categories]
        } for task in tasks]), HTTPStatus.OK
