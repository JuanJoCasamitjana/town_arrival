from django.contrib import admin
from django.urls import include, path

from app import views
from shoppingCart import views as v

urlpatterns = [
    path('', views.busqueda, name='busqueda'),
    path("",views.catalogo_casas,name="index"),
    path('catalogo-casas/', views.catalogo_casas, name='catalogo_casas'),
    path('casa/<int:casa_id>/', views.info_casa, name='detalle_casa'),
    path('nueva-casa', views.crear_casa, name='crear_casa'),
    path('carrito/', v.carrito, name='carrito'),
    
]