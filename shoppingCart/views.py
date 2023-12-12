from decimal import Decimal
import re
import time
from django.http import HttpResponse
from django.core.mail import send_mail
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse
import stripe
from shoppingCart.models import Carrito
from django.contrib import messages
from users.models import Profile, User
from app.models import Casa
from app.models import Alquiler
from datetime import datetime, timedelta
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
import uuid
from django.conf import settings
from app.forms import AlquilerForm
from django.contrib.auth.decorators import login_required
from django.db.models import F

def carrito(request):
    auth =request.user.is_authenticated
    gestion=request.session.get('gestion')
    total_post_gestion=request.session.get('total_post_gestion')
    cosas=request.session.get('cosas')

    try:
        if auth:
            # Obtener el carrito del usuario o crear uno nuevo si no existe
            carrito_usuario, created = Carrito.objects.get_or_create(user=request.user)
            productos_en_carrito = carrito_usuario.productos.all()
            total_carrito = carrito_usuario.total
            gestion=total_carrito<20
            if gestion:
                total_post_gestion= total_carrito + 10
            else:
                total_post_gestion = total_carrito
            cosas = productos_en_carrito.count() >=1 
            stripe.api_key = settings.STRIPE_SECRET_KEY_TEST
            if request.method == 'POST':
                checkout_session = stripe.checkout.Session.create(
                    payment_method_types = ['card'],
                    line_items = [
                        {
                            'price_data': {
                                'currency': 'eur',
                                'product_data': {
                                'name': 'Alquiler_de_casas',
                                },
                                'unit_amount': int(total_post_gestion*100)
                                },
                            'quantity': 1,
                        },
                    ],
                    mode = 'payment',
                    customer_creation = 'always',
                    success_url = settings.REDIRECT_DOMAIN + '/payment_successful?session_id={CHECKOUT_SESSION_ID}',
                    cancel_url = settings.REDIRECT_DOMAIN + '/payment_cancelled',
                )
                return redirect(checkout_session.url, code=303)
        else:
            alquileres = request.session.get('alquileres')
            if not alquileres:
                alquileres = []
            productos_en_carrito = []
            for ids in alquileres:
                alq= Alquiler.objects.get(id = ids)
                productos_en_carrito.append(alq)
            total_carrito = request.session.get('total_carrito')
            if not productos_en_carrito:
                productos_en_carrito = []
            if not total_carrito:
                 total_carrito = 0
            productos_en_carrito = productos_en_carrito
            gestion=Decimal(total_carrito)<20
            if gestion:
                total_post_gestion= Decimal(total_carrito) + 10
            else:
                total_post_gestion = Decimal(total_carrito)
            cosas = len(productos_en_carrito) >=1 
            stripe.api_key = settings.STRIPE_SECRET_KEY_TEST
            if request.method == 'POST':
                checkout_session = stripe.checkout.Session.create(
                    payment_method_types = ['card'],
                    line_items = [
                        {
                            'price_data': {
                                'currency': 'eur',
                                'product_data': {
                                'name': 'Alquiler_de_casas',
                                },
                                'unit_amount': int(total_post_gestion*100)
                                },
                            'quantity': 1,
                        },
                    ],
                    mode = 'payment',
                    customer_creation = 'always',
                    success_url = settings.REDIRECT_DOMAIN + '/payment_successful?session_id={CHECKOUT_SESSION_ID}',
                    cancel_url = settings.REDIRECT_DOMAIN + '/payment_cancelled',
                )
                return redirect(checkout_session.url, code=303)
    except Carrito.DoesNotExist:
        # Si el carrito no existe para el usuario, se crea uno nuevo
        if auth:
            carrito_usuario = Carrito.objects.create(user=request.user)
        productos_en_carrito = []
        total_carrito = 0


        # Crear una lista de diccionarios con información adicional para cada alquiler en el carrito
    alquileres_con_info = []
    for alquiler in productos_en_carrito:
        dias_alquiler = (alquiler.FechaFinal - alquiler.FechaInicio).days
        total = dias_alquiler * alquiler.alquilo.precioPorDia
        alquiler_info = {
            'alquiler': alquiler,
            'dias_alquiler': dias_alquiler,
            'total':total
        }
        alquileres_con_info.append(alquiler_info)


    request.session['total_carrito'] = total_carrito.__str__()
    print(alquileres_con_info)
    return render(request, 'carrito.html', {
        'productos_en_carrito': alquileres_con_info,
        'total_carrito': total_carrito,
        'auth' : auth,
        'gestion': gestion,
        'total_post_gestion': total_post_gestion,
        'cosas': cosas,
    })

