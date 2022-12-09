from rest_framework import serializers

from .models import (
    GoalCategory,
    Goal, GoalComment
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


class GoalCommentCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    def validate_goal(self, value):
        if not Goal.objects.filter(
            id=value.id,
            user=self.context["request"].user,
        ).exists():
            raise serializers.ValidationError(
                'Вы должны быть автором цели которую комментируете'
            )
        return value

    class Meta:
        model = GoalComment
        fields = '__all__'
        read_only_fields = (
            'id',
            'created',
            'updated',
            'user'
        )



class GoalCommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = GoalComment
        fields = '__all__'
        read_only_fields = (
            'id',
            'created',
            'updated',
            'user',
            'goal'
        )
