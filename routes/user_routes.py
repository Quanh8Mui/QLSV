from flask import Blueprint, render_template
from flask_login import login_required
from routes.decorators import admin_required
from models.user import User

user_bp = Blueprint("user", __name__)

@user_bp.route("/admin/users")
@login_required
@admin_required
def user_list():
    users = User.query.all()
    return render_template("admin/users.html", users=users)
