from django.contrib.auth import get_user_model
from django.db import models

UserModel = get_user_model()

MAX_LENGTH = 20

# Create your models here.
#-----------------------------------------------------------------------------------------------------------------------
class Loyalty(models.Model):
    user = models.OneToOneField(UserModel, on_delete=models.CASCADE, related_name='loyalty')
    used_points = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Loyalty: {self.user.profile.get_profile_name}'

    # Nakon ulaska u Loyalty program, uzmi broj završenih rezervacija korisnika
    @property
    def total_earned_points(self):
        return self.user.appointments.filter(
            created_at__gte=self.created_at,
            status='COMPLETED'
        ).count()

    # I računaj poene od momenta ulaska u Loyalty program
    @property
    def current_points(self):
        total = self.total_earned_points
        vouchers_created = self.user.vouchers.count()
        points = total - (vouchers_created * 5)
        return max(0, points)

    # Proračun koliko je još poena potrebno za vaučer
    @property
    def remaining_until_reward(self):
        points = self.current_points
        if points >= 5:
            return 5 - (points % 5) if points % 5 != 0 else 5
        return 5 - points

    # Vraća sve vaučere korisnika koji još nisu iskorišćeni - služe za prikaz na dashboard-u
    @property
    def active_vouchers(self):
        return Voucher.objects.filter(user=self.user, is_used=False)

#-----------------------------------------------------------------------------------------------------------------------
class Voucher(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='vouchers')
    code = models.CharField(max_length=MAX_LENGTH, unique=True)
    is_used = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.code} - {self.user.email} ({'Iskorišćen' if self.is_used else 'Aktivan'})"

#-----------------------------------------------------------------------------------------------------------------------
