from django.contrib import admin

from .models import (
    GoalCategory,
    Goal,
    GoalComment,
    Board,
    BoardParticipant
)


admin.site.register(Board)
admin.site.register(BoardParticipant)


@admin.register(GoalCategory)
class GoalCategoryAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'user',
        'created',
        'updated'
    )
    search_fields = (
        'title',
        'user'
    )


@admin.register(Goal)
class GoalAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'user',
        'created',
        'updated'
    )
    search_fields = (
        'title',
        'user'
    )


@admin.register(GoalComment)
class GoalCommentAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'goal',
        'created',
        'updated'
    )
