from django.contrib import admin
from .models import Casa, Reclamacion, Categoria, Comentario
from shoppingCart.models import Carrito
# Register your models here.
admin.site.register(Casa)
admin.site.register(Reclamacion)
admin.site.register(Categoria)
admin.site.register(Comentario)
admin.site.register(Carrito)