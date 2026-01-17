from django.test import TestCase
from .models import Meeting, Participant
from django.utils.timezone import now, timedelta

class MeetingTest(TestCase):

    def test_create_meeting(self):
        p = Participant.objects.create(email="a@test.com")
        meeting = Meeting.objects.create(
            title="Test",
            start_time=now(),
            end_time=now() + timedelta(hours=1),
        )
        meeting.participants.add(p)
        self.assertEqual(meeting.title, "Test")
