from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class AccountForm(UserCreationForm):
    email = forms.EmailField(required=True)
    username = forms.CharField(label='username')
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
