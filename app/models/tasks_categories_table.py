from sqlalchemy import Column, ForeignKey, Integer

from app.configs.database import db

tasks_categories = db.Table("tasks_categories",

    Column('id', Integer, primary_key=True),

    Column('task_id', Integer, ForeignKey('tasks.id')),

    Column('category_id', Integer, ForeignKey('categories.id'))
)
