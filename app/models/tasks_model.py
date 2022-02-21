from sqlalchemy import Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import validates
from dataclasses import dataclass

from app.configs.database import db
from app.exc.classification_error import ClassificationError


@dataclass
class TasksModel(db.Model):

    id: int
    name: str
    description: str
    duration: int
    importance: int
    urgency: int

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
        if not 1 <= value <= 2:
            raise ClassificationError

        return value
