from django.urls import path
from .views import *

urlpatterns = [
    path('meetings/create/', MeetingCreateView.as_view()),
    path('meetings/', MeetingListView.as_view()),
    path('meetings/<int:meeting_id>/', MeetingDetailView.as_view()),
    path('meetings/<int:meeting_id>/ics/', MeetingICSView.as_view()),
    path('meetings/<int:meeting_id>/add-participants/', AddParticipantView.as_view()),
]
