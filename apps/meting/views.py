from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse
from icalendar import Calendar, Event
from .models import Meeting
from .serializers import *


#meeting create view
class MeetingCreateView(APIView):
    def post(self, request):
        serializer = MeetingSerializer(data=request.data)
        if serializer.is_valid():
            meeting = serializer.save()
            return Response(MeetingSerializer(meeting).data, status=201)
        return Response(serializer.errors, status=400)

#meeting list view
class MeetingListView(APIView):
    def get(self, request):
        meetings = Meeting.objects.all()
        return Response(MeetingListSerializer(meetings, many=True).data)

#meeting detail view
class MeetingDetailView(APIView):
    def get(self, request, meeting_id):
        meeting = Meeting.objects.get(id=meeting_id)
        return Response(MeetingDetailSerializer(meeting).data)


#meeting ics view
class MeetingICSView(APIView):
    def get(self, request, meeting_id):
        meeting = Meeting.objects.get(id=meeting_id)

        cal = Calendar()
        cal.add("prodid", "-//Meeting Scheduler//EN")
        cal.add("version", "2.0")

        event = Event()
        event.add("summary", meeting.title)
        event.add("dtstart", meeting.start_time)
        event.add("dtend", meeting.end_time)
        event.add("description", meeting.description)

        cal.add_component(event)

        ics_content = cal.to_ical()

        response = HttpResponse(
            ics_content,
            content_type="application/octet-stream",
        )
        response["Content-Disposition"] = (
            f'attachment; filename="meeting_{meeting.id}.ics"'
        )

        return response

# add participant view
class AddParticipantView(APIView):

    def patch(self, request, meeting_id):
        meeting = Meeting.objects.get(id=meeting_id)
        participants_data = request.data.get("participants", [])

        new_participants = []

        for p in participants_data:
            obj, _ = Participant.objects.get_or_create(email=p["email"])
            new_participants.append(obj)


        if has_conflict(
            new_participants,
            meeting.start_time,
            meeting.end_time,
        ):
            return Response(
                {"error": "Participant has a conflicting meeting."},
                status=status.HTTP_400_BAD_REQUEST,
            )


        for p in new_participants:
            meeting.participants.add(p)
            send_meeting_email(p.email, meeting)

        return Response(
            {"message": "Participants added successfully"},
            status=status.HTTP_200_OK,
        )
