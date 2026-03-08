from django.contrib import admin
from grooming_salon.notifications_api.models import Notification

# Register your models here.
#-----------------------------------------------------------------------------------------------------------------------
@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'appointment', 'notification_type', 'message', 'is_read', 'created_at',)
    search_fields = ('id',)
    ordering = ('created_at',)

#-----------------------------------------------------------------------------------------------------------------------
