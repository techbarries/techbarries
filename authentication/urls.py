from authentication.views import DeviceByUserView, RegisterAPIView, UserByTokenView,UserListAPIView
from django.urls import path

urlpatterns=[
    path('pulse-user',RegisterAPIView.as_view(),name="pulseUser"),
    path('users',UserListAPIView.as_view(),name="users"),
    path('user/<int:user_id>/devices',DeviceByUserView.as_view({'get': 'list',}),name="device-by-user"),
    path('user/token/<slug:user_token>',UserByTokenView.as_view(),name="user-by-token")
]