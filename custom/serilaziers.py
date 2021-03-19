from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from .models import CustomUser
from .utils import send_activation_mail


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('password', 'first_name', 'last_name', 'email',
                  'is_staff', 'is_active', 'date_joined')
        read_only_fields = ('is_staff', 'is_superuser', 'is_active', 'date_joined', 'is_confirmed')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser(**validated_data)
        user.set_password(validated_data['password'])
        user.save()

        send_activation_mail(user)

        return user


class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True, max_length=100)


class TokenSerializer(serializers.Serializer):
    token = serializers.CharField(required=True, max_length=400)


class PasswordResetSerializer(serializers.Serializer):
    """
    Serializer for password reset endpoint.
    """
    token = serializers.CharField(required=True, max_length=400)
    password = serializers.CharField(required=True)


class ChangePasswordSerializer(serializers.Serializer):
    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_new_password(self, value):
        validate_password(value)
        return value
