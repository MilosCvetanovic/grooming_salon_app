from unittest.mock import patch
from django.test import TestCase
from grooming_salon.accounts.forms import AppUserCreationForm, ProfileEditForm
from grooming_salon.accounts.models import EmailVerificationToken

# Create your tests here.
#-----------------------------------------------------------------------------------------------------------------------
class AppUserCreationFormTests(TestCase):

    # Patch-ujemo funkciju za slanje mejla da se ne bi stvarno izvršila
    @patch('grooming_salon.accounts.forms.send_verification_email')
    def test_save__should_create_user_profile_and_token(self, mock_send_email):
        # Arrange
        form_data = {
            'email': 'milos@test.com',
            'first_name': 'Miloš',
            'last_name': 'Cvetanović',
            'password1': 'lozinka123',
            'password2': 'lozinka123',
        }
        form = AppUserCreationForm(data=form_data)

        # Act
        self.assertTrue(form.is_valid())
        user = form.save()

        # Assert
        self.assertEqual(user.profile.first_name, 'Miloš')
        self.assertEqual(user.profile.last_name, 'Cvetanović')

        token_exists = EmailVerificationToken.objects.filter(user=user).exists()
        self.assertTrue(token_exists)

        mock_send_email.assert_called_once()

#-----------------------------------------------------------------------------------------------------------------------
class ProfileEditFormTests(TestCase):
    def test_clean__when_remove_picture_is_true__should_set_picture_to_none(self):
        # Arrange
        form_data = {
            'first_name': 'Miloš',
            'last_name': 'Cvetanović',
            'remove_picture': True,
        }
        form = ProfileEditForm(data=form_data)

        # Act
        form.is_valid()

        # Assert
        self.assertIsNone(form.cleaned_data.get('picture'))
        self.assertTrue(form.cleaned_data.get('remove_picture'))

    def test_clean__when_remove_picture_is_false__should_keep_picture(self):
        # Arrange
        form_data = {
            'first_name': 'Marko',
            'last_name': 'Markovic',
            'remove_picture': False,
        }
        form = ProfileEditForm(data=form_data)

        # Act
        form.is_valid()

        # Assert
        self.assertFalse(form.cleaned_data.get('remove_picture'))

#-----------------------------------------------------------------------------------------------------------------------
