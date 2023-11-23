from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from .models import Casa
import requests
from .forms import CasaForm, ImageUploadForm

# Create your views here.
def index(request):
    return HttpResponse("Hello, world. You're at the town_arrival index.")

def catalogo_casas(request):
    casas = Casa.objects.all()
    return render(request, 'catalogo_casas.html', {'casas': casas})

def info_casa(request, casa_id):
    casa = get_object_or_404(Casa, pk=casa_id)
    return render(request, 'info_casa.html', {'casa': casa})

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

def upload_image_to_external_service(image_file):
    # Lógica para subir la imagen al servicio externo y obtener la URL
    # Este es un ejemplo simple utilizando el servicio 'imgbb', pero puedes ajustarlo según tus necesidades
    upload_url = 'https://api.imgbb.com/1/upload'
    api_key = '78a7e53f033d954800e7f90ff1fcfca2'  # Reemplaza esto con tu clave de API real

    files = {'image': image_file}
    params = {'key': api_key}

    response = requests.post(upload_url, params=params, files=files)
    result = response.json()

    if 'data' in result and 'url' in result['data']:
        return result['data']['url']

    return None