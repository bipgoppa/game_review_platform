from django import forms
from .models import Review

class GameSearchForm(forms.Form):
    search_query = forms.CharField(label = 'Search for a Game', max_length = 100, widget = forms.TextInput(attrs={'placeholder' : 'e.g., Elden Ring'}))

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['playtime', 'title', 'body', 'stars']

        widgets = {'review': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Write your review here'}),
                   'starcount': forms.NumberInput(attrs={'min' : 1, 'max':  5}),
                }