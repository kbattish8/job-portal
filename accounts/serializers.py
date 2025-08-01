from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.models import Group
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User


# ---------------------- SIGNUP SERIALIZER ----------------------
class SignUpSerializer(serializers.ModelSerializer):
    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name', 'role', 'access', 'refresh']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password')
        role = validated_data.pop('role', None)

        # Create user
        user = User.objects.create_user(password=password, **validated_data)

        # Assign role & group
        if role:
            user.role = role
            group, _ = Group.objects.get_or_create(name=role)
            user.groups.add(group)
        user.save()

        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        self._tokens = {
            "access": str(refresh.access_token),
            "refresh": str(refresh),
        }

        return user

    def to_representation(self, instance):
        """Add tokens to the response after user creation."""
        data = super().to_representation(instance)
        data.update(self._tokens)
        return data


# ---------------------- LOGIN SERIALIZER ----------------------
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            raise serializers.ValidationError("Both username and password are required.")

        user = authenticate(username=username, password=password)
        if not user:
            raise serializers.ValidationError("Invalid username or password.")
        if not user.is_active:
            raise serializers.ValidationError("User account is disabled.")

        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        data['access'] = str(refresh.access_token)
        data['refresh'] = str(refresh)
        data['user'] = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'full_name': user.get_full_name(),
            'role': user.role
        }
        return data
