from datetime import date, timedelta
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils.text import slugify
from grooming_salon.dogs.models import Dog

UserModel = get_user_model()

# Create your tests here.
#-----------------------------------------------------------------------------------------------------------------------
class DogModelTests(TestCase):
    def setUp(self):
        # Pripremamo korisnika jer je on strani ključ
        self.user = UserModel.objects.create_user(email='testuser@tmail.com', password='password123')

    def test_dog_str_method__should_return_name(self):
        # Arrange
        dog = Dog(
            name='Dekster',
            date_of_birth=date(2020, 1, 1),
            breed='Labradudla',
            user=self.user
        )

        dog.save()

        # Act & Assert
        self.assertEqual(str(dog), 'Dekster')

    def test_dog_save_method__should_generate_correct_slug(self):
        # Arrange
        dog_name = 'Dekster'
        dog = Dog(
            name=dog_name,
            date_of_birth=date(2020, 1, 1),
            breed='Labrador',
            user=self.user
        )

        dog.save()

        # Act
        expected_slug = slugify(f'{dog_name}-{dog.id}')

        # Assert
        self.assertEqual(dog.slug, expected_slug)

    def test_dog_filename_property__should_return_basename(self):
        # Arrange
        dog = Dog(name='Dekster', user=self.user)
        dog.picture.name = 'images/dogs/moj_pas.jpg' # Simuliramo putanju slike bez stvarnog otpremanja fajla

        # Act
        result = dog.filename

        # Assert
        self.assertEqual(result, 'moj_pas.jpg')

    def test_dog_age_property__should_calculate_correctly(self):
        # Arrange
        today = date.today()
        birth_date = date(today.year - 3, today.month, today.day) - timedelta(days=2)

        dog = Dog(
            name='Dekster',
            date_of_birth=birth_date,
            breed='Labrador',
            user=self.user
        )

        # Act
        dog.save()
        calculated_age = dog.age

        # Assert
        self.assertEqual(calculated_age, 3)

    def test_dog_age_property__when_birthday_has_not_passed_this_year(self):
        # Arrange
        today = date.today()

        # Rođen pre 2 godine, ali sledećeg meseca (rođendan još nije bio)
        birth_date = (today - timedelta(days=365 * 2)).replace(month=(today.month % 12) + 1)

        dog = Dog(date_of_birth=birth_date)

        # Act
        calculated_age = dog.age

        # Assert
        self.assertEqual(calculated_age, 1)

#-----------------------------------------------------------------------------------------------------------------------
