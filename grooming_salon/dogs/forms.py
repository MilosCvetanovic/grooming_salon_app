from django import forms
from grooming_salon.dogs.models import Dog
from grooming_salon.utils.mixins import RemovePictureMixin

# Create your forms here.
#-----------------------------------------------------------------------------------------------------------------------
class DogForm(RemovePictureMixin, forms.ModelForm):
    class Meta:
        model = Dog
        exclude = ['user', 'slug', 'notes']
        widgets = {
            'name': forms.TextInput(attrs={'autofocus': True}),
            'date_of_birth': forms.DateInput(
                attrs={'type': 'date'},
                format='%Y-%m-%d',
            ),
            'breed': forms.TextInput(),
            'picture': forms.FileInput(attrs={'id': 'photo-input'})
        }
        labels = {
            'name': 'Ime psa:',
            'date_of_birth': 'Datum rođenja:',
            'breed': 'Rasa:',
            'picture': 'Fotografija psa:',
        }

    # Čistimo polje "picture" ako je korisnik aktivirao (X)
    def clean(self):
        cleaned_data = super().clean()
        remove_picture = cleaned_data.get('remove_picture')

        if remove_picture:
            cleaned_data['picture'] = None
            cleaned_data['remove_picture'] = True

        return cleaned_data

#-----------------------------------------------------------------------------------------------------------------------
class DogDeleteForm(DogForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for (_, field) in self.fields.items():
            field.widget.attrs['disabled'] = 'disabled'
            field.widget.attrs['readonly'] = 'readonly'

#-----------------------------------------------------------------------------------------------------------------------
