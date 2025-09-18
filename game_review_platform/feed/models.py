from django.db import models

# Create your models here.

class Message(models.Model):
    game = models.CharField(max_length=100)
    cover_art = models.ImageField()
    playtime = models.DecimalField(..., max_digits=6, decimal_places=2)
    title = models.CharField(max_length=100)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)