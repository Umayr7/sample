from django import forms
from .models import ImageCompress


class GetImageForm(forms.ModelForm):
    class Meta:
        model = ImageCompress
        fields = [
            'image'
        ]
