from models import db

class Major(db.Model):
    __tablename__ = "majors"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    code = db.Column(db.String(10), nullable=False)

    faculty_id = db.Column(
        db.Integer,
        db.ForeignKey("faculties.id"),
        nullable=False
    )

    faculty = db.relationship(
        "Faculty",
        backref=db.backref("majors", lazy=True)
    )

    def __repr__(self):
        return f"<Major {self.name}>"
