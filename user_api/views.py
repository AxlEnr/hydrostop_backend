from rest_framework.response import Response
from rest_framework.decorators import api_view
from user.models import User
from .serializers import UserSerializer
from django.shortcuts import get_object_or_404
from rest_framework import status

#GET ALL USERS
@api_view(['GET'])
def get_all_users(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)

    return Response(serializer.data, status=status.HTTP_200_OK)

#POST USERS
@api_view(['POST'])
def signup(request):
    serializer = UserSerializer(data = request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

#UPDATE DATA USERS
@api_view(['PUT'])
def update_user(request, user_id):
    user = get_object_or_404(User, id = user_id)
    serializer = UserSerializer(user, data = request.data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

#DEACTIVATE USER
@api_view(['PUT'])
def delete_user(request, user_id):
    user = get_object_or_404(User, id = user_id)
    serializer = UserSerializer(user, data = request.data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)