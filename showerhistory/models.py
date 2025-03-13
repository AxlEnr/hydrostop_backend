from django.db import models
from user.models import User
from shower.models import Shower 

# Create your models here.
class ShowerHistory(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    shower_id = models.ForeignKey(Shower, on_delete=models.CASCADE)
    showerStarted = models.DateTimeField(verbose_name="When the shower has started")
    showerFinished = models.DateTimeField(verbose_name="When the shower has finished")

    
