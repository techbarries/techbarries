from authentication.views import DetailUserAPIView, DeviceByUserView,DeleteUserAPIView, PulseUserAPIView, UserByTokenView,UserListAPIView
from django.urls import path

urlpatterns=[
    path('pulse-user',PulseUserAPIView.as_view(),name="pulseUser"),
    path('user/<int:id>/delete',DeleteUserAPIView.as_view(),name="pulseUserDelete"),
    path('user/<int:user_id>/detail',DetailUserAPIView.as_view(),name="pulseUserDetail"),
    path('users',UserListAPIView.as_view(),name="users"),
    path('user/<int:user_id>/devices',DeviceByUserView.as_view(),name="device-by-user"),
    path('user/uid/<slug:uid>',UserByTokenView.as_view(),name="user-by-token")
]