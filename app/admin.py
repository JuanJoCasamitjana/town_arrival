from django.contrib import admin

from app.forms import CategoriaAdminForm
from .models import Casa, Reclamacion, Categoria, Comentario
from shoppingCart.models import Carrito
from django.utils.text import slugify
# Register your models here.
admin.site.register(Casa)
admin.site.register(Reclamacion)
class CategoriaAdmin(admin.ModelAdmin):
    form = CategoriaAdminForm
    readonly_fields = ['url_generated']

    def get_readonly_fields(self, request, obj=None):
        # Devuelve una lista de campos readonly dependiendo de si estás creando o editando
        if obj:
            return ['url_generated']
        else:
            return []

    def url_generated(self, obj):
        return slugify(obj.nombre)

    url_generated.short_description = 'URL Generada'

admin.site.register(Categoria, CategoriaAdmin)
admin.site.register(Comentario)
admin.site.register(Carrito)