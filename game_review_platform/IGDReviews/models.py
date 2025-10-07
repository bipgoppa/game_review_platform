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