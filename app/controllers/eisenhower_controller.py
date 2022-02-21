from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.session import Session
from flask import current_app

from app.models.eisenhowers_model import EisenhowersModel


def populate_table():   
     
    session: Session = current_app.db.session
    
    table_data = [
        {"id": 11, 'type': 'Do it First'}, 
        {"id": 12, 'type': 'Delegate It'}, 
        {"id": 21, 'type': 'Schedule It'}, 
        {"id": 22, 'type': 'Delete It'}
    ] 
       
    try:
        for value in table_data:
            eisenhower = EisenhowersModel(**value)
            session.add(eisenhower)
            session.commit()   
    except IntegrityError:
        print("Tabela Eisenhower criada e já populada")
    