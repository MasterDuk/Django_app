from django import forms
from .models import Profile
from django.contrib.auth.models import User

class UserForm(forms.ModelForm):
    # pass
    class Meta:
        model = User
        fields = 'username', 'first_name', 'last_name', 'email'


    bio = forms.CharField(initial="")
    images = forms.ImageField()


