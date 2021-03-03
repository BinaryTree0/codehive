from rest_framework import serializers

from .models import CustomUser
from .utils import send_activation_mail


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('password', 'first_name', 'last_name', 'email', 'company',
                  'is_staff', 'is_active', 'date_joined')
        read_only_fields = ('is_staff', 'is_superuser', 'is_active', 'date_joined',)
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
    token = serializers.CharField(required=True, max_length=400)
    password = serializers.CharField(required=True, write_only=True)
