from django.contrib import admin
from django.urls import include, path

from app import views
from shoppingCart import views as v
from pagos import views as pago
from vistasAdministrador import views as ad


urlpatterns = [
    path('', views.busqueda, name='busqueda'),
    path("",views.catalogo_casas,name="index"),
    path('catalogo-casas/', views.catalogo_casas, name='catalogo_casas'),
    path('casa/<int:casa_id>/', views.info_casa, name='detalle_casa'),
    path('nueva-casa', views.crear_casa, name='crear_casa'),
    path('carrito/', v.carrito, name='carrito'),
    path('agregar_carrito/<int:casa_id>/', v.agregar_carrito, name='agregar_carrito'),
    path('pagos/', pago.pagos, name='pagos'),
    path('ventasAdmin/', ad.vistaVentas, name='ventasAdmin'),
    path('gestionAdmin/', ad.vistaClientes, name='gestionAdmin'),
    path('editar_casa/<int:pk>', ad.editar_casa,name='editar_casa' )
]