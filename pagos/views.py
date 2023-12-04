import time
from django.http import HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from shoppingCart.models import Carrito
from users.models import Profile
from app.models import Casa
import stripe
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

def pagos(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            user_payment = Carrito.objects.get(user=request.user)
            cliente = Profile.objects.get(user=request.user)
            productos_en_carrito = user_payment.productos.all()
            total_vendido = user_payment.total
            
            for alq in productos_en_carrito:
                cliente.alquiladas.add(alq)
                hogar = Casa.objects.get(titulo = alq.alquilo.titulo)
                hogar.ocupadas.add(alq)
                hogar.save()
            cliente.save()
            todos = productos_en_carrito
            # Restablecer el carrito del usuario
            user_payment.productos.clear()
            user_payment.total = 0
            user_payment.save()
        else:
            productos_en_carrito = []
            total_vendido = 0


    return render(request, 'pagos.html', {
        'todos': todos,
        'total_vendido': total_vendido
    })
    
def stripePagos(request):
    user_payment = Carrito.objects.get(user=request.user)
    productos_en_carrito = user_payment.productos.all()
    total_vendido = user_payment.total
    if request.method == 'POST':
        checkout_session = stripe.checkout.Session.create(
            payment_method_types = ['card'],
            line_items = [
                {
                    'price' : total_vendido,
                    'quantity': 1,
                },
            ],
            mode = 'payment',
            customer_creation = 'always',
            succes_url = settings.REDIRECT_DOMAIN + '/ payment_successful?session_id={CHECKOUT_SESSION_ID}',
            cancel_url=settings.REDIRECT_DOMAIN + '/payment_cancelled' 
        )
        return redirect(checkout_session.url, code=303)
    return render(request, 'carrito.html', {
        'productos_en_carrito': productos_en_carrito,
        'total_carrito': total_vendido
    })
    
    
def payment_successful(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY_TEST
    cliente = Profile.objects.get(user=request.user)
    checkout_session_id = request.GET.get('session_id', None)
    session = stripe.checkout.Session.retrieve(checkout_session_id)
    customer = stripe.Customer.retrieve(session.customer)
    user_id = request.user
    user_payment = Carrito.objects.get(user=user_id)
    user_payment.stripe_checkout_id = checkout_session_id
    productos_en_carrito = user_payment.productos.all()
    total_vendido = user_payment.total

    for alq in productos_en_carrito:
        cliente.alquiladas.add(alq)
        hogar = Casa.objects.get(titulo = alq.alquilo.titulo)
        hogar.ocupadas.add(alq)
        hogar.save()
    cliente.save()
    todos = productos_en_carrito
    # Restablecer el carrito del usuario
    user_payment.productos.clear()
    user_payment.total = 0
    user_payment.save()
    return render(request, 'pagos.html', {
        'todos': todos,
        'total_vendido': total_vendido
    })


def payment_cancelled(request):
	stripe.api_key = settings.STRIPE_SECRET_KEY_TEST
	return render(request, 'user_payment/payment_cancelled.html')


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