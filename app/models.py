from django.db import models
from users.models import Profile, Alquiler

# Create your models here.
class Casa(models.Model):
    arrendador = models.ForeignKey(Profile, on_delete=models.CASCADE)
    titulo = models.TextField(blank=False, max_length=150)
    descripcion = models.TextField(blank=False, max_length=500)
    imagen = models.URLField()
    localidad = models.TextField(blank=False, max_length=50)
    direccion = models.TextField(blank=False, max_length=100)
    precioPorDia = models.DecimalField(max_digits=10, decimal_places=2, default=10)
    ocupadas= models.ManyToManyField(Alquiler, blank=True)

    def __str__(self):
        return self.titulo
