from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class RegisterUserSerializer(serializers.ModelSerializer):
    # on force le mot de passe à être en écriture seule pour des raisons de sécurité
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'phone_number', 'is_teacher', 'latitude', 'longitude', 'is_premium_subscriber']

    def create(self, validated_data):
        # utilisation de create_user pour hacher automatiquement le mot de passe en base de données
        user = User.objects.create_user(
            username = validated_data['username'],
            email = validated_data.get('email', ''),
            password = validated_data.pop('password'),
            phone_number = validated_data.get('phone_number', ''),
            is_teacher = validated_data.get('is_teacher', False),
            latitude = validated_data.get('latitude', None),
            longitude = validated_data.get('longitude', None)
        )
        return user