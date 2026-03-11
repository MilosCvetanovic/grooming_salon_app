from datetime import timedelta
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase
from grooming_salon.accounts.models import Profile, EmailVerificationToken

UserModel = get_user_model()

# Create your tests here.
#-----------------------------------------------------------------------------------------------------------------------
class AppUserAndProfileTests(TestCase):
    def setUp(self):
        self.user = UserModel.objects.create_user(email='test@tmail.com', password='password123')

        # Pošto koristim Django Signal za kreiranje profila, ako je kreiran dopuni podatke
        self.profile, created = Profile.objects.update_or_create(
            user=self.user,
            defaults={
                'first_name': 'Miloš',
                'last_name': 'Cvetanović'
            }
        )

    def test_appUser_str_method__should_return_email(self):
        self.assertEqual(str(self.user), 'test@tmail.com')

    def test_profile_get_profile_name__should_return_full_name(self):
        self.assertEqual(self.profile.get_profile_name, 'Miloš Cvetanović')

    def test_profile_creation__when_invalid_name__should_raise_error(self):
        self.profile.first_name = 'miloš' # Malo slovo
        with self.assertRaises(ValidationError):
            self.profile.full_clean()

#-----------------------------------------------------------------------------------------------------------------------
class EmailVerificationTokenTests(TestCase):
    def setUp(self):
        self.user = UserModel.objects.create_user(
            email='token@test.com',
            password='password123'
        )

    def test_token_auto_generation_on_save(self):
        # Act
        token_obj = EmailVerificationToken.objects.create(user=self.user)

        # Assert
        self.assertIsNotNone(token_obj.token)
        self.assertGreater(len(token_obj.token), 32)

    def test_is_expired__when_token_is_new__should_return_false(self):
        # Arrange
        token_obj = EmailVerificationToken.objects.create(user=self.user)

        # Assert
        self.assertFalse(token_obj.is_expired())

    def test_is_expired__when_token_older_than_24h__should_return_true(self):
        # Arrange
        token_obj = EmailVerificationToken.objects.create(user=self.user)

        token_obj.created_at = timezone.now() - timedelta(hours=25)
        token_obj.save()

        # Assert
        self.assertTrue(token_obj.is_expired())

#-----------------------------------------------------------------------------------------------------------------------
