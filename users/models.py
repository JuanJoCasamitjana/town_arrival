from django.db import models
from django.contrib.auth.models import User
from shoppingCart.models import Carrito
from django.apps import apps

# Create your models here.
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
    carrito = models.OneToOneField(Carrito, on_delete=models.CASCADE, blank=True, null=True)
    alquiladas = models.ManyToManyField('app.Casa', blank=True)
    def __str__(self):
        return self.user.username
    

