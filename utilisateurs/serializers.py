from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
User = get_user_model()

class ClassicRegisterUserSerializer(serializers.ModelSerializer):
    # on force le mot de passe à être en écriture seule pour des raisons de sécurité
    full_name = serializers.CharField(write_only=True, required=True, min_length=2)
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    confirm_password = serializers.CharField(write_only=True, required=True)
    class Meta:
        model = User
        fields = ['full_name', 'username', 'email', 'password', 'confirm_password', 'phone_number', 'is_teacher', 'is_premium_subscriber']

    def validate_email(self, value):
        email_clean = value.lower().strip()
        if User.objects.filter(email=email_clean).exists():
            raise serializers.ValidationError("Cet email est déjà utilisé.")
        return email_clean

    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError("Les mots de passe ne correspondent pas.")
        return attrs

    def create(self, validated_data):
        # On retire le confirm_password des données validées car il n'est pas nécessaire pour la création de l'utilisateur
        validated_data.pop('confirm_password', None)
        # utilisation de create_user pour hacher automatiquement le mot de passe en base de données
        full_name = validated_data.pop('full_name')
        username = validated_data.get('username', None)
        password = validated_data.pop('password')
        email = validated_data['email']

        name_parts = full_name.strip().split(' ', 1)
        first_name = name_parts[0]
        last_name = name_parts[1] if len(name_parts) > 1 else ''

        user = User.objects.create(
            username=username if username else email,
            email=email,
            first_name=first_name,
            last_name=last_name
        )
        user.set_password(password)
        user.save()
        return user
    
class LoginSerializer(serializers.Serializer):
    login_id = serializers.CharField(
        required=True, 
        help_text="Peut être l'adresse email ou le nom d'utilisateur."
    )
    password = serializers.CharField(
        write_only=True, 
        required=True,
        style={'input_type': 'password'}
    )
class GoogleAuthSerializer(serializers.Serializer):
    """Reçoit le token Google envoyé par le frontend"""
    id_token = serializers.CharField(required=True)