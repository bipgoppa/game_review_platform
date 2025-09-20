from django.urls import path
from . import views



urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('', views.user_login, name='login'),  # /login/
    path('home/', views.home, name='home'),  # /login/home/
]
# homepage after login

