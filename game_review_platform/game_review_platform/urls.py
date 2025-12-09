"""
URL configuration for game_review_platform project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from IGDReviews import views
from django.conf import settings
from django.conf.urls.static import static
from profiles import views as profile_views


def home_redirect(request):
    if request.user.is_authenticated:
        return redirect('feed')
    return redirect('login')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', include('login.urls')),
    path('feed/', include('feed.urls'), name='feed-home'),
    path('create_account/', include('create_account.urls')),

    path('search/', views.search_game_view, name = 'search-game'),
    path('review/new/<int:game_id>/', views.create_review_view, name = 'create-review'),
    path('review/edit/<int:review_id>/', views.edit_review, name='edit_review'),
    path('review/delete/<int:review_id>/', views.delete_review, name='delete_review'),
    path('profile/', profile_views.profile, name='profile'),
    path('profile/edit/', profile_views.edit_profile, name='edit_profile'),
    path('', include('profiles.urls')),
    path('friends/', profile_views.friends_view, name='friends_page'),
    path('', include('IGDReviews.urls')), # Include the URLs for voting
    
    path('', home_redirect, name='home'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
