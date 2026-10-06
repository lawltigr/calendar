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