from flask import Blueprint, render_template, request, redirect, flash
from flask_login import login_required
from routes.decorators import admin_required
from models.major import Major
from models.faculty import Faculty
from models import db

admin_major_bp = Blueprint("admin_major", __name__)

# LIST
@admin_major_bp.route("/admin/majors")
@login_required
@admin_required
def major_list():
    majors = Major.query.all()
    return render_template(
        "admin/majors/list.html",
        majors=majors
    )

# ADD
@admin_major_bp.route("/admin/majors/add", methods=["GET", "POST"])
@login_required
@admin_required
def major_add():
    faculties = Faculty.query.all()

    if request.method == "POST":
        name = request.form["name"]
        faculty_id = request.form["faculty_id"]

        major = Major(
            name=name,
            faculty_id=faculty_id
        )
        db.session.add(major)
        db.session.commit()

        flash("Thêm ngành thành công", "success")
        return redirect("/admin/majors")

    return render_template(
        "admin/majors/add.html",
        faculties=faculties
    )

# EDIT
@admin_major_bp.route("/admin/majors/edit/<int:id>", methods=["GET", "POST"])
@login_required
@admin_required
def major_edit(id):
    major = Major.query.get_or_404(id)
    faculties = Faculty.query.all()

    if request.method == "POST":
        major.name = request.form["name"]
        major.faculty_id = request.form["faculty_id"]
        db.session.commit()

        flash("Cập nhật ngành thành công", "success")
        return redirect("/admin/majors")

    return render_template(
        "admin/majors/edit.html",
        major=major,
        faculties=faculties
    )

# DELETE
@admin_major_bp.route("/admin/majors/delete/<int:id>")
@login_required
@admin_required
def major_delete(id):
    major = Major.query.get_or_404(id)

    if major.classes:
        flash("Không thể xoá ngành đang có lớp", "danger")
        return redirect("/admin/majors")

    db.session.delete(major)
    db.session.commit()

    flash("🗑Đã xoá ngành", "success")
    return redirect("/admin/majors")
