from django.db import transaction
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveUpdateDestroyAPIView
)
from rest_framework import (
    permissions,
    filters,
)
from rest_framework.pagination import LimitOffsetPagination

from .filters import GoalDateFilter
from .models import (
    GoalCategory,
    Goal,
    GoalComment,
    Board,
    Status
)
from .permissions import (
    GoalCommentPermission,
    BoardPermission,
    GoalPermission,
    GoalCategoryPermission,
)
from .serializers import (
    GoalCategoryCreateSerializer,
    GoalCategorySerializer,
    GoalSerializer,
    GoalCreateSerializer,
    GoalCommentSerializer,
    GoalCommentCreateSerializer,
    BoardCreateSerializer,
    BoardSerializer,
    BoardListSerializer,
)


class GoalCategoryCreateView(CreateAPIView):
    model = GoalCategory
    permission_classes = (
        permissions.IsAuthenticated,
    )
    serializer_class = GoalCategoryCreateSerializer


class GoalCategoryListView(ListAPIView):
    model = GoalCategory
    permission_classes = (
        permissions.IsAuthenticated,
    )
    serializer_class = GoalCategorySerializer
    pagination_class = LimitOffsetPagination
    filter_backends = (
        DjangoFilterBackend,
        filters.OrderingFilter,
        filters.SearchFilter,
    )
    filterset_fields = (
        'board',
        'user'
    )
    ordering_fields = (
        'title',
        'created'
    )
    ordering = (
        'title',
    )
    search_fields = (
        'title',
    )

    def get_queryset(self):
        return GoalCategory.objects.filter(
            board__participants__user=self.request.user,
            is_deleted=False
        )


class GoalCategoryView(RetrieveUpdateDestroyAPIView):
    model = GoalCategory
    serializer_class = GoalCategorySerializer
    permission_classes = (
        permissions.IsAuthenticated,
        GoalCategoryPermission,
    )

    def get_queryset(self):
        return GoalCategory.objects.filter(
            board__participants__user=self.request.user,
            is_deleted=False
        )

    def perform_destroy(self, instance):
        with transaction.atomic():
            instance.is_deleted = True
            instance.save()
            goals = Goal.objects.filter(category=instance)
            for goal in goals:
                goal.is_deleted = True
                goal.status = Status.archived
                goal.save()
        return instance


class GoalCreateView(CreateAPIView):
    model = Goal
    permission_classes = (
        permissions.IsAuthenticated,
    )
    serializer_class = GoalCreateSerializer


class GoalListView(ListAPIView):
    model = Goal
    permission_classes = (
        permissions.IsAuthenticated,
    )
    serializer_class = GoalSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = (
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    )
    filterset_class = GoalDateFilter
    ordering_fields = (
        'title',
        'created'
    )
    search_fields = (
        'title',
        'description',
    )

    def get_queryset(self):
        return Goal.objects.filter(
            category__board__participants__user=self.request.user
        )


class GoalView(RetrieveUpdateDestroyAPIView):
    model = Goal
    serializer_class = GoalSerializer
    permission_classes = (
        permissions.IsAuthenticated,
        GoalPermission,
    )

    def get_queryset(self):
        return Goal.objects.filter(
            category__board__participants__user=self.request.user
        )

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.status = Status.archived
        instance.save()
        return instance


class GoalCommentCreateView(CreateAPIView):
    model = GoalComment
    serializer_class = GoalCommentCreateSerializer
    permission_classes = (
        permissions.IsAuthenticated,
    )


class GoalCommentView(RetrieveUpdateDestroyAPIView):
    model = GoalComment
    serializer_class = GoalCommentSerializer
    permission_classes = (
        permissions.IsAuthenticated,
        GoalCommentPermission
    )

    def get_queryset(self):
        return GoalComment.objects.filter(
            goal__category__board__participants__user=self.request.user
        )


class GoalCommentListView(ListAPIView):
    model = GoalComment
    serializer_class = GoalCommentSerializer
    permission_classes = (
        permissions.IsAuthenticated,
    )
    pagination_class = LimitOffsetPagination
    filter_backends = (
        DjangoFilterBackend,
        filters.OrderingFilter,
    )
    filterset_fields = (
        'goal',
    )
    ordering = '-created'

    def get_queryset(self):
        return GoalComment.objects.filter(
            goal__category__board__participants__user=self.request.user
        )


class BoardCreateView(CreateAPIView):
    model = Board
    permission_classes = (
        permissions.IsAuthenticated,
    )
    serializer_class = BoardCreateSerializer


class BoardView(RetrieveUpdateDestroyAPIView):
    model = Board
    permission_classes = (
        permissions.IsAuthenticated,
        BoardPermission,
    )
    serializer_class = BoardSerializer

    def get_queryset(self):
        return Board.objects.filter(
            participants__user=self.request.user,
            is_deleted=False
        )

    def perform_destroy(self, instance: Board):
        with transaction.atomic():
            instance.is_deleted = True
            instance.save()
            instance.categories.update(is_deleted=True)
            Goal.objects.filter(
                category__board=instance
            ).update(
                status=Status.archived
            )
        return instance


class BoardListView(ListAPIView):
    model = Board
    permission_classes = (
        permissions.IsAuthenticated,
    )
    pagination_class = LimitOffsetPagination
    serializer_class = BoardListSerializer
    filter_backends = (
        filters.OrderingFilter,
    )
    ordering = (
        'title',
    )

    def get_queryset(self):
        return Board.objects.filter(
            participants__user=self.request.user,
            is_deleted=False
        )
