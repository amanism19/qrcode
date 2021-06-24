from django import forms
from .models import *

class ImageForm(forms.ModelForm):
    """Form for the image model"""
    class Meta:
        model = Image
        fields = ('title', 'image')

class AdvImageForm(forms.ModelForm):
    """Form for the image model"""
    class Meta:
        model = AdvImage
        fields = ('title', 'image')