from django.shortcuts import render, redirect, get_object_or_404
from .forms import GameSearchForm, ReviewForm
from django.contrib.auth.decorators import login_required
from .igdb_api import search_igdb_games, get_igdb_game_details
from .models import Review, Vote
from django.db.models import Sum, Avg

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

def game_detail_view(request, game_id):
    """
    Displays the details for a single game, including its summary,
    average rating, and all user reviews.
    """
    game_details = get_igdb_game_details(game_id)
    if not game_details:
        # Or render a "game not found" page
        return redirect('search-game')
        
    # **THIS BLOCK IS CRITICAL:** It correctly adds the 'url_big' key 
    # to the 'cover' dictionary before passing it to the template.
    if 'cover' in game_details and 'url' in game_details['cover']:
        cover_url = game_details['cover']['url']
        # The key 'url_big' is set on the cover dictionary
        game_details['cover']['url_big'] = cover_url.replace('t_thumb', 't_cover_big')

    # Fetch reviews from your database for this game
    reviews = Review.objects.filter(game_id=game_id).select_related('user').order_by('-created_at')

    # Calculate the average star rating
    # Use float to ensure it's a number that can be formatted
    average_rating = reviews.aggregate(Avg('stars'))['stars__avg'] 

    context = {
        'game': game_details,
        'reviews': reviews,
        'average_rating': average_rating,
    }
    return render(request, 'reviews/game_detail_page.html', context)
@login_required
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
            new_review.user = request.user
            new_review.game = game_details.get('name')
            cover_data = game_details.get('cover', {})
            #verify we are storing the alrge version of our cover art
            if cover_data:
                new_review.cover_art = cover_data.get('url','').replace('t_thumb', 't_cover_big')
            if 'genres' in game_details:
                genre_names = [genre['name'] for genre in game_details['genres']]
                new_review.genres = ','.join(genre_names)

            #saves a copy of the review to our database
            new_review.save()
            #spits you out at home
            return redirect('/feed')
    else:
        #if the user is not submitting a form, display a blank form
        review_form = ReviewForm()

        context = {
        'form': review_form,
        'game': game_details,
    }
    return render(request, 'reviews/create_review.html', context)

@login_required
def vote_review(request, review_id, vote_type):
    review = get_object_or_404(Review, id=review_id)
    vote_value = Vote.UPVOTE if vote_type == 'up' else Vote.DOWNVOTE

    # Check if a vote already exists
    existing_vote = Vote.objects.filter(user=request.user, review=review).first()

    if existing_vote:
        # If the user is clicking the same button again, remove the vote
        if existing_vote.vote_type == vote_value:
            existing_vote.delete()
        # If the user is changing their vote, update it
        else:
            existing_vote.vote_type = vote_value
            existing_vote.save()
    else:
        # If no vote exists, create a new one
        Vote.objects.create(user=request.user, review=review, vote_type=vote_value)

    # Recalculate the review's total rating
    # The .get('total', 0) or 0 handles the case where there are no votes
    new_rating = Vote.objects.filter(review=review).aggregate(total=Sum('vote_type')).get('total') or 0
    review.rating = new_rating
    review.save()

    # Redirect back to the feed
    return redirect('/feed/')

@login_required
def edit_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)

    # Ensure the user is the owner of the review
    if review.user != request.user:
        # You can redirect or show a forbidden error
        return redirect('feed')

    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            return redirect('feed')
    else:
        form = ReviewForm(instance=review)

    context = {
        'form': form,
        'review': review
    }
    return render(request, 'reviews/edit_review.html', context)

@login_required
def delete_review(request, review_id):
    # Get the review object, or return a 404 if not found
    review = get_object_or_404(Review, id=review_id)

    # Check if the logged-in user is the owner of the review
    if review.user == request.user:
        review.delete()
        # Optionally, you can add a success message here
    return redirect('feed')