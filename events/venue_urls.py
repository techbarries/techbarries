from events.views import CreateVenueAPIView,RequestVenueAPIView, VenueDetailAPIView,VenueStatusAPIView, VenuePopularListAPIView,VenueListAPIView, VenueNearMeListAPIView, VerifyVenueCheckInAPIView
from django.urls import path

urlpatterns=[
    # path('',VenueListAPIView.as_view(),name="venues"),
    path('<int:venue_id>/verify/<str:latitude>/<str:longitude>',VerifyVenueCheckInAPIView.as_view(),name="venue-verify"),
    path('<int:user_id>/<str:latitude>/<str:longitude>',VenueListAPIView.as_view(),name="venues"),
    path('popular/<int:user_id>/<str:latitude>/<str:longitude>',VenuePopularListAPIView.as_view(),name="venues"),
    path('near-me/<int:user_id>/<str:latitude>/<str:longitude>',VenueNearMeListAPIView.as_view(),name="venues"),
    path('create',CreateVenueAPIView.as_view(),name="venue-create"),
    path('request',RequestVenueAPIView.as_view(),name="request-venue"),
    path('detail/venue/<int:venue_id>/user/<int:user_id>',VenueDetailAPIView.as_view(),name="venue-details-update"),
    path('<int:venue_id>/user/<int:user_id>/<slug:status>',VenueStatusAPIView.as_view(),name="venue-status-update"),
    # path('<int:id>',VenueAPIView.as_view(),name="venue")
]