def agregar_carrito(request, casa_id):
    if request.method == 'POST':
        if request.user.is_authenticated:
            casa = get_object_or_404(Casa, pk=casa_id)
            usuario = request.user
            form_alquiler = AlquilerForm(request.POST)
            if form_alquiler.is_valid():
                fecha_inicio = form_alquiler.cleaned_data['fecha_inicio']
                fecha_final = form_alquiler.cleaned_data['fecha_fin']
                fecha_inicio = datetime.combine(fecha_inicio, datetime.min.time())
                fecha_final = datetime.combine(fecha_final, datetime.max.time())

            
                # Validación para asegurar que FechaInicio no sea mayor que FechaFinal
                if fecha_inicio > fecha_final:
                    messages.error(request, "La fecha de inicio no puede ser mayor que la fecha de finalización.")
                    return HttpResponse('La fecha inicio no puede ser mayor a la fecha fin.')
                

                modos_entrega = form_alquiler.cleaned_data['modoEntrega']
            # Verificar si el usuario ya tiene un alquiler activo para esta casa
                alquiler_existente = Alquiler.objects.filter(
                    Q(alquilo=casa) &(
                    Q(FechaInicio__lte=fecha_inicio, FechaFinal__gte=fecha_inicio) |
                    Q(FechaInicio__lte=fecha_final, FechaFinal__gte=fecha_final) |
                    Q(FechaInicio__gte=fecha_inicio, FechaFinal__lte=fecha_final))).exists()
            
                if alquiler_existente:
                    messages.error(request, f"Ya tienes un alquiler activo para esta casa.")
                    return redirect('info_casa', casa_id=casa_id)
            
            alquiler, created = Alquiler.objects.get_or_create(
                user=usuario,
                alquilo=casa,
                FechaInicio=fecha_inicio,
                FechaFinal=fecha_final,
                modosEntrega=modos_entrega
            )

            # Verificar si el alquiler ya está en el carrito antes de agregarlo
            carrito_usuario, created = Carrito.objects.get_or_create(user=usuario)
            if alquiler not in carrito_usuario.productos.all():
                carrito_usuario.productos.add(alquiler)
                dias= (alquiler.FechaFinal - alquiler.FechaInicio).days
                # Actualizar el total del carrito después de agregar el producto
                carrito_usuario.total += casa.precioPorDia * dias
                carrito_usuario.save()
                messages.success(request, f"{casa.titulo} ha sido agregada al carrito.")
                print("Producto agregado correctamente al carrito")
            else:
                messages.info(request, f"{casa.titulo} ya está en el carrito.")
                print("El producto ya está en el carrito")
            print("Producto eliminado, redireccionando a la página de detalle de la casa")
            return redirect('detalle_casa', casa_id=casa_id)
        else:
            casa = get_object_or_404(Casa, pk=casa_id)
            form_alquiler = AlquilerForm(request.POST)
            if form_alquiler.is_valid():
                fecha_inicio = form_alquiler.cleaned_data['fecha_inicio']
                fecha_final = form_alquiler.cleaned_data['fecha_fin']
                fecha_inicio = datetime.combine(fecha_inicio, datetime.min.time())
                fecha_final = datetime.combine(fecha_final, datetime.max.time())
                modos_entrega = form_alquiler.cleaned_data['modoEntrega']
            # Verificar si el usuario ya tiene un alquiler activo para esta casa
                alquiler_existente = Alquiler.objects.filter(
                    Q(alquilo=casa) &(
                    Q(FechaInicio__lte=fecha_inicio, FechaFinal__gte=fecha_inicio) |
                    Q(FechaInicio__lte=fecha_final, FechaFinal__gte=fecha_final) |
                    Q(FechaInicio__gte=fecha_inicio, FechaFinal__lte=fecha_final))).exists()
            
                if alquiler_existente:
                    messages.error(request, f"Ya tienes un alquiler activo para esta casa.")
                    print("tontito borra la abse de datos")
                    return redirect('info_casa', casa_id=casa_id)
            
            

            alquileres = request.session.get('alquileres')
            if not alquileres:
                 alquileres = []
            alquiler, created = Alquiler.objects.get_or_create(
                alquilo=casa,
                FechaInicio=fecha_inicio,
                FechaFinal=fecha_final,
                modosEntrega=modos_entrega
            )
            print(alquiler)
            if alquiler.id not in alquileres:
                alquileres.append(alquiler.id)
                request.session['alquileres'] = alquileres
                dias= (alquiler.FechaFinal - alquiler.FechaInicio).days
                # Actualizar el total del carrito después de agregar el producto
                total_carrito = request.session.get('total_carrito')
                if not total_carrito:
                    total_carrito = Decimal(0.)
                else:
                    total_carrito = Decimal(total_carrito)
                total_carrito += casa.precioPorDia * dias
                request.session['total_carrito'] = total_carrito.__str__()
                messages.success(request, f"{casa.titulo} ha sido agregada al carrito.")
            else:
                messages.info(request, f"{casa.titulo} ya está en el carrito.")
                print("El producto ya está en el carrito")
            print("Producto eliminado, redireccionando a la página de detalle de la casa")
            return redirect('detalle_casa', casa_id=casa_id)

    return redirect('info_casa', casa_id=casa_id)

