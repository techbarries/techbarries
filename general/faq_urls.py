from django.urls import path
from general.views import FaqListApiView

urlpatterns=[
       path('',FaqListApiView.as_view(),name="faqs"),
]