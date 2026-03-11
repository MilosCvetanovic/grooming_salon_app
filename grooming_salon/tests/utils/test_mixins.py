import os
from django import forms
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, RequestFactory
from django.views.generic import ListView
from grooming_salon.dogs.models import Dog
from grooming_salon.utils.mixins import UserOwnedModelMixin, RemovePictureMixin, ImageCleanupMixin

UserModel = get_user_model()

# Create your tests here.
#-----------------------------------------------------------------------------------------------------------------------
# Mock View koji simulira listu pasa (model ima 'user')
class MockDogListView(UserOwnedModelMixin, ListView):
    model = Dog

# Mock View koji simulira profil (model je sam User, nema 'user' polje već 'pk')
class MockProfileView(UserOwnedModelMixin, ListView):
    model = UserModel

class UserOwnedModelMixinTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user1 = UserModel.objects.create_user(email='user1@tmail.com', password='pass')
        self.user2 = UserModel.objects.create_user(email='user2@tmail.com', password='pass')

        dog1 = Dog(name='Dekster', date_of_birth='2020-01-01', user=self.user1, breed='Labradudla')
        dog1.save()

        dog2 = Dog(name='Rina', date_of_birth='2021-01-01', user=self.user2, breed='Bigl')
        dog2.save()

    def test_get_queryset__when_model_has_user_field__should_filter_by_user(self):
        # Arrange
        request = self.factory.get('/')
        request.user = self.user1
        view = MockDogListView()
        view.request = request

        # Act
        qs = view.get_queryset()

        # Assert
        self.assertEqual(qs.count(), 1)
        self.assertEqual(qs.first().user, self.user1)
        self.assertEqual(qs.first().name, 'Dekster')

    def test_get_queryset__when_model_is_user_itself__should_filter_by_pk(self):
        # Arrange
        request = self.factory.get('/')
        request.user = self.user2
        view = MockProfileView()
        view.request = request

        # Act
        qs = view.get_queryset()

        # Assert
        self.assertEqual(qs.count(), 1)
        self.assertEqual(qs.first().pk, self.user2.pk)

#-----------------------------------------------------------------------------------------------------------------------
class UserOwnedModelMixinNoneTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = UserModel.objects.create_user(email='user@tmail.com', password='pass')

    def test_get_queryset__when_super_returns_none__should_return_none(self):
        # Arrange
        request = self.factory.get('/')
        request.user = self.user

        # Napravili smo lažan view koji smo naterali da vrati None
        class BaseView:
            def get_queryset(self):
                return None

        class TestNoneView(UserOwnedModelMixin, BaseView):
            pass

        view = TestNoneView()

        # Act
        result = view.get_queryset()

        # Assert
        self.assertIsNone(result)

#-----------------------------------------------------------------------------------------------------------------------
# Pravimo lažnu formu koja koristi Mixin radi testiranja
class MockForm(RemovePictureMixin, forms.Form):
    name = forms.CharField()

class RemovePictureMixinTests(TestCase):
    def test_removePictureMixin_initialization__should_add_remove_picture_field(self):
        # Arrange & Act
        form = MockForm()

        # Assert
        # 1. Proveravamo da li polje postoji
        self.assertIn('remove_picture', form.fields)

        # 2. Proveravamo tip polja
        field = form.fields['remove_picture']
        self.assertIsInstance(field, forms.BooleanField)

        # 3. Proveravamo da polje NIJE obavezno (required=False)
        self.assertFalse(field.required)

    def test_removePictureMixin_widget_attrs__should_have_correct_css_class(self):
        # Arrange & Act
        form = MockForm()
        widget = form.fields['remove_picture'].widget

        # Assert
        # Proveravamo da li je widget Checkbox i da li ima klasu
        self.assertIsInstance(widget, forms.CheckboxInput)
        self.assertEqual(widget.attrs.get('class'), 'delete-checkbox')

#-----------------------------------------------------------------------------------------------------------------------
# Pravimo Mock Formu jer Mixin očekuje 'form' objekat
class MockFormMixin:
    def __init__(self, instance, remove_picture=False):
        self.instance = instance
        self.cleaned_data = {'remove_picture': remove_picture}


class ImageCleanupMixinTests(TestCase):
    def setUp(self):
        # Kreiramo korisnika (jer Dog model to traži)
        self.user = get_user_model().objects.create_user(email='user@tmail.com', password='pass')

        # Pravimo lažnu sliku
        self.image_content = b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\x00\x00\x05\x04\x03\x02\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02\x44\x01\x00\x3b'
        self.test_image = SimpleUploadedFile('test_dog.jpg', self.image_content, content_type='image/jpeg')

    def test_handle_image_cleanup__when_remove_is_true__should_delete_file_and_set_none(self):
        # Arrange
        dog = Dog(name='Dekster', date_of_birth='2021-01-01', user=self.user, picture=self.test_image)
        dog.save()

        file_path = dog.picture.path
        self.assertTrue(os.path.exists(file_path))

        mixin = ImageCleanupMixin()
        form = MockFormMixin(instance=dog, remove_picture=True)

        # Act
        result = mixin.handle_image_cleanup(form)

        # Assert
        self.assertTrue(result)
        self.assertIsNone(dog.picture.name)
        self.assertFalse(os.path.exists(file_path))

    def test_handle_image_cleanup__when_remove_is_false__should_do_nothing(self):
        # Arrange
        dog = Dog(name='Dekster', date_of_birth='2021-01-01', user=self.user, picture=self.test_image)
        dog.save()

        mixin = ImageCleanupMixin()
        form = MockFormMixin(instance=dog, remove_picture=False)

        # Act
        result = mixin.handle_image_cleanup(form)

        # Assert
        self.assertFalse(result)
        self.assertIsNotNone(dog.picture.name)
        self.assertTrue(os.path.exists(dog.picture.path))

#-----------------------------------------------------------------------------------------------------------------------
