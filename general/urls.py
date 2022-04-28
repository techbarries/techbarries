from django.urls import path
from general.views import CreateNotificationAPIView,NotificationAPIView,NotificationListAPIView,NotificationMarkReadAPIView

urlpatterns=[
    path('',NotificationAPIView.as_view(),name="notifications"),
    path('create',CreateNotificationAPIView.as_view(),name="notification-create"),
    path('<int:user_id>',NotificationListAPIView.as_view(),name="notification"),
    path('<int:user_id>/mark-read',NotificationMarkReadAPIView.as_view(),name="notification-mark-read"),
    path('<int:user_id>/mark-read/<int:id>',NotificationMarkReadAPIView.as_view(),name="notification-mark-read")
]