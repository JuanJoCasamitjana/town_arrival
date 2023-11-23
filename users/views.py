from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import UserRegistrationForm, UserProfileForm, UserLoginForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, authenticate

def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            
            login(request, user)  # Loguear al usuario después de registrarse
            return redirect('catalogo_casas')  # Redirigir a la página de inicio

    else:
        user_form = UserRegistrationForm()
        profile_form = UserProfileForm()

    return render(request, 'register.html', {'user_form': user_form, 'profile_form': profile_form})


@login_required
def update_profile(request):
    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST, instance=request.user.profile)

        if profile_form.is_valid():
            profile_form.save()
            return redirect('profile')  # Redirigir a la página de perfil

    else:
        profile_form = UserProfileForm(instance=request.user.profile)

    return render(request, 'update_profile.html', {'profile_form': profile_form})

def user_login(request):
    if request.method == 'POST':
        login_form = UserLoginForm(request.POST)

        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('catalogo_casas')  # Cambia 'home' con el nombre de tu página de inicio

    else:
        login_form = UserLoginForm()

    return render(request, 'login.html', {'login_form': login_form})

def user_logout(request):
    logout(request)
    return redirect("catalogo_casas")