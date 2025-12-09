from django.urls import path
from . import views

urlpatterns = [
    path('', views.profile, name='profile'),
    path('edit/', views.edit_profile, name='edit_profile'),
    path('user/<str:username>/', views.user_profile_view, name='user_profile'),
]