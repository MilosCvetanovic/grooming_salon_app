from datetime import date, timedelta, time
from django.contrib.auth import get_user_model
from django.db import connection
from django.test import TestCase
from grooming_salon.dogs.models import Dog
from grooming_salon.services.models import Groomer, Service, Appointment

UserModel = get_user_model()

# Create your tests here
#-----------------------------------------------------------------------------------------------------------------------
class AppointmentManagerTests(TestCase):
    def setUp(self):
        with connection.cursor() as cursor:
            cursor.execute("SELECT setval(pg_get_serial_sequence('dogs_dog', 'id'), 1, false)")

        self.user = UserModel.objects.create_user(email='user@test.com', password='pass')
        self.groomer = Groomer.objects.create(name='Groomer Test')
        self.dog = Dog.objects.create(
            name='Dekster',
            breed='Labradudla',
            date_of_birth=date(2020, 1, 1),
            user=self.user
        )
        self.service = Service.objects.create(name='Kupanje')

    def _create_appointment(self, appt_date, appt_time, status='BOOKED'):
        appt = Appointment.objects.create(
            date=appt_date,
            time=appt_time,
            status=status,
            groomer=self.groomer,
            dog=self.dog,
            user=self.user,
        )
        appt.services.add(self.service)
        return appt

    def test_markAppointmentExpired__with_past_booked__should_mark_completed(self):
        yesterday = date.today() - timedelta(days=1)
        appt = self._create_appointment(yesterday, time(10, 0))

        Appointment.objects.mark_appointment_expired(self.groomer)

        appt.refresh_from_db()
        self.assertEqual(appt.status, 'COMPLETED')

    def test_freeCancelledSlots__with_booked_slot__should_be_in_unavailable(self):
        today = date.today()
        self._create_appointment(today, time(10, 0), status='BOOKED')

        unavailable = Appointment.objects.free_cancelled_slots(self.groomer, today)

        self.assertIn(time(10, 0), unavailable)

    def test_freeCancelledSlots__with_cancelled_slot__should_not_be_in_unavailable(self):
        today = date.today()
        self._create_appointment(today, time(10, 0), status='CANCELLED')

        unavailable = Appointment.objects.free_cancelled_slots(self.groomer, today)

        self.assertNotIn(time(10, 0), unavailable)

#-----------------------------------------------------------------------------------------------------------------------
