from rest_framework import serializers
from user.models import User

class UserSerializer(serializers.ModelSerializer):
    time_per_shower = serializers.CharField(required=False)

    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'first_name', 'last_name', 
                 'age', 'phone_number', 'genre', 'shower_per_week', 
                 'time_per_shower', 'role', 'password']
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'required': True}
        }

    def validate_time_per_shower(self, value):
        """Convierte el string HH:MM:SS a timedelta."""
        if isinstance(value, str):
            try:
                hours, minutes, seconds = map(int, value.split(':'))
                return timedelta(hours=hours, minutes=minutes, seconds=seconds)
            except (ValueError, AttributeError):
                raise serializers.ValidationError(
                    "Formato inválido. Use HH:MM:SS"
                )
        return value

    def get_role(self, obj):
        return "admin" if obj.is_superuser else "user" 

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists")
        return value

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user