from models.student import Student

def generate_mssv(student_class):
    """
    MSSV dạng: SV21CNTT0001
    """

    # Khoá: K21 → 21
    course_code = student_class.course.code.replace("K", "")

    # Ngành: CNTT
    major_code = student_class.major.code

    prefix = f"SV{course_code}{major_code}"

    last_student = (
        Student.query
        .filter(Student.mssv.like(f"{prefix}%"))
        .order_by(Student.mssv.desc())
        .first()
    )

    next_stt = 1
    if last_student:
        next_stt = int(last_student.mssv[-4:]) + 1

    return f"{prefix}{next_stt:04d}"
