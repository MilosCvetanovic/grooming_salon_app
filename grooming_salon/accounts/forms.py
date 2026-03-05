from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from django import forms

from grooming_salon.utils.mixins import RemovePictureMixin
from grooming_salon.utils.validators import validate_capitalized_name

MAX_LENGTH = 30
UserModel = get_user_model()

#-----------------------------------------------------------------------------------------------------------------------
class AppUserCreationForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=MAX_LENGTH,
        widget=forms.TextInput(attrs={'autofocus': True}),
        validators=[validate_capitalized_name]
    )
    last_name = forms.CharField(
        max_length=MAX_LENGTH,
        validators=[validate_capitalized_name]
    )

    class Meta(UserCreationForm.Meta):
        model = UserModel
        fields = ['email']
        error_messages = {'email': {'unique': 'Korisnik sa ovom e-mail adresom već postoji.',},}

    def save(self, commit=True):
        # Sačuvaj korisnika (ovo će trigerovati Django signal koji ce napraviti prazan Profil)
        user = super().save(commit=commit)

        # Popuni profil koji je Django signal napravio dodavanjem imena i prezimena
        profile = user.profile
        profile.first_name = self.cleaned_data['first_name']
        profile.last_name = self.cleaned_data['last_name']

        if commit:
            profile.save()

        return user

#-----------------------------------------------------------------------------------------------------------------------
class AppUserLoginForm(AuthenticationForm):
    username = forms.EmailField(
        widget=forms.TextInput(attrs={
            'autofocus': True,
            'placeholder': 'E-mail adresa'
        }),
    )
    password = forms.CharField(
        strip=False,
        widget=forms.PasswordInput(attrs={
            'autocomplete': 'current-password',
            'placeholder': 'Lozinka'
        }),
    )

#-----------------------------------------------------------------------------------------------------------------------
class AppUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = UserModel

#-----------------------------------------------------------------------------------------------------------------------
class ProfileEditForm(RemovePictureMixin, forms.ModelForm):
    pass