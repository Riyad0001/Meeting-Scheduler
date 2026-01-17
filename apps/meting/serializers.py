from rest_framework import serializers
from .models import Meeting, Participant
from .services import has_conflict,send_meeting_email

from rest_framework import serializers
from .models import Meeting, Participant

class MeetingListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meeting
        fields = ["id", "title", "start_time", "end_time"]


class ParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participant
        fields = ["id", "email"]


class MeetingDetailSerializer(serializers.ModelSerializer):
    participants = ParticipantSerializer(many=True)

    class Meta:
        model = Meeting
        fields = "__all__"



class MeetingSerializer(serializers.ModelSerializer):
    participants = ParticipantSerializer(many=True)

    class Meta:
        model = Meeting
        fields = "__all__"

    def create(self, validated_data):
        participants_data = validated_data.pop("participants")
        participants = []

        for p in participants_data:
            obj, _ = Participant.objects.get_or_create(email=p["email"])
            participants.append(obj)

        if has_conflict(participants, validated_data["start_time"], validated_data["end_time"]):
            raise serializers.ValidationError("Participant has a conflicting meeting.")

        meeting = Meeting.objects.create(**validated_data)
        meeting.participants.set(participants)


        for p in participants:
            send_meeting_email(p.email, meeting)

        return meeting
