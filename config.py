import os 
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key-change-me-in-production")
    SQLALCHEMY_DATABASE_URL = os.environ.get(
        "DATABASE_URL", "sqlite:///" + os.path.join(basedir, "booking.db")
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = True