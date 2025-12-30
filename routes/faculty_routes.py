from flask import Blueprint, render_template, request, redirect, flash
from flask_login import login_required
from routes.decorators import admin_required
from models.faculty import Faculty
from models import db

faculty_bp = Blueprint("faculty", __name__)

# LIST
@faculty_bp.route("/admin/faculties")
@login_required
@admin_required
def faculty_list():
    faculties = Faculty.query.order_by(Faculty.id).all()
    return render_template("admin/faculty/list.html", faculties=faculties)

# ADD
@faculty_bp.route("/admin/faculties/add", methods=["GET", "POST"])
@login_required
@admin_required
def faculty_add():
    if request.method == "POST":
        name = request.form.get("name")

        if not name:
            flash("Tên khoa không được để trống", "danger")
            return redirect("/admin/faculties/add")

        if Faculty.query.filter_by(name=name).first():
            flash("Khoa đã tồn tại", "warning")
            return redirect("/admin/faculties/add")

        faculty = Faculty(name=name)
        db.session.add(faculty)
        db.session.commit()

        flash("Thêm khoa thành công", "success")
        return redirect("/admin/faculties")

    return render_template("admin/faculty/add.html")

# EDIT
@faculty_bp.route("/admin/faculties/edit/<int:id>", methods=["GET", "POST"])
@login_required
@admin_required
def faculty_edit(id):
    faculty = Faculty.query.get_or_404(id)

    if request.method == "POST":
        name = request.form.get("name")

        if not name:
            flash("Tên khoa không được để trống", "danger")
            return redirect(f"/admin/faculties/edit/{id}")

        exists = Faculty.query.filter(
            Faculty.name == name,
            Faculty.id != id
        ).first()

        if exists:
            flash("Tên khoa đã tồn tại", "warning")
            return redirect(f"/admin/faculties/edit/{id}")

        faculty.name = name
        db.session.commit()

        flash("Cập nhật khoa thành công", "success")
        return redirect("/admin/faculties")

    return render_template("admin/faculty/edit.html", faculty=faculty)

# DELETE
@faculty_bp.route("/admin/faculties/delete/<int:id>")
@login_required
@admin_required
def faculty_delete(id):
    faculty = Faculty.query.get_or_404(id)

    db.session.delete(faculty)
    db.session.commit()

    flash("Đã xoá khoa", "success")
    return redirect("/admin/faculties")
