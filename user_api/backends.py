from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model

User = get_user_model()

class EmailBackend(BaseBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        print("Intentando autenticar con el backend personalizado")  # Depuración
        try:
            user = User.objects.get(email=email)
            print(f"Usuario encontrado: {user.email}")  # Depuración
            if user.check_password(password):
                print("Contraseña correcta")  # Depuración
                return user
        except User.DoesNotExist:
            print("Usuario no encontrado")  # Depuración
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None