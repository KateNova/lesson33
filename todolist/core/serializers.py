from django.contrib.auth import (
    get_user_model,
)
from django.contrib.auth.password_validation import validate_password

from rest_framework import serializers
from rest_framework.exceptions import ValidationError


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'id'
            'username',
            'first_name',
            'last_name',
            'email'
        )
        read_only_fields = (
            'id',
        )


class SignUpSerializer(UserSerializer):
    user = None
    password = serializers.CharField(
        write_only=True,
        validators=(
            validate_password,
        )
    )
    password_repeat = serializers.CharField(
        write_only=True,
        validators=(
            validate_password,
        )
    )

    def create(self, validated_data):
        user = User.objects.create_user(
            **validated_data
        )
        self.user = user
        return user

    def validate(self, data):
        password = data.get(
            'password',
            None
        )
        password_repeat = data.pop(
            'password_repeat',
            None
        )
        if not (password and password_repeat) or password != password_repeat:
            raise ValidationError(
                'Введенные пароли не совпадают'
            )
        return data


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)


class PasswordUpdateSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(
        write_only=True,
        validators=(
            validate_password,
        )
    )
    new_password = serializers.CharField(
        write_only=True,
        validators=(
            validate_password,
        )
    )

    class Meta:
        model = User
        read_only_fields = (
            'id',
        )
        fields = (
            'id',
            'old_password',
            'new_password'
        )

    def validate(self, data):
        old_password = data.get("old_password")
        user = self.instance
        if not user.check_password(old_password):
            raise ValidationError(
                {
                    'old_password': 'Введенный пароль не соответсвует старому'
                }
            )
        return data

    def update(self, instance, validated_data):
        instance.set_password(
            validated_data['new_password']
        )
        instance.save(
            update_fields=('password', )
        )
        return instance
