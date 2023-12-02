from django.db import models
from django.contrib.auth.models import User

from app.models import Casa

class Reclamacion(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    casa = models.ForeignKey(Casa, on_delete=models.CASCADE)
    motivo = models.TextField()
    pretensiones = models.TextField()
    informacion_adicional = models.TextField()
    