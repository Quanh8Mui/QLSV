import os
from flask import Blueprint, render_template, request, redirect, flash, current_app
from flask_login import login_required, current_user
from routes.decorators import student_required
from models import db
from werkzeug.utils import secure_filename

student_bp = Blueprint("student", __name__)

# ===== PROFILE =====
@student_bp.route("/student/profile", methods=["GET", "POST"])
@login_required
@student_required
def profile():
    user = current_user
    student = user.student

    if request.method == "POST":
        user.phone = request.form.get("phone")  # an toàn
        db.session.commit()
        flash("Cập nhật hồ sơ thành công", "success")
        return redirect("/student/profile")

    return render_template(
        "students/profile.html",
        student=student,
        user=user
    )

@student_bp.route("/student/change-avatar", methods=["POST"])
@login_required
@student_required
def change_avatar():
    file = request.files.get("avatar")

    if not file or file.filename == "":
        flash("Chưa chọn ảnh", "warning")
        return redirect("/student/profile")

    ext = file.filename.rsplit(".", 1)[1].lower()
    if ext not in current_app.config["ALLOWED_EXTENSIONS"]:
        flash("Định dạng ảnh không hợp lệ", "danger")
        return redirect("/student/profile")

    filename = secure_filename(f"user_{current_user.id}.{ext}")
    path = os.path.join(current_app.config["UPLOAD_FOLDER"], filename)
    file.save(path)

    current_user.avatar = filename
    db.session.commit()

    flash("Đổi ảnh đại diện thành công", "success")
    return redirect("/student/profile")

