from django.shortcuts import render, get_object_or_404
from shoppingCart.models import Carrito
from users.models import Profile

def pagos(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            carrito_usuario = Carrito.objects.get(user=request.user)
            cliente = Profile.objects.get(user=request.user)
            productos_en_carrito = carrito_usuario.productos.all()
            total_vendido = carrito_usuario.total

            # Actualizar el campo 'alquiladas' del perfil del usuario
            for casa in productos_en_carrito:
                cliente.alquiladas.add(casa)
            cliente.save()
            todos = cliente.alquiladas.all()
            # Restablecer el carrito del usuario
            carrito_usuario.productos.clear()
            carrito_usuario.total = 0
            carrito_usuario.save()
        else:
            productos_en_carrito = []
            total_vendido = 0


    return render(request, 'pagos.html', {
        'todos': todos,
        'total_vendido': total_vendido
    })