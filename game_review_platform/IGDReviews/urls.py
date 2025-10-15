from django.urls import path
from . import views

urlpatterns = [
    # URL for voting on a review
    path('review/<int:review_id>/vote/<str:vote_type>/', views.vote_review, name='vote_review'),
]