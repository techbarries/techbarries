from events.views import CreateEventAPIView,UniversityAPIView 
from django.urls import path

urlpatterns=[
    path('create',CreateEventAPIView.as_view(),name="event-create")
]