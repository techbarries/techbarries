from events.views import CreateVenueAPIView, VenuePopularListAPIView,VenueListAPIView, VenueNearMeListAPIView
from django.urls import path

urlpatterns=[
    # path('',VenueListAPIView.as_view(),name="venues"),
    path('<int:user_id>',VenueListAPIView.as_view(),name="venues"),
    path('popular/<int:user_id>',VenuePopularListAPIView.as_view(),name="venues"),
    path('near-me/<int:user_id>/<str:latitude>/<str:longitude>',VenueNearMeListAPIView.as_view(),name="venues"),
    path('create',CreateVenueAPIView.as_view(),name="venue-create"),
    # path('<int:id>',VenueAPIView.as_view(),name="venue")
]