from decimal import Decimal
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
import requests
from .models import Casa, Categoria, Comentario, Reclamacion
from .forms import CategoriasForm, ReclamacionForm
from .forms import CasaForm, ImageUploadForm, ComentarioForm, AlquilerForm, OptionalImageUploadForm
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponseRedirect
from django.urls import reverse
import requests
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger



API_KEY = '78a7e53f033d954800e7f90ff1fcfca2'

def busqueda(request):
    query = request.GET.get('query', '')
    price = request.GET.get('price', '')
    casas = Casa.objects.all()
    action_url = "/busqueda"
    categorias = Categoria.objects.all()
    if query:
        casas = casas.filter(Q(titulo__icontains=query) | Q(descripcion__icontains=query) | Q(localidad__icontains=query))
    if price:
        price = Decimal(price)
        casas = casas.filter(Q(precioPorDia__lte=price))
    items_por_pagina = 30
    paginator = Paginator(casas, items_por_pagina)
    page = request.GET.get('page')
    try:
        casas = paginator.page(page)
    except PageNotAnInteger:
        casas = paginator.page(1)
    except EmptyPage:
        casas = paginator.page(paginator.num_pages)
    return render(request, 'buscador.html', {
        'casas': casas,
        'query': query,
        'price': price,
        'categorias': categorias,
        'action_url': action_url
    })
# Create your views here.
def index(request):
    return HttpResponse("Hello, world. You're at the town_arrival index.")

def catalogo_casas(request):
    casas = Casa.objects.all()
    items_por_pagina = 30
    paginator = Paginator(casas, items_por_pagina)
    page = request.GET.get('page')
    try:
        casas = paginator.page(page)
    except PageNotAnInteger:
        casas = paginator.page(1)
    except EmptyPage:
        casas = paginator.page(paginator.num_pages)

    return render(request, 'catalogo_casas.html', {'casas': casas})

def info_casa(request, casa_id):
    casa = get_object_or_404(Casa, pk=casa_id)


    es_propietario = False
    form_alquiler = AlquilerForm()
    if request.user.is_authenticated and casa.arrendador == request.user.profile:
        es_propietario = True
    is_owner = es_propietario
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
        'alquiler_form': form_alquiler,
        'is_owner':is_owner
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

def anadir_categorias(request, id):
    casa = Casa.objects.get(pk=id)
    if request.method == 'POST':
        form = CategoriasForm(request.POST)
        if form.is_valid():
            selected_objects = form.cleaned_data['categorias']
            casa.categorias.clear()
            casa.categorias.add(*selected_objects)
            casa.save()
            return redirect('detalle_casa', casa_id=casa.id)
    else:
        form = CategoriasForm()
        return render(request, 'add_categoria.html', {'form':form, 'casa':casa})


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

    return "https://i.ibb.co/GtpDyr5/will-li-kk6wsx-VBuy-A-unsplash.jpg"

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

    return render(request, 'detalle_reclamacion.html', {
        'reclamacion': reclamacion,
    })
def mostrar_formulario_contacto(request):
    return render(request, 'contacto.html')

def contacto(request):
    if request.method == 'POST':
        email = request.POST.get('email', '')
        motivo = request.POST.get('motivo', '')
        mensaje = request.POST.get('mensaje', '')

        asunto = f"Mensaje de contacto: {motivo}"
        cuerpo_mensaje = f"Email: {email}\n\nMensaje: {mensaje}"

        try:
            send_mail(
                asunto,
                cuerpo_mensaje,
                settings.EMAIL_HOST_USER,  # Remitente
                [settings.EMAIL_HOST_USER],  # Se autoenvía el correo
                fail_silently=False,
            )
            # Redirige a una página de éxito después de enviar el correo
            return HttpResponseRedirect(reverse('pagina_de_exito'))
        except Exception as e:
            # Maneja errores en el envío del correo
            print(f"Error al enviar el correo: {e}")
            # En caso de error, redirige a una página de error
            return HttpResponseRedirect(reverse('pagina_de_error'))

    # Si el método no es POST, muestra el formulario nuevamente
    return render(request, 'contacto.html')

def pagina_de_exito(request):
    return render(request, 'exito.html')

def pagina_de_error(request):
    return render(request, 'error.html')

def pagina_inexistente(request):
    return render(request, 'inexistente.html')

def quienes_somos(request):
    return render(request, 'quienes_somos.html')

def por_categoria(request, categoria):
    query = request.GET.get('query', '')
    price = request.GET.get('price', '')
    cat = Categoria.objects.get(url=categoria)
    action_url = f"/busqueda/{cat.url}"
    casas = cat.casa_set.all()
    if query:
        casas = casas.filter(Q(titulo__icontains=query) | Q(descripcion__icontains=query) | Q(localidad__icontains=query))
    if price:
        price = Decimal(price)
        casas = casas.filter(Q(precioPorDia__lte=price))
    items_por_pagina = 30
    paginator = Paginator(casas, items_por_pagina)
    page = request.GET.get('page')

    try:
        casas = paginator.page(page)
    except PageNotAnInteger:
        casas = paginator.page(1)
    except EmptyPage:
        casas = paginator.page(paginator.num_pages)
    return render(request, 'buscador.html', {
        'casas': casas,
        'query': query,
        'price': price,
        'action_url': action_url
    })


    return None

def delete_casa(request, casa_id):
    casa = get_object_or_404(Casa, pk=casa_id)
    user = request.user.profile
    is_owner = user == casa.arrendador
    if is_owner:
        Casa.delete(casa)
    return redirect('catalogo_casas')

def editar_casa(request, casa_id):
    casa = get_object_or_404(Casa, pk=casa_id)
    user = request.user.profile
    is_owner = user == casa.arrendador
    if request.method == 'POST':
        if is_owner:
            form = CasaForm(request.POST, instance=casa)
            image_form = OptionalImageUploadForm(request.POST, request.FILES)

            if form.is_valid() and image_form.is_valid():
                casa = form.save(commit=False)
                image_file = image_form.cleaned_data['imagen']
                if image_file:
                    image_url = upload_image_to_external_service(image_file)
                    casa.imagen = image_url
                casa.save()

                return redirect('detalle_casa', casa_id=casa.id)
        else:
            # Manejar el caso en que el usuario no sea el propietario
            # Puedes redirigir a una página de error, mostrar un mensaje, etc.
            pass
    else:
        form = CasaForm(instance=casa)
        image_form = OptionalImageUploadForm()

    return render(request, 'editar_casa.html', {'form': form, 'image_form': image_form, 'casa': casa})


