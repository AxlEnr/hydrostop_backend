from rest_framework.response import Response
from rest_framework.decorators import api_view
from showerhistory.models import ShowerHistory
from .serializers import ShowerHistorySerializers
from django.shortcuts import get_object_or_404
from rest_framework import status

@api_view(['GET'])
def get_all_histories(request):
    shower_history = ShowerHistory.objects.all()
    serializer = ShowerHistorySerializers(shower_history, many=True)

    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
def create_history(request):
    serializer = ShowerHistorySerializers(data = request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
        
@api_view(['PUT'])
def update_history(request, shower_history_id):
    shower_history = get_object_or_404(ShowerHistory, id = shower_history_id)
    serializer = ShowerHistorySerializers(shower_history, data = request.data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def delete_history(request, shower_history_id):
    shower_history = get_object_or_404(ShowerHistory, id = shower_history_id)
    serializer = ShowerHistorySerializers(shower_history, data = request.data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)