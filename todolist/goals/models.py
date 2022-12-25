from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone


User = get_user_model()


class Status(models.IntegerChoices):
    to_do = 1, 'К выполнению'
    in_progress = 2, 'В процессе'
    done = 3, 'Выполнено'
    archived = 4, 'Архив'


class Priority(models.IntegerChoices):
    low = 1, 'Низкий'
    medium = 2, 'Средний'
    high = 3, 'Высокий'
    critical = 4, 'Критический'


class DatesModelMixin(models.Model):
    class Meta:
        abstract = True

    created = models.DateTimeField(
        verbose_name='Дата создания'
    )
    updated = models.DateTimeField(
        verbose_name='Дата последнего обновления'
    )

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = timezone.now()
        self.updated = timezone.now()
        return super().save(*args, **kwargs)


class GoalCategory(DatesModelMixin):
    title = models.CharField(
        verbose_name='Название',
        max_length=255
    )
    user = models.ForeignKey(
        User,
        verbose_name='Автор',
        on_delete=models.PROTECT
    )
    is_deleted = models.BooleanField(
        verbose_name='Удалена',
        default=False
    )
    board = models.ForeignKey(
        'Board',
        verbose_name='Доска',
        on_delete=models.PROTECT,
        related_name='categories',
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Goal(DatesModelMixin):
    title = models.CharField(
        verbose_name='Название',
        max_length=255
    )
    description = models.TextField(
        verbose_name='Описание',
        blank=True,
        null=True,
        max_length=255
    )
    due_date = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name='Дата последнего обновления'
    )
    user = models.ForeignKey(
        User,
        verbose_name='Автор',
        on_delete=models.PROTECT
    )
    status = models.PositiveSmallIntegerField(
        verbose_name='Статус',
        choices=Status.choices,
        default=Status.to_do
    )
    priority = models.PositiveSmallIntegerField(
        verbose_name='Приоритет',
        choices=Priority.choices,
        default=Priority.medium
    )
    category = models.ForeignKey(
        GoalCategory,
        verbose_name='Категория',
        on_delete=models.PROTECT
    )
    is_deleted = models.BooleanField(
        verbose_name='Удалена',
        default=False
    )

    def get_absolute_url(self):
        return (
            f'/boards/{self.category.board.pk}/'
            f'goals?goal={self.pk}'
        )

    class Meta:
        verbose_name = 'Цель'
        verbose_name_plural = 'Цели'


class GoalComment(DatesModelMixin):
    user = models.ForeignKey(
        User,
        verbose_name='Автор',
        related_name='goal_comments',
        on_delete=models.PROTECT,
    )
    goal = models.ForeignKey(
        Goal,
        verbose_name='Цель',
        related_name='goal_comments',
        on_delete=models.PROTECT,
    )
    text = models.TextField(
        verbose_name='Текст'
    )

    class Meta:
        verbose_name = 'Комментарий к цели'
        verbose_name_plural = 'Комментарии к целям'


class Board(DatesModelMixin):
    title = models.CharField(
        verbose_name='Название',
        max_length=255
    )
    is_deleted = models.BooleanField(
        verbose_name='Удалена',
        default=False
    )

    class Meta:
        verbose_name = 'Доска'
        verbose_name_plural = 'Доски'


class BoardParticipant(DatesModelMixin):
    class Role(models.IntegerChoices):
        owner = 1, 'Владелец'
        writer = 2, 'Редактор'
        reader = 3, 'Читатель'

    board = models.ForeignKey(
        Board,
        verbose_name='Доска',
        on_delete=models.PROTECT,
        related_name='participants',
    )
    user = models.ForeignKey(
        User,
        verbose_name='Пользователь',
        on_delete=models.PROTECT,
        related_name='participants',
    )
    role = models.PositiveSmallIntegerField(
        verbose_name='Роль',
        choices=Role.choices,
        default=Role.owner
    )

    class Meta:
        unique_together = (
            'board',
            'user'
        )
        verbose_name = 'Участник'
        verbose_name_plural = 'Участники'
