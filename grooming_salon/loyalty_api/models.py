from django.contrib.auth import get_user_model
from django.db import models

MAX_LENGTH = 20
UserModel = get_user_model()

# Create your models here.
#-----------------------------------------------------------------------------------------------------------------------
class Loyalty(models.Model):
    user = models.OneToOneField(UserModel, on_delete=models.CASCADE, related_name='loyalty')
    points = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Loyalty: {self.user.profile.get_profile_name}'

    @property
    def appointment_count(self):
        return self.user.appointments.count()


    def active_vouchers(self):
        """Vraća samo vaučere koji nisu iskorišćeni"""
        # Pretpostavljam da vaučer ima ForeignKey ka Useru ili Loyalty objektu
        return Voucher.objects.filter(user=self.user, is_used=False)

    # Uzmi sve završene rezervacije korisnika nakon što je kreiran Loyalty objekat
    def get_points_since_joining(self):
        """Računa poene samo od momenta učlanjenja"""
        return self.user.appointments.filter(
            created_at__gte=self.created_at,
            status='COMPLETED'
        ).count()

    def remaining_until_reward(self):
        points = self.get_points_since_joining()
        remaining = 5 - (points % 5)  # Ako ima 3 poena, fali mu 2. Ako ima 5, resetuje se.
        return remaining

#-----------------------------------------------------------------------------------------------------------------------
class Voucher(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='vouchers')
    code = models.CharField(max_length=MAX_LENGTH, unique=True)
    is_used = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.code} - {self.user.email}'

#-----------------------------------------------------------------------------------------------------------------------
