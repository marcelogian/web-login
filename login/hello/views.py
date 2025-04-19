from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import CreateUserForm
from django.contrib.auth.models import User

@login_required(login_url='login')
def home(request):
    context = {}
    return render(request, 'setup/main.html', context)

def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            email = request.POST.get('email')
            password = request.POST.get('password')

            user = authenticate(request, email=email, password=password)

            if user is not None:
                auth_login(request, user)
                return redirect('home')
            else:
                messages.info(request, 'Email or Password is incorrect. Try Again')

        context = {}
        return render(request, 'setup/login.html', context)

def logoutPage(request):
    logout(request)
    return redirect('login')

def register(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = CreateUserForm()

        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                email = form.cleaned_data.get('email')
                first_name = form.cleaned_data.get('first_name')
                last_name = form.cleaned_data.get('last_name')
                password = form.cleaned_data.get('password1')

                # Generate a unique username from the email
                username = email.split('@')[0]
                
                # Ensure the username is unique
                while User.objects.filter(username=username).exists():
                    username += str(User.objects.count())

                # Create the user
                user = User.objects.create_user(
                    username=username,  # generated unique username
                    email=email,
                    password=password,
                    first_name=first_name,
                    last_name=last_name
                )
                user.save()
                messages.success(request, f"Created an account for {first_name} {last_name}")
                return redirect('login')

        context = {'form': form}
        return render(request, 'setup/register.html', context)
