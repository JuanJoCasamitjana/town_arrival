# Ejemplo de vista para crear una reclamación
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from reclamaciones.models import Reclamacion
from .forms import ReclamacionForm

@login_required
def crear_reclamacion(request):
    if request.method == 'POST':
        form = ReclamacionForm(request.user, request.POST, request.FILES)

        if form.is_valid():
            # Crear la casa con la URL obtenida
            reclamacion = form.save(commit=False)
            reclamacion.usuario = request.user.profile
            reclamacion.save()

            return redirect('')

    else:
        form = ReclamacionForm()

    return render(request, 'creacion_reclamacion.html', {'form': form})


def mostrar_reclamaciones(request):
    reclamaciones = Reclamacion.objects.all()
    return render(request, 'ver_reclamaciones.html', {'reclamaciones': reclamaciones})