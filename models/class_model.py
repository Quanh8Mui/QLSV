from models import db

class ClassModel(db.Model):
    __tablename__ = "classes"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(50), nullable=False, unique=True)

    major_id = db.Column(
        db.Integer,
        db.ForeignKey("majors.id"),
        nullable=False
    )

    course_id = db.Column(
        db.Integer,
        db.ForeignKey("courses.id"),
        nullable=False
    )

    major = db.relationship(
        "Major",
        backref=db.backref("classes", lazy=True)
    )

    course = db.relationship(
        "Course",
        backref=db.backref("classes", lazy=True)
    )

    def __repr__(self):
        return f"<Class {self.name}>"
