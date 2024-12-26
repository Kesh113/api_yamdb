from django.contrib.auth import get_user_model
from rest_framework import serializers

from .constants import ME_FORBIDDEN


User = get_user_model()


class UserSignupSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    username = serializers.CharField(max_length=150, required=True)


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'username')

    def validate_username(self, value):
        if value.lower() == 'me':
            raise serializers.ValidationError(ME_FORBIDDEN)
        return value


class UserConfirmationSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150, required=True)


class UserBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )

    def validate_username(self, value):
        if value.lower() == 'me':
            raise serializers.ValidationError(ME_FORBIDDEN)
        return value


class UserProfileSerializer(UserBaseSerializer):
    def update(self, instance, validated_data):
        validated_data.pop('role', None)
        return super().update(instance, validated_data)


class UsersSerializer(UserBaseSerializer):
    pass
