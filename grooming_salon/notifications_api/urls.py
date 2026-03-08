from django.urls import path
from grooming_salon.notifications_api import views

#-----------------------------------------------------------------------------------------------------------------------
urlpatterns = [
    path('notifications/', views.NotificationListView.as_view(), name='notifications'),
    path('notifications/mark-all-read/', views.NotificationMarkAllReadView.as_view(), name='notifications_mark_all_read'),
    path('notifications/<int:pk>/mark-read/', views.NotificationMarkReadView.as_view(), name='notification_mark_read'),
    path('notifications/<int:pk>/delete/', views.NotificationDeleteView.as_view(), name='notification_delete'),
]

#-----------------------------------------------------------------------------------------------------------------------
