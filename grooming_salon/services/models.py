from datetime import datetime, timedelta
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import UniqueConstraint, Q
from grooming_salon.dogs.models import Dog
from grooming_salon.services.managers import AppointmentManager

UserModel = get_user_model()

MAX_LENGTH = 30
STATUS_CHOICES = [
    ('BOOKED', 'Booked'),
    ('COMPLETED', 'Completed'),
    ('CANCELLED', 'Cancelled'),
]

# Create your models here.
#-----------------------------------------------------------------------------------------------------------------------
class Service(models.Model):
    name = models.CharField(max_length=MAX_LENGTH, null=False, blank=False)
    picture = models.ImageField(upload_to='images/services/')

    def __str__(self):
        return self.name

#-----------------------------------------------------------------------------------------------------------------------
class Groomer(models.Model):
    name = models.CharField(max_length=MAX_LENGTH, null=False, blank=False)
    picture = models.ImageField(upload_to='images/groomers/')

    def __str__(self):
        return self.name

#-----------------------------------------------------------------------------------------------------------------------
class Appointment(models.Model):
    date = models.DateField()
    time = models.TimeField()
    status = models.CharField(max_length=MAX_LENGTH, choices=STATUS_CHOICES, default='BOOKED')
    created_at = models.DateTimeField(auto_now_add=True)
    services = models.ManyToManyField(Service, related_name='appointments')
    groomer = models.ForeignKey(Groomer, on_delete=models.CASCADE)
    dog = models.ForeignKey(Dog, on_delete=models.CASCADE)
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='appointments')

    objects = AppointmentManager()

    class Meta:
        ordering = ['date', 'time']
        constraints = [
            UniqueConstraint(
                fields=['date', 'time', 'groomer'],
                condition=Q(status='BOOKED'),
                name='unique_active_appointment'
        )]

    def __str__(self):
        return f'{self.id} - {self.groomer.name} - {self.date} {self.time}'

    # Ako je termin prošao, postavi njegov status na COMPLETED
    def mark_completed_if_past(self):
        if self.status != 'BOOKED':
            return False

        appointment_start = timezone.make_aware(datetime.combine(self.date, self.time))

        if timezone.now() > (appointment_start + timedelta(hours=1)):
            self.status = 'COMPLETED'
            self.save()
            return True

        return False

#-----------------------------------------------------------------------------------------------------------------------
