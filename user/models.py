from django.db import models
from django.contrib.auth.hashers import make_password

# Create your models here.
class User(models.Model):
    class Roles(models.TextChoices):
        admin = "admin", "Administrator"
        user = "user", "User"

    class Genre(models.IntegerChoices):
        male = 0, "Male"
        female = 1, "Female"
        other = 2, "Other"

    class Status(models.IntegerChoices):
        activate = 1, "Activated"
        deactivate = 0, "Deactivated"

    role = models.CharField(max_length=20, choices=Roles.choices)
    name = models.CharField(max_length=30)
    firstName = models.CharField(max_length=30)
    genre = models.IntegerField(choices=Genre.choices, null=True)
    age = models.PositiveBigIntegerField()
    phoneNumber = models.CharField(max_length=12)
    email = models.EmailField(null=True)
    showerPerWeek = models.IntegerField()
    timePerShower = models.TimeField()
    createdAt = models.DateField()
    status = models.IntegerField(choices=Status.choices)
    fingerPrint = models.CharField(max_length=254)
    password = models.CharField(max_length=254, default="1234")

    def save(self, *args, **kwargs):
        if (self.password and not self.password.startswith('pbkdf2_')) and (self.fingerPrint and not self.fingerPrint.startswith('pbkdf2_')):
            self.password = make_password(self.password)
            self.fingerPrint = make_password(self.fingerPrint)
        super().save(*args, **kwargs)



