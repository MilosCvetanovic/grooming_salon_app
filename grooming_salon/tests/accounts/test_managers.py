from django.contrib.auth import get_user_model
from django.test import TestCase

UserModel = get_user_model()

# Create your tests here.
#-----------------------------------------------------------------------------------------------------------------------
class AppUserManagerTests(TestCase):

    def test_createUser__with_valid_email__should_create_user(self):
        user = UserModel.objects.create_user(email='test@test.com', password='pass123')

        self.assertEqual(user.email, 'test@test.com')
        self.assertTrue(user.check_password('pass123'))
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_createUser__with_uppercase_email__should_normalize_to_lowercase(self):
        user = UserModel.objects.create_user(email='TEST@TEST.COM', password='pass123')

        self.assertEqual(user.email, 'test@test.com')

    def test_createUser__without_email__should_raise_value_error(self):
        with self.assertRaises(ValueError):
            UserModel.objects.create_user(email='', password='pass123')

    def test_createUser__without_password__should_create_user_with_unusable_password(self):
        user = UserModel.objects.create_user(email='test@test.com', password=None)

        self.assertFalse(user.has_usable_password())

    def test_createSuperuser__should_set_is_staff_and_is_superuser(self):
        user = UserModel.objects.create_superuser(email='admin@test.com', password='pass123')

        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)

#-----------------------------------------------------------------------------------------------------------------------
