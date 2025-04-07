from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.hashers import make_password
from datetime import timedelta
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings


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

    # Campos personalizados
    role = models.CharField(max_length=20, choices=Roles.choices, default=Roles.USER)
    genre = models.IntegerField(choices=Genre.choices, null=True, blank=True)
    age = models.PositiveIntegerField(null=True, blank=True)
    phone_number = models.CharField(max_length=12)
    email = models.EmailField(unique=True)
    shower_per_week = models.IntegerField(default=5)
    time_per_shower = models.DurationField(default=timedelta(minutes=10))
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    status = models.IntegerField(choices=Status.choices, default=Status.ACTIVATE)
 
    # Configuración para evitar conflictos
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_groups',
        blank=True,
        verbose_name='groups',
        help_text='The groups this user belongs to.'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions',
        blank=True,
        verbose_name='user permissions',
        help_text='Specific permissions for this user.'
    )

    

    # Configuración de autenticación
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    def get_creator_admin(self):
        """Retorna el admin que creó este usuario"""
        if self.created_by and self.created_by.role == "admin":
            return self.created_by
        return None

    def __str__(self):
        return self.get_full_name() or self.email

    def get_full_name(self):
        """Devuelve el nombre completo del usuario."""
        return f"{self.first_name} {self.last_name}".strip()

    def set_fingerprint(self, fingerprint):
        """Encripta y guarda la huella dactilar."""
        self.fingerprint = make_password(fingerprint)

    def save(self, *args, **kwargs):
        self.email = self.email.lower()
        if self.username:
            self.username = self.username.lower()
        
        # Si time_per_shower es un string, convertirlo a timedelta
        if isinstance(self.time_per_shower, str):
            try:
                hours, minutes, seconds = map(int, self.time_per_shower.split(':'))
                self.time_per_shower = timedelta(
                    hours=hours, 
                    minutes=minutes, 
                    seconds=seconds
                )
            except (ValueError, AttributeError):
                raise ValueError("Formato inválido para time_per_shower. Use HH:MM:SS")
        
        super().save(*args, **kwargs)