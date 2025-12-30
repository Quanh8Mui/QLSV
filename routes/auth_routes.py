from flask import Blueprint, render_template, request, redirect, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from models.user import User
from models import db
from routes.decorators import student_required
from models.student import Student

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = User.query.filter_by(username=request.form["username"]).first()

        if not user or not check_password_hash(
            user.password, request.form["password"]
        ):
            flash("Sai tài khoản hoặc mật khẩu", "danger")
            return redirect("/login")

        login_user(user)

        if user.must_change_password:
            return redirect("/student/change-password")

        if user.role == "admin":
            return redirect("/admin/students")
        elif user.role == "student":
            return redirect("/student/profile")
        else:
            flash("Vai trò không hợp lệ", "danger")
            return redirect("/login")

    return render_template("auth/login.html")


@auth_bp.route("/student/change-password", methods=["GET", "POST"])
@login_required
@student_required
def change_password():
    if request.method == "POST":
        if not check_password_hash(
            current_user.password, request.form["old_password"]
        ):
            flash("Mật khẩu cũ không đúng", "danger")
            return redirect("/student/change-password")

        current_user.password = generate_password_hash(
            request.form["new_password"]
        )
        current_user.must_change_password = False
        db.session.commit()

        flash("Đổi mật khẩu thành công", "success")
        return redirect("/student/profile")

    return render_template("students/change_password.html")

@auth_bp.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():
    if request.method == "POST":
        mssv = request.form.get("mssv")
        email = request.form.get("email")

        student = Student.query.filter_by(mssv=mssv).first()

        if not student or not student.user:
            flash("MSSV không tồn tại", "danger")
            return redirect("/forgot-password")

        if student.user.email != email:
            flash("Email không khớp với MSSV", "danger")
            return redirect("/forgot-password")

        # xác thực thành công → chuyển sang đặt mật khẩu mới
        return redirect(f"/reset-password/{student.user.id}")

    return render_template("auth/forgot_password.html")

@auth_bp.route("/reset-password/<int:user_id>", methods=["GET", "POST"])
def reset_password(user_id):
    user = User.query.get_or_404(user_id)

    if request.method == "POST":
        password = request.form.get("password")
        confirm = request.form.get("confirm")

        if not password or not confirm:
            flash("Vui lòng nhập đầy đủ thông tin", "warning")
            return redirect(request.url)

        if password != confirm:
            flash("Mật khẩu không khớp", "danger")
            return redirect(request.url)

        user.password = generate_password_hash(password)
        user.must_change_password = False
        db.session.commit()

        flash("Đặt lại mật khẩu thành công. Vui lòng đăng nhập", "success")
        return redirect("/login")

    return render_template("auth/reset_password.html")

@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/login")
