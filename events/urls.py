from events.views import CreateEventAPIView, EventListAPIView, PastEventListAPIView,UniversityAPIView, UpcomingEventListAPIView 
from django.urls import path

urlpatterns=[
    path('create',CreateEventAPIView.as_view(),name="event-create"),
    path('events/<int:user_id>',EventListAPIView.as_view(),name="events"),
    path('events/<int:user_id>/past',PastEventListAPIView.as_view(),name="events"),
    path('events/<int:user_id>/upcoming',UpcomingEventListAPIView.as_view(),name="events"),
]