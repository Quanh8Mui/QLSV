from . import db

class Course(db.Model):
    __tablename__ = "courses"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    code = db.Column(db.String(10), nullable=False, unique=True)
    start_year = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"<Course {self.code}>"