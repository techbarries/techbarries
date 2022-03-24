from events import views
from django.urls import path

urlpatterns=[
    path('create',views.CreateEventAPIView.as_view(),name="event-create")
]