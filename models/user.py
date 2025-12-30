from flask_login import UserMixin
from werkzeug.security import generate_password_hash
from . import db

class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)

    role = db.Column(db.String(10), nullable=False, default="user")

    phone = db.Column(db.String(20), nullable=True)
    avatar = db.Column(
        db.String(200),
        nullable=False
    )

    must_change_password = db.Column(
        db.Boolean,
        default=True
    )

    student = db.relationship(
        "Student",
        backref="user",
        uselist=False
    )

    @staticmethod
    def create_default_admin():
        if not User.query.filter_by(username="admin").first():
            admin = User(
                username="admin",
                password=generate_password_hash("admin123"),
                full_name="Administrator",
                email="admin@system.local",
                role="admin"
            )
            db.session.add(admin)
            db.session.commit()
