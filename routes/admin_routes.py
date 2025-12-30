from flask import Blueprint, render_template, request, redirect, flash
from werkzeug.security import generate_password_hash
from flask_login import login_required
from routes.decorators import admin_required
from models.student import Student
from models.class_model import ClassModel
from models import db
from datetime import datetime
from models.faculty import Faculty
from models.major import Major
from models.user import User
from utils.mssv import generate_mssv
from sqlalchemy.exc import IntegrityError

admin_bp = Blueprint("admin", __name__)

@admin_bp.route("/admin/dashboard")
@login_required
@admin_required
def dashboard():
    return render_template(
        "admin/dashboard.html",
        student_count=Student.query.count(),
        class_count=ClassModel.query.count(),
        major_count=Major.query.count(),
        faculty_count=Faculty.query.count()
    )

# Danh sách sinh viên
@admin_bp.route("/admin/students")
@login_required
@admin_required
def student_list():
    faculty_id = request.args.get("faculty_id", type=int)
    major_id = request.args.get("major_id", type=int)
    class_id = request.args.get("class_id", type=int)

    # query gốc
    query = Student.query \
        .join(ClassModel) \
        .join(Major) \
        .join(Faculty)

    if faculty_id:
        query = query.filter(Faculty.id == faculty_id)

    if major_id:
        query = query.filter(Major.id == major_id)

    if class_id:
        query = query.filter(ClassModel.id == class_id)

    students = query.all()

    faculties = Faculty.query.all()
    majors = Major.query.all()
    classes = ClassModel.query.all()

    return render_template(
        "students/list.html",
        students=students,
        faculties=faculties,
        majors=majors,
        classes=classes,
        faculty_id=faculty_id,
        major_id=major_id,
        class_id=class_id
    )

# Thêm sinh viên
@admin_bp.route("/admin/students/add", methods=["GET", "POST"])
@login_required
@admin_required
def add_student():
    faculties = Faculty.query.all()
    majors = Major.query.all()
    classes = ClassModel.query.all()

    if request.method == "POST":
        try:
            name = request.form["name"]
            date_of_birth = datetime.strptime(
                request.form["date_of_birth"], "%Y-%m-%d"
            )
            class_id = int(request.form["class_id"])

            student_class = ClassModel.query.get_or_404(class_id)
            mssv = generate_mssv(student_class)

            student = Student(
                mssv=mssv,
                name=name,
                date_of_birth=date_of_birth,
                class_id=class_id
            )

            db.session.add(student)
            db.session.commit()

            flash(f"Đã thêm sinh viên (MSSV: {mssv})", "success")
            return redirect("/admin/students")

        except IntegrityError:
            db.session.rollback()
            flash("Trùng MSSV, vui lòng thử lại", "danger")

        except Exception as e:
            db.session.rollback()
            flash(f"Lỗi: {str(e)}", "danger")

    return render_template(
        "students/add.html",
        faculties=faculties,
        majors=majors,
        classes=classes
    )


# Sửa sinh viên
@admin_bp.route("/admin/students/edit/<int:id>", methods=["GET", "POST"])
@login_required
@admin_required
def edit_student(id):
    student = Student.query.get_or_404(id)
    faculties = Faculty.query.all()
    classes = ClassModel.query.all()

    if request.method == "POST":
        new_class_id = int(request.form["class_id"])

        student.name = request.form["name"]
        student.date_of_birth = datetime.strptime(
            request.form["date_of_birth"], "%Y-%m-%d"
        )

        # Nếu đổi lớp → sinh lại MSSV
        if student.class_id != new_class_id:
            student_class = ClassModel.query.get_or_404(new_class_id)
            student.mssv = generate_mssv(student_class)
            student.class_id = new_class_id

        db.session.commit()
        flash("Cập nhật sinh viên thành công", "success")
        return redirect("/admin/students")

    return render_template(
        "students/edit.html",
        student=student,
        faculties=faculties,
        classes=classes
    )

# Xoá sinh viên
@admin_bp.route("/admin/students/delete/<int:id>")
@login_required
@admin_required
def delete_student(id):
    student = Student.query.get_or_404(id)

    if student.user:
        db.session.delete(student.user)

    db.session.delete(student)
    db.session.commit()

    flash("🗑️ Đã xoá sinh viên", "success")
    return redirect("/admin/students")


# Tạo tài khoản
@admin_bp.route("/admin/students/create-account-bulk", methods=["POST"])
@login_required
@admin_required
def create_student_account_bulk():
    student_ids = request.form.getlist("student_ids")

    if not student_ids:
        flash("Chưa chọn sinh viên nào", "warning")
        return redirect("/admin/students")

    created = 0

    for sid in student_ids:
        student = Student.query.get(int(sid))

        if not student or student.user_id or not student.mssv:
            continue

        # username = MSSV
        if User.query.filter_by(username=student.mssv).first():
            continue

        user = User(
            username=student.mssv,
            password=generate_password_hash("123456"),
            full_name=student.name,
            email=f"{student.mssv}@student.clould",
            role="student",
            must_change_password=True
        )

        db.session.add(user)
        db.session.flush()

        student.user_id = user.id
        created += 1

    db.session.commit()
    flash(f"Đã cấp {created} tài khoản sinh viên", "success")
    return redirect("/admin/students")

# Xem thông tin sinh viên
@admin_bp.route("/admin/students/view/<int:id>")
@login_required
@admin_required
def view_student(id):
    student = Student.query.get_or_404(id)
    return render_template(
        "students/view.html",
        student=student
    )

