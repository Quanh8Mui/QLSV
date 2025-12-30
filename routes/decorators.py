from flask_login import current_user
from flask import abort
from functools import wraps

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            abort(401)  # chưa đăng nhập
        if current_user.role != "admin":
            abort(403)  # không đủ quyền
        return f(*args, **kwargs)
    return decorated_function

def student_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            abort(401)  # chưa đăng nhập
        if current_user.role != "student":
            abort(403)  # không đủ quyền
        return f(*args, **kwargs)
    return decorated_function

