from django.contrib.auth import get_user_model
from django.utils import timezone

import factory

from goals.models import (
    GoalCategory,
    Goal,
    GoalComment,
    Board,
    BoardParticipant
)


User = get_user_model()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    first_name = factory.Faker('name')
    username = factory.Faker('name')
    email = factory.Faker('email')


class GoalCategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = GoalCategory

    title = 'test'


class GoalFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Goal

    title = 'test'
    due_date = timezone.now()
    description = 'test'
    user = factory.SubFactory(UserFactory)


class GoalCommentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = GoalComment

    text = 'test'
    goal = factory.SubFactory(GoalFactory)
    user = factory.SubFactory(UserFactory)


class BoardFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Board

    title = 'test'
