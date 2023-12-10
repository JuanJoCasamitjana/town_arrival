from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import UserRegistrationForm, UserProfileForm, UserLoginForm, ImageUploadForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, authenticate
from app.views import upload_image_to_external_service
from .models import User

def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST, request.FILES)
        profile_form = UserProfileForm(request.POST, request.FILES)
        image_form = ImageUploadForm(request.POST, request.FILES)

        if user_form.is_valid() and profile_form.is_valid() and image_form.is_valid():
            #Subir imagen
            image_file = image_form.cleaned_data['avatar']
            image_url = upload_image_to_external_service(image_file)
            #Cosas de usuario
            user = user_form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.avatar = image_url
            profile.save()
            
            login(request, user)  # Loguear al usuario después de registrarse
            return redirect('catalogo_casas')  # Redirigir a la página de inicio

    else:
        user_form = UserRegistrationForm()
        profile_form = UserProfileForm()
        image_form = ImageUploadForm()

    return render(request, 'register.html', {'user_form': user_form, 'profile_form': profile_form, 'image_form': image_form})


@login_required
def update_profile(request):
    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST, request.FILES, instance=request.user.profile)
        image_form = ImageUploadForm(request.POST, request.FILES, instance=request.user.profile)

        if profile_form.is_valid() and image_form.is_valid():
            image_file = image_form.cleaned_data['avatar']
            image_url = upload_image_to_external_service(image_file)

            profile = profile_form.save(commit=False)
            profile.avatar = image_url
            profile.save()
            return redirect('profile')  # Redirigir a la página de perfil

    else:
        profile_form = UserProfileForm(instance=request.user.profile)
        image_form = ImageUploadForm()

    return render(request, 'update_profile.html', {'profile_form': profile_form,'image_form':image_form})

def user_login(request):
    if request.method == 'POST':
        login_form = UserLoginForm(request.POST)

        if login_form.is_valid():
            email = login_form.cleaned_data['email']
            try:
                user = User.objects.get(email=email)
            except:
                print("FAILED")
                return render(request, 'login.html', {'login_form': login_form})
            password = login_form.cleaned_data['password']
            user = authenticate(request, username=user.username, password=password)
            print(user)
            if user is not None:
                login(request, user)
                return redirect('catalogo_casas')  # Cambia 'home' con el nombre de tu página de inicio

    else:
        login_form = UserLoginForm()

    return render(request, 'login.html', {'login_form': login_form})

def user_logout(request):
    logout(request)
    return redirect("catalogo_casas")