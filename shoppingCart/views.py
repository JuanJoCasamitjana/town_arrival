from django.shortcuts import render
from shoppingCart.models import Carrito

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
