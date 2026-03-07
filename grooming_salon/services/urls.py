from django.urls import path
from grooming_salon.services import views

#-----------------------------------------------------------------------------------------------------------------------
urlpatterns = [
    path('', views.ServicesPageView.as_view(), name='services'),
    path('groomers/', views.GroomerPageView.as_view(), name='groomers'),
    path('appointments/', views.AppointmentBookingView.as_view(), name='appointments'),
    path('dog-selection/', views.DogSelectionView.as_view(), name='dog_selection'),
    path('confirmation/', views.ConfirmAppointmentView.as_view(), name='confirmation'),
    path('my-appointments/', views.MyAppointmentsView.as_view(), name='my_appointments'),
    path('appointments/<int:appointment_id>/cancel/', views.cancel_appointment, name='cancel_appointment')
]

#-----------------------------------------------------------------------------------------------------------------------
