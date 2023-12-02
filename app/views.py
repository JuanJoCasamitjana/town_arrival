from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from .models import Casa, Comentario, Comentario_Reclamacion
from django.db.models import Q
import requests
from .models import Reclamacion
from .forms import ReclamacionForm
from .forms import CasaForm, ImageUploadForm, ComentarioForm
from django.contrib.auth.decorators import login_required



API_KEY = '78a7e53f033d954800e7f90ff1fcfca2'

def busqueda(request):
    query = request.GET.get('query', '')
    casas = Casa.objects.all()

    if query:
        casas = casas.filter(Q(titulo__icontains=query) | Q(descripcion__icontains=query) | Q(localidad__icontains=query))

    return render(request, 'buscador.html', {
        'casas': casas,
        'query':query,
        })
# Create your views here.
def index(request):
    return HttpResponse("Hello, world. You're at the town_arrival index.")

def catalogo_casas(request):
    casas = Casa.objects.all()
    return render(request, 'catalogo_casas.html', {'casas': casas})

def info_casa(request, casa_id):
    casa = get_object_or_404(Casa, pk=casa_id)
    es_propietario = False

    if request.user.is_authenticated and casa.arrendador == request.user.profile:
        es_propietario = True

    comentarios = Comentario.objects.filter(casa=casa)

    if request.method == 'POST' and not es_propietario:
        comentario_form = ComentarioForm(request.POST)
        if comentario_form.is_valid():
            nuevo_comentario = comentario_form.save(commit=False)
            nuevo_comentario.usuario = request.user
            nuevo_comentario.casa = casa
            nuevo_comentario.save()
            return redirect('info_casa', casa_id=casa_id)
    else:
        comentario_form = ComentarioForm()

    return render(request, 'info_casa.html', {
        'casa': casa,
        'es_propietario': es_propietario,
        'comentarios': comentarios,
        'comentario_form': comentario_form,
    })

@login_required
def crear_casa(request):
    if request.method == 'POST':
        form = CasaForm(request.POST, request.FILES)
        image_form = ImageUploadForm(request.POST, request.FILES)

        if form.is_valid() and image_form.is_valid():
            # Subir imagen al servicio externo y obtener la URL
            image_file = image_form.cleaned_data['imagen']
            image_url = upload_image_to_external_service(image_file)

            # Crear la casa con la URL obtenida
            casa = form.save(commit=False)
            casa.imagen = image_url
            casa.arrendador = request.user.profile
            casa.save()

            return redirect('detalle_casa', casa_id=casa.id)

    else:
        form = CasaForm()
        image_form = ImageUploadForm()

    return render(request, 'crear_casa.html', {'form': form, 'image_form': image_form})

import requests

def upload_image_to_external_service(image_file):
    try:
        upload_url = 'https://api.imgbb.com/1/upload'
        api_key = API_KEY

        files = {'image': image_file}
        params = {'key': api_key}

        response = requests.post(upload_url, params=params, files=files)

        # Verifica si la solicitud fue exitosa
        response.raise_for_status()

        result = response.json()

        if 'data' in result and 'url' in result['data']:
            return result['data']['url']
    except Exception as e:
        print(f"Error al cargar la imagen: {e}")

    return None

def presentar_reclamacion(request, casa_id):
    casa = Casa.objects.get(pk=casa_id)
    
    if request.method == 'POST':
        form = ReclamacionForm(request.POST)
        if form.is_valid():
            reclamacion = form.save(commit=False)
            reclamacion.casa = casa
            reclamacion.usuario = request.user
            reclamacion.save()
            return redirect('detalle_casa', casa_id=casa_id)
    else:
        form = ReclamacionForm()

    return render(request, 'presentar_reclamacion.html', {'form': form, 'casa': casa})


def mostrar_reclamaciones(request):
    reclamaciones = Reclamacion.objects.filter(usuario=request.user)
    return render(request, 'mostrar_reclamaciones.html', {'reclamaciones': reclamaciones})

def ver_detalle_reclamacion(request, reclamacion_id):
    reclamacion = get_object_or_404(Reclamacion, pk=reclamacion_id)
    return render(request, 'detalle_reclamacion.html', {'reclamacion': reclamacion})


def info_reclamacion(request, reclamacion_id):
    reclamacion = get_object_or_404(Reclamacion, pk=reclamacion_id)

    comentarios = Comentario_Reclamacion.objects.filter(reclamacion=reclamacion)

    if request.method == 'POST':
        comentario_form = ComentarioForm(request.POST)
        if comentario_form:
            print("holi")
        else:
            print("suicidio")
        if comentario_form.is_valid():
            nuevo_comentario = comentario_form.save(commit=False)
            nuevo_comentario.usuario = request.user
            nuevo_comentario.reclamacion = reclamacion
            nuevo_comentario.save()
            return redirect('info_reclamacion', reclamacion_id=reclamacion_id)
    else:
        comentario_form = ComentarioForm()

    return render(request, 'detalle_reclamacion.html', {
        'reclamacion': reclamacion,
        'comentarios': comentarios,
        'comentario_form_rec': comentario_form,
    })
