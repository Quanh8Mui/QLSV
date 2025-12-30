from models import db

class Student(db.Model):
    __tablename__ = "students"

    id = db.Column(db.Integer, primary_key=True)

    mssv = db.Column(
        db.String(20),
        nullable=False,
        unique=True  
    )

    name = db.Column(db.String(100), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)

    class_id = db.Column(
        db.Integer,
        db.ForeignKey("classes.id"),
        nullable=False
    )

    # BẮT BUỘC PHẢI CÓ
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        unique=True,
        nullable=True
    )

    class_model = db.relationship("ClassModel", backref="students")
