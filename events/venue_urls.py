from events.views import CreateVenueAPIView, VenueAPIView,VenueListAPIView
from django.urls import path

urlpatterns=[
    # path('',VenueListAPIView.as_view(),name="venues"),
    path('<int:user_id>',VenueListAPIView.as_view(),name="venues"),
    path('create',CreateVenueAPIView.as_view(),name="venue-create"),
    # path('<int:id>',VenueAPIView.as_view(),name="venue")
]