from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from extensions import db
from models import Course, CourseSession, Booking
from forms import CourseForm, SessionForm
main_bp = Blueprint("main", __name__)

@main_bp.route("/")
def index():
    return redirect(url_for("main.dashboard"))

@main_bp.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html")

@main_bp.route("/api/sessions")
@login_required
def api_sessions():
    """JSON events for the calendar (FullCalendar.)"""
    sessions = CourseSession.query.join(Course).all()
    events = []
    for s in sessions:
        my_booking = s.user_booking(current_user.id)
        if my_booking:
            color = "#198754"
        elif s.is_full:
            color = "#6c757d"
        elif s.is_past:
            color = "#adb5bd"
        else:
            color = "#0d6efd"
        events.append(
            {
                "id": s.id,
                "title": f"{s.course.title} ({s.booked_count}/{s.capacity})",
                "start": s.start_time.isoformat(),
                "end": s.end_time.isoformat(),
                "url": url_for("main.session_detail", session_id=s.id),
                "color": color,
            }
        )
        return jsonify(events)

@main_bp.route("/courses")
@login_required
def courses_list():
    courses = Course.query.order_by(Course.title).all()
    return render_template("courses_list.html", courses=courses)

@main_bp.route("/courses/<int:course_id>")
@login_required
def course_detail(course_id):
    course = Course.query.get_or_404(course_id)
    return render_template("course_detail.html", course=course)

@main_bp.route("/courses/neq", methods=["GET", "POST"])
@login_required
def course_new():
    form = CourseForm()
    if form.validate_on_submit():
        course = Course(
            title=form.title.data.strip(),
            description=form.description.data,
            instructor_id=current_user.id,
        )
        db.session.add(course)
        db.session.commit()
        flash("Course created! Now, add at least one class.", "success")
        return redirect(url_for("main.course_detail", course_id=course.id))
    return render_template("course_form.html", form=form)

@main_bp.route("/courses/<int:course_id>/sessions/new", methods=["GET", "POST"])
@login_required
def session_new(course_id):
    course = Course.query.get_or_404(course_id)
    if course.instructor_id !=current_user.id:
        flash("Only the owner of the course can add classes.", "danger")
        return redirect(url_for("main.course_detail", course_id=course.id))
    form = SessionForm()
    if form.validate_on_submit():
        session_obj = CourseSession(
            course_id=course.id,
            start_time=form.start_time.data,
            end_time=form.end_time.data,
            location=form.location.data,
            capacity=form.capacity.data,
        )
        db.session.add(session_obj)
        db.session.commit()
        flash("Class is added to the schedule.", "success")
        return redirect(url_for("main.course_detail", course_id=course.id))
    return render_template("session_form.html", form=form, course=course)

@main_bp.route("/sessions/<int:session_id>/book", methods=["POST"])
@login_required
def session_book(session_id):
    s = CourseSession.query.get_or_404(session_id)
    if s.is_past:
        flash("Cannot sign up for the class that is over.", "danger")
        return redirect(url_for("main.session_detail", session_id=session_id))
    if s.user_booking(current_user.id):
        flash("You are already signed up for this class.", "info")
        return redirect(url_for("main.session_detail", session_id=session_id))
    if s.is_full:
        flash("Unfortunately, all spots are booked.", "danger")
        return redirect(url_for("main.session_detail", session_id=session_id))
    overlapping = (CourseSession.query.join(Booking).filter(
        Booking.user_id == current_user.id,
        Booking.status == "active",
        CourseSession.start_time < s.end_time,
        CourseSession.end_time > s.start_time,
    ).first())
    if overlapping:
        flash(
            f"You already have a booking for this time: '{overlapping.course.title}'"
            f"({overlapping.start_time.strftime('%d.%m.%Y %H:%M')}).", 
            "danger",
        )
        return redirect(url_for("main.session_detail", session_id=session_id))
    Booking = Booking(session_id=s.id, user_id=current_user.id, status="active")
    db.session.add(booking)
    db.session.commit()
    flash("You successfully signed up for the class!", "success")
    return redirect(url_for("main.session_detail", session_id=session_id))

@main_bp.route("/sessions/<int:session_id>/cancel", methods=["POST"])
@login_required
def session_cancel(session_id):
    pass