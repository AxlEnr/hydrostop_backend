from django.db import models
from django.utils import timezone
from user.models import User
from shower.models import Shower

class ShowerHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='shower_histories', null=True, blank=True)
    shower = models.ForeignKey(Shower, on_delete=models.CASCADE, related_name='histories', null=True, blank=True)
    start_time = models.DateTimeField(auto_now_add=True, verbose_name="Hora de inicio", null=True, blank=True)  # Solo auto_now_add
    end_time = models.DateTimeField(null=True, blank=True, verbose_name="Hora de fin")
    duration_seconds = models.IntegerField(default=0, verbose_name="Duración en segundos")
    completed = models.BooleanField(default=False, verbose_name="¿Se completó el ciclo?")

    class Meta:
        verbose_name = "Historial de Regadera"
        verbose_name_plural = "Historial de Regaderas"
        ordering = ['-start_time']

    def save(self, *args, **kwargs):
        if self.end_time and self.start_time:
            delta = self.end_time - self.start_time
            self.duration_seconds = delta.total_seconds()
        super().save(*args, **kwargs)
