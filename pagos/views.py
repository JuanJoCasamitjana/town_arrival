from django.shortcuts import render, get_object_or_404
from shoppingCart.models import Carrito
from users.models import Profile

def pagos(request):

    # Obtener el carrito del usuario actual si está autenticado
    if request.user.is_authenticated:
        carrito_usuario = Carrito.objects.get(user=request.user)
        cliente = Profile.objects.get(user=request.user)
        productos_en_carrito = carrito_usuario.productos.all()
        total_vendido= carrito_usuario.total
        cliente.update(alquiladas=productos_en_carrito)
        carrito_usuario.update(productos = [])
        carrito_usuario.update(total = 0)
    else:
        productos_en_carrito = []
        total_vendido = 0


    return render(request, 'pagos.html', {
        'productos_en_carrito': productos_en_carrito,
        'total_vendido': total_vendido
    })