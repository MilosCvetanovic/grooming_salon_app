import os
from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from grooming_salon.services.models import Appointment
from grooming_salon.utils.validators import validate_file_size

UserModel = get_user_model()

MAX_LENGTH = 500

# Create your models here.
#-----------------------------------------------------------------------------------------------------------------------
class Review(models.Model):
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], null=False, blank=False)
    description = models.TextField(max_length=MAX_LENGTH, null=True, blank=True)
    picture = models.ImageField(upload_to='images/reviews/', validators=[validate_file_size], null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE, related_name='review')

    def __str__(self):
        return f'Recenziju za {self.appointment}'

    @property
    def filename(self):
        return os.path.basename(self.picture.name)

#-----------------------------------------------------------------------------------------------------------------------
class ReviewLike(models.Model):
    to_review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)

    # Osiguravamo da jedan korisnik može lajkovati recenziju samo jednom
    class Meta:
        unique_together = ('to_review', 'user')

    def __str__(self):
        return f'{self.user} je lajkovao {self.to_review}'

#-----------------------------------------------------------------------------------------------------------------------
