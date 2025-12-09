from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Friendship, Profile
from .forms import FriendRequestForm, UserEditForm, ProfileEditForm
from django.contrib import messages
from django.db.models import Q
from IGDReviews.models import Review


@login_required
def profile(request):
    user_reviews = Review.objects.filter(user=request.user).order_by('-created_at')

    return render(request, 'profiles/profile.html', {
        'user': request.user,
        'user_reviews': user_reviews
    })

@login_required
def edit_profile(request):
    # Ensure a profile exists for the user, create if not.
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        user_form = UserEditForm(request.POST, instance=request.user)
        profile_form = ProfileEditForm(request.POST, request.FILES, instance=profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('profile')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }
    return render(request, 'profiles/edit_profile.html', context)

@login_required
def friends_view(request):
    current_user = request.user
    form = FriendRequestForm()

    if request.method == 'POST':
        # Logic for sending a friend request
        if 'send_request' in request.POST:
            form = FriendRequestForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data['username']
                try:
                    to_user = User.objects.get(username=username)
                    if to_user == current_user:
                        messages.error(request, "You cannot send a friend request to yourself.")
                    # Check if a friendship already exists or is pending
                    elif Friendship.objects.filter(
                        (Q(from_user=current_user, to_user=to_user) | Q(from_user=to_user, to_user=current_user))
                    ).exists():
                        messages.warning(request, f"A friend request with {username} already exists.")
                    else:
                        Friendship.objects.create(from_user=current_user, to_user=to_user, status='pending')
                        messages.success(request, f"Friend request sent to {username}.")
                except User.DoesNotExist:
                    messages.error(request, f"User '{username}' not found.")
                return redirect('friends_page')

        # Logic for accepting/declining requests
        if 'accept_request' in request.POST:
            friendship_id = request.POST.get('friendship_id')
            friendship = get_object_or_404(Friendship, id=friendship_id, to_user=current_user)
            friendship.status = 'accepted'
            friendship.save()
            messages.success(request, "Friend request accepted.")
            return redirect('friends_page')

    # Get incoming friend requests
    incoming_requests = Friendship.objects.filter(to_user=current_user, status='pending')

    # Get current friends
    accepted_friendships = Friendship.objects.filter(
        Q(from_user=current_user) | Q(to_user=current_user),
        status='accepted'
    ).select_related('from_user', 'to_user')

    friends_list = []
    for friendship in accepted_friendships:
        friends_list.append(friendship.to_user if friendship.from_user == current_user else friendship.from_user)

    context = {
        'form': form,
        'incoming_requests': incoming_requests,
        'friends_list': friends_list,
    }
    return render(request, 'profiles/friends.html', context)

@login_required
def user_profile_view(request, username):
    viewed_user = get_object_or_404(User, username=username)
    profile = Profile.objects.get_or_create(user=viewed_user)[0]
    
    user_reviews = viewed_user.reviews.all().order_by('-created_at')

    current_user = request.user
    friendship_status = None
    friendship = None

    # Handle sending a friend request from this page
    if request.method == 'POST' and 'send_request' in request.POST:
        # Prevent sending to self
        if current_user == viewed_user:
            messages.error(request, "You cannot send a friend request to yourself.")
            return redirect('user_profile', username=viewed_user.username)

        # Check if a friendship or request already exists in either direction
        existing = Friendship.objects.filter(
            (Q(from_user=current_user, to_user=viewed_user) | Q(from_user=viewed_user, to_user=current_user))
        ).first()

        if existing:
            messages.warning(request, f"A friendship or request with {viewed_user.username} already exists.")
        else:
            Friendship.objects.create(from_user=current_user, to_user=viewed_user, status='pending')
            messages.success(request, f"Friend request sent to {viewed_user.username}.")

        return redirect('user_profile', username=viewed_user.username)

    # Handle removing a friend from this page
    if request.method == 'POST' and 'remove_friend' in request.POST:
        # Find the accepted friendship between the two users
        friendship_to_remove = Friendship.objects.filter(
            (Q(from_user=current_user, to_user=viewed_user) | Q(from_user=viewed_user, to_user=current_user)),
            status='accepted'
        ).first()

        if friendship_to_remove:
            friendship_to_remove.delete()
            messages.success(request, f"{viewed_user.username} has been removed from your friends.")
        else:
            messages.warning(request, "No active friendship found to remove.")

        return redirect('user_profile', username=viewed_user.username)

    if current_user != viewed_user:
        friendship = Friendship.objects.filter(
            Q(from_user=current_user, to_user=viewed_user) | Q(from_user=viewed_user, to_user=current_user)
        ).first()

        if friendship:
            if friendship.status == 'accepted':
                friendship_status = 'friends'
            elif friendship.from_user == current_user:
                friendship_status = 'pending_sent'
            else:
                friendship_status = 'pending_received'

    context = {
        'viewed_user': viewed_user,
        'profile': profile,
        'user_reviews': user_reviews,
        'friendship_status': friendship_status,
        'friendship': friendship,
    }

    return render(request, 'profiles/user_profile.html', context)
