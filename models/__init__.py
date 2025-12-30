from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .user import User
from .student import Student
from .course import Course
from .major import Major
from .class_model import ClassModel
from .faculty import Faculty

