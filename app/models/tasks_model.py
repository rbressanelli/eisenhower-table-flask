from sqlalchemy import Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import validates
from dataclasses import dataclass
from werkzeug.exceptions import BadRequest

from app.configs.database import db
from app.exc.classification_error import ClassificationError


@dataclass
class TasksModel(db.Model):

    id: int
    name: str
    description: str
    duration: int
    # importance: int
    # urgency: int

    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)
    description = Column(Text)
    duration = Column(Integer)
    importance = Column(Integer)
    urgency = Column(Integer)

    eisenhower_id = Column(Integer, ForeignKey('eisenhowers.id'))


    @validates("importance", "urgency")
    def validate_eisenhowers_indexes(self, key, value):
        if type(value) != int:
            raise TypeError({'error': "importance and urgency must be int type"})
        if not 1 <= value <= 2:
            raise ClassificationError

        return value


    @validates("name", "description")
    def validade_strings_type(self, key, value):
        if type(value) != str:
            raise BadRequest(description={'error': 'name and description must be string type'})
        
        return value
