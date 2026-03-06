from django.urls import path
from grooming_salon.accounts import views

#-----------------------------------------------------------------------------------------------------------------------
urlpatterns = [
    path('register/', views.AppUserRegisterView.as_view(), name='register'),
    path('login/', views.AppUserLoginView.as_view(), name='login'),
    path('logout/', views.AppUserLogoutView.as_view(), name='logout'),
    path('password/change/', views.AppUserPasswordChangeView.as_view(), name='password_change'),
    path('profile/', views.AppUserDetailView.as_view(), name='profile_details'),
    path('profile/edit/', views.ProfileEditView.as_view(), name='profile_edit'),
    path('profile/delete/', views.AppUserDeleteView.as_view(), name='profile_delete'),
]

#-----------------------------------------------------------------------------------------------------------------------
