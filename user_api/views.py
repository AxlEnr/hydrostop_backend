from rest_framework.response import Response
from rest_framework.decorators import api_view
from user.models import User
from .serializers import UserSerializer
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny


# GET ALL USERS
@api_view(['GET'])
def get_all_users(request):
    users = User.objects.exclude(role="admin").filter(status=1)
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

#GET USER
@api_view(['GET'])
def get_user(request):
    try:
        user = User.objects.get(id=request.user.id)
        return Response({
            'user': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'phone_number': user.phone_number,
            'age': user.age,
        }, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

# POST USERS (Signup)
@api_view(['POST'])
def signup(request):
    serializer = UserSerializer(data=request.data)

    if serializer.is_valid():
        user = serializer.save()
        user.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# UPDATE DATA USERS
@api_view(['PUT'])
def update_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    serializer = UserSerializer(user, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    print(serializer.errors)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# views.py
class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return Response({'error': 'Email and password are required'}, 
                            status=status.HTTP_400_BAD_REQUEST)

        # Verifica si el usuario existe antes de autenticar
        try:
            user = User.objects.get(email=email)
            if user.status == 0:  # Si el status es 0, el usuario está bloqueado
                return Response({'error': 'Tu cuenta ha sido bloqueda por el administrador'}, 
                                status=status.HTTP_403_FORBIDDEN)
        except User.DoesNotExist:
            return Response({'error': 'Email o Contraseña inválidas'}, 
                            status=status.HTTP_401_UNAUTHORIZED)

        # Usa el backend de autenticación
        user = authenticate(request, username=email, password=password)
        
        if not user:
            return Response({'error': 'Email o Contraseña inválidas'}, 
                            status=status.HTTP_401_UNAUTHORIZED)

        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': UserSerializer(user).data
        }, status=status.HTTP_200_OK)


@api_view(['PUT'])
def change_password(request):
    user = request.user
    old_password = request.data.get('old_password')
    new_password = request.data.get('new_password')
    
    if not user.check_password(old_password):
        return Response({'error': 'Wrong password'}, 
                      status=status.HTTP_400_BAD_REQUEST)
    
    user.set_password(new_password)
    user.save()
    return Response({'message': 'Password updated successfully'}, 
                  status=status.HTTP_200_OK)

@api_view(['PUT'])
def delete_user(request, user_id):
    try:
        user = get_object_or_404(User, id=user_id)
        
        # Verificar si el usuario que hace la solicitud es admin
        if not request.user.role == "admin":
            return Response(
                {'error': 'Solo administradores pueden realizar esta acción'}, 
                status=status.HTTP_403_FORBIDDEN
            )
    
        user.status = 0
        user.save()
        
        return Response(
            {'message': 'Usuario desactivado exitosamente'}, 
            status=status.HTTP_200_OK
        )
        
    except Exception as e:
        return Response(
            {'error': str(e)}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


from django.core.mail import send_mail
from django.conf import settings
import random
import string
from twilio.rest import Client
import logging

logger = logging.getLogger(__name__)

@api_view(['POST'])
def request_password_reset(request):
    email = request.data.get('email')
    
    if not email:
        return Response(
            {'error': 'El correo electrónico es requerido'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response(
            {'error': 'No existe un usuario con este correo electrónico'}, 
            status=status.HTTP_404_NOT_FOUND
        )
    
    if not user.phone_number:
        return Response(
            {'error': 'El usuario no tiene un número de teléfono registrado'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Generar contraseña temporal
    temp_password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
    
    try:
        phone = user.phone_number
        if not user.phone_number.startswith("+"):
            phone = "+52" + user.phone_number
            
        # Actualizar contraseña del usuario primero
        user.set_password(temp_password)
        user.save()
        
        # Verificar configuración de Twilio
        if not all([settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN, settings.TWILIO_PHONE_NUMBER]):
            raise ValueError("Configuración de Twilio incompleta")

        
        # Enviar SMS con Twilio
        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        
        message = client.messages.create(
            body=f"Tu contraseña temporal es: {temp_password}. Por favor cámbiala después de iniciar sesión.",
            from_=settings.TWILIO_PHONE_NUMBER,
            to=phone
        )
        
        logger.info(f"SMS enviado a {user.phone_number}. SID: {message.sid}")
        
        return Response(
            {'message': f'Se ha enviado una contraseña temporal al número registrado'}, 
            status=status.HTTP_200_OK
        )
        
    except TwilioRestException as e:
        logger.error(f"Error de Twilio: {str(e)}")
        # Revertir el cambio de contraseña
        user.set_password(None)
        user.save()
        return Response(
            {'error': 'Error al enviar el SMS. Por favor intenta más tarde.'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
        
    except Exception as e:
        logger.error(f"Error inesperado: {str(e)}")
        # Revertir el cambio de contraseña si hubo otro error
        user.set_password(None)
        user.save()
        return Response(
            {'error': 'Ocurrió un error inesperado. Por favor contacta al administrador.'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['PUT'])
def activate_user(request, user_id):
    try:
        user = get_object_or_404(User, id=user_id)
        
        # Verificar si el usuario que hace la solicitud es admin
        if not request.user.role == "admin":
            return Response(
                {'error': 'Solo administradores pueden realizar esta acción'}, 
                status=status.HTTP_403_FORBIDDEN
            )
    
        user.status = 1
        user.save()
        
        return Response(
            {'message': 'Usuario activado exitosamente'}, 
            status=status.HTTP_200_OK
        )
        
    except Exception as e:
        return Response(
            {'error': str(e)}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
def get_all_users_a(request):
    users = User.objects.exclude(role="admin").filter(status=0)
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
