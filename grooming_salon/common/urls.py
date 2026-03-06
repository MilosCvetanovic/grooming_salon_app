from django.urls import path
from grooming_salon.common import views

urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
]