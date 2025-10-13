from django.contrib import admin
from IGDReviews.models import Review 
from profiles.models import Friendship

admin.site.register(Review)
admin.site.register(Friendship)