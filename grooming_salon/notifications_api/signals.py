from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from .models import Notification
from grooming_salon.services.models import Appointment
from ..loyalty_api.models import Voucher


#-----------------------------------------------------------------------------------------------------------------------
# Notifikacija za kreiranje termina
@receiver(m2m_changed, sender=Appointment.services.through)
def create_booking_confirmed_notification(sender, instance, action, **kwargs):

    # Termin upravo kreiran
    if action == "post_add":
        services_display = ", ".join(s.name for s in instance.services.all())

        Notification.objects.create(
            user=instance.user,
            appointment=instance,
            notification_type=Notification.NotificationType.APPOINTMENT_BOOKED,
            message=f"Tvoj termin za '{services_display}' je potvrđen "
                    f"za {instance.date.strftime('%d.%m.%Y')} u {instance.time.strftime('%H:%M')}h."
        )

#-----------------------------------------------------------------------------------------------------------------------
# Notifikacije za promenu statusa termina
@receiver(post_save, sender=Appointment)
def create_status_notification(sender, instance, created, **kwargs):
    if created:
        return

    services_display = ", ".join(s.name for s in instance.services.all())

    # Termin završen
    if instance.status == 'COMPLETED':
        Notification.objects.create(
            user=instance.user,
            appointment=instance,
            notification_type=Notification.NotificationType.APPOINTMENT_COMPLETED,
            message=f"Tvoj termin za '{services_display}' zakazan za "
                    f"{instance.date.strftime('%d.%m.%Y')} u {instance.time.strftime('%H:%M')}h je završen. "
                    f"Ostavi recenziju!"
        )

    # Termin otkazan
    elif instance.status == 'CANCELLED':
        Notification.objects.create(
            user=instance.user,
            appointment=instance,
            notification_type=Notification.NotificationType.APPOINTMENT_CANCELLED,
            message=f"Tvoj termin za '{services_display}' zakazan za "
                    f"{instance.date.strftime('%d.%m.%Y')} u {instance.time.strftime('%H:%M')}h je otkazan."
        )

#-----------------------------------------------------------------------------------------------------------------------
# Notifikacija kada se generiše novi vaučer za popust
@receiver(post_save, sender=Voucher)
def create_voucher_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            user=instance.user,
            notification_type=Notification.NotificationType.VOUCHER_CREATED,
            message=f"Čestitamo! Dobili ste vaučer {instance.code}. "
                    f"Pokažite ga u salonu za 20% popusta."
        )

#-----------------------------------------------------------------------------------------------------------------------
