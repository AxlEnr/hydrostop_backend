# models.py
from django.db import models
from user.models import User

class Shower(models.Model):
    name = models.CharField(verbose_name="Name of the shower", unique=True, max_length=30)
    ip_address = models.CharField(default="192.168.0.67", max_length=100)
    last_user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    
    class StatusChoices(models.IntegerChoices):
        On = 1, "Shower On"
        Off = 0, "Shower Off"

    class GenderChoices(models.IntegerChoices):
        Male = 0, "Male"
        Female = 1, "Female"
        Unisex = 2, "Unisex"

    gender = models.CharField(choices=GenderChoices.choices, default="Unisex")
    status = models.IntegerField(choices=StatusChoices.choices, default=StatusChoices.Off)
    
    class ShowerChoices(models.IntegerChoices):
        Available = 1, "Shower available"
        Unavailable = 0, "Shower unavailable"

    available = models.IntegerField(choices=ShowerChoices.choices, default=ShowerChoices.Available)

    class TimeChoices(models.IntegerChoices):
        test = 10, "10 segundos (prueba)"
        test3 = 30, "30 segundos (prueba)"
        test4 = 60, "60 segundos (prueba)"
        minimo = 300, "5 minutos"
        medio = 480, "8 minutos"
        recomendado = 600, "10 minutos"
        maximo = 900, "15 minutos"
        test2 = 15, "15 segundos (prueba)"
        
    time = models.IntegerField(choices=TimeChoices.choices, default=TimeChoices.recomendado)
    alert_time = models.IntegerField(default=2, verbose_name="Tiempo de alerta antes de cerrar (segundos)")