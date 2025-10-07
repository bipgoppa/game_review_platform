from django.shortcuts import render, redirect

from .forms import AccountForm


# Create your views here.

def create_account(request):
    if request.method == "POST":
        form = AccountForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/login')

    else:
        form = AccountForm()

    return render(request, 'create_account/create_account.html', {'form': form})
