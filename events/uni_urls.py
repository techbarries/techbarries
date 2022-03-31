from events.views import CreateUniversityAPIView, UniversityAPIView,UniversityListAPIView 
from django.urls import path

urlpatterns=[
    path('',UniversityListAPIView.as_view(),name="universities"),
    path('create',CreateUniversityAPIView.as_view(),name="university-create"),
    path('<int:id>',UniversityAPIView.as_view(),name="university")
]