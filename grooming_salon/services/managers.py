from datetime import date
from django.db import models

# Create your managers here
#-----------------------------------------------------------------------------------------------------------------------
class AppointmentManager(models.Manager):
    def mark_appointment_expired(self, groomer) -> None:
        potential_expired = self.filter(
            groomer=groomer,
            status='BOOKED',
            date__lte=date.today()
        ).prefetch_related('services')

        for appoint in potential_expired:
            appoint.mark_completed_if_past()

    def free_cancelled_slots(self, groomer, selected_date):
        unavailable_slots = self.filter(
            groomer=groomer,
            date=selected_date
        ).exclude(status='CANCELLED').values_list('time', flat=True)

        return unavailable_slots

#-----------------------------------------------------------------------------------------------------------------------
