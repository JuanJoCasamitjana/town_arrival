from django.apps import apps
from django.db import models
from users.models import Alquiler, User

class Carrito(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    productos = models.ManyToManyField(Alquiler, blank=True)  # Importación diferida
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    def __str__(self):
        return f"Carrito de {self.user.username}"
    
    class Meta:
        app_label = 'shoppingCart'