from django.urls import path
from general.views import CreateNotificationAPIView,NotificationAPIView,NotificationListAPIView

urlpatterns=[
    path('',NotificationAPIView.as_view(),name="notifications"),
    path('create',CreateNotificationAPIView.as_view(),name="notification-create"),
    path('<int:user_id>',NotificationListAPIView.as_view(),name="notification")
]