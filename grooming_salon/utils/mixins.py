from django import forms

class RemovePictureMixin:
    remove_picture = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'delete-checkbox'})
    )
