from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from IGDReviews.forms import GameSearchForm, ReviewForm 
from IGDReviews.models import Review

# Create your views here.
def home(request):
    search_form = GameSearchForm()
    myReviews = Review.objects.all().values()
    template = loader.get_template('feed/home.html')
    context = {'myReviews': myReviews, 'form': search_form,}
    return HttpResponse(template.render(context, request))