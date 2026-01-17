from .models import Meeting

def has_conflict(participants, start, end):
    return Meeting.objects.filter(
        participants__in=participants,
        start_time__lt=end,
        end_time__gt=start
    ).exists()


from django.core.mail import send_mail
from django.conf import settings

def send_meeting_email(participant_email, meeting):
    subject = f"Meeting Scheduled: {meeting.title}"
    message = f"""
You have been invited to a meeting.

Title: {meeting.title}
Description: {meeting.description}
Start Time: {meeting.start_time}
End Time: {meeting.end_time}

Thank you.
"""
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [participant_email],
        fail_silently=False,
    )
