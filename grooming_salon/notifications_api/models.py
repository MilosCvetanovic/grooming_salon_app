from django.contrib.auth import get_user_model
from django.db import models
from grooming_salon.services.models import Appointment

UserModel = get_user_model()

MAX_LENGTH = 30

# Create your models here.
#-----------------------------------------------------------------------------------------------------------------------
class Notification(models.Model):
    class NotificationType(models.TextChoices):
        APPOINTMENT_BOOKED = 'appointment_booked', 'Appointment Booked'
        APPOINTMENT_COMPLETED = 'appointment_completed', 'Appointment Completed'
        APPOINTMENT_CANCELLED = 'appointment_canceled', 'Appointment Canceled'
        APPOINTMENT_REMINDER = 'appointment_reminder', 'Appointment Reminder'
        VOUCHER_CREATED = 'voucher_created', 'Voucher Created'

    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='notifications')
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE, related_name='notifications', null=True, blank=True)
    notification_type = models.CharField(max_length=MAX_LENGTH, choices=NotificationType)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.notification_type} - {self.user} - {self.created_at}"

#-----------------------------------------------------------------------------------------------------------------------
