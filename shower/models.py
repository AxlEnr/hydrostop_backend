from django.db import models

# Create your models here.
class Shower(models.Model):
    showerCode = models.CharField( verbose_name="Name of the de shower", unique=True, max_length=30)
    
    #Choices from status, only 0 or 1
    class StatusChoices(models.IntegerChoices):
        On = 1, "Shower On"
        Off = 0, "Shower Off"

    status = models.IntegerField(choices=StatusChoices)
    
    class ShowerChoices(models.IntegerChoices):
        Available = 1, "Shower available"
        Unavailable = 0, "Shower unavailable"

    available = models.IntegerField(choices=ShowerChoices)


