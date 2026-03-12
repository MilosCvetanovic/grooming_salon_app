from multiprocessing.managers import dispatch

from django import forms
from django.shortcuts import redirect


#-----------------------------------------------------------------------------------------------------------------------
# Mixin za dodavanje opcije brisanja slike (X) u add/edit formama
class RemovePictureMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['remove_picture'] = (
            forms.BooleanField(
                required=False,
                widget=forms.CheckboxInput(attrs={'class': 'delete-checkbox'})
            )
        )

#-----------------------------------------------------------------------------------------------------------------------
# Mixin za osiguravanje da korisnik može videti i menjati samo svoje podatke, nikada tuđe.
class UserOwnedModelMixin:
    def get_queryset(self):
        queryset = super().get_queryset()

        if queryset is None:
            return None

        if hasattr(queryset.model, 'user'):
            return queryset.filter(user=self.request.user)

        return queryset.filter(pk=self.request.user.pk)

#-----------------------------------------------------------------------------------------------------------------------
# Mixin koji briše fizički fajl slike sa servera i postavlja polje na None u bazi.
class ImageCleanupMixin:
    image_field_name = 'picture'

    def handle_image_cleanup(self, form):
        if form.cleaned_data.get('remove_picture'):

            obj = form.instance
            image_field = getattr(obj, self.image_field_name, None)

            if image_field:
                image_field.delete(save=False)
                setattr(obj, self.image_field_name, None)
                obj.save()

            return True
        return False

#-----------------------------------------------------------------------------------------------------------------------
# Mixin koji redirektuje korisnika ako je prošao autentifikaciju
class RedirectIfAuthenticatedMixin:
    redirect_url = 'home'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(self.redirect_url)
        return super().dispatch(request, *args, **kwargs)

#-----------------------------------------------------------------------------------------------------------------------
