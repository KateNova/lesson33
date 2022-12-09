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
    Goal, GoalComment
)
from .permissions import CommentPermission
from .serializers import (
    GoalCategoryCreateSerializer,
    GoalCategorySerializer,
    GoalSerializer,
    GoalCreateSerializer, GoalCommentSerializer, GoalCommentCreateSerializer,
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
        filters.OrderingFilter,
        filters.SearchFilter,
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
            user=self.request.user,
            is_deleted=False
        )


class GoalCategoryView(RetrieveUpdateDestroyAPIView):
    model = GoalCategory
    serializer_class = GoalCategorySerializer
    permission_classes = (
        permissions.IsAuthenticated,
    )

    def get_queryset(self):
        return GoalCategory.objects.filter(
            user=self.request.user,
            is_deleted=False
        )

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save()
        goals = Goal.objects.filter(category=instance)
        for goal in goals:
            goal.is_deleted = True
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
            user=self.request.user,
            is_deleted=False,
        )


class GoalView(RetrieveUpdateDestroyAPIView):
    model = Goal
    serializer_class = GoalSerializer
    permission_classes = (
        permissions.IsAuthenticated,
    )

    def get_queryset(self):
        return Goal.objects.filter(
            user=self.request.user,
            is_deleted=False,
        )

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save()
        return instance


class CommentCreateView(CreateAPIView):
    model = GoalComment
    serializer_class = GoalCommentCreateSerializer
    permission_classes = (
        permissions.IsAuthenticated,
    )


class CommentView(RetrieveUpdateDestroyAPIView):
    model = GoalComment
    serializer_class = GoalCommentSerializer
    permission_classes = (
        permissions.IsAuthenticated,
        CommentPermission
    )

    def get_queryset(self):
        return GoalComment.objects.filter(
            goal__user=self.request.user
        )


class CommentListView(ListAPIView):
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
            goal__user=self.request.user
        )
