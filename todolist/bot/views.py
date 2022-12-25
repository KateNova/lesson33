from django.conf import settings
from rest_framework import permissions
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from .models import TgUser
from .serializers import TgUserSerializer
from .tg.client import TgClient


class VerificationView(GenericAPIView):
    model = TgUser
    permission_classes = (
        permissions.IsAuthenticated,
    )
    serializer_class = TgUserSerializer

    def patch(self, request, *args, **kwargs):
        serializer: TgUserSerializer = self.get_serializer(
            data=request.data
        )
        serializer.is_valid(raise_exception=True)
        tg_user: TgUser = serializer.validated_data['tg_user']
        tg_user.user = self.request.user
        tg_user.save()
        instance_s: TgUserSerializer = self.get_serializer(tg_user)
        tg_client = TgClient(
            token=settings.TG_TOKEN
        )
        tg_client.send_message(
            tg_user.chat_id,
            'Верификационный код принят!'
        )
        return Response(instance_s.data)
