from django.shortcuts import render, redirect
from django.contrib import messages

from .forms import AccountForm


# Create your views here.

def create_account(request):
    if request.method == "POST":
        form = AccountForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully! Please log in.")
            return redirect('/login')

    else:
        form = AccountForm()

    return render(request, 'create_account/create_account.html', {'form': form})
