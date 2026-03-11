import os
from datetime import date
from django.contrib.auth import get_user_model
from django.db import models
from django.utils.text import slugify
from grooming_salon.utils.validators import validate_capitalized_name, validate_file_size

UserModel = get_user_model()

MAX_LENGTH = 50

# Create your models here.
#-----------------------------------------------------------------------------------------------------------------------
class Note(models.Model):
    condition = models.CharField(max_length=MAX_LENGTH, null=False, blank=False)

#-----------------------------------------------------------------------------------------------------------------------
class Dog(models.Model):
    name = models.CharField(max_length=MAX_LENGTH, validators=[validate_capitalized_name], null=False, blank=False)
    date_of_birth = models.DateField(null=False, blank=False)
    breed = models.CharField(max_length=MAX_LENGTH, validators=[validate_capitalized_name], null=False, blank=False)
    picture = models.ImageField(upload_to='images/dogs/', validators=[validate_file_size], null=True, blank=True)
    slug = models.SlugField(unique=True, null=False, blank=False, editable=False)
    notes = models.ManyToManyField(Note, blank=True, related_name='dogs')
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='dogs')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.slug:
            self.slug = slugify(f'{self.name}-{self.id}')
            super().save(update_fields=['slug'])

    @property
    def filename(self):
        return os.path.basename(self.picture.name)

    @property
    def age(self):
        today = date.today()
        age = today.year - self.date_of_birth.year - (
            (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))
        return max(0, age)

#-----------------------------------------------------------------------------------------------------------------------
