from sqlalchemy import Column, Integer, String
from dataclasses import dataclass

from app.configs.database import db


@dataclass
class EisenhowersModel(db.Model):

    id: int
    type: str

    __tablename__ = "eisenhowers"

    id = Column(Integer, primary_key=True, autoincrement=False)
    type = Column(String(100))

    tasks = db.relationship("TasksModel", backref="eisenhower")   
    