from django.urls import path, include
from grooming_salon.dogs import views

#-----------------------------------------------------------------------------------------------------------------------
urlpatterns = [
    path('add/', views.AddDogView.as_view(), name='add_dog'),
    path('dog/<slug:dog_slug>/', include([
        path('', views.DogDetailsView.as_view(), name='dog_details'),
        path('edit/', views.EditDogView.as_view(), name='edit_dog'),
        path('delete/', views.DeleteDogView.as_view(), name='delete_dog'),
    ])),
]

#-----------------------------------------------------------------------------------------------------------------------
