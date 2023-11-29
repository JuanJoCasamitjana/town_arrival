from django.shortcuts import render
from shoppingCart.models import Carrito
from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404
from shoppingCart.models import Carrito
from app.models import Casa

def carrito(request):
    # Obtener el carrito del usuario actual
    if request.user.is_authenticated:
        carrito_usuario = Carrito.objects.get(user=request.user)
        productos_en_carrito = carrito_usuario.productos.all()
        total_carrito = carrito_usuario.total
    else:
        productos_en_carrito = []
        total_carrito = 0

    return render(request, 'carrito.html', {
        'productos_en_carrito': productos_en_carrito,
        'total_carrito': total_carrito
    })

def agregar_carrito(request, casa_id):
    if request.method == 'POST':
        if request.user.is_authenticated:
            casa = get_object_or_404(Casa, pk=casa_id)
            carrito_usuario, created = Carrito.objects.get_or_create(user=request.user)
            carrito_usuario.productos.add(casa)
            messages.success(request, f"{casa.titulo} ha sido agregada al carrito.")
            return redirect('detalle_casa', casa_id=casa_id)
        else:
            messages.error(request, "Debes iniciar sesión para agregar al carrito.")

    return redirect('info_casa', casa_id=casa_id)