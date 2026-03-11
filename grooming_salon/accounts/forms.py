from django import forms
from django.contrib.auth import get_user_model
from grooming_salon.accounts.models import Profile, EmailVerificationToken
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from grooming_salon.utils.utils import send_verification_email
from grooming_salon.utils.validators import validate_capitalized_name
from grooming_salon.utils.mixins import RemovePictureMixin

MAX_LENGTH = 30
UserModel = get_user_model()

# Create your forms here.
#-----------------------------------------------------------------------------------------------------------------------
class AppUserCreationForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=MAX_LENGTH,
        widget=forms.TextInput(attrs={
            'autofocus': True,
            'placeholder': 'Ime',
        }),
        validators=[validate_capitalized_name]
    )
    last_name = forms.CharField(
        max_length=MAX_LENGTH,
        widget=forms.TextInput(attrs={
            'placeholder': 'Prezime',
        }),
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

            # Kreiraj verifikacioni token i pošalji email asinhrono
            token = EmailVerificationToken.objects.create(user=user)
            send_verification_email(user, token.token)

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
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'phone', 'picture']
        widgets = {
            'first_name': forms.TextInput(attrs={'autofocus': True}),
            'last_name': forms.TextInput(),
            'phone': forms.TextInput(),
            'picture': forms.FileInput(attrs={'id': 'photo-input'}),
        }
        labels = {
            'first_name': 'Ime:',
            'last_name': 'Prezime:',
            'phone': 'Telefon:',
            'picture': 'Profilna fotografija:'
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
