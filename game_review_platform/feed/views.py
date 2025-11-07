from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from IGDReviews.forms import GameSearchForm
from IGDReviews.models import Review
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from profiles.models import Friendship

# Create your views here.


def get_accepted_friend_ids(user):
    # Find all accepted friendships where the user is either the sender or receiver
    accepted_friendships = Friendship.objects.filter(Q(from_user=user) | Q(to_user=user),status='accepted')

    friend_ids = set()
    for friendship in accepted_friendships:
        # Add the ID of the *other* person
        if friendship.from_user == user:
            friend_ids.add(friendship.to_user_id)
        else:
            friend_ids.add(friendship.from_user_id)
            
    return list(friend_ids)
@login_required
def home(request):
    current_user = request.user
    friend_ids = get_accepted_friend_ids(current_user)
    search_form = GameSearchForm()

    selected_genre = request.GET.get('genre', '')

    myReviews = Review.objects.filter(user=current_user).select_related('user')
    friend_reviews = Review.objects.filter(user__id__in=friend_ids).select_related('user')
    highest_rated_reviews = Review.objects.select_related('user')

    if selected_genre:
        myReviews = myReviews.filter(genres__icontains=selected_genre)
        friend_reviews = friend_reviews.filter(genres__icontains=selected_genre)
        highest_rated_reviews = highest_rated_reviews.filter(genres__icontains=selected_genre)

    myReviews = myReviews.order_by('-created_at')
    friend_reviews = friend_reviews.order_by('-created_at')
    highest_rated_reviews = highest_rated_reviews.order_by('-rating')[:10]


    all_reviews = Review.objects.exclude(genres='')
    genres_set = set()
    for review in all_reviews:
        if review.genres:
            genre_list = [g.strip() for g in review.genres.split(',')]
            genres_set.update(genre_list)
    template = loader.get_template('feed/home.html')
    context = {
        'myReviews': myReviews,
        'friend_reviews' : friend_reviews,
        'highest_rated_reviews': highest_rated_reviews,
        'form': search_form,
        'all_genres': sorted(genres_set),
        'selected_genre': selected_genre,
    }
    return HttpResponse(template.render(context, request))