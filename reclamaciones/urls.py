from django.contrib import admin
from django.urls import include, path

from reclamaciones import views

urlpatterns = [
    path('crear_reclamacion', views.crear_reclamacion, name='crearReclamaciones'),
    path('ver_reclamaciones',views.mostrar_reclamaciones, name='verReclamaciones'),
    ]