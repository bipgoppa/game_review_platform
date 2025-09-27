from django.contrib import admin
from IGDReviews.models import Review # 1. Import your Review model

# 2. Register your model with the admin site
admin.site.register(Review)