from django.shortcuts import render, get_object_or_404
from shoppingCart.models import Carrito

def carrito(request):
    try:
        # Obtener el carrito del usuario actual si está autenticado
        if request.user.is_authenticated:
            carrito_usuario = Carrito.objects.get(user=request.user)
            productos_en_carrito = carrito_usuario.productos.all()
            total_carrito = carrito_usuario.total
        else:
            productos_en_carrito = []
            total_carrito = 0
    except Carrito.DoesNotExist:
        # Si el carrito no existe para el usuario, se crea uno nuevo
        carrito_usuario = Carrito.objects.create(user=request.user)
        productos_en_carrito = []
        total_carrito = 0

    return render(request, 'carrito.html', {
        'productos_en_carrito': productos_en_carrito,
        'total_carrito': total_carrito
    })
