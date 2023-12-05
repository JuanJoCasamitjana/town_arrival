from django.shortcuts import render, get_object_or_404, redirect
from app.forms import CasaForm
from app.models import Casa
from users.models import Profile
from django.urls import reverse_lazy
from django.contrib.auth.decorators import user_passes_test

def vistaVentas(request):
    try:
        profiles = Profile.objects.all()
        compras=[]
        if request.user.is_superuser:
            for usuarios in profiles:
                compras.append(usuarios)
        else:
            compras = ['no ere superuser quillo']
    except Profile.DoesNotExist:
        compras = ['no hay profiles surmanito']

    return render(request, 'ventasAdmin.html', {
        'compras': compras
    })

def vistaClientes(request):
    try:
        if request.user.is_authenticated:
            profiles = Profile.objects.all()
            nombres = []
            if request.user.is_superuser:
                for usuario in profiles:
                    nombres.append(usuario.user.username)
            else:
                nombres = ['no ere superuser quillo']
        else:
            nombres = ['usuario no autenticado']
    except Profile.DoesNotExist:
        nombres = ['no hay profiles surmanito']
    return render(request, 'gestionAdmin.html', {
        'nombres': nombres
    })

@user_passes_test(lambda u: u.is_superuser)  # Solo permitir acceso a administradores
def editar_casa(request, pk):
    casa = get_object_or_404(Casa, pk=pk)

    if request.method == 'POST':
        form = CasaForm(request.POST, instance=casa)
        if form.is_valid():
            form.save()
            return redirect('catalogo_casas')  # Redirige a la página deseada después de la edición
    else:
        form = CasaForm(instance=casa)

    return render(request, 'editar_casa.html', {'form': form})