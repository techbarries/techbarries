from events.views import CreateEventAPIView, EventImageDeleteAPIView,EventShareAPIView, EventListAPIView,EventNearMeListAPIView, EventStatusAPIView, PastEventListAPIView, UpcomingEventListAPIView 
from django.urls import path

urlpatterns=[
    path('create',CreateEventAPIView.as_view(),name="event-create"),
    path('image/delete/<int:id>',EventImageDeleteAPIView.as_view(),name="event-image-delete"),
    path('<int:event_id>/user/<int:user_id>/share/to-user/<int:to_user_id>',EventShareAPIView.as_view(),name="event-status-update"),
    path('<int:event_id>/user/<int:user_id>/<slug:status>',EventStatusAPIView.as_view(),name="event-status-update"),
    path('events/<int:user_id>',EventListAPIView.as_view(),name="events"),
    path('near-me/events/<int:user_id>/<str:latitude>/<str:longitude>',EventNearMeListAPIView.as_view(),name="events"),
    path('events/<int:user_id>/past',PastEventListAPIView.as_view(),name="events"),
    path('events/<int:user_id>/upcoming',UpcomingEventListAPIView.as_view(),name="events"),
]