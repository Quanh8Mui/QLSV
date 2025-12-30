from flask import Blueprint, render_template, request, redirect, flash
from flask_login import login_required
from routes.decorators import admin_required
from models.class_model import ClassModel
from models.major import Major
from models import db
from models.course import Course
from utils.class_name import generate_class_name
from sqlalchemy.exc import IntegrityError
from models.faculty import Faculty


admin_class_bp = Blueprint("admin_class", __name__)

# LIST
@admin_class_bp.route("/admin/classes")
@login_required
@admin_required
def class_list():
    faculty_id = request.args.get("faculty_id", type=int)
    major_id = request.args.get("major_id", type=int)
    course_id = request.args.get("course_id", type=int)

    query = ClassModel.query \
        .join(Major) \
        .join(Faculty) \
        .join(Course)

    if faculty_id:
        query = query.filter(Faculty.id == faculty_id)

    if major_id:
        query = query.filter(Major.id == major_id)

    if course_id:
        query = query.filter(Course.id == course_id)

    classes = query.all()

    faculties = Faculty.query.all()
    majors = Major.query.all()
    courses = Course.query.all()

    return render_template(
        "admin/classes/list.html",
        classes=classes,
        faculties=faculties,
        majors=majors,
        courses=courses,
        faculty_id=faculty_id,
        major_id=major_id,
        course_id=course_id
    )


# ADD
@admin_class_bp.route("/admin/classes/add", methods=["GET", "POST"])
@login_required
@admin_required
def class_add():
    majors = Major.query.all()
    courses = Course.query.all()

    if request.method == "POST":
        major_id = int(request.form["major_id"])
        course_id = int(request.form["course_id"])

        major = Major.query.get_or_404(major_id)
        course = Course.query.get_or_404(course_id)

        class_name = generate_class_name(major, course)

        class_obj = ClassModel(
            name=class_name,
            major_id=major_id,
            course_id=course_id
        )

        try:
            db.session.add(class_obj)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            flash("Lớp đã tồn tại, vui lòng thử lại", "danger")
            return redirect("/admin/classes/add")

        flash(f"Đã tạo lớp {class_name}", "success")
        return redirect("/admin/classes")

    return render_template(
        "admin/classes/add.html",
        majors=majors,
        courses=courses
    )

# EDIT
@admin_class_bp.route("/admin/classes/edit/<int:id>", methods=["GET", "POST"])
@login_required
@admin_required
def class_edit(id):
    class_obj = ClassModel.query.get_or_404(id)
    majors = Major.query.all()
    courses = Course.query.all()

    if request.method == "POST":
        class_obj.name = request.form["name"]
        class_obj.major_id = request.form["major_id"]
        class_obj.course_id = request.form["course_id"]

        db.session.commit()
        flash("Cập nhật lớp thành công", "success")
        return redirect("/admin/classes")

    return render_template(
        "admin/classes/edit.html",
        class_obj=class_obj,
        majors=majors,
        courses=courses
    )


# DELETE
@admin_class_bp.route("/admin/classes/delete/<int:id>")
@login_required
@admin_required
def class_delete(id):
    class_obj = ClassModel.query.get_or_404(id)

    if class_obj.students:
        flash("Không thể xoá lớp đang có sinh viên", "danger")
        return redirect("/admin/classes")

    db.session.delete(class_obj)
    db.session.commit()

    flash("🗑️ Đã xoá lớp", "success")
    return redirect("/admin/classes")
