from events.views import VenueAPIView,VenueListAPIView
from django.urls import path

urlpatterns=[
    path('',VenueListAPIView.as_view(),name="venues"),
    path('<int:id>',VenueAPIView.as_view(),name="venue")
]