from unittest.mock import MagicMock
from django.core.exceptions import ValidationError
from django.test import SimpleTestCase
from grooming_salon.utils.validators import validate_capitalized_name, validate_phone_number, validate_file_size

# Create your tests here.
#-----------------------------------------------------------------------------------------------------------------------
class CapitalizedNameValidatorTests(SimpleTestCase):

    def test_validator_when_properly_capitalized__should_do_nothing(self):
        # Arrange
        valid_name = 'Milos Cvetanovic'

        # Act & Assert
        validate_capitalized_name(valid_name)

    def test_validator_when_not_capitalized__should_raise_error(self):
        # Arrange
        invalid_name = 'milos Cvetanovic'

        # Act & Assert
        with self.assertRaises(ValidationError) as context:
            validate_capitalized_name(invalid_name)

        self.assertEqual(
            context.exception.message,
            'Unos mora početi velikim slovom i sadržati samo slova i razmake.'
        )

    def test_validator_when_contains_numbers__should_raise_error(self):
        # Arrange
        invalid_name = "Milos Cvetanovic123"

        # Act & Assert
        with self.assertRaises(ValidationError):
            validate_capitalized_name(invalid_name)

    def test_validator_when_contains_special_chars__should_raise_error(self):
        # Arrange
        invalid_name = "Milos @Cvetanovic"

        # Act & Assert
        with self.assertRaises(ValidationError):
            validate_capitalized_name(invalid_name)

#-----------------------------------------------------------------------------------------------------------------------
class PhoneNumberValidatorTests(SimpleTestCase):

    def test_validator_when_only_digits__should_pass(self):
        # Arrange
        valid_phone = "064123456"

        # Act & Assert
        validate_phone_number(valid_phone)

    def test_validator_when_starts_with_plus__should_pass(self):
        # Arrange
        valid_phone = "+38164123456"

        # Act & Assert
        validate_phone_number(valid_phone)

    def test_validator_when_contains_letters__should_raise(self):
        # Arrange
        invalid_phone = "+38164abc123"

        # Act & Assert
        with self.assertRaises(ValidationError) as context:
            validate_phone_number(invalid_phone)
        self.assertEqual(context.exception.message, 'Broj telefona mora sadržati samo cifre ili početi sa "+" pa cifre.')

    def test_validator_when_contains_spaces__should_raise(self):
        # Arrange
        invalid_phone = "+381 64 123"

        # Act & Assert
        with self.assertRaises(ValidationError):
            validate_phone_number(invalid_phone)

#-----------------------------------------------------------------------------------------------------------------------
class FileSizeValidatorTests(SimpleTestCase):

    def test_validator_when_size_is_exactly_5MB__should_pass(self):
        # Arrange - Pravimo mock objekat kako bismo simulirali tačno 5MB i testirali granični slučaj
        mock_file = MagicMock()
        mock_file.size = 5242880

        # Act & Assert
        validate_file_size(mock_file)

    def test_validator_when_size_is_under_5MB__should_pass(self):
        # Arrange
        mock_file = MagicMock()
        mock_file.size = 1024 # jedan kilobajt

        # Act & Assert
        validate_file_size(mock_file)

    def test_validator_when_size_is_over_5MB__should_raise(self):
        # Arrange
        mock_file = MagicMock()
        mock_file.size = 5242881 # jedan bajt preko dozvoljenog

        # Act & Assert
        with self.assertRaises(ValidationError) as context:
            validate_file_size(mock_file)

        self.assertEqual(
            context.exception.message,
            'Maksimalna veličina fotografije koja se može otpremiti je 5MB.'
        )

#-----------------------------------------------------------------------------------------------------------------------
