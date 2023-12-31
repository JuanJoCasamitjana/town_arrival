from dataclasses import dataclass
from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.forms import ValidationError
from django.http import HttpResponse
from datetime import date, datetime
from django.apps import apps


class User(AbstractUser):
    email = models.EmailField(unique=True)
    groups = models.ManyToManyField(Group, related_name='custom_user_groups')
    user_permissions = models.ManyToManyField(
        Permission, related_name='custom_user_permissions'
    )

class Alquiler(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    alquilo = models.ForeignKey('app.Casa', on_delete=models.CASCADE)  # Referencia a la Casa alquilada
    FechaInicio = models.DateField()
    FechaFinal = models.DateField()
    modosEntrega = models.CharField(max_length=2, choices=[
        ("LB", "Dejar las llaves en buzón"),
        ("LV", "Dejar las llaves con vecino"),
        ("LP", "Entrega de llaves personal")
    ], default='LP')
    
    def clean(self):
        super().clean()
        fecha_actual = date.today()
        if type(self.FechaFinal) != date:
            fechaFinal = self.FechaFinal.date()
            fechaInicia = self.FechaFinal.date()
        else:
            fechaFinal = self.FechaFinal
            fechaInicia = self.FechaFinal
        if fechaInicia and fechaFinal:
            if fechaInicia > fechaFinal:
                raise ValidationError("La fecha de inicio no puede ser mayor que la fecha de finalización.")
            if fechaInicia < fecha_actual:
                raise ValidationError("No puedes volver al pasado.")

    
    def save(self, *args, **kwargs):
        self.clean()  # Llama al método clean antes de guardar
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.alquilo.titulo} - ({self.FechaFinal.isoformat()} - {self.FechaInicio.isoformat()})"

class Profile(models.Model):
    #Modelo de usuario basico de Django
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    #Propiedades extra
    avatar = models.URLField()
    bio = models.TextField(blank=True)
    rol = models.CharField(max_length=2,choices=[
        ("Ar", "Arrendador"),
        ("Cl", "Cliente")
    ])
    carrito = models.OneToOneField('shoppingCart.Carrito', on_delete=models.CASCADE, blank=True, null=True)
    alquiladas = models.ManyToManyField(Alquiler, blank=True)
    def __str__(self):
        return self.user.username
    


