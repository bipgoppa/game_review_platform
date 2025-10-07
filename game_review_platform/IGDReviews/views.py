from django.shortcuts import render, redirect
from .forms import GameSearchForm, ReviewForm
from .models import Review
from .igdb_api import search_igdb_games, get_igdb_game_details

# Create your views here.

def search_game_view(request):
    #Creates an instance of the search form to use in code
    form = GameSearchForm() 
    search_results = []
    query = ""
    raw_search_results = []
    
    #Check if submit button was pressed
    if request.method == 'POST':
        #Changes the form to a version using the submitted data
        form = GameSearchForm(request.POST) 
        #cleans the data to prevent injections, and then runs the api function for searching
        if form.is_valid():
            query = form.cleaned_data['search_query']
            raw_search_results = search_igdb_games(query)

            for game in raw_search_results:
                if 'cover' in game and 'url' in game['cover']:
                    cover_url = game['cover']['url']
                    #changes our url for the cover image to a new cover image witha different scale
                    game['cover']['url'] = cover_url.replace('t_thumb', 't_cover_big')
    search_results = raw_search_results
    #creates context for the page we need to render
    context = {
        'form': form, 
        'results': search_results,
        'query': query
    }
    
    #shows the result HTML page, given the specific context we pass in
    return render(request, 'reviews/search_results_page.html', context)
    
def create_review_view(request, game_id):
    #finds a game given the game ID
    game_details = get_igdb_game_details(game_id)
    #if the game is not found, redirect back to a search page
    if not game_details: return redirect('search-game')
    #verify we have a cover url
    if 'cover' in game_details and 'url' in game_details['cover']:
        cover_url = game_details['cover']['url']
        #changes our url for the cover image to a new cover image witha different scale
        game_details['cover']['url_big'] = cover_url.replace('t_thumb', 't_cover_big')

    #if the user is trying to submit a review
    if request.method == 'POST':
        #change the review form object to one filled with our data
        review_form = ReviewForm(request.POST)
        #if this form exists
        if review_form.is_valid():
            #start storing information about the game
            new_review = review_form.save(commit = False)
            new_review.game_id = game_id
            new_review.game = game_details.get('name')
            cover_data = game_details.get('cover', {})
            #verify we are storing the alrge version of our cover art
            if cover_data:
                new_review.cover_art = cover_data.get('url','').replace('t_thumb', 't_cover_big')
            #saves a copy of the review to our database
            new_review.save()
            #spits you out at home
            return redirect('/home')
    else:
        #if the user is not submitting a form, display a blank form
        review_form = ReviewForm()

        context = {
        'form': review_form,
        'game': game_details,
    }
    return render(request, 'reviews/create_review.html', context)