from authentication.views import RegisterAPIView,UserListAPIView
from django.urls import path

urlpatterns=[
    path('register',RegisterAPIView.as_view(),name="register"),
    path('users',UserListAPIView.as_view(),name="register")
]