from django.contrib.auth.models import User
from django.db import models

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

from django.db import models
from django.conf import settings # Use settings.AUTH_USER_MODEL

class Friendship(models.Model):
    # The user who initiated the request
    from_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='friendship_requests_sent',
        on_delete=models.CASCADE
    )
    # The user who received the request
    to_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='friendship_requests_received',
        on_delete=models.CASCADE
    )
    # Status of the friendship (e.g., 'pending', 'accepted')
    status = models.CharField(max_length=10, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Ensures a user can't request friendship with the same person twice
        unique_together = ('from_user', 'to_user')

    def __str__(self):
        return f"{self.from_user.username} is {self.status} with {self.to_user.username}"
