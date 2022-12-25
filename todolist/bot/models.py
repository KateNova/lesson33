import random

from django.contrib.auth import get_user_model
from django.db import models

from goals.models import GoalCategory


CHARS = (
    'abcdefghijklmnopqrstuvwxyz'
    'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    '0123456789'
)

User = get_user_model()


class TgUser(models.Model):
    class Stage(models.IntegerChoices):
        zero = 0, 'Создание не запрашивалось'
        category = 1, 'Запрос категории'
        title = 2, 'Запрос заголовка'

    chat_id = models.BigIntegerField(
        verbose_name='ID чата Telegram'
    )
    user_ud = models.CharField(
        max_length=512,
        verbose_name='Пользователь Telegram',
        null=True,
        blank=True,
        default=None
    )
    user = models.ForeignKey(
        User,
        models.PROTECT,
        null=True,
        blank=True,
        default=None,
        verbose_name='Пользователь в системе',
    )
    verification_code = models.CharField(
        max_length=32,
        verbose_name='Код подтверждения'
    )
    stage = models.PositiveSmallIntegerField(
        verbose_name='Статус',
        choices=Stage.choices,
        default=Stage.zero
    )
    current_category = models.ForeignKey(
        GoalCategory,
        null=True,
        blank=True,
        default=None,
        on_delete=models.PROTECT,
        verbose_name='Категория',
    )

    def set_verification_code(self):
        self.verification_code = ''.join(
            [
                random.choice(CHARS)
                for _
                in range(8)
            ]
        )

    class Meta:
        verbose_name = 'Пользователь Telegram'
        verbose_name_plural = 'Пользователи Telegram'
