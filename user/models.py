from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    class Roles(models.TextChoices):
        ADMIN = "admin", "Administrator"
        USER = "user", "User"

    class Genre(models.IntegerChoices):
        MALE = 0, "Male"
        FEMALE = 1, "Female"
        OTHER = 2, "Other"

    class Status(models.IntegerChoices):
        ACTIVATE = 1, "Activated"
        DEACTIVATE = 0, "Deactivated"

    role = models.CharField(max_length=20, choices=Roles.choices, default=Roles.USER)
    genre = models.IntegerField(choices=Genre.choices, null=True, blank=True)
    age = models.PositiveIntegerField(null=True, blank=True)
    phone_number = models.CharField(max_length=12)
    email = models.EmailField(unique=True)
    shower_per_week = models.IntegerField(default=5)
    time_per_shower = models.DurationField(default="00:10:00") 
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=Status.choices, default=Status.ACTIVATE)
    fingerprint = models.CharField(max_length=254)
    fingerprint = models.CharField(max_length=254)

    # Evita conflictos con los nombres de `AbstractUser`
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_groups',
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions',
        blank=True
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    def set_fingerprint(self, fingerprint):
        """Método para encriptar la huella dactilar"""
        from django.contrib.auth.hashers import make_password
        self.fingerprint = make_password(fingerprint)

    def set_password(self, password):
        """Método para encriptar la huella dactilar"""
        from django.contrib.auth.hashers import make_password
        self.password = make_password(password)

    def save(self, *args, **kwargs):
        if not self.pk:  # Si es un usuario nuevo
            self.set_password(self.password)
            self.set_fingerprint(self.fingerprint)
        super().save(*args, **kwargs)
