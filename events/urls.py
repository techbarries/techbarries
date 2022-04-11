from events.views import CreateEventAPIView, EventListAPIView,UniversityAPIView 
from django.urls import path

urlpatterns=[
    path('create',CreateEventAPIView.as_view(),name="event-create"),
    path('events/<int:user_id>',EventListAPIView.as_view(),name="events"),
]