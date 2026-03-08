from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.db.models.signals import post_save
from django.dispatch import receiver
from grooming_salon.accounts.models import Profile

UserModel = get_user_model()

#-----------------------------------------------------------------------------------------------------------------------
# Registracija korisnika će trigerovati Django signal da napravi prazan profil
@receiver(post_save, sender=UserModel)
def create_profile(sender, instance, created, **kwargs):
    # Kreiraj profil
    if created:
        Profile.objects.create(user=instance)

        # Dodaj korisnika u User grupu
        user_group, _ = Group.objects.get_or_create(name='User')
        instance.groups.add(user_group)

#-----------------------------------------------------------------------------------------------------------------------
