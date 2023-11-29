from django.db import models
from django.contrib.auth.models import User

# Create your models here.
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
    def __str__(self):
        return self.user.username

