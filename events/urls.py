from events.views import CreateEventAPIView, EventListAPIView, EventStatusAPIView, PastEventListAPIView, UpcomingEventListAPIView 
from django.urls import path

urlpatterns=[
    path('create',CreateEventAPIView.as_view(),name="event-create"),
    path('<int:event_id>/user/<int:user_id>/<slug:status>',EventStatusAPIView.as_view(),name="event-status-update"),
    path('events/<int:user_id>',EventListAPIView.as_view(),name="events"),
    path('events/<int:user_id>/past',PastEventListAPIView.as_view(),name="events"),
    path('events/<int:user_id>/upcoming',UpcomingEventListAPIView.as_view(),name="events"),
]