from rest_framework import serializers
from grooming_salon.notifications_api.models import Notification

# Create your serializers here.
#-----------------------------------------------------------------------------------------------------------------------
class NotificationSerializer(serializers.ModelSerializer):
    notification_type_display = serializers.CharField(source='get_notification_type_display', read_only=True)

    class Meta:
        model = Notification
        fields = 'id', 'notification_type', 'notification_type_display', 'message', 'is_read', 'created_at', 'appointment'
        read_only_fields = ['id', 'notification_type', 'notification_type_display', 'message', 'created_at', 'appointment']

#-----------------------------------------------------------------------------------------------------------------------
