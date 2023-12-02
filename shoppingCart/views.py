from django.shortcuts import redirect, render, get_object_or_404
from shoppingCart.models import Carrito
from django.contrib import messages
from app.models import Casa
from app.models import Alquiler
from datetime import datetime, timedelta
from django.db.models import Q

def carrito(request):
    try:
        if request.user.is_authenticated:
            # Obtener el carrito del usuario o crear uno nuevo si no existe
            carrito_usuario, created = Carrito.objects.get_or_create(user=request.user)
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

def agregar_carrito(request, casa_id):
    if request.method == 'POST':
        if request.user.is_authenticated:
            casa = get_object_or_404(Casa, pk=casa_id)
            usuario = request.user
            
            # Supongamos que deseas establecer la fecha de inicio como el momento actual
            fecha_inicio = datetime.today()
            
            # Supongamos que el alquiler dura 7 días a partir de la fecha de inicio
            fecha_final = fecha_inicio + timedelta(days=7)
            
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
            
            alquiler, created = Alquiler.objects.get_or_create(
                user=usuario,
                alquilo=casa,
                FechaInicio=fecha_inicio,
                FechaFinal=fecha_final
            )

            # Verificar si el alquiler ya está en el carrito antes de agregarlo
            carrito_usuario, created = Carrito.objects.get_or_create(user=usuario)
            if alquiler not in carrito_usuario.productos.all():
                carrito_usuario.productos.add(alquiler)

                # Actualizar el total del carrito después de agregar el producto
                carrito_usuario.total += casa.precioPorDia
                carrito_usuario.save()
                messages.success(request, f"{casa.titulo} ha sido agregada al carrito.")
                print("Producto agregado correctamente al carrito")
            else:
                messages.info(request, f"{casa.titulo} ya está en el carrito.")
                print("El producto ya está en el carrito")
            print("Producto eliminado, redireccionando a la página de detalle de la casa")
            return redirect('detalle_casa', casa_id=casa_id)
        else:
            messages.error(request, "Debes iniciar sesión para agregar al carrito.")

    return redirect('info_casa', casa_id=casa_id)

def eliminar_del_carrito(request, producto_id):
    if request.user.is_authenticated:
        carrito_usuario = Carrito.objects.get(user=request.user)
        
        alquiler = get_object_or_404(Alquiler, pk=producto_id)
        
        carrito_usuario.productos.remove(alquiler)

        print(f"Producto eliminado: {alquiler.alquilo.titulo}")  # Mensaje de depuración
        print(f"Total antes de la resta: {carrito_usuario.total}")  # Mensaje de depuración

        carrito_usuario.total -= alquiler.alquilo.precioPorDia  # Restar el precio del producto eliminado
        carrito_usuario.save()
        alquiler.delete()

        print(f"Total después de la resta: {carrito_usuario.total}")  # Mensaje de depuración

        messages.success(request, f"{alquiler.alquilo.titulo} ha sido eliminado del carrito.")
    else:
        messages.error(request, "Debes iniciar sesión para eliminar productos del carrito.")

    return redirect('carrito')

