from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from showerhistory.models import ShowerHistory
from .serializers import ShowerHistorySerializer
from django.shortcuts import get_object_or_404
from rest_framework import status
from django.utils import timezone
from user.models import User
from shower.models import Shower

@api_view(['POST'])
def start_shower_session(request):
    try:
        shower_id = request.data.get('shower_id')
        duration = request.data.get('duration')

        # Validaciones
        if not shower_id:
            return Response({'error': 'shower_id es requerido'}, status=status.HTTP_400_BAD_REQUEST)
        if duration is None or not str(duration).isdigit():
            return Response({'error': 'Duración inválida'}, status=status.HTTP_400_BAD_REQUEST)

        duration = int(duration)  # Convertir a entero
        if duration <= 0:
            return Response({'error': 'Duración debe ser mayor a 0'}, status=status.HTTP_400_BAD_REQUEST)

        # Obtener el usuario autenticado
        user = request.user
        if user.is_anonymous:
            return Response({'error': 'Usuario no autenticado'}, status=status.HTTP_401_UNAUTHORIZED)

        user = User.objects.get(pk=user.pk)  # Convertir a una instancia real

        # Verificar si la regadera existe
        try:
            shower = Shower.objects.get(id=shower_id)
        except Shower.DoesNotExist:
            return Response({'error': 'La regadera no existe'}, status=status.HTTP_404_NOT_FOUND)

        # Calcular tiempos
        start_time = timezone.now()
        end_time = start_time + timezone.timedelta(seconds=duration)

        # Crear el historial
        history = ShowerHistory.objects.create(
            user=user,
            shower=shower,
            start_time=start_time,
            end_time=end_time,
            duration_seconds=duration,
            completed=True
        )

        serializer = ShowerHistorySerializer(history)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def end_shower_session(request, history_id):
    try:
        history = ShowerHistory.objects.get(id=history_id)
        
        # Obtener la duración del cuerpo de la solicitud
        duration_seconds = request.data.get('duration', 0)
        
        if duration_seconds > 0:
            # Calcular end_time sumando la duración al start_time
            history.end_time = history.start_time + timezone.timedelta(seconds=duration_seconds)
            history.duration_seconds = duration_seconds
            history.completed = True
            history.save()
            
            serializer = ShowerHistorySerializer(history)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Duración inválida'}, status=status.HTTP_400_BAD_REQUEST)
            
    except ShowerHistory.DoesNotExist:
        return Response({'error': 'Historial no encontrado'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

from datetime import timedelta

@api_view(['PUT'])
def end_shower_history(request, history_id):
    try:
        from django.utils import timezone
        history = ShowerHistory.objects.get(id=history_id)
        
        # Obtén la duración del cuerpo de la solicitud
        duration = int(request.data.get('duration', 0))
        
        # Calcula end_time basado en start_time + duration
        history.end_time = history.start_time + timedelta(seconds=duration)
        history.duration_seconds = duration
        history.save()
        
        return Response({
            'status': 'success',
            'message': 'Historial actualizado correctamente',
            'data': {
                'history_id': history.id,
                'shower_id': history.shower.id,
                'start_time': history.start_time,
                'end_time': history.end_time,
                'duration': duration
            }
        }, status=status.HTTP_200_OK)
        
    except ShowerHistory.DoesNotExist:
        return Response(
            {"status": "error", "message": "Historial no encontrado"},
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response(
            {"status": "error", "message": str(e)},
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['GET'])
def get_user_shower_history(request):
    histories = ShowerHistory.objects.filter(user=request.user).order_by('-start_time')
    serializer = ShowerHistorySerializer(histories, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_histories(request):
    histories = ShowerHistory.objects.all()
    serializer = ShowerHistorySerializer(histories, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
