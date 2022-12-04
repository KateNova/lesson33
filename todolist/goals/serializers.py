from rest_framework import serializers

from .models import (
    GoalCategory,
    Goal
)
from core.serializers import UserSerializer


class GoalCategoryCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = GoalCategory
        read_only_fields = (
            'id',
            'created',
            'updated',
            'user'
        )
        fields = '__all__'


class GoalCategorySerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = GoalCategory
        fields = '__all__'
        read_only_fields = (
            'id',
            'created',
            'updated',
            'user'
        )


class GoalCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Goal
        read_only_fields = (
            'id',
            'created',
            'updated',
            'user'
        )
        fields = '__all__'


class GoalSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Goal
        fields = '__all__'
        read_only_fields = (
            'id',
            'created',
            'updated',
            'user'
        )
