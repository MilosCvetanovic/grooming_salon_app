import os
from django.db import models
from django.contrib.auth import models as auth_models, get_user_model
from grooming_salon.utils.validators import validate_capitalized_name, validate_phone_number, validate_file_size


# Create your models here.
#-----------------------------------------------------------------------------------------------------------------------
class AppUser(auth_models.PermissionsMixin, auth_models.AbstractBaseUser):
    email = models.EmailField(null=False, blank=False, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

#-----------------------------------------------------------------------------------------------------------------------
MAX_LENGTH = 30
UserModel = get_user_model()

class Profile(models.Model):
    first_name = models.CharField(max_length=MAX_LENGTH, validators=[validate_capitalized_name], null=False, blank=False)
    last_name = models.CharField(max_length=MAX_LENGTH, validators=[validate_capitalized_name], null=False, blank=False)
    phone = models.CharField(max_length=MAX_LENGTH, validators=[validate_phone_number], null=True, blank=True)
    picture = models.ImageField(upload_to='images/profile/', validators=[validate_file_size], null=True, blank=True)
    user = models.OneToOneField(UserModel, on_delete=models.CASCADE, primary_key=True)

    # Vrati puno ime i prezime
    def get_profile_name(self):
        return f"{self.first_name} {self.last_name}".strip()

    # Atribut koji vraca ime slike bez apsolutne putanje
    @property
    def filename(self):
        return os.path.basename(self.picture.name)

#-----------------------------------------------------------------------------------------------------------------------
