from django.db import models
from django.contrib.auth.models import User

from django.apps import apps

class Alquiler(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    alquilo = models.ForeignKey('app.Casa', on_delete=models.CASCADE)  # Referencia a la Casa alquilada
    FechaInicio = models.DateField()
    FechaFinal = models.DateField()
    
    def __str__(self):
        return f"{self.user.username} - {self.alquilo.titulo}"
    
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
    


    

