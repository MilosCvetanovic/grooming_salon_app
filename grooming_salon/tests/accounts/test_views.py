from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.test import TestCase
from django.urls import reverse
from grooming_salon.accounts.models import EmailVerificationToken, Profile
from datetime import timedelta
from django.utils import timezone
from grooming_salon.accounts.signals import create_profile

UserModel = get_user_model()

# Create your tests here.
#-----------------------------------------------------------------------------------------------------------------------
class ProfileViewsTests(TestCase):
    def login(self):
        self.client.force_login(
            self.user,
            backend='django.contrib.auth.backends.ModelBackend'
        )

    def setUp(self):
        post_save.disconnect(create_profile, sender=UserModel)

        self.user = UserModel.objects.create_user(
            email='milos@test.com',
            password='pass123',
            is_active=True,
            is_superuser=True,
        )
        self.user = UserModel.objects.get(pk=self.user.pk)

        self.profile = Profile.objects.create(user=self.user)
        self.profile.first_name = 'Milos'
        self.profile.last_name = 'Cvetanovic'
        self.profile.save()

    def tearDown(self):
        post_save.connect(create_profile, sender=UserModel)

    def test_profileDetailView_get__should_render_correct_template_and_context(self):
        self.login()

        response = self.client.get(reverse('profile_details'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/profile-details-page.html')

    def test_profileEditView_post__should_update_profile_and_redirect(self):
        self.login()

        data = {
            'first_name': 'Ana',
            'last_name': 'Ilic',
            'phone': '',
        }

        response = self.client.post(reverse('profile_edit'), data=data)

        self.assertEqual(response.status_code, 302)
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.first_name, 'Ana')
        self.assertEqual(self.profile.last_name, 'Ilic')

    def test_profileDeleteView_post(self):
        self.login()

        response = self.client.post(reverse('profile_delete'))

        self.assertRedirects(response, reverse('home'))
        self.assertFalse(UserModel.objects.filter(pk=self.user.pk).exists())

#-----------------------------------------------------------------------------------------------------------------------
class VerifyEmailTests(TestCase):
    def setUp(self):
        self.user = UserModel.objects.create_user(email='test@test.com', password='pass', is_active=False)
        self.token_obj = EmailVerificationToken.objects.create(user=self.user)

    def test_verifyEmail__with_valid_token__should_activate_user(self):
        response = self.client.get(reverse('verify_email', kwargs={'token': self.token_obj.token}))

        self.user.refresh_from_db()
        self.assertTrue(self.user.is_active)
        self.assertRedirects(response, reverse('login'))
        # Provera da li je token obrisan
        self.assertFalse(EmailVerificationToken.objects.filter(token=self.token_obj.token).exists())

    def test_verifyEmail__with_expired_token__should_redirect_to_register(self):
        # Ručno postavljamo da je token star 25 sati
        self.token_obj.created_at = timezone.now() - timedelta(hours=25)
        self.token_obj.save()

        response = self.client.get(reverse('verify_email', kwargs={'token': self.token_obj.token}))

        self.user.refresh_from_db()
        self.assertFalse(self.user.is_active)
        self.assertRedirects(response, reverse('register'))

    def test_verifyEmail__with_invalid_token__should_show_error(self):
        response = self.client.get(reverse('verify_email', kwargs={'token': 'ne-postojim'}))
        self.assertRedirects(response, reverse('register'))

#-----------------------------------------------------------------------------------------------------------------------
