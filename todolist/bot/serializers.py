from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import TgUser


class TgUserSerializer(serializers.ModelSerializer):
    verification_code = serializers.CharField(
        write_only=True
    )

    class Meta:
        model = TgUser
        read_only_fields = (
            'chat_id',
            'user_ud',
            'user_id'
        )
        fields = (
            'chat_id',
            'user_ud',
            'verification_code',
            'user_id'
        )

    def validate(self, attrs):
        verification_code = attrs.get('verification_code')
        tg_user = TgUser.objects.filter(
            verification_code=verification_code
        ).first()
        if not tg_user:
            raise ValidationError(
                {
                    'verification_code': 'Неверное значение'
                }
            )
        attrs['tg_user'] = tg_user
        return attrs