def actualizar_dias_alquiler(request, producto_id):
    if request.method == 'POST':
        nuevos_dias = request.POST.get('nuevos_dias')
        try:
            nuevos_dias = int(nuevos_dias)
            if nuevos_dias < 1:
                return HttpResponse('Los días no pueden ser negativos..')
            else:
                alquiler = get_object_or_404(Alquiler, pk=producto_id)

                # Guardar el precio actual del alquiler antes de actualizar los días
                precio_alquiler_anterior = alquiler.alquilo.precioPorDia * (alquiler.FechaFinal - alquiler.FechaInicio).days

                # Actualizar la duración del alquiler
                alquiler.FechaFinal = alquiler.FechaInicio + timedelta(days=nuevos_dias)
                alquiler.save()

                # Calcular el nuevo precio del alquiler
                precio_alquiler_nuevo = alquiler.alquilo.precioPorDia * nuevos_dias

                # Actualizar el precio del alquiler en el carrito
                carrito_usuario = Carrito.objects.get(user=request.user)
                carrito_usuario.total = F('total') - precio_alquiler_anterior + precio_alquiler_nuevo
                carrito_usuario.save()

                return redirect('carrito')
        except ValueError:
            # Realiza alguna acción si no se puede convertir a un número entero (por ejemplo, mostrar un mensaje de error)
            return HttpResponse('Tienes que poner números enteros.')
    else:

        return render(request, 'carrito.html')

def eliminar_del_carrito(request, producto_id):
    if request.user.is_authenticated:
        carrito_usuario = Carrito.objects.get(user=request.user)
        alquiler = get_object_or_404(Alquiler, pk=producto_id)
        
        carrito_usuario.productos.remove(alquiler)

        dias = (alquiler.FechaFinal - alquiler.FechaInicio).days
        carrito_usuario.total -= alquiler.alquilo.precioPorDia * dias

        if carrito_usuario.total <= 0:
            carrito_usuario.total = 0

        carrito_usuario.save()

        alquiler.delete()


        print(f"Total después de la resta: {carrito_usuario.total}")  # Mensaje de depuración

        messages.success(request, f"{alquiler.alquilo.titulo} ha sido eliminado del carrito.")
    else:

        messages.error(request, "Debes iniciar sesión para eliminar productos del carrito.")

        alquileres = request.session.get('alquileres')
        alquiler = get_object_or_404(Alquiler, pk=producto_id)
        alquileres.remove(producto_id)
        request.session['alquileres'] = alquileres
        
        dias= (alquiler.FechaFinal - alquiler.FechaInicio).days
        # Actualizar el total del carrito después de agregar el producto
        total_carrito = Decimal(request.session.get('total_carrito'))
        total_carrito -= alquiler.alquilo.precioPorDia * dias
        request.session['total_carrito'] = total_carrito.__str__()
        messages.success(request, f"{alquiler.alquilo.titulo} ha sido eliminada del carrito.")
        alquiler.delete()

    return redirect('carrito')

