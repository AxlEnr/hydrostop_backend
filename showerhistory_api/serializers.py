from rest_framework import serializers
from showerhistory.models import ShowerHistory

class ShowerHistorySerializers(serializers.ModelSerializer):
    class Meta:
        model = ShowerHistory
        fields = '__all__'