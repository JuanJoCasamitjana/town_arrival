from django.shortcuts import render, get_object_or_404
from users.models import Profile

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