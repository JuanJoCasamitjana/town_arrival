from django.contrib import admin
from django.urls import include, path

from app import views
from shoppingCart import views as v
from pagos import views as pago
from vistasAdministrador import views as ad

urlpatterns = [
    path('',views.busqueda,name="index"),
    path('inicio',views.busqueda,name="inicio"),
    path('catalogo-casas/', views.catalogo_casas, name='catalogo_casas'),
    path('casa/<int:casa_id>/', views.info_casa, name='detalle_casa'),
    path('nueva-casa', views.crear_casa, name='crear_casa'),
    path('carrito/', v.carrito, name='carrito'),
    path('agregar_carrito/<int:casa_id>/', v.agregar_carrito, name='agregar_carrito'),
    path('eliminar_del_carrito/<int:producto_id>/', v.eliminar_del_carrito, name='eliminar_del_carrito'),      
    path('pagos/', pago.pagos, name='pagos'),
    path('ventasAdmin/', ad.vistaVentas, name='ventasAdmin'),
    path('gestionAdmin/', ad.vistaClientes, name='gestionAdmin'),
    path('info_casa/<int:casa_id>/', views.info_casa, name='info_casa'),
    path('casa/<int:casa_id>/presentar_reclamacion/', views.presentar_reclamacion, name='presentar_reclamacion'),
    path('mis-reclamaciones', views.mostrar_reclamaciones, name='mis-reclamaciones'),
    path('reclamacion/<int:reclamacion_id>/', views.ver_detalle_reclamacion, name='ver_detalle_reclamacion'),


]