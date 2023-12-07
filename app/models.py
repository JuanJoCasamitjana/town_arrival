from django.db import models
from users.models import Profile, Alquiler, User

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
    
class Comentario(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    casa = models.ForeignKey(Casa, on_delete=models.CASCADE)
    texto = models.TextField(max_length=500)
    fecha_publicacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comentario de {self.usuario.username} en {self.casa.titulo}"
    
    
class Reclamacion(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    casa = models.ForeignKey(Casa, on_delete=models.CASCADE)
    texto = models.TextField(max_length=500)
    pretensiones = models.TextField(max_length=500)
    fecha_publicacion = models.DateTimeField(auto_now_add=True)
    ESTADO = (('PENDIENTE', 'pendiente'), ('PROCESADA', 'procesada'), ('DESECHADA', 'desechada'))
    estado = models.CharField(max_length=20, choices=ESTADO, default='PENDIENTE')
    contestacion = models.CharField(max_length=300, default="Sin respuesta")

    def __str__(self):
        return f"Reclamacion de {self.usuario.username} en {self.casa.titulo}"