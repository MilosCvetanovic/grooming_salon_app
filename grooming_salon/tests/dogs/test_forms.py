from django.test import TestCase
from grooming_salon.dogs.forms import DogForm, DogDeleteForm

# Create your tests here.
#-----------------------------------------------------------------------------------------------------------------------
class DogFormTests(TestCase):

    def test_dogForm_when_valid_data__should_be_valid(self):
        # Arrange
        valid_data = {
            'name': 'Dekster',
            'date_of_birth': '2020-01-01',
            'breed': 'Labradudla',
        }

        # Act
        form = DogForm(data=valid_data)

        # Assert
        self.assertTrue(form.is_valid())

    def test_dogForm_when_invalid_name__should_be_invalid(self):
        invalid_data = {
            'name': 'dekster',
            'date_of_birth': '2020-01-01',
            'breed': 'Labradudla',
        }

        # Act
        form = DogForm(data=invalid_data)

        # Assert
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)
        self.assertEqual(
            form.errors['name'][0],
            'Unos mora početi velikim slovom i sadržati samo slova i razmake.'
        )

    def test_dogForm_clean_method__when_remove_picture_is_true(self):
        # Arrange
        data = {
            'name': 'Dekster',
            'date_of_birth': '2020-01-01',
            'breed': 'Labrador',
            'remove_picture': True  # Simuliramo klik na (X)
        }

        # Act
        form = DogForm(data=data)

        # Assert
        if form.is_valid():
            # Proveravamo da li je clean() postavio picture na None
            self.assertIsNone(form.cleaned_data.get('picture'))
            self.assertTrue(form.cleaned_data.get('remove_picture'))

    def test_dogForm_labels__are_correct(self):
        # Arrange
        form = DogForm()

        # Assert
        self.assertEqual(form.fields['name'].label, 'Ime psa:')
        self.assertEqual(form.fields['date_of_birth'].label, 'Datum rođenja:')

#-----------------------------------------------------------------------------------------------------------------------
class DogDeleteFormTests(TestCase):

    def test_dogDeleteForm_allFields__should_be_disabled_and_readonly(self):
        # Arrange & Act
        form = DogDeleteForm()

        # Assert
        for field_name, field in form.fields.items():
            self.assertEqual(
                field.widget.attrs['disabled'],
                'disabled',
                f'Polje {field_name} nije onemogućeno (disabled)!'
            )
            self.assertEqual(
                field.widget.attrs['readonly'],
                'readonly',
                f'Polje {field_name} nije samo za čitanje (readonly)!'
            )

    def test_dogDeleteForm_inheritance__should_have_same_labels_as_dogForm(self):
        # Arrange
        form = DogDeleteForm()

        # Assert - Proveravamo da li je nasledio labele iz DogForm
        self.assertEqual(form.fields['name'].label, 'Ime psa:')
        self.assertEqual(form.fields['breed'].label, 'Rasa:')

#-----------------------------------------------------------------------------------------------------------------------
