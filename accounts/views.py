
from .forms import CreateUserForm
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages
from django.shortcuts import render, redirect

from store.models import Customer

# Create your views here.


User = get_user_model()


def register(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            Customer.objects.create(user=user, name=user.username, email=user.email)
            username = form.cleaned_data.get('username')
            messages.success(request, 'Compte crée pour ' + username + '. Connectez vous avec vos informations.')
            return redirect('accounts:login')
        else:
            form = CreateUserForm

    context = {'form': form}
    return render(request, 'accounts/register.html', context)


def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('store:index')
        else:
            messages.info(request, 'Identifiants invalides.')

    context = {}
    return render(request, 'accounts/login.html', context)


def logout_user(request):
    logout(request)
    return redirect('store:index')


def profile(request):
    return HttpResponse(f"Bienvenue {request.user.email}")
