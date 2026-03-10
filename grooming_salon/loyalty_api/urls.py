from django.urls import path, include
from rest_framework.routers import DefaultRouter
from grooming_salon.loyalty_api import views

# Kreiramo ruter
router = DefaultRouter()

# Registrujemo ViewSet.
router.register(r'loyalty', views.LoyaltyViewSet, basename='loyalty')

urlpatterns = [
    # Sve rute koje ruter generiše uključujemo ovde
    path('', include(router.urls)),
]