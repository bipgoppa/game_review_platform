from django import forms
from .models import Review

class GameSearchForm(forms.Form):
    #defines the search form that allows you to search games
    search_query = forms.CharField(label = 'Search for a Game', max_length = 100, widget = forms.TextInput(attrs={'placeholder' : 'Enter Search e.g., Elden Ring'}))

class ReviewForm(forms.ModelForm):
    #defines a form based off of the Review model, making the fields exposed for the form, and defines new information for stars and body of review
    class Meta:
        model = Review
        fields = ['playtime', 'title', 'body', 'stars']

        widgets = {'body': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Write your review here'}),
                   'stars': forms.NumberInput(attrs={'min' : 1, 'max':  5}),
                }