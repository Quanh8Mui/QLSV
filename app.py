from flask import Flask
from flask_login import LoginManager, current_user, login_required
from config import Config
from models import db
from models.user import User
from routes.auth_routes import auth_bp
from routes.admin_routes import admin_bp
from routes.api_routes import api_bp
from routes.user_routes import user_bp
from routes.student_routes import student_bp
from routes.faculty_routes import faculty_bp
from routes.admin_major_routes import admin_major_bp
from routes.admin_class_routes import admin_class_bp
from routes.admin_courses import admin_course_bp


app = Flask(__name__)
app.config.from_object(Config)
app.config["MAX_CONTENT_LENGTH"] = Config.MAX_CONTENT_LENGTH

db.init_app(app)

login_manager = LoginManager(app)
login_manager.login_view = "auth.login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

app.register_blueprint(auth_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(student_bp)
app.register_blueprint(api_bp)
app.register_blueprint(user_bp)
app.register_blueprint(faculty_bp)
app.register_blueprint(admin_major_bp)
app.register_blueprint(admin_class_bp)
app.register_blueprint(admin_course_bp)

with app.app_context():
    db.create_all()
    User.create_default_admin()

@app.route("/")
@login_required
def home():
    return f"""
        <h2>Xin chào {current_user.username} ({current_user.role})</h2>
        <a href="/logout">Đăng xuất</a>
    """



if __name__ == "__main__":
    app.run(debug=True)
