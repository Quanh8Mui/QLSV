from app import app
from models import db
from models.faculty import Faculty
from models.major import Major
from models.course import Course
from models.class_model import ClassModel
from models.student import Student
from models.user import User
from werkzeug.security import generate_password_hash
from datetime import date
from utils.mssv import generate_mssv


def seed_data():
    with app.app_context():
        print("Reset database...")
        db.drop_all()
        db.create_all()

        # =====================
        # 1. FACULTIES (4)
        # =====================
        faculties = [
            Faculty(name="Công nghệ thông tin"),
            Faculty(name="Kinh tế"),
            Faculty(name="Kỹ thuật"),
            Faculty(name="Khoa học xã hội"),
        ]
        db.session.add_all(faculties)
        db.session.commit()

        f_cntt, f_kt, f_ktcn, f_xh = faculties

        # =====================
        # 2. MAJORS (8)
        # =====================
        majors = [
            Major(name="Công nghệ thông tin", code="CNTT", faculty_id=f_cntt.id),
            Major(name="Khoa học máy tính", code="KHMT", faculty_id=f_cntt.id),

            Major(name="Quản trị kinh doanh", code="QTKD", faculty_id=f_kt.id),
            Major(name="Kế toán", code="KT", faculty_id=f_kt.id),

            Major(name="Kỹ thuật điện", code="KTD", faculty_id=f_ktcn.id),
            Major(name="Kỹ thuật cơ khí", code="CK", faculty_id=f_ktcn.id),

            Major(name="Xã hội học", code="XHH", faculty_id=f_xh.id),
            Major(name="Tâm lý học", code="TLH", faculty_id=f_xh.id),
        ]
        db.session.add_all(majors)
        db.session.commit()

        # =====================
        # 3. COURSES (4)
        # =====================
        courses = [
            Course(name="K21", code="K21", start_year=2021),
            Course(name="K22", code="K22", start_year=2022),
            Course(name="K23", code="K23", start_year=2023),
            Course(name="K24", code="K24", start_year=2024),
        ]
        db.session.add_all(courses)
        db.session.commit()

        # =====================
        # 4. CLASSES (10)
        # =====================
        class_data = [
            ("CNTT-K21-01", majors[0], courses[0]),
            ("CNTT-K21-02", majors[0], courses[0]),
            ("KHMT-K22-01", majors[1], courses[1]),
            ("QTKD-K22-01", majors[2], courses[1]),
            ("KT-K21-01", majors[3], courses[0]),
            ("KTD-K24-01", majors[4], courses[3]),
            ("CK-K23-01", majors[5], courses[2]),
            ("XHH-K22-01", majors[6], courses[1]),
            ("TLH-K23-01", majors[7], courses[2]),
            ("CNTT-K24-01", majors[0], courses[3]),
        ]

        classes = []
        for name, major, course in class_data:
            c = ClassModel(name=name, major_id=major.id, course_id=course.id)
            classes.append(c)

        db.session.add_all(classes)
        db.session.commit()

        # =====================
        # 5. STUDENTS (10) + USER
        # =====================
        students_data = [
            ("Trần Văn A", date(2005, 1, 10), classes[0]),
            ("Nguyễn Thị B", date(2004, 9, 22), classes[0]),
            ("Lê Văn C", date(2005, 3, 15), classes[1]),
            ("Phạm Thị D", date(2004, 12, 1), classes[3]),
            ("Hoàng Văn E", date(2005, 6, 30), classes[3]),
            ("Phạm Minh Mẫn", date(2005, 12, 12), classes[5]),
            ("Nguyễn Thị Hà", date(2006, 6, 16), classes[9]),
            ("Lê Thị Lan", date(2005, 2, 8), classes[6]),
            ("Trần Quốc Huy", date(2004, 11, 19), classes[7]),
            ("Võ Thanh Tùng", date(2005, 7, 25), classes[8]),
        ]

        for name, dob, cls in students_data:
            mssv = generate_mssv(cls)

            student = Student(
                mssv=mssv,
                name=name,
                date_of_birth=dob,
                class_id=cls.id
            )
            db.session.add(student)
            db.session.flush()

            user = User(
                username=mssv,                 # username = MSSV
                password=generate_password_hash("123456"),
                full_name=name,
                email=f"{mssv.lower()}@student.local",
                role="student"
            )
            db.session.add(user)
            db.session.flush()

            student.user_id = user.id

        # =====================
        # 6. ADMIN
        # =====================
        admin = User(
            username="admin",
            password=generate_password_hash("admin123"),
            full_name="Administrator",
            email="admin@system.local",
            role="admin"
        )
        db.session.add(admin)

        db.session.commit()
        print("Seed dữ liệu hoàn tất!")


if __name__ == "__main__":
    seed_data()
