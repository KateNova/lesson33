from django.conf import settings
from django.core.management import BaseCommand
from django.contrib.sites.models import Site

from bot.models import TgUser
from bot.tg.client import TgClient
from bot.tg.dc import Message
from django.utils import timezone
from goals.models import (
    Goal,
    GoalCategory,
    BoardParticipant
)


class Command(BaseCommand):
    help = 'Запускает бота'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tg_client = TgClient(
            settings.TG_TOKEN
        )

    def handle_user_without_verification(self, msg: Message, tg_user: TgUser):
        tg_user.set_verification_code()
        tg_user.save()
        self.tg_client.send_message(
            msg.chat.id,
            f'Код верификации: {tg_user.verification_code}'
        )

    def get_goals(self, msg: Message, tg_user: TgUser):
        qs = Goal.objects.filter(user=tg_user.user)
        if qs.count() > 0:
            resp_msg = [
                f'№{item.id} - {item.title}'
                for item
                in qs
            ]
            self.tg_client.send_message(
                msg.chat.id,
                '\n'.join(resp_msg)
            )
        else:
            self.tg_client.send_message(
                msg.chat.id,
                'Список целей пуст'
            )

    def create_goal(self, msg: Message, tg_user: TgUser):
        goal = Goal.objects.create(
            title=msg.text,
            due_date=timezone.now(),
            user=tg_user.user,
            category=tg_user.current_category
        )
        if goal.id:
            current_site = Site.objects.get_current()
            message_link = current_site.domain + goal.get_absolute_url()
            self.tg_client.send_message(
                msg.chat.id,
                f'Цель добавлена успешно! Ссылка на цель:'
                f'{message_link}'
            )
        else:
            self.tg_client.send_message(
                msg.chat.id,
                'Произошла ошибка при добавлении цели! '
                'Начните процесс заново.'
            )

    def get_categories(self, tg_user: TgUser):
        return GoalCategory.objects.filter(
            board__participants__role__in=(
                BoardParticipant.Role.owner,
                BoardParticipant.Role.writer
            ),
            board__participants__user=tg_user.user,
            is_deleted=False,
        )

    def set_category(self, msg: Message, tg_user: TgUser):
        cat = GoalCategory.objects.filter(
            title=msg.text,
            board__participants__role__in=(
                BoardParticipant.Role.owner,
                BoardParticipant.Role.writer
            ),
            board__participants__user=tg_user.user,
            is_deleted=False,
        ).first()
        if cat:
            tg_user.current_category = cat
            tg_user.save()
            return True
        return False

    def handle_verified_user(self, msg: Message, tg_user: TgUser):
        if not msg.text:
            return
        if '/goals' in msg.text and tg_user.stage == 0:
            self.get_goals(msg, tg_user)
        elif '/create' in msg.text and tg_user.stage == 0:
            cat_str = ', '.join(
                [
                    x.title
                    for x
                    in self.get_categories(tg_user=tg_user)
                ]
            )
            self.tg_client.send_message(
                msg.chat.id,
                f'Пожалуйста выберете категорию: {cat_str}'
            )
            tg_user.stage = 1
            tg_user.save()
        elif tg_user.stage == 1:
            cat_result = self.set_category(msg, tg_user)
            if cat_result:
                self.tg_client.send_message(
                    msg.chat.id,
                    'Пожалуйста введите заголовок'
                )
                tg_user.stage = 2
                tg_user.save()
            else:
                self.tg_client.send_message(
                    msg.chat.id,
                    'Пожалуйста выберете верную категорию'
                )
        elif tg_user.stage == 2:
            self.create_goal(msg, tg_user)
            tg_user.stage = 0
            tg_user.save()
        else:
            self.tg_client.send_message(
                msg.chat.id,
                'Неизвестная команда'
            )

    def handle_message(self, msg: Message):
        tg_user, created = TgUser.objects.get_or_create(
            tg_id=msg.from_.id,
            defaults={
                'chat_id': msg.chat.id,
                'user_ud': msg.from_.username,
            },
        )
        if created:
            self.tg_client.send_message(
                msg.chat.id,
                'Привет дорогой друг!'
            )
        if tg_user.user:
            self.handle_verified_user(msg, tg_user)
        else:
            self.handle_user_without_verification(msg, tg_user)

    def handle(self, *args, **kwargs):
        offset = 0
        while True:
            res = self.tg_client.get_updates(offset=offset)
            for item in res.result:
                offset = item.update_id + 1
                self.handle_message(item.message)
