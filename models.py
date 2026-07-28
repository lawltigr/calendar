from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from extensions import db

class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    courses = db.relationship("course", backref="instructor", lazy=True)
    bookings = db.relationship("booking", backref="user", lazy=True)
    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)
    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)
    
class Course(db.Model):
    __tablename__ = "courses"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=True)
    instructor_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    sessions = db.relationship(
        "CourseSession", backref="course", lazy=True, cascade="all, delete-orphan", order_by="CourseSession.start_time",
    )
class CourseSession(db.Model):
    """Course session on the exact time/date."""
    __tablename__ = "course_sessions"
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey("courses.id"), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False, index=True)
    end_time = db.Column(db.DateTime, nullable=False)
    location = db.Column(db.String(150), nullable=True)
    capacity = db.Column(db.Integer, nullable=False, default=10)
    bookings = db.relationship("Booking", backref="session", lazy=True, cascade="all, delete-orphan")

@property
def active_bookings(self):
    return [b for b in self.bookings if b.status == "active"]
@property
def booked_count(self) -> int:
    return len(self.active_bookings)
@property
def spots_left(self) -> int:
    return max(self.capacity - self.booked_count, 0)
@property
def is_full(self) -> bool:
    return self.spots_left <=0
@property
def is_past(self) -> bool:
    return self.start_time < datetime.utcnow()
def user_booking(self, user_id):
    for b in self.bookings:
        if b.user_id == user_id and b.status == "active":
            return b
        return None
    
class Booking(db.Model):
    __tablename__ = "bookings"
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.Integer, db.ForeignKey("course_sessions.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    status = db.Column(db.String(20), nullable=False, default="active") # active| cancelled
    created_at = db.Column(db.DateTime, default=datetime.utcnow)