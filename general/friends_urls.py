from django.urls import path
from general.views import CreateFriendRequestAPIView, FriendRequestsListAPIView, FriendsListAPIView,FriendRequestStatusAPIView

urlpatterns=[
    path('create',CreateFriendRequestAPIView.as_view(),name="friend-create"),
    path('<int:user_id>',FriendsListAPIView.as_view(),name="friends"),
    path('requests/<int:user_id>',FriendRequestsListAPIView.as_view(),name="friends-requests"),
    path('<int:id>/<str:status>',FriendRequestStatusAPIView.as_view(),name="friend-request-accept"),
]