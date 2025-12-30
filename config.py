import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SQLALCHEMY_DATABASE_URI = (
        "postgresql://neondb_owner:npg_psqlL6unhtF3@ep-twilight-brook-ahzge7zn-pooler.c-3.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "SECRET_KEY_DO_AN"

    UPLOAD_FOLDER = os.path.join(BASE_DIR, "static/uploads")
    ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}
    MAX_CONTENT_LENGTH = 2 * 1024 * 1024  # 2MB





