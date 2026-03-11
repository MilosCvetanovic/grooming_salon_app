from datetime import timedelta, date, time
from django.contrib.auth import get_user_model
from django.db import connection
from django.test import TestCase
from grooming_salon.dogs.models import Dog
from grooming_salon.services.models import Service, Groomer, Appointment

UserModel = get_user_model()

# Create your tests here.
#-----------------------------------------------------------------------------------------------------------------------
class ServiceAndGroomerTests(TestCase):
    def test_service_str__should_return_name(self):
        service = Service.objects.create(name='Šišanje')
        self.assertEqual(str(service), 'Šišanje')

    def test_groomer_str__should_return_name(self):
        groomer = Groomer.objects.create(name='Jovana')
        self.assertEqual(str(groomer), 'Jovana')

#-----------------------------------------------------------------------------------------------------------------------
class AppointmentTests(TestCase):
    def setUp(self):
        # Resetuj PostgreSQL sekvencu za generisanje ID-a za Dog tabelu
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

    def test_mark_completed_if_past__when_appointment_is_old__should_update_status(self):

        yesterday = date.today() - timedelta(days=1)
        appt = Appointment.objects.create(
            date=yesterday,
            time=time(10, 0),
            groomer=self.groomer,
            dog=self.dog,
            user=self.user,
            status='BOOKED'
        )

        # Act
        result = appt.mark_completed_if_past()

        # Assert
        appt.refresh_from_db()
        self.assertTrue(result)
        self.assertEqual(appt.status, 'COMPLETED')

    def test_mark_completed_if_past__when_appointment_is_future__should_stay_booked(self):
        tomorrow = date.today() + timedelta(days=1)
        appt = Appointment.objects.create(
            date=tomorrow,
            time=time(10, 0),
            groomer=self.groomer,
            dog=self.dog,
            user=self.user
        )

        # Act
        result = appt.mark_completed_if_past()

        # Assert
        appt.refresh_from_db()
        self.assertFalse(result)
        self.assertEqual(appt.status, 'BOOKED')

    def test_mark_completed_if_past__when_already_completed__should_return_false(self):
        yesterday = date.today() - timedelta(days=1)
        appt = Appointment.objects.create(
            date=yesterday,
            time=time(10, 0),
            groomer=self.groomer,
            dog=self.dog,
            user=self.user,
            status='COMPLETED'
        )

        result = appt.mark_completed_if_past()

        self.assertFalse(result)
        self.assertEqual(appt.status, 'COMPLETED')

#-----------------------------------------------------------------------------------------------------------------------
