from sqlalchemy import Column, ForeignKey, Integer, String, Text
from dataclasses import dataclass

from app.configs.database import db


@dataclass
class EisenhowersModel(db.Model):

    id: int
    type: str

    __tablename__ = "eisenhowers"

    id = Column(Integer, primary_key=True, autoincrement=False)
    type = Column(String(100))
