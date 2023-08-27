from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

from myauth.models import Profile


class ProfileUploaFileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["avatar", ]
        widgets = {
            'avatar': forms.ClearableFileInput(attrs={'id': 'id_image'}),
        }


