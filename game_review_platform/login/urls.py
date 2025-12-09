from django.urls import path
from . import views



urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('login/home/', views.home, name='home'),  # /login/home/
    path('logout/', views.user_logout, name='logout'),
]
# homepage after login

