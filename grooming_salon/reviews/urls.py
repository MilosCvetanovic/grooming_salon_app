from django.urls import path
from grooming_salon.reviews import views

#-----------------------------------------------------------------------------------------------------------------------
urlpatterns = [
    path('add/<int:appointment_id>/', views.AddReviewView.as_view(), name='add_review'),
    path('edit/<int:appointment_id>/', views.EditReviewView.as_view(), name='edit_review'),
    path('delete/<int:appointment_id>/', views.DeleteReviewView.as_view(), name='delete_review'),
    path('', views.ReviewDetailsView.as_view(), name='review_details'),
    path('like/<int:review_pk>/', views.ReviewLikeView.as_view(), name='toggle_like')
]

#-----------------------------------------------------------------------------------------------------------------------
