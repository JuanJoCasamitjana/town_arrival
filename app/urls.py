from django.contrib import admin
from django.urls import include, path

from app import views
from shoppingCart import views as v
from pagos import views as pago
from vistasAdministrador import views as ad

urlpatterns = [
    path('busqueda/', views.busqueda, name='busqueda'),
    path('',views.catalogo_casas,name="index"),
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
    path('contacto/', views.contacto, name='contacto'),
    path('formulario-contacto/', views.mostrar_formulario_contacto, name='mostrar_formulario_contacto'),
    path('error-formulario/', views.pagina_de_error, name='pagina_de_error'),
    path('exito-formulario/', views.pagina_de_exito, name='pagina_de_exito'),
    path('inexistente/', views.pagina_inexistente, name='pagina_inexistente'),
]