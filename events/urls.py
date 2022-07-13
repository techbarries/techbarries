from events.views import CreateEventAPIView, EventArchiveAPIView, EventImageDeleteAPIView,EventNotificaionStatusAPIView,EventShareAPIView, EventListAPIView,EventNearMeListAPIView, EventStatusAPIView, PastEventListAPIView, UpcomingEventListAPIView,EventDetailAPIView 
from django.urls import path

urlpatterns=[
    path('create',CreateEventAPIView.as_view(),name="event-create"),
    path('image/delete/<int:id>',EventImageDeleteAPIView.as_view(),name="event-image-delete"),
    path('share',EventShareAPIView.as_view(),name="event-status-update"),
    path('user/<int:user_id>/notificaion/<int:notificaion_id>/event/<int:event_id>/<slug:status>',EventNotificaionStatusAPIView.as_view(),name="event-notificaion-accept-update"),
    path('<int:event_id>/user/<int:user_id>',EventDetailAPIView.as_view(),name="event-detail"),
    path('<int:event_id>/archive',EventArchiveAPIView.as_view(),name="event-archive"),
    path('<int:event_id>/user/<int:user_id>/<slug:status>',EventStatusAPIView.as_view(),name="event-status-update"),
    path('events/<int:user_id>',EventListAPIView.as_view(),name="events"),
    path('near-me/events/<int:user_id>/<str:latitude>/<str:longitude>',EventNearMeListAPIView.as_view(),name="events"),
    path('events/<int:user_id>/past',PastEventListAPIView.as_view(),name="events"),
    path('events/<int:user_id>/upcoming',UpcomingEventListAPIView.as_view(),name="events"),
]