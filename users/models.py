from django.db import models
from django.contrib.auth.models import User

from django.apps import apps

# Create your models here.
class Alquiler(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    alquilo = models.OneToOneField('app.Casa',on_delete=models.CASCADE, blank=True)
    FechaInicio = models.DateTimeField()
    FechaFinal = models.DateTimeField()
    
    def __str__(self):
        return self.user.username
class Profile(models.Model):
    #Modelo de usuario basico de Django
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    #Propiedades extra
    avatar = models.ImageField(default='default.jpg', upload_to='profile_images') #Cambiar a URL
    email = models.EmailField()
    bio = models.TextField(blank=True)
    rol = models.CharField(max_length=2,choices=[
        ("Ar", "Arrendador"),
        ("Cl", "Cliente")
    ])
    carrito = models.OneToOneField('shoppingCart.Carrito', on_delete=models.CASCADE, blank=True, null=True)
    alquiladas = models.ManyToManyField(Alquiler, blank=True)
    def __str__(self):
        return self.user.username
    


    

