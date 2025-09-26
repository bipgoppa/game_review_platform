from django.shortcuts import render, redirect
from .forms import GameSearchForm, ReviewForm
from .models import Review
from .igdb_api import search_igdb_games, get_igdb_game_details

# Create your views here.

def search_game_view(request):
    # This will be the form instance used in all cases
    form = GameSearchForm() 
    search_results = []

    # Check if the form was submitted
    if request.method == 'POST':
        # Bind the submitted data to the form
        form = GameSearchForm(request.POST) 

        if form.is_valid():
            query = form.cleaned_data['search_query']
            search_results = search_igdb_games(query)
            # The context will be built and rendered at the end

    # This context will be used for both GET requests and POST requests (valid or not)
    context = {
        'form': form, 
        'results': search_results,
        'query': query
    }
    
    # Render the page with the context
    return render(request, 'reviews/search_results_page.html', context)
    
def create_review_view(request, game_id):
    game_details = get_igdb_game_details(game_id)
    if not game_details: return redirect('search-game')
    
    if 'cover' in game_details and 'url' in game_details['cover']:
        cover_url = game_details['cover']['url']
        # Use Python's .replace() method to change the image size
        game_details['cover']['url_big'] = cover_url.replace('t_thumb', 't_cover_big')


    if request.method == 'POST':
        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            new_review = review_form.save(commit = False)
            new_review.game_id = game_id
            new_review.game = game_details.get('name')
            cover_data = game_details.get('cover', {})
            if cover_data:
                new_review.cover_art = cover_data.get('url','').replace('t_thumb', 't_cover_big')
            new_review.save()
            return redirect('/')
    else:
        review_form = ReviewForm()

        context = {
        'form': review_form,
        'game': game_details,
    }
    return render(request, 'reviews/create_review.html', context)