from flask import Blueprint, render_template, request, redirect, flash
from flask_login import login_required
from routes.decorators import admin_required
from models.course import Course
from models import db
from utils.course_code import generate_course_code
from sqlalchemy.exc import IntegrityError

admin_course_bp = Blueprint("admin_course", __name__)

# LIST
@admin_course_bp.route("/admin/courses")
@login_required
@admin_required
def course_list():
    courses = Course.query.order_by(Course.start_year.desc()).all()
    return render_template("admin/courses/list.html", courses=courses)

# ADD
@admin_course_bp.route("/admin/courses/add", methods=["GET", "POST"])
@login_required
@admin_required
def course_add():
    if request.method == "POST":
        try:
            start_year = int(request.form["start_year"])

            code = generate_course_code(start_year)

            # kiểm tra trùng
            if Course.query.filter_by(code=code).first():
                flash(f"Khóa {code} đã tồn tại", "danger")
                return redirect("/admin/courses/add")

            course = Course(
                code=code,
                name=code,          # name = code
                start_year=start_year
            )

            db.session.add(course)
            db.session.commit()

            flash(f"Đã tạo khóa học {code}", "success")
            return redirect("/admin/courses")

        except IntegrityError:
            db.session.rollback()
            flash("Lỗi dữ liệu", "danger")

    return render_template("admin/courses/add.html")

# EDIT
@admin_course_bp.route("/admin/courses/edit/<int:id>", methods=["GET", "POST"])
@login_required
@admin_required
def course_edit(id):
    course = Course.query.get_or_404(id)

    if request.method == "POST":
        course.code = request.form["code"].upper()
        course.start_year = int(request.form["start_year"])
        db.session.commit()

        flash("Cập nhật khóa học thành công", "success")
        return redirect("/admin/courses")

    return render_template("admin/courses/edit.html", course=course)

# DELETE
@admin_course_bp.route("/admin/courses/delete/<int:id>")
@login_required
@admin_required
def course_delete(id):
    course = Course.query.get_or_404(id)

    db.session.delete(course)
    db.session.commit()

    flash("Đã xoá khóa học", "success")
    return redirect("/admin/courses")
