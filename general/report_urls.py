from django.urls import path
from general.views import CreateFriendRequestAPIView, CreateReportAPIView,InviteByPhoneAPIView, FriendRequestsListAPIView, FriendsListAPIView,FriendRequestStatusAPIView

urlpatterns=[
    path('create',CreateReportAPIView.as_view(),name="report-create"),
]