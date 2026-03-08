import os
import secrets
from datetime import timedelta

from django.db import models
from django.contrib.auth import models as auth_models, get_user_model
from django.utils import timezone

from grooming_salon.accounts.managers import AppUserManager
from grooming_salon.utils.validators import validate_capitalized_name, validate_phone_number, validate_file_size


# Create your models here.
#-----------------------------------------------------------------------------------------------------------------------
class AppUser(auth_models.PermissionsMixin, auth_models.AbstractBaseUser):
    email = models.EmailField(null=False, blank=False, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = AppUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

#-----------------------------------------------------------------------------------------------------------------------
MAX_LENGTH = 30
MAX_TOKEN_LENGTH = 64
UserModel = get_user_model()

class Profile(models.Model):
    first_name = models.CharField(max_length=MAX_LENGTH, validators=[validate_capitalized_name], null=False, blank=False)
    last_name = models.CharField(max_length=MAX_LENGTH, validators=[validate_capitalized_name], null=False, blank=False)
    phone = models.CharField(max_length=MAX_LENGTH, validators=[validate_phone_number], null=True, blank=True)
    picture = models.ImageField(upload_to='images/profile/', validators=[validate_file_size], null=True, blank=True)
    user = models.OneToOneField(UserModel, on_delete=models.CASCADE, primary_key=True)

    # Vrati puno ime i prezime
    @property
    def get_profile_name(self):
        return f"{self.first_name} {self.last_name}"

    # Atribut koji vraca ime slike bez apsolutne putanje
    @property
    def filename(self):
        return os.path.basename(self.picture.name)

#-----------------------------------------------------------------------------------------------------------------------
class EmailVerificationToken(models.Model):
    user = models.OneToOneField(UserModel, on_delete=models.CASCADE, related_name='verification_token')
    token = models.CharField(max_length=MAX_TOKEN_LENGTH, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    # Automatski generiši token pri kreiranju objekta
    def save(self, *args, **kwargs):
        if not self.token:
            self.token = secrets.token_urlsafe(32)
        super().save(*args, **kwargs)

    # Token važi 24 sata
    def is_expired(self):
        return timezone.now() > self.created_at + timedelta(hours=24)

    def __str__(self):
        return f'Token za {self.user.email}'

#-----------------------------------------------------------------------------------------------------------------------
