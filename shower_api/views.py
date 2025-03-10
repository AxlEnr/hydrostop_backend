from rest_framework.response import Response
from rest_framework.decorators import api_view
from shower.models import Shower
from .serializers import ShowerSerializer
from django.shortcuts import get_object_or_404
from rest_framework import status

#GET ALL SHOWERS
@api_view(['GET'])
def get_all_showers(request):
    showers = Shower.objects.all()
    serializer = ShowerSerializer(showers, many=True)

    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
def create_showers(request):
    serializer = ShowerSerializer(data = request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def update_showers(request, shower_id):
    shower = get_object_or_404(Shower, id = shower_id)
    serializer = ShowerSerializer(shower, data = request.data, partial = True)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def delete_showers(request, shower_id):
    shower = get_object_or_404(Shower, id = shower_id)
    serializer = ShowerSerializer(shower, data = request.data, partial = True)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
