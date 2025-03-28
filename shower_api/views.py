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

#Get times
@api_view(['GET'])
def get_timer(request, shower_id):
    try:
        shower = Shower.objects.get(id=shower_id)
        serializer = ShowerSerializer(shower)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Shower.DoesNotExist:
        return Response(
            {"error": f"Ducha con id {shower_id} no encontrada"},
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response(
            {"error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
def get_shower_config(request, shower_id):
    try:
        shower = Shower.objects.get(id=shower_id)
        serializer = ShowerSerializer(shower)
        return Response({
            'id_shower': shower.id,
            'shower_time': shower.time,
            'alert_time': shower.alert_time,
            'status': shower.status,
            'available': shower.available
        }, status=status.HTTP_200_OK)
    except Shower.DoesNotExist:
        return Response(
            {"error": f"Ducha con id {shower_id} no encontrada"},
            status=status.HTTP_404_NOT_FOUND
        )

@api_view(['PUT'])
def update_shower_config(request, shower_id):
    shower = get_object_or_404(Shower, id=shower_id)
    
    try:
        shower.time = request.data.get('shower_time', shower.time)
        shower.alert_time = request.data.get('alert_time', shower.alert_time)
        shower.save()
        
        return Response({
            'message': 'Configuración actualizada correctamente',
            'shower_time': shower.time,
            'alert_time': shower.alert_time
        }, status=status.HTTP_200_OK)
    except Exception as e:
        return Response(
            {"error": str(e)},
            status=status.HTTP_400_BAD_REQUEST
        )