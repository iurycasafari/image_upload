from django import forms

from webapp.core.models import Image


class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ('name', 'image', )
