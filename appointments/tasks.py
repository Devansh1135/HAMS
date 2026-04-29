from celery import shared_task
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags


@shared_task
def send_appointment_confirmation_mail(appointment_id):
    from appointments.models import Appointment

    try:
        appointment = Appointment.objects.get(id=appointment_id)
    except Appointment.DoesNotExist:
        print(f"Appointment {appointment_id} not found")
        return

    context = {
        "patient_name": appointment.patient.user.username,
        "doctor_name": f"Dr. {appointment.doctor.user.first_name} {appointment.doctor.user.last_name}",
        "appointment_date": appointment.day,
        "appointment_time": appointment.time_slot,
    }

    html_message = render_to_string(
        "appointments/appointment_confirmation.html", context
    )
    plain_message = strip_tags(html_message)

    try:
        send_mail(
            subject="Appointment Confirmation",
            message=plain_message,
            html_message=html_message,
            from_email="devanshjagatiya1135@gmail.com",
            recipient_list=[appointment.patient.user.email],
            fail_silently=False,
        )
        print(f"Email sent to {appointment.patient.user.email}")
    except Exception as e:
        print(f"Error sending email: {e}")
