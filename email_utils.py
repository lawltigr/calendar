from flask_mail import Message
from extensions import mail

def send_booking_confirmation(user, session_obj):
    msg = Message(
        subject=f"Booking confirmed: {session_obj.course.title}",
        recipients=[user.email],
        body=(
            f"Hi {user.username},\n\n"
            f"You are signed up for:\n"
            f"{session_obj.course.title}\n"
            f"Date and time: {session_obj.start_time.strftime('%d.%m.%Y %H:%M')}\n"
            f"Location: {session_obj.location or 'not specified'}\n\n"
            f"See you there!"
        ),
    )
    mail.send(msg)

def send_cancellation_notice(user, session_obj):
    msg = Message(
        subject=f"Booking cancelled: {session_obj.course.title}",
        recipients=[user.email],
        body=(
            f"Hi {user.username},\n\n"
            f"Your booking has been cancelled:\n"
            f"{session_obj.course.title}\n"
            f"Date and time: {session_obj.start_time.strftime('%d.%m.%Y %H:%M')}\n"
            f"Location: {session_obj.location or 'not specified'}\n\n"
            f"You can book again any time while the spots are available."
        ),
    )
    mail.send(msg)

def send_course_deleted_notice(username, email, course_title, session_times):
    lines = "\n".join(f"- {t.strftime('%d.%m.%Y %H:%M')}" for t in session_times)
    msg = Message(
        subject=f"Course removed: {course_title}",
        recipients=[email],
        body=(
            f"Hi {username},\n\n"
            f"The course '{course_title} was removed by an administrator,"
            f"so your bookings for these sessions were cancelled:\n"
            f"{lines}\n\n"
            f"We apologize for the inconvenience."
        ),
    )
    mail.send(msg)