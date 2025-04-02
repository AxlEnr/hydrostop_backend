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
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

# POST USERS (Signup)
@api_view(['POST'])
def signup(request):
    serializer = UserSerializer(data=request.data)

    if serializer.is_valid():
        user = serializer.save()
        user.set_password(serializer.validated_data['password'])  # Encripta la contraseña
        user.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  # Devuelve errores correctos

# UPDATE DATA USERS
@api_view(['PUT'])
def update_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    serializer = UserSerializer(user, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# DEACTIVATE USER
@api_view(['PUT'])
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.is_active = False  # Desactiva al usuario en lugar de modificar datos
    user.save()
    return Response({'message': 'Usuario desactivado'}, status=status.HTTP_200_OK)

# views.py
class LoginView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return Response({'error': 'Email and password are required'}, 
                          status=status.HTTP_400_BAD_REQUEST)

        # Usa el backend personalizado
        user = authenticate(request, username=email, password=password)
        
        if not user:
            return Response({'error': 'Invalid credentials'}, 
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
