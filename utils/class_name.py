from sqlalchemy import func
from models.class_model import ClassModel
from models import db

def generate_class_name(major, course):
    if not major.code or not course.code:
        raise ValueError("Ngành hoặc khoá học chưa có mã (code)")

    prefix = f"{major.code}-{course.code}"

    last_class = (
        ClassModel.query
        .filter(ClassModel.name.like(f"{prefix}-%"))
        .order_by(ClassModel.name.desc())
        .first()
    )

    if last_class:
        last_stt = int(last_class.name.split("-")[-1])
        next_stt = last_stt + 1
    else:
        next_stt = 1

    return f"{prefix}-{next_stt:02d}"

