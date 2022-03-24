from events.views import UniversityAPIView,UniversityListAPIView 
from django.urls import path

urlpatterns=[
    path('',UniversityListAPIView.as_view(),name="universities"),
    path('<int:id>',UniversityAPIView.as_view(),name="university")
]