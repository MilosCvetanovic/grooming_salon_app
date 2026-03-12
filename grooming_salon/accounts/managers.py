from django.contrib.auth import models as auth_models

# Create your managers here.
#-----------------------------------------------------------------------------------------------------------------------
# Pravimo custom manager kako bismo pregazili username sa email
class AppUserManager(auth_models.BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('E-mail polje mora biti popunjeno.')

        email = self.normalize_email(email).lower()
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        return self.create_user(email, password, **extra_fields)

#-----------------------------------------------------------------------------------------------------------------------
