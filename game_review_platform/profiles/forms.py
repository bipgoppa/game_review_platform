from django import forms
from django.contrib.auth.models import User
from .models import Profile

class FriendRequestForm(forms.Form):
    username = forms.CharField(
        label='Username', 
        max_length=150,
        widget=forms.TextInput(attrs={'placeholder': 'Enter a username to send a request'}))

class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email']

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'avatar']