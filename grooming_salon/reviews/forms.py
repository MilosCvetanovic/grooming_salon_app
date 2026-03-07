from django import forms
from grooming_salon.reviews.models import Review
from grooming_salon.utils.mixins import RemovePictureMixin

# Create your forms here.
#-----------------------------------------------------------------------------------------------------------------------
class ReviewForm(RemovePictureMixin, forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'description', 'picture']
        widgets = {
            'rating': forms.RadioSelect(choices=[(i, i) for i in range(5, 0, -1)]),
            'description': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Podelite vaše utiske...',
                'class': 'form-control'
            }),
            'picture': forms.FileInput(
                attrs={'id': 'photo-input'}
            ),
        }
        labels = {
            'rating': 'Ocena:',
            'description': 'Utisci (opciono):',
            'picture': 'Fotografija (opciono):',
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
