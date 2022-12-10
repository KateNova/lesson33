from django.contrib.auth import get_user_model
from django.db import transaction
from rest_framework import serializers

from .models import (
    GoalCategory,
    Goal,
    GoalComment,
    Board,
    BoardParticipant
)
from core.serializers import UserSerializer


User = get_user_model()


class GoalCategoryCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    def validate_board(self, value):
        if value.is_deleted:
            raise serializers.ValidationError(
                'Запрещено для удаленной доски'
            )
        if not BoardParticipant.objects.filter(
            board=value,
            role__in=[
                BoardParticipant.Role.owner,
                BoardParticipant.Role.writer
            ],
            user=self.context['request'].user,
        ).exists():
            raise serializers.ValidationError(
                'Вы должны быть владельцем или иметь права на запись на указанной доске'
            )
        return value

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
            'user',
            'board',
        )


class GoalCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    def validate_category(self, value):
        if value.is_deleted:
            raise serializers.ValidationError(
                'Запрещено для удаленной категории'
            )
        if not BoardParticipant.objects.filter(
                board_id=value.board_id,
                role__in=[
                    BoardParticipant.Role.owner,
                    BoardParticipant.Role.writer
                ],
                user=self.context['request'].user,
        ).exists():
            raise serializers.ValidationError(
                'Вы должны быть владельцем или иметь права на запись на доске категории'
            )
        return value

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
        if not BoardParticipant.objects.filter(
                board_id=value.category.board_id,
                role__in=[
                    BoardParticipant.Role.owner,
                    BoardParticipant.Role.writer
                ],
                user=self.context['request'].user,
        ).exists():
            raise serializers.ValidationError(
                'Вы должны быть владельцем или иметь права на запись на доске категории'
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


class BoardCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    def create(self, validated_data):
        user = validated_data.pop('user')
        board = Board.objects.create(**validated_data)
        BoardParticipant.objects.create(
            user=user,
            board=board,
            role=BoardParticipant.Role.owner
        )
        return board

    class Meta:
        model = Board
        read_only_fields = (
            'id',
            'created',
            'updated'
        )
        fields = '__all__'


class BoardParticipantSerializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(
        required=True,
        choices=BoardParticipant.Role.choices
    )
    user = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all()
    )

    class Meta:
        model = BoardParticipant
        fields = '__all__'
        read_only_fields = (
            'id',
            'created',
            'updated',
            'board'
        )


class BoardSerializer(serializers.ModelSerializer):
    participants = BoardParticipantSerializer(many=True)
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    def update(self, instance, validated_data):
        owner = validated_data.pop('user')
        new_participants = validated_data.pop('participants')
        new_by_id = {
            party['user'].id: party
            for party
            in new_participants
        }
        old_participants = instance.participants.exclude(user=owner)
        with transaction.atomic():
            for old_party in old_participants:
                if old_party.user_id not in new_by_id:
                    old_party.delete()
                else:
                    if (
                            old_party.role
                            != new_by_id[old_party.user_id]['role']
                    ):
                        old_party.role = new_by_id[old_party.user_id]['role']
                        old_party.save()
                    new_by_id.pop(old_party.user_id)
            for new_party in new_by_id.values():
                BoardParticipant.objects.create(
                    board=instance,
                    user=new_party['user'],
                    role=new_party['role']
                )
            instance.title = validated_data['title']
            instance.save()
        return instance

    class Meta:
        model = Board
        fields = '__all__'
        read_only_fields = (
            'id',
            'created',
            'updated'
        )


class BoardListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = '__all__'