def pagos(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            user_payment = Carrito.objects.get(user=request.user)
            cliente = Profile.objects.get(user=request.user)
            productos_en_carrito = user_payment.productos.all()
            total_vendido = user_payment.total
            if total_vendido < 20:
                total_vendido = total_vendido + 10
            for alq in productos_en_carrito:
                cliente.alquiladas.add(alq)
                hogar = Casa.objects.get(titulo = alq.alquilo.titulo)
                hogar.ocupadas.add(alq)
                hogar.save()
            cliente.save()
            todos = productos_en_carrito
            # Restablecer el carrito del usuario
            asunto = 'Compra realizada en Town Arrival'
            cuerpo_mensaje = f"Se ha realizado su compra con exito. Método utilizado: Contrarrembolso. Importe total: {user_payment.total}."
            send_mail(
                asunto,
                cuerpo_mensaje,
                settings.EMAIL_HOST_USER,
                [cliente.user.email],  
                fail_silently=False,
            )
            user_payment.productos.clear()
            user_payment.total = 0
            user_payment.save()
        else:
            productos_en_carrito = request.session.get('alquileres')
            total_vendido = Decimal(request.session.get('total_carrito'))
            if total_vendido < 20:
                total_vendido = total_vendido + 10
            for alq in productos_en_carrito:
                hogar = Casa.objects.get(titulo = alq.alquilo.titulo)
                hogar.ocupadas.add(alq)
                hogar.save()
            todos = productos_en_carrito


    return render(request, 'pagos.html', {
        'todos': todos,
        'total_vendido': total_vendido
    })




def payment_successful(request):
    if request.user.is_authenticated:
        stripe.api_key = settings.STRIPE_SECRET_KEY_TEST
        checkout_session_id = request.GET.get('session_id', None)
        user_payment = Carrito.objects.get(user=request.user)
        cliente = Profile.objects.get(user=request.user)
        productos_en_carrito = user_payment.productos.all()
        total_vendido = user_payment.total
        user_payment.stripe_checkout_id = checkout_session_id
        if total_vendido < 20:
            total_vendido = total_vendido + 10
        for alq in productos_en_carrito:
            cliente.alquiladas.add(alq)
            hogar = Casa.objects.get(titulo = alq.alquilo.titulo)
            hogar.ocupadas.add(alq)
            hogar.save()
        cliente.save()
        todos = productos_en_carrito
        asunto = 'Compra realizada en Town Arrival'
        cuerpo_mensaje = f"Se ha realizado su compra con exito. Método utilizado: Tarjeta. Importe total: {total_vendido}."
        send_mail(
                asunto,
                cuerpo_mensaje,
                settings.EMAIL_HOST_USER,
                [cliente.user.email],  
                fail_silently=False,
            )
        user_payment.productos.clear()
        user_payment.total = 0
        user_payment.save()
        
    else:
        stripe.api_key = settings.STRIPE_SECRET_KEY_TEST
        checkout_session_id = request.GET.get('session_id', None)
        productos_en_carrito = request.session.get('alquileres')
        total_vendido = Decimal(request.session.get('total_carrito'))
        if total_vendido < 20:
            total_vendido = total_vendido + 10
        for alq in productos_en_carrito:
            hogar = Casa.objects.get(titulo = alq.alquilo.titulo)
            hogar.ocupadas.add(alq)
            hogar.save()
        todos = productos_en_carrito
    return render(request, 'pagos.html', {'todos': todos,
        'total_vendido': total_vendido})
    


def payment_cancelled(request):
	stripe.api_key = settings.STRIPE_SECRET_KEY_TEST
	return render(request, 'pago_cancelado.html')


@csrf_exempt
def stripe_webhook(request):
	stripe.api_key = settings.STRIPE_SECRET_KEY_TEST
	time.sleep(10)
	payload = request.body
	signature_header = request.META['HTTP_STRIPE_SIGNATURE']
	event = None
	try:
		event = stripe.Webhook.construct_event(
			payload, signature_header, settings.STRIPE_WEBHOOK_SECRET_TEST
		)
	except ValueError as e:
		return HttpResponse(status=400)
	except stripe.error.SignatureVerificationError as e:
		return HttpResponse(status=400)
	if event['type'] == 'checkout.session.completed':
		session = event['data']['object']
		session_id = session.get('id', None)
		time.sleep(15)
		user_payment = Carrito.objects.get(stripe_checkout_id=session_id)
		user_payment.payment_bool = True
		user_payment.save()
	return HttpResponse(status=200)