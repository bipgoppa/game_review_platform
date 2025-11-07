from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User

# Create your models here.
class Review(models.Model):
    game = models.CharField(max_length=100)
    cover_art = models.ImageField()
    playtime = models.DecimalField(max_digits=6, decimal_places=2)
    title = models.CharField(max_length=100)
    body = models.TextField()
    stars = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField(default=0)
    genres = models.CharField(max_length=200, blank=True, default='')

class Vote(models.Model):
    UPVOTE = 1
    DOWNVOTE = -1
    VOTE_CHOICES = (
        (UPVOTE, 'Upvote'),
        (DOWNVOTE, 'Downvote'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='votes')
    vote_type = models.SmallIntegerField(choices=VOTE_CHOICES)

    class Meta:
        # A user can only vote once per review
        unique_together = ('user', 'review')