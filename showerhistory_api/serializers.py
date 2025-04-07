from rest_framework import serializers
from showerhistory.models import ShowerHistory

class ShowerHistorySerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.first_name', read_only=True)
    shower_name = serializers.CharField(source='shower.name', read_only=True)
    
    class Meta:
        model = ShowerHistory
        fields = ['id', 'user', 'user_name', 'shower', 'shower_name', 
                 'start_time', 'end_time', 'duration_seconds', 'completed']
        read_only_fields = ['start_time', 'duration_seconds']