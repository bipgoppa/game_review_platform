from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponse
from .forms import LoginForm
from django.contrib.auth.decorators import login_required


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, "Login successful!")
                return redirect('/feed/')
            else:
                messages.error(request, "Invalid username or password.")
                return redirect('login')

    else:
        form = LoginForm()

    return render(request, 'login/login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('login')

@login_required
def home(request):
    return HttpResponse("Welcome! You are logged in.")

def dashboard(request):
    return render(request, 'home.html')



# Create your views here.
