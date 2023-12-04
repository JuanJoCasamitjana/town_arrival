from django.apps import apps
from django.db import models
from django.contrib.auth.models import User
from users.models import Alquiler

class Carrito(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    productos = models.ManyToManyField(Alquiler, blank=True)  # Importación diferida
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    payment_bool = models.BooleanField(default=False)
    stripe_checkout_id= models.CharField(max_length=500,default='')
    
    def __str__(self):
        return f"Carrito de {self.user.username}"
    
    class Meta:
        app_label = 'shoppingCart'