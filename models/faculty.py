from models import db

class Faculty(db.Model):
    __tablename__ = "faculties"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)

    def __repr__(self):
        return f"<Faculty {self.name}>"
