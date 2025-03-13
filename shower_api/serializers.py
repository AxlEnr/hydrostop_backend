from rest_framework import serializers
from shower.models import Shower

class ShowerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shower
        fields = '__all__'