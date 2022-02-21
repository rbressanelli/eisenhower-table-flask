from flask import current_app
from sqlalchemy.orm.session import Session

from app.models.categories_model import CategoriesModel


def add_categories(*args, **kwargs):
    session: Session = current_app.db.session
    
    info_categories, registered_categories, new_task = args
    
    for value in info_categories:
        if value in registered_categories:                
            new = CategoriesModel.query.filter_by(name=value).one()
            new_task.categories.append(new)
        elif value not in registered_categories:
            category_data = {"name": f"{value}", "description": ""}                
            new_category = CategoriesModel(**category_data)
            session.add(new_category)
            session.commit()                 
            new = CategoriesModel.query.filter_by(name=value).one()                
            new_task.categories.append(new) 

    return None
