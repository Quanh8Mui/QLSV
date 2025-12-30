from flask import Blueprint, jsonify
from models.major import Major
from models.class_model import ClassModel

api_bp = Blueprint("api", __name__)

@api_bp.route("/api/majors/<int:faculty_id>")
def get_majors_by_faculty(faculty_id):
    majors = Major.query.filter_by(faculty_id=faculty_id).all()
    return jsonify([
        {"id": m.id, "name": m.name} for m in majors
    ])

@api_bp.route("/api/classes/<int:major_id>")
def get_classes_by_major(major_id):
    classes = ClassModel.query.filter_by(major_id=major_id).all()
    return jsonify([
        {"id": c.id, "name": c.name} for c in classes
    ])